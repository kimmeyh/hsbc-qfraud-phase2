"""F158 (Sprint 29 Task G, #70): the label delay, the shuffled reference,
the primary reading and the step-3 count, each proven red.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
PHASE2 = ROOT / "experiments" / "phase2" / "src"
THIS = Path(__file__).relative_to(ROOT).as_posix()
sys.path.insert(0, str(PHASE2))

import f158_fraud_types as ft  # noqa: E402


def _world():
    """One terminal, one customer, a fraud on day 10 and a row every day."""
    day = np.arange(40)
    y = (day == 10).astype(int)
    return {"customer": np.zeros(40, int), "terminal": np.zeros(40, int),
            "day": day, "time": np.zeros(40), "amount": np.ones(40),
            "mu": np.ones(40), "y_main": y, "n_customers": 1, "n_terminals": 1}


def test_a_label_is_seen_only_after_the_delay():
    X = ft.features(_world())
    col = X[:, ft.FEATURES.index("term_fraud_d14_d8")]
    # Day 10's fraud enters the d-14..d-8 window on day 18 and leaves after 24.
    assert col[17] == 0 and col[18] == 1 and col[24] == 1 and col[25] == 0
    cust = X[:, ft.FEATURES.index("cust_fraud_d35_d8")]
    assert cust[17] == 0 and cust[18] == 1 and cust[39] == 1
    prev = X[:, ft.FEATURES.index("cust_txn_prev_day")]
    assert prev[0] == 0 and np.all(prev[1:] == 1)


def test_the_shuffle_keeps_every_fraud_a_fraud():
    rng = np.random.default_rng(0)
    s2 = rng.random(500) < 0.05
    s3 = rng.random(500) < 0.05
    a, b = ft.shuffled_types(s2, s3, 42)
    assert np.array_equal(a | b, s2 | s3)
    assert a.sum() == s2.sum() and b.sum() == s3.sum()
    assert not (np.array_equal(a, s2) and np.array_equal(b, s3))


def test_eight_positive_seeds_read_above():
    out = ft.paired_test([0.01, 0.02, 0.015, 0.03, 0.012, 0.022, 0.018, 0.025])
    assert out["wilcoxon"]["p"] < 0.01
    assert out["reading"] == "above"


def test_mixed_seeds_read_no_reliable_difference():
    out = ft.paired_test([0.01, -0.02, 0.015, -0.03, 0.012, -0.022, 0.018, 0.0])
    assert out["reading"] == "no reliable difference"


def test_a_fraud_any_family_catches_is_not_missed():
    y = np.array([1, 1, 1, 0])
    m = ft.missed_by_all(y, [np.array([1, 0, 0, 1]), np.array([0, 1, 0, 0])])
    assert m.tolist() == [False, False, True, False]


UP = [0.01, 0.02, 0.015, 0.03, 0.012, 0.022, 0.018, 0.025]
FLAT = [0.0] * 8


def _rows(cascade, shuffled):
    return [{"models": {"single": {"recall_at_budget": 0.5},
                        "cascade": {"recall_at_budget": 0.5 + c},
                        "shuffled": {"recall_at_budget": 0.5 + s}}}
            for c, s in zip(cascade, shuffled)]


def test_step2_needs_the_cascade_above():
    assert ft.summarize(_rows(FLAT, FLAT))["step2_condition_met"] is False


def test_step2_needs_the_shuffled_reference_not_above():
    assert ft.summarize(_rows(UP, UP))["step2_condition_met"] is False


def test_step2_runs_when_both_terms_hold():
    assert ft.summarize(_rows(UP, FLAT))["step2_condition_met"] is True


STEP2 = ("    go = primary[\"reading\"] == \"above\" and "
         "shuffled[\"reading\"] != \"above\"\n")


def test_the_step2_cascade_term_can_fail():
    _fails(STEP2, "    go = shuffled[\"reading\"] != \"above\"\n",
           "test_step2_needs_the_cascade_above", "cascade term dropped")


def test_the_step2_shuffled_term_can_fail():
    _fails(STEP2, "    go = primary[\"reading\"] == \"above\"\n",
           "test_step2_needs_the_shuffled_reference_not_above",
           "shuffled term dropped")


def _fails(old, new, node, label):
    from injection import Mutation, assert_can_fail, run_pytest
    assert_can_fail([Mutation(PHASE2 / "f158_fraud_types.py", old, new,
                              expect_occurrences=1)],
                    lambda: run_pytest(f"{THIS}::{node}", ROOT), label)


def test_the_delay_can_fail():
    _fails("    gap = DELAY + 1\n", "    gap = DELAY\n",
           "test_a_label_is_seen_only_after_the_delay", "label seen a day early")


def test_the_shuffle_can_fail():
    _fails("    a[fraud], b[fraud] = s2[fraud][perm], s3[fraud][perm]\n",
           "    a[fraud], b[fraud] = s2[perm], s3[perm]\n",
           "test_the_shuffle_keeps_every_fraud_a_fraud",
           "types drawn from all rows")


def test_the_reading_can_fail():
    _fails("    if rejects and ci[\"low\"] > 0:\n",
           "    if rejects and ci[\"low\"] > 1:\n",
           "test_eight_positive_seeds_read_above", "above never read")


def test_the_missed_count_can_fail():
    _fails("        caught |= np.asarray(f, bool)\n",
           "        caught &= np.asarray(f, bool)\n",
           "test_a_fraud_any_family_catches_is_not_missed",
           "caught by every family instead of any")
