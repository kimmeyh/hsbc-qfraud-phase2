"""F112 (Sprint 27 Task D): the recorded Experiment 1 result follows its rule.

Reads `f112_intervals.json` and writes nothing. The readings (P1 holds, P2
equivalent) must follow from the recorded interval, p-value and margin by
the entry's rule, and the recorded mean must be the mean of the recorded
seeds. Where the untracked prediction files exist, the per-seed deltas are
also recomputed from them; in CI they are absent and that test skips.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))

import f112_intervals as fi      # noqa: E402

DOC = json.loads(fi.OUT.read_text(encoding="utf-8"))


def p1(e: dict) -> bool:
    lo, _ = e["interval_975"]
    return bool(lo > 0 and e["wilcoxon_p_exact"] < DOC["alpha_each"]
                and e["mean_delta_auprc"] > 0)


def p2(e: dict) -> bool:
    lo, hi = e["interval_975"]
    return bool(-DOC["margin"] <= lo and hi <= DOC["margin"])


def test_the_readings_follow_from_the_recorded_figures():
    assert DOC["order"]["p1_holds"] is p1(DOC["order"])
    assert DOC["k"]["p2_equivalent_within_margin"] is p2(DOC["k"])


def test_the_reading_rule_can_fail():
    """Shift the k interval just outside the margin: P2 must flip."""
    e = {**DOC["k"], "interval_975": [DOC["k"]["interval_975"][0],
                                      DOC["margin"] + 1e-6]}
    assert p2(DOC["k"]) and not p2(e)
    o = {**DOC["order"], "wilcoxon_p_exact": DOC["alpha_each"]}
    assert p1(DOC["order"]) and not p1(o)


@pytest.mark.parametrize("eff", list(fi.EFFECTS))
def test_the_recorded_mean_is_the_mean_of_the_seeds(eff):
    e = DOC[eff]
    seeds = [r["seed"] for r in e["per_seed"]]
    assert seeds == list(fi.SEEDS) and e["n_seeds"] == len(fi.SEEDS)
    assert np.isclose(e["mean_delta_auprc"],
                      np.mean([r["delta_auprc"] for r in e["per_seed"]]))


@pytest.mark.skipif(not all((fi.PRED / f"cvqboost_proxy_{h}_stratified_42.npz")
                            .exists() for h in fi.CELLS.values()),
                    reason="prediction files are untracked; absent in CI")
@pytest.mark.parametrize("eff", list(fi.EFFECTS))
def test_the_per_seed_deltas_reproduce_from_the_predictions(eff):
    from sklearn.metrics import average_precision_score
    a, b = fi.EFFECTS[eff]
    for r in DOC[eff]["per_seed"]:
        y, pa = fi.load(a, r["seed"])
        _, pb = fi.load(b, r["seed"])
        assert np.isclose(average_precision_score(y, pa)
                          - average_precision_score(y, pb), r["delta_auprc"])
