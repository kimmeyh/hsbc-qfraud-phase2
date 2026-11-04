"""F156 (Sprint 29 Task D, #67): the Henze-Penrose Bayes-error bound on
F108's simulator.

The entry is the 2026-10-26 amendment to "F108" in
`experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, committed before
this module existed (a4df8a2). F108's generator, posterior, splits, seeds,
arms and margin are imported from `f108_ceiling`, unchanged.

The bound (Berisha, Wisler, Hero and Spanias, IEEE TSP 2016,
arXiv:1412.6534): on a Euclidean minimum spanning tree of the pooled
rows, C counts the edges joining the two classes; with m fraud and n
legitimate rows, D = 1 - C (m + n) / (2 m n), p = m / (m + n), and
u = 4 p q D + (p - q)^2 bounds the Bayes error to
[1/2 - sqrt(u)/2, 1/2 - u/2].

The entry shows before any bound is computed that the two pass terms
cannot both hold here (the width of a containing interval is at least
about half the Bayes error). The run answers term 1 alone.

    <venv python> experiments/phase2/src/f156_hp_bound.py pilot
    <venv python> experiments/phase2/src/f156_hp_bound.py run

Zero metered seconds. Writes `experiments/phase2/results/f156_hp_bound.json`
through `provenance.write_result` (the pilot writes `f156_hp_bound_pilot.json`).
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import f108_ceiling as fc  # noqa: E402  (Phase 2, F108; not edited)

OUT = fc.ROOT / "experiments" / "phase2" / "results" / "f156_hp_bound.json"
OUT_PILOT = OUT.with_name("f156_hp_bound_pilot.json")
# F168 part 7: a long run resumes through provenance.start (the run).
LONG_RUN = True
SUBSAMPLE = 60_000
PILOT_CAP_S = 600.0
DECIDING_ARM = "none"


def emst_edges(X: np.ndarray) -> np.ndarray:
    """The Euclidean minimum spanning tree's edges, as index pairs. Exact:
    the tree lies in the Delaunay triangulation's edges."""
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import minimum_spanning_tree
    from scipy.spatial import Delaunay
    tri = Delaunay(X)
    s = tri.simplices
    k = s.shape[1]
    pairs = np.concatenate([s[:, [i, j]] for i in range(k)
                            for j in range(i + 1, k)])
    pairs = np.unique(np.sort(pairs, axis=1), axis=0)
    w = np.linalg.norm(X[pairs[:, 0]] - X[pairs[:, 1]], axis=1)
    # A zero-length edge (duplicate rows) would vanish from a sparse
    # matrix; a tiny floor keeps it as an edge.
    w = np.maximum(w, 1e-300)
    n = len(X)
    g = coo_matrix((w, (pairs[:, 0], pairs[:, 1])), shape=(n, n)).tocsr()
    t = minimum_spanning_tree(g).tocoo()
    edges = np.column_stack([t.row, t.col])
    if len(edges) != n - 1:
        raise ValueError(f"spanning tree has {len(edges)} edges for {n} rows")
    return edges


def hp_bound(X: np.ndarray, y: np.ndarray) -> dict:
    y = np.asarray(y).astype(int)
    m, n = int(y.sum()), int(len(y) - y.sum())
    if m == 0 or n == 0:
        raise ValueError("both classes are needed")
    e = emst_edges(X)
    c = int(np.sum(y[e[:, 0]] != y[e[:, 1]]))
    d = 1.0 - c * (m + n) / (2.0 * m * n)
    p = m / (m + n)
    q = 1.0 - p
    u = min(1.0, max(0.0, 4 * p * q * d + (p - q) ** 2))
    lo, hi = 0.5 - 0.5 * np.sqrt(u), 0.5 - 0.5 * u
    return {"m": m, "n": n, "cross_edges": c, "D": d, "u": u,
            "lower": float(lo), "upper": float(hi), "width": float(hi - lo)}


def terms(bound: dict, bayes: float) -> dict:
    cap = 2 * max(fc.MARGIN_ABS, fc.MARGIN_REL * bayes)
    contains = bool(bound["lower"] <= bayes <= bound["upper"])
    narrow = bool(bound["width"] <= cap)
    return {"contains": contains, "width_cap": cap, "narrow": narrow,
            "pass": contains and narrow}


def stratified(y: np.ndarray, size: int, seed: int) -> np.ndarray:
    """Row indices keeping the class share (the theorem's prior)."""
    if size >= len(y):
        return np.arange(len(y))
    rng = np.random.default_rng(seed)
    keep = []
    for c in (0, 1):
        idx = np.nonzero(y == c)[0]
        k = max(1, int(round(size * len(idx) / len(y))))
        keep.append(rng.choice(idx, k, replace=False))
    return np.sort(np.concatenate(keep))


