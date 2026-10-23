"""Store every device job in full, before anything reads it.

Sprint 28 D4 (team lead, 2026-10-23): every Dirac-3 and Dirac-3S run must
store all its returned values, and enough to rebuild the problem, so results
can be reproduced and compared over time. F142's Dirac-3 B4 lane stored its
metrics and samples but not the per-row scores, and its pool was built
unseeded, so it can never be rescored.

This lifts F142's raw-response save (`run_dirac3s_verify._guarded`) into one
place every Phase 2 device runner uses, on any eqc-models cloud solver
(the CVQBoost solver through `eqc_submit.device(wrap=...)`, or the integer
solver class directly):

- `saving(...)` refuses, before anything is sent, a problem it could not
  rebuild: a missing or malformed problem hash, a CVQBoost pool whose weak
  learners are unseeded, or a bare Hamiltonian without its arrays.
- The wrapped `solve` refuses a model whose Hamiltonian differs from the
  declared hash (nothing sent).
- The wrapped `makeResults` writes the full response, the problem
  declaration and the hash to disk, then hands the response on. A write
  failure raises; it is never swallowed.
- `require_saved(saved)` raises when a job returned and nothing was saved.

`test_device_store_required.py` fails a Phase 2 module that submits to a
device without `saving` and `require_saved`.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "src"))
import eqc_submit  # noqa: E402

STORE_DIR = ROOT / "experiments" / "phase2" / "results" / "device_samples"
_SHA = re.compile(r"^[0-9a-f]{64}$")
# Learner types with no random state to seed (KNN is deterministic).
UNSEEDABLE_WEAK_TYPES = ("knn",)


def problem_arrays(model) -> tuple:
    """The arrays that define what the device solves: (J, C) on a CVQBoost
    classifier, `H` on an eqc-models polynomial model."""
    if hasattr(model, "_J") and hasattr(model, "_C"):
        return (model._J, model._C)
    if hasattr(model, "H"):
        return tuple(model.H)
    raise TypeError(f"cannot read the problem from {type(model).__name__}")


def problem_sha256(arrays) -> str:
    h = hashlib.sha256()
    for a in arrays:
        h.update(np.ascontiguousarray(np.asarray(a, dtype=np.float64)).tobytes())
    return h.hexdigest()


def check_problem(problem: dict) -> None:
    """Refuse a declaration that could not rebuild the problem."""
    kind = problem.get("kind")
    if kind == "cvqboost_pool":
        wtype = problem.get("weak_cls_type")
        params = problem.get("weak_cls_params")
        if not wtype or params is None:
            raise ValueError("cvqboost_pool needs weak_cls_type and "
                             "weak_cls_params")
        if (wtype not in UNSEEDABLE_WEAK_TYPES
                and not isinstance(params.get("random_state"), int)):
            raise ValueError("unseeded pool: pass qubo_proxy."
                             "seeded_weak_params(seed) so it can be rebuilt")
        for key in ("seed", "data"):
            if problem.get(key) is None:
                raise ValueError(f"cvqboost_pool needs {key!r}")
    elif kind == "hamiltonian":
        if not problem.get("arrays"):
            raise ValueError("hamiltonian needs its arrays, saved with the job")
    else:
        raise ValueError(f"unknown problem kind {kind!r}")


def saving(card: str, unit: str, device_type: str, problem_hash: str,
           problem: dict, store_dir: Path | None = None):
    """(wrap, saved): `wrap(cls)` returns a solver subclass that checks the
    hash before sending and stores the full response before returning it.
    Every check here runs before any solver exists, so a refusal sends
    nothing."""
    if not isinstance(problem_hash, str) or not _SHA.match(problem_hash):
        raise ValueError("problem_hash must be a SHA-256 hex digest")
    check_problem(problem)
    if problem["kind"] == "hamiltonian" and \
            problem_sha256(problem["arrays"]) != problem_hash:
        raise ValueError("the arrays do not hash to problem_hash")
    out = Path(store_dir or STORE_DIR)
    saved: dict = {}
    declared = {k: v for k, v in problem.items() if k != "arrays"}

    def wrap(cls):
        class Stored(cls):
            def solve(self, model, *a, **kw):
                if problem_sha256(problem_arrays(model)) != problem_hash:
                    raise eqc_submit.NoRetry(
                        "pre-submit: the model differs from the declared "
                        "problem; nothing sent")
                return super().solve(model, *a, **kw)

            def makeResults(self, model, response):
                job_id = str((response.get("job_info") or {}).get("job_id"))
                out.mkdir(parents=True, exist_ok=True)
                stem = f"{card.lower()}_{unit}_{job_id}"
                path = out / f"{stem}.json"
                if path.exists():
                    path = out / f"{stem}_{time.strftime('%Y%m%dT%H%M%S')}.json"
                doc = {"job_id": job_id, "device_type": device_type,
                       "card": card, "unit": unit,
                       "problem_sha256": problem_hash, "problem": declared,
                       "saved": time.strftime("%Y-%m-%dT%H:%M:%S"),
                       "response": eqc_submit.to_jsonable(response)}
                if problem["kind"] == "hamiltonian":
                    arrays = path.with_suffix(".npz")
                    np.savez_compressed(arrays, *[np.asarray(a) for a in
                                                  problem["arrays"]])
                    doc["arrays_file"] = arrays.name
                tmp = path.with_suffix(".tmp")
                tmp.write_text(json.dumps(doc, indent=1), encoding="utf-8")
                tmp.replace(path)
                saved["path"], saved["job_id"] = path, job_id
                return super().makeResults(model, response)
        return Stored
    return wrap, saved


def require_saved(saved: dict) -> Path:
    """Raise when a job returned and its response is not on disk."""
    path = saved.get("path")
    if not path or not Path(path).exists():
        raise RuntimeError("device job returned but its response was not "
                           "stored; do not score it")
    return Path(path)
