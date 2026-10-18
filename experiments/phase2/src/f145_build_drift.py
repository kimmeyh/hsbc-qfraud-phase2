"""F145 (Sprint 26 Task B): the pool build's run-to-run drift, as evidence.

Builds seed 42's `free` pool (ULB, k=13, schedule 2, sequential, 78
learners) twice unseeded and twice with `qubo_proxy.seeded_weak_params`,
and counts the learners and cells that differ between the two builds on
each fold. The figures quoted in the Phase 2 draft's section 7 and in
F126's write-up come from this file, not from a test docstring (Sprint 26
fresh-eyes review, finding 9). ULB only: no drift has been measured on any
other dataset's pools.

    python experiments/phase2/src/f145_build_drift.py

Zero metered seconds. Output: experiments/phase2/results/f145_build_drift.json
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "experiments" / "src"))
import qubo_proxy as qp  # noqa: E402

OUT = ROOT / "experiments" / "phase2" / "results" / "f145_build_drift.json"
SEED, CONFIG = 42, "free"


def _build(seeded: bool) -> dict:
    split, cols, Xtr, Xva, Xte, y_pm1 = qp._prep(SEED, qp.CONFIGS[CONFIG]["k"])
    clf = qp.build_pool(Xtr, y_pm1, qp.CONFIGS[CONFIG]["schedule"], "dct",
                        "sequential",
                        weak_params=qp.seeded_weak_params(SEED) if seeded
                        else None)
    return {k: qp.h_matrix(clf, X) for k, X in
            (("train", Xtr), ("validation", Xva), ("test", Xte))}


def _compare(a: dict, b: dict) -> dict:
    out = {}
    for fold in ("train", "validation", "test"):
        d = a[fold] != b[fold]
        out[fold] = {"learners": int(a[fold].shape[0]),
                     "learners_differing": int(d.any(axis=1).sum()),
                     "cells": int(d.size),
                     "cells_differing": int(d.sum())}
    return out


def main() -> int:
    t0 = time.time()
    result = {}
    for seeded in (False, True):
        key = "seeded" if seeded else "unseeded"
        result[key] = _compare(_build(seeded), _build(seeded))
        print(key, json.dumps(result[key]), flush=True)
    OUT.write_text(json.dumps({
        "generator": "experiments/phase2/src/f145_build_drift.py",
        "card": "F145", "sprint": 26, "evidence_tag": "SIM",
        "metered_seconds": 0, "dataset": "ulb", "seed": SEED,
        "config": CONFIG, "pair_build": "sequential",
        "scope": "ULB only; no other dataset's drift is measured",
        "elapsed_s": round(time.time() - t0, 1),
        "two_builds_compared": result}, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
