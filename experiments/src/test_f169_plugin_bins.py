"""F169 (Sprint 30 Task F, #80): the two estimators as the entry sets
them, F108's pass rule and the attribution, each term proven red.

No simulator run here: `summarize` is fed hand-built rows.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PHASE2 = ROOT / "experiments" / "phase2" / "src"
THIS = Path(__file__).relative_to(ROOT).as_posix()
sys.path.insert(0, str(PHASE2))

import f169_plugin_bins as f169  # noqa: E402


def _rows(hgb: list[bool], lgbm: list[bool]) -> list[dict]:
    rows = []
    for i, (h, g) in enumerate(zip(hgb, lgbm)):
        arms = {arm: {"hgb_no_es": {"recovered": h if arm == "none" else True},
                      "lgbm_bins": {"recovered": g if arm == "none" else True}}
                for arm in ("none", "flip", "reference")}
        rows.append({"seed": 42 + i, "arms": arms})
    return rows


ALL, FOUR, THREE = [True] * 5, [True] * 4 + [False], [True] * 3 + [False] * 2


def test_the_estimators_are_set_as_the_entry_says():
    h = f169.make("hgb_no_es", 42)
    assert h.early_stopping is False and h.max_bins == 255
    g = f169.make("lgbm_bins", 42)
    p = g.get_params()
    assert (p["max_bin"], p["n_estimators"], p["learning_rate"],
            p["num_leaves"], p["min_child_samples"]) == (4095, 100, 0.1, 31, 20)


def test_four_of_five_on_the_main_arm_passes_three_does_not():
    s = f169.summarize(_rows(FOUR, THREE))
    assert s["passes"] == {"hgb_no_es": True, "lgbm_bins": False}


def test_a_stopped_seed_counts_as_a_miss():
    rows = _rows(ALL, ALL)
    rows[0] = {"seed": 42, "arms": {}, "stopped": "generator check failed"}
    rows[1]["arms"]["none"]["hgb_no_es"]["recovered"] = False
    s = f169.summarize(rows)
    assert s["by_arm"]["none"]["hgb_no_es"]["seeds_recovered"] == 3
    assert s["by_arm"]["none"]["hgb_no_es"]["n_seeds"] == 5
    assert s["passes"]["hgb_no_es"] is False
    assert s["passes"]["lgbm_bins"] is True       # 4 of 5 live seeds


def test_the_attribution_names_each_case():
    assert f169.summarize(_rows(ALL, ALL))["reading"].startswith("both pass")
    assert f169.summarize(_rows(THREE, ALL))["reading"].startswith(
        "only LightGBM")
    assert f169.summarize(_rows(ALL, THREE))["reading"].startswith(
        "only HGB")
    assert f169.summarize(_rows(THREE, THREE))["reading"].startswith(
        "neither passes")


def _rows_lr05(rec: list[bool]) -> list[dict]:
    return [{"seed": 42 + i,
             "arms": {arm: {"lgbm_lr05": {"recovered": r if arm == "none"
                                          else True}}
                      for arm in ("none", "flip", "reference")}}
            for i, r in enumerate(rec)]


def test_the_lr05_estimator_differs_only_in_its_rate():
    # The F114 re-run amendment, stage 1: half the rate, nothing else.
    a = f169.make("lgbm_bins", 42).get_params()
    b = f169.make("lgbm_lr05", 42).get_params()
    assert b["learning_rate"] == 0.05 and a["learning_rate"] == 0.1
    assert {k: v for k, v in a.items() if k != "learning_rate"} == {
        k: v for k, v in b.items() if k != "learning_rate"}


def test_lr05_needs_four_recovered_and_a_partial_run_never_passes():
    assert f169.summarize_lr05(_rows_lr05(FOUR))["passes"] is True
    assert f169.summarize_lr05(_rows_lr05(THREE))["passes"] is False
    assert f169.summarize_lr05(_rows_lr05([True] * 2))["passes"] is False
    stopped = _rows_lr05(ALL)
    stopped[0] = {"seed": 42, "arms": {}, "stopped": "generator check failed"}
    stopped[1]["arms"]["none"]["lgbm_lr05"]["recovered"] = False
    assert f169.summarize_lr05(stopped)["passes"] is False


def test_lr05_writes_only_its_own_file(tmp_path, monkeypatch):
    """Through the real writer, with the simulator stubbed: the default
    result is never touched, and only `lgbm_lr05` is fit."""
    import json
    monkeypatch.setattr(f169, "OUT", tmp_path / "default.json")
    monkeypatch.setattr(f169, "OUT_LR05", tmp_path / "lr05.json")
    asked = []

    def fake(seed, estimators):
        asked.append(estimators)
        return _rows_lr05([True])[0] | {"seed": seed}
    monkeypatch.setattr(f169, "seed_run", fake)
    assert f169.main(["lr05"]) == 0
    assert not (tmp_path / "default.json").exists()
    assert [p.name for p in tmp_path.iterdir()
            if not p.name.startswith("lr05.json")] == []
    doc = json.loads((tmp_path / "lr05.json").read_text(encoding="utf-8"))
    assert set(asked) == {("lgbm_lr05",)}
    assert list(doc["estimators"]) == ["lgbm_lr05"]
    assert doc["complete"] is True and doc["summary"]["passes"] is True
    assert f169.main(["lr5"]) == 2


def test_the_rule_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    src = PHASE2 / "f169_plugin_bins.py"

    def test(name):
        return lambda: run_pytest(f"{THIS}::{name}", ROOT)
    assert_can_fail([Mutation(src, "                        >= min(fc.PASS_"
                              "SEEDS, len(rows))}\n",
                              "                        >= 3}\n",
                              expect_occurrences=1)],
                    test("test_four_of_five_on_the_main_arm_passes_three_"
                         "does_not"),
                    "three of five counted as a pass")
    assert_can_fail([Mutation(src, '                        "n_seeds": '
                              'len(rows),\n',
                              '                        "n_seeds": len(live),\n',
                              expect_occurrences=1)],
                    test("test_a_stopped_seed_counts_as_a_miss"),
                    "a stopped seed dropped from the count")
    assert_can_fail([Mutation(src, '                                        '
                              '      early_stopping=False)\n',
                              "                                              )\n",
                              expect_occurrences=1)],
                    test("test_the_estimators_are_set_as_the_entry_says"),
                    "HGB left with early stopping on")
    assert_can_fail([Mutation(src, '    elif passes["lgbm_bins"]:\n',
                              '    elif passes["hgb_no_es"]:\n',
                              expect_occurrences=1)],
                    test("test_the_attribution_names_each_case"),
                    "the attribution swapped")
    assert_can_fail([Mutation(src, "LR05 = 0.05\n", "LR05 = 0.1\n",
                              expect_occurrences=1)],
                    test("test_the_lr05_estimator_differs_only_in_its_rate"),
                    "the re-run estimator at the old rate")
    assert_can_fail([Mutation(src, '                    "recovers": rec >= '
                              'fc.PASS_SEEDS}\n',
                              '                    "recovers": rec >= '
                              'min(fc.PASS_SEEDS, len(rows))}\n',
                              expect_occurrences=1)],
                    test("test_lr05_needs_four_recovered_and_a_partial_run_"
                         "never_passes"),
                    "a two-seed partial run read as a pass")
    assert_can_fail([Mutation(src, "    rid, resume = provenance.start("
                              "OUT_LR05)\n",
                              "    rid, resume = provenance.start(OUT)\n",
                              expect_occurrences=1)],
                    test("test_lr05_writes_only_its_own_file"),
                    "stage 1 started on the default result")
