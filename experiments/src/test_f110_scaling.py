"""F110: the subsample, the slope test and the pilot gate match the entry.

Sprint 28 Task E (#52). Synthetic inputs; the timing run builds ULB pools
and is not run here.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))

import f110_scaling as fs  # noqa: E402


def test_the_entry_constants():
    assert fs.FRACTIONS == (0.10, 0.25, 0.50, 1.00)
    assert fs.FREE_SEEDS == (42, 43, 44, 45, 46)
    assert fs.PROJECTION_CAP_MIN == 120.0
    assert fs.P1_BAND == (0.7, 1.3) and fs.P2_BAND == (-0.2, 0.2)


def test_subsample_keeps_each_class_share():
    y = np.array([0] * 900 + [1] * 100)
    idx = fs.subsample(y, 0.25, 42)
    assert len(idx) == 250 and y[idx].sum() == 25
    assert np.array_equal(idx, fs.subsample(y, 0.25, 42))
    assert len(fs.subsample(y, 1.0, 42)) == 1000


def _rows(exp_build, exp_solve, noise=0.0, seed=0):
    rng = np.random.default_rng(seed)
    out = []
    for s in range(5):
        for n in (1000, 2500, 5000, 10000):
            e = np.exp(rng.normal(0, noise, 2)) if noise else (1.0, 1.0)
            out.append({"cell": "free", "seed": s, "fraction": n / 10000, "rows": n,
                        "build_s": 1e-3 * n ** exp_build * e[0],
                        "construction_s": 1e-6 * n,
                        "solve_s": 0.01 * n ** exp_solve * e[1],
                        "total_s": 1.0})
    return out


def test_slope_recovers_a_known_exponent():
    s = fs.slope(_rows(1.0, 0.0, noise=0.05), "build_s")
    assert s["low"] < 1.0 < s["high"]


def test_predictions_hold_on_linear_build_and_flat_solve():
    a = fs.analyze({"runs": _rows(1.0, 0.0, noise=0.02)})["free"]
    assert a["P1_holds"] and a["P2_holds"]


def test_a_quadratic_build_breaks_p1():
    a = fs.analyze({"runs": _rows(2.0, 0.0, noise=0.02)})["free"]
    assert not a["P1_holds"]


def test_a_growing_solve_breaks_p2():
    a = fs.analyze({"runs": _rows(1.0, 0.8, noise=0.02)})["free"]
    assert not a["P2_holds"]


def test_solve_time_subtracts_only_the_j_rebuild(monkeypatch):
    # H is slow and the solve is short: subtracting H as well clamps the
    # solve to zero (the first version's defect).
    import time
    import types

    class Split:
        y_train = types.SimpleNamespace(to_numpy=lambda: np.array([0, 1] * 50))
    X = np.zeros((100, 4), dtype=np.float32)
    y = np.array([-1, 1] * 50)
    qp = types.SimpleNamespace(
        CONFIGS={"free": {"k": 4, "schedule": 2}}, LAMBDA_MULT=2.0,
        _prep=lambda seed, k: (Split, None, X, None, None, y),
        seeded_weak_params=lambda seed: {},
        h_matrix=lambda clf, X_: (time.sleep(0.20), np.zeros((10, len(X_))))[1],
        hamiltonian=lambda H, y_, lam: time.sleep(0.02),
        solve_simplex_qp=lambda H, y_, lam: time.sleep(0.12))
    fpp = types.SimpleNamespace(build_full=lambda *a, **k: object())
    monkeypatch.setitem(sys.modules, "qubo_proxy", qp)
    monkeypatch.setitem(sys.modules, "full_pair_pool", fpp)
    r = fs.time_one("free", 42, 1.0)
    assert 0.06 < r["solve_s"] < 0.15 and not r["solve_clamped"]
    assert r["construction_s"] == pytest.approx(r["h_matrix_s"] + r["j_build_s"], abs=2e-3)


def test_projection_scales_the_pilot_by_the_remaining_seeds():
    pilot = [{"total_s": 300.0}] * 4                 # 20 minutes per seed
    assert fs.projection_min(pilot) == pytest.approx(80.0)
