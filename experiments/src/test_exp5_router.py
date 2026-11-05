"""Experiment 5 (F121, Sprint 31 Task H, #100): the recall at the budget,
section 5's matched pair, the router criterion and the reference stop,
each term proven red.

No stored score is read here: every input is hand-built.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
PHASE2 = ROOT / "experiments" / "phase2" / "src"
SRC = PHASE2 / "exp5_router.py"
THIS = Path(__file__).relative_to(ROOT).as_posix()
sys.path.insert(0, str(PHASE2))

import exp5_router as e5  # noqa: E402


def test_recall_flags_the_top_half_percent_within_the_rows():
    # 1,000 rows: ceil(5) = 5 flagged. Positives at rows 0-3 and 999.
    y = np.zeros(1000, dtype=int)
    y[[0, 1, 2, 3, 999]] = 1
    s = np.zeros(1000)
    s[[0, 1, 2, 999]] = 1.0          # 4 positives scored high
    s[500] = 0.9                     # one negative above the rest
    idx = np.arange(1000)
    assert e5.recall_at_budget(y, s, idx) == 4 / 5
    # 201 rows: ceil(1.005) = 2 flagged, not 1.
    sub = np.arange(201)
    assert e5.recall_at_budget(y, s, sub) == 2 / 4


def test_the_pair_is_downsized_to_the_complement():
    big = e5.matched_pair(900, 100, 800, 50_000)
    assert (big["positives"], big["negatives"], big["downsized"]) == (
        800, 89, True)
    small = e5.matched_pair(50, 950, 3_000, 80_000)
    assert (small["positives"], small["negatives"], small["downsized"]) == (
        50, 950, False)
    assert small["feasible"] is True
    assert e5.matched_pair(50, 950, 3_000, 900)["feasible"] is False


def _seeds(edges, controls):
    return [{"seed": 42 + i, "edge": e, "control_edge": c}
            for i, (e, c) in enumerate(zip(edges, controls))]


def test_acceptance_needs_one_point_and_an_interval_above_zero():
    up = [0.02 + 0.001 * i for i in range(10)]
    assert e5.accept(_seeds(up, [0.0] * 10))["accepted"] is True
    # The interval clears zero, but the mean edge is under one point.
    low = [0.008 + 0.0001 * i for i in range(10)]
    assert e5.accept(_seeds(low, [0.0] * 10))["accepted"] is False
    # One point of edge, but the control gives as much: not accepted.
    assert e5.accept(_seeds(up, up))["accepted"] is False
    # Noisy around the control: the interval crosses zero.
    noisy = [0.02 + (0.03 if i % 2 else -0.03) for i in range(10)]
    assert e5.accept(_seeds(noisy, [0.02] * 10))["accepted"] is False
    r = e5.accept(_seeds(up, [0.0] * 10))
    assert abs(r["level"] - (1 - 0.05 / 5)) < 1e-12


def test_an_accepted_reference_blocks_the_proxy():
    ref = {"W": {"criterion": {"accepted": False}},
           "C": {"criterion": {"accepted": True}}}
    assert e5.blocked_by_reference(ref) == ["C"]
    assert e5.blocked_by_reference(
        {"W": {"criterion": {"accepted": False}}}) == []


def test_the_rules_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest

    def test(name):
        return lambda: run_pytest(f"{THIS}::{name}", ROOT)
    assert_can_fail([Mutation(SRC, "    k = math.ceil(BUDGET * len(idx))\n",
                              "    k = int(BUDGET * len(idx))\n",
                              expect_occurrences=1)],
                    test("test_recall_flags_the_top_half_percent_within_"
                         "the_rows"),
                    "the budget rounded down")
    assert_can_fail([Mutation(SRC, "    p = min(seg_pos, comp_pos)\n",
                              "    p = seg_pos\n", expect_occurrences=1)],
                    test("test_the_pair_is_downsized_to_the_complement"),
                    "a pair the complement cannot supply")
    assert_can_fail([Mutation(SRC,
                              "            \"feasible\": p > 0 and n <= "
                              "comp_neg and n <= seg_neg,\n",
                              "            \"feasible\": p > 0,\n",
                              expect_occurrences=1)],
                    test("test_the_pair_is_downsized_to_the_complement"),
                    "an infeasible pair drawn")
    assert_can_fail([Mutation(SRC, "    ok = bool(e.mean() >= MIN_EDGE and "
                                   "lo > 0)\n",
                              "    ok = bool(lo > 0)\n",
                              expect_occurrences=1)],
                    test("test_acceptance_needs_one_point_and_an_interval_"
                         "above_zero"),
                    "acceptance without one point of recall")
    assert_can_fail([Mutation(SRC, "    ok = bool(e.mean() >= MIN_EDGE and "
                                   "lo > 0)\n",
                              "    ok = bool(e.mean() >= MIN_EDGE)\n",
                              expect_occurrences=1)],
                    test("test_acceptance_needs_one_point_and_an_interval_"
                         "above_zero"),
                    "acceptance without the control")
    assert_can_fail([Mutation(SRC, "ALPHA = 0.05 / len(SEGMENTS)\n",
                              "ALPHA = 0.05\n", expect_occurrences=1)],
                    test("test_acceptance_needs_one_point_and_an_interval_"
                         "above_zero"),
                    "no Bonferroni correction")
    assert_can_fail([Mutation(SRC,
                              "    return [s for s, v in reference.items() "
                              "if v[\"criterion\"][\"accepted\"]]\n",
                              "    return []\n", expect_occurrences=1)],
                    test("test_an_accepted_reference_blocks_the_proxy"),
                    "the reference check ignored")
