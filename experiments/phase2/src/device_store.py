"""Store every device job in full, before anything reads it.

Sprint 28 D4 (team lead, 2026-10-23): every Dirac-3 and Dirac-3S run must
store all its returned values, and enough to rebuild the problem, so results
can be reproduced and compared over time. F142's Dirac-3 B4 lane stored its
metrics and samples but not the per-row scores, and its pool was built
unseeded, so it can never be rescored.

This lifts F142's raw-response save (`run_dirac3s_verify._guarded`) into one
place every Phase 2 device runner uses, on any eqc-models cloud solver
(the CVQBoost solver through eqc_submit's `device` context with `wrap=`, or the integer
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
- A resume never repeats a metered call (F168 part 3, Sprint 30). The
  wrapped `solve` writes an intent record, `intents/<hash>_<card>_<unit>.json`,
  BEFORE it sends, because the response is saved only in `makeResults`,
  after the job returns: a process stopped between the two would otherwise
  leave no trace of a job that was sent. `saving(...)` refuses a problem
  hash that already has an intent or a response (`lookup`), before any
  solver exists. A response file with no `problem_sha256` (the Phase 1
  backfills) cannot be matched; `unhashed()` lists them, so the lookup
  says what it cannot cover instead of matching nothing silently. A block
  refused here is re-approved by the team lead with its count and seconds
  (Criterion H), after the vendor's job list shows whether it ran.

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


INTENTS = "intents"


def _store(path: Path, doc: dict) -> None:
    """Write one store record atomically: a temporary file, then a replace.
    A store record is not a result, so it does not go through
    `provenance.write_result`."""
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(doc, indent=1), encoding="utf-8")
    tmp.replace(path)


def lookup(problem_hash: str, store_dir: Path | None = None) -> dict:
    """Every record of `problem_hash` in the store: {"responses": [...],
    "intents": [...]}, paths sorted. An intent with no response is a job
    that may have been sent and whose process stopped before it returned."""
    out = Path(store_dir or STORE_DIR)
    responses, unreadable = [], []
    for path in sorted(out.glob("*.json")):
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            # It may be this problem's response; `saving` refuses on it
            # (PR 74 review: it was skipped, so a resend could pass).
            unreadable.append(path)
            continue
        if isinstance(doc, dict) and doc.get("problem_sha256") == problem_hash:
            responses.append(path)
    intents = sorted((out / INTENTS).glob(f"{problem_hash}_*.json"))
    return {"responses": responses, "intents": intents,
            "unreadable": unreadable}


def unhashed(store_dir: Path | None = None) -> list[Path]:
    """Response files with no problem hash, which `lookup` cannot match."""
    out = Path(store_dir or STORE_DIR)
    found = []
    for path in sorted(out.glob("*.json")):
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            found.append(path)
            continue
        if not (isinstance(doc, dict) and _SHA.match(
                str(doc.get("problem_sha256", "")))):
            found.append(path)
    return found


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
    found = lookup(problem_hash, out)
    if found["unreadable"]:
        raise ValueError(
            f"the store holds unreadable response files "
            f"({[p.name for p in found['unreadable']]}); one may be this "
            "problem's, so a send cannot be shown to be the first. Repair "
            "or move them, then retry")
    if found["responses"] or found["intents"]:
        names = [p.name for p in found["responses"] + found["intents"]]
        raise ValueError(
            f"problem {problem_hash[:12]} was already sent ({names}); a "
            "resume never repeats a metered call. Check the vendor's job "
            "list, then ask the team lead to re-approve the block with its "
            "count and seconds (Criterion H)")
    saved: dict = {}
    declared = {k: v for k, v in problem.items() if k != "arrays"}

    def wrap(cls):
        class Stored(cls):
            def solve(self, model, *a, **kw):
                if problem_sha256(problem_arrays(model)) != problem_hash:
                    raise eqc_submit.NoRetry(
                        "pre-submit: the model differs from the declared "
                        "problem; nothing sent")
                # Written before the send: the response is saved only
                # after the job returns.
                intent = out / INTENTS / f"{problem_hash}_{card.lower()}_{unit}.json"
                intent.parent.mkdir(parents=True, exist_ok=True)
                _store(intent, {"problem_sha256": problem_hash, "card": card,
                                "unit": unit, "device_type": device_type,
                                "sending": time.strftime("%Y-%m-%dT%H:%M:%S")})
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
                _store(path, doc)
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
