"""F110: Experiment 6, training time against sample count, proxy first.

Sprint 28 Task E (#52). Zero metered seconds. The entry is
`experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "Experiment 6",
committed before any timing. Times the three parts of CVQBoost training
on the classical proxy (`qubo_proxy`, Phase 1, read only) at four row
fractions.

Modes:
  free    the 91-variable cell, seeds 42-46
  pilot   the 833-variable cell, seed 42 only, with the five-seed projection
  full    the 833-variable cell, seeds 43-46 (run only if the pilot projects
          five seeds at 120 minutes or less)
  analyze the slopes, from every recorded run

Run:  <venv python> experiments/phase2/src/f110_scaling.py free|pilot|full|analyze
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "experiments" / "src"))

OUT = ROOT / "experiments" / "phase2" / "results" / "f110_scaling.json"
FRACTIONS = (0.10, 0.25, 0.50, 1.00)
CELLS = {"free": "free", "full": "full"}       # qubo_proxy config names
FREE_SEEDS = (42, 43, 44, 45, 46)
FULL_PILOT_SEED = 42
FULL_REST = (43, 44, 45, 46)
PROJECTION_CAP_MIN = 120.0
P1_BAND, P2_BAND = (0.7, 1.3), (-0.2, 0.2)
LEVEL = 1 - 0.05 / 2


def subsample(y01: np.ndarray, frac: float, seed: int) -> np.ndarray:
    """Row indices: `frac` of each class, chosen with the seed, sorted."""
    if frac >= 1.0:
        return np.arange(len(y01))
    rng = np.random.default_rng(seed)
    keep = []
    for c in (0, 1):
        idx = np.nonzero(y01 == c)[0]
        keep.append(rng.choice(idx, max(1, int(round(frac * len(idx)))), replace=False))
    return np.sort(np.concatenate(keep))


def time_one(config: str, seed: int, frac: float) -> dict:
    import full_pair_pool as fpp
    import qubo_proxy as qp
    c = qp.CONFIGS[config]
    split, cols, Xtr, _, _, y_pm1 = qp._prep(seed, c["k"])
    idx = subsample(split.y_train.to_numpy(), frac, seed)
    X, y = Xtr[idx], y_pm1[idx]
    t0 = time.perf_counter()
    # The library's full-pair builder needs fork (absent on Windows); this
    # builds the same learners serially (entry's implementation note).
    clf = fpp.build_full(X, y, c["schedule"], "dct",
                         weak_params=qp.seeded_weak_params(seed))
    t_build = time.perf_counter() - t0
    lam = qp.LAMBDA_MULT * len(y)
    t0 = time.perf_counter()
    H = qp.h_matrix(clf, X)
    t_h = time.perf_counter() - t0
    t0 = time.perf_counter()
    qp.hamiltonian(H, y, lam)
    t_j = time.perf_counter() - t0
    t0 = time.perf_counter()
    qp.solve_simplex_qp(H, y, lam)
    t_solve_raw = time.perf_counter() - t0
    # solve_simplex_qp rebuilds J (not H), so only the J build is
    # subtracted; subtracting H too clamped the solve to zero.
    t_solve = max(t_solve_raw - t_j, 0.0)
    return {"cell": config, "seed": seed, "fraction": frac, "rows": int(len(y)),
            "n_variables": int(H.shape[0]),
            "build_s": round(t_build, 3), "construction_s": round(t_h + t_j, 3),
            "h_matrix_s": round(t_h, 3), "j_build_s": round(t_j, 3),
            "solve_raw_s": round(t_solve_raw, 3), "solve_s": round(t_solve, 3),
            "solve_clamped": t_solve_raw < t_j,
            "total_s": round(t_build + t_h + t_j + t_solve, 3)}


def slope(rows: list[dict], part: str, level: float = LEVEL) -> dict:
    from scipy import stats
    x = np.log([r["rows"] for r in rows])
    y = np.log([max(r[part], 1e-4) for r in rows])
    res = stats.linregress(x, y)
    dof = len(x) - 2
    half = float(stats.t.ppf(1 - (1 - level) / 2, dof) * res.stderr) if dof > 0 else float("nan")
    return {"slope": float(res.slope), "low": float(res.slope - half),
            "high": float(res.slope + half), "level": level, "n": len(x)}


def projection_min(pilot_rows: list[dict], n_more: int = len(FULL_REST)) -> float:
    return sum(r["total_s"] for r in pilot_rows) * n_more / 60.0


def analyze(doc: dict) -> dict:
    out = {}
    for cell in CELLS:
        rows = [r for r in doc.get("runs", []) if r["cell"] == cell]
        if len(rows) < 3:
            continue
        b, s = slope(rows, "build_s"), slope(rows, "solve_s")
        largest = all(r["build_s"] >= max(r["construction_s"], r["solve_s"]) for r in rows)
        out[cell] = {
            "n_runs": len(rows), "seeds": sorted({r["seed"] for r in rows}),
            "build": b, "construction": slope(rows, "construction_s"), "solve": s,
            "P1_build_largest_everywhere": largest,
            "P1_holds": bool(largest and P1_BAND[0] <= b["low"] and b["high"] <= P1_BAND[1]),
            "P2_holds": bool(P2_BAND[0] <= s["low"] and s["high"] <= P2_BAND[1]),
            # A clamped solve is below the timer's resolution; its log is
            # the 1e-4 floor, so P2 is not readable where many rows clamp.
            "n_solve_clamped": sum(bool(r.get("solve_clamped")) for r in rows),
            "mean_by_fraction": {str(f): {k: float(np.mean([r[k] for r in rows
                                                            if r["fraction"] == f]))
                                          for k in ("rows", "build_s", "construction_s",
                                                    "solve_s", "total_s")}
                                 for f in FRACTIONS}}
    return out


def _load() -> dict:
    if OUT.exists():
        return json.loads(OUT.read_text(encoding="utf-8"))
    return {"generator": "experiments/phase2/src/f110_scaling.py", "card": "F110",
            "sprint": 28, "evidence_tag": "SIM", "metered_seconds": 0,
            "entry": "experiments/phase2/PREREGISTRATION_DRAFT.md section 6, Experiment 6",
            "cpu_count": os.cpu_count(), "fractions": list(FRACTIONS),
            "build": "serial full-pair (full_pair_pool.build_full)", "runs": []}


def _save(doc: dict) -> None:
    tmp = OUT.with_suffix(".tmp.json")
    tmp.write_text(json.dumps(doc, indent=1), encoding="utf-8")
    tmp.replace(OUT)


def _run(cell: str, seeds) -> list[dict]:
    doc = _load()
    new = []
    for seed in seeds:
        for frac in FRACTIONS:
            r = time_one(CELLS[cell], seed, frac)
            doc["runs"].append(r)
            new.append(r)
            _save(doc)                 # durable after every run
            print(json.dumps(r), flush=True)
    return new


def main(argv=None) -> int:
    mode = (argv or sys.argv[1:] or ["free"])[0]
    if mode == "free":
        _run("free", FREE_SEEDS)
    elif mode == "pilot":
        rows = _run("full", (FULL_PILOT_SEED,))
        doc = _load()
        proj = projection_min(rows)
        doc["full_pilot"] = {"seed": FULL_PILOT_SEED,
                             "projected_minutes_for_seeds_43_46": proj,
                             "cap_minutes": PROJECTION_CAP_MIN,
                             "run_five_seeds": proj <= PROJECTION_CAP_MIN}
        _save(doc)
        print(json.dumps(doc["full_pilot"]))
    elif mode == "full":
        doc = _load()
        if not doc.get("full_pilot", {}).get("run_five_seeds"):
            raise SystemExit("the pilot did not project five seeds within the cap")
        _run("full", FULL_REST)
    elif mode == "analyze":
        doc = _load()
        doc["analysis"] = analyze(doc)
        _save(doc)
        print(json.dumps(doc["analysis"], indent=1))
    else:
        raise SystemExit(f"unknown mode {mode!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
