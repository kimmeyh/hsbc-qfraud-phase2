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


def new_run_id() -> str:
    """One per run, made fresh when the run starts. Every write of that run
    passes the same id, so the run may rewrite its own file. The refusal
    holds only while each run makes its own id: `write_result` refuses an
    id that is not 32 hex characters, so a constant name cannot switch it
    off, but a caller that copies the id out of a recorded result can.
    A resumed run in a new process is a new run and states `replace=`."""
    return uuid.uuid4().hex


def write_result(path, doc: dict, generator, seeds, run_id: str,
                 replace: str | None = None) -> dict:
    """Write `doc` with its provenance block to `path`; return what was
    written. Refuses, with nothing written:
      - a file there from another run (or from before this rule), unless
        `replace` states why; the reason and the replaced run's id are
        recorded in the block;
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
        elif isinstance(old, dict) and "replaces" in old.get("provenance", {}):
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
