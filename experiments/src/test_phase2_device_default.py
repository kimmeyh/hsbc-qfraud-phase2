"""Phase 2 fits go to Dirac-3S unless a runner names its device and says why.

Team lead, Sprint 26 Decision 11 (2026-10-16), after F142: Dirac-3S is the
default device for every future Dirac run. The shared default in
`eqc_submit` stays Dirac-3, because a fit outside `eqc_submit.device()`
is how Phase 1's runners reach Dirac-3 (CLAUDE.md, Phase 1 boundary rule 4).
So the default lives where future runs are written: every module under
`experiments/phase2/src/` that sends a fit.

The rule, per module:
- a module that calls `metered_fit` also calls `eqc_submit.device(`, because
  a fit outside it silently goes to Dirac-3;
- a module that calls `eqc_submit.device(` uses `eqc_submit.PHASE2_DEVICE`,
  or names the device on a line marked `# device named:` with its reason;
- any line naming `eqc_submit.DIRAC_3S` carries that marker;
- no module names `eqc_submit.DIRAC_3`, or passes `'dirac-3'` to
  `eqc_submit.device(`, marker or not. Team lead, Sprint 31 D5
  (2026-11-04): "this and all future runs will be on the Dirace-3S [sic]"
  (F181, Sprint 32 Task A). A Dirac-3 contrast run would need that rule
  changed first.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from source_scan import code_text  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
PHASE2_SRC = ROOT / "experiments" / "phase2" / "src"
RUNNER = PHASE2_SRC / "run_dirac3s_verify.py"
MARK = "# device named:"
NAMED = re.compile(r"eqc_submit\.DIRAC_3S?\b")
# Anywhere in the code, not only inside eqc_submit.device(: a constant held
# in a variable, a keyword argument and a `from` import all reach the device
# (PR #116 review). Strings stay in `code_text`, so a literal is seen.
# One form is data, not a device: a record's `"device": "dirac-3"` label
# for a Dirac-3 history row (run_dirac3s_units.dirac3_history).
DIRAC3 = re.compile(r"\bDIRAC_3\b(?!S)"
                    r"|(?<![\"']device[\"']: )['\"]dirac-3['\"]")


def problems(text: str) -> list[str]:
    """What breaks the rule in one module's source text. Calls are matched
    in the code alone (`source_scan.code_text`), so a docstring or comment
    that names a call is not read as one (Sprint 28 IMP-2). The marker is a
    comment, so it is looked for in the raw lines."""
    out = []
    lines = text.splitlines()
    code = code_text(text)
    if "metered_fit(" in code and "eqc_submit.device(" not in code:
        out.append("calls metered_fit outside eqc_submit.device(): the fit "
                   "would go to Dirac-3")
    for i, (line, raw) in enumerate(zip(code.splitlines(), lines), 1):
        if DIRAC3.search(line):
            out.append(f"line {i} names Dirac-3; every Phase 2 run is on "
                       f"Dirac-3S (Sprint 31 D5): {raw.strip()}")
        elif NAMED.search(line) and MARK not in raw:
            out.append(f"line {i} names a device without '{MARK}': "
                       f"{raw.strip()}")
    if "eqc_submit.device(" in code and "eqc_submit.PHASE2_DEVICE" not in code \
            and not any(MARK in line for line in lines):
        out.append("calls eqc_submit.device( with neither PHASE2_DEVICE nor "
                   f"a '{MARK}' line")
    return out


def test_phase2_default_is_dirac3s():
    import eqc_submit
    assert eqc_submit.PHASE2_DEVICE == eqc_submit.DIRAC_3S == "dirac-3s"


def test_every_phase2_module_follows_the_default():
    found = {p.name: problems(p.read_text(encoding="utf-8"))
             for p in sorted(PHASE2_SRC.glob("*.py"))}
    bad = {k: v for k, v in found.items() if v}
    assert not bad, bad


def test_the_rule_reads_each_shape():
    ok_default = ("with eqc_submit.device(eqc_submit.PHASE2_DEVICE):\n"
                  "    eqc_submit.metered_fit(a, b)\n")
    ok_named = ("D = eqc_submit.DIRAC_3S  # device named: F142 verifies it\n"
                "with eqc_submit.device(D):\n    metered_fit(a)\n")
    assert problems(ok_default) == []
    assert problems(ok_named) == []
    assert problems("eqc_submit.metered_fit(a, b)\n")   # outside device()
    assert problems("D = eqc_submit.DIRAC_3\n"
                    "with eqc_submit.device(D):\n    metered_fit(a)\n")
    assert problems("with eqc_submit.device('dirac-3'):\n    metered_fit(a)\n")


def test_dirac3_is_refused_even_with_its_reason():
    """F181: the marker no longer admits Dirac-3; one test per form."""
    named = ("D = eqc_submit.DIRAC_3  # device named: Dirac-3 contrast\n"
             "with eqc_submit.device(D):\n    metered_fit(a)\n")
    literal = ("with eqc_submit.device('dirac-3'):  # device named: x\n"
               "    metered_fit(a)\n")
    assert any("names Dirac-3" in p for p in problems(named))
    assert any("names Dirac-3" in p for p in problems(literal))
    # Dirac-3S under either spelling is not Dirac-3.
    assert problems("from eqc_submit import DIRAC_3S  # device named: r\n") == []
    assert problems("D = eqc_submit.DIRAC_3S  # device named: r\n") == []
    assert problems("with eqc_submit.device('dirac-3s'):  # device named: r\n"
                    "    metered_fit(a)\n") == []


def test_dirac3_held_imported_or_by_keyword_is_refused():
    """PR #116 review: each shape passed the first F181 rule."""
    held = ('D = "dirac-3"  # device named: contrast\n'
            "with eqc_submit.device(D):\n    metered_fit(a)\n")
    keyword = ('with eqc_submit.device(device_type="dirac-3"):'
               "  # device named: x\n    metered_fit(a)\n")
    imported = ("from eqc_submit import DIRAC_3  # device named: x\n"
                "with eqc_submit.device(DIRAC_3):\n    metered_fit(a)\n")
    for src in (held, keyword, imported):
        assert any("names Dirac-3" in p for p in problems(src)), src


