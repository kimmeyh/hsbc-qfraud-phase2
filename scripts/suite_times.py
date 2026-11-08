"""Compare test-run times from `pytest --junitxml` reports (F177, Sprint 31
Task C).

    <venv python> scripts/suite_times.py --before B.xml --after A1.xml [A2.xml ...]

Each side is one or more reports of runs made one after another (the
parallel non-proof run, then the `serial` files alone), so a side's wall
time is the sum of its reports' `testsuite` times. Printed per side: the
tests, failures, errors and skips counted in its reports and its wall
seconds; then the after side's wall time as a share of the before side's.
The figures come only from the reports, so the comparison can be
re-made from them. A report with no `testsuite` element is refused.
"""
from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

COUNTS = ("tests", "failures", "errors", "skipped")


class ReportError(ValueError):
    pass


def read(path: Path) -> dict:
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else root.findall("testsuite")
    if not suites:
        raise ReportError(f"{path}: no testsuite element")
    out = {k: 0 for k in COUNTS}
    out["seconds"] = 0.0
    for s in suites:
        for k in COUNTS:
            out[k] += int(s.get(k, 0))
        out["seconds"] += float(s.get("time", 0))
    return out


def side(paths: list[Path]) -> dict:
    total = {k: 0 for k in COUNTS}
    total["seconds"] = 0.0
    for p in paths:
        r = read(p)
        for k in total:
            total[k] += r[k]
    return total


def line(name: str, s: dict) -> str:
    return (f"{name}: {s['tests']} tests, {s['failures']} failed, "
            f"{s['errors']} errors, {s['skipped']} skipped; "
            f"{s['seconds']:.0f} s wall")


def compare(before: list[Path], after: list[Path]) -> str:
    b, a = side(before), side(after)
    if b["seconds"] <= 0:
        raise ReportError("the before side records no time")
    share = a["seconds"] / b["seconds"]
    return "\n".join([line("before", b), line("after", a),
                      f"after / before: {share:.2f}"])


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--before", nargs="+", type=Path, required=True)
    ap.add_argument("--after", nargs="+", type=Path, required=True)
    args = ap.parse_args(argv)
    try:
        print(compare(args.before, args.after))
    except (ReportError, ET.ParseError, OSError) as exc:
        print(f"suite_times: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
