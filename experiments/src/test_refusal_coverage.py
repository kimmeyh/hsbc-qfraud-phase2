"""`scripts/refusal_coverage.py` fails only on an untested changed
refusal line (Sprint 31 D16 option 1). Each refusal and exit state has a
test, and each test is proven red below."""
from __future__ import annotations

import json
import os
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


def test_a_one_line_raise_is_a_refusal():
    """Sprint 31 i3: `if bad: raise ...` on one line."""
    assert rc.is_refusal("    if bad: raise ValueError('no')")
    assert rc.is_refusal("    else: raise ClaimError('x')")
    assert not rc.is_refusal("    if raised: count += 1")
    assert not rc.is_refusal("    note = 'x: raise later'")


def test_a_refusing_print_is_a_refusal():
    """Sprint 31 i3: the repository's commonest refusal,
    `print("REFUSING: ..."); return N`, seen by its print."""
    assert rc.is_refusal('    print("REFUSING: no ledger", file=sys.stderr)')
    assert rc.is_refusal("    print(f'REFUSING {label}: {why}')")
    assert rc.is_refusal('    sys.stderr.write("REFUSING: x")')
    assert not rc.is_refusal('    assert "REFUSING" in out')
    assert not rc.is_refusal('    print("not REFUSING anything")')


def test_a_refusing_print_with_any_prefix_is_a_refusal():
    """F194: the `rf"`, `fr"` and `F"` prefixes, each on its own line."""
    assert rc.is_refusal('    print(rf"REFUSING {p}: no match")')
    assert rc.is_refusal('    print(fr"REFUSING {p}: no match")')
    assert rc.is_refusal('    print(F"REFUSING: {why}")')


def test_raise_inside_a_string_is_not_a_one_line_refusal():
    """F194: `: raise` inside a string on an `if` line refuses nothing."""
    assert not rc.is_refusal('    if note == "x: raise": count += 1')
    assert not rc.is_refusal("    if s.endswith(': raise'): n += 1")
    assert rc.is_refusal('    if note == "x": raise ValueError("y")')


BRANCHY = ("def f(bad):\n"
           "    if bad: raise ValueError('bad')\n"
           "    return 1\n")


def test_a_refusal_whose_branch_no_test_takes_fails(tmp_path):
    """F194 end to end: coverage by branch and diff-cover's
    `--branch-coverage`, as CI runs them, fail a one-line refusal whose
    condition ran and whose raise did not."""
    env = {k: v for k, v in os.environ.items()
           if not k.startswith("COVERAGE_")}

    def sh(*cmd):
        r = subprocess.run(cmd, cwd=tmp_path, env=env, capture_output=True,
                           text=True)
        assert r.returncode == 0, (cmd, r.stdout, r.stderr)

    git = ("git", "-c", "user.name=t", "-c", "user.email=t@t",
           "-c", "core.autocrlf=false")
    sh(*git, "init", "-q", "-b", "main")
    (tmp_path / "base.py").write_text("x = 1\n", encoding="utf-8")
    sh(*git, "add", "base.py")
    sh(*git, "commit", "-q", "-m", "base")
    sh(*git, "checkout", "-q", "-b", "change")
    (tmp_path / "m.py").write_text(BRANCHY, encoding="utf-8")
    (tmp_path / "run.py").write_text("import m\nm.f(False)\n",
                                     encoding="utf-8")
    sh(*git, "add", "m.py", "run.py")
    sh(*git, "commit", "-q", "-m", "change")
    (tmp_path / ".coveragerc").write_text(
        "[run]\nbranch = " + str(coveragerc_branch()) + "\n",
        encoding="utf-8")
    sh(sys.executable, "-m", "coverage", "run", "run.py")
    sh(sys.executable, "-m", "coverage", "xml", "-q", "-o", "cov.xml")
    flags = [f for f in ("--branch-coverage",) if f in ci_diff_cover_line()]
    sh(sys.executable, "-m", "diff_cover.diff_cover_tool", "cov.xml",
       "--compare-branch=main", *flags, "--format", "json:d.json")
    r = _run("d.json", cwd=tmp_path)
    assert r.returncode == 1, r.stdout + r.stderr
    assert "::error file=m.py,line=2::" in r.stdout


