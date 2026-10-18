"""F112 (Sprint 27 Task D): Experiment 1's paired intervals.

The entry is `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6,
"Experiment 1 (F112)", written before this ran. Reads the stored Phase 1
proxy predictions of three ULB corners and writes nothing under
`experiments/results/`:

    free  k=13, order 2   640ed4cf9c46ea4b
    mid   k=17, order 2   1e6bf03caab3676b
    deep  k=13, order 3   47012b1404d5d4de

    order effect = deep - free     (P1: positive)
    k effect     = mid  - free     (P2: equivalent to zero within 0.005)

Primary (family m = 2, Bonferroni, each at alpha 0.025): the exact
two-sided Wilcoxon test on the 10 per-seed AUPRC deltas, and a paired
bootstrap interval on the across-seed mean delta: each replicate resamples
every seed's test rows stratified by label, with the same indices for both
arms, and averages the 10 per-seed deltas; 2,000 replicates; 97.5%
percentile interval. Secondary: per-seed BCa (`metrics.paired_delta_ci`),
floor-normalized AUPRC and AUROC deltas, and the interaction against
F144's twin (seed-level, Inferred).

Zero metered seconds. Writes `experiments/phase2/results/f112_intervals.json`.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
from scipy import stats
from sklearn.metrics import average_precision_score, roc_auc_score

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "experiments" / "src"))
import metrics                                       # noqa: E402

PRED = ROOT / "experiments" / "results" / "predictions"
OUT = ROOT / "experiments" / "phase2" / "results" / "f112_intervals.json"
F144 = ROOT / "experiments" / "phase2" / "results" / "f144_proxy_twin.json"
CELLS = {"free": "640ed4cf9c46ea4b", "mid": "1e6bf03caab3676b",
         "deep": "47012b1404d5d4de"}
EFFECTS = {"order": ("deep", "free"), "k": ("mid", "free")}
SEEDS = tuple(range(42, 52))
ALPHA = 0.05 / 2
MARGIN = 0.005
N_BOOT = 2000


def load(cell: str, seed: int):
    d = np.load(PRED / f"cvqboost_proxy_{CELLS[cell]}_stratified_{seed}.npz")
    return d["y_test"].astype(int), d["p_test"].astype(np.float64)


def norm_ap(y, p) -> float:
    base = float(y.mean())
    return (average_precision_score(y, p) - base) / (1.0 - base)


def main() -> int:
    data = {s: {c: load(c, s) for c in CELLS} for s in SEEDS}
    for s in SEEDS:
        ys = [data[s][c][0] for c in CELLS]
        if not all(np.array_equal(ys[0], y) for y in ys[1:]):
            raise SystemExit(f"REFUSING: test labels differ across arms on "
                             f"seed {s}; the pairing is broken")
    out: dict = {}
    for eff, (a, b) in EFFECTS.items():
        per_seed, boot = [], np.zeros((len(SEEDS), N_BOOT))
        for i, s in enumerate(SEEDS):
            y, pa = data[s][a]
            _, pb = data[s][b]
            rng = np.random.default_rng(1000 + s)
            for j, idx in enumerate(metrics.stratified_indices(y, rng, N_BOOT)):
                boot[i, j] = (average_precision_score(y[idx], pa[idx])
                              - average_precision_score(y[idx], pb[idx]))
            bca = metrics.paired_delta_ci(y, pa, pb, "auprc", seed=s)
            per_seed.append({
                "seed": s, "delta_auprc": bca["diff"],
                "bca_ci95": bca["ci95"],
                "delta_norm_auprc": norm_ap(y, pa) - norm_ap(y, pb),
                "delta_auroc": float(roc_auc_score(y, pa)
                                     - roc_auc_score(y, pb))})
            print(f"  {eff} s{s} {bca['diff']:+.4f} {bca['ci95']}", flush=True)
        d = np.array([r["delta_auprc"] for r in per_seed])
        mean_boot = boot.mean(axis=0)
        lo, hi = np.percentile(mean_boot, [100 * ALPHA / 2,
                                           100 * (1 - ALPHA / 2)])
        w = stats.wilcoxon(d, alternative="two-sided", method="exact")
        entry = {"arms": f"{a} - {b}", "n_seeds": len(SEEDS),
                 "mean_delta_auprc": float(d.mean()),
                 "interval_975": [float(lo), float(hi)],
                 "wilcoxon_p_exact": float(w.pvalue),
                 "seeds_positive": int((d > 0).sum()),
                 "mean_delta_norm_auprc": float(np.mean(
                     [r["delta_norm_auprc"] for r in per_seed])),
                 "mean_delta_auroc": float(np.mean(
                     [r["delta_auroc"] for r in per_seed])),
                 "per_seed": per_seed}
        if eff == "order":
            entry["p1_holds"] = bool(lo > 0 and w.pvalue < ALPHA
                                     and d.mean() > 0)
        else:
            inside = bool(-MARGIN <= lo and hi <= MARGIN)
            entry["p2_equivalent_within_margin"] = inside
            entry["p2_reading"] = ("equivalent" if inside else
                                   "inconclusive" if lo <= 0 <= hi else
                                   "differs")
        out[eff] = entry

    # Secondary, Inferred: the interaction against F144's twin of the fourth
    # corner (k=17, order 3), seed-level; seeded pools against unseeded.
    twin = {r["seed"]: r["twin"]["auprc"]
            for r in json.loads(F144.read_text(encoding="utf-8"))["rows"]}
    ap = {c: {s: average_precision_score(*data[s][c]) for s in SEEDS}
          for c in CELLS}
    inter = [twin[s] - ap["mid"][s] - ap["deep"][s] + ap["free"][s]
             for s in SEEDS if s in twin]
    out["interaction_secondary"] = {
        "formula": "twin(k17,o3) - mid - deep + free, per seed",
        "n_seeds": len(inter), "mean": float(np.mean(inter)),
        "seed_sd": float(np.std(inter, ddof=1)),
        "label": "Inferred: the twin's pools are seeded rebuilds and the "
                 "three corners' are unseeded Phase 1 pools (F145 drift); "
                 "AUPRC only, F144 stored no predictions"}
    OUT.write_text(json.dumps({
        "generator": "experiments/phase2/src/f112_intervals.py",
        "card": "F112", "experiment": 1, "sprint": 27, "phase": 2,
        "evidence_tag": "SIM", "metered_seconds": 0,
        "date": time.strftime("%Y-%m-%d"),
        "entry": "experiments/phase2/PREREGISTRATION_DRAFT.md section 6, "
                 "Experiment 1 (F112)",
        "alpha_each": ALPHA, "margin": MARGIN, "n_boot": N_BOOT,
        "cells": CELLS, **out}, indent=1) + "\n", encoding="utf-8")
    for eff in EFFECTS:
        e = out[eff]
        print(eff, round(e["mean_delta_auprc"], 4),
              [round(x, 4) for x in e["interval_975"]],
              round(e["wilcoxon_p_exact"], 5))
    print(out["interaction_secondary"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
