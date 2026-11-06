"""F177 change b: `scripts/select_proofs.py` selects a test file's red
proofs when the test or a file it names changed (D17: shared machinery
selects only the tests that name it), a 5% rotating sample, and local
tests by the same rules plus the repository guards.
Each rule is proven red."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
THIS = Path(__file__).relative_to(ROOT).as_posix()
SRC = ROOT / "scripts" / "select_proofs.py"
sys.path.insert(0, str(ROOT / "scripts"))

import select_proofs as sp  # noqa: E402

SOURCES = {
    "experiments/src/test_a.py": 'SRC = PHASE2 / "f157_spectra_algorithms.py"\n',
    "experiments/src/test_b.py": "import outcome_record as orec\n",
    "experiments/src/test_c.py": "x = 1\n",
}
TESTS = sorted(SOURCES)


def pick(changed):
    return sp.select(set(changed), TESTS, read=SOURCES.__getitem__)


def test_a_changed_test_file_is_selected():
    assert pick(["experiments/src/test_c.py"]) == ["experiments/src/test_c.py"]


def test_a_named_file_selects_the_tests_that_name_it():
    assert pick(["experiments/phase2/src/f157_spectra_algorithms.py"]) == [
        "experiments/src/test_a.py"]
    assert pick(["experiments/phase2/src/outcome_record.py"]) == [
        "experiments/src/test_b.py"]


def test_shared_machinery_selects_only_the_tests_that_name_it():
    # D17 option 1 (c): it selected every file before, about 4 hours here.
    sources = dict(SOURCES)
    sources["experiments/src/test_injection.py"] = "import injection\n"
    tests = sorted(sources)
    assert sp.select({"experiments/src/injection.py"}, tests,
                     read=sources.__getitem__) == [
        "experiments/src/test_injection.py"]
    assert pick(["conftest.py"]) == []


def _proof_sources(n=45):
    return {f"experiments/src/test_{i:02d}.py":
            ("assert_can_fail(x)\n" if i % 3 else "x = 1\n")
            for i in range(n)}


def test_the_sample_is_a_rotating_twentieth_of_the_proof_files():
    src = _proof_sources()
    tests = sorted(src)
    proofs = [t for t in tests if "assert_can_fail" in src[t]]
    slices = [sp.sample(tests, s, read=src.__getitem__) for s in range(20)]
    assert sorted(t for s in slices for t in s) == proofs   # each once
    assert slices[0] == proofs[0::20] and slices[3] == proofs[3::20]
    assert sp.sample(tests, 23, read=src.__getitem__) == slices[3]
    assert all("assert_can_fail" in src[t] for s in slices for t in s)


def test_local_tests_add_the_guards_and_the_directory_rule():
    src = dict(SOURCES)
    src["experiments/src/test_us_english.py"] = "x = 1\n"
    src["experiments/src/test_evidence_immutability.py"] = "x = 1\n"
    src["experiments/src/test_learning.py"] = 'DOCS = ROOT / "docs" / "learning"\n'
    src["experiments/src/test_other.py"] = 'P = "docs/phase2/x.md"\n'
    tests = sorted(src)
    got = sp.select_tests({"docs/learning/a.md"}, tests, read=src.__getitem__)
    assert got == ["experiments/src/test_evidence_immutability.py",
                   "experiments/src/test_learning.py",
                   "experiments/src/test_us_english.py"]
    got = sp.select_tests({"docs/phase2/y.md"}, tests, read=src.__getitem__)
    assert "experiments/src/test_other.py" in got
    assert not sp.names_directory("x", "README.md")


def test_a_shallow_folder_or_a_python_file_selects_no_directory_tests():
    # Almost every test names `docs` or `experiments/src`.
    src = 'D = ROOT / "docs"\nS = "experiments/src"\n'
    assert not sp.names_directory(src, "docs/SPRINT_CHECKLIST.md")
    assert not sp.names_directory(src, "experiments/src/test_x.py")
    assert sp.names_directory('S = "experiments/src"\n',
                              "experiments/src/notes.md")


def test_an_unreadable_sprint_number_is_refused(tmp_path):
    import pytest
    bad = tmp_path / "s.json"
    for text in ("{not json", '{"current_sprint": {}}',
                 '{"current_sprint": {"number": "31"}}',
                 '{"current_sprint": {"number": true}}'):
        bad.write_text(text, encoding="utf-8")
        with pytest.raises(SystemExit, match="sprint number"):
            sp.sprint_number(bad)
    bad.write_text('{"current_sprint": {"number": 31}}', encoding="utf-8")
    assert sp.sprint_number(bad) == 31


def test_tests_mode_refuses_the_proof_flags(monkeypatch):
    # Nothing may run if the refusal is gone: a real run here selects
    # this file, whose test calls main again, without end.
    def no_run(*a, **k):
        raise AssertionError("main ran tests instead of refusing")
    monkeypatch.setattr(sp, "changed_files", no_run)
    monkeypatch.setattr(sp.subprocess, "run", no_run)
    assert sp.main(["--tests", "--run"]) == 2
    assert sp.main(["--tests", "--sample"]) == 2


def test_an_unrelated_change_selects_nothing():
    assert pick(["docs/phase2/F95_SCHEDULE4.md"]) == []
    assert pick(["experiments/phase2/src/f95_other.py"]) == []


def test_a_module_stem_matches_only_as_a_name():
    assert sp.names_file("import data as dmod\n", "experiments/src/data.py")
    assert not sp.names_file("metadata = 1\n", "experiments/src/data.py")


def test_the_rules_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest

    def test(name):
        return lambda: run_pytest(f"{THIS}::{name}", ROOT)
    assert_can_fail([Mutation(SRC, "        if t in changed:\n",
                              "        if False:\n", expect_occurrences=1)],
                    test("test_a_changed_test_file_is_selected"),
                    "a changed test file left out")
    assert_can_fail([Mutation(SRC, "    if name in source:\n",
                              "    if False:\n", expect_occurrences=1)],
                    test("test_a_named_file_selects_the_tests_that_name_it"),
                    "a mutated file named by path left out")
    for old, new, name, label in (
            ("        if any(names_file(src, c) for c in changed if c != t):\n",
             "        if any(names_file(src, c) for c in changed if c != t) "
             "or 'conftest' in str(changed):\n",
             "test_shared_machinery_selects_only_the_tests_that_name_it",
             "a shared-machinery change selecting every file"),
            ("            if i % SAMPLE_CYCLE == sprint % SAMPLE_CYCLE]\n",
             "            if i % SAMPLE_CYCLE == 0]\n",
             "test_the_sample_is_a_rotating_twentieth_of_the_proof_files",
             "a sample that does not rotate"),
            ('    proofs = [t for t in sorted(tests) if "assert_can_fail" in read(t)]\n',
             "    proofs = sorted(tests)\n",
             "test_the_sample_is_a_rotating_twentieth_of_the_proof_files",
             "a sample that counts files with no proofs"),
            ("    chosen |= {t for t in ALWAYS if t in tests}\n", "",
             "test_local_tests_add_the_guards_and_the_directory_rule",
             "the repository guards left out of a local run"),
            ("        if t not in chosen and any(names_directory(read(t), c)\n",
             "        if False and any(names_directory(read(t), c)\n",
             "test_local_tests_add_the_guards_and_the_directory_rule",
             "a guard over a changed directory left out"),
            ('    if Path(changed).suffix == ".py" or len(parts) < 2:\n',
             "    if not parts:\n",
             "test_a_shallow_folder_or_a_python_file_selects_no_directory_tests",
             "a shallow folder or a Python file selecting by directory"),
            ("    if not isinstance(n, int) or isinstance(n, bool):\n",
             "    if False:\n",
             "test_an_unreadable_sprint_number_is_refused",
             "a sprint number that is not an integer used"),
            ("    if args.tests and (args.run or args.sample):\n",
             "    if False:\n",
             "test_tests_mode_refuses_the_proof_flags",
             "--tests with --run read as a proof run")):
        assert_can_fail([Mutation(SRC, old, new, expect_occurrences=1)],
                        test(name), label)


# Sprint 31 D16 option 1: each changed refusal has a test and a proof.

def test_a_failed_git_command_is_refused():
    import pytest
    with pytest.raises(SystemExit, match="git no-such-subcommand failed"):
        sp.git("no-such-subcommand")


def test_the_git_refusal_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    assert_can_fail([Mutation(SRC, "    if out.returncode != 0:\n",
                              "    if False:\n", expect_occurrences=1)],
                    lambda: run_pytest(
                        f"{THIS}::test_a_failed_git_command_is_refused", ROOT),
                    "a failed git command read as no changes")
