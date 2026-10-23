"""F109 (Sprint 27 Task G): Tier 1 across the six datasets on disk, and
the IEEE-CIS UID aggregation before and after.

The entry is `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6,
"F109", written before this module existed. Tier 1 is F103's code,
unchanged (`f103_tier1.run_target`), so every value is comparable with
F103's known-answer check. UCI Steel is F103's five rows, cited.

    <venv python> experiments/phase2/src/f109_ladder.py pilot
    <venv python> experiments/phase2/src/f109_ladder.py run

The pilot is one seed with IEEE-CIS on a 10% time-ordered sample
(`ieee_harness.time_sample`). Zero metered seconds. Writes
`experiments/phase2/results/f109_ladder.json` (the pilot writes
`f109_ladder_pilot.json`).
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "experiments" / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import f103_tier1 as t1                              # noqa: E402  (Phase 2)

OUT = ROOT / "experiments" / "phase2" / "results" / "f109_ladder.json"
OUT_PILOT = OUT.with_name("f109_ladder_pilot.json")
F103 = ROOT / "experiments" / "phase2" / "results" / "f103_tier1.json"
SEEDS = (42, 43, 44, 45, 46)
SPECTRA = ("maintenance_ai4i", "oilgas_gasturbine", "telecom_churn")
N_SUB, MAX_POS, D_TOP = 30_000, 3_000, 6
MISSING = -999.0
PILOT_FRAC = 0.10
PILOT_LIMIT_S = 3 * 3600
G4_SMALL = 0.02


def spectra_phases(name: str) -> tuple[np.ndarray, np.ndarray, list]:
    import data
    df = data.load_spectra(name)
    cols = [c for c in df.columns if c.endswith("_phase")]
    P = t1.whiten_rerank(df[cols].to_numpy(dtype=np.float64))
    return P, df["target_real"].to_numpy().astype(int), cols


def subsample(y: np.ndarray, seed: int) -> np.ndarray:
    """N_SUB rows: every positive up to MAX_POS, the rest negatives."""
    rng = np.random.default_rng(seed)
    pos, neg = np.flatnonzero(y == 1), np.flatnonzero(y == 0)
    pos = rng.choice(pos, min(len(pos), MAX_POS), replace=False)
    neg = rng.choice(neg, N_SUB - len(pos), replace=False)
    return np.sort(np.concatenate([pos, neg]))


def top_phases(X: pd.DataFrame, y: np.ndarray, tr: np.ndarray,
               seed: int) -> tuple[np.ndarray, list]:
    """Top D_TOP by mutual information on training rows, then the rank
    phase on all rows, whitened and re-ranked."""
    from sklearn.feature_selection import mutual_info_classif
    X = X.astype(np.float64).fillna(MISSING)
    keep = [c for c in X.columns if X[c].iloc[tr].nunique() > 1]
    mi = mutual_info_classif(X[keep].iloc[tr], y[tr], random_state=seed)
    feats = [keep[i] for i in np.argsort(mi)[::-1][:D_TOP]]
    P = np.column_stack([t1.rank_phase(X[c].to_numpy()) for c in feats])
    return t1.whiten_rerank(P), feats


def ulb_run(seed: int, scores: dict | None = None) -> dict:
    """`scores`, opt-in (Sprint 28 DV4 outcome backfill): passed to
    `f103_tier1.run_target`. The row returned is the same with or without."""
    import data
    df = data.load_ulb()
    y_all = df[data.LABEL_COL].to_numpy().astype(int)
    S = subsample(y_all, seed)
    X = df.drop(columns=[data.LABEL_COL]).iloc[S].reset_index(drop=True)
    y = y_all[S]
    tr, _ = t1._split(len(y), y, seed)
    P, feats = top_phases(X, y, tr, seed)
    row = t1.run_target("ulb", P, y, seed, scores=scores)
    row["features"] = feats
    return row


def ieee_runs(df: pd.DataFrame, seed: int,
              scores: dict | None = None) -> dict:
    """`scores`, opt-in: filled under "before" and "after" as
    `f103_tier1.run_target` describes."""
    import ieee_features

    def sink(k):
        return None if scores is None else scores.setdefault(k, {})
    y_all = df["isFraud"].to_numpy().astype(int)
    S = subsample(y_all, seed)
    y = y_all[S]
    tr, te = t1._split(len(y), y, seed)
    sub = df.iloc[S].reset_index(drop=True)

    raw = sub.drop(columns=["isFraud", "TransactionID", "TransactionDT"])
    raw = raw.select_dtypes(include=[np.number])
    P, feats = top_phases(raw, y, tr, seed)
    before = t1.run_target("ieee_before", P, y, seed, scores=sink("before"))
    before["features"] = feats

    t0 = time.perf_counter()
    pool = df.drop(index=df.index[S[te]]).drop(columns=["isFraud"])
    pipe = ieee_features.IEEEFeaturePipeline()
    pipe.fit_transform(pool)
    agg = pipe.transform(sub.drop(columns=["isFraud"]))
    agg = agg.select_dtypes(include=[np.number])
    assert not any(c in agg.columns for c in ("TransactionID", "TransactionDT"))
    pipe_s = time.perf_counter() - t0
    P, feats = top_phases(agg, y, tr, seed)
    after = t1.run_target("ieee_after", P, y, seed, scores=sink("after"))
    after["features"] = feats
    after["pipeline_seconds"] = round(pipe_s, 1)
    after["uid_features_chosen"] = [f for f in feats if f.startswith("uid_")
                                    or f.endswith("_freq")]
    return {"before": before, "after": after}


def summarize(res: dict) -> dict:
    out = {}
    for name, rows in res["datasets"].items():
        out[name] = {
            "tier1_words": [r["gates"]["tier1"] for r in rows],
            **{g: [r["gates"][g] for r in rows] for g in (
                "g1_rho_off", "g2_gam_auc", "g3_hgb_minus_gam",
                "g4_joint_minus_ga2m", "g5_qubits_q1")}}
    fraud = [n for n in ("ulb", "ieee_before", "ieee_after") if n in out]
    out["falsifier_g4_large"] = {
        n: int(sum(v >= G4_SMALL for v in out[n]["g4_joint_minus_ga2m"]))
        for n in fraud}
    return out


def main(argv=None) -> int:
    import data
    argv = sys.argv[1:] if argv is None else argv
    mode = argv[0] if argv else "pilot"
    if mode not in ("pilot", "run"):
        raise SystemExit("usage: f109_ladder.py pilot|run")
    seeds = SEEDS[:1] if mode == "pilot" else SEEDS
    t_all = time.perf_counter()
    f103 = json.loads(F103.read_text(encoding="utf-8"))
    ds: dict = {"energy_steel": [dict(r, cited="f103_tier1.json")
                                 for r in f103["real"]]}
    timing: dict = {}
    for name in SPECTRA:
        t0 = time.perf_counter()
        P, y, cols = spectra_phases(name)
        ds[name] = [dict(t1.run_target(name, P, y, s), features=cols)
                    for s in seeds]
        timing[name] = round(time.perf_counter() - t0, 1)
    t0 = time.perf_counter()
    ds["ulb"] = [ulb_run(s) for s in seeds]
    timing["ulb"] = round(time.perf_counter() - t0, 1)
    t0 = time.perf_counter()
    cis = data.load_ieee_cis_train()
    if mode == "pilot":
        import ieee_harness
        cis = ieee_harness.time_sample(cis, PILOT_FRAC)
    timing["ieee_load"] = round(time.perf_counter() - t0, 1)
    t0 = time.perf_counter()
    pairs = [ieee_runs(cis, s) for s in seeds]
    timing["ieee"] = round(time.perf_counter() - t0, 1)
    ds["ieee_before"] = [p["before"] for p in pairs]
    ds["ieee_after"] = [p["after"] for p in pairs]
    res = {"generator": "experiments/phase2/src/f109_ladder.py",
           "card": "F109", "sprint": 27, "phase": 2, "evidence_tag": "SIM",
           "metered_seconds": 0, "date": time.strftime("%Y-%m-%d"),
           "entry": "experiments/phase2/PREREGISTRATION_DRAFT.md section 6, "
                    "F109",
           "mode": mode, "seeds": list(seeds),
           "ieee_rows_available": int(len(cis)), "datasets": ds,
           "timing_s": timing}
    res["summary"] = summarize(res)
    res["elapsed_s"] = round(time.perf_counter() - t_all, 1)
    if mode == "pilot":
        # The pipeline fit scales with the rows it sees (10% here); the
        # lanes run on the same 30,000-row subsample either way.
        pipe_s = pairs[0]["after"]["pipeline_seconds"]
        lanes_s = res["elapsed_s"] - timing["ieee_load"] - pipe_s
        res["projected_run_s"] = round(
            len(SEEDS) * (lanes_s + pipe_s / PILOT_FRAC), 1)
        res["run_within_limit"] = bool(res["projected_run_s"] <= PILOT_LIMIT_S)
    (OUT_PILOT if mode == "pilot" else OUT).write_text(
        json.dumps(res, indent=1, default=str) + "\n", encoding="utf-8")
    print(json.dumps(res["summary"], indent=1))
    print("elapsed", res["elapsed_s"], res.get("projected_run_s"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
