"""F113's oracle, budget and verdict are computed the way the plan stated.

Sprint 25 Task D. The falsifier (an oracle gap under 1 point of recall at the
0.5% budget rules a router out) was written into the plan before the run.
These guards use synthetic scores: zero metered, no dataset, nothing written
to an evidence directory.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))

import oracle_gap as og     # noqa: E402


def test_budget_and_criterion_are_the_ones_stated_in_the_plan():
    assert og.ALERT_BUDGET == 0.005
    assert og.ROUTER_CRITERION == 0.01


def test_recall_flags_exactly_the_budget():
    y = np.zeros(1000, dtype=int)
    y[[0, 1, 2, 3]] = 1
    s = np.zeros(1000)
    s[[0, 1, 10, 11, 12]] = 1.0      # 5 flagged rows, 2 of them frauds
    assert og.recall_at_budget(y, s) == pytest.approx(0.5)


def test_the_oracle_takes_the_better_rank_for_each_label():
    y = np.array([1, 0, 0, 0])
    a = np.array([0.9, 0.8, 0.1, 0.2])   # a ranks the fraud first
    b = np.array([0.1, 0.0, 0.9, 0.8])   # b ranks the first legit lowest
    o = og.oracle_scores(y, a, b)
    ra, rb = og.percentile_rank(a), og.percentile_rank(b)
    assert o[0] == pytest.approx(max(ra[0], rb[0]))
    assert o[1] == pytest.approx(min(ra[1], rb[1]))


def test_the_oracle_never_loses_to_either_model():
    rng = np.random.default_rng(0)
    y = (rng.random(4000) < 0.01).astype(int)
    a = rng.random(4000) + y * 0.5
    b = rng.random(4000) + y * 0.4
    r = og.one_seed(y, a, b)
    assert r["recall_oracle"] >= max(r["recall_cvq"], r["recall_xgb"])


def test_identical_models_leave_no_oracle_gap():
    rng = np.random.default_rng(1)
    y = (rng.random(4000) < 0.02).astype(int)
    a = rng.random(4000) + y
    r = og.one_seed(y, a, a.copy())
    assert r["oracle_gap"] == pytest.approx(0.0)


def test_verdict_rules_a_router_out_below_one_point():
    assert og.verdict([0.004, 0.006])["router_ruled_out"] is True
    assert og.verdict([0.02, 0.03])["router_ruled_out"] is False


def test_no_positives_is_refused():
    with pytest.raises(ValueError):
        og.recall_at_budget(np.zeros(10, dtype=int), np.arange(10.0))
