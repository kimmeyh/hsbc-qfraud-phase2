"""F157 QNN part (Sprint 31 Task G, #99): F106's circuit and twins on
IEEE-CIS month 4, a test fold with about 30 times F106's positives.

The entry is the 2026-11-05 amendment to "F106" in
`experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, committed before
this module existed. The circuit, the twins, the comparison and the
outcome rule are F106's (`f106_dequant`, imported, not edited). Only the
data changes:

- F174's month-4 fold (features fitted on months 0-3, item-4 controls),
  missing values filled with the training months' median;
- k = 8 features by `data.top_k_features` on a stratified 50,000-row
  subsample of the training rows, seeded by the seed;
- training rows: 295 positives and 6,000 negatives drawn from the seed
  (F106's size and rate); validation (the RFF bandwidth only): a
  stratified 20,000-row draw from the rest; test: the whole month.

Modes:
  pilot  seed 42 alone, timed; projects the eight seeds against the
         entry's 4-hour limit and the seed count that fits (at least 5)
  run    the seeds the pilot set, resumable by seed; then F106's compare

    <venv python> experiments/phase2/src/f157_qnn_ieee.py pilot|run

Zero metered seconds. Writes `experiments/phase2/results/f157_qnn_ieee.json`
(and `_pilot.json`) through `provenance.write_result`.
"""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "experiments" / "src"))
import f106_dequant as f106  # noqa: E402  (Phase 2, F106; not edited)

OUT = ROOT / "experiments" / "phase2" / "results" / "f157_qnn_ieee.json"
OUT_PILOT = OUT.with_name("f157_qnn_ieee_pilot.json")
# F168 part 7: a long run resumes through provenance.start.
LONG_RUN = True
SEEDS = f106.SEEDS
N_POS_TRAIN, N_NEG_TRAIN = 295, f106.N_NEG_TRAIN
N_VAL = 20_000
MI_ROWS = 50_000
LIMIT_S = 4 * 3600
MIN_SEEDS = 5

_FOLD: dict | None = None


def fold() -> dict:
    """F174's month-4 fold, built once."""
    global _FOLD
    if _FOLD is None:
        import data as dmod
        import f174_ieee_algorithms as f174
        import ieee_loader
        import ieee_splits
        df, _ = ieee_loader.dedupe_ieee(dmod.load_ieee_cis_train())
        folds = ieee_splits.rolling_origin_folds(df, n_folds=4)
        ieee_splits.assert_no_temporal_leakage(df, folds)
        f = {int(x.eval_month): x for x in folds}[f174.TEST_MONTH]
        _FOLD = f174.fold_data(df, f)
    return _FOLD


