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
             "test_a_gain_is_kept_unrounded_and_lost_when_coarse",
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
            ("    if len(rows) != n_expected or n_expected == 0:\n",
             "    if False:\n",
             "test_a_result_short_of_f176s_instances_is_refused",
             "a short result marked complete")):
        assert_can_fail([Mutation(MODULE, old, new, expect_occurrences=1)],
                        lambda test=test: run_pytest(f"{THIS}::{test}", ROOT),
                        label)
