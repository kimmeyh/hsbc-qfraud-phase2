"""F159: the full-pair weak-learner pool built across processes, timed.

Sprint 29 Task B (#65). Zero metered seconds. F110 found the serial pool
build is the cost of CVQBoost training on the proxy (about 13 minutes at
833 learners and full ULB rows). The learners are independent, so they
split across processes. Windows has no `fork`, so the pool uses `spawn`:
each worker receives the rows once (the initializer) and then only the
column indices of each learner.

`build_parallel` returns the classifier `full_pair_pool.build_full`
returns, learners in the same order, so `qubo_proxy.h_matrix` reads it
unchanged. `full_pair_pool.py` is not edited.

The check: the parallel pool's H on the VALIDATION rows equals the serial
pool's. On the training rows it would be vacuous: two pools built with
different seeds agree there and differ on held-out rows (Sprint 29
planning probe).

Modes:
  run      seed 42, the 833-variable cell, F110's four row fractions; per
           fraction a serial build (the reference), then 1, 4, 8, 16 and 32
           workers. Resumable per (fraction, build): a unit already
           recorded is skipped, never timed twice.
  analyze  speed-up against workers, the longest single learner, equality.

Run:  <venv python> experiments/phase2/src/f159_parallel_pool.py run|analyze
"""
from __future__ import annotations

import hashlib
import multiprocessing as mp
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "experiments" / "src"))

OUT = ROOT / "experiments" / "phase2" / "results" / "f159_parallel_pool.json"
CELL = "full"                      # qubo_proxy config: 833 variables
SEED = 42
FRACTIONS = (0.10, 0.25, 0.50, 1.00)   # F110's
WORKERS = (1, 4, 8, 16, 32)

# Set once per worker by the initializer, so each task sends only indices.
_W: dict = {}


def _init(X, y, weak_type, params):
    _W.update(X=X, y=y, weak_type=weak_type, params=params)


def _train(idx):
    from eqc_models.ml.classifierqboost import WeakClassifier
    t0 = time.perf_counter()
    wc = WeakClassifier(_W["X"][:, idx], _W["y"], _W["weak_type"],
                        dict(_W["params"]))
    wc.train()
    return wc, time.perf_counter() - t0