def draw_rows(y: np.ndarray, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """Training rows (295 positives, 6,000 negatives) and a stratified
    20,000-row validation draw from the rest, both from the seed."""
    rng = np.random.default_rng(seed)
    pos = rng.choice(np.flatnonzero(y == 1), N_POS_TRAIN, replace=False)
    neg = rng.choice(np.flatnonzero(y == 0), N_NEG_TRAIN, replace=False)
    tr = np.sort(np.concatenate([pos, neg]))
    rest = np.setdiff1d(np.arange(len(y)), tr)
    rate = y[rest].mean()
    n_pos = int(round(N_VAL * rate))
    vpos = rng.choice(rest[y[rest] == 1], n_pos, replace=False)
    vneg = rng.choice(rest[y[rest] == 0], N_VAL - n_pos, replace=False)
    return tr, np.sort(np.concatenate([vpos, vneg]))


def prepare(seed: int) -> dict:
    import data as dmod
    import f166_ulb_algorithms as f166
    import pandas as pd
    b = fold()
    X, y = b["Xtr"], b["ytr"]
    med = X.median()
    Xf = X.fillna(med).fillna(0.0)
    sub = f166.stratified_rows(y, MI_ROWS, seed)
    feats = dmod.top_k_features(Xf.iloc[sub], pd.Series(y[sub]),
                                f106.N_QUBITS, seed=seed)
    tr, va = draw_rows(y, seed)
    A = Xf[feats].to_numpy(np.float64)
    Xte = b["Xev"].fillna(med).fillna(0.0)[feats].to_numpy(np.float64)
    ph = f106.Phases(A[tr])
    return {"feats": feats, "rows": tr, "Ptr": ph(A[tr]), "ytr": y[tr],
            "Pva": ph(A[va]), "yva": y[va], "Pte": ph(Xte),
            "yte": b["yev"].astype(int)}


def seed_run(seed: int) -> tuple[dict, dict]:
    import outcome_record as orec
    from sklearn.metrics import average_precision_score, roc_auc_score
    d = prepare(seed)
    t0 = time.perf_counter()
    params, trace = f106.train_circuit(d["Ptr"], d["ytr"], seed, f106.STEPS)
    train_s = time.perf_counter() - t0
    t0 = time.perf_counter()
    scores = {"circuit": f106.predict(params, d["Pte"])}
    predict_s = time.perf_counter() - t0
    twins, sec = f106.twin_scores(d["Ptr"], d["ytr"], d["Pva"], d["yva"],
                                  d["Pte"], seed)
    scores.update(twins)
    yte = d["yte"]
    base = float(yte.mean())
    lanes = {}
    for k, p in scores.items():
        a = float(average_precision_score(yte, p))
        lanes[k] = {"auprc": a, "auroc": float(roc_auc_score(yte, p)),
                    "norm_auprc": (a - base) / (1 - base),
                    "outcome": orec.record(f"f157_qnn_{k}", seed, yte, p)}
    diag = np.random.default_rng(seed).choice(len(d["Ptr"]), f106.DIAG_ROWS,
                                              replace=False)
    row = {"seed": seed, "features": d["feats"], "n_train": int(len(d["rows"])),
           "n_train_pos": int(d["ytr"].sum()), "n_test": int(len(yte)),
           "n_test_pos": int(yte.sum()), "lanes": lanes,
           "lambdas": [round(float(v), 4) for v in params.lam],
           "loss_trace": trace,
           "diagnostics": f106.diagnostics(params, d["Ptr"][diag]),
           "seconds": {"circuit_train": round(train_s, 1),
                       "circuit_predict": round(predict_s, 1),
                       **{k: v for k, v in sec.items()
                          if k.startswith("seconds")}}}
    print(f"  s{seed} " + " ".join(f"{k} {v['auprc']:.4f}"
                                   for k, v in lanes.items())
          + f" C {row['diagnostics']['C']} {row['seconds']}", flush=True)
    return row, scores


def seed_plan(pilot_s: float) -> dict:
    """Eight seeds if they fit in 4 hours; else as many as fit, at least 5."""
    fit = math.floor(LIMIT_S / pilot_s) if pilot_s > 0 else len(SEEDS)
    n = max(MIN_SEEDS, min(len(SEEDS), fit))
    return {"pilot_s": round(pilot_s, 1),
            "projected_s": round(pilot_s * len(SEEDS), 1),
            "n_seeds": n, "cut": n < len(SEEDS)}


def stored(row: dict, lane: str) -> np.ndarray:
    f = ROOT / row["lanes"][lane]["outcome"]["test_scores"]["path"]
    return np.load(f, allow_pickle=False)["p_test"]


def _doc(rows, plan, complete=False, cmp=None) -> dict:
    doc = {"card": "F157", "part": "QNN", "sprint": 31, "phase": 2,
           "evidence_tag": "SIM", "metered_seconds": 0,
           "entry": "experiments/phase2/PREREGISTRATION_DRAFT.md section 6, "
                    "F106, amendment 2026-11-05 (F157 QNN part)",
           "dataset": "ieee-cis month 4 (F174's test fold)",
           "seeds": [r["seed"] for r in rows], "seed_plan": plan,
           "alpha_each": f106.ALPHA, "margin": f106.MARGIN,
           "n_boot": f106.N_BOOT, "steps": f106.STEPS, "rows": rows,
           "complete": complete}
    if cmp is not None:
        doc["compare"] = cmp
        doc["outcome"] = f106.outcome(cmp)
        doc["encoding_built_wrong"] = bool(np.mean(
            [r["diagnostics"]["C"] for r in rows]) < f106.C_FLOOR)
    return doc


def main(argv=None) -> int:
    import provenance
    argv = sys.argv[1:] if argv is None else argv
    mode = argv[0] if argv else ""
    if mode not in ("pilot", "run"):
        raise SystemExit("usage: f157_qnn_ieee.py pilot|run")
    if mode == "pilot":
        rid, _ = provenance.start(OUT_PILOT, resumable=False)
        t0 = time.perf_counter()
        fold()
        build_s = time.perf_counter() - t0
        t0 = time.perf_counter()
        row, _ = seed_run(SEEDS[0])
        plan = seed_plan(time.perf_counter() - t0)
        plan["fold_build_s"] = round(build_s, 1)
        doc = _doc([row], plan, complete=True)
        provenance.write_result(OUT_PILOT, doc, __file__, [SEEDS[0]], rid)
        print("plan", plan)
        print("complete", flush=True)
        return 0
    pilot = json.loads(OUT_PILOT.read_text(encoding="utf-8"))
    plan = pilot["seed_plan"]
    rid, resume = provenance.start(OUT)
    rows = json.loads(OUT.read_text(encoding="utf-8"))["rows"] if resume else []
    seeds = SEEDS[:plan["n_seeds"]]
    for s in seeds:
        if s in {r["seed"] for r in rows}:
            continue           # resume: never redo a seed
        row, _ = seed_run(s)
        rows.append(row)
        provenance.write_result(OUT, _doc(rows, plan), __file__,
                                [r["seed"] for r in rows], rid)
    ys = {r["seed"]: np.load(ROOT / r["lanes"]["circuit"]["outcome"][
        "test_scores"]["path"], allow_pickle=False)["y_test"] for r in rows}
    scores = {r["seed"]: {k: stored(r, k) for k in r["lanes"]} for r in rows}
    cmp = f106.compare(list(seeds), ys, scores)
    doc = _doc(rows, plan, complete=True, cmp=cmp)
    provenance.write_result(OUT, doc, __file__, list(seeds), rid)
    print("outcome:", doc["outcome"])
    print("complete", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
