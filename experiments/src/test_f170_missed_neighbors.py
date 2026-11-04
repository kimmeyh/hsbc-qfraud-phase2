"""F170 (Sprint 30 Task G, #81): the neighbor share, the test's direction
and the reading's terms, each proven red. Synthetic rows only.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
PHASE2 = ROOT / "experiments" / "phase2" / "src"
THIS = Path(__file__).relative_to(ROOT).as_posix()
sys.path.insert(0, str(PHASE2))

import f170_missed_neighbors as f170  # noqa: E402


def test_the_share_counts_legitimate_neighbors():
    # Ten legitimate rows near 0, ten frauds near 10.
    Xtr = np.r_[np.zeros((10, 2)) + np.arange(10)[:, None] * 0.01,
                np.full((10, 2), 10.0) + np.arange(10)[:, None] * 0.01]
    ytr = np.r_[np.zeros(10, int), np.ones(10, int)]
    s = f170.legit_share(Xtr, ytr, np.array([[0.0, 0.0], [10.0, 10.0]]))
    assert list(s) == [1.0, 0.0]


def test_the_direction_is_higher_only_when_missed_sit_among_more_legit():
    rng = np.random.default_rng(0)
    hi, lo = rng.uniform(0.7, 1.0, 60), rng.uniform(0.0, 0.4, 60)
    assert f170.compare(hi, lo)["direction"] == "higher"
    assert f170.compare(lo, hi)["direction"] == "lower"
    same = rng.uniform(0, 1, 60)
    assert f170.compare(same, rng.uniform(0, 1, 60))["direction"] == \
        "no difference"
    assert f170.compare([], lo)["direction"] == "no test"


def _res(direction, median):
    return {"primary": {"direction": direction, "missed_median": median}}


def test_the_reading_needs_both_terms():
    fired = {"fires": True}
    assert "information limit" in f170.reading(fired, _res("higher", 0.9))
    assert "weakness" in f170.reading(fired, _res("higher", 0.4))
    assert "weakness" in f170.reading(fired, _res("no difference", 0.9))


def test_no_reading_without_the_simulator_check():
    assert "no ULB reading" in f170.reading({"fires": False}, None)


def test_the_reading_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    src = PHASE2 / "f170_missed_neighbors.py"

    def test(name):
        return lambda: run_pytest(f"{THIS}::{name}", ROOT)
    assert_can_fail([Mutation(src, '    if p["direction"] == "higher" and '
                              'p["missed_median"] > 0.5:\n',
                              '    if p["direction"] == "higher":\n',
                              expect_occurrences=1)],
                    test("test_the_reading_needs_both_terms"),
                    "the majority-legitimate term dropped")
    assert_can_fail([Mutation(src, '    if p["direction"] == "higher" and '
                              'p["missed_median"] > 0.5:\n',
                              '    if p["missed_median"] > 0.5:\n',
                              expect_occurrences=1)],
                    test("test_the_reading_needs_both_terms"),
                    "the direction term dropped")
    assert_can_fail([Mutation(src, "    if not check[\"fires\"]:\n",
                              "    if False:\n", expect_occurrences=1)],
                    test("test_no_reading_without_the_simulator_check"),
                    "a ULB reading made without the check")
    assert_can_fail([Mutation(src, "    return (np.asarray(ytr)[idx] == 0)"
                              ".mean(axis=1)\n",
                              "    return (np.asarray(ytr)[idx] == 1)"
                              ".mean(axis=1)\n", expect_occurrences=1)],
                    test("test_the_share_counts_legitimate_neighbors"),
                    "fraud neighbors counted as legitimate")
