"""F111: Experiment 4's harness matches its entry.

Sprint 28 Task D (#51). Synthetic inputs; the ULB runs are not run here.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "src"))

import f111_loke_protocol as fl  # noqa: E402


def test_the_entry_constants():
    assert fl.SEEDS == tuple(range(42, 52)) and fl.SENS_SEEDS == (42, 43, 44)
    assert (fl.RATIO, fl.SENS_RATIO) == (0.02, 0.05)
    assert fl.KNN_PARAMS == {"n_neighbors": 15}
    assert (fl.SCHEDULE, fl.LAMBDA, fl.HGB_L2) == (2, 0.0, 1.0)
    assert fl.VAL_EVAL_TEST_SIZE == 0.67 and fl.CAP_MIN == 120.0
    assert (fl.TARGET, fl.TOLERANCE) == (0.8108, 0.03)


def _imbalanced(n=3000, pos=30, seed=0):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, 4))
    y = np.zeros(n, dtype=int)
    y[:pos] = 1
    X[:pos] += 2.0
    return X, y


def test_smote_tomek_reaches_the_ratio_with_the_codes_neighbors():
    X, y = _imbalanced()
    Xr, yr, info = fl.smote_tomek(X, y, 0.02, 42)
    assert info["applied"] and info["k_neighbors"] == 10
    # SMOTE reaches 0.02 of the majority; the Tomek step then removes
    # linked rows of both classes, so the count lands at or a little under.
    assert info["pos_before"] * 1.5 < info["pos_after"] <= 0.02 * info["neg_before"] + 1
    assert len(yr) == len(Xr) and yr.sum() == info["pos_after"]


def test_smote_tomek_is_skipped_when_already_balanced():
    X, y = _imbalanced(n=1000, pos=100)
    Xr, yr, info = fl.smote_tomek(X, y, 0.02, 42)
    assert not info["applied"] and Xr is X


def test_duplicates_counts_exact_copies_including_the_label():
    X = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    y = np.array([0, 1, 0])
    Xq = np.array([[1.0, 2.0], [3.0, 4.0], [3.0, 4.0], [9.0, 9.0]])
    yq = np.array([0, 1, 0, 0])            # the third differs by label only
    assert fl.duplicates_in_train(X, y, Xq, yq) == 2
    # Same features, every label flipped: no exact copies.
    assert fl.duplicates_in_train(X[:2], y[:2], X[:2], 1 - y[:2]) == 0


def test_score_is_monotone_in_w_dot_h():
    rng = np.random.default_rng(0)
    H = np.where(rng.random((5, 200)) < 0.5, 1.0, -1.0)
    w = rng.dirichlet(np.ones(5))
    raw = w @ H
    assert np.array_equal(np.argsort(fl.score(w, H), kind="stable"),
                          np.argsort(raw, kind="stable"))
    assert fl.score(w, H).min() >= 0 and fl.score(w, H).max() <= 1


def test_paired_interval_matches_a_hand_computed_t():
    from scipy import stats
    a = [0.80, 0.82, 0.79, 0.81]
    b = [0.78, 0.80, 0.78, 0.80]
    r = fl.paired(a, b)
    d = np.subtract(a, b)
    half = stats.t.ppf(0.975, 3) * d.std(ddof=1) / 2
    assert r["mean"] == pytest.approx(0.015)
    assert (r["low"], r["high"]) == pytest.approx((0.015 - half, 0.015 + half))
    assert r["excludes_zero"]


def _rows(knn_a, knn_b, hgb_a=0.8, hgb_b=0.8):
    rows = []
    for i, s in enumerate(fl.SEEDS):
        for p, ratio, lane, v in (("A", 0.02, "knn", knn_a[i]), ("B", None, "knn", knn_b[i]),
                                  ("A", 0.02, "hgb", hgb_a), ("B", None, "hgb", hgb_b)):
            rows.append({"protocol": p, "ratio": ratio, "lane": lane, "seed": s,
                         "test_auprc": v + (0.001 * i if lane == "hgb" else 0),
                         "eval_duplicates_in_train": 3 if p == "A" else 0})
    return {"rows": rows}


def test_analysis_pairs_by_seed_and_reads_consistency():
    knn_b = [0.77 + 0.002 * i for i in range(10)]
    knn_a = [v + 0.03 + (0.001 if i % 2 else -0.001) for i, v in enumerate(knn_b)]
    out = fl.analyze(_rows(knn_a, knn_b))
    assert out["knn_A_minus_B"]["mean"] == pytest.approx(0.03)
    assert out["knn_A_minus_B"]["excludes_zero"]
    assert out["consistent_with_0_8108"] is True       # mean 0.809
    assert out["eval_duplicates_in_train_A"][0] == (42, 3)


def test_a_far_mean_is_not_consistent():
    out = fl.analyze(_rows([0.70] * 10, [0.70] * 10))
    assert out["consistent_with_0_8108"] is False


def test_projection_adds_preparation_and_counts_the_sensitivity_seeds():
    p = {k: {"seconds": 6.0, "prep_seconds_full": 30.0, "full_train": 100,
             "pilot_train": 10, "full_query": 200, "pilot_query": 20}
         for k in ("A", "B")}
    # lane 6 s x 10 x 10 = 600 s per seed, plus 30 s preparation
    assert fl.projection_min(p) == pytest.approx((630 * 13 + 630 * 10) / 60)


def test_run_refuses_without_a_passing_pilot(tmp_path, monkeypatch):
    monkeypatch.setattr(fl, "OUT", tmp_path / "f111.json")
    with pytest.raises(SystemExit, match="Manual Validation"):
        fl.run()
