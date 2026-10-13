"""F29: does the CVQBoost optimum move with the training sample size?

Sprint 25 Task E (#17). Phase 2 code: it IMPORTS Phase 1 modules (`data`,
`qubo_proxy`) and edits none. Results go to
`experiments/phase2/results/f29_sample_size.json`. Zero metered seconds.

DESIGN. The weak pool is built ONCE per seed on the full ULB train fold, with
the frozen `free` cell (k=13, schedule 2, sequential, dct). Only the SOLVE
sees a subsample: the rows of H_train are subsampled, stratified on the
label, and the simplex QP is re-solved with lambda = 2 * n_sub (the frozen
LAMBDA_MULT rule). Holding the pool fixed is what makes the weight vectors
comparable index by index; a pool rebuilt per size would change the learners
themselves and the cosine would measure the builder, not the optimum.

PREMISE FALSIFIER, stated before the run (Sprint 25 plan, Task E): the
optimum is called insensitive if every subsample's weights have cosine at
least COSINE_THRESHOLD with the full-fold weights on the same seed. Any
value below it, and the card's premise is wrong. The card closes either way.

Run:  <venv python> experiments/phase2/src/sample_size.py
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "experiments" / "src"))
import qubo_proxy as qp                              # noqa: E402  (Phase 1, read-only)

OUT = ROOT / "experiments" / "phase2" / "results" / "f29_sample_size.json"
SEEDS = (42, 43, 44)
FRACTIONS = (0.125, 0.25, 0.5, 1.0)
CONFIG = "free"
WEAK_TYPE = "dct"
COSINE_THRESHOLD = 0.99


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    na, nb = float(np.linalg.norm(a)), float(np.linalg.norm(b))
    if na == 0.0 or nb == 0.0:
        raise ValueError("cosine of a zero vector is undefined")
    return float(a @ b / (na * nb))


def centered(w: np.ndarray, w_full: np.ndarray) -> dict:
    """Compare the non-uniform parts of two weight vectors.

    `centered_cosine` is the cosine of (w - 1/n) and (w_full - 1/n), None when
    either part is exactly zero. `relative_distance` is |w - w_full| divided by
    |w_full - 1/n|, None when the full-fold weights are exactly uniform."""
    u = np.full(len(w), 1.0 / len(w))
    a, b = w - u, w_full - u
    na, nb = float(np.linalg.norm(a)), float(np.linalg.norm(b))
    return {"centered_cosine": float(a @ b / (na * nb)) if na > 0 and nb > 0 else None,
            "relative_distance": float(np.linalg.norm(w - w_full) / nb) if nb > 0 else None}


def stratified_rows(y01: np.ndarray, fraction: float, seed: int) -> np.ndarray:
    """Row indices of a label-stratified subsample; all rows at fraction 1."""
    y01 = np.asarray(y01)
    if fraction >= 1.0:
        return np.arange(len(y01))
    rng = np.random.default_rng(seed)
    keep = []
    for label in (0, 1):
        idx = np.flatnonzero(y01 == label)
        n = max(1, int(round(fraction * len(idx))))
        keep.append(rng.choice(idx, size=n, replace=False))
    return np.sort(np.concatenate(keep))


def summarize(rows: list[dict], threshold: float = COSINE_THRESHOLD) -> dict:
    """Per-fraction cosine and AUPRC, and the verdict against the threshold."""
    by_frac: dict[float, list[dict]] = {}
    for r in rows:
        by_frac.setdefault(r["fraction"], []).append(r)
    per_fraction = {}
    for frac in sorted(by_frac):
        rs = by_frac[frac]
        cos = np.array([r["cosine_to_full"] for r in rs])
        ap = np.array([r["test_auprc"] for r in rs])
        per_fraction[str(frac)] = {
            "n_seeds": len(rs),
            "n_train_rows_mean": float(np.mean([r["n_train_rows"] for r in rs])),
            "cosine_min": float(cos.min()), "cosine_mean": float(cos.mean()),
            "test_auprc_mean": float(ap.mean()),
            "test_auprc_std": float(ap.std(ddof=1)) if len(ap) > 1 else 0.0,
        }
    subs = [r["cosine_to_full"] for r in rows if r["fraction"] < 1.0]
    worst = float(min(subs)) if subs else float("nan")
    cc = [r["centered_cosine"] for r in rows
          if r["fraction"] < 1.0 and r.get("centered_cosine") is not None]
    uni = [r["cosine_to_uniform"] for r in rows if "cosine_to_uniform" in r]
    return {"per_fraction": per_fraction, "worst_subsample_cosine": worst,
            "worst_subsample_centered_cosine": float(min(cc)) if cc else None,
            "min_cosine_to_uniform": float(min(uni)) if uni else None,
            "pinned_at_uniform": bool(uni) and min(uni) >= threshold,
            "cosine_threshold": threshold,
            "insensitive": bool(subs) and worst >= threshold}


def run() -> dict:
    from sklearn.metrics import average_precision_score
    rows = []
    for seed in SEEDS:
        t0 = time.perf_counter()
        split, cols, Xtr, Xva, Xte, y_pm1 = qp._prep(seed, qp.CONFIGS[CONFIG]["k"])
        clf = qp.build_pool(Xtr, y_pm1, qp.CONFIGS[CONFIG]["schedule"],
                            WEAK_TYPE, "sequential")
        H_tr, H_te = qp.h_matrix(clf, Xtr), qp.h_matrix(clf, Xte)
        y01 = (y_pm1 == 1).astype(int)
        y_te = split.y_test.to_numpy()
        build_s = time.perf_counter() - t0
        weights = {}
        for frac in sorted(FRACTIONS, reverse=True):     # full fold first
            t1 = time.perf_counter()
            idx = stratified_rows(y01, frac, seed)
            w = qp.solve_simplex_qp(H_tr[:, idx], y_pm1[idx],
                                    qp.LAMBDA_MULT * len(idx))
            weights[frac] = w
            p_te = np.clip((w @ H_te + 1.0) / 2.0, 0.0, 1.0)
            rows.append({
                "seed": seed, "fraction": frac, "n_train_rows": int(len(idx)),
                "n_train_positives": int(y01[idx].sum()),
                "n_pool": int(H_tr.shape[0]),
                "cosine_to_full": cosine(w, weights[1.0]),
                # Sprint 4 found the optimum near-uniform under this ridge; if
                # so, "insensitive" means "pinned", and this field shows it.
                "cosine_to_uniform": cosine(w, np.ones_like(w)),
                # Sprint 25 code review: near uniform, the plain cosine is
                # dominated by the shared uniform part. These compare only
                # the parts of the weights that are NOT uniform.
                **centered(w, weights[1.0]),
                "max_over_min_weight": float(w.max() / w.min()) if w.min() > 0 else None,
                "nonzero_weights": int((w > 1e-9).sum()),
                "test_auprc": float(average_precision_score(y_te, p_te)),
                "solve_s": round(time.perf_counter() - t1, 3),
                "pool_build_s": round(build_s, 3),
                "features": cols,
            })
            print(f"[F29] seed={seed} frac={frac} rows={len(idx)} "
                  f"cos={rows[-1]['cosine_to_full']:.6f} "
                  f"ap={rows[-1]['test_auprc']:.4f}", flush=True)
    return {"rows": rows, "summary": summarize(rows)}


def main() -> int:
    res = run()
    header = {
        "generator": "experiments/phase2/src/sample_size.py", "card": "F29",
        "sprint": 25, "phase": 2, "evidence_tag": "SIM", "metered_seconds": 0,
        "date": time.strftime("%Y-%m-%d"), "dataset": "ulb",
        "config": CONFIG, "weak_type": WEAK_TYPE, "pair_build": "sequential",
        "lambda_rule": "LAMBDA_MULT * n_rows_solved",
        "seeds": list(SEEDS), "fractions": list(FRACTIONS),
        "generator_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    OUT.write_text(json.dumps({**header, **res}, indent=2), encoding="utf-8")
    print(json.dumps(res["summary"], indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
