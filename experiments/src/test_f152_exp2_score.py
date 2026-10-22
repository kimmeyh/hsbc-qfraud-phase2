"""F152: the Experiment 2 scorer's bootstrap and constants match the entry.

Sprint 28 Task B (#49). Synthetic inputs; the run reads IEEE-CIS and is not
run here.
"""
from __future__ import annotations

import inspect
import sys
from pathlib import Path

import numpy as np
import pytest
from sklearn.metrics import average_precision_score

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))

import f152_exp2_score as fs  # noqa: E402


def test_the_entry_constants():
    assert fs.SEEDS == (42, 43, 44, 45, 46)
    assert fs.LANES == ("xgboost", "lightgbm", "hgb", "logistic")
    assert fs.FULL_MONTHS == (4, 5)
    assert fs.PRIMARY_LEVEL == pytest.approx(0.975)
    assert fs.CONTROLS_SEED == 42


def test_weighted_ap_matches_sklearn_with_ties_and_weights():
    rng = np.random.default_rng(0)
    y = (rng.random(4000) < 0.05).astype(int)
    p = np.round(rng.random(4000) + 0.4 * y, 2)        # many ties
    parts = fs.ap_parts(y, p)
    assert fs.weighted_ap(parts, np.ones(4000, int)) == pytest.approx(
        average_precision_score(y, p))
    c = fs.stratified_counts(y, rng)
    assert fs.weighted_ap(parts, c) == pytest.approx(
        average_precision_score(y, p, sample_weight=c))


def test_stratified_counts_keep_the_class_totals():
    y = np.array([0] * 90 + [1] * 10)
    c = fs.stratified_counts(y, np.random.default_rng(1))
    assert c.sum() == 100 and c[y == 1].sum() == 10


def test_floor_normalization():
    assert fs.floor_norm(0.035, 0.035) == pytest.approx(0.0)
    assert fs.floor_norm(1.0, 0.035) == pytest.approx(1.0)


def test_a_real_difference_is_found_and_no_difference_is_not():
    rng = np.random.default_rng(2)
    y = (rng.random(3000) < 0.05).astype(int)
    good = [rng.random(3000) + 1.5 * y for _ in range(2)]
    poor = [rng.random(3000) + 0.2 * y for _ in range(2)]
    iv = fs.boot_seed_mean_delta(y, good, poor, n_boot=200)
    assert iv["low"] > 0
    same = fs.boot_seed_mean_delta(y, good, good, n_boot=200)
    assert same["estimate"] == pytest.approx(0.0) and not same["excludes_zero"]


def test_hgb_lane_uses_f151s_stable_setting():
    src = inspect.getsource(fs.fit_predict)
    assert "HistGradientBoostingClassifier(l2_regularization=1.0" in src


def test_the_harness_stays_score_free():
    # The scorer imports the harness; it never edits it (F105's no-score test).
    import ieee_harness  # noqa: F401
    src = (ROOT / "experiments" / "phase2" / "src" / "ieee_harness.py").read_text(
        encoding="utf-8")
    assert "average_precision_score" not in src
