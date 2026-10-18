"""F109 (Sprint 27 Task G): the ladder's own pieces. Tier 1 itself is
F103's code and is tested in `test_f103_tier1.py`.

Synthetic data only; nothing written.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "src"))

import f109_ladder as fl         # noqa: E402


def test_subsample_keeps_positives_up_to_the_cap():
    y = np.zeros(100_000, dtype=int)
    y[:500] = 1
    S = fl.subsample(y, 0)
    assert len(S) == fl.N_SUB and y[S].sum() == 500
    y[:5000] = 1
    S = fl.subsample(y, 0)
    assert y[S].sum() == fl.MAX_POS and len(np.unique(S)) == fl.N_SUB


def test_top_phases_selects_on_training_rows_and_skips_constants():
    rng = np.random.default_rng(1)
    n = 4000
    y = (rng.uniform(size=n) < 0.3).astype(int)
    X = pd.DataFrame({f"noise{i}": rng.normal(size=n) for i in range(8)})
    X["signal"] = y + 0.3 * rng.normal(size=n)
    X["const"] = 1.0
    X.loc[::7, "noise0"] = np.nan
    tr = np.arange(3000)
    P, feats = fl.top_phases(X, y, tr, 0)
    assert feats[0] == "signal" and "const" not in feats
    assert P.shape == (n, fl.D_TOP)
    assert np.isfinite(P).all() and P.min() > -np.pi and P.max() < np.pi


def test_summary_counts_the_falsifier():
    def row(g4):
        return {"gates": {"tier1": "candidate", "g1_rho_off": 0.8,
                          "g2_gam_auc": 0.9, "g3_hgb_minus_gam": 0.05,
                          "g4_joint_minus_ga2m": g4, "g5_qubits_q1": 6}}
    s = fl.summarize({"datasets": {"ulb": [row(0.0), row(0.03), row(0.02)]}})
    assert s["falsifier_g4_large"] == {"ulb": 2}
