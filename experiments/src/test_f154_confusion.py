"""F154's counts, interaction and table are computed as the entry states.

Sprint 28 Task F (#47). Synthetic inputs: zero metered, no dataset, nothing
written to an evidence directory. The run itself reads local prediction
files and ULB, so it is not run here.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))

import f154_confusion as fc  # noqa: E402


def test_the_entry_constants():
    assert fc.ALERT_BUDGET == 0.005
    assert fc.SEEDS == tuple(range(42, 52))
    assert fc.DAY_S == 86_400


def test_catch_and_miss_counts_frauds_only():
    y = np.array([1, 1, 1, 1, 0, 0])
    a = np.array([1, 1, 0, 0, 1, 0], bool)
    b = np.array([1, 0, 1, 0, 1, 1], bool)
    assert fc.catch_and_miss(y, a, b) == {"a_only": 1, "b_only": 1,
                                          "both": 1, "neither": 1}


def test_a_uniform_advantage_has_no_interaction():
    # A beats B by the same margin inside and outside the subset.
    y = np.array([1] * 8)
    mask = np.array([1, 1, 1, 1, 0, 0, 0, 0], bool)
    a = np.array([1, 1, 1, 0, 1, 1, 1, 0], bool)
    b = np.array([1, 1, 0, 0, 1, 1, 0, 0], bool)
    assert fc.interaction(y, a, b, mask) == pytest.approx(0.0)


def test_an_advantage_only_inside_the_subset_is_an_interaction():
    y = np.array([1] * 8)
    mask = np.array([1, 1, 1, 1, 0, 0, 0, 0], bool)
    a = np.array([1, 1, 1, 1, 1, 1, 0, 0], bool)
    b = np.array([1, 1, 0, 0, 1, 1, 0, 0], bool)
    assert fc.interaction(y, a, b, mask) == pytest.approx(0.5)


def test_the_bonferroni_interval_is_wider_than_the_plain_one():
    v = [0.02, 0.03, 0.01, 0.04, 0.02, 0.03, 0.01, 0.02, 0.03, 0.02]
    plain, corrected = fc.t_interval(v, 0.95), fc.t_interval(v, 1 - 0.05 / 132)
    assert corrected["high"] - corrected["low"] > plain["high"] - plain["low"]
    assert plain["excludes_zero"]


def test_tie_neutral_weights_flag_exactly_the_budget():
    s = np.zeros(1000)
    s[[0, 1, 2]] = 2.0
    s[[3, 4, 5, 6]] = 1.0
    w = fc.budget_weights(s)
    assert w.sum() == pytest.approx(5.0)
    assert w[3] == pytest.approx(0.5) and w[0] == 1.0 and w[7] == 0.0


def test_table_rows_carry_every_confusion_with_its_source():
    rows = [{"arm": "xgboost", "dataset": "ulb", "protocol": "stratified",
             "config_hash": "h", "seed": 42, "evidence_tag": "SIM",
             "metrics": {"operating_points": [
                 {"operating_point": "max_f1_on_val",
                  "confusion": {"tn": 1, "fp": 2, "fn": 3, "tp": 4}},
                 {"operating_point": "alert_budget_0.005",
                  "confusion": {"tn": 5, "fp": 6, "fn": 7, "tp": 8}}]}},
            {"arm": "x", "metrics": {}}]
    t, skipped = fc.table_rows(rows, "src.json")
    assert len(t) == 2 and skipped == 0
    assert t[1]["tp"] == 8 and t[1]["source"] == "src.json"


def test_families_need_all_ten_seeds(tmp_path):
    for s in fc.SEEDS:
        np.savez(tmp_path / f"full_abc_stratified_{s}.npz", y_test=[0])
    np.savez(tmp_path / "part_abc_stratified_42.npz", y_test=[0])
    np.savez(tmp_path / "full_abc_temporal_None.npz", y_test=[0])
    assert fc.families(tmp_path) == ["full_abc"]


def test_table_rows_count_an_operating_point_without_confusion():
    rows = [{"arm": "a", "metrics": {"operating_points": [
        {"operating_point": "max_f1_on_val",
         "confusion": {"tn": 1, "fp": 2, "fn": 3, "tp": 4}},
        {"operating_point": "alert_budget_0.005"}]}}]
    t, skipped = fc.table_rows(rows, "src.json")
    assert len(t) == 1 and skipped == 1


def test_a_subset_with_no_fraud_is_not_estimable():
    y = np.array([1, 1, 1, 1, 0, 0, 0, 0])
    mask = np.array([0, 0, 0, 0, 1, 1, 1, 1], bool)     # no fraud inside
    a = np.array([1, 1, 0, 0, 0, 0, 0, 0], bool)
    assert np.isnan(fc.interaction(y, a, a, mask))
    iv = fc.interaction_interval([0.1, 0.2, float("nan"), 0.1], 0.95)
    assert iv["estimable"] is False and iv["n_nonfinite"] == 1
    assert "excludes_zero" not in iv
    ok = fc.interaction_interval([0.1, 0.2, 0.15, 0.1], 0.95)
    assert ok["estimable"] and ok["excludes_zero"]


def _pair(*cells):
    return {"interaction": dict(zip(("amount_above_median", "day_1"), cells))}


def test_the_verdict_counts_estimable_pairs_and_never_reads_nan_as_null():
    names = ("amount_above_median", "day_1")
    nan = fc.interaction_interval([float("nan")] * 3, 0.95)
    null = fc.interaction_interval([0.1, -0.1, 0.05], 0.95)
    fired = fc.interaction_interval([0.1, 0.11, 0.12], 0.95)
    assert fc.verdict([_pair(nan, nan)], names).startswith("not estimable")
    v = fc.verdict([_pair(null, nan)], names)
    assert v.startswith("null") and "1 of 2 pair-subsets estimable" in v
    v = fc.verdict([_pair(fired, nan)], names)
    assert v.startswith("some pair") and "1 of 2" in v
