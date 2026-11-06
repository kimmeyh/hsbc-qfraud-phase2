"""`scripts/suite_times.py` compares test-run times from junit reports
(F177, Sprint 31 Task C): each side's wall time is the sum of its
reports' testsuite times, and a report with no testsuite is refused.
Each term is proven red.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "suite_times.py"
sys.path.insert(0, str(SCRIPT.parent))
import suite_times as st  # noqa: E402

THIS = Path(__file__).relative_to(ROOT).as_posix()


def _report(path: Path, tests: int, failures: int, seconds: float,
            wrapped: bool = True) -> Path:
    suite = (f'<testsuite name="pytest" errors="0" failures="{failures}" '
             f'skipped="1" tests="{tests}" time="{seconds}"/>')
    path.write_text(f"<testsuites>{suite}</testsuites>" if wrapped else suite,
                    encoding="utf-8")
    return path


def test_a_side_sums_its_reports(tmp_path):
    before = _report(tmp_path / "b.xml", 100, 0, 200.0)
    a1 = _report(tmp_path / "a1.xml", 90, 2, 60.0)
    a2 = _report(tmp_path / "a2.xml", 20, 0, 40.0, wrapped=False)
    text = st.compare([before], [a1, a2])
    assert "before: 100 tests, 0 failed, 0 errors, 1 skipped; 200 s wall" in text
    assert "after: 110 tests, 2 failed, 0 errors, 2 skipped; 100 s wall" in text
    assert "after / before: 0.50" in text
    two = tmp_path / "two.xml"
    two.write_text('<testsuites><testsuite tests="3" time="10.0"/>'
                   '<testsuite tests="4" time="5.0"/></testsuites>',
                   encoding="utf-8")
    assert st.read(two)["seconds"] == 15.0 and st.read(two)["tests"] == 7


def test_a_report_with_no_testsuite_is_refused(tmp_path):
    bad = tmp_path / "bad.xml"
    bad.write_text("<other/>", encoding="utf-8")
    with pytest.raises(st.ReportError, match="no testsuite"):
        st.read(bad)
    good = _report(tmp_path / "g.xml", 1, 0, 1.0)
    assert st.main(["--before", str(bad), "--after", str(good)]) == 1


def test_a_before_side_with_no_time_is_refused(tmp_path):
    zero = _report(tmp_path / "z.xml", 1, 0, 0.0)
    good = _report(tmp_path / "g.xml", 1, 0, 1.0)
    with pytest.raises(st.ReportError, match="records no time"):
        st.compare([zero], [good])


def test_the_comparison_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    for old, new, test, label in (
            ('        out["seconds"] += float(s.get("time", 0))\n',
             '        out["seconds"] = float(s.get("time", 0))\n',
             "test_a_side_sums_its_reports", "a side keeps only its last report"),
            ("    if not suites:\n", "    if False:\n",
             "test_a_report_with_no_testsuite_is_refused",
             "an empty report read as zero"),
            ('    if b["seconds"] <= 0:\n', "    if False:\n",
             "test_a_before_side_with_no_time_is_refused",
             "a ratio against no time")):
        assert_can_fail([Mutation(SCRIPT, old, new, expect_occurrences=1)],
                        lambda test=test: run_pytest(f"{THIS}::{test}", ROOT),
                        label)
