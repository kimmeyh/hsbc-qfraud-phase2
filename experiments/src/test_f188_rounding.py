"""F188 (Sprint 32 Task C): the rounding test's rule, each state and each
refusal, on small built problems. No data, no device. Each rule's term is
proven red below."""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import f188_rounding as fr  # noqa: E402

MODULE = ROOT / "experiments" / "phase2" / "src" / "f188_rounding.py"
THIS = Path(__file__).relative_to(ROOT).as_posix()


def test_rounding_uses_the_largest_coefficient_over_r():
    J = np.array([[2.0, 0.013], [0.013, 2.0]])
    C = np.array([-0.5, 0.004])
    Jq, Cq, step = fr.rounded(J, C, 200.0)
    assert step == pytest.approx(0.01)
    assert Jq[0, 1] == pytest.approx(0.01) and Cq[1] == 0.0
    assert Jq[0, 0] == pytest.approx(2.0) and Cq[0] == pytest.approx(-0.5)


def test_no_rounding_at_infinity():
    J, C = np.eye(2), np.array([0.1, 0.2])
    Jq, Cq, step = fr.rounded(J, C, math.inf)
    assert Jq is J and Cq is C and step == 0.0


def test_an_all_zero_problem_is_refused():
    with pytest.raises(ValueError, match="every coefficient is zero"):
        fr.rounded(np.zeros((2, 2)), np.zeros(2), 200.0)


# Two supports, {0} and {1}, differing by a small amount on the linear term.
J2 = np.eye(2) * 1.0
C2 = np.array([-0.40, -0.41])


def test_a_gain_is_kept_unrounded_and_lost_when_coarse():
    kept = fr.gain(J2, C2, math.inf, [0], {"other": [1]})
    assert kept["kept"] and kept["gain"] < -fr.TOL
    lost = fr.gain(J2, C2, 2.0, [0], {"other": [1]})
    assert not lost["kept"] and lost["step"] == pytest.approx(0.5)


def test_a_gain_inside_the_tolerance_is_not_kept():
    C = np.array([-0.40, -0.40 - 5e-7])     # a gain of 5e-7 < TOL (1e-6)
    g = fr.gain(J2, C, math.inf, [0], {"other": [1]})
    assert g["gain"] < 0 and not g["kept"]


def test_the_best_other_support_is_the_one_read():
    g = fr.gain(J2, C2, math.inf, [0], {"same": [0], "better": [1]})
    assert g["best_other"] == "better"


def _case(unrounded_kept: bool, coarse_kept: bool) -> dict:
    return {"unrounded": {"kept": unrounded_kept},
            "coarse": {"kept": coarse_kept}}


def test_can_fire_needs_every_case_kept_and_one_lost():
    assert fr.can_fire({"a": _case(True, False), "b": _case(True, True)})[
        "can_fire"]


def test_can_fire_is_false_with_no_case_lost():
    out = fr.can_fire({"a": _case(True, True)})
    assert not out["can_fire"] and out["lost_at_coarse_on"] == []


def test_can_fire_is_false_when_a_case_loses_its_gain_unrounded():
    assert not fr.can_fire({"a": _case(False, False)})["can_fire"]


def test_can_fire_is_false_with_no_cases():
    assert not fr.can_fire({})["can_fire"]


def _row(kept: bool) -> dict:
    return {"seed": 42, "instance": "free",
            "reading": {"kept_at_200": kept}}


def test_summary_states_all_lost():
    s = fr.summary([_row(False), _row(False)])
    assert s["all_lost_at_200"] and s["kept_at_200"] == []
    assert s["finding"].startswith("lost at R = 200 on every instance")


def test_summary_states_where_kept():
    s = fr.summary([_row(True), _row(False)])
    assert not s["all_lost_at_200"] and s["kept_at_200"] == ["42/free"]
    assert "stays open" in s["finding"]


def test_an_incomplete_f176_is_refused():
    with pytest.raises(RuntimeError, match="not complete"):
        fr.require_complete({"complete": False})
    fr.require_complete({"complete": True})