def build_parallel(X_tr: np.ndarray, y_pm1: np.ndarray, schedule: int,
                   weak_type: str, seed: int, workers: int = 4,
                   lambda_coef: float | None = None):
    """`full_pair_pool.build_full` across `workers` spawned processes, with
    `qubo_proxy.seeded_weak_params(seed)` (F145) as the learners' params.
    Returns (classifier, seconds of each learner's training, in order)."""
    import full_pair_pool as fpp
    import qubo_proxy as qp
    # An empty build gives the classifier, its arguments and their check
    # exactly as the serial build makes them; the learners are added below.
    clf = fpp.build_full(X_tr, y_pm1, schedule, weak_type,
                         weak_params=qp.seeded_weak_params(seed),
                         lambda_coef=lambda_coef, indices=[])
    inds = fpp.learner_indices(X_tr.shape[1], schedule)
    params = qp.seeded_weak_params(seed)
    chunk = max(1, len(inds) // (workers * 8))
    with ProcessPoolExecutor(max_workers=workers,
                             mp_context=mp.get_context("spawn"),
                             initializer=_init,
                             initargs=(X_tr, y_pm1, weak_type, params)) as ex:
        out = list(ex.map(_train, inds, chunksize=chunk))
    clf.ind_list = [list(i) for i in inds]
    clf.h_list = [wc for wc, _ in out]
    return clf, [s for _, s in out]


def h_sha256(clf, X) -> str:
    import qubo_proxy as qp
    H = np.ascontiguousarray(qp.h_matrix(clf, X))
    return hashlib.sha256(H.tobytes()).hexdigest()


def _data(frac: float):
    import qubo_proxy as qp
    from f110_scaling import subsample
    c = qp.CONFIGS[CELL]
    split, _, Xtr, Xva, _, y_pm1 = qp._prep(SEED, c["k"])
    idx = subsample(split.y_train.to_numpy(), frac, SEED)
    return c["schedule"], Xtr[idx], y_pm1[idx], Xva


def time_unit(frac: float, build: str) -> dict:
    """One build: "serial" (`build_full`) or a worker count as text."""
    import full_pair_pool as fpp
    import qubo_proxy as qp
    schedule, X, y, Xva = _data(frac)
    t0 = time.perf_counter()
    if build == "serial":
        clf = fpp.build_full(X, y, schedule, "dct",
                             weak_params=qp.seeded_weak_params(SEED))
        per = None
    else:
        clf, per = build_parallel(X, y, schedule, "dct", SEED,
                                  workers=int(build))
    secs = time.perf_counter() - t0
    row = {"fraction": frac, "build": build, "rows": int(len(y)),
           "n_learners": len(clf.h_list), "build_s": round(secs, 3),
           "h_validation_sha256": h_sha256(clf, Xva)}
    if per is not None:
        row["longest_learner_s"] = round(max(per), 4)
        row["sum_learner_s"] = round(sum(per), 3)
    return row


def analyze(units: list[dict]) -> dict:
    out = {}
    for frac in FRACTIONS:
        rows = {u["build"]: u for u in units if u["fraction"] == frac}
        if "serial" not in rows:
            continue
        ref = rows["serial"]
        par = [rows[str(w)] for w in WORKERS if str(w) in rows]
        out[str(frac)] = {
            "rows": ref["rows"], "serial_s": ref["build_s"],
            "equal_on_validation": {u["build"]: u["h_validation_sha256"]
                                    == ref["h_validation_sha256"] for u in par},
            "speedup": {u["build"]: round(ref["build_s"] / u["build_s"], 2)
                        for u in par},
            "longest_learner_s": max((u["longest_learner_s"] for u in par),
                                     default=None)}
    out["all_equal"] = bool(out) and all(
        all(v["equal_on_validation"].values())
        for k, v in out.items() if k != "all_equal")
    return out


def _doc(units: list[dict]) -> dict:
    # `complete` is the run's own marker: a reader checks it, never the
    # file's presence alone (CLAUDE.md, Sprint 13).
    return {"card": "F159", "sprint": 29, "evidence_tag": "SIM",
            "complete": len(units) == len(FRACTIONS) * (1 + len(WORKERS)),
            "metered_seconds": 0, "cell": CELL, "seed": SEED,
            "cpu_count": os.cpu_count(), "fractions": list(FRACTIONS),
            "workers": list(WORKERS), "start_method": "spawn",
            "equality": "H on the validation rows, SHA-256 of the bytes, "
                        "against the serial build_full pool",
            "units": units, "analysis": analyze(units)}


def main(argv=None) -> int:
    import json
    import provenance
    mode = (argv or sys.argv[1:] or ["run"])[0]
    if mode == "run":
        resume = provenance.sidecar(OUT).exists() and OUT.exists()
        rid = provenance.run_id_for(OUT, resume=resume)
        units = json.loads(OUT.read_text(encoding="utf-8"))["units"] \
            if resume else []
        done = {(u["fraction"], u["build"]) for u in units}
        for frac in FRACTIONS:
            for build in ("serial", *map(str, WORKERS)):
                if (frac, build) in done:
                    continue           # resume: never time a unit twice
                u = time_unit(frac, build)
                units.append(u)
                provenance.write_result(OUT, _doc(units), __file__, [SEED], rid)
                print(json.dumps(u), flush=True)
        print("complete", flush=True)
    elif mode == "analyze":
        print(json.dumps(analyze(json.loads(
            OUT.read_text(encoding="utf-8"))["units"]), indent=1))
    else:
        raise SystemExit(f"unknown mode {mode!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
