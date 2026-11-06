"""F177 change b: `scripts/select_proofs.py` selects a test file's red
proofs when the test, a file it names, or the shared machinery changed.
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


def test_shared_machinery_selects_everything():
    assert pick(["experiments/src/injection.py"]) == TESTS
    assert pick(["conftest.py"]) == TESTS
    assert pick(["pytest.ini"]) == TESTS


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
    assert_can_fail([Mutation(SRC, "        return list(tests)\n",
                              "        return []\n", expect_occurrences=1)],
                    test("test_shared_machinery_selects_everything"),
                    "a change to the shared machinery selecting nothing")
