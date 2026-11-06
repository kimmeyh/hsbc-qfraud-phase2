"""Fail CI's push job only on a changed refusal line that no test ran.

Sprint 31 D16 option 1 (team lead, 2026-11-06). F177 change c failed the
push job on every changed line no test ran; on cdb8471 that was 478
lines, almost all the `run` and `main` paths of experiment modules that
need the raw data or a device. The class the gate exists for is the
untested refusal (37 reached review in Sprints 28-30), so this script
reads diff-cover's JSON report and fails only when an uncovered changed
line is a refusal: a `raise`, `sys.exit(...)` or `SystemExit`. Every other
uncovered line is listed, and does not fail.

Usage: python scripts/refusal_coverage.py diff-cover.json

Exit 0: no untested changed refusal. Exit 1: at least one, each listed.
Exit 2: the report is missing or malformed, or names a file that is not
there. "Could not tell" is never green.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# A statement that refuses: `raise ...`, `sys.exit(...)`, `SystemExit(...)`
# anywhere on the line (as in `raise SystemExit(...)` or `exit(SystemExit)`).
REFUSAL = re.compile(r"^\s*raise\b|\bsys\.exit\s*\(|\bSystemExit\b")
# A module's entry line, `raise SystemExit(main(...))` or
# `sys.exit(main(...))`, passes on main's exit code and refuses nothing:
# 10 of the 19 "refusals" counted on cdb8471 were these.
ENTRY = re.compile(r"^\s*(raise\s+SystemExit|sys\.exit)\(\s*main\(")


def is_refusal(line: str) -> bool:
    code = line.split("#", 1)[0]
    return bool(REFUSAL.search(code)) and not ENTRY.match(code)


def uncovered(report: dict) -> dict[str, list[int]]:
    """{path: sorted uncovered changed line numbers} from diff-cover's
    JSON report (`src_stats` -> path -> `violation_lines`)."""
    stats = report["src_stats"]
    if not isinstance(stats, dict):
        raise ValueError("src_stats is not an object")
    out = {}
    for path, entry in stats.items():
        lines = entry["violation_lines"]
        if not all(isinstance(n, int) for n in lines):
            raise ValueError(f"{path}: violation_lines are not line numbers")
        if lines:
            out[path] = sorted(lines)
    return out


def classify(missed: dict[str, list[int]], root: Path | None = None):
    """([(path, line, text)] refusals, [(path, line, text)] others).
    Paths are relative to `root`, by default the working directory, where
    diff-cover ran (the repository root in CI)."""
    root = Path.cwd() if root is None else root
    refusals, others = [], []
    for path, numbers in sorted(missed.items()):
        src = (root / path).read_text(encoding="utf-8").splitlines()
        for n in numbers:
            if not 1 <= n <= len(src):
                raise ValueError(f"{path}:{n} is past the end of the file")
            row = (path, n, src[n - 1].strip())
            (refusals if is_refusal(src[n - 1]) else others).append(row)
    return refusals, others


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: refusal_coverage.py <diff-cover JSON report>",
              file=sys.stderr)
        return 2
    try:
        report = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
        refusals, others = classify(uncovered(report))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"::error::cannot read the diff-cover report: {exc}")
        return 2
    print(f"{len(others)} changed line(s) no test ran that are not "
          "refusals (listed, not failed):")
    for path, n, text in others:
        print(f"  {path}:{n}: {text}")
    if refusals:
        print(f"::error::{len(refusals)} changed refusal line(s) no test "
              "ran. Each refusal needs a test (the per-term rule):")
        for path, n, text in refusals:
            print(f"::error file={path},line={n}::{text}")
        return 1
    print("Every changed refusal line was run by a test.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
