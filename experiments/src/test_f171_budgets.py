"""F171 amendment (Sprint 30 Task H, #82; Decision D7): the budgets, the
count, the capacity floor and the recorded-count check, each proven red.
Synthetic scores only.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
PHASE2 = ROOT / "experiments" / "phase2" / "src"
THIS = Path(__file__).relative_to(ROOT).as_posix()
sys.path.insert(0, str(PHASE2))

import f171_budgets as fb  # noqa: E402


def test_the_matched_budget_is_three_times_the_folds_fraud_rate():
    y = np.r_[np.ones(5), np.zeros(95)]
    b = fb.budgets(y)
    assert b["recorded_0.5"] == 0.005 and b["fixed_3.5"] == 0.035
    assert abs(b["matched"] - 0.15) < 1e-12


def test_the_count_and_its_capacity_floor():
    # 100 rows, 10 frauds; a 2% budget gives each family 2 alerts.
    y = np.r_[np.ones(10), np.zeros(90)]
    a = np.r_[np.arange(10, 0, -1), np.zeros(90)] / 10   # ranks frauds 0, 1
    b = np.r_[np.zeros(2), np.arange(8, 0, -1) / 8, np.zeros(90)]  # 2, 3
    c = fb.count(y, [a, b], 0.02)
    assert c["alerts_per_family"] == 2 and c["frauds"] == 10
    assert c["missed_by_all"] == 6 and c["capacity_floor"] == 6


def test_a_recomputed_count_that_differs_stops_the_run():
    fb.check_recorded("x", {"missed": 3, "frauds": 10}, (3, 10))
    with pytest.raises(ValueError, match="not the recorded"):
        fb.check_recorded("x", {"missed": 4, "frauds": 10}, (3, 10))


def test_the_rules_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    src = PHASE2 / "f171_budgets.py"

    def test(name):
        return lambda: run_pytest(f"{THIS}::{name}", ROOT)
    assert_can_fail([Mutation(src, "            \"matched\": min(1.0, RATIO * "
                              "float(np.mean(np.asarray(y) == 1)))}\n",
                              "            \"matched\": min(1.0, RATIO * 0.005)}\n",
                              expect_occurrences=1)],
                    test("test_the_matched_budget_is_three_times_the_folds_"
                         "fraud_rate"), "the matched budget not from the fold")
    assert_can_fail([Mutation(src, "            \"capacity_floor\": max(0, "
                              "frauds - len(scores) * k)}\n",
                              "            \"capacity_floor\": max(0, "
                              "frauds - k)}\n", expect_occurrences=1)],
                    test("test_the_count_and_its_capacity_floor"),
                    "the floor counted for one family")
    assert_can_fail([Mutation(src, "    if (got[\"missed\"], got[\"frauds\"]) "
                              "!= tuple(want):\n", "    if False:\n",
                              expect_occurrences=1)],
                    test("test_a_recomputed_count_that_differs_stops_the_run"),
                    "a differing 0.5% count accepted")
