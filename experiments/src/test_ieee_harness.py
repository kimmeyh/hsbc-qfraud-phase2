"""F105 (Sprint 26 Task G): the Phase 2 IEEE-CIS harness, on a synthetic
frame (CI has no IEEE-CIS data). Each audit is shown to fire on an
injected leak, not only to pass on clean data.
"""
from __future__ import annotations

import inspect
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))
import ieee_features  # noqa: E402
import ieee_harness as H  # noqa: E402
from test_ieee_features import _make_fixture  # noqa: E402


def _frame(n: int = 1500, seed: int = 0) -> pd.DataFrame:
    """The feature tests' fixture, stretched to 210 days so the rolling-
    origin splitter finds seven month buckets."""
    df = _make_fixture(n=n, seed=seed)
    rng = np.random.default_rng(seed + 1)
    df["TransactionDT"] = 86400 + rng.integers(0, 210 * 86400, size=n)
    return df


class _LeakyPipeline(ieee_features.IEEEFeaturePipeline):
    """Refits the UID aggregates on the frame it transforms: the leak the
    aggregate audit exists to catch."""

    def transform(self, df):
        prepped, _day, uid = self._prep(df)
        self.uid_agg.fit(prepped, uid)
        return super().transform(df)


def test_folds_are_rolling_origin_and_leak_free():
    df = _frame()
    folds = H.folds_for(df)
    assert len(folds) == 3
    for f in folds:
        assert all(m < f.eval_month for m in f.train_months)


def test_the_aggregate_audit_passes_the_real_pipeline():
    df = _frame()
    out = H.audit_aggregate_leakage(df, H.folds_for(df)[0])
    assert out["aggregate_columns_checked"] > 0
    assert out["moved"] == [] and out["passes"]


def test_the_aggregate_audit_fires_on_aggregates_fitted_on_eval_rows():
    df = _frame()
    out = H.audit_aggregate_leakage(df, H.folds_for(df)[0],
                                    pipe_factory=_LeakyPipeline)
    assert not out["passes"]
    assert any(c.startswith("uid_") for c in out["moved"])


class _FreqLeakyPipeline(ieee_features.IEEEFeaturePipeline):
    """Refits ONLY the frequency tables on the frame it transforms. The
    scramble cannot see this (code review finding 7)."""

    def transform(self, df):
        prepped, _day, _uid = self._prep(df)
        self.uid_agg.freq_tables = {
            c: prepped[c].value_counts()
            for c in ieee_features.FREQ_ENCODE_COLS if c in prepped.columns}
        return super().transform(df)


def test_the_audit_fires_on_frequency_tables_fitted_on_eval_rows():
    df = _frame()
    out = H.audit_aggregate_leakage(df, H.folds_for(df)[0],
                                    pipe_factory=_FreqLeakyPipeline)
    assert not out["passes"]
    assert out["frequency_columns_not_from_training_rows"]
    assert out["moved"] == []      # the scramble alone would have passed it


def test_the_entity_key_never_reaches_the_features():
    df = _frame()
    b = H.build_fold(df, H.folds_for(df)[0])
    assert H.audit_entity_key_not_a_feature(b["X_eval"], b["uid_eval"]) == []
    leaked = b["X_eval"].assign(
        key_code=pd.factorize(b["uid_eval"].values)[0])
    assert H.audit_entity_key_not_a_feature(leaked, b["uid_eval"]) == [
        "key_code"]


def test_random_halves_stay_near_chance_and_the_check_can_fire():
    df = _frame(n=3000)
    b = H.build_fold(df, H.folds_for(df)[0])
    X = b["X_train"]
    assert H.random_halves_auc(X, seed=0) <= H.RANDOM_HALVES_MAX_AUC
    # A feature that identifies the half: the check must see it.
    halves = np.arange(len(X)) % 2
    leaked = X.assign(row_parity=halves)
    assert H.random_halves_auc(leaked, seed=0, halves=halves) > 0.95


def test_client_mean_averages_within_the_entity_key():
    uid = pd.Series(["a", "a", "b", "c", "c", "c"])
    p = np.array([0.1, 0.3, 0.5, 0.0, 0.3, 0.6])
    assert np.allclose(H.client_mean(p, uid), [0.2, 0.2, 0.5, 0.3, 0.3, 0.3])


def test_the_harness_computes_no_score():
    """F105: no model score until F102 names the preregistration entry. The
    whole module is scanned (the model is fitted in `_fold_audit`, not in
    `pilot`; code review finding 13). The one allowed AUC is the random-
    halves check, which scores a classifier of row halves, not the model."""
    src = inspect.getsource(H)
    allowed = inspect.getsource(H.random_halves_auc)
    rest = src.replace(allowed, "")
    for banned in ("average_precision", "roc_auc", "auprc", "f1_score",
                   "recall_score", "precision_score", "log_loss"):
        assert banned not in rest, f"the harness computes {banned}"
