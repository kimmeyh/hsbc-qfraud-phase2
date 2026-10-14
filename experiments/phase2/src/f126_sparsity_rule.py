"""F126 (Sprint 26 Task F): a rule for the device's exact zeros, tested on
fits it was not fitted to.

FIXED BEFORE ANY FIT (this file was committed before it was first run):

- **Target**: the exact-zero fraction of each B4 fit's lowest-energy device
  sample (`experiments/phase2/results/device_samples/`, 10 fits: 5
  oilgas_gasturbine, 5 telecom_churn), as F17 measured it.
- **Primary rule, R1 (relative threshold)**: the device zeroes every
  learner whose weight in the exact proxy optimum is below tau / n, where
  n is the pool size. One parameter, tau, scale-free across pool sizes.
  Predicted zero fraction = fraction of exact weights below tau / n.
- **Fit**: tau on a grid from 0 to 3 in steps of 0.001, minimizing the
  mean absolute error over the 5 training fits.
- **Test**: the mean absolute error over the 5 held-out fits. **Pass iff
  at most 0.05**, in BOTH directions (fit on oilgas, test on telecom; and
  the reverse). Plan, `docs/sprints/SPRINT_26_PLAN.md` Task F.
- **Reported beside it, not tests**: R2, an absolute threshold t on the
  exact weight (same fit and test); R0, the reference "predict the other
  dataset's mean zero fraction", which the plan showed fails by about
  0.21; and B5's 12 QSVM fits' zero fractions, descriptive only.

LIMITATION, stated before the fit: the device's pools were built unseeded
and never stored, so the exact optimum is computed on a REBUILT pool
(seeded, F145). The comparison is of fractions, never of weights index by
index. If the rule fails, the rebuild drift is one candidate explanation,
and the write-up says so.

Zero metered seconds. Pools are cached in experiments/phase2/results/pools/
(ignored). Output: experiments/phase2/results/f126_sparsity_rule.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "experiments" / "src"))
import qubo_proxy as qp  # noqa: E402
import spectra_segment as ss  # noqa: E402

SAMPLES = ROOT / "experiments" / "phase2" / "results" / "device_samples"
POOLS = ROOT / "experiments" / "phase2" / "results" / "pools"
OUT = ROOT / "experiments" / "phase2" / "results" / "f126_sparsity_rule.json"
DATASETS = ("oilgas_gasturbine", "telecom_churn")
SEEDS = (42, 43, 44, 45, 46)
TOLERANCE = 0.05
TAU_GRID = np.round(np.arange(0.0, 3.0 + 1e-9, 0.001), 3)


def zero_fraction(w) -> float:
    """Exactly 0.0 only, as F17 measured it."""
    return float((np.asarray(w, dtype=np.float64) == 0.0).mean())


def device_best(name: str, seed: int) -> np.ndarray:
    d = json.loads((SAMPLES / f"b4_{name}_stratified_{seed}.json")
                   .read_text(encoding="utf-8"))
    return np.asarray(d["solutions"][int(np.argmin(d["energies"]))],
                      dtype=np.float64)


def exact_weights(name: str, seed: int) -> np.ndarray:
    """The exact proxy optimum on a seeded rebuild of the B4 pool, cached."""
    cache = POOLS / f"f126_{name}_{seed}_wexact.npy"
    if cache.exists():
        return np.load(cache)
    c = ss.frozen_cell_by_name(name)["config"]
    split, cols = ss._prep_spectra(name, seed)
    Xtr = ss.coerce_features_to_numeric(split.X_train[cols]).to_numpy(
        "float32")
    y_pm1 = np.where(split.y_train.to_numpy() == 1, 1, -1)
    lam = c["lambda_coef_alpha"] * len(y_pm1)
    clf = qp.build_pool(Xtr, y_pm1, c["weak_cls_schedule"], "dct",
                        "sequential",
                        weak_params=qp.seeded_weak_params(
                            seed, c["weak_cls_params"]),
                        lambda_coef=lam)
    w = qp.solve_simplex_qp(qp.h_matrix(clf, Xtr), y_pm1, lam)
    POOLS.mkdir(parents=True, exist_ok=True)
    np.save(cache, w)
    return w


def r1_pred(w: np.ndarray, tau: float) -> float:
    return float((w < tau / w.size).mean())


def r2_pred(w: np.ndarray, t: float) -> float:
    return float((w < t).mean())


def fit_and_test(train, test, pred, grid) -> dict:
    """train/test: lists of (exact weights, device zero fraction)."""
    def mae(fits, p):
        return float(np.mean([abs(pred(w, p) - z) for w, z in fits]))
    errs = [mae(train, p) for p in grid]
    best = float(grid[int(np.argmin(errs))])
    held = [pred(w, best) - z for w, z in test]
    return {"param": best, "train_mae": float(min(errs)),
            "test_mae": float(np.mean(np.abs(held))),
            "test_max_abs_error": float(np.max(np.abs(held))),
            "test_errors": [float(e) for e in held],
            "passes": bool(np.mean(np.abs(held)) <= TOLERANCE)}


def b5_descriptive() -> list[dict]:
    out = []
    for f in sorted(SAMPLES.glob("b5_*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        best = d["solutions"][int(np.argmin(d["energies"]))]
        out.append({"file": f.name, "n": len(best),
                    "zero_fraction": round(zero_fraction(best), 4)})
    return out


def main() -> int:
    fits = {}
    for name in DATASETS:
        fits[name] = []
        for seed in SEEDS:
            w = exact_weights(name, seed)
            dev = device_best(name, seed)
            assert w.size == dev.size, f"{name} {seed}: {w.size} vs {dev.size}"
            fits[name].append((w, zero_fraction(dev)))
            print(f"  {name:18s} s{seed} n={w.size} device "
                  f"{zero_fraction(dev):.4f} exact {zero_fraction(w):.4f}",
                  flush=True)

    t_grid = np.round(np.arange(0.0, 0.01 + 1e-12, 0.00001), 5)
    directions = {}
    for a, b in (DATASETS, DATASETS[::-1]):
        key = f"fit_{a}_test_{b}"
        mean_a = float(np.mean([z for _, z in fits[a]]))
        r0 = [mean_a - z for _, z in fits[b]]
        directions[key] = {
            "R1_relative_threshold": fit_and_test(fits[a], fits[b], r1_pred,
                                                  TAU_GRID),
            "R2_absolute_threshold": fit_and_test(fits[a], fits[b], r2_pred,
                                                  t_grid),
            "R0_reference_other_mean": {
                "test_mae": float(np.mean(np.abs(r0))),
                "passes": bool(np.mean(np.abs(r0)) <= TOLERANCE)},
        }
    primary_pass = all(d["R1_relative_threshold"]["passes"]
                       for d in directions.values())
    doc = {
        "generator": "experiments/phase2/src/f126_sparsity_rule.py",
        "card": "F126", "sprint": 26, "evidence_tag": "SIM",
        "metered_seconds": 0, "tolerance": TOLERANCE,
        "primary_rule": "R1: zero iff exact weight < tau / n",
        "primary_passes_both_directions": primary_pass,
        "directions": directions,
        "fits": {n: [{"seed": s, "n": int(w.size),
                      "device_zero_fraction": round(z, 4),
                      "exact_zero_fraction": round(zero_fraction(w), 4)}
                     for s, (w, z) in zip(SEEDS, fits[n])]
                 for n in DATASETS},
        "b5_descriptive_only": b5_descriptive(),
        "limitation": "exact weights are from seeded rebuilds of the B4 "
                      "pools; the device's own pools were never stored",
    }
    OUT.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
    for k, d in directions.items():
        print(k, {r: {kk: round(v, 4) if isinstance(v, float) else v
                      for kk, v in d[r].items() if kk != "test_errors"}
                  for r in d})
    print("PRIMARY passes both directions:", primary_pass)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
