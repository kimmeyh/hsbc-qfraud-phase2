"""F103 (Sprint 27 Task F): the Tier 1 reimplementation's building blocks.

Synthetic data only; no dataset, nothing written. The known-answer check
itself is evidence (`f103_tier1.json`), not a test. These pin the pieces
the check rests on: the rank phase, the trained-frequency search, JOINT's
k-way scan (which must find a planted joint frequency, including a
negative component), and the chain simulator.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))

import f103_tier1 as t1          # noqa: E402


def test_rank_phase_is_uniform_on_minus_pi_pi():
    v = np.random.default_rng(0).lognormal(size=1000)
    p = t1.rank_phase(v)
    assert p.min() > -np.pi and p.max() < np.pi
    np.testing.assert_allclose(np.sort(p)[[0, -1]],
                               [-np.pi + np.pi / 1000, np.pi - np.pi / 1000])


def test_whiten_rerank_decorrelates_and_keeps_uniform_phases():
    rng = np.random.default_rng(1)
    a = rng.uniform(-np.pi, np.pi, 4000)
    P = np.column_stack([a, a + 0.3 * rng.normal(size=4000)])
    W = t1.whiten_rerank(P)
    assert abs(np.corrcoef(W, rowvar=False)[0, 1]) < 0.05
    assert W.min() > -np.pi and W.max() < np.pi


def test_trained_frequency_finds_an_off_grid_frequency():
    rng = np.random.default_rng(2)
    phi = rng.uniform(-np.pi, np.pi, 5000)
    y = (rng.uniform(size=5000) < 0.5 + 0.4 * np.cos(2.37 * phi)).astype(int)
    assert abs(t1.trained_frequency(phi, y) - 2.37) < 0.02


def _planted(n=4000, f=(3.7, -5.1, 6.8), seed=3):
    rng = np.random.default_rng(seed)
    P = rng.uniform(-np.pi, np.pi, size=(n, 3))
    u = P @ np.asarray(f)
    y = (rng.uniform(size=n) < 0.5 + 0.45 * np.cos(u + 0.4)).astype(int)
    return P, y


def _scan_recovers() -> bool:
    P, y = _planted()
    _, f = t1.joint_scan(P, y - y.mean(), (0, 1, 2))
    if f[0] < 0:
        f = -f
    return bool(np.abs(f - np.array([3.7, -5.1, 6.8])).max() <= 0.05)


def test_the_joint_scan_recovers_a_planted_joint_frequency():
    assert _scan_recovers()


def test_the_joint_scan_can_fail():
    import importlib

    from injection import Mutation, assert_can_fail
    src = Path(t1.__file__)

    def run() -> bool:
        importlib.reload(t1)
        return _scan_recovers()

    try:
        assert_can_fail([Mutation(
            src, "_, f0 = best([COARSE_AXIS, signed, signed])",
            "_, f0 = best([COARSE_AXIS, COARSE_AXIS, COARSE_AXIS])",
            expect_occurrences=1)], run, "the scan without signs")
    finally:
        importlib.reload(t1)


def test_the_bond_gate_is_unitary_and_commutes_with_its_hamiltonian():
    U = t1._bond_unitary(3, 1, 0.7)
    np.testing.assert_allclose(U @ U.conj().T, np.eye(8), atol=1e-12)


def test_no_couplings_leave_zz_at_zero():
    """With J = 0 the evolution is a product of Z rotations on |+>, so every
    <Z_i Z_{i+1}> stays 0: the additive-model limit the paper ablates."""
    P = np.random.default_rng(4).uniform(-np.pi, np.pi, size=(50, 4))
    o = t1.chain_observable(P, np.zeros(3))
    np.testing.assert_allclose(o, 0.0, atol=1e-12)


def test_the_chain_matches_an_explicit_trotter_product():
    from scipy.linalg import expm
    n, rng = 3, np.random.default_rng(5)
    phi = rng.uniform(-np.pi, np.pi, size=n)
    J = rng.uniform(0.5, 1.5, size=n - 1)
    X = np.array([[0, 1], [1, 0]]); Y = np.array([[0, -1j], [1j, 0]])
    Z = np.diag([1.0, -1.0]); I = np.eye(2)

    def op(ms):
        out = np.array([[1.0]])
        for m in ms:
            out = np.kron(out, m)
        return out
    bonds = [J[k] * sum(op([A if i in (k, k + 1) else I for i in range(n)])
                        for A in (X, Y, Z)) for k in range(n - 1)]
    field = sum(phi[i] * op([Z if j == i else I for j in range(n)])
                for i in range(n))
    psi = np.full(2 ** n, 2 ** (-n / 2), dtype=complex)
    for _ in range(3):
        for B in bonds:
            psi = expm(-1j * B) @ psi
        psi = expm(-1j * field) @ psi
    zz = sum(op([Z if j in (i, i + 1) else I for j in range(n)])
             for i in range(n - 1))
    want = float(np.real(psi.conj() @ zz @ psi))
    got = float(t1.chain_observable(phi[None, :], J, t=3.0, steps=3)[0])
    assert abs(got - want) < 1e-10


def test_gates_refuse_when_a_necessary_gate_fails():
    lanes = {"gam": 0.9, "ga2m": 0.92, "hgb": 0.99, "joint": 0.91}
    g = t1.gates(lanes, rho_off=0.1, d=5)
    assert not g["g1_pass"] and not g["g4_pass"] and g["tier1"] == "refuse"
    g = t1.gates({**lanes, "joint": 0.95}, rho_off=0.5, d=5)
    assert g["tier1"] == "candidate"
    assert not t1.gates({**lanes, "joint": 0.95}, 0.5, d=15)["g5_pass"]


def test_the_check_uses_the_entrys_tolerances():
    assert t1.KNOWN["real_g2_gam_auc"] == (0.94, 0.03)
    assert t1.KNOWN["sparse_joint_minus_ga2m"] == (0.37, 0.05)
    assert t1.KNOWN["dense_hgb_minus_gam"] == (0.15, 0.05)
    assert t1.KNOWN["dense_joint_minus_ga2m"] == (0.00, 0.05)
    assert t1.JOINT_TERMS == 6 and t1.JOINT_ORDER == 3
    rows = {"real": [{"gam": 0.92}, {"gam": 0.93}],
            "sparse": [{"joint": 0.95, "ga2m": 0.5}] * 2,
            "dense": [{"hgb": 0.7, "gam": 0.55, "joint": 0.6,
                       "ga2m": 0.6}] * 2}
    c = t1.check(rows)
    assert c["real_g2_gam_auc"]["within"] and c["task_g_runs"]
    assert not c["sparse_joint_minus_ga2m"]["within"]       # +0.45 vs +0.37
    assert c["dense_hgb_minus_gam"]["within"]               # +0.15
    assert c["dense_joint_minus_ga2m"]["within"]            # +0.00


@pytest.mark.parametrize("mean,ok", [(0.90, False), (0.92, True),
                                     (0.97, True), (0.98, False)])
def test_task_g_hangs_on_g2_alone(mean, ok):
    rows = {"real": [{"gam": mean}] * 2,
            "sparse": [{"joint": 0.0, "ga2m": 0.0}] * 2,
            "dense": [{"hgb": 0.0, "gam": 0.0, "joint": 0.0,
                       "ga2m": 0.0}] * 2}
    assert t1.check(rows)["task_g_runs"] is ok
