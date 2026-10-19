"""F130 (Sprint 27 Task E): the lever screens' building blocks and rule.

Zero metered, no dataset, nothing written to an evidence directory: pools
are built on small synthetic data and the decision rule is checked on
synthetic seed deltas. `qubo_proxy.build_pool`'s new `pair_count` must leave
Phase 1's build unchanged when it is not passed (CLAUDE.md, the Phase 1
boundary, rule 4).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))

import f130_levers as fl         # noqa: E402
import qubo_proxy as qp          # noqa: E402


def _data(n=200, d=7, seed=0):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, d)).astype("float32")
    y = np.where(X[:, 0] + X[:, 1] + 0.5 * rng.normal(size=n) > 0, 1, -1)
    return X, y


def test_pair_count_limits_the_pairs_and_the_default_is_unchanged():
    X, y = _data()
    d = X.shape[1]
    default = qp.build_pool(X, y, 2, "dct", "sequential",
                            weak_params=qp.seeded_weak_params(42))
    assert len(default.h_list) == d + fl.pair_cap(d)
    assert not hasattr(default, "weak_cls_pair_count") or \
        default.weak_cls_pair_count is None
    five = qp.build_pool(X, y, 2, "dct", "sequential",
                         weak_params=qp.seeded_weak_params(42), pair_count=5)
    assert len(five.h_list) == d + 5
    assert sum(len(i) == 2 for i in five.ind_list) == 5


def test_pair_count_is_refused_on_a_full_pair_build():
    X, y = _data()
    with pytest.raises(ValueError, match="sequential"):
        qp.build_pool(X, y, 2, "dct", "full", pair_count=5)


def test_a_pair_count_above_the_cap_cannot_be_built():
    """Why the plan's rank 6 values stop at the cap: eqc-models asserts."""
    X, y = _data()
    with pytest.raises(AssertionError):
        qp.build_pool(X, y, 2, "dct", "sequential",
                      pair_count=fl.pair_cap(X.shape[1]) + 1)


def test_a_pair_count_at_the_cap_is_the_default_pool():
    """The identity control: pairs_N at the cap rebuilds the default pool."""
    X, y = _data()
    cap = fl.pair_cap(X.shape[1])
    default = qp.build_pool(X, y, 2, "dct", "sequential",
                            weak_params=qp.seeded_weak_params(42))
    capped = qp.build_pool(X, y, 2, "dct", "sequential",
                           weak_params=qp.seeded_weak_params(42),
                           pair_count=cap)
    assert [tuple(i) for i in capped.ind_list] == \
        [tuple(i) for i in default.ind_list]
    assert np.array_equal(qp.h_matrix(capped, X), qp.h_matrix(default, X))


@pytest.mark.parametrize("schedule,count,match", [
    (2, 0, ">= 1"), (2, -3, ">= 1"), (1, 5, "schedule >= 2")])
def test_a_pair_count_the_builder_would_ignore_is_refused(schedule, count,
                                                         match):
    X, y = _data()
    with pytest.raises(ValueError, match=match):
        qp.build_pool(X, y, schedule, "dct", "sequential", pair_count=count)


def test_the_pair_count_floor_can_fail():
    import importlib

    from injection import Mutation, assert_can_fail
    src = Path(qp.__file__)

    def run() -> bool:
        importlib.reload(qp)
        X, y = _data()
        try:
            qp.build_pool(X, y, 2, "dct", "sequential", pair_count=0)
        except ValueError:
            return True
        return False

    try:
        assert_can_fail([Mutation(src, "if int(pair_count) < 1:",
                                  "if int(pair_count) < -99:",
                                  expect_occurrences=1)],
                        run, "the pair_count floor")
    finally:
        importlib.reload(qp)


def test_the_planned_pair_counts_respect_each_datasets_cap():
    n_features = {"energy_steel": 17, "oilgas_gasturbine": 15,
                  "telecom_churn": 17}
    for ds, counts in fl.PAIR_COUNTS.items():
        assert max(counts) <= fl.pair_cap(n_features[ds]), ds
    assert fl.PAIR_COUNTS["energy_steel"] == (30, 60, 90, 119)
    assert fl.PAIR_COUNTS["oilgas_gasturbine"] == (30, 60, 90)


