"""F159 (Sprint 29 Task B, #65): the parallel pool equals the serial one.

Equality is read on HELD-OUT rows. On the training rows it is vacuous: two
pools built with different seeds agree there (Sprint 29 planning probe).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
PHASE2 = ROOT / "experiments" / "phase2" / "src"
THIS = Path(__file__).relative_to(ROOT).as_posix()
sys.path.insert(0, str(PHASE2))
sys.path.insert(0, str(ROOT / "experiments" / "src"))

import f159_parallel_pool as f159  # noqa: E402
import full_pair_pool as fpp  # noqa: E402


def _data():
    rng = np.random.default_rng(7)
    X = rng.normal(size=(400, 6))
    y = np.where(X[:, 0] + 0.5 * X[:, 1] * X[:, 2]
                 + rng.normal(scale=0.5, size=400) > 0, 1, -1)
    return X[:300], y[:300], X[300:]


def test_the_parallel_pool_equals_the_serial_pool_on_held_out_rows():
    import qubo_proxy as qp
    X, y, X_held = _data()
    params = qp.seeded_weak_params(42)
    serial = fpp.build_full(X, y, 2, "dct", weak_params=params)
    par, per = f159.build_parallel(X, y, 2, "dct", 42, workers=2)
    assert par.ind_list == serial.ind_list
    assert len(per) == len(serial.h_list) == 21
    assert np.array_equal(qp.h_matrix(par, X_held), qp.h_matrix(serial, X_held))
    assert f159.h_sha256(par, X_held) == f159.h_sha256(serial, X_held)
    for k in ("lambda_coef", "weak_cls_schedule", "weak_cls_type",
              "weak_cls_params"):
        assert getattr(par, k) == getattr(serial, k)


def test_an_empty_index_list_builds_no_learners():
    X, y, _ = _data()
    clf = fpp.build_full(X, y, 2, "dct", indices=[])
    assert clf.h_list == [] and clf.ind_list == []


def _unit(frac, build, sha, secs):
    u = {"fraction": frac, "build": build, "rows": 10, "build_s": secs,
         "h_validation_sha256": sha}
    if build != "serial":
        u["longest_learner_s"] = 0.1
    return u


def test_analyze_reads_speedup_and_flags_a_mismatch():
    units = [_unit(0.1, "serial", "a", 8.0), _unit(0.1, "4", "a", 2.0),
             _unit(0.1, "8", "b", 1.0)]
    a = f159.analyze(units)
    assert a["0.1"]["speedup"] == {"4": 4.0, "8": 8.0}
    assert a["0.1"]["equal_on_validation"] == {"4": True, "8": False}
    assert a["all_equal"] is False
    assert f159.analyze(units[:2])["all_equal"] is True
    assert f159.analyze([])["all_equal"] is False


def test_a_failed_build_is_recorded_and_left_out_of_the_comparison():
    units = [_unit(0.1, "serial", "a", 8.0), _unit(0.1, "4", "a", 2.0),
             {"fraction": 0.1, "build": "32", "rows": 10,
              "failed": "MemoryError", "seconds_to_failure": 3.0}]
    a = f159.analyze(units)
    assert a["0.1"]["failed"] == {"32": "MemoryError"}
    assert a["0.1"]["speedup"] == {"4": 4.0}
    assert a["all_equal"] is True


def test_the_failed_build_exclusion_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    assert_can_fail(
        [Mutation(PHASE2 / "f159_parallel_pool.py",
                  "        par = [u for u in built if \"failed\" not in u]\n",
                  "        par = built\n", expect_occurrences=1)],
        lambda: run_pytest(
            f"{THIS}::test_a_failed_build_is_recorded_and_left_out_of_the_comparison",
            ROOT),
        "a failed build compared")


def test_the_complete_marker_needs_every_unit():
    units = [_unit(f, b, "a", 1.0) for f in f159.FRACTIONS
             for b in ("serial", *map(str, f159.WORKERS))]
    assert f159._doc(units)["complete"] is True
    assert f159._doc(units[:-1])["complete"] is False


def test_the_equality_check_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    assert_can_fail(
        [Mutation(PHASE2 / "f159_parallel_pool.py",
                  "    clf.h_list = [wc for wc, _ in out]\n",
                  "    clf.h_list = [wc for wc, _ in out][::-1]\n",
                  expect_occurrences=1)],
        lambda: run_pytest(
            f"{THIS}::test_the_parallel_pool_equals_the_serial_pool_on_held_out_rows",
            ROOT),
        "learners out of order")
