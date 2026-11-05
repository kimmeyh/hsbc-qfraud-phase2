"""The test inventory: one row per test file (F180, Sprint 31).

Usage:
    python scripts/test_inventory.py --local LOCAL.xml [--ci CI.xml] \\
        [--out docs/testing/F180_TEST_INVENTORY.md]

LOCAL.xml and CI.xml are `pytest --junitxml` reports of a full run (every
proof and every slow test). The script collects the suite itself, so the
proof and slow markers are the ones `conftest.py` sets, not a second
reading of the source. Every figure in a row is measured or counted; the
kind and the risk tier follow the stated rules below, and the rules, not a
judgment per file, decide them.

Columns:
  - Guards: the first sentence of the file's docstring.
  - Kind: "red proof" if a test in it is marked proof; else "pipeline" if
    one is marked slow; else "document" if it reads a file under `docs/`;
    else "guard" if it reads repository source, a hook or CI by path;
    else "unit".
  - Tests, proofs, slow: counts from collection.
  - Local s and CI s: summed test time from each report, proofs apart.
  - Runs in: push (non-proof, non-slow tests), full (every non-slow test),
    local (slow tests, which no CI job runs).
  - Tier: "high" when the file guards a record or a boundary (HIGH_IMPACT
    below); otherwise "normal".
  - Last fix: the date of the newest `fix` commit that touched the file.
    This is when the file last changed in a fix, which is not always when
    it caught a defect; the retrospectives name the catches.
"""
from __future__ import annotations

import argparse
import ast
import re
import subprocess
import sys
# The reports are this suite's own output, read locally.
import xml.etree.ElementTree as ET  # noqa: S405
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "experiments" / "src"
OUT = ROOT / "docs" / "testing" / "F180_TEST_INVENTORY.md"

# A missed defect here damages a document of record, the evidence, the
# confidentiality boundary or a metered run (F180 part 7, ISTQB CTFL v4.0.1
# section 5.2: risk is likelihood times impact; these are the high-impact
# guards).
HIGH_IMPACT = (
    "test_evidence_immutability", "test_published_artifacts",
    "test_submission", "test_provenance", "test_result_writer",
    "test_device_store", "test_criterion_h", "test_confidential",
    "test_cross_repo", "test_phase1_boundary", "test_preregistration",
    "test_outcome_record", "test_row_schema", "test_hardware",
    "test_metered", "test_pre_commit", "test_commit_msg",
    "test_phase2_device_default",
)


def _empty() -> dict:
    return {"tests": 0, "proofs": 0, "slow": 0}


class _Collector:
    def __init__(self):
        self.items: dict[str, dict] = defaultdict(_empty)
        self.proofs: dict[str, set[str]] = defaultdict(set)

    def pytest_collection_finish(self, session):
        for item in session.items:
            f = Path(str(item.fspath)).name
            row = self.items[f]
            row["tests"] += 1
            if item.get_closest_marker("proof"):
                row["proofs"] += 1
                self.proofs[f].add(item.name)
            if item.get_closest_marker("slow"):
                row["slow"] += 1


def collect() -> tuple[dict[str, dict], dict[str, set[str]]]:
    import pytest
    c = _Collector()
    code = pytest.main(["--collect-only", "-q", "-p", "no:cacheprovider",
                        str(TESTS)], plugins=[c])
    if code not in (0, 5):
        raise SystemExit(f"collection failed (pytest exit {code})")
    return dict(c.items), dict(c.proofs)


def times(report: Path, proofs: dict[str, set[str]]):
    """Per file: [non-proof seconds, proof seconds] from a junit report."""
    out: dict[str, list[float]] = defaultdict(lambda: [0.0, 0.0])
    for case in ET.parse(report).getroot().iter("testcase"):
        cls = case.get("classname", "")
        if not cls:
            continue
        f = cls.split(".")[-1] + ".py"
        is_proof = case.get("name", "") in proofs.get(f, set())
        out[f][1 if is_proof else 0] += float(case.get("time", 0) or 0)
    return out


def guards(path: Path) -> str:
    try:
        doc = ast.get_docstring(ast.parse(path.read_text(encoding="utf-8")))
    except SyntaxError:
        return "(does not parse)"
    if not doc:
        return "(no docstring)"
    first = " ".join(doc.split("\n\n")[0].split())
    m = re.match(r"(.+?[.!?])(\s|$)", first)
    s = m.group(1) if m else first
    return (s[:117] + "...") if len(s) > 120 else s


def kind(path: Path, row: dict) -> str:
    if row["proofs"]:
        return "red proof"
    if row["slow"]:
        return "pipeline"
    src = path.read_text(encoding="utf-8")
    if re.search(r"[\"']docs[/\"']|ROOT / \"docs\"", src):
        return "document"
    if re.search(r"\.claude|\.github|\.githooks|scripts[/\"']|"
                 r"ROOT / \"experiments\"", src):
        return "guard"
    return "unit"


def last_fix(path: Path) -> str:
    r = subprocess.run(["git", "log", "-1", "--format=%as", "-E",
                        "--grep=^fix", "--", path.relative_to(ROOT).as_posix()],
                       cwd=ROOT, capture_output=True, text=True)
    return r.stdout.strip() or "none"


def tier(name: str) -> str:
    stem = name[:-3]
    return "high" if any(stem.startswith(h) for h in HIGH_IMPACT) else "normal"


def runs_in(row: dict) -> str:
    places = []
    if row["tests"] - row["proofs"] - row["slow"] > 0:
        places.append("push")
    if row["tests"] - row["slow"] > 0:
        places.append("full")
    if row["slow"]:
        places.append("local")
    return ", ".join(places) or "nowhere"


def render(rows, local, ci, local_name, ci_name) -> str:
    head = [
        "# F180 Test Inventory",
        "",
        "Generated by `scripts/test_inventory.py`; do not edit by hand. "
        "The command and the column rules are in that script's docstring.",
        "",
        f"- Local report: `{local_name}`",
        f"- CI report: `{ci_name}`" if ci_name else
        "- CI report: none given; the CI columns are blank",
        "",
        "| File | Guards | Kind | Tests | Proofs | Slow | Local s | "
        "Local proof s | CI s | CI proof s | Runs in | Tier | Last fix |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    lines = []
    for name in sorted(rows):
        r = rows[name]
        path = TESTS / name
        lt, ct = local.get(name, [0.0, 0.0]), ci.get(name)
        cis = (f"{ct[0]:.1f}", f"{ct[1]:.1f}") if ct else ("", "")
        g = guards(path).replace("|", "\\|")
        lines.append(
            f"| {name} | {g} | {kind(path, r)} | {r['tests']} | "
            f"{r['proofs']} | {r['slow']} | {lt[0]:.1f} | {lt[1]:.1f} | "
            f"{cis[0]} | {cis[1]} | {runs_in(r)} | {tier(name)} | "
            f"{last_fix(path)} |")
    return "\n".join(head + lines) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--local", type=Path, required=True)
    ap.add_argument("--ci", type=Path, default=None)
    ap.add_argument("--out", type=Path, default=OUT)
    args = ap.parse_args(argv)
    rows, names = collect()
    # A file with no test collected is still a row: an empty test file is
    # a guard that cannot fail.
    for p in TESTS.glob("test_*.py"):
        rows.setdefault(p.name, _empty())
    local = times(args.local, names)
    ci = times(args.ci, names) if args.ci else {}
    text = render(rows, local, ci, args.local.name,
                  args.ci.name if args.ci else "")
    args.out.write_bytes(text.encode("utf-8"))
    print(f"wrote {args.out} ({len(rows)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
