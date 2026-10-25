"""F151: the "spread closes" rule, the variants and F130's restatement.

Sprint 28 Task A (#48). Synthetic inputs; the run itself reads ULB and is
not run here.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))

import f151_hgb_cause as fh  # noqa: E402


def test_the_rule_is_the_one_the_plan_fixed():
    assert (fh.SD_MAX, fh.RANGE_MAX, fh.LEVEL_TOL) == (0.03, 0.10, 0.03)
    assert fh.SEEDS == (42, 43, 44, 45, 46)


def test_each_variant_moves_one_setting_except_the_named_combination():
    for name, kw in fh.VARIANTS.items():
        if name == "l2_1p0_no_early_stopping":
            assert len(kw) == 2
        else:
            assert len(kw) <= 1
    assert fh.VARIANTS[fh.REFERENCE_VARIANT] == {"l2_regularization": 1.0}


def test_a_stable_but_low_comparator_does_not_close():
    # F130's "no early stopping": tight spread at the wrong level.
    r = fh.spread_closes([0.20, 0.25, 0.21, 0.21, 0.22], level=0.816)
    assert r["sd_ok"] and r["range_ok"] and not r["level_ok"]
    assert not r["closes"]


def test_a_wide_spread_at_the_right_level_does_not_close():
    r = fh.spread_closes([0.70, 0.90, 0.80, 0.85, 0.83], level=0.816)
    assert r["level_ok"] and not r["closes"]


def test_the_sd_term_alone_stops_a_close():
    # Range 0.09 (passes) and the right level; only the SD (about 0.045)
    # fails. Dropping the SD term from `closes` turns this green.
    r = fh.spread_closes([0.77, 0.77, 0.86, 0.86, 0.82], level=0.816)
    assert r["range_ok"] and r["level_ok"] and not r["sd_ok"]
    assert not r["closes"]


def test_a_tight_spread_at_the_right_level_closes():
    r = fh.spread_closes([0.80, 0.82, 0.79, 0.81, 0.80], level=0.816)
    assert r["closes"]


def test_the_reference_level_reads_five_matched_rows():
    rows = [{"config_hash": fh.XGB_MATCHED13, "seed": s, "protocol": "stratified",
             "metrics": {"auprc": 0.8}} for s in fh.SEEDS]
    assert fh.reference_level(rows) == pytest.approx(0.8)
    with pytest.raises(ValueError):
        fh.reference_level(rows[:4])


def test_f130_is_restated_against_the_reference_by_seed():
    # The reference differs by seed, so a delta taken against the wrong
    # seed's reference changes the answer.
    f151 = [{"variant": fh.REFERENCE_VARIANT, "seed": s, "test_auprc": 0.7 + 0.02 * i}
            for i, s in enumerate(fh.SEEDS)]
    f130 = {"ulb_full": {"rows": [{"variant": "knn", "seed": s,
                                   "test_auprc": 0.7 + 0.02 * i - 0.01}
                                  for i, s in enumerate(fh.SEEDS)]}}
    r = fh.restate_f130(f151, f130)["variants"]["knn"]
    assert r["mean_delta_vs_stable_hgb"] == pytest.approx(-0.01)
    assert r["per_seed"] == pytest.approx([-0.01] * 5)
