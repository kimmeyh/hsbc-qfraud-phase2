"""F153: the ridge rule, the floor, the quote and the guide's resolution check.

Sprint 28 Task C (#50). Synthetic inputs; the run builds ULB pools and is
not run here.
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "src"))

import device_resolution as dr  # noqa: E402
import exp3_controls as ec  # noqa: E402
import f153_exp3_design as fd  # noqa: E402


def test_the_entry_constants():
    assert fd.SWEEP == (2.0, 0.2, 0.02, 0.002)
    assert fd.DATA_SHARE_MIN == 0.10 and fd.GAP_MIN == 0.01
    assert fd.SCIP_CAP_S == 300.0


def test_the_floor_bounds_every_objective():
    rng = np.random.default_rng(0)
    H = np.where(rng.random((12, 200)) < 0.5, 1.0, -1.0)
    y = np.where(rng.random(200) < 0.5, 1.0, -1.0)
    for lm in fd.SWEEP:
        J, C = ec.problem(H, y, lm)
        g = ec.greedy(J, C, 4)
        assert g["objective"] >= fd.floor(lm, 4) - 1e-12
        w = ec.solve_on_support(J, C, g["support"])
        assert fd.data_term(J, C, w, lm) >= -1e-12


def test_ridge_rule_takes_the_largest_qualifying_weight():
    rows = [{"lam_mult": lm, "data_share": s}
            for lm, s in ((2.0, 0.01), (0.2, 0.12), (0.02, 0.5), (0.002, 0.9))
            for _ in range(6)]
    assert fd.choose_ridge(rows) == {"lam_mult": 0.2, "rule_met": True}


def test_ridge_rule_falls_back_to_the_smallest_labeled():
    rows = [{"lam_mult": lm, "data_share": 0.01} for lm in fd.SWEEP for _ in range(6)]
    assert fd.choose_ridge(rows) == {"lam_mult": 0.002, "rule_met": False}


def test_one_failing_instance_disqualifies_a_weight():
    rows = [{"lam_mult": 0.2, "data_share": 0.5}] * 5 + [{"lam_mult": 0.2, "data_share": 0.05}]
    rows += [{"lam_mult": 0.02, "data_share": 0.5}] * 6
    assert fd.choose_ridge(rows)["lam_mult"] == 0.02


def test_the_quote_is_a_bracket_from_the_two_probes():
    q = fd.quote()
    assert q["dirac3_total_s"] == 193
    assert (q["dirac3s_low_s"], q["dirac3s_high_s"]) == (77, 251)
    assert "inferred" in q["label"]


def _brute(J, C):
    t = np.r_[J[np.triu_indices(J.shape[0])], C]
    t = t[t != 0]
    step = np.abs(t).max() / 200
    pairs = list(itertools.combinations(t, 2))
    return (sum(abs(a - b) >= step for a, b in pairs), sum(a != b for a, b in pairs))


def test_guide_check_counts_pairs_as_brute_force_does():
    rng = np.random.default_rng(3)
    J = rng.normal(size=(7, 7)); J = J + J.T
    C = rng.normal(size=7)
    r = dr.resolution_check_guide(J, C)
    assert (r["resolved_pairs"], r["distinct_pairs"]) == _brute(J, C)


def test_guide_check_fails_on_ratio_and_on_close_pairs():
    J = np.array([[1000.0, 1.0], [1.0, 1000.0]])
    C = np.array([500.0, 500.5])
    r = dr.resolution_check_guide(J, C)
    assert r["max_min_ratio"] == pytest.approx(1000.0) and not r["ratio_ok"]
    assert r["resolved_pair_share"] < 1.0 and not r["pass"]


def test_guide_check_fails_on_the_ratio_alone():
    # One distinct value: every pair (none) is resolved, so only the ratio
    # part can fail. Dropping the ratio part from `pass` turns this green.
    r = dr.resolution_check_guide(np.array([[1000.0]]), np.array([1.0]))
    assert not r["ratio_ok"] and r["resolved_pair_share"] == 1.0
    assert not r["pass"]


def test_guide_check_fails_on_close_pairs_alone():
    # The ratio is fine; the coefficients sit closer than the step. This is
    # the real F153 case (ratio about 2, share well under 1).
    J = np.array([[10.0, 10.02], [10.02, 10.0]])
    C = np.array([9.99, 10.01])
    r = dr.resolution_check_guide(J, C)
    assert r["ratio_ok"] and r["resolved_pair_share"] < 1.0
    assert not r["pass"]


def _chosen(greedy_gap, best_gap, gate=True, guide=True):
    fl = -0.5
    return {"floor": fl, "gap_best_to_floor": best_gap,
            "methods": {"greedy": {"objective": fl + greedy_gap}},
            "f104_gate": {"pass": gate}, "guide_check": {"pass": guide}}


def test_design_fails_when_every_greedy_gap_is_below_the_minimum():
    rows = [_chosen(0.002, 0.002) for _ in range(6)]
    assert fd.design_fails(rows)


def test_design_holds_with_one_gap_and_both_checks_passing():
    rows = [_chosen(0.002, 0.002) for _ in range(5)] + [_chosen(0.05, 0.05)]
    assert not fd.design_fails(rows)


def test_design_fails_when_every_instance_fails_both_checks():
    rows = [_chosen(0.05, 0.05, gate=False, guide=False) for _ in range(6)]
    assert fd.design_fails(rows)
    # One instance passing one check is enough to keep the design.
    rows[3] = _chosen(0.05, 0.05, gate=False, guide=True)
    assert not fd.design_fails(rows)


def test_design_reads_the_greedy_gap_not_the_best_found():
    # The entry: "the gap between greedy and the floor". Greedy leaves room
    # (>= 0.01) although the best found does not: the design holds.
    rows = [_chosen(0.02, 0.005) for _ in range(6)]
    assert not fd.design_fails(rows)


def test_design_verdict_refuses_no_rows():
    with pytest.raises(ValueError, match="empty"):
        fd.design_fails([])


def test_guide_check_passes_a_well_spread_problem():
    J = np.array([[10.0, 2.0], [2.0, 8.0]])
    C = np.array([-4.0, 6.0])
    assert dr.resolution_check_guide(J, C)["pass"]


def test_f104_gate_is_unchanged_by_the_new_check():
    J = np.array([[10.0, 2.0], [2.0, 8.0]])
    C = np.array([-4.0, 6.0])
    g = dr.resolution_gate(J, C)
    assert set(g) == {"off_diagonal_spread_over_resolvable",
                      "linear_spread_over_resolvable", "resolvable_difference",
                      "n_variables", "pass"}