def test_a_seeded_knn_build_raises_so_knn_skips_the_seed():
    X, y = _data()
    with pytest.raises(TypeError):
        qp.build_pool(X, y, 1, "knn", "sequential",
                      weak_params=qp.seeded_weak_params(42))
    assert fl.weak_params("knn", 42) == {}
    assert fl.weak_params("dct", 42) == {"random_state": 42}
    clf = qp.build_pool(X, y, 1, "knn", "sequential",
                        weak_params=fl.weak_params("knn", 42))
    assert len(clf.h_list) == X.shape[1]


def test_the_knn_seed_skip_can_fail():
    import importlib

    from injection import Mutation, assert_can_fail
    src = Path(fl.__file__)

    def run() -> bool:
        importlib.reload(fl)
        X, y = _data()
        try:
            qp.build_pool(X, y, 1, "knn", "sequential",
                          weak_params=fl.weak_params("knn", 42))
        except TypeError:
            return False
        return True

    try:
        assert_can_fail([Mutation(src, '    if weak_type == "knn":\n'
                                  '        return dict(params or {})\n',
                                  "", expect_occurrences=1)],
                        run, "a seeded KNN build")
    finally:
        importlib.reload(fl)


def test_the_phase_block_is_whitened_on_training_rows_only():
    rng = np.random.default_rng(1)
    cols = ["a", "x_phase", "y_phase"]
    Xtr = np.column_stack([rng.normal(size=500),
                           rng.uniform(-np.pi, np.pi, 500),
                           rng.uniform(-np.pi, 0, 500)]).astype("float32")
    Xte = Xtr[:50] + 1.0
    Ptr, Pte, names = fl.phase_block(Xtr, Xte, cols)
    assert names == ["a", "cos_x_phase", "cos_y_phase", "sin_x_phase",
                     "sin_y_phase"]
    np.testing.assert_allclose(Ptr[:, 0], Xtr[:, 0])
    B = Ptr[:, 1:].astype(np.float64)
    np.testing.assert_allclose(B.mean(axis=0), 0, atol=1e-5)
    np.testing.assert_allclose(np.cov(B, rowvar=False), np.eye(4), atol=1e-3)
    # The test rows are transformed with the training statistics, not their
    # own: their block is not re-centered.
    assert np.abs(Pte[:, 1:].mean(axis=0)).max() > 0.1


def test_the_decision_rule():
    flat = [0.001, 0.002, 0.0015, 0.001, 0.002]       # CI > 0 but below 0.005
    up = [0.010, 0.012, 0.008, 0.011, 0.009]
    mixed = [0.02, -0.02, 0.03, -0.03, 0.0]
    v = fl.verdict(flat, mixed)
    assert not v["moves_auprc"] and not v["beats_hgb"] and v["rejected"]
    v = fl.verdict(up, up)
    assert v["moves_auprc"] and v["direction"] == "up" and v["beats_hgb"]
    v = fl.verdict([-x for x in up], mixed)
    assert v["moves_auprc"] and v["direction"] == "down" and not v["rejected"]
    v = fl.verdict(mixed, [-x for x in up])
    assert not v["moves_auprc"] and not v["beats_hgb"] and v["rejected"]


def test_the_decision_rule_can_fail():
    import importlib

    from injection import Mutation, assert_can_fail
    src = Path(fl.__file__)

    def run() -> bool:
        importlib.reload(fl)
        return not fl.verdict([0.001, 0.002, 0.0015, 0.001, 0.002],
                              [0.0] * 5)["moves_auprc"]

    try:
        assert_can_fail([Mutation(src, "abs(mean_b) >= MOVE_MIN and ",
                                  "", expect_occurrences=1)],
                        run, "a CI-only move rule")
    finally:
        importlib.reload(fl)


def test_a_lever_missing_a_seed_is_not_judged():
    rows = []
    for s in (42, 43, 44, 45, 46):
        rows.append({"dataset": "spectra_x", "seed": s,
                     "variant": "baseline_dct", "test_auprc": 0.5,
                     "train_auprc": 0.6, "hgb_test_auprc": 0.5,
                     "n_learners": 10})
        lever = {"dataset": "spectra_x", "seed": s, "variant": "knn",
                 "hgb_test_auprc": 0.5}
        lever.update({"error": "boom"} if s == 46 else
                     {"test_auprc": 0.6, "train_auprc": 0.6,
                      "n_learners": 10})
        rows.append(lever)
    out = fl.summarize(rows)["spectra_x"]["knn"]
    assert out["n_seeds"] == 4 and out["errors"] == ["boom"]
    assert out["verdict"].startswith("not judged")
    assert "moves_auprc" not in out
