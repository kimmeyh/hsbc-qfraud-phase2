"""F17 (Sprint 22 Task D): the emulator validation's helpers and summary.

Sprint 27 IMP-3: the script shipped without a test. Known answers for the
cosine and energy-spread helpers, and the recorded summary in
`f17_emulator_validation.json` must follow from its own rows: each budget's
mean cosine and gap, the device mean, and the calibrated budget as the one
with the smallest gap. Reads the result; writes nothing; runs no fit.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))

import validate_emulator as ve      # noqa: E402

SRC = ROOT / "experiments" / "phase2" / "src" / "validate_emulator.py"
DOC = json.loads(ve.OUT.read_text(encoding="utf-8"))


def test_cosine_known_answers():
    assert ve._cos(np.array([1.0, 0.0]), np.array([2.0, 0.0])) == 1.0
    assert ve._cos(np.array([1.0, 0.0]), np.array([0.0, 3.0])) == 0.0
    assert ve._cos(np.zeros(2), np.ones(2)) is None


def test_relative_spread_known_answers():
    assert ve._rel_spread([-4.0, -3.0, -2.0]) == pytest.approx(0.5)
    assert ve._rel_spread([]) is None
    assert ve._rel_spread([0.0, 1.0]) is None


def test_the_spread_check_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    node = ("experiments/src/test_validate_emulator.py"
            "::test_relative_spread_known_answers")
    assert_can_fail([Mutation(SRC, "(e.max() - e.min()) / abs(e.min())",
                              "e.max() / abs(e.min())",
                              expect_occurrences=1)],
                    lambda: run_pytest(node, ROOT),
                    "the spread no longer a range")


@pytest.mark.parametrize("budget", [str(b) for b in ve.BUDGETS])
def test_the_recorded_summary_follows_from_the_rows(budget):
    dev = np.array([r["device"]["weight_cosine"] for r in DOC["rows"]])
    emu = np.array([r["emulated"][budget]["weight_cosine"]
                    for r in DOC["rows"]])
    s = DOC["summary_by_iteration_budget"][budget]
    assert s["mean_cosine"] == round(float(emu.mean()), 4)
    assert s["mean_abs_cosine_gap_vs_device"] == round(
        float(np.mean(np.abs(emu - dev))), 4)
    assert DOC["device_mean_cosine"] == round(float(dev.mean()), 4)


def test_the_calibrated_budget_has_the_smallest_gap():
    s = DOC["summary_by_iteration_budget"]
    gaps = {k: v["mean_abs_cosine_gap_vs_device"] for k, v in s.items()}
    assert DOC["calibrated_budget"] == min(gaps, key=gaps.get)
    assert sorted(s) == sorted(str(b) for b in ve.BUDGETS)
