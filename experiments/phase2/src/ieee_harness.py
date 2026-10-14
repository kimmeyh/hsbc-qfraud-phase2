"""F105 (Sprint 26 Task G): the Experiment 2 harness on IEEE-CIS.

A harness, not a result. **No model score is reported** until F102 names
this experiment's preregistration entry (Phase 2 draft, section 6,
Experiment 2). The pilot fits a model only to time it; it computes no
metric and writes none.

What it adds to Phase 1's IEEE-CIS pipeline (`run_ieee.py`, which this
module imports and never edits):

- **Rolling-origin folds over TransactionDT** (`ieee_splits`, unchanged:
  the last three month buckets, each trained on every earlier month), with
  the hard leakage assertion run on every build.
- **The entity key `card1_addr1_(day - D1)` for aggregations only.**
  `ieee_features.IEEEFeaturePipeline` computes it, fits the UID aggregates
  on training rows, and drops the key. `audit_entity_key_not_a_feature`
  checks no column carries it.
- **A temporal-leakage audit of the aggregate features**
  (`audit_aggregate_leakage`): every evaluation row's own transaction
  values are scrambled and the evaluation features rebuilt. An aggregate
  computed from training rows only cannot move; any `uid_*` column that
  moves was fitted on evaluation rows. The `*_freq` columns are checked
  directly instead (`audit_frequency_columns`), because their sources are
  the entity key's inputs, which the scramble leaves fixed. There are no
  graph features in this pipeline; the audit says so rather than passing
  them.
- **Time-consistency selection and adversarial validation** inside the
  training fold (`ieee_controls`, unchanged).
- **The random-halves adversarial check** (`random_halves_auc`): one time
  window split into two random halves; a classifier that tells them apart
  above AUC 0.55 means the pipeline or the classifier leaks row identity,
  and no cross-window adversarial result is read (plan, Task G).
- **Client-mean post-processing** (`client_mean`): each evaluation
  prediction replaced by the mean over its entity key, computed from
  evaluation-fold predictions only, never labels.

Usage:
    python experiments/phase2/src/ieee_harness.py pilot --frac 0.10
    python experiments/phase2/src/ieee_harness.py audit   (3 folds, full data)

The pilot writes a heartbeat line per stage to
`experiments/phase2/results/f105_pilot.heartbeat` and its timings and audit
results to `experiments/phase2/results/f105_pilot.json`.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "experiments" / "src"))
import ieee_controls  # noqa: E402
import ieee_features  # noqa: E402
import ieee_splits  # noqa: E402

RESULTS = ROOT / "experiments" / "phase2" / "results"
PILOT_OUT = RESULTS / "f105_pilot.json"
AUDIT_OUT = RESULTS / "f105_full_audit.json"
HEARTBEAT = RESULTS / "f105_pilot.heartbeat"
RANDOM_HALVES_MAX_AUC = 0.55
AGG_PREFIXES = ("uid_",)
AGG_SUFFIXES = ("_freq",)
# The eval-row values scrambled by the aggregate audit: every value input of
# the UID aggregates (ieee_features). The frequency encodings are checked by
# audit_frequency_columns instead.
SCRAMBLE_COLS = ("TransactionAmt",) + ieee_features.UID_AGG_C_COLS \
    + ieee_features.UID_AGG_D_COLS


def numeric(df: pd.DataFrame) -> pd.DataFrame:
    """Numeric columns only, as `run_ieee._numeric` does."""
    return df.select_dtypes(include=[np.number])


def time_sample(df: pd.DataFrame, frac: float) -> pd.DataFrame:
    """Every k-th row in time order, so a sample spans all months (a head
    sample lands in month 0 and the folds refuse it; run_ieee.py)."""
    step = max(1, int(round(1.0 / frac)))
    return (df.sort_values("TransactionDT").iloc[::step]
            .reset_index(drop=True))


def folds_for(df: pd.DataFrame) -> list:
    folds = ieee_splits.rolling_origin_folds(df)
    ieee_splits.assert_no_temporal_leakage(df, folds)
    return folds


def build_fold(df: pd.DataFrame, fold, pipe_factory=None) -> dict:
    """Features for one fold, fitted on its training months only."""
    parts = ieee_splits.split_xy(df, fold)
    pipe = (pipe_factory or ieee_features.IEEEFeaturePipeline)()
    Xtr = numeric(pipe.fit_transform(parts["X_train"]))
    Xev = numeric(pipe.transform(parts["X_eval"])).reindex(
        columns=Xtr.columns)
    day_ev = ieee_features.add_day(parts["X_eval"])
    uid_ev = ieee_features.compute_uid(parts["X_eval"], day_ev)
    return {"parts": parts, "pipe": pipe, "X_train": Xtr, "X_eval": Xev,
            "uid_eval": uid_ev}


def audit_entity_key_not_a_feature(X: pd.DataFrame, uid: pd.Series) -> list:
    """Columns that carry the entity key itself. Empty is the pass."""
    bad = [c for c in X.columns if c.lower() in ("uid", "_uid")]
    codes = pd.Series(pd.factorize(uid.values)[0], index=X.index)
    n_keys = codes.nunique()
    for c in X.columns:
        col = X[c].fillna(-9e9)
        if col.nunique() != n_keys:
            continue
        # One-to-one with the key in both directions: an encoding of it.
        if (col.groupby(codes).nunique().max() == 1
                and codes.groupby(col).nunique().max() == 1):
            bad.append(c)
    return sorted(set(bad))


def audit_aggregate_leakage(df: pd.DataFrame, fold, pipe_factory=None,
                            seed: int = 0) -> dict:
    """Scramble the evaluation rows' own values; aggregate columns built from
    training rows cannot change. Returns the columns that did."""
    base = build_fold(df, fold, pipe_factory)
    rng = np.random.default_rng(seed)
    scrambled = df.copy()
    ev = fold.eval_idx
    for c in SCRAMBLE_COLS:
        if c in scrambled.columns:
            vals = scrambled.loc[ev, c].to_numpy()
            scrambled.loc[ev, c] = rng.permutation(vals) * 3.0 + 1.0
    # Keep the entity key fixed: card1, addr1, D1 and TransactionDT are not
    # scrambled, so each row still joins the same training aggregate.
    after = build_fold(scrambled, fold, pipe_factory)
    agg_cols = [c for c in base["X_eval"].columns
                if c.startswith(AGG_PREFIXES) or c.endswith(AGG_SUFFIXES)]
    moved = []
    for c in agg_cols:
        a = base["X_eval"][c].to_numpy(dtype=float)
        b = after["X_eval"][c].to_numpy(dtype=float)
        if not np.array_equal(np.nan_to_num(a, nan=-9e9),
                              np.nan_to_num(b, nan=-9e9)):
            moved.append(c)
    train_same = base["X_train"].equals(after["X_train"])
    freq_bad = audit_frequency_columns(base)
    return {"aggregate_columns_checked": len(agg_cols),
            "moved": moved, "training_features_unchanged": bool(train_same),
            "frequency_columns_not_from_training_rows": freq_bad,
            "graph_features": "none in this pipeline",
            "passes": (bool(agg_cols) and not moved and train_same
                       and not freq_bad)}


def audit_frequency_columns(built: dict) -> list:
    """Each `*_freq` column recomputed from the fold's TRAINING rows only and
    compared exactly. The scramble above cannot test these: their sources
    (card1, addr1, P_emaildomain) are the entity key's inputs and are left
    fixed (Sprint 26 code review, finding 7)."""
    tr = ieee_features.build_card1_addr1(built["parts"]["X_train"])
    ev = ieee_features.build_card1_addr1(built["parts"]["X_eval"])
    bad = []
    for col in ieee_features.FREQ_ENCODE_COLS:
        name = f"{col}_freq"
        if col not in tr.columns or name not in built["X_eval"].columns:
            continue
        expected = ev[col].map(tr[col].value_counts()).fillna(0).astype(
            "float32").to_numpy()
        if not np.array_equal(expected,
                              built["X_eval"][name].to_numpy("float32")):
            bad.append(name)
    return bad


def random_halves_auc(X: pd.DataFrame, seed: int = 0,
                      halves: np.ndarray | None = None) -> float:
    """AUC of a classifier telling two RANDOM halves of one window apart.
    Near 0.5 by construction; above RANDOM_HALVES_MAX_AUC means something
    in the features or the classifier identifies rows. `halves` overrides
    the random split, for the test that shows the check can fire."""
    from sklearn.ensemble import HistGradientBoostingClassifier
    from sklearn.metrics import roc_auc_score
    from sklearn.model_selection import train_test_split

    rng = np.random.default_rng(seed)
    half = (rng.permutation(np.arange(len(X)) % 2) if halves is None
            else np.asarray(halves))
    Xtr, Xte, ytr, yte = train_test_split(
        X, half, test_size=0.3, random_state=seed, stratify=half)
    clf = HistGradientBoostingClassifier(max_iter=60, random_state=seed)
    clf.fit(Xtr, ytr)
    return float(roc_auc_score(yte, clf.predict_proba(Xte)[:, 1]))


def client_mean(pred: np.ndarray, uid: pd.Series) -> np.ndarray:
    """Each prediction replaced by its entity's mean prediction, over the
    evaluation fold only. Uses predictions, never labels."""
    s = pd.Series(np.asarray(pred, dtype=float), index=uid.index)
    return s.groupby(uid.values).transform("mean").to_numpy()


def _beat(stage: str, **kw) -> None:
    HEARTBEAT.parent.mkdir(parents=True, exist_ok=True)
    with HEARTBEAT.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"t": time.strftime("%Y-%m-%dT%H:%M:%S"),
                            "stage": stage, **kw}) + "\n")


def _fold_audit(df: pd.DataFrame, fold, seed: int) -> dict:
    """Every audit and control on one fold, each stage timed, plus one model
    fit and prediction to time it. No metric is computed."""
    from lightgbm import LGBMClassifier

    em = int(fold.eval_month)
    t = {}
    t0 = time.time()
    b = build_fold(df, fold)
    t["features_s"] = round(time.time() - t0, 1)
    _beat("features", eval_month=em, n_features=b["X_train"].shape[1])

    key_cols = audit_entity_key_not_a_feature(b["X_eval"], b["uid_eval"])
    t0 = time.time()
    leak = audit_aggregate_leakage(df, fold, seed=seed)
    t["aggregate_audit_s"] = round(time.time() - t0, 1)
    _beat("aggregate_audit", eval_month=em, passes=leak["passes"])

    t0 = time.time()
    day_tr = ieee_features.add_day(b["parts"]["X_train"]).to_numpy()
    y_tr = b["parts"]["y_train"].to_numpy()
    halves = random_halves_auc(b["X_train"], seed=seed)
    ctrl = ieee_controls.apply_item4_controls(b["X_train"], y_tr, day_tr,
                                              seed=seed)
    # An empty selection is recorded, never silently replaced (code review
    # finding 12); the timing fit then uses every feature, and says so.
    selected_none = not ctrl["features"]
    keep = ctrl["features"] or list(b["X_train"].columns)
    t["controls_s"] = round(time.time() - t0, 1)
    _beat("controls", eval_month=em, random_halves_auc=round(halves, 4),
          kept=len(keep))

    t0 = time.time()
    m = LGBMClassifier(num_leaves=64, n_estimators=400, learning_rate=0.05,
                       subsample=0.8, colsample_bytree=0.8, verbose=-1,
                       random_state=seed)
    m.fit(b["X_train"][keep], y_tr)
    p = m.predict_proba(b["X_eval"][keep])[:, 1]
    p_cm = client_mean(p, b["uid_eval"])
    t["fit_predict_s"] = round(time.time() - t0, 1)
    _beat("fit_predict", eval_month=em, n_eval=len(p))

    return {
        "eval_month": em,
        "train_months": [int(x) for x in fold.train_months],
        "n_train": int(len(fold.train_idx)),
        "n_eval": int(len(fold.eval_idx)),
        "timings_s": t,
        "audits": {
            "entity_key_columns_found": key_cols,
            "aggregate_leakage": leak,
            "random_halves_auc": halves,
            "random_halves_passes": halves <= RANDOM_HALVES_MAX_AUC,
            "item4_controls": {k: v for k, v in ctrl.items()
                               if k != "features"},
        },
        "controls_selected_none": selected_none,
        "client_mean_changed_fraction": float(np.mean(p_cm != p)),
    }


def pilot(frac: float, n_folds: int = 1, seed: int = 42,
          out_path: Path = PILOT_OUT) -> dict:
    """`n_folds` folds on a time-spread `frac` sample (1.0 is the full
    data). Every stage timed. No metric is computed or written."""
    import data
    import ieee_loader

    HEARTBEAT.unlink(missing_ok=True)
    t0 = time.time()
    df, n_dupes = ieee_loader.dedupe_ieee(data.load_ieee_cis_train())
    n_full = len(df)
    if frac < 1.0:
        df = time_sample(df, frac)
    load_s = round(time.time() - t0, 1)
    _beat("loaded", rows=len(df))

    folds = [_fold_audit(df, f, seed) for f in folds_for(df)[:n_folds]]
    out = {
        "generator": "experiments/phase2/src/ieee_harness.py",
        "card": "F105", "sprint": 26, "evidence_tag": "SIM",
        "metered_seconds": 0, "fraction": frac,
        "no_score_reported": "F105: no model score until F102 names the "
                             "Experiment 2 preregistration entry",
        "rows_after_dedupe_full": n_full,
        "rows_used": len(df), "exact_duplicates_removed": n_dupes,
        "load_s": load_s,
        "folds": folds,
    }
    out_path.write_text(json.dumps(out, indent=1, default=str) + "\n",
                        encoding="utf-8")
    _beat("done")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("pilot", help="one fold on a time-spread sample")
    p.add_argument("--frac", type=float, default=0.10)
    sub.add_parser("audit", help="all three folds on the full data")
    args = ap.parse_args()
    if args.cmd == "pilot":
        out = pilot(args.frac)
    else:
        out = pilot(1.0, n_folds=ieee_splits.N_ROLLING_FOLDS,
                    out_path=AUDIT_OUT)
    print(json.dumps(out, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
