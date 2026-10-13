"""F29's verdict and subsample are computed the way the plan stated in advance.

Sprint 25 Task E. The premise falsifier (every subsample's weights at cosine
0.99 or more with the full-fold weights) was written into the plan before the
run. These guards pin the threshold, the verdict arithmetic and the stratified
subsample on synthetic inputs: zero metered, no dataset, nothing written to an
evidence directory.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))

import sample_size as ss     # noqa: E402


def _rows(cosines):
    rows = [{"fraction": 1.0, "cosine_to_full": 1.0, "test_auprc": 0.8,
             "n_train_rows": 1000}]
    for c in cosines:
        rows.append({"fraction": 0.5, "cosine_to_full": c, "test_auprc": 0.79,
                     "n_train_rows": 500})
    return rows


def test_the_threshold_is_the_one_stated_in_the_plan():
    assert ss.COSINE_THRESHOLD == 0.99


def test_insensitive_only_when_every_subsample_clears_the_threshold():
    assert ss.summarize(_rows([0.995, 0.999]))["insensitive"] is True
    s = ss.summarize(_rows([0.995, 0.989]))
    assert s["insensitive"] is False
    assert s["worst_subsample_cosine"] == pytest.approx(0.989)


def test_the_full_fold_rows_do_not_decide_the_verdict():
    # Full-fold rows are cosine 1.0 by construction; counting them would hide
    # a failing subsample behind a perfect self-comparison.
    s = ss.summarize(_rows([0.5]))
    assert s["insensitive"] is False
    assert s["worst_subsample_cosine"] == pytest.approx(0.5)


def test_no_subsample_rows_is_not_a_pass():
    assert ss.summarize(_rows([]))["insensitive"] is False


def test_the_subsample_is_stratified_and_deterministic():
    y = np.array([0] * 900 + [1] * 100)
    idx = ss.stratified_rows(y, 0.25, seed=42)
    assert len(idx) == 250
    assert int(y[idx].sum()) == 25
    assert np.array_equal(idx, ss.stratified_rows(y, 0.25, seed=42))
    assert np.array_equal(ss.stratified_rows(y, 1.0, seed=42), np.arange(1000))


def test_the_centered_metrics_see_what_the_plain_cosine_hides():
    # The code review's example: two weight vectors near uniform whose
    # non-uniform parts are orthogonal. Plain cosine 0.990; centered 0.
    n = 78
    u = np.full(n, 1.0 / n)
    d1 = np.zeros(n); d1[0], d1[1] = 1, -1
    d2 = np.zeros(n); d2[2], d2[3] = 1, -1
    scale = 0.1 * np.linalg.norm(u) / np.linalg.norm(d1)
    wa, wb = u + scale * d1, u + scale * d2
    assert ss.cosine(wa, wb) > 0.99
    c = ss.centered(wa, wb)
    assert c["centered_cosine"] == pytest.approx(0.0, abs=1e-12)
    assert c["relative_distance"] == pytest.approx(np.sqrt(2.0))


def test_pinned_is_reported_beside_the_verdict():
    rows = _rows([0.999])
    for r in rows:
        r["cosine_to_uniform"] = 0.9999
    s = ss.summarize(rows)
    assert s["insensitive"] is True and s["pinned_at_uniform"] is True


def test_cosine_of_a_zero_vector_is_refused():
    with pytest.raises(ValueError):
        ss.cosine(np.zeros(3), np.ones(3))
