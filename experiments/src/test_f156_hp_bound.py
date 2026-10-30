"""F156 (Sprint 29 Task D, #67): the Henze-Penrose bound and its pass rule.

One test per term of the rule, each with only that term failing, each
proven red (Sprint 28 IMP-5).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
PHASE2 = ROOT / "experiments" / "phase2" / "src"
THIS = Path(__file__).relative_to(ROOT).as_posix()
sys.path.insert(0, str(PHASE2))

import f156_hp_bound as hp  # noqa: E402


def _brute_mst_weight(X):
    from scipy.sparse.csgraph import minimum_spanning_tree
    from scipy.spatial.distance import cdist
    return float(minimum_spanning_tree(cdist(X, X)).sum())


def test_the_tree_is_the_exact_euclidean_mst():
    X = np.random.default_rng(3).normal(size=(400, 3))
    e = hp.emst_edges(X)
    assert len(e) == 399
    w = float(np.linalg.norm(X[e[:, 0]] - X[e[:, 1]], axis=1).sum())
    assert w == pytest.approx(_brute_mst_weight(X), rel=1e-12)


def test_separated_classes_bound_the_error_near_zero():
    rng = np.random.default_rng(4)
    X = np.vstack([rng.normal(size=(300, 3)), rng.normal(size=(30, 3)) + 50])
    y = np.r_[np.zeros(300), np.ones(30)]
    b = hp.hp_bound(X, y)
    assert b["cross_edges"] == 1 and b["upper"] < 0.01 and b["lower"] >= 0


def test_identical_classes_at_equal_priors_bound_the_error_at_one_half():
    # The Bayes error of two identical classes at p = q is 0.5.
    rng = np.random.default_rng(5)
    X = rng.normal(size=(4000, 3))
    y = rng.integers(0, 2, size=4000)
    b = hp.hp_bound(X, y)
    assert abs(b["D"]) < 0.06
    assert b["lower"] > 0.37 and b["upper"] > 0.47


def test_the_subsample_keeps_the_class_share():
    y = np.r_[np.zeros(9900, int), np.ones(100, int)]
    idx = hp.stratified(y, 2000, 42)
    assert len(idx) == 2000 and y[idx].sum() == 20


def test_term_1_alone_fails_when_the_interval_misses():
    t = hp.terms({"lower": 0.0070, "upper": 0.0075, "width": 0.0005}, 0.0061)
    assert t["narrow"] and not t["contains"] and not t["pass"]


def test_term_2_alone_fails_when_the_interval_is_wide():
    t = hp.terms({"lower": 0.0, "upper": 0.0083, "width": 0.0083}, 0.0061)
    assert t["contains"] and not t["narrow"] and not t["pass"]
    assert t["width_cap"] == pytest.approx(2 * 0.10 * 0.0061)


def test_both_terms_pass_a_tight_containing_interval():
    t = hp.terms({"lower": 0.0058, "upper": 0.0066, "width": 0.0008}, 0.0061)
    assert t["pass"]


def test_four_of_five_decides():
    def row(ok):
        return {"arms": {"none": {"contains": ok, "narrow": ok, "pass": ok}}}
    assert hp.summarize([row(True)] * 4 + [row(False)])["passes"]
    assert not hp.summarize([row(True)] * 3 + [row(False)] * 2)["passes"]


def _fails(old, new, node, label):
    from injection import Mutation, assert_can_fail, run_pytest
    assert_can_fail([Mutation(PHASE2 / "f156_hp_bound.py", old, new,
                              expect_occurrences=1)],
                    lambda: run_pytest(f"{THIS}::{node}", ROOT), label)


def test_term_1_can_fail():
    _fails("    contains = bool(bound[\"lower\"] <= bayes <= bound[\"upper\"])\n",
           "    contains = True\n",
           "test_term_1_alone_fails_when_the_interval_misses",
           "containment not checked")


def test_term_2_can_fail():
    _fails("    narrow = bool(bound[\"width\"] <= cap)\n",
           "    narrow = True\n",
           "test_term_2_alone_fails_when_the_interval_is_wide",
           "width not checked")


def test_the_exact_tree_can_fail():
    _fails("    t = minimum_spanning_tree(g).tocoo()\n",
           "    t = g.tocoo()\n",
           "test_the_tree_is_the_exact_euclidean_mst", "not a spanning tree")
