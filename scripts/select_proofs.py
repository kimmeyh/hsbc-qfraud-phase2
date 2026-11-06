"""Which test files' red proofs need a local run for this branch (F177
change b, Sprint 31 D8).

    <venv python> scripts/select_proofs.py              list the test files
    <venv python> scripts/select_proofs.py --run        run their proofs
    <venv python> scripts/select_proofs.py --base REF   compare with REF

A red proof's answer changes only when its own test file, a file it
mutates, or the shared machinery (`injection.py`, `conftest.py`)
changes (`docs/testing/F180_PROOFS_AND_RISK_BASED_TESTING.md`). So a
test file is selected when, against the merge base with `--base`
(default `origin/develop`), plus uncommitted and untracked files:
  - the test file itself changed, or
  - `experiments/src/injection.py`, a `conftest.py` or `pytest.ini`
    changed (then every test file is selected), or
  - a changed file is named in the test file's source, by its file name
    (`f157_spectra_algorithms.py`) or by its module stem as an import or
    a quoted string (`f157_spectra_algorithms`).
The name rule finds the file a proof mutates when the test names it, as
every proof here does (`Mutation(SRC, ...)` with `SRC` built from the
file name). It can select too much, never too little, for such a proof.
A proof that mutates a file it never names is the gap; CI's full job,
which runs every proof, is the safety net (D8 change a).
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = "experiments/src"
SHARED = ("experiments/src/injection.py", "conftest.py", "pytest.ini")


def git(*args: str) -> list[str]:
    out = subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                         text=True)
    if out.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed: {out.stderr.strip()}")
    return [ln for ln in out.stdout.splitlines() if ln.strip()]


def changed_files(base: str) -> set[str]:
    merge = git("merge-base", base, "HEAD")[0]
    files = set(git("diff", "--name-only", merge))      # committed + staged + tree
    files |= set(git("ls-files", "--others", "--exclude-standard"))
    return {f.replace("\\", "/") for f in files}


def test_files() -> list[str]:
    return sorted(p.relative_to(ROOT).as_posix()
                  for p in (ROOT / TESTS).glob("test_*.py"))


def names_file(source: str, changed: str) -> bool:
    name = Path(changed).name
    if name in source:
        return True
    stem = Path(changed).stem
    if Path(changed).suffix != ".py" or not stem.isidentifier():
        return False
    return re.search(rf"(?:\bimport\s+{re.escape(stem)}\b|\bfrom\s+"
                     rf"{re.escape(stem)}\b|[\"']{re.escape(stem)}[\"'])",
                     source) is not None


def select(changed: set[str], tests: list[str] | None = None,
           read=lambda f: (ROOT / f).read_text(encoding="utf-8")) -> list[str]:
    tests = test_files() if tests is None else tests
    if any(c == s or c.endswith("/conftest.py") for c in changed
           for s in SHARED):
        return list(tests)
    out = []
    for t in tests:
        if t in changed:
            out.append(t)
            continue
        src = read(t)
        if any(names_file(src, c) for c in changed if c != t):
            out.append(t)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--base", default="origin/develop")
    ap.add_argument("--run", action="store_true",
                    help="run the selected files' proofs (-m proof)")
    args = ap.parse_args(argv)
    chosen = select(changed_files(args.base))
    for t in chosen:
        print(t)
    print(f"{len(chosen)} test file(s) with proofs to run locally",
          file=sys.stderr)
    if not args.run or not chosen:
        return 0
    return subprocess.run([sys.executable, "-m", "pytest", "-m", "proof",
                           "-q", "-p", "no:cacheprovider", *chosen],
                          cwd=ROOT).returncode


if __name__ == "__main__":
    sys.exit(main())
