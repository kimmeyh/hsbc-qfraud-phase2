"""`scripts/refusal_coverage.py` fails only on an untested changed
refusal line (Sprint 31 D16 option 1). Each refusal and exit state has a
test, and each test is proven red below."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "refusal_coverage.py"
THIS = Path(__file__).relative_to(ROOT).as_posix()
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import refusal_coverage as rc  # noqa: E402

SRC = ("def f(x):\n"
       "    if x:\n"
       "        raise ValueError('no')\n"
       "    y = x + 1  # raise in a comment is not a refusal\n"
       "    sys.exit(2)\n"
       "    raise SystemExit(1)\n"
       "    return y\n")


def _report(tmp: Path, lines: list, name: str = "m.py") -> Path:
    (tmp / name).write_text(SRC, encoding="utf-8")
    p = tmp / "diff.json"
    p.write_text(json.dumps({"src_stats": {name: {
        "violation_lines": lines}}}), encoding="utf-8")
    return p


def _run(*args: str, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT), *args], cwd=cwd,
                          capture_output=True, text=True)


def test_refusal_lines_are_recognized():
    assert rc.is_refusal("        raise ValueError('no')")
    assert rc.is_refusal("    raise")
    assert rc.is_refusal("    sys.exit(2)")
    assert rc.is_refusal("    raise SystemExit(1)")
    assert rc.is_refusal("    exc = SystemExit(2)")
    # The bare name refuses nothing (PR 92 review).
    assert not rc.is_refusal("    except SystemExit as exc:")
    assert not rc.is_refusal("    with pytest.raises(SystemExit, match='x'):")
    assert not rc.is_refusal("    y = x + 1  # raise in a comment")
    assert not rc.is_refusal("    y = x + 1  # not sys.exit(2): a comment")
    assert not rc.is_refusal("    raised = True")
    assert not rc.is_refusal("    return y")


def test_a_module_entry_line_is_not_a_refusal():
    assert not rc.is_refusal("    raise SystemExit(main())")
    assert not rc.is_refusal("    raise SystemExit(main(sys.argv[1:]))")
    assert not rc.is_refusal("    sys.exit(main())")
    assert rc.is_refusal("    raise SystemExit(mainly_wrong)")


def test_classify_splits_refusals_from_other_lines(tmp_path):
    (tmp_path / "m.py").write_text(SRC, encoding="utf-8")
    refusals, others = rc.classify({"m.py": [3, 4, 5, 6, 7]}, tmp_path)
    assert [n for _, n, _ in refusals] == [3, 5, 6]
    assert [n for _, n, _ in others] == [4, 7]


def test_an_untested_refusal_fails_and_is_named(tmp_path):
    report = _report(tmp_path, [3, 4])
    r = _run(str(report), cwd=tmp_path)
    assert r.returncode == 1, r.stdout + r.stderr
    assert "::error file=m.py,line=3::raise ValueError('no')" in r.stdout


def test_other_untested_lines_are_listed_and_pass(tmp_path):
    report = _report(tmp_path, [4, 7])
    r = _run(str(report), cwd=tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "m.py:4:" in r.stdout and "m.py:7:" in r.stdout
    assert "Every changed refusal line was run by a test." in r.stdout


def test_a_clean_report_passes(tmp_path):
    report = _report(tmp_path, [])
    assert _run(str(report), cwd=tmp_path).returncode == 0


def test_usage_and_unreadable_reports_exit_2(tmp_path):
    assert _run(cwd=tmp_path).returncode == 2
    assert _run(str(tmp_path / "absent.json"), cwd=tmp_path).returncode == 2
    bad = tmp_path / "bad.json"
    bad.write_text("not json", encoding="utf-8")
    assert _run(str(bad), cwd=tmp_path).returncode == 2


def test_malformed_report_contents_exit_2(tmp_path):
    for doc in ({}, {"src_stats": []},
                {"src_stats": {"m.py": {}}},
                {"src_stats": {"m.py": {"violation_lines": ["3"]}}},
                {"src_stats": {"m.py": {"violation_lines": [99]}}},
                {"src_stats": {"gone.py": {"violation_lines": [1]}}}):
        (tmp_path / "m.py").write_text(SRC, encoding="utf-8")
        p = tmp_path / "doc.json"
        p.write_text(json.dumps(doc), encoding="utf-8")
        r = _run(str(p), cwd=tmp_path)
        assert r.returncode == 2, (doc, r.stdout)
        assert "cannot read the diff-cover report" in r.stdout


# ------------------------------------------------------------- red proofs

def test_each_rule_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    for old, new, test, label in (
            ('REFUSAL = re.compile(r"^\\s*raise\\b|', 'REFUSAL = re.compile(r"^\\s*raisex\\b|',
             "test_refusal_lines_are_recognized", "a raise not recognized"),
            ('|\\bSystemExit\\s*\\(")', '|\\bSystemExit\\b")',
             "test_refusal_lines_are_recognized",
             "the bare name SystemExit read as a refusal"),
            ('    code = line.split("#", 1)[0]\n', "    code = line\n",
             "test_refusal_lines_are_recognized", "a comment read as code"),
            (" and not ENTRY.match(code)", "",
             "test_a_module_entry_line_is_not_a_refusal",
             "an entry line read as a refusal"),
            ('ENTRY = re.compile(r"^\\s*(raise\\s+SystemExit|sys\\.exit)\\(\\s*main\\(")',
             'ENTRY = re.compile(r"^\\s*(raise\\s+SystemExit|sys\\.exit)\\(")',
             "test_a_module_entry_line_is_not_a_refusal",
             "every SystemExit read as an entry line"),
            ("            (refusals if is_refusal(src[n - 1]) else others).append(row)\n",
             "            others.append(row)\n",
             "test_classify_splits_refusals_from_other_lines",
             "every line classed as not a refusal"),
            ("        return 1\n", "        return 0\n",
             "test_an_untested_refusal_fails_and_is_named",
             "an untested refusal passes"),
            ("            if not 1 <= n <= len(src):\n", "            if False:\n",
             "test_malformed_report_contents_exit_2",
             "a line past the end read as covered")):
        assert_can_fail([Mutation(SCRIPT, old, new, expect_occurrences=1)],
                        lambda test=test: run_pytest(f"{THIS}::{test}", ROOT),
                        label)
