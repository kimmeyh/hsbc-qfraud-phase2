"""F104 (Sprint 27 Task B): the pre-run resolution gate, as a tested gate.

`device_resolution.resolution_gate` is A31's test: a job passes only when
both its off-diagonal and its linear coefficient spreads reach max
|coefficient| / 200. The F142 runner screens every job through it. The
gate's result on the real B2 and B4 pools is evidence, not a test fixture:
`experiments/phase2/src/f104_gate_check.py` records it, because the data
and the full-pair build are not available in CI. Zero metered.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))

import device_resolution as dres     # noqa: E402
import run_dirac3s_verify as R       # noqa: E402


def _cvqboost_like(spread_off: float, spread_lin: float, n=20, seed=0):
    """Large, nearly equal off-diagonals (B1's shape under A31), with the
    off-diagonal and linear spreads set in units of the device step."""
    rng = np.random.default_rng(seed)
    diag, off_base, lin_base = 3000.0, 1000.0, -200.0
    step = diag / dres.DYNAMIC_RANGE
    off = off_base + rng.uniform(0, spread_off * step, size=(n, n))
    J = np.triu(off, 1) + np.triu(off, 1).T
    np.fill_diagonal(J, diag)
    C = lin_base - rng.uniform(0, spread_lin * step, size=n)
    return J, C


def _gate_holds() -> bool:
    """Fails an unresolvable job (either spread short), passes a resolvable
    one, and the F142 runner's screen gives the same verdict."""
    cases = {(0.01, 0.01): False, (5.0, 0.01): False, (0.01, 5.0): False,
             (5.0, 5.0): True}
    for (o, lin), want in cases.items():
        J, C = _cvqboost_like(o, lin)
        if dres.resolution_gate(J, C)["pass"] is not want:
            return False
        if R.resolution_screen(J, C)["pass"] is not want:
            return False
    return True


def test_the_gate_is_a31s_spread_test():
    assert _gate_holds()


def test_the_gate_passes_what_the_dynamic_range_would_wrongly_pass():
    J, C = _cvqboost_like(0.01, 0.01)
    dr_db = 10 * np.log10(np.abs(J).max() / np.abs(C).min())
    assert dr_db < 23.0                     # the library figure says "fine"
    g = dres.resolution_gate(J, C)
    assert not g["pass"]
    assert g["off_diagonal_spread_over_resolvable"] < 1.0


def test_the_gate_reads_a_column_vector_and_writes_nothing(tmp_path,
                                                            monkeypatch):
    monkeypatch.chdir(tmp_path)
    J, C = _cvqboost_like(5.0, 5.0)
    assert dres.resolution_gate(J, C.reshape(-1, 1))["pass"]
    assert list(tmp_path.iterdir()) == []


def test_the_gate_can_fail():
    import importlib

    from injection import Mutation, assert_can_fail
    src = Path(dres.__file__)

    def run() -> bool:
        importlib.reload(dres)
        return _gate_holds()

    gate_pass = ('            "pass": bool(s["off_diagonal_resolvable"]\n'
                 '                         and s["linear_resolvable"])}')
    try:
        assert_can_fail([Mutation(src, gate_pass, '            "pass": '
                                  'bool(s["off_diagonal_resolvable"])}',
                                  expect_occurrences=1)],
                        run, "the linear spread ignored")
        assert_can_fail([Mutation(src, gate_pass,
                                  '            "pass": True}',
                                  expect_occurrences=1)],
                        run, "the gate always passes")
    finally:
        importlib.reload(dres)
