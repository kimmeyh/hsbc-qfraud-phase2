"""Which test files to run for this branch: their red proofs (F177
change b, Sprint 31 D8) or their ordinary tests (Sprint 31 D17 option 1).

    <venv python> scripts/select_proofs.py              list the files
    <venv python> scripts/select_proofs.py --run        run their proofs
    <venv python> scripts/select_proofs.py --sample --run
                                     ... plus this sprint's 5% sample (CI)
    <venv python> scripts/select_proofs.py --tests      run their tests
    <venv python> scripts/select_proofs.py --base REF   compare with REF
    Arguments after `--` go to pytest (`-- --junitxml=out.xml`).

A red proof's answer changes only when its own test file, a file it
mutates, or the proof machinery changes
(`docs/testing/F180_PROOFS_AND_RISK_BASED_TESTING.md`). So a test file
is selected when, against the merge base with `--base` (default
`origin/develop`), plus uncommitted and untracked files:
  - the test file itself changed, or
  - a changed file is named in the test file's source, by its file name
    (`f157_spectra_algorithms.py`) or by its module stem as an import or
    a quoted string (`f157_spectra_algorithms`).
A change to the shared machinery (`injection.py`, a `conftest.py`,
`pytest.ini`) selects the test files that name it, not every file: it
selected all 58 proof files before D17, about 4 hours here (Sprint 31).

`--sample` adds a 5% rotating sample of the proof files: the files at
the positions that equal the sprint number modulo 20, so every proof file
runs at least once in 20 sprints (D17 c). CI's full job runs the
selection with the sample.

`--tests` runs the ordinary (non-proof) tests of the selected files, plus
the repository guards in `ALWAYS` and any test file whose source names a
changed file's directory (D17 a). CI's push job runs every non-proof test
on every push; it is the safety net for what this selection misses.

A passing `--tests` run records the tree it tested and its merge base, in
the git directory, for `.githooks/pre-push` (`check_pre_push.py`, Sprint
32 i2). Nothing is recorded when the run was narrowed by arguments after
`--`, when a file other than `UNTESTED_OK` is changed or untracked (the
tests would not have run on a committed tree), or when the tree changed
during the run. `--base origin/<branch>` tests only what is not pushed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = "experiments/src"
STATUS = ROOT / ".claude" / "sprint_status.json"
SAMPLE_CYCLE = 20                    # 5%: every proof file once in 20 sprints
# Cheap guards over the whole repository, run on every local change.
ALWAYS = ("experiments/src/test_us_english.py",
          "experiments/src/test_evidence_immutability.py")


def git(*args: str) -> list[str]:
    out = subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                         text=True)
    if out.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed: {out.stderr.strip()}")
    return [ln for ln in out.stdout.splitlines() if ln.strip()]


# Sprint state, not code: tracked, and changed by the task timer through
# the whole sprint, so a clean tree is never reached while a task runs.
# It is the one path a pushed tree may differ from the tested one in.
UNTESTED_OK = (".claude/sprint_status.json",)
MARKER = "select_proofs_passed"          # under the git directory
MARKER_KEEP = 50


def fingerprint(rev: str) -> str:
    """The tree at `rev`, less `UNTESTED_OK`, as one hash."""
    lines = [ln for ln in git("ls-tree", "-r", rev)
             if ln.split("\t", 1)[1] not in UNTESTED_OK]
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()


def other_changes() -> list[str]:
    """Changed or untracked paths besides `UNTESTED_OK`."""
    paths = [ln[3:].strip('"') for ln in
             git("status", "--porcelain", "--untracked-files=all")]
    return [p for p in paths if p not in UNTESTED_OK]


def marker_path() -> Path:
    p = Path(git("rev-parse", "--git-path", MARKER)[0])
    return p if p.is_absolute() else ROOT / p


def passed_runs() -> list[tuple[str, str]]:
    """(fingerprint, merge base) of each recorded passing run."""
    p = marker_path()
    if not p.exists():
        return []
    return [tuple(ln.split()[:2]) for ln in
            p.read_text(encoding="utf-8").splitlines() if len(ln.split()) >= 2]


def note_pass(before: str | None, merge: str, extra: list[str]) -> str:
    """Record a passing `--tests` run for the pre-push hook, or say why not."""
    if extra:
        return "not recorded for push: arguments after -- narrowed the run"
    if before is None or other_changes():
        return ("not recorded for push: files besides "
                f"{', '.join(UNTESTED_OK)} are changed or untracked; commit "
                "them and run again")
    if fingerprint("HEAD") != before:
        return "not recorded for push: HEAD changed during the run"
    runs = passed_runs() + [(before, merge)]
    marker_path().write_text("".join(f"{f} {m}\n" for f, m in
                                     runs[-MARKER_KEEP:]), encoding="utf-8")
    return f"recorded for push: HEAD's tree, tested from {merge[:9]}"


def changed_files(base: str) -> set[str]:
    merge = git("merge-base", base, "HEAD")[0]
    files = set(git("diff", "--name-only", merge))      # committed + staged + tree
    files |= set(git("ls-files", "--others", "--exclude-standard"))
    return {f.replace("\\", "/") for f in files}


def test_files() -> list[str]:
    return sorted(p.relative_to(ROOT).as_posix()
                  for p in (ROOT / TESTS).glob("test_*.py"))


def _read(f: str) -> str:
    return (ROOT / f).read_text(encoding="utf-8")


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


def names_directory(source: str, changed: str) -> bool:
    """The test names the changed file's directory, as a path string
    ("docs/learning") or a Path join ("docs" / "learning").

    Only a changed non-Python file in a folder two or more levels deep
    counts: a Python file is found by name, and almost every test names
    `docs` or `experiments/src`, which selected 110 of 163 files for one
    task's change on Sprint 31."""
    parts = Path(changed).parent.parts
    if Path(changed).suffix == ".py" or len(parts) < 2:
        return False
    return ("/".join(parts) in source
            or '" / "'.join(parts) in source)


