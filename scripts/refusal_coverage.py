"""Fail CI's push job only on a changed refusal line that no test ran.

Sprint 31 D16 option 1 (team lead, 2026-11-06). F177 change c failed the
push job on every changed line no test ran; on cdb8471 that was 478
lines, almost all the `run` and `main` paths of experiment modules that
need the raw data or a device. The class the gate exists for is the
untested refusal (37 reached review in Sprints 28-30), so this script
reads diff-cover's JSON report and fails only when an uncovered changed
line is a refusal: a `raise` (also a one-line `if bad: raise`),
`sys.exit(...)`, `SystemExit(...)` or a `print("REFUSING ...")`. Every
other uncovered line is listed, and does not fail. Coverage is by branch
(F194, Sprint 32: `branch = True` in `.coveragerc`, `--branch-coverage`
on diff-cover in `ci.yml`), so a line counts as uncovered when a branch
on it was not taken: a one-line `if bad: raise` whose raise no test
takes is listed, though its condition ran.

Usage: python scripts/refusal_coverage.py diff-cover.json

Exit 0: no untested changed refusal. Exit 1: at least one, each listed.
Exit 2: the report is missing or malformed, or names a file that is not
there. "Could not tell" is never green.
"""
from __future__ import annotations

import json
import re
import sys
import tokenize
from pathlib import Path

# A statement that refuses: `raise ...`, `sys.exit(...)`, or a
# `SystemExit(...)` built anywhere on the line. The bare name is not one:
# `except SystemExit as exc:` and `pytest.raises(SystemExit, ...)` refuse
# nothing (PR 92 review). Sprint 31 i3 (team lead, 2026-11-07) adds the
# repository's two other forms: a one-line `if bad: raise ...`, and the
# commonest, `print("REFUSING: ...")` followed by `return N`, seen by its
# print (silent-failure finding 4 of the PR 92 review). The print may
# carry any string prefix (`f"`, `rf"`, `fr"`, `F"`, `R"` ...; F194). The
# one-line form is matched with string literals blanked, so `: raise`
# inside a string on an `if` line is not a refusal (F194).
REFUSAL = re.compile(
    r"^\s*raise\b|\bsys\.exit\s*\(|\bSystemExit\s*\("
    r"|\b(?:print|write)\s*\(\s*[rRfFbBuU]{0,2}[\"']REFUSING\b")
ONE_LINE = re.compile(
    r"^\s*(?:if|elif|else|except|for|while|with)\b.*:\s*raise\b")
STRING = re.compile(r"""(?<!\w)[rRfFbBuU]{0,2}"""
                    r"""("[^"\\]*(?:\\.[^"\\]*)*"|'[^'\\]*(?:\\.[^'\\]*)*')""")
# A module's entry line, `raise SystemExit(main(...))` or
# `sys.exit(main(...))`, passes on main's exit code and refuses nothing:
# 10 of the 19 "refusals" counted on cdb8471 were these.
ENTRY = re.compile(r"^\s*(raise\s+SystemExit|sys\.exit)\(\s*main\(")


def is_refusal(line: str) -> bool:
    code = line.split("#", 1)[0]
    hit = REFUSAL.search(code) or ONE_LINE.search(STRING.sub("''", code))
    return bool(hit) and not ENTRY.match(code)


def statement(src: list[str], n: int) -> str:
    """The statement that starts on line `n` (1-based), its continuation
    lines joined and each line's comment removed. coverage.py names a
    multi-line statement by its first line, so `print(` alone on line n
    with `"REFUSING: ..."` on line n + 1 is still seen. Source the
    tokenizer cannot read from line n is judged by line n alone."""
    rest = iter(s + "\n" for s in src[n - 1:])
    end = n
    try:
        for tok in tokenize.generate_tokens(lambda: next(rest, "")):
            if tok.type in (tokenize.NEWLINE, tokenize.ENDMARKER):
                end = n + tok.start[0] - 1
                break
    except (tokenize.TokenError, SyntaxError):
        end = n
    return " ".join(s.split("#", 1)[0] for s in src[n - 1:max(end, n)])


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
            (refusals if is_refusal(statement(src, n)) else others).append(row)
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
