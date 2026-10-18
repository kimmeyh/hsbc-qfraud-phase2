"""F106 (Sprint 27 Task I): the dequantization check's building blocks.

Synthetic data only; no dataset, nothing written. The check itself is
evidence (`f106_dequant.json`), not a test. These pin what it rests on:
the batched statevector against an explicit Kronecker-product circuit,
the adjoint gradient against finite differences, the Inverse Born Rule
case (C = 0 with the entangler off, C > 0 with it on), the phases, and
the outcome rule.
"""
from __future__ import annotations

import importlib
import sys
from functools import reduce
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "src"))

import f106_dequant as fd        # noqa: E402

Q = fd.N_QUBITS


def _params(seed=0, lam=None):
    p = fd.Params(0.3, seed)
    p.rot = np.random.default_rng(seed).uniform(-1, 1, p.rot.shape)
    p.w = np.random.default_rng(seed + 1).uniform(-1, 1, Q)
    if lam is not None:
        p.lam = np.full(fd.N_LAYERS, lam)
    return p


def _phases(n, seed=0):
    return np.random.default_rng(seed).uniform(-np.pi, np.pi, (n, Q))


def _on(q, M):
    I = np.eye(2)
    return reduce(np.kron, [M if k == q else I for k in range(Q)])


def _explicit_state(p, phi):
    """The same circuit as one 256 x 256 matrix product, qubit 0 the most
    significant bit."""
    psi = np.zeros(fd.DIM, dtype=complex)
    psi[0] = 1
    for l in range(fd.N_LAYERS):
        zz = np.diag(np.exp(-1j * p.lam[l] * fd.ZZ_DIAG))
        enc = [_on(q, fd._ry(phi[q] / 2)) for q in range(Q)]
        for U in enc:
            psi = U @ psi
        psi = zz @ psi
        for U in enc:
            psi = U @ psi
        for q in range(Q):
            psi = _on(q, fd._ry(p.rot[l, q, 0])) @ psi
            psi = _on(q, fd._rz(p.rot[l, q, 1])) @ psi
    return psi


def test_batched_state_matches_the_explicit_circuit():
    p, Phi = _params(), _phases(3)
    got = fd.state(p, Phi)
    for i in range(3):
        np.testing.assert_allclose(got[i], _explicit_state(p, Phi[i]),
                                   atol=1e-10)
    np.testing.assert_allclose((np.abs(got) ** 2).sum(1), 1, atol=1e-12)


def test_ring_diagonal_counts_eight_bonds():
    assert fd.ZZ_DIAG[0] == Q                     # |00000000>: all aligned
    alt = int("10101010", 2)
    assert fd.ZZ_DIAG[alt] == -Q                  # every bond anti-aligned


def _grad_matches_fd() -> bool:
    p, Phi = _params(3), _phases(12, 3)
    y = (np.arange(12) % 3 == 0).astype(float)
    _, g = fd.loss_and_grad(p, Phi, y)
    x0, h, num = p.flat(), 1e-6, []
    for k in range(len(x0)):
        for sgn in (1, -1):
            x = x0.copy()
            x[k] += sgn * h
            p.set_flat(x)
            num.append(fd.loss_and_grad(p, Phi, y)[0])
    num = (np.array(num[0::2]) - np.array(num[1::2])) / (2 * h)
    p.set_flat(x0)
    return bool(np.allclose(g, num, atol=1e-6, rtol=1e-4))


def test_adjoint_gradient_matches_finite_differences():
    assert _grad_matches_fd()


def test_gradient_check_can_fail():
    from injection import Mutation, assert_can_fail
    src = Path(fd.__file__)

    def run() -> bool:
        importlib.reload(fd)
        return _grad_matches_fd()

    try:
        assert_can_fail([Mutation(
            src, 'Y if gen[0] == "ry" else ZM, q), 0.5',
            'Y if gen[0] == "ry" else ZM, q), 1.0',
            expect_occurrences=1)], run, "the rotation generator's half")
    finally:
        importlib.reload(fd)


def _ibr_case() -> bool:
    Phi = _phases(50, 5)
    off = fd.diagnostics(_params(lam=0.0), Phi)
    on = fd.diagnostics(_params(lam=0.5), Phi)
    return (off["C"] == 0 and off["berry_abs"] < 1e-6
            and on["C"] > fd.C_FLOOR and on["berry_abs"] > 1e-3)


def test_entangler_off_is_real_and_on_is_phase_active():
    """IBR Theorem 1's case: RY-only encoding has real amplitudes."""
    assert _ibr_case()


def test_phase_active_check_can_fail():
    from injection import Mutation, assert_can_fail
    src = Path(fd.__file__)

    def run() -> bool:
        importlib.reload(fd)
        return _ibr_case()

    try:
        assert_can_fail([Mutation(
            src, 'seq.append(("zz", None, np.exp(-1j * params.lam[l] * ZZ_DIAG),',
            'seq.append(("zz", None, np.cos(params.lam[l] * ZZ_DIAG),',
            expect_occurrences=1)], run, "a real-valued entangler")
    finally:
        importlib.reload(fd)


def test_ecdf_phase_on_training_rows_is_the_rank_phase():
    import f103_tier1 as t1
    v = np.random.default_rng(2).lognormal(size=500)
    np.testing.assert_allclose(fd.ecdf_phase(v, v), t1.rank_phase(v))
    out = fd.ecdf_phase(v, np.array([v.min() - 1, v.max() + 1]))
    np.testing.assert_allclose(out, [-np.pi, np.pi])


def test_phases_are_fit_on_training_rows_and_decorrelated():
    rng = np.random.default_rng(4)
    a = rng.normal(size=(3000, Q))
    a[:, 1] = a[:, 0] + 0.3 * a[:, 1]
    ph = fd.Phases(a[:2000])
    P = ph(a[:2000])
    assert abs(np.corrcoef(P, rowvar=False)[0, 1]) < 0.05
    Pte = ph(a[2000:])
    assert Pte.min() >= -np.pi and Pte.max() <= np.pi


def _cmp(lo, hi):
    return {"no_worse_within_margin": lo > -fd.MARGIN, "circuit_ahead": hi < 0}


def test_outcome_rule():
    behind = _cmp(-0.05, -0.01)
    assert fd.outcome({"a": behind, "b": _cmp(-0.004, 0.01)}) == "dequantized"
    assert fd.outcome({"a": behind, "b": behind}) == "circuit ahead"
    assert fd.outcome({"a": behind, "b": _cmp(-0.02, 0.01)}) == "inconclusive"


def test_compare_flags_an_identical_twin_and_clears_a_noise_twin(monkeypatch):
    monkeypatch.setattr(fd, "N_BOOT", 200)
    monkeypatch.setattr(fd, "TWINS", ("same", "noise"))
    rng = np.random.default_rng(6)
    ys, scores = {}, {}
    for s in (1, 2):
        y = (rng.uniform(size=2000) < 0.1).astype(int)
        p = y + rng.normal(scale=0.8, size=2000)
        ys[s] = y
        scores[s] = {"circuit": p, "same": p.copy(),
                     "noise": rng.uniform(size=2000)}
    cmp = fd.compare((1, 2), ys, scores)
    assert cmp["same"]["no_worse_within_margin"]
    assert cmp["same"]["mean_delta_auprc"] == 0
    assert cmp["noise"]["circuit_ahead"]
    assert not cmp["noise"]["no_worse_within_margin"]