def test_a_different_greedy_is_refused():
    rec = {"seed": 42, "instance": "free",
           "methods": {"greedy": {"objective": -0.7}}}
    fr.require_same_greedy(rec, -0.7)
    with pytest.raises(RuntimeError, match="not F176's instance"):
        fr.require_same_greedy(rec, -0.7 + 1e-6)


def test_a_result_short_of_f176s_instances_is_refused():
    with pytest.raises(RuntimeError, match="not complete"):
        fr.final_doc({}, [_row(False)], 2)
    with pytest.raises(RuntimeError, match="not complete"):
        fr.final_doc({}, [], 0)
    assert fr.final_doc({}, [_row(False)], 1)["complete"] is True


def test_a_pick_that_beats_greedy_unrounded_delivers():
    d = fr.delivered(J2, C2, math.inf, [0], {"other": [1]})
    assert d["pick"] == "other" and d["delivers"]
    assert d["delivered_gain"] == pytest.approx(-0.01)


def test_a_pick_made_on_a_coarse_problem_can_fail_to_deliver():
    # At R = 2 both supports round to the same objective; the pick is the
    # first seen, greedy, which delivers nothing.
    d = fr.delivered(J2, C2, 2.0, [0], {"other": [1]})
    assert d["pick"] == "greedy" and not d["delivers"]


def test_the_pick_is_scored_on_the_unrounded_problem():
    # Unrounded, support 0 is better (0.70 against 0.74). At R = 2 the
    # step is 0.62: J rounds to 1.24 on both, C to 0 and -0.62, so the
    # rounded problem picks support 1, which delivers nothing.
    J = np.diag([1.0, 1.24])
    C = np.array([-0.3, -0.5])
    d = fr.delivered(J, C, 2.0, [0], {"other": [1]})
    assert d["pick"] == "other"
    assert d["greedy_unrounded_objective"] == pytest.approx(0.70)
    assert d["pick_unrounded_objective"] == pytest.approx(0.74)
    assert not d["delivers"] and d["delivered_gain"] == pytest.approx(0.04)


def test_a_short_delivered_result_is_refused():
    row = {"seed": 42, "instance": "free",
           "rounded": {"200": {"delivers": True}}}
    with pytest.raises(RuntimeError, match="not complete"):
        fr.delivered_doc([row], 2)
    with pytest.raises(RuntimeError, match="not complete"):
        fr.delivered_doc([], 0)
    doc = fr.delivered_doc([row], 1)
    assert doc["complete"] is True
    assert doc["summary"]["delivers_at_200"] == ["42/free"]


# ---------------------------------------- F200: the release rule as filed

def test_release_solves_greedy_on_the_rounded_problem():
    # The filed rule's difference from the delivered reading: greedy's
    # weights are solved on the rounded problem, like the pick's, and both
    # are scored on the unrounded one.
    # Two learners each, so the weights differ: at R = 3 greedy's {0, 1}
    # solves to (2/3, 1/3) on the rounded problem and to about (0.497,
    # 0.503) on the real one.
    J = np.array([[1.0, 0.3, 0.1], [0.3, 1.2, 0.2], [0.1, 0.2, 0.9]])
    C = np.array([-0.31, -0.52, -0.45])
    r = fr.release(J, C, 3.0, [0, 1], {"other": [1, 2]})
    Jq, Cq, _ = fr.rounded(J, C, 3.0)
    want = fr.ec.objective(J, C, fr.ec.solve_on_support(Jq, Cq, [0, 1]))
    assert r["greedy_objective"] == pytest.approx(want, abs=1e-9)
    old = fr.delivered(J, C, 3.0, [0, 1], {"other": [1, 2]})
    assert r["greedy_objective"] > old["greedy_unrounded_objective"] + 1e-4
    assert r["release_gain"] == pytest.approx(
        r["pick_objective"] - r["greedy_objective"])


