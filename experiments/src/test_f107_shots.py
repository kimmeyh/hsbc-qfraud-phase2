"""F107 (Sprint 27 Task J): the shot estimator and the Schmidt rank.

Synthetic states only; no dataset, nothing written. The shot-budget result
is evidence (`f107_shots.json`), not a test.
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "src"))

import f106_dequant as fd        # noqa: E402
import f107_shots as fs          # noqa: E402


def _states(n=40, seed=0):
    p = fd.Params(0.3, seed)
    p.rot = np.random.default_rng(seed).uniform(-1, 1, p.rot.shape)
    Phi = np.random.default_rng(seed + 1).uniform(-np.pi, np.pi, (n, fd.N_QUBITS))
    return fd.state(p, Phi)


def _converges() -> bool:
    p = fs.probabilities(_states())
    exact = p @ fd.Z.T
    rng = np.random.default_rng(3)
    err = [np.abs(fs.shot_expectations(p, m, rng) - exact).mean()
           for m in (100, 100000)]
    return bool(err[1] < 0.01 and err[1] < err[0] / 10)


def test_shot_estimator_converges_to_the_exact_expectation():
    assert _converges()


def test_shot_estimator_check_can_fail():
    from injection import Mutation, assert_can_fail
    src = Path(fs.__file__)

    def run() -> bool:
        importlib.reload(fs)
        return _converges()

    try:
        assert_can_fail([Mutation(
            src, "return (counts / m) @ fd.Z.T",
            "return (counts / (2 * m)) @ fd.Z.T",
            expect_occurrences=1)], run, "a miscounted shot total")
    finally:
        importlib.reload(fs)


def test_shots_keep_qubit_correlations():
    """A Bell-like state: qubits 0 and 4 always agree in every shot."""
    psi = np.zeros((1, fd.DIM), dtype=complex)
    psi[0, 0] = psi[0, int("10001000", 2)] = 2 ** -0.5
    rng = np.random.default_rng(4)
    counts = rng.multinomial(1000, fs.probabilities(psi))
    bits = fd._BITS[counts[0] > 0]
    assert np.all(bits[:, 0] == bits[:, 4])


def test_effective_schmidt_rank_product_and_maximal():
    prod = np.zeros((1, fd.DIM), dtype=complex)
    prod[0, 0] = 1
    np.testing.assert_allclose(fs.effective_schmidt_rank(prod), [1.0])
    maxent = np.zeros((1, 16, 16), dtype=complex)
    maxent[0, np.arange(16), np.arange(16)] = 0.25
    np.testing.assert_allclose(
        fs.effective_schmidt_rank(maxent.reshape(1, fd.DIM)), [16.0])


def test_critical_budget():
    exact = 0.80
    assert fs.critical_budget({10: 0.5, 100: 0.79, 1000: 0.799,
                               10000: 0.80}, exact) == 1000
    assert fs.critical_budget({10: 0.5, 100: 0.6, 1000: 0.7,
                               10000: 0.78}, exact) == "above 10000"
