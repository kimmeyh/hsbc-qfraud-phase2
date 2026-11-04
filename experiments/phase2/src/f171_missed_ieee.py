"""F171 (Sprint 30 Task H, #82): F158 step 3 on IEEE-CIS, do richer
features shrink the group every model misses?

The entry is "F171" in `experiments/phase2/PREREGISTRATION_DRAFT.md`
section 6, committed before this module existed. F158's step 3, counted
the same way, on F152's four stored IEEE-CIS families (xgboost, lightgbm,
hgb, logistic), months 4-6, seeds 42-46: a (month, seed, test fraud) is
missed by all when no family flags it at the 0.5% alert budget. Each
family's stored labels must equal the fold's own evaluation labels, in
order, and each score file must still hash to its outcome block, before
it is used. The missed against caught profile reads raw IEEE-CIS fields.
Descriptive: no test, and the comparison with ULB is not causal.

    <venv python> experiments/phase2/src/f171_missed_ieee.py

Zero metered seconds. Writes `experiments/phase2/results/f171_missed_ieee.json`
through `provenance.write_result`.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "experiments" / "src"))

OUT = ROOT / "experiments" / "phase2" / "results" / "f171_missed_ieee.json"
F152 = ROOT / "experiments" / "phase2" / "results" / "f152_exp2.json"
F158 = ROOT / "experiments" / "phase2" / "results" / "f158_fraud_types.json"
LONG_RUN = False                       # minutes; one pass, not resumable
NUMERIC = ("TransactionAmt", "dist1", "C1", "C13", "D1")
CATEGORICAL = ("ProductCD", "card4", "card6", "P_emaildomain", "DeviceType")


def stored(rec: dict) -> tuple[np.ndarray, np.ndarray]:
    """One family's labels and scores for one (month, seed), from its
    outcome block's file, checked against the block's SHA-256."""
    import outcome_record as orec
    ts = rec["outcome"]["test_scores"]
    path = ROOT / ts["path"]
    got = orec.sha256_of(path)
    if got != ts["sha256"]:
        raise ValueError(f"{ts['path']}: SHA-256 {got} does not match the "
                         f"recorded {ts['sha256']}")
    z = np.load(path)
    return z["y_test"].astype(int), np.asarray(z["p_test"], float)


def profile(raw, missed: np.ndarray, caught: np.ndarray) -> dict:
    out = {}
    for c in NUMERIC:
        if c in raw:
            m, k = raw.loc[missed, c], raw.loc[caught, c]
            out[c] = {"missed_median": float(m.median()),
                      "caught_median": float(k.median()),
                      "missed_missing": float(m.isna().mean()),
                      "caught_missing": float(k.isna().mean())}
    for c in CATEGORICAL:
        if c in raw:
            m = raw.loc[missed, c].fillna("(missing)").value_counts(normalize=True)
            k = raw.loc[caught, c].fillna("(missing)").value_counts(normalize=True)
            top = list(dict.fromkeys(list(m.index[:5]) + list(k.index[:5])))
            out[c] = {str(v): {"missed": float(m.get(v, 0.0)),
                               "caught": float(k.get(v, 0.0))} for v in top}
    return out


def ulb_share() -> dict:
    """F158 step 3's ULB count, read from its recorded result."""
    s = json.loads(F158.read_text(encoding="utf-8"))
    s = s.get("step3_ulb_missed_by_all") or s["analysis"]["step3_ulb_missed_by_all"]
    missed = sum(r["missed_by_all"] for r in s["per_seed"])
    frauds = sum(r["frauds"] for r in s["per_seed"])
    return {"missed": missed, "frauds": frauds, "share": missed / frauds}


def run() -> dict:
    import pandas as pd
    import data
    import f158_fraud_types as f158
    import ieee_harness as ih
    import ieee_loader
    import outcome_record as orec
    f152 = json.loads(F152.read_text(encoding="utf-8"))
    scores = f152["scores"]
    df, _ = ieee_loader.dedupe_ieee(data.load_ieee_cis_train())
    folds = {int(f.eval_month): f for f in ih.folds_for(df)}
    per, missed_idx, caught_idx, fams_used = [], [], [], set()
    for month in sorted(scores, key=int):
        fold = folds[int(month)]
        y = df.loc[fold.eval_idx, "isFraud"].to_numpy().astype(int)
        lanes = scores[month]
        seeds = sorted({r["seed"] for recs in lanes.values() for r in recs})
        for seed in seeds:
            flags, used = [], []
            for fam, recs in sorted(lanes.items()):
                rec = next((r for r in recs if r["seed"] == seed), None)
                if rec is None:
                    continue
                ys, p = stored(rec)
                if not f158.on_split(ys, y):
                    raise ValueError(f"{fam} month {month} seed {seed}: stored "
                                     "labels are not the fold's, in order")
                flags.append(orec.flagged_at_budget(p, orec.ALERT_BUDGET))
                used.append(fam)
            fams_used.update(used)
            miss = f158.missed_by_all(y, flags)
            idx = np.asarray(fold.eval_idx)
            missed_idx += list(idx[miss])
            caught_idx += list(idx[(y == 1) & ~miss])
            per.append({"eval_month": int(month), "seed": seed,
                        "families": used, "frauds": int(y.sum()),
                        "missed_by_all": int(miss.sum()),
                        "share": float(miss.sum() / y.sum())})
    frauds = sum(r["frauds"] for r in per)
    missed = sum(r["missed_by_all"] for r in per)
    by_month = {}
    for r in per:
        b = by_month.setdefault(str(r["eval_month"]), {"frauds": 0, "missed": 0})
        b["frauds"] += r["frauds"]
        b["missed"] += r["missed_by_all"]
    for b in by_month.values():
        b["share"] = b["missed"] / b["frauds"]
    distinct_missed = sorted(set(int(i) for i in missed_idx))
    raw = df.drop(columns=[c for c in df.columns if c == "isFraud"])
    return {"families": sorted(fams_used), "per_month_seed": per,
            "by_month": by_month,
            "pairs": {"missed": missed, "frauds": frauds,
                      "share": missed / frauds},
            "distinct_missed_rows": len(distinct_missed),
            "ulb_f158_step3": ulb_share(),
            "profile": profile(raw, pd.Index(sorted(set(missed_idx))),
                               pd.Index(sorted(set(caught_idx)))),
            "test": "none (descriptive)"}


def main() -> int:
    import provenance
    rid, _ = provenance.start(OUT, resumable=False)
    t0 = time.perf_counter()
    res = run()
    doc = {"card": "F171", "sprint": 30, "phase": 2, "evidence_tag": "SIM",
           "metered_seconds": 0,
           "entry": "experiments/phase2/PREREGISTRATION_DRAFT.md section 6, "
                    "F171",
           "source": "f152_exp2.json's outcome blocks and score files",
           **res, "seconds": round(time.perf_counter() - t0, 1),
           "complete": True}
    provenance.write_result(OUT, doc, __file__, [42, 43, 44, 45, 46], rid)
    print(json.dumps({"pairs": res["pairs"], "ulb": res["ulb_f158_step3"]}))
    print("complete", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
