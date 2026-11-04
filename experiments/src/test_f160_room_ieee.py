"""F160 (Sprint 29 Task E, #68): the room check and its positive control.

The rule has never passed on a recorded instance, so the first test shows
it can: random-sign learners leave room. The second shows it can fail.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
PHASE2 = ROOT / "experiments" / "phase2" / "src"
THIS = Path(__file__).relative_to(ROOT).as_posix()
sys.path.insert(0, str(PHASE2))

import f160_room_ieee as fr  # noqa: E402

N_ROWS = 2000


def _labels(rate: float, seed: int = 0) -> np.ndarray:
    y = -np.ones(N_ROWS)
    y[np.random.default_rng(seed).choice(N_ROWS, int(rate * N_ROWS),
                                         replace=False)] = 1
    return y


def _scip_returns(monkeypatch, objective):
    monkeypatch.setattr(fr.ec, "ScipSolver", lambda: None)
    monkeypatch.setattr(fr.ec, "exact_solver_control",
                        lambda J, C, m, solver, cap: {"objective": objective})


def test_best_found_is_the_lower_of_greedy_and_scip(monkeypatch):
    # F172: SCIP's value is taken only when it is lower, and only when it
    # has one.
    rng = np.random.default_rng(1)
    H, y = rng.choice([-1.0, 1.0], size=(8, 200)), _labels(0.1)[:200]
    g = fr.chosen(3, H, y, 1.0, scip=False)["greedy"]["objective"]
    _scip_returns(monkeypatch, g - 1.0)
    assert fr.chosen(3, H, y, 1.0, scip=True)["best_found"] == g - 1.0
    _scip_returns(monkeypatch, g + 1.0)
    assert fr.chosen(3, H, y, 1.0, scip=True)["best_found"] == g
    _scip_returns(monkeypatch, None)
    assert fr.chosen(3, H, y, 1.0, scip=True)["best_found"] == g


def test_random_sign_learners_leave_room():
    labels = {(42, "free"): (_labels(0.035), 60, 10)}
    res = fr.evaluate(fr.random_sign_instances(labels), scip=False)
    row = res["rows"][0]
    assert row["chosen"]["gap_greedy_to_floor"] > 0.5
    assert res["design_fails"] is False


def test_learners_that_say_legitimate_everywhere_leave_no_room():
    # Rare fraud and a pool of near-constant "legitimate" learners: the data
    # term is about 4 x fraud rate, below the rule's 0.01.
    y = _labels(0.0017)
    rng = np.random.default_rng(1)
    H = -np.ones((60, N_ROWS))
    H[rng.random(H.shape) < 0.0005] = 1.0
    res = fr.evaluate({(42, "free"): (H, y, 10)}, scip=False)
    assert res["rows"][0]["chosen"]["gap_greedy_to_floor"] < 0.01
    assert res["design_fails"] is True


def test_the_falsifier_reads_greedy_and_the_floor():
    rows = [{"chosen": {"greedy": {"objective": -0.5}, "floor": -0.8,
                        "f104_gate": {"pass": True},
                        "guide_check": {"pass": True}}}]
    out = fr.falsifier_rows(rows)[0]
    assert out["methods"]["greedy"]["objective"] == -0.5
    assert out["floor"] == -0.8


def test_the_falsifier_reads_both_resolution_checks():
    rows = [{"chosen": {"greedy": {"objective": -0.5}, "floor": -0.8,
                        "f104_gate": {"pass": False},
                        "guide_check": {"pass": False}}}]
    out = fr.falsifier_rows(rows)[0]
    assert out["f104_gate"] == {"pass": False}
    assert out["guide_check"] == {"pass": False}


def _control(gap, resolves):
    return {"rows": [{"chosen": {"greedy": {"objective": gap - 1.0},
                                 "floor": -1.0,
                                 "f104_gate": {"pass": resolves},
                                 "guide_check": {"pass": resolves}}}]}


def test_ieee_is_read_only_after_a_control_with_room():
    reads = []
    doc = {}
    fr.gate(doc, _control(0.0, True), lambda: reads.append(1) or {"x": 1})
    assert reads == [] and "no IEEE-CIS pool built" in doc["stopped"]
    doc = {}
    fr.gate(doc, _control(0.5, True), lambda: reads.append(1) or {"x": 1})
    assert reads == [1] and doc["ieee"] == {"x": 1}


def test_unresolvable_control_rows_do_not_stop_the_reading():
    # Room, but both resolution checks fail: the entry's gate is room alone.
    assert not fr.no_room(_control(0.5, False))
    assert fr.no_room(_control(0.0, True))


def test_a_refused_pool_is_recorded():
    meta = {(42, "free"): {"pool_size": 50, "refused": "pool has 50 "
                           "learners, instance needs 60"}}
    out = fr.read_instances({}, meta)
    assert out["refused"] == {"42/free": meta[(42, "free")]}
    assert out["design_fails"] is None


def test_the_best_found_minimum_can_fail():
    _fails("            best = min(best, sc[\"objective\"])\n",
           "            best = sc[\"objective\"]\n",
           "test_best_found_is_the_lower_of_greedy_and_scip",
           "a worse SCIP value taken as best found")
    _fails("        if sc.get(\"objective\") is not None:\n",
           "        if sc.get(\"objective\") is None:\n",
           "test_best_found_is_the_lower_of_greedy_and_scip",
           "SCIP's value ignored")


def test_the_order_gate_can_fail():
    _fails("    if no_room(control):\n", "    if not no_room(control):\n",
           "test_ieee_is_read_only_after_a_control_with_room",
           "IEEE-CIS read after a control with no room")


def test_the_room_only_gate_can_fail():
    _fails("    return all(r[\"methods\"][\"greedy\"][\"objective\"] - "
           "r[\"floor\"] < fd.GAP_MIN\n",
           "    return fd.design_fails(falsifier_rows(res[\"rows\"])) or all("
           "r[\"methods\"][\"greedy\"][\"objective\"] - r[\"floor\"] < fd.GAP_MIN\n",
           "test_unresolvable_control_rows_do_not_stop_the_reading",
           "the gate read as design_fails")


def test_the_resolution_passthrough_can_fail():
    _fails("             \"floor\": r[\"chosen\"][\"floor\"], \"f104_gate\": "
           "r[\"chosen\"][\"f104_gate\"],\n",
           "             \"floor\": r[\"chosen\"][\"floor\"], \"f104_gate\": "
           "{\"pass\": True},\n",
           "test_the_falsifier_reads_both_resolution_checks",
           "the F104 gate hardcoded to pass")


def _fails(old, new, node, label):
    from injection import Mutation, assert_can_fail, run_pytest
    assert_can_fail([Mutation(PHASE2 / "f160_room_ieee.py", old, new,
                              expect_occurrences=1)],
                    lambda: run_pytest(f"{THIS}::{node}", ROOT), label)


def test_the_room_reading_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    assert_can_fail(
        [Mutation(PHASE2 / "f160_room_ieee.py",
                  "    return [{\"methods\": {\"greedy\": {\"objective\": "
                  "r[\"chosen\"][\"greedy\"][\"objective\"]}},\n",
                  "    return [{\"methods\": {\"greedy\": {\"objective\": "
                  "r[\"chosen\"][\"floor\"]}},\n",
                  expect_occurrences=1)],
        lambda: run_pytest(f"{THIS}::test_random_sign_learners_leave_room",
                           ROOT),
        "greedy read as the floor")
