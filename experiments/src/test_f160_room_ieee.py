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
