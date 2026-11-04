"""F171 amendment (Sprint 30 Task H, #82; Decision D7, option 1): the
missed-by-all count at higher alert budgets, on both datasets.

POST HOC. The entry's 0.5% budget is F171's recorded result
(`f171_missed_ieee.json`) and is not replaced. At 0.5% one IEEE-CIS
family can flag at most 14% of a month's frauds, so the count measures
the budget more than the models. This module adds, by the dated
amendment to "F171" in `experiments/phase2/PREREGISTRATION_DRAFT.md`
section 6, written after the 0.5% result was seen:

- `fixed_3.5`: a 3.5% budget, about IEEE-CIS's fraud rate;
- `matched`: 3.0 times each fold's own test fraud rate, the ratio ULB's
  0.5% has (about 10.4% on IEEE-CIS, 0.5% on ULB).

Each is counted on IEEE-CIS (F171's families, months and checks) and on
ULB (F158 step 3's on-split families and seeds). The 0.5% count is
recomputed first and must equal the recorded F171 and F158 counts, or
the run stops. Descriptive: no test.

    <venv python> experiments/phase2/src/f171_budgets.py

Zero metered seconds. Writes `experiments/phase2/results/f171_budgets.json`
through `provenance.write_result`.
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

OUT = ROOT / "experiments" / "phase2" / "results" / "f171_budgets.json"
F171 = ROOT / "experiments" / "phase2" / "results" / "f171_missed_ieee.json"
LONG_RUN = False                       # minutes; one pass, not resumable
RECORDED = 0.005                       # the entry's budget, recomputed first
FIXED = 0.035
RATIO = 3.0                            # ULB's 0.5% over its test fraud rate


def budgets(y) -> dict:
    """The three budgets for one fold, from its own test fraud rate."""
    return {"recorded_0.5": RECORDED, "fixed_3.5": FIXED,
            "matched": min(1.0, RATIO * float(np.mean(np.asarray(y) == 1)))}


def count(y, scores: list, budget: float) -> dict:
    """Frauds no family flags at `budget`, and the share that capacity
    alone forces: with k alerts each, f families flag at most f * k."""
    import f158_fraud_types as f158
    import outcome_record as orec
    y = np.asarray(y).astype(int)
    miss = f158.missed_by_all(y, [orec.flagged_at_budget(p, budget)
                                  for p in scores])
    frauds = int(y.sum())
    k = math.ceil(budget * len(y))
    return {"budget": budget, "alerts_per_family": k, "frauds": frauds,
            "missed_by_all": int(miss.sum()),
            "capacity_floor": max(0, frauds - len(scores) * k)}


def total(rows: list, name: str) -> dict:
    sel = [r[name] for r in rows]
    missed = sum(c["missed_by_all"] for c in sel)
    frauds = sum(c["frauds"] for c in sel)
    floor = sum(c["capacity_floor"] for c in sel)
    return {"missed": missed, "frauds": frauds, "share": missed / frauds,
            "capacity_floor_share": floor / frauds,
            "mean_budget": float(np.mean([c["budget"] for c in sel]))}


def check_recorded(name: str, got: dict, want: tuple[int, int]) -> None:
    """The 0.5% count must be the recorded one before any new figure."""
    if (got["missed"], got["frauds"]) != tuple(want):
        raise ValueError(f"{name}: recomputed 0.5% count {got['missed']} of "
                         f"{got['frauds']} is not the recorded {want[0]} of "
                         f"{want[1]}; no other budget is counted")


def ieee_folds():
    """(month, seed, labels, scores) on F171's families and checks."""
    import data
    import f158_fraud_types as f158
    import f171_missed_ieee as f171
    import ieee_harness as ih
    import ieee_loader
    scores = json.loads(f171.F152.read_text(encoding="utf-8"))["scores"]
    df, _ = ieee_loader.dedupe_ieee(data.load_ieee_cis_train())
    folds = {int(f.eval_month): f for f in ih.folds_for(df)}
    for month in sorted(scores, key=int):
        y = df.loc[folds[int(month)].eval_idx, "isFraud"].to_numpy().astype(int)
        lanes = scores[month]
        for seed in sorted({r["seed"] for recs in lanes.values() for r in recs}):
            ps = []
            for fam, recs in sorted(lanes.items()):
                rec = next((r for r in recs if r["seed"] == seed), None)
                if rec is None:
                    continue
                ys, p = f171.stored(rec)
                if not f158.on_split(ys, y):
                    raise ValueError(f"{fam} month {month} seed {seed}: stored "
                                     "labels are not the fold's, in order")
                ps.append(p)
            yield int(month), seed, y, ps


def ulb_folds():
    """(seed, labels, scores) on F158 step 3's on-split families."""
    import data
    import f154_confusion as fcf
    import f158_fraud_types as f158
    df = data.load_ulb().drop_duplicates().reset_index(drop=True)
    for seed in fcf.SEEDS:
        x_te = fcf.test_features(seed, df)
        y = df.loc[x_te.index, data.LABEL_COL].to_numpy().astype(int)
        ps = [st["p_test"] for st in (fcf.load(f, seed) for f in fcf.families())
              if f158.on_split(st["y_test"], y)]
        yield seed, y, ps


def per_fold(y, ps) -> dict:
    return {name: count(y, ps, b) for name, b in budgets(y).items()}


def summarize(rows: list) -> dict:
    return {name: total(rows, name) for name in budgets([0, 1])}


def run() -> dict:
    import f158_fraud_types as f158
    rec171 = json.loads(F171.read_text(encoding="utf-8"))["pairs"]
    rec158 = json.loads(f158.OUT.read_text(encoding="utf-8"))
    s3 = rec158["step3_ulb_missed_by_all"]["per_seed"]
    want_ulb = (sum(r["missed_by_all"] for r in s3), sum(r["frauds"] for r in s3))
    ieee = [{"eval_month": m, "seed": s, "families": len(ps), **per_fold(y, ps)}
            for m, s, y, ps in ieee_folds()]
    ulb = [{"seed": s, "families": len(ps), **per_fold(y, ps)}
           for s, y, ps in ulb_folds()]
    out = {"ieee": {"per_fold": ieee, "totals": summarize(ieee)},
           "ulb": {"per_fold": ulb, "totals": summarize(ulb)}}
    check_recorded("IEEE-CIS", out["ieee"]["totals"]["recorded_0.5"],
                   (rec171["missed"], rec171["frauds"]))
    check_recorded("ULB", out["ulb"]["totals"]["recorded_0.5"], want_ulb)
    return out


def main() -> int:
    import provenance
    rid, _ = provenance.start(OUT, resumable=False)
    t0 = time.perf_counter()
    res = run()
    doc = {"card": "F171", "sprint": 30, "phase": 2, "evidence_tag": "SIM",
           "metered_seconds": 0, "post_hoc": True,
           "entry": "experiments/phase2/PREREGISTRATION_DRAFT.md section 6, "
                    "F171, amendment 2026-10-31 (Decision D7)",
           "budgets": {"recorded_0.5": RECORDED, "fixed_3.5": FIXED,
                       "matched": f"{RATIO} x the fold's test fraud rate"},
           **res, "test": "none (descriptive)",
           "seconds": round(time.perf_counter() - t0, 1), "complete": True}
    seeds = sorted({r["seed"] for d in ("ieee", "ulb")
                    for r in res[d]["per_fold"]})
    provenance.write_result(OUT, doc, __file__, seeds, rid)
    print(json.dumps({d: {n: round(t["share"], 4) for n, t in res[d]["totals"].items()}
                      for d in ("ieee", "ulb")}))
    print("complete", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