def select(changed: set[str], tests: list[str] | None = None,
           read=_read) -> list[str]:
    tests = test_files() if tests is None else tests
    out = []
    for t in tests:
        if t in changed:
            out.append(t)
            continue
        src = read(t)
        if any(names_file(src, c) for c in changed if c != t):
            out.append(t)
    return out


def sample(tests: list[str], sprint: int, read=_read) -> list[str]:
    """This sprint's slice of the proof files: every SAMPLE_CYCLE-th one,
    starting at the sprint number modulo SAMPLE_CYCLE."""
    proofs = [t for t in sorted(tests) if "assert_can_fail" in read(t)]
    return [t for i, t in enumerate(proofs)
            if i % SAMPLE_CYCLE == sprint % SAMPLE_CYCLE]


def select_tests(changed: set[str], tests: list[str] | None = None,
                 read=_read) -> list[str]:
    tests = test_files() if tests is None else tests
    chosen = set(select(changed, tests, read))
    chosen |= {t for t in ALWAYS if t in tests}
    for t in tests:
        if t not in chosen and any(names_directory(read(t), c)
                                   for c in changed):
            chosen.add(t)
    return sorted(chosen)


def sprint_number(path: Path = STATUS) -> int:
    try:
        n = json.loads(path.read_text(encoding="utf-8"))[
            "current_sprint"]["number"]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise SystemExit(f"cannot read the sprint number from {path}: {exc}")
    if not isinstance(n, int) or isinstance(n, bool):
        raise SystemExit(f"{path}: the sprint number is not an integer")
    return n


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else list(argv)
    extra = argv[argv.index("--") + 1:] if "--" in argv else []
    argv = argv[:argv.index("--")] if "--" in argv else argv
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--base", default="origin/develop")
    ap.add_argument("--run", action="store_true",
                    help="run the selected files' proofs (-m proof)")
    ap.add_argument("--sample", action="store_true",
                    help="add this sprint's 5%% sample of proof files")
    ap.add_argument("--tests", action="store_true",
                    help="run the selected files' non-proof tests")
    args = ap.parse_args(argv)
    if args.tests and (args.run or args.sample):
        print("--tests runs ordinary tests; it takes no --run or --sample",
              file=sys.stderr)
        return 2
    changed = changed_files(args.base)
    if args.tests:
        before = None if other_changes() else fingerprint("HEAD")
        merge = git("merge-base", args.base, "HEAD")[0]
        chosen = select_tests(changed)
        marker, what = "not proof", "test file(s) to run locally"
    else:
        chosen = select(changed)
        if args.sample:
            chosen = sorted(set(chosen) | set(sample(test_files(),
                                                     sprint_number())))
        marker, what = "proof", "test file(s) with proofs to run"
    for t in chosen:
        print(t)
    print(f"{len(chosen)} {what}", file=sys.stderr)
    if not (args.run or args.tests):
        return 0
    rc = 0 if not chosen else subprocess.run(
        [sys.executable, "-m", "pytest", "-m", marker, "-q", "-p",
         "no:cacheprovider", *extra, *chosen], cwd=ROOT).returncode
    if args.tests and rc == 0:
        print(note_pass(before, merge, extra), file=sys.stderr)
    return rc


if __name__ == "__main__":
    sys.exit(main())
