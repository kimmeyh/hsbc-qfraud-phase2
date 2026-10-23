"""What a Phase 2 result was made with, so it can be reproduced.

Sprint 28 D4 part 3 (team lead, 2026-10-23): every future ML, QML,
optimization or tensor run stores its data so results can be reproduced
and compared over time. Every new result file under
`experiments/phase2/results/` carries `provenance`: the generator's git
commit, whether the generator file matched that commit, the seeds, and the
library versions. `test_outcome_record_required.py` fails a new file
without it.

Use:  doc["provenance"] = provenance.record(__file__, seeds)
"""
from __future__ import annotations

import subprocess
import sys
from importlib import metadata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

# Recorded when installed; a package that is absent is left out, not faked.
PACKAGES = ("numpy", "scipy", "pandas", "scikit-learn", "xgboost", "lightgbm",
            "catboost", "imbalanced-learn", "eqc-models", "qci-client")
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
