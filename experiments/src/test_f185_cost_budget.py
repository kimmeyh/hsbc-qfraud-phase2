"""F185 (Sprint 32 Task D): the cost-weighted budget's join, its two
rankings, the check and each refusal, on small built data. No dataset,
no device. Each rule's term is proven red below."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import f185_cost_budget as fc  # noqa: E402
import outcome_record as orec  # noqa: E402

MODULE = ROOT / "experiments" / "phase2" / "src" / "f185_cost_budget.py"
THIS = Path(__file__).relative_to(ROOT).as_posix()


# ----------------------------------------------------------- the join
def test_aligned_rows_are_joined():
    y, s, a = fc.joined([0, 1], [0.2, 0.9], [0, 1], [3.0, 4.0])
    assert list(y) == [0, 1] and list(a) == [3.0, 4.0]


def test_a_label_that_differs_is_refused():
    with pytest.raises(fc.Refused, match="1 labels differ"):
        fc.joined([0, 1, 0], [0.1, 0.2, 0.3], [0, 1, 1], [1.0, 1.0, 1.0])


def test_a_shape_that_differs_is_refused():
    with pytest.raises(fc.Refused, match="shapes differ"):
        fc.joined([0, 1], [0.1, 0.2], [0, 1, 0], [1.0, 1.0])
    with pytest.raises(fc.Refused, match="shapes differ"):
        fc.joined([0, 1], [0.1, 0.2], [0, 1], [1.0])
    with pytest.raises(fc.Refused, match="shapes differ"):
        fc.joined([0, 1], [0.1], [0, 1], [1.0, 1.0])


def test_a_bad_amount_is_refused():
    for bad in (np.nan, np.inf, -1.0):
        with pytest.raises(fc.Refused, match="amount"):
            fc.joined([0, 1], [0.1, 0.2], [0, 1], [1.0, bad])


def _stored(tmp_path: Path) -> dict:
    p = tmp_path / "s.npz"
    np.savez(p, y_test=np.array([0, 1]), p_test=np.array([0.1, 0.9]))
    return {"test_scores": {"path": str(p), "sha256": orec.sha256_of(p)}}


def test_a_stored_file_with_its_hash_is_read(tmp_path):
    y, p = fc.checked_scores(_stored(tmp_path))
    assert list(y) == [0, 1] and list(p) == [0.1, 0.9]


def test_a_stored_file_with_another_hash_is_refused(tmp_path):
    block = _stored(tmp_path)
    block["test_scores"]["sha256"] = "0" * 64
    with pytest.raises(fc.Refused, match="SHA-256 differs"):
        fc.checked_scores(block)


def test_a_missing_stored_file_is_refused(tmp_path):
    block = {"test_scores": {"path": str(tmp_path / "gone.npz"),
                             "sha256": "0" * 64}}
    with pytest.raises(fc.Refused, match="not on disk"):
        fc.checked_scores(block)


# ----------------------------------------------------------- the reading
Y = np.array([1, 1, 0, 0] + [0] * 396)
S = np.array([0.9, 0.5, 0.8, 0.1] + [0.0] * 396)
A = np.array([10.0, 1000.0, 50.0, 5.0] + [1.0] * 396)


def test_the_score_ranking_flags_the_top_k_and_counts_dollars():
    r = fc.ranking(Y, S, A)        # k = 2: rows 0 and 2
    assert r["n_flagged"] == 2
    assert r["confusion"] == {"tn": 397, "fp": 1, "fn": 1, "tp": 1}
    assert r["dollars_caught"] == 10.0 and r["dollars_missed"] == 1000.0
    assert r["net_savings"]["10.0"] == 10.0 - 2 * 10.0


def test_the_expected_loss_ranking_catches_the_large_fraud():
    c = fc.compare(Y, S, A)        # s x A: 9, 500, 40, 0.5; k = 2
    assert c["by_expected_loss"]["dollars_caught"] == 1000.0
    assert c["dollars_gain"] == 990.0


def test_hoppner_counts_alerts_above_cost_over_amount():
    # s x A = 9, 500, 40, 0.5, then 0 for the rest
    assert fc.hoppner_alerts(S, A) == {"5.0": 3, "10.0": 2, "25.0": 2}
    assert fc.hoppner_alerts([0.9], [0.0]) == {"5.0": 0, "10.0": 0,
                                               "25.0": 0}


def test_the_check_fires():
    c = fc.can_fire()
    assert c["can_fire"] and c["by_loss_caught"] > c["by_score_caught"]


def test_the_label_flip_check_fires():
    assert fc.refusal_fires() == {"label_flip_refused": True}


def test_an_unfired_check_is_refused():
    fc.require_fired({"can_fire": True, "label_flip_refused": True})
    for bad in ({"can_fire": False, "label_flip_refused": True},
                {"can_fire": True, "label_flip_refused": False}):
        with pytest.raises(RuntimeError, match="did not fire"):
            fc.require_fired(bad)


def _ds(n: int) -> dict:
    return {"rows": [{}] * n}


def test_a_short_result_is_refused():
    with pytest.raises(RuntimeError, match="incomplete"):
        fc.final_doc({}, {"ulb": _ds(10), "ieee_cis": _ds(9)})
    with pytest.raises(RuntimeError, match="incomplete"):
        fc.final_doc({}, {"ulb": _ds(10)})
    assert fc.final_doc({}, {"ulb": _ds(10), "ieee_cis": _ds(10)})[
        "complete"] is True


def test_the_interval_needs_two_seeds():
    assert fc.t_interval([1.0])["t95"] is None
    t = fc.t_interval([1.0, 2.0, 3.0])
    assert t["mean"] == 2.0 and t["t95"][0] < 2.0 < t["t95"][1]


# ------------------------------------------------------------- red proofs

def test_each_rule_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    for old, new, test, label in (
            ("    if not np.array_equal(y_s, y_r):\n", "    if False:\n",
             "test_a_label_that_differs_is_refused", "a misaligned join"),
            ("    if y_s.shape != y_r.shape or a.shape != y_s.shape \\\n",
             "    if False and a.shape != y_s.shape \\\n",
             "test_a_shape_that_differs_is_refused", "another shape joined"),
            ("    if not np.all(np.isfinite(a)) or (a < 0).any():\n",
             "    if False:\n",
             "test_a_bad_amount_is_refused", "a bad amount joined"),
            ('    if orec.sha256_of(path) != src["sha256"]:\n',
             "    if False:\n",
             "test_a_stored_file_with_another_hash_is_refused",
             "another file read"),
            ("    if not path.exists():\n", "    if False:\n",
             "test_a_missing_stored_file_is_refused",
             "a missing file not named"),
            ("    caught = float(amounts[flagged & fraud].sum())\n",
             "    caught = float(amounts[flagged].sum())\n",
             "test_the_score_ranking_flags_the_top_k_and_counts_dollars",
             "legitimate dollars counted as caught"),
            ("    by_loss = ranking(y, scores * amounts, amounts)\n",
             "    by_loss = ranking(y, scores, amounts)\n",
             "test_the_expected_loss_ranking_catches_the_large_fraud",
             "the loss ranking is the score ranking"),
            ("    return {str(c): int((loss > c).sum()) for c in costs}\n",
             "    return {str(c): int((loss >= 0).sum()) for c in costs}\n",
             "test_hoppner_counts_alerts_above_cost_over_amount",
             "the cost ignored"),
            ('"can_fire": bool(c["dollars_gain"] > 0)}',
             '"can_fire": bool(c["dollars_gain"] < 0)}',
             "test_the_check_fires", "the check's direction inverted"),
            ("        return {\"label_flip_refused\": True}\n",
             "        return {\"label_flip_refused\": False}\n",
             "test_the_label_flip_check_fires", "the flip check inverted"),
            ('    if not (check["can_fire"] and check["label_flip_refused"]):\n',
             "    if False:\n",
             "test_an_unfired_check_is_refused", "an unfired check read"),
            ("    if short or set(datasets) != set(SOURCES):\n",
             "    if False:\n",
             "test_a_short_result_is_refused", "a short result complete"),
            ("    if n < 2:\n", "    if False:\n",
             "test_the_interval_needs_two_seeds",
             "an interval from one seed")):
        assert_can_fail([Mutation(MODULE, old, new, expect_occurrences=1)],
                        lambda test=test: run_pytest(f"{THIS}::{test}", ROOT),
                        label)