def test_release_solves_the_pick_on_the_rounded_problem():
    # The pick's side of the filed comparison (PR #134 review): at R = 4
    # the pick is {1, 2}, not greedy; its weights solved on the rounded
    # problem are (0.4, 0.6), and on the real one they differ, so the two
    # objectives differ by about 0.0018.
    J = np.array([[1.0, 0.3, 0.1], [0.3, 1.2, 0.2], [0.1, 0.2, 0.9]])
    C = np.array([-0.31, -0.52, -0.45])
    r = fr.release(J, C, 4.0, [0, 1], {"other": [1, 2]})
    assert r["pick"] == "other"
    Jq, Cq, _ = fr.rounded(J, C, 4.0)
    want = fr.ec.objective(J, C, fr.ec.solve_on_support(Jq, Cq, [1, 2]))
    assert r["pick_objective"] == pytest.approx(want, abs=1e-9)
    real = fr.ec.objective(J, C, fr.ec.solve_on_support(J, C, [1, 2]))
    assert r["pick_objective"] > real + 1e-3


def test_a_pick_that_is_greedys_selection_gains_exactly_zero():
    r = fr.release(J2, C2, 2.0, [0], {"other": [1]})
    assert r["pick"] == "greedy"
    assert r["release_gain"] == 0.0 and not r["passes"]


def test_a_clear_gain_passes():
    r = fr.release(J2, C2, math.inf, [0], {"other": [1]})
    assert r["pick"] == "other" and r["passes"]


def test_a_gain_inside_the_tolerance_does_not_pass():
    C = np.array([-0.40, -0.40 - 5e-7])
    r = fr.release(J2, C, math.inf, [0], {"other": [1]})
    assert r["release_gain"] < 0 and not r["passes"]


def _rel(seed, pick, gain, passes=False):
    return {"seed": seed, "instance": "free",
            "release": {"pick": pick, "release_gain": gain, "passes": passes}}


def test_a_nonzero_gain_where_the_pick_is_greedy_is_refused():
    with pytest.raises(RuntimeError, match="not zero on"):
        fr.require_zero_where_greedy([_rel(42, "greedy", 1e-5)])
    assert fr.require_zero_where_greedy(
        [_rel(42, "greedy", 0.0), _rel(43, "scip", -1e-3)]) == ["42/free"]


def test_the_rule_is_met_on_one_passing_instance():
    v = fr.verdict([_rel(42, "scip", -1e-3, True), _rel(43, "greedy", 0.0)])
    assert v["rule_met"] and v["passes_on"] == ["42/free"]
    assert v["finding"].startswith("met")


def test_the_rule_is_not_met_with_no_passing_instance():
    v = fr.verdict([_rel(42, "scip", 1e-3), _rel(43, "greedy", 0.0)])
    assert not v["rule_met"] and v["passes_on"] == []
    assert "stays on HOLD" in v["finding"]


def test_a_short_release_result_is_refused():
    with pytest.raises(RuntimeError, match="not complete"):
        fr.release_doc([_rel(42, "greedy", 0.0)], 2, {})
    with pytest.raises(RuntimeError, match="not complete"):
        fr.release_doc([], 0, {})
    assert fr.release_doc([_rel(42, "greedy", 0.0)], 1, {})["complete"] is True


def test_each_release_term_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    for old, new, test, label in (
            ("    greedy_true = ec.objective(J, C, ec.solve_on_support(Jq, Cq, greedy_support))\n",
             "    greedy_true = support_objective(J, C, greedy_support)\n",
             "test_release_solves_greedy_on_the_rounded_problem",
             "greedy solved on the unrounded problem (the old reading)"),
            ("    pick_true = ec.objective(J, C, ec.solve_on_support(Jq, Cq, supports[pick]))\n",
             "    pick_true = ec.objective(J, C, ec.solve_on_support(J, C, supports[pick]))\n",
             "test_release_solves_the_pick_on_the_rounded_problem",
             "the pick solved on the unrounded problem"),
            ('"release_gain": d, "passes": bool(d < -TOL)}',
             '"release_gain": d, "passes": bool(d < 0)}',
             "test_a_gain_inside_the_tolerance_does_not_pass",
             "a gain inside the tolerance passes"),
            ('           if r["release"]["release_gain"] != 0.0]\n',
             "           if False]\n",
             "test_a_nonzero_gain_where_the_pick_is_greedy_is_refused",
             "the zero-gain check that cannot fire"),
            ('            "rule_met": bool(at),\n',
             '            "rule_met": len(at) == len(rows),\n',
             "test_the_rule_is_met_on_one_passing_instance",
             "every instance required, not one"),
            ("    if n_expected == 0 or len(rows) != n_expected:\n",
             "    if False:\n",
             "test_a_short_release_result_is_refused",
             "a short release result marked complete")):
        assert_can_fail([Mutation(MODULE, old, new, expect_occurrences=1)],
                        lambda test=test: run_pytest(f"{THIS}::{test}", ROOT),
                        label)


