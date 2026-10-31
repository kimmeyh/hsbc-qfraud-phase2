"""F174 (Sprint 30 Task D, #78): the month protocol, on synthetic folds.

Tune on the validation month, refit the chosen configuration on the test
fold's training months, score the test month once, thresholds from the
tuning fit. Nothing here reads IEEE-CIS; predictions go to tmp_path.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PHASE2 = ROOT / "experiments" / "phase2" / "src"
THIS = Path(__file__).relative_to(ROOT).as_posix()
sys.path.insert(0, str(PHASE2))

import f174_ieee_algorithms as f174  # noqa: E402


def _fold(seed: int, n_tr: int, n_ev: int, n_feat: int = 16) -> dict:
    rng = np.random.default_rng(seed)

    def part(n):
        X = rng.normal(size=(n, n_feat))
        y = (X[:, 0] + X[:, 1] + rng.normal(scale=0.8, size=n) > 2.2).astype(int)
        X[rng.random(X.shape) < 0.02] = np.nan       # missing values, as IEEE-CIS
        return pd.DataFrame(X, columns=[f"c{i}" for i in range(n_feat)]), y
    Xtr, ytr = part(n_tr)
    Xev, yev = part(n_ev)
    return {"Xtr": Xtr, "ytr": ytr, "Xev": Xev, "yev": yev}


D = {"val": _fold(1, 1500, 600), "test": _fold(2, 2000, 700)}


def test_the_grids_and_seeds_are_f166s_and_d5s():
    assert f174.GRIDS is f174.f166.GRIDS and f174.ALGOS == f174.f166.ALGOS
    assert f174.SEEDS == tuple(range(42, 52))


def test_the_chosen_config_is_refit_on_the_test_folds_training_rows(
        tmp_path, monkeypatch):
    calls = []
    real = f174.fit_classical

    def spy(algo, params, seed, X, y):
        calls.append((len(y), params))
        return real(algo, params, seed, X, y)
    monkeypatch.setattr(f174, "fit_classical", spy)
    monkeypatch.setitem(f174.GRIDS, "logreg",
                        [{"C": 0.01, "class_weight": None},
                         {"C": 1.0, "class_weight": "balanced"}])
    row, p_te = f174.lane("logreg", 42, D, pred_dir=tmp_path)
    assert [n for n, _ in calls] == [1500, 1500, 2000]
    assert calls[-1][1] == f174.GRIDS["logreg"][row["chosen"]]
    assert len(p_te) == 700 and row["outcome"]


def test_thresholds_come_from_the_tuning_fits_validation_scores(
        tmp_path, monkeypatch):
    import metrics
    monkeypatch.setitem(f174.GRIDS, "hgb", [{"max_leaf_nodes": 15}])
    seen = []
    real = metrics.threshold_max_f1

    def spy(y, p):
        seen.append(len(y))
        return real(y, p)
    monkeypatch.setattr(metrics, "threshold_max_f1", spy)
    f174.lane("hgb", 42, D, pred_dir=tmp_path)
    # Every threshold is set on the validation month's 600 rows, in the
    # metrics and in the outcome block.
    assert seen and set(seen) == {600}


def test_the_proxy_lane_runs_on_missing_values(tmp_path, monkeypatch):
    monkeypatch.setitem(f174.GRIDS, "proxy", [{"config": "free"}])
    monkeypatch.setattr(f174, "MI_ROWS", 800)
    row, p_te = f174.lane("proxy", 42, D, pred_dir=tmp_path)
    assert row["n_learners"] > 0 and len(row["features"]) == 13
    assert np.all((p_te >= 0) & (p_te <= 1)) and len(p_te) == 700


def test_the_refit_can_fail(tmp_path):
    from injection import Mutation, assert_can_fail, run_pytest
    src = PHASE2 / "f174_ieee_algorithms.py"
    assert_can_fail([Mutation(src, '        m, _ = fit_classical(algo, '
                              'GRIDS[algo][i], seed, T["Xtr"], T["ytr"])\n',
                              '        m, _ = fit_classical(algo, '
                              'GRIDS[algo][i], seed, V["Xtr"], V["ytr"])\n',
                              expect_occurrences=1)],
                    lambda: run_pytest(f"{THIS}::test_the_chosen_config_is_"
                                       "refit_on_the_test_folds_training_rows",
                                       ROOT),
                    "the chosen configuration not refit on months 0-3")
    assert_can_fail([Mutation(src, '           "test": f166.fold_metrics('
                              'T["yev"], V["yev"], p_vas[i], p_te,\n',
                              '           "test": f166.fold_metrics('
                              'T["yev"], T["yev"], p_te, p_te,\n',
                              expect_occurrences=1)],
                    lambda: run_pytest(f"{THIS}::test_thresholds_come_from_"
                                       "the_tuning_fits_validation_scores",
                                       ROOT),
                    "thresholds set on the test month")
