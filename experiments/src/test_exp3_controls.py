"""F94's controls return feasible selections, and SCIP matches enumeration.

Sprint 25 Task F. Synthetic instances only: zero metered, no dataset, nothing
written to an evidence directory. The real-pool run is
`experiments/phase2/src/exp3_controls.py`.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))

import exp3_controls as ec     # noqa: E402


def _instance(n=10, rows=200, seed=0):
    rng = np.random.default_rng(seed)
    H = np.sign(rng.normal(size=(n, rows)))
    y = np.sign(rng.normal(size=rows))
    return ec.problem(H, y)


def _feasible(res, m):
    assert res["support_size"] <= m
    assert res["weight_sum"] == pytest.approx(1.0, abs=1e-9)
    assert res["min_weight"] >= -1e-12


def test_the_plan_constants():
    assert ec.INSTANCES == (("free", 60, 10), ("mid", 136, 25))
    assert ec.EXACT_CHECK == ("free", 20, 4)
    assert ec.SCIP_TIME_LIMIT_S == 600.0


def test_every_control_returns_a_feasible_selection():
    J, C = _instance()
    for res in (ec.exact_enumeration(J, C, 3), ec.greedy(J, C, 3),
                ec.simulated_annealing(J, C, 3, seed=1, iterations=200),
                ec.exact_solver_control(J, C, 3, ec.ScipSolver(), 60.0)):
        _feasible(res, 3)


def test_enumeration_is_never_beaten():
    for seed in range(3):
        J, C = _instance(seed=seed)
        ex = ec.exact_enumeration(J, C, 3)["objective"]
        for res in (ec.greedy(J, C, 3),
                    ec.simulated_annealing(J, C, 3, seed=seed, iterations=200)):
            assert res["objective"] >= ex - 1e-9


def test_greedy_takes_the_best_learner_at_each_step():
    # With m = 1 greedy is one step, so it must find the best single learner,
    # which enumeration certifies. A greedy that picked badly would still be
    # feasible and still no better than enumeration; only this catches it.
    for seed in range(3):
        J, C = _instance(seed=seed)
        assert ec.greedy(J, C, 1)["objective"] == pytest.approx(
            ec.exact_enumeration(J, C, 1)["objective"], rel=1e-9)


def test_scip_matches_enumeration_on_small_instances():
    for seed in range(3):
        J, C = _instance(seed=seed)
        ex = ec.exact_enumeration(J, C, 3)
        sc = ec.exact_solver_control(J, C, 3, ec.ScipSolver(), 60.0)
        assert sc["status"] == "optimal"
        assert sc["objective"] == pytest.approx(ex["objective"], rel=1e-6)
        assert ec.agrees(ex, sc)


def test_an_uncertified_match_does_not_count():
    ex = {"objective": -1.0}
    assert ec.agrees(ex, {"objective": -1.0, "status": "optimal"})
    assert not ec.agrees(ex, {"objective": -1.0, "status": "timelimit"})
    assert not ec.agrees(ex, {"objective": -0.9, "status": "optimal"})


def test_scip_is_not_ranked_when_it_failed_a_check():
    rows = [{"source": "validation", "seed": 42, "config": "free", "method": k,
             "objective": v, "test_auprc": 0.5}
            for k, v in (("greedy", 0.2), ("scip", 0.1))]
    s = ec.summarize([{"agree": False}], rows)
    inst = s["per_instance"][0]
    assert inst["best_method"] == ["greedy"]
    assert inst["gap_to_best"]["greedy"] == 0.0
    assert "scip_excluded_reason" in s
    assert ec.summarize([], rows)["scip_agrees_with_enumeration"] is False


def test_a_small_pool_is_refused_not_relabeled():
    with pytest.raises(ValueError):
        ec._first(np.zeros((50, 4)), 60)


def test_annealing_finds_the_certified_optimum_on_a_small_instance():
    # Rejecting every move would leave annealing at its random start, which
    # is feasible and no better than enumeration: only this catches it.
    for seed in range(3):
        J, C = _instance(seed=seed)
        ex = ec.exact_enumeration(J, C, 3)["objective"]
        sa = ec.simulated_annealing(J, C, 3, seed=seed, iterations=1500)
        assert sa["objective"] == pytest.approx(ex, rel=1e-9)


def test_greedy_re_solves_on_the_growing_support():
    # Reference greedy written out here: each step adds the learner that
    # minimizes the objective re-solved on the support so far plus it.
    for seed in range(4):
        J, C = _instance(n=12, seed=seed)
        chosen = []
        for _ in range(3):
            best = min((j for j in range(12) if j not in chosen),
                       key=lambda j: ec.objective(J, C, ec.solve_on_support(J, C, chosen + [j])))
            chosen.append(best)
        ref = ec.objective(J, C, ec.solve_on_support(J, C, chosen))
        assert ec.greedy(J, C, 3)["objective"] == pytest.approx(ref, rel=1e-9)


def test_the_cardinality_limit_binds():
    # Under the ridge the unconstrained optimum spreads over every learner;
    # a control that ignored m would report that support instead.
    J, C = _instance()
    relaxed = ec.solve_on_support(J, C, range(len(C)))
    assert int((relaxed > 1e-12).sum()) > 3
    assert ec.greedy(J, C, 3)["support_size"] <= 3


def test_pool_diagnostics_detect_memorizing_learners():
    y = np.array([1, -1, -1, 1, -1, -1])
    H = np.vstack([y, y, -y])          # two perfect learners, one inverted
    d = ec.pool_diagnostics(H.astype(float), y)
    assert d["learners_perfect_on_these_rows"] == 2
    assert d["pairwise_agreement_min"] == pytest.approx(-1.0)


def test_summary_keeps_sources_apart():
    rows = [{"source": s, "seed": 42, "config": "free", "method": "greedy",
             "objective": v, "test_auprc": 0.5} for s, v in (("train", -0.8), ("validation", 0.1))]
    keys = {(p["source"], p["objectives"]["greedy"])
            for p in ec.summarize([], rows)["per_instance"]}
    assert keys == {("train", -0.8), ("validation", 0.1)}


def test_the_exact_solver_is_an_interface():
    with pytest.raises(NotImplementedError):
        ec.ExactSolver().solve(None, None, 1, 1.0)
