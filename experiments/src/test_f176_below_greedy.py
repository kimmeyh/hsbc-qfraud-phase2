"""F176 (Sprint 30 Task E, #79): "below greedy" can fire, and is read right.

Small seeded instances (10 learners, m = 3), solved exactly by
enumeration; nothing here reads IEEE-CIS or calls SCIP.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
PHASE2 = ROOT / "experiments" / "phase2" / "src"
THIS = Path(__file__).relative_to(ROOT).as_posix()
sys.path.insert(0, str(PHASE2))

import exp3_controls as ec  # noqa: E402
import f176_below_greedy as f176  # noqa: E402


def _small(seed: int):
    rng = np.random.default_rng(5000 + seed)
    y = np.where(rng.random(200) < 0.1, 1, -1)
    H = rng.choice([-1.0, 1.0], size=(10, 200))
    return H, y


def test_the_swap_search_gets_below_greedy_where_greedy_is_not_optimal(
        monkeypatch):
    monkeypatch.setattr(f176, "CHECK_N", 10)
    monkeypatch.setattr(f176, "CHECK_M", 3)
    c = f176.check_instance(*_small(11), 2.0)       # greedy 0.811, exact 0.764
    assert c["greedy_not_optimal"] and c["search_reaches_exact"]
    assert c["swap_search"] < c["greedy"] - f176.TOL


def test_can_fire_needs_a_case_the_search_solves(monkeypatch):
    monkeypatch.setattr(f176, "CHECK_N", 10)
    monkeypatch.setattr(f176, "CHECK_M", 3)
    fires = f176.check_instance(*_small(11), 2.0)
    missed = f176.check_instance(*_small(32), 2.0)  # a local optimum
    assert missed["greedy_not_optimal"] and not missed["search_reaches_exact"]
    assert f176.can_fire({"a": fires, "b": missed})["fires_on"] == ["a"]
    assert f176.can_fire({"b": missed})["can_fire"] is False
    assert f176.can_fire({"b": missed})["search_missed"] == ["b"]


def test_the_reading_and_its_bound():
    res = {"greedy": {"objective": -0.70},
           "swap_search": {"objective": -0.70 - 1e-7},       # within TOL
           "scip": {"objective": None, "dual_bound": -0.88}}
    r = f176.reading(res, -0.70, -0.80)
    assert r["below_greedy"] is False
    assert abs(r["room_bound"] - 0.10) < 1e-12     # floor binds over the dual
    res["swap_search"]["objective"] = -0.71
    r = f176.reading(res, -0.70, -0.80)
    assert r["below_greedy"] is True and r["best_method"] == "swap_search"
    assert abs(r["gap_best_to_greedy"] + 0.01) < 1e-12
    res["scip"]["dual_bound"] = -0.75
    assert abs(f176.reading(res, -0.70, -0.80)["room_bound"] - 0.05) < 1e-12


def test_the_search_never_returns_worse_than_its_start():
    H, y = _small(3)
    J, C = ec.problem(H, y, 2.0)
    g = ec.greedy(J, C, 3)
    assert f176.swap_search(J, C, 3, g["support"])["objective"] <= \
        g["objective"] + 1e-12


def test_the_reading_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    src = PHASE2 / "f176_below_greedy.py"

    def test(name):
        return lambda: run_pytest(f"{THIS}::{name}", ROOT)
    assert_can_fail([Mutation(src, '           "below_greedy": bool(best < '
                              'greedy_obj - TOL)}\n',
                              '           "below_greedy": bool(best < '
                              'greedy_obj)}\n', expect_occurrences=1)],
                    test("test_the_reading_and_its_bound"),
                    "a difference inside the tolerance read as below")
    assert_can_fail([Mutation(src, "            if e < best_e - TOL:\n",
                              "            if False:\n",
                              expect_occurrences=1)],
                    test("test_the_swap_search_gets_below_greedy_where_"
                         "greedy_is_not_optimal"),
                    "a search that never moves")
    assert_can_fail([Mutation(src, "             if c[\"greedy_not_optimal\"] "
                              "and c[\"search_reaches_exact\"]]\n",
                              "             if c[\"greedy_not_optimal\"]]\n",
                              expect_occurrences=1)],
                    test("test_can_fire_needs_a_case_the_search_solves"),
                    "a missed case counted as firing")
