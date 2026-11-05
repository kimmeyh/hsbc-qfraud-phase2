"""F114 (Sprint 31 Task E, #97): the shuffled-label check, the seed
count, the calibration warning and the reading, each term proven red.

No model is fit here: `summarize` is fed hand-built rows.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
PHASE2 = ROOT / "experiments" / "phase2" / "src"
SRC = PHASE2 / "f114_real_ceiling.py"
THIS = Path(__file__).relative_to(ROOT).as_posix()
sys.path.insert(0, str(PHASE2))

import f114_real_ceiling as f114  # noqa: E402


def _row(ds, seed, est, achieved, q=0.0017):
    return {"dataset": ds, "seed": seed, "estimate": est,
            "achieved_error": achieved, "consistency_gap": est - achieved,
            "auprc": 0.8, "test_fraud_rate": q}


def test_the_check_uses_the_entrys_margin():
    # q = 0.0017: margin max(0.0005, 0.00017) = 0.0005.
    assert f114.check_passes(0.0017 + 0.0005, 0.0017)
    assert not f114.check_passes(0.0017 + 0.00051, 0.0017)
    assert not f114.check_passes(0.0017 - 0.00051, 0.0017)
    # q = 0.035: margin 0.0035, the relative term.
    assert f114.check_passes(0.035 + 0.0034, 0.035)
    assert not f114.check_passes(0.035 + 0.0036, 0.035)


def test_the_seed_count_follows_seed_42s_time():
    assert f114.seed_count(1.0) == 10          # 60 fit, capped at 10
    assert f114.seed_count(8.0) == 7           # floor(60 / 8)
    assert f114.seed_count(30.0) == 5          # floor 2, raised to 5


def test_a_failed_check_reports_no_ceiling():
    rows = [_row("ulb", 42 + i, 0.0015, 0.0006) for i in range(5)]
    s = f114.summarize({"pass": False}, rows)
    assert s["ceilings_reported"] is False
    assert s["reading"].startswith("check failed")
    s = f114.summarize({"pass": True}, rows)
    assert s["ceilings_reported"] is True
    assert s["reading"].startswith("check passed")
    assert f114.summarize(None, rows)["ceilings_reported"] is False


def test_a_gap_whose_interval_excludes_zero_is_a_warning():
    off = [_row("ulb", 42 + i, 0.0015 + i * 1e-5, 0.0006) for i in range(5)]
    on = [_row("ulb", 42 + i, 0.0006 + (-1) ** i * 1e-4, 0.0006)
          for i in range(5)]
    assert f114.summarize({"pass": True}, off)["by_dataset"]["ulb"][
        "calibration_warning"] is True
    assert f114.summarize({"pass": True}, on)["by_dataset"]["ulb"][
        "calibration_warning"] is False


def test_the_check_is_saved_before_any_seed(tmp_path, monkeypatch):
    """Through the real writer: the check's save names its seed. The run of
    2026-11-05 crashed here, because the first save had no seed rows and
    `provenance.record` refuses an empty seed list."""
    import json

    monkeypatch.setattr(f114, "OUT", tmp_path / "f114.json")
    check = {"dataset": "ulb", "seed": 42, "estimate": 0.0011,
             "test_fraud_rate": 0.0017, "margin": 0.0005, "pass": False}
    monkeypatch.setattr(f114, "shuffle_check", lambda: dict(check))

    def stop(ds, seed):
        raise KeyboardInterrupt("stopped after the check")
    monkeypatch.setattr(f114, "seed_row", stop)
    try:
        f114.main()
    except KeyboardInterrupt:
        pass
    doc = json.loads(f114.OUT.read_text(encoding="utf-8"))
    assert doc["check"] == check and doc["rows"] == []
    assert doc["provenance"]["seeds"] == [42]
    assert doc["complete"] is False


def test_the_seeds_recorded_include_the_check():
    assert f114.seeds_used({"rows": [], "check": None}) == []
    assert f114.seeds_used({"rows": [], "check": {"pass": False}}) == [42]
    assert f114.seeds_used({"rows": [{"seed": 43}, {"seed": 43}],
                            "check": {"pass": True}}) == [42, 43]


def test_lr05_uses_its_estimator_and_writes_only_its_own_file(
        tmp_path, monkeypatch):
    """The F114 re-run amendment, stage 2, through the real writer, stopped
    after the check: the default result is never touched."""
    import json
    for name in ("OUT", "ESTIMATOR", "TRAIN_AUPRC", "RECORD"):
        monkeypatch.setattr(f114, name, getattr(f114, name))
    monkeypatch.setattr(f114, "OUT", tmp_path / "default.json")
    monkeypatch.setattr(f114, "OUT_LR05", tmp_path / "lr05.json")
    monkeypatch.setattr(f114, "shuffle_check", lambda: {
        "dataset": "ulb", "seed": 42, "estimate": 0.0017,
        "test_fraud_rate": 0.0017, "margin": 0.0005, "pass": True})

    def stop(ds, seed):
        raise KeyboardInterrupt("stopped after the check")
    monkeypatch.setattr(f114, "seed_row", stop)
    try:
        f114.main(["--lr05"])
    except KeyboardInterrupt:
        pass
    assert [p.name for p in tmp_path.iterdir()
            if not p.name.startswith("lr05.json")] == []
    doc = json.loads((tmp_path / "lr05.json").read_text(encoding="utf-8"))
    assert doc["estimator"] == "f169_plugin_bins.make('lgbm_lr05', seed)"
    assert doc["entry"].endswith("(F114 re-run)")
    assert f114.TRAIN_AUPRC is True
    assert f114.RECORD == "f114lr05"   # D13: never the first run's stem
    assert f114.main(["--lr5"]) == 2


def test_the_training_auprc_is_recorded_in_lr05(monkeypatch):
    class Model:
        def predict_proba(self, X):
            p = np.asarray(X, dtype=float)[:, 0]
            return np.column_stack([1 - p, p])
    X = np.array([[0.1], [0.9], [0.2], [0.8]])
    y = np.array([0, 1, 0, 1])
    monkeypatch.setitem(f114.LOADERS, "ulb", lambda seed: {
        "Xtr": X, "ytr": y, "Xte": X, "yte": y})
    monkeypatch.setattr(f114, "fit_plugin", lambda Xtr, ytr, seed: Model())
    # The real record saves test scores under predictions/: never here.
    import outcome_record
    names = []
    monkeypatch.setattr(outcome_record, "record",
                        lambda name, *a, **k: names.append(name) or {})
    monkeypatch.setattr(f114, "TRAIN_AUPRC", False)
    assert "train_auprc" not in f114.seed_row("ulb", 42)
    monkeypatch.setattr(f114, "TRAIN_AUPRC", True)
    assert f114.seed_row("ulb", 42)["train_auprc"] == 1.0
    # D13: the score files are named by the mode's own stem.
    monkeypatch.setattr(f114, "RECORD", "f114lr05")
    f114.seed_row("ulb", 42)
    assert names == ["f114_ulb", "f114_ulb", "f114lr05_ulb"]


def test_the_rules_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest

    def test(name):
        return lambda: run_pytest(f"{THIS}::{name}", ROOT)
    assert_can_fail([Mutation(SRC,
                              "    return abs(estimate - q) <= margin(q)\n",
                              "    return abs(estimate - q) <= 2 * "
                              "margin(q)\n", expect_occurrences=1)],
                    test("test_the_check_uses_the_entrys_margin"),
                    "a check twice as loose as the entry")
    assert_can_fail([Mutation(SRC, "MIN_SEEDS = 5\n", "MIN_SEEDS = 3\n",
                              expect_occurrences=1)],
                    test("test_the_seed_count_follows_seed_42s_time"),
                    "a seed floor under 5")
    assert_can_fail([Mutation(SRC, "BUDGET_MIN = 60\n", "BUDGET_MIN = 120\n",
                              expect_occurrences=1)],
                    test("test_the_seed_count_follows_seed_42s_time"),
                    "a 120-minute budget")
    assert_can_fail([Mutation(SRC,
                              "            \"ceilings_reported\": bool(check "
                              "and check[\"pass\"])}\n",
                              "            \"ceilings_reported\": True}\n",
                              expect_occurrences=1)],
                    test("test_a_failed_check_reports_no_ceiling"),
                    "a ceiling reported after a failed check")
    assert_can_fail([Mutation(SRC,
                              "                       gap[\"ci95\"] and "
                              "(gap[\"ci95\"][0] > 0\n",
                              "                       False and "
                              "(gap[\"ci95\"][0] > 0\n",
                              expect_occurrences=1)],
                    test("test_a_gap_whose_interval_excludes_zero_is_a_"
                         "warning"),
                    "a calibration gap left unflagged")
    assert_can_fail([Mutation(SRC,
                              "    if state.get(\"check\") is not None and "
                              "CHECK_SEED not in seeds:\n",
                              "    if False:\n", expect_occurrences=1)],
                    test("test_the_check_is_saved_before_any_seed"),
                    "the check's save with no seed")
    assert_can_fail([Mutation(SRC,
                              "        OUT, ESTIMATOR, TRAIN_AUPRC = OUT_LR05, "
                              "\"lgbm_lr05\", True\n",
                              "        OUT, ESTIMATOR, TRAIN_AUPRC = OUT, "
                              "\"lgbm_lr05\", True\n",
                              expect_occurrences=1)],
                    test("test_lr05_uses_its_estimator_and_writes_only_its_"
                         "own_file"),
                    "stage 2 written over the default result")
    assert_can_fail([Mutation(SRC,
                              "        OUT, ESTIMATOR, TRAIN_AUPRC = OUT_LR05, "
                              "\"lgbm_lr05\", True\n",
                              "        OUT, ESTIMATOR, TRAIN_AUPRC = OUT_LR05, "
                              "\"lgbm_bins\", True\n",
                              expect_occurrences=1)],
                    test("test_lr05_uses_its_estimator_and_writes_only_its_"
                         "own_file"),
                    "stage 2 run with the old estimator")
    assert_can_fail([Mutation(SRC, "    if TRAIN_AUPRC:\n", "    if False:\n",
                              expect_occurrences=1)],
                    test("test_the_training_auprc_is_recorded_in_lr05"),
                    "the training AUPRC left out")
    assert_can_fail([Mutation(SRC, '        RECORD = "f114lr05"\n',
                              "        pass\n", expect_occurrences=1)],
                    test("test_lr05_uses_its_estimator_and_writes_only_its_"
                         "own_file"),
                    "the re-run recording under the first run's name")
    assert_can_fail([Mutation(SRC, 'orec.record(f"{RECORD}_{dataset}"',
                              'orec.record(f"f114_{dataset}"',
                              expect_occurrences=1)],
                    test("test_the_training_auprc_is_recorded_in_lr05"),
                    "seed rows ignoring the mode's record name")