def test_an_unknown_argument_is_refused():
    import subprocess
    r = subprocess.run([sys.executable, str(MODULE), "--deliverd"],
                       capture_output=True, text=True, cwd=ROOT)
    assert r.returncode != 0 and "usage: f188_rounding.py" in r.stderr


# ------------------------------------------------------------- red proofs

def test_each_rule_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    for old, new, test, label in (
            ("    return np.round(J / step) * step, np.round(C / step) * step, step\n",
             "    return J, C, step\n",
             "test_a_gain_is_kept_unrounded_and_lost_when_coarse",
             "no rounding applied"),
            ("    if not step > 0:\n", "    if False:\n",
             "test_an_all_zero_problem_is_refused", "a zero step accepted"),
            ('"kept": bool(d < -TOL)}', '"kept": bool(d < 0)}',
             "test_a_gain_inside_the_tolerance_is_not_kept",
             "a gain inside the tolerance kept"),
            ("    best = min(objs, key=objs.get)\n",
             "    best = next(iter(objs))\n",
             "test_the_best_other_support_is_the_one_read",
             "the first support read, not the best"),
            ('"can_fire": bool(cases) and kept and bool(lost)}',
             '"can_fire": bool(lost)}',
             "test_can_fire_is_false_when_a_case_loses_its_gain_unrounded",
             "can fire without every gain kept unrounded"),
            ('"can_fire": bool(cases) and kept and bool(lost)}',
             '"can_fire": kept}',
             "test_can_fire_is_false_with_no_case_lost",
             "can fire with nothing lost"),
            ("            if r[\"reading\"][\"kept_at_200\"]]\n",
             "            if False]\n",
             "test_summary_states_where_kept", "kept instances not listed"),
            ('    if f176_doc.get("complete") is not True:\n',
             "    if False:\n",
             "test_an_incomplete_f176_is_refused", "an incomplete F176 read"),
            ("    if not abs(rebuilt - recorded) <= GREEDY_MATCH:\n",
             "    if False:\n",
             "test_a_different_greedy_is_refused", "another instance read"),
            ("    true_pick = ec.objective(J, C, w)\n",
             "    true_pick = ec.objective(Jq, Cq, w)\n",
             "test_the_pick_is_scored_on_the_unrounded_problem",
             "the pick scored on the rounded problem"),
            ('"delivers": bool(d < -TOL)}', '"delivers": bool(d <= 0)}',
             "test_a_pick_made_on_a_coarse_problem_can_fail_to_deliver",
             "no gain read as delivered"),
            ("    elif sys.argv[1:]:\n", "    elif False:\n",
             "test_an_unknown_argument_is_refused",
             "an unknown argument runs the first reading")):
        assert_can_fail([Mutation(MODULE, old, new, expect_occurrences=1)],
                        lambda test=test: run_pytest(f"{THIS}::{test}", ROOT),
                        label)
    # The two `complete` guards share their text; each is broken alone.
    guard = "    if len(rows) != n_expected or n_expected == 0:\n"
    text = MODULE.read_text(encoding="utf-8")
    assert text.count(guard) == 2
    first, second = text.index(guard), text.rindex(guard)
    # delivered_doc is defined before final_doc.
    for at, test in ((first, "test_a_short_delivered_result_is_refused"),
                     (second, "test_a_result_short_of_f176s_instances_is_refused")):
        broken = text[:at] + "    if False:\n" + text[at + len(guard):]
        assert_can_fail([Mutation(MODULE, text, broken, expect_occurrences=1)],
                        lambda test=test: run_pytest(f"{THIS}::{test}", ROOT),
                        "a short result marked complete")
