"""F102 (Sprint 27 Task C): the downsized matched pair follows its rule.

Sprint 27 IMP-3: the script shipped without a test. Known answers for
`pair()`, and every recorded row in `f102_downsized_pair.json` must equal
`pair()` applied to that row's own counts. Reads the result; writes nothing.
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

import f102_downsized_pair as fp      # noqa: E402

SRC = ROOT / "experiments" / "phase2" / "src" / "f102_downsized_pair.py"


def test_a_segment_the_complement_can_already_match():
    r = fp.pair(10, 990, 50, 4950)
    assert (r["positives_per_side"], r["negatives_per_side"]) == (10, 990)
    assert r["feasible"] and r["already_matchable_without_downsizing"]
    assert r["segment_positives_kept"] == 1.0
    assert r["auc_interval_width_ratio_approx"] == 1.0


def test_a_downsized_pair_keeps_the_segment_rate():
    r = fp.pair(50, 950, 20, 2000)
    assert (r["positives_per_side"], r["negatives_per_side"]) == (20, 380)
    assert r["feasible"] and not r["already_matchable_without_downsizing"]
    assert r["segment_positives_kept"] == 0.4
    want = np.sqrt((1 / 20 + 1 / 380) / (1 / 50 + 1 / 950))
    assert r["auc_interval_width_ratio_approx"] == round(float(want), 4)


@pytest.mark.parametrize("args", [(50, 950, 20, 100), (0, 100, 10, 100)])
def test_an_infeasible_pair_reports_no_widening(args):
    r = fp.pair(*args)
    assert not r["feasible"]
    assert r["auc_interval_width_ratio_approx"] is None


def recorded_rows_follow_the_rule() -> bool:
    doc = json.loads(fp.OUT.read_text(encoding="utf-8"))
    for row in doc["rows"]:
        want = fp.pair(row["segment_positives"], row["segment_negatives"],
                       row["complement_positives"],
                       row["complement_negatives"])
        if any(row[k] != v for k, v in want.items()):
            return False
    return bool(doc["rows"])


def test_the_recorded_rows_follow_the_rule():
    assert recorded_rows_follow_the_rule()


def test_the_rule_check_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    node = ("experiments/src/test_f102_downsized_pair.py"
            "::test_the_recorded_rows_follow_the_rule")
    assert_can_fail([Mutation(SRC, "    p = min(seg_pos, comp_pos)",
                              "    p = seg_pos", expect_occurrences=1)],
                    lambda: run_pytest(node, ROOT),
                    "the pair no longer capped by the complement")
