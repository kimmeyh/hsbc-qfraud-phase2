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
    par, per = f159.build_parallel(X, y, 2, "dct", 42, budget_s=600,
                                   workers=2)
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


def test_a_fraction_with_no_compared_pool_is_not_all_equal():
    # Every parallel build at 0.1 failed: nothing was compared there
    # (PR 63 review), so the pools are not shown equal at every fraction.
    units = [_unit(0.1, "serial", "a", 8.0),
             {"fraction": 0.1, "build": "4", "rows": 10,
              "failed": "MemoryError", "seconds_to_failure": 3.0}]
    a = f159.analyze(units)
    assert a["0.1"]["equal_on_validation"] == {}
    assert a["all_equal"] is False


def test_the_compared_pool_term_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    assert_can_fail(
        [Mutation(PHASE2 / "f159_parallel_pool.py",
                  "        bool(v[\"equal_on_validation\"]) and "
                  "all(v[\"equal_on_validation\"].values())\n",
                  "        all(v[\"equal_on_validation\"].values())\n",
                  expect_occurrences=1)],
        lambda: run_pytest(
            f"{THIS}::test_a_fraction_with_no_compared_pool_is_not_all_equal",
            ROOT),
        "a fraction with nothing compared read as equal")


def test_each_parallel_build_gets_its_budget():
    import pytest
    units = [_unit(0.25, "serial", "a", 30.0)]
    assert f159.budget_for(units, 0.25, "serial") is None
    assert f159.budget_for(units, 0.25, "32") == f159.BUDGET_X * 30.0
    with pytest.raises(ValueError):
        f159.budget_for(units, 0.5, "32")


def test_the_budget_derivation_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    assert_can_fail(
        [Mutation(PHASE2 / "f159_parallel_pool.py",
                  "    return BUDGET_X * serial[0][\"build_s\"]\n",
                  "    return None\n", expect_occurrences=1)],
        lambda: run_pytest(f"{THIS}::test_each_parallel_build_gets_its_budget",
                           ROOT),
        "a parallel build with no budget")


def test_an_abandoned_build_leaves_with_its_status(monkeypatch):
    codes = []
    monkeypatch.setattr(f159.os, "_exit", codes.append)
    monkeypatch.setattr(f159, "_ABANDONED", False)
    f159.leave_if_abandoned(failed=True)
    assert codes == []                 # nothing abandoned: a normal exit
    monkeypatch.setattr(f159, "_ABANDONED", True)
    f159.leave_if_abandoned(failed=True)
    f159.leave_if_abandoned(failed=False)
    assert codes == [1, 0]


def test_the_exit_status_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    assert_can_fail(
        [Mutation(PHASE2 / "f159_parallel_pool.py",
                  "        os._exit(1 if failed else 0)\n",
                  "        os._exit(0)\n", expect_occurrences=1)],
        lambda: run_pytest(
            f"{THIS}::test_an_abandoned_build_leaves_with_its_status", ROOT),
        "an error after a timeout exits 0")


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


def test_a_build_past_its_budget_is_recorded_as_failed(monkeypatch):
    import time
    X, y, X_held = _data()
    monkeypatch.setattr(f159, "_data", lambda frac: (2, X, y, X_held))
    monkeypatch.setattr(f159, "_build_unbudgeted",
                        lambda *a, **k: time.sleep(5))
    monkeypatch.setattr(f159, "_ABANDONED", False)
    t0 = time.perf_counter()
    row = f159.time_unit(0.1, "32", budget_s=0.2)
    assert time.perf_counter() - t0 < 3
    assert row["failed"] == "BuildTimeout"
    assert row["error"].startswith("no result in")
    assert row["budget_s"] == 0.2 and row["rows"] == 300
    assert f159._ABANDONED is True
    a = f159.analyze([_unit(0.1, "serial", "a", 8.0), row])
    assert a["0.1"]["failed"] == {"32": "BuildTimeout"}
    assert a["0.1"]["speedup"] == {}


def test_a_build_within_its_budget_returns_its_result(monkeypatch):
    monkeypatch.setattr(f159, "_build_unbudgeted",
                        lambda *a, **k: ("clf", [1]))
    assert f159.build_parallel(1, 2, 3, "dct", 42, budget_s=5) == ("clf", [1])

    def boom(*a, **k):
        raise MemoryError
    monkeypatch.setattr(f159, "_build_unbudgeted", boom)
    import pytest
    with pytest.raises(MemoryError):
        f159.build_parallel(1, 2, 3, "dct", 42, budget_s=5)


def test_the_parallel_build_needs_a_budget(monkeypatch):
    # Sprint 29 IMP-3: F166 called the build without the time limit.
    import pytest
    calls = []
    monkeypatch.setattr(f159, "_build_unbudgeted",
                        lambda *a, **k: calls.append(1) or ("clf", []))
    with pytest.raises(TypeError):
        f159.build_parallel(1, 2, 3, "dct", 42)
    for bad in (None, 0, -1, float("nan"), float("inf"), True, "60"):
        with pytest.raises(ValueError, match="nothing was built"):
            f159.build_parallel(1, 2, 3, "dct", 42, budget_s=bad)
    assert calls == []


def test_no_module_calls_the_unbudgeted_build():
    import re
    pattern = re.compile(r"\b_build_unbudgeted\b")
    callers = sorted(p.name for d in (PHASE2, ROOT / "experiments" / "src",
                                      ROOT / "scripts")
                     for p in d.glob("*.py")
                     if not p.name.startswith("test_")
                     and p.name != "f159_parallel_pool.py"
                     and pattern.search(p.read_text(encoding="utf-8")))
    assert callers == []


def test_the_budget_requirement_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    assert_can_fail(
        [Mutation(PHASE2 / "f159_parallel_pool.py",
                  "            or not math.isfinite(budget_s) or budget_s <= 0):\n",
                  "            and False):\n", expect_occurrences=1)],
        lambda: run_pytest(
            f"{THIS}::test_the_parallel_build_needs_a_budget", ROOT),
        "a build with no valid budget")
    assert_can_fail(
        [Mutation(PHASE2 / "f166_ulb_algorithms.py",
                  "        clf, _ = f159.build_parallel(",
                  "        clf, _ = f159._build_unbudgeted(",
                  expect_occurrences=1)],
        lambda: run_pytest(
            f"{THIS}::test_no_module_calls_the_unbudgeted_build", ROOT),
        "a module calling the unbudgeted build")


def test_the_budget_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    assert_can_fail(
        [Mutation(PHASE2 / "f159_parallel_pool.py",
                  "        raise BuildTimeout(f\"no result in {budget_s:.0f} s\")\n",
                  "        pass\n", expect_occurrences=1)],
        lambda: run_pytest(
            f"{THIS}::test_a_build_past_its_budget_is_recorded_as_failed",
            ROOT),
        "a build past its budget not stopped")


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