def coveragerc_branch() -> bool:
    """`branch = True` in the repository's `.coveragerc` [run] section."""
    import configparser
    cp = configparser.ConfigParser()
    cp.read(ROOT / ".coveragerc", encoding="utf-8")
    return cp.getboolean("run", "branch", fallback=False)


def ci_diff_cover_line() -> str:
    """The diff-cover command in CI's push job."""
    text = (ROOT / ".github" / "workflows" / "ci.yml").read_text(
        encoding="utf-8")
    hits = [ln for ln in text.splitlines()
            if ln.strip().startswith("diff-cover ")]
    assert len(hits) == 1, hits
    return hits[0]


def test_ci_measures_branches():
    assert coveragerc_branch()
    assert "--branch-coverage" in ci_diff_cover_line()


MULTI = ("def g(x):\n"
         "    print(\n"
         "        \"REFUSING: no ledger\",  # the reason\n"
         "        file=sys.stderr)\n"
         "    return 2\n")


def test_a_multi_line_refusal_is_seen_by_its_first_line(tmp_path):
    """coverage.py names a multi-line statement by its first line, which
    here is `print(` alone."""
    (tmp_path / "m.py").write_text(MULTI, encoding="utf-8")
    refusals, others = rc.classify({"m.py": [2, 5]}, tmp_path)
    assert [n for _, n, _ in refusals] == [2]
    assert [n for _, n, _ in others] == [5]


def test_source_the_tokenizer_cannot_read_is_judged_by_its_line(tmp_path):
    (tmp_path / "m.py").write_text("x = (\n", encoding="utf-8")
    refusals, others = rc.classify({"m.py": [1]}, tmp_path)
    assert refusals == [] and [n for _, n, _ in others] == [1]


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
            ('    r"^\\s*raise\\b|', '    r"^\\s*raisex\\b|',
             "test_refusal_lines_are_recognized", "a raise not recognized"),
            ('|\\bSystemExit\\s*\\("\n', '|\\bSystemExit\\b"\n',
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
            ('    hit = REFUSAL.search(code) or '
             'ONE_LINE.search(STRING.sub("\'\'", code))\n',
             '    hit = REFUSAL.search(code)\n',
             "test_a_one_line_raise_is_a_refusal",
             "a one-line raise not recognized"),
            ('ONE_LINE.search(STRING.sub("\'\'", code))',
             'ONE_LINE.search(code)',
             "test_raise_inside_a_string_is_not_a_one_line_refusal",
             "a raise inside a string read as a refusal"),
            (r'''    r"|\b(?:print|write)\s*\(\s*[rRfFbBuU]{0,2}[\"']REFUSING\b")''',
             '    )',
             "test_a_refusing_print_is_a_refusal",
             "a REFUSING print not recognized"),
            (r'''[rRfFbBuU]{0,2}[\"']REFUSING''', r'''f?[\"']REFUSING''',
             "test_a_refusing_print_with_any_prefix_is_a_refusal",
             "only the f prefix read"),
            ("is_refusal(statement(src, n))", "is_refusal(src[n - 1])",
             "test_a_multi_line_refusal_is_seen_by_its_first_line",
             "only the first line of a statement read"),
            ("    except (tokenize.TokenError, SyntaxError):\n",
             "    except ZeroDivisionError:\n",
             "test_source_the_tokenizer_cannot_read_is_judged_by_its_line",
             "unreadable source raises"),
            ("            (refusals if is_refusal(statement(src, n)) else others).append(row)\n",
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


def test_branch_measurement_can_fail():
    """F194: line coverage alone, in `.coveragerc` or on CI's diff-cover
    line, lets the untaken one-line raise pass."""
    from injection import Mutation, assert_can_fail, run_pytest
    e2e = f"{THIS}::test_a_refusal_whose_branch_no_test_takes_fails"
    config = f"{THIS}::test_ci_measures_branches"
    for path, old, new, label in (
            (ROOT / ".coveragerc", "branch = True\n", "branch = False\n",
             "coverage by line in .coveragerc"),
            (ROOT / ".github" / "workflows" / "ci.yml",
             " --branch-coverage", "", "diff-cover without --branch-coverage")):
        for test in (e2e, config):
            assert_can_fail([Mutation(path, old, new, expect_occurrences=1)],
                            lambda test=test: run_pytest(test, ROOT), label)