def seed_run(seed: int, size: int = SUBSAMPLE, arms=None) -> dict:
    t0 = time.perf_counter()
    d = fc.generate(seed)
    tr = (d["day"] >= fc.TRAIN_DAYS[0]) & (d["day"] <= fc.TRAIN_DAYS[1])
    te = (d["day"] >= fc.TEST_DAYS[0]) & (d["day"] <= fc.TEST_DAYS[1])
    X = np.column_stack([d["amount"], d["mu"], d["time"]])
    pi_t, q = fc.world_rates(d, te)
    eta = fc.posterior(d["amount"], d["mu"], pi_t, q)
    check = fc.generator_check(d["y_main"][te], eta[te])
    row = {"seed": seed, "subsample": size, "generator_check": check,
           "arms": {}}
    if not check["pass"]:
        row["stopped"] = "generator check failed"
        return row
    rng = np.random.default_rng(seed + 7)       # F108's noise stream
    labels = {}
    for name, rates in fc.NOISE.items():
        labels[name] = (X, *fc.add_noise(d["y_main"], eta, rates, rng))
    ref_eta = (d["base_amount"] > fc.S1_AMOUNT).astype(float)
    labels["reference"] = (np.column_stack([d["base_amount"], d["mu"],
                                            d["time"]]),
                           d["y_ref"], ref_eta)
    for name, (Xa, y, e) in labels.items():
        if arms is not None and name not in arms:
            continue
        Xtr, ytr = Xa[tr], y[tr]
        bayes = float(np.mean(np.minimum(e[te], 1 - e[te])))
        idx = stratified(ytr, size, seed)
        mu, sd = Xtr.mean(axis=0), Xtr.std(axis=0)
        t1 = time.perf_counter()
        b = hp_bound((Xtr[idx] - mu) / sd, ytr[idx])
        row["arms"][name] = {"bayes_error": bayes, **b, **terms(b, bayes),
                             "bound_seconds": round(time.perf_counter() - t1, 1)}
    row["seconds"] = round(time.perf_counter() - t0, 1)
    print(f"  s{seed} " + " | ".join(
        f"{a}: bayes {v['bayes_error']:.5f} [{v['lower']:.5f}, "
        f"{v['upper']:.5f}] contains {v['contains']} narrow {v['narrow']}"
        for a, v in row["arms"].items()) + f" {row['seconds']} s", flush=True)
    return row


def summarize(rows: list) -> dict:
    live = [r for r in rows if DECIDING_ARM in r["arms"]]
    arm = [r["arms"][DECIDING_ARM] for r in live]
    return {"deciding_arm": DECIDING_ARM, "n_seeds": len(rows),
            "contains": sum(a["contains"] for a in arm),
            "narrow": sum(a["narrow"] for a in arm),
            "both": sum(a["pass"] for a in arm),
            # Out of every seed run, as F108 counts a stopped seed.
            "passes": sum(a["pass"] for a in arm) >= min(fc.PASS_SEEDS,
                                                          len(rows)),
            "term1_alone_4_of_5": sum(a["contains"] for a in arm)
            >= min(fc.PASS_SEEDS, len(rows))}


def _doc(rows, size, mode):
    return {"card": "F156", "sprint": 29, "phase": 2, "evidence_tag": "SIM",
            "metered_seconds": 0, "mode": mode,
            "entry": "experiments/phase2/PREREGISTRATION_DRAFT.md section 6, "
                     "F108, amendment 2026-10-26 (a4df8a2)",
            "estimator": "Henze-Penrose bound, Berisha et al. 2016 "
                         "(arXiv:1412.6534), exact EMST via Delaunay",
            "subsample": size, "seeds": [r["seed"] for r in rows],
            "rows": rows, "summary": summarize(rows),
            "complete": mode == "pilot" or len(rows) == len(fc.SEEDS)}


def main(argv=None) -> int:
    import json
    import provenance
    mode = (argv or sys.argv[1:] or ["pilot"])[0]
    if mode == "pilot":
        rid, _ = provenance.start(OUT_PILOT, resumable=False)
        row = seed_run(fc.SEEDS[0], SUBSAMPLE, arms=(DECIDING_ARM,))
        secs = row["arms"][DECIDING_ARM]["bound_seconds"]
        size = SUBSAMPLE if secs <= PILOT_CAP_S else SUBSAMPLE // 2
        doc = _doc([row], SUBSAMPLE, "pilot")
        doc["size_for_run"] = size
        provenance.write_result(OUT_PILOT, doc, __file__, [fc.SEEDS[0]], rid)
        print(json.dumps({"bound_seconds": secs, "size_for_run": size}))
    elif mode == "run":
        pilot = json.loads(OUT_PILOT.read_text(encoding="utf-8"))
        size = pilot["size_for_run"]
        rid, resume = provenance.start(OUT)
        rows = json.loads(OUT.read_text(encoding="utf-8"))["rows"] \
            if resume else []
        done = {r["seed"] for r in rows}
        for seed in fc.SEEDS:
            if seed in done:
                continue           # resume: never redo a seed
            rows.append(seed_run(seed, size))
            provenance.write_result(OUT, _doc(rows, size, "run"), __file__,
                                    [r["seed"] for r in rows], rid)
        print(json.dumps(_doc(rows, size, "run")["summary"]))
        print("complete", flush=True)
    else:
        raise SystemExit(f"unknown mode {mode!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
