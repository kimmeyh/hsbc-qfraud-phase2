"""F166 (Sprint 29 Task F, #69): the seed rule, the selection, the ranking
test's choice and the parallel-build gate, each proven red.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
PHASE2 = ROOT / "experiments" / "phase2" / "src"
THIS = Path(__file__).relative_to(ROOT).as_posix()
sys.path.insert(0, str(PHASE2))

import f166_ulb_algorithms as fu  # noqa: E402


def test_every_classical_grid_holds_eight_and_the_proxy_three():
    for algo in ("hgb", "lightgbm", "xgboost", "catboost", "logreg", "svm"):
        assert len(fu.GRIDS[algo]) == 8, algo
    assert [g["config"] for g in fu.GRIDS["proxy"]] == ["free", "mid", "full"]
    assert {"max_depth": 6, "learning_rate": 0.3, "n_estimators": 100} \
        in fu.GRIDS["xgboost"]


def test_the_seed_count_follows_seed_42s_time():
    assert fu.choose_seeds(25.0)["n_seeds"] == 4
    assert fu.choose_seeds(5.0)["n_seeds"] == 10
    slow = fu.choose_seeds(50.0)
    assert slow["n_seeds"] == 3 and slow["over_cap"]
    assert fu.choose_seeds(25.0)["below_section2_five_seeds"]
    assert fu.choose_seeds(25.0)["seeds"] == [42, 43, 44, 45]


def test_selection_takes_the_best_validation_and_the_first_tie():
    tried = [{"val_auprc": 0.5}, {"val_auprc": 0.7}, {"val_auprc": 0.7}]
    assert fu.choose(tried) == 1


def test_the_primary_test_is_chosen_by_seed_count():
    diffs = [0.01] * 8
    wide = np.zeros(2000)                  # a bootstrap that cannot reject
    assert fu.pair_test(diffs, wide, 8)["primary"] == "wilcoxon"
    assert fu.pair_test(diffs, wide, 8)["reading"] == "above"
    assert fu.pair_test(diffs[:4], wide, 4)["primary"] == "bootstrap"
    assert fu.pair_test(diffs[:4], wide, 4)["reading"] == "no reliable difference"


def test_the_parallel_build_needs_a_complete_equal_f159(tmp_path):
    f = tmp_path / "f159.json"
    assert not fu.parallel_ok(f)["use"]
    doc = {"complete": True, "analysis": {"all_equal": True,
                                           "1.0": {"speedup": {"4": 2.0, "8": 3.5}}}}
    f.write_text(json.dumps(doc), encoding="utf-8")
    ok = fu.parallel_ok(f)
    assert ok["use"] and ok["workers"] == 8
    doc["analysis"]["all_equal"] = False
    f.write_text(json.dumps(doc), encoding="utf-8")
    assert not fu.parallel_ok(f)["use"]
    doc["analysis"]["all_equal"], doc["complete"] = True, False
    f.write_text(json.dumps(doc), encoding="utf-8")
    assert not fu.parallel_ok(f)["use"]


def test_operating_point_metrics():
    y = np.array([1, 1, 0, 0, 0, 0])
    p = np.array([0.9, 0.2, 0.8, 0.1, 0.1, 0.1])
    op = fu.op_metrics(y, p, 0.5, "x")
    assert op["confusion"] == {"tn": 3, "fp": 1, "fn": 1, "tp": 1}
    assert op["specificity"] == 0.75
    assert abs(op["balanced_accuracy"] - 0.625) < 1e-12


def test_svm_margins_are_mapped_into_the_unit_interval():
    class M:
        def decision_function(self, X):
            return np.array([-30.0, 0.0, 30.0])
    s = fu.scores(M(), None)
    assert np.all((s >= 0) & (s <= 1)) and np.all(np.diff(s) > 0)


def _fails(old, new, node, label):
    from injection import Mutation, assert_can_fail, run_pytest
    assert_can_fail([Mutation(PHASE2 / "f166_ulb_algorithms.py", old, new,
                              expect_occurrences=1)],
                    lambda: run_pytest(f"{THIS}::{node}", ROOT), label)


def test_the_seed_rule_can_fail():
    _fails("    n = max(MIN_SEEDS, n)\n", "    n = max(1, n)\n",
           "test_the_seed_count_follows_seed_42s_time", "no minimum")


def test_the_selection_can_fail():
    _fails("    return next(i for i, t in enumerate(tried) if t[\"val_auprc\"] == best)\n",
           "    return 0\n",
           "test_selection_takes_the_best_validation_and_the_first_tie",
           "first configuration always")


def test_the_primary_choice_can_fail():
    _fails("    primary = \"wilcoxon\" if n >= WILCOXON_MIN_SEEDS else \"bootstrap\"\n",
           "    primary = \"wilcoxon\"\n",
           "test_the_primary_test_is_chosen_by_seed_count", "Wilcoxon at any n")


def test_the_parallel_gate_can_fail():
    _fails("    if not a.get(\"all_equal\"):\n", "    if False:\n",
           "test_the_parallel_build_needs_a_complete_equal_f159",
           "unequal pools accepted")
