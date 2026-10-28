"""What a Phase 2 result was made with, so it can be reproduced.

Sprint 28 D4 part 3 (team lead, 2026-10-23): every future ML, QML,
optimization or tensor run stores its data so results can be reproduced
and compared over time. Every new result file under
`experiments/phase2/results/` carries `provenance`: the generator's git
commit, whether the generator file matched that commit, the seeds, and the
library versions. `test_outcome_record_required.py` fails a new file
without it.

Use:  doc["provenance"] = provenance.record(__file__, seeds)

Sprint 28 IMP-6: a new module writes its result through `write_result`,
which adds the block itself, refuses to replace a recorded result from
another run unless the call states why, and checks the written file before
it takes the result's place. f110, f111 and f152 each overwrote or
duplicated recorded output in a default mode, and the backfill replaced a
file before checking it (PR #46 review); each was fixed one module at a
time. `test_result_writer_required.py` routes new modules here.

F165 (Sprint 29 Task A): a resumable run takes its id from `run_id_for`,
which keeps it in a gitignored sidecar beside the result, so a resume in a
new process is the same run and is recorded as a resume; an id copied out
of a recorded result is refused.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import uuid
from importlib import metadata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import strict_json  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]

# Recorded when installed; a package that is absent is left out, not faked.
PACKAGES = ("numpy", "scipy", "pandas", "scikit-learn", "xgboost", "lightgbm",
            "catboost", "imbalanced-learn", "eqc-models", "qci-client")
RUN_ID = re.compile(r"[0-9a-f]{32}")
REQUIRED = ("generator", "generator_commit", "generator_clean", "seeds",
            "versions")


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                          text=True, check=True).stdout.strip()


def versions() -> dict:
    out = {"python": sys.version.split()[0]}
    for name in PACKAGES:
        try:
            out[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            continue
    return out


def record(generator, seeds) -> dict:
    """The block. `generator_clean` is False when the generator file
    differs from the commit, so a reader knows the commit alone does not
    reproduce it."""
    seeds = [int(s) for s in seeds]
    if not seeds:
        raise ValueError("a result records the seeds it used; none given")
    rel = Path(generator).resolve().relative_to(ROOT).as_posix()
    return {"generator": rel,
            "generator_commit": _git("rev-parse", "HEAD"),
            "generator_clean": _git("status", "--porcelain", "--", rel) == "",
            "seeds": seeds,
            "versions": versions()}


# Ids this process made or resumed. `write_result` lets a run rewrite its
# own file only with one of these, so an id copied out of a recorded result
# cannot replace it (F165, Sprint 29 Task A).
_ISSUED: set[str] = set()


def new_run_id() -> str:
    """One per run, made fresh when the run starts. Every write of that run
    passes the same id, so the run may rewrite its own file. `write_result`
    refuses an id that is not 32 hex characters, and an id this process
    did not make or resume, so neither a constant name nor a copied id
    switches the refusal off. A run that may stop and resume in a new
    process takes its id from `run_id_for` instead."""
    rid = uuid.uuid4().hex
    _ISSUED.add(rid)
    return rid


def sidecar(path) -> Path:
    """Where `run_id_for` keeps a result's run id: `<result>.run_id`,
    gitignored, plain text (the id, then one line per resume)."""
    path = Path(path)
    return path.with_name(path.name + ".run_id")


def run_id_for(path, resume: bool = False) -> str:
    """The run's id for the result at `path`, kept in its sidecar so a
    resume in a new process is the same run (F165, Sprint 29 Task A).

    A start (`resume=False`) makes a new id and writes the sidecar before
    any result exists, so a rerun is a new run: replacing a recorded
    result still needs `replace=`. A resume reads the id back, refusing
    when there is no sidecar, and adds a line; `write_result` records how
    many resumes the run had."""
    side = sidecar(path)
    if not resume:
        rid = new_run_id()
        side.write_text(rid + "\n", encoding="utf-8", newline="\n")
        return rid
    if not side.exists():
        raise FileNotFoundError(f"{side.name} not found: no started run to "
                                "resume; start with resume=False")
    lines = side.read_text(encoding="utf-8").splitlines()
    rid = lines[0].strip() if lines else ""
    if not RUN_ID.fullmatch(rid):
        raise ValueError(f"{side.name} does not start with a run id")
    with side.open("a", encoding="utf-8", newline="\n") as f:
        f.write("resumed\n")
    _ISSUED.add(rid)
    return rid


def _resumes(path, run_id: str) -> int:
    side = sidecar(path)
    if not side.exists():
        return 0
    lines = side.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != run_id:
        return 0
    return sum(1 for ln in lines[1:] if ln.strip() == "resumed")


def write_result(path, doc: dict, generator, seeds, run_id: str,
                 replace: str | None = None) -> dict:
    """Write `doc` with its provenance block to `path`; return what was
    written. Refuses, with nothing written:
      - a file there from another run (or from before this rule), unless
        `replace` states why; the reason and the replaced run's id are
        recorded in the block;
      - a file there from this id when this process did not make or
        resume the id (`new_run_id`, `run_id_for`): a copied id;
      - a file that does not read back equal to what was meant.
    The temporary file sits beside the result, so the final step is one
    `os.replace` on the same volume."""
    path = Path(path)
    if not isinstance(run_id, str) or not RUN_ID.fullmatch(run_id):
        raise ValueError("write_result needs the run's id from new_run_id() "
                         "(32 hex characters)")
    if replace is not None and not str(replace).strip():
        raise ValueError("replace must state why the recorded result goes")
    block = record(generator, seeds)
    block["run_id"] = run_id
    resumes = _resumes(path, run_id)
    if resumes:
        block["resumed"] = resumes
    if path.exists():
        try:
            old = json.loads(path.read_text(encoding="utf-8"))
        except ValueError:
            old = None
        old_run = (old.get("provenance") or {}).get("run_id") \
            if isinstance(old, dict) else None
        if old_run != run_id:
            if replace is None:
                raise FileExistsError(
                    f"{path.name} holds a recorded result from another run "
                    f"({old_run or 'no run id'}); pass replace='<why>' to "
                    "replace it")
            block["replaces"] = {"reason": str(replace),
                                 "previous_run_id": old_run}
        else:
            if run_id not in _ISSUED:
                raise FileExistsError(
                    f"{path.name} holds run {run_id}, and this process did "
                    "not make or resume that id; resume a run with "
                    "run_id_for(path, resume=True)")
            if "replaces" in old.get("provenance", {}):
                block["replaces"] = old["provenance"]["replaces"]
    out = {**doc, "provenance": block}
    text = json.dumps(out, indent=1, default=strict_json.numpy_scalar) + "\n"
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8", newline="\n")
    try:
        back = json.loads(tmp.read_text(encoding="utf-8"))
        if back != json.loads(text):
            raise OSError(f"{tmp.name} did not read back as written")
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()
    return out


def problems(block) -> list[str]:
    """What a `provenance` block is missing or has malformed."""
    if not isinstance(block, dict):
        return ["no provenance block"]
    out = [f"missing {k}" for k in REQUIRED if k not in block]
    c = block.get("generator_commit")
    if "generator_commit" in block and not (
            isinstance(c, str) and len(c) == 40
            and all(ch in "0123456789abcdef" for ch in c)):
        out.append("generator_commit is not a full commit hash")
    if "generator_clean" in block and not isinstance(block["generator_clean"], bool):
        out.append("generator_clean is not true or false")
    s = block.get("seeds")
    if "seeds" in block and not (isinstance(s, list) and s
                                 and all(isinstance(x, int) for x in s)):
        out.append("seeds is not a non-empty list of integers")
    v = block.get("versions")
    if "versions" in block and not (isinstance(v, dict) and "python" in v
                                    and "numpy" in v):
        out.append("versions lacks python and numpy")
    return out
