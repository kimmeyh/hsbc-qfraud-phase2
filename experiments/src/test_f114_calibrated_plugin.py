"""F114 gate: the calibrated plug-in matches the F108 amendment.

Sprint 28 Task G (#53). Synthetic inputs; the simulator run is not run here.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))

import f114_calibrated_plugin as fp  # noqa: E402


def test_the_amendment_constants():
    assert fp.HOLDOUT == 0.25 and fp.L2 == 1.0
    assert fp.DECIDING_ARM == "none"


def test_split_is_stratified_disjoint_and_repeatable():
    y = np.array([0] * 900 + [1] * 100)
    fit, hold = fp.split_train(y, 42)
    assert len(hold) == 250 and y[hold].sum() == 25
    assert not set(fit) & set(hold) and len(fit) + len(hold) == 1000
    f2, h2 = fp.split_train(y, 42)
    assert np.array_equal(fit, f2) and np.array_equal(hold, h2)


def test_calibration_repairs_distorted_probabilities():
    # Labels from a known posterior; the scores are a monotone distortion
    # of it, so the raw plug-in is far off and the calibrated one is near.
    rng = np.random.default_rng(0)
    n = 40_000
    eta = 1 / (1 + np.exp(-(rng.normal(size=n) - 2.5)))
    y = (rng.uniform(size=n) < eta).astype(int)
    p = np.sqrt(eta)
    hold, te = slice(0, 20_000), slice(20_000, n)
    bayes = float(np.mean(np.minimum(eta[te], 1 - eta[te])))
    assert abs(fp.plugin(p[te]) - bayes) > 0.5 * bayes
    p_cal = fp.calibrate(p[hold], y[hold], p[te])
    assert abs(fp.plugin(p_cal) - bayes) < 0.1 * bayes


def test_the_plugins_come_from_one_75_percent_model():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(4000, 1))
    y = (rng.uniform(size=4000) < 1 / (1 + np.exp(-X[:, 0]))).astype(int)
    est = fp.calibrated_plugins(X[:3000], y[:3000], X[3000:], 0)
    assert est["n_fit"] == 2250 and est["n_holdout"] == 750


def test_score_arm_draws_what_f108_draws():
    # F108's score_arm takes one Cover-Hart subsample from the shared
    # stream; skipping it would change the next arm's noisy labels.
    rng = np.random.default_rng(1)
    X = rng.normal(size=(2000, 2))
    y = (X[:, 0] > 0).astype(int)
    eta = y.astype(float)
    a, b = np.random.default_rng(9), np.random.default_rng(9)
    fp.score_arm(X[:1500], y[:1500], X[1500:], eta[1500:], 0, a)
    b.choice(500, 500, replace=False)
    assert a.uniform() == b.uniform()


def _row(seed, rec_none, rec_cal=True):
    arm = {"calibrated_recovered": rec_cal, "uncalibrated_recovered": False}
    return {"seed": seed, "arms": {"none": {**arm, "calibrated_recovered": rec_none},
                                   "flip": arm, "reference": arm}}


def test_verdict_needs_four_of_five_on_the_main_arm():
    rows = [_row(s, s != 42) for s in range(42, 47)]
    assert fp.verdict(fp.summarize(rows))["calibrated_plugin_recovers"]
    rows = [_row(s, s > 43) for s in range(42, 47)]
    v = fp.verdict(fp.summarize(rows))
    assert not v["calibrated_plugin_recovers"] and "blocked" in v["f114"]


def test_a_stopped_seed_counts_as_a_miss():
    rows = [_row(s, True) for s in range(42, 46)]
    rows.append({"seed": 46, "arms": {}, "stopped": "generator check failed"})
    rows[0]["arms"]["none"]["calibrated_recovered"] = False
    s = fp.summarize(rows)["none"]["calibrated"]
    assert s == {"seeds_recovered": 3, "n_seeds": 5, "recovers": False}