def test_a_history_records_device_label_is_not_a_device():
    assert problems('row = {"file": f, "device": "dirac-3"}\n') == []
    # The label form only: the same string anywhere else is refused.
    assert problems('row = {"file": f, "dev": "dirac-3"}\n')


def test_the_history_label_exclusion_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    here = ROOT / "experiments" / "src" / "test_phase2_device_default.py"
    assert_can_fail([Mutation(here, "(?<![\\\"']device[\\\"']: )", "",
                              expect_occurrences=1)],
                    lambda: run_pytest(
                        "experiments/src/test_phase2_device_default.py::"
                        "test_a_history_records_device_label_is_not_a_device",
                        ROOT),
                    "a history label read as a device")


def test_the_dirac3_refusal_can_fail():
    """Each form of the F181 refusal, removed, turns BOTH its tests red:
    one mutation per form (test_no_duplicate_proofs.py), and the run
    passes if either test still passes."""
    from injection import Mutation, assert_can_fail, run_pytest
    here = ROOT / "experiments" / "src" / "test_phase2_device_default.py"
    base = "experiments/src/test_phase2_device_default.py::"

    def either_passes() -> bool:
        return (run_pytest(base + "test_dirac3_is_refused_even_with_its_"
                           "reason", ROOT)
                or run_pytest(base + "test_dirac3_held_imported_or_by_"
                              "keyword_is_refused", ROOT))
    for old, new, label in (
            ('r"\\bDIRAC_3\\b(?!S)"', 'r"NO_MATCH_A"',
             "DIRAC_3, named or imported, admitted"),
            ("['\\\"]dirac-3['\\\"]\")", 'NO_MATCH_B")',
             "'dirac-3', passed, held or by keyword, admitted")):
        assert_can_fail([Mutation(here, old, new, expect_occurrences=1)],
                        either_passes, label)


def test_prose_naming_a_call_is_not_a_call():
    # The device_store.py docstring that turned CI red (39f9943).
    doc = ('"""Through `eqc_submit.device(wrap=...)` and `metered_fit(`."""\n'
           "# eqc_submit.DIRAC_3 is named here only in a comment\n"
           "x = 1\n")
    assert problems(doc) == []
    assert code_text(doc).count("\n") == doc.count("\n")
    assert "x = 1" in code_text(doc)


def test_a_call_after_prose_is_still_found():
    src = ('"""Only prose: eqc_submit.device(."""\n'
           "s = 'eqc_submit.device( in a value string'\n"
           "with eqc_submit.device(D):\n    metered_fit(a)\n")
    assert problems(src)
    assert "eqc_submit.device(" in code_text(src).splitlines()[2]


def test_a_form_feed_does_not_shift_the_blanking():
    src = ("x = 1\n\x0c\ndef f():\n" + '    """doc"""\n'
           + "    eqc_submit.device(D)\n")
    code = code_text(src)
    assert "eqc_submit.device(D)" in code and "doc" not in code
    assert "def f():" in code


def test_the_line_split_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    assert_can_fail([Mutation(ROOT / "experiments" / "src" / "source_scan.py",
                              "    lines = io.StringIO(src).readlines()\n",
                              "    lines = src.splitlines(keepends=True)\n",
                              expect_occurrences=1)],
                    lambda: run_pytest(
                        "experiments/src/test_phase2_device_default.py::"
                        "test_a_form_feed_does_not_shift_the_blanking", ROOT),
                    "lines split at a form feed")


def test_the_prose_blanking_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    assert_can_fail([Mutation(ROOT / "experiments" / "src" / "source_scan.py",
                              "            spans.append((tok.start, tok.end))\n"
                              "        elif",
                              "            pass\n        elif",
                              expect_occurrences=1)],
                    lambda: run_pytest(
                        "experiments/src/test_phase2_device_default.py::"
                        "test_prose_naming_a_call_is_not_a_call", ROOT),
                    "comments kept as code")
    assert_can_fail([Mutation(ROOT / "experiments" / "src" / "source_scan.py",
                              "elif tok.type == tokenize.STRING and prev in",
                              "elif False and prev in", expect_occurrences=1)],
                    lambda: run_pytest(
                        "experiments/src/test_phase2_device_default.py::"
                        "test_prose_naming_a_call_is_not_a_call", ROOT),
                    "docstrings kept as code")


def test_the_module_check_can_fail():
    """Removing the runner's marker, or its device() block, turns it red."""
    from injection import Mutation, assert_can_fail

    def run() -> bool:
        return problems(RUNNER.read_text(encoding="utf-8")) == []

    assert_can_fail([Mutation(RUNNER, "  # device named: F142 verifies "
                              "Dirac-3S itself", "", expect_occurrences=1)],
                    run, "a named device without its reason")
    assert_can_fail([Mutation(RUNNER, "eqc_submit.device(",
                              "contextlib.nullcontext(", expect_occurrences=1)],
                    run, "a metered fit outside device()")
