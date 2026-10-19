"""Every Phase 2 script is named by at least one test (Sprint 27 IMP-3).

Sprint 27 shipped two scripts with no test: F112's, found by the code
review, and `f102_downsized_pair.py`, found only at the retrospective.
Sprint 22's `validate_emulator.py` had none either. A script counts as
tested when its module name appears as a word in some `test_*.py` under
`experiments/src/`. That is a floor, not a coverage measure: it catches a
script nobody wrote a test for, which is the failure that happened.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "experiments" / "phase2" / "src"
TESTS = ROOT / "experiments" / "src"


def untested(scripts: Path, tests: Path) -> list[str]:
    corpus = "\n".join(p.read_text(encoding="utf-8")
                       for p in sorted(tests.glob("test_*.py")))
    return sorted(p.stem for p in scripts.glob("*.py")
                  if p.stem != "__init__"
                  and not re.search(rf"\b{re.escape(p.stem)}\b", corpus))


def test_every_phase2_script_is_named_by_a_test():
    assert SCRIPTS.is_dir() and any(SCRIPTS.glob("*.py"))
    missing = untested(SCRIPTS, TESTS)
    assert not missing, (f"{missing} have no test in experiments/src/; "
                         "a new Phase 2 script commits with its test")


def test_the_check_can_fail(tmp_path):
    scripts, tests = tmp_path / "src", tmp_path / "tests"
    scripts.mkdir()
    tests.mkdir()
    (scripts / "f999_new.py").write_text("x = 1\n", encoding="utf-8")
    (scripts / "f998_other.py").write_text("x = 1\n", encoding="utf-8")
    (tests / "test_other.py").write_text("import f998_other\n",
                                         encoding="utf-8")
    assert untested(scripts, tests) == ["f999_new"]
    (tests / "test_new.py").write_text("import f999_new_extra\n",
                                       encoding="utf-8")
    assert untested(scripts, tests) == ["f999_new"]     # a prefix is not a name
    (tests / "test_new.py").write_text("import f999_new\n", encoding="utf-8")
    assert untested(scripts, tests) == []
