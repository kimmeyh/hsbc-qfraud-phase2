"""F142 readout (Sprint 26 Task D): the band and the pool-identity check."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))
import f142_readout as F  # noqa: E402


def test_the_band_is_the_one_written_before_any_call():
    draft = (ROOT / "experiments" / "phase2" / "PREREGISTRATION_DRAFT.md"
             ).read_text(encoding="utf-8")
    assert f"[{F.BAND[0]}, {F.BAND[1]}]" in draft


def _row(cos_recorded):
    return {"seed": 42, "weight_cosine_vs_classical": cos_recorded,
            "objective_device": 0.0, "objective_proxy_optimum": 0.0,
            "metrics": {"auprc": 0.5},
            "in_segment": {"in_segment": {"auprc": 0.5},
                           "random_control": {"auprc": 0.5}}}


def _patch(monkeypatch, w_exact, w_dev):
    monkeypatch.setattr(F.f126, "exact_weights", lambda c, s: w_exact)
    monkeypatch.setattr(F.f126, "device_best", lambda c, s: w_dev)
    monkeypatch.setattr(F, "_response", lambda row: {"results": {
        "solutions": [list(w_dev)], "energies": [0.0]}})


D3 = {42: {"weight_cosine_vs_classical": 0.9, "metrics": {"auprc": 0.5},
           "in_segment": {"in_segment": {"auprc": 0.5}}}}


def test_a_different_pool_is_refused(monkeypatch):
    """The exact optimum must be the one the row was scored against."""
    w = np.array([0.5, 0.3, 0.2, 0.0])
    _patch(monkeypatch, w, w)
    out = F.b4(_row(1.0), D3)                   # same pool: read
    assert out["dirac3s"]["zeros_shared_with_exact"] == 1
    assert not out["dirac3s"]["in_band"]
    with pytest.raises(SystemExit, match="REFUSING"):
        F.b4(_row(0.95), D3)                    # row scored a different pool
