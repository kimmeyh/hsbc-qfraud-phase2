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
- any line naming `eqc_submit.DIRAC_3` or `eqc_submit.DIRAC_3S` carries that
  marker.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PHASE2_SRC = ROOT / "experiments" / "phase2" / "src"
RUNNER = PHASE2_SRC / "run_dirac3s_verify.py"
MARK = "# device named:"
NAMED = re.compile(r"eqc_submit\.DIRAC_3S?\b")


def problems(text: str) -> list[str]:
    """What breaks the rule in one module's source text."""
    out = []
    lines = text.splitlines()
    if "metered_fit(" in text and "eqc_submit.device(" not in text:
        out.append("calls metered_fit outside eqc_submit.device(): the fit "
                   "would go to Dirac-3")
    for i, line in enumerate(lines, 1):
        if NAMED.search(line) and MARK not in line:
            out.append(f"line {i} names a device without '{MARK}': "
                       f"{line.strip()}")
    if "eqc_submit.device(" in text and "eqc_submit.PHASE2_DEVICE" not in text \
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
    ok_named = ("D = eqc_submit.DIRAC_3  # device named: Dirac-3 contrast\n"
                "with eqc_submit.device(D):\n    metered_fit(a)\n")
    assert problems(ok_default) == []
    assert problems(ok_named) == []
    assert problems("eqc_submit.metered_fit(a, b)\n")   # outside device()
    assert problems("D = eqc_submit.DIRAC_3\n"
                    "with eqc_submit.device(D):\n    metered_fit(a)\n")
    assert problems("with eqc_submit.device('dirac-3'):\n    metered_fit(a)\n")


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
