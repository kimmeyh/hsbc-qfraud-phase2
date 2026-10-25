"""F115: the integer-probe fit is reproduced from the probe's own rows.

Sprint 28 Task I (#55). Reads `experiments/results/integer_probe.json`
(tracked Phase 1 evidence) and writes nothing.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))

import f115_cost_scaling as fcs  # noqa: E402


def test_the_hardware_plans_exponents_come_back_from_the_probe():
    r = fcs.run()
    f = r["two_factor_fit"]
    assert f["vars_exponent"] == pytest.approx(0.75, abs=0.005)
    assert f["levels_exponent"] == pytest.approx(0.52, abs=0.005)
    assert f["r2"] == pytest.approx(0.953, abs=0.001)
    assert f["max_abs_miss"] == pytest.approx(0.45, abs=0.01)


def test_sublinear_in_variables_superlinear_only_when_levels_grow():
    f = fcs.run()["two_factor_fit"]
    assert f["vars_exponent"] < 1 < f["exponent_sum"]


def test_one_point_alone_sets_the_split_between_the_exponents():
    r = fcs.run()
    assert r["points_off_the_line"] == ["probe_deep"]
    # Four proportional points identify only the sum, and it matches.
    assert r["sum_only_fit_on_proportional_points"]["exponent_sum"] == \
        pytest.approx(r["two_factor_fit"]["exponent_sum"], abs=0.01)


def test_a_fit_on_known_exponents_returns_them():
    v = np.array([10, 20, 40, 80, 30.0])
    lv = np.array([40, 80, 160, 320, 500.0])
    s = 0.1 * v ** 0.8 * lv ** 0.4
    f = fcs.log_fit(v, lv, s)
    assert f["vars_exponent"] == pytest.approx(0.8)
    assert f["levels_exponent"] == pytest.approx(0.4)


def test_the_duplicate_small_probe_counts_once():
    calls = json.loads(fcs.PROBE.read_text(encoding="utf-8"))["calls"]
    assert len(calls) == 6
    assert len(fcs.distinct_points(calls)) == 5
