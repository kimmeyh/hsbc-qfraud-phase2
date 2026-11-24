"""F197 (Sprint 34 Task G): the saturation check's rules, each term on
built data, each proven red. No data file, no device."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import f197_saturation as fs  # noqa: E402

MODULE = ROOT / "experiments" / "phase2" / "src" / "f197_saturation.py"
THIS = Path(__file__).relative_to(ROOT).as_posix()


def _segment(n=1000, pos=20, perfect=True):
    """`pos` frauds among `n` rows; a perfect score ranks them first."""
    y = np.zeros(n, dtype=int)
    y[:pos] = 1
    s = np.linspace(1, 0, n) if perfect else np.random.default_rng(3).random(n)
    return y, s, np.arange(n)


def test_a_perfect_top_saturates_the_old_measure():
    y, s, idx = _segment()             # 5 alerts, all frauds
    assert fs.most_recall(y, idx) == 5 / 20
    assert fs.old_saturated(y, s, idx)


def test_a_random_score_does_not_saturate_the_old_measure():
    y, s, idx = _segment(perfect=False)
    assert not fs.old_saturated(y, s, idx)


def test_room_is_one_minus_the_minimum_edge():
    assert fs.has_room(0.99) and not fs.has_room(0.995)


def test_a_segment_saturates_only_when_every_seed_does():
    rows = [{"old_saturated": True, "new_room": True, "champion_auprc": 0.5},
            {"old_saturated": False, "new_room": False,
             "champion_auprc": 0.999}]
    r = fs.segment_reading(rows)
    assert not r["old_saturated_on_every_seed"]
    assert not r["new_room_on_every_seed"]
    assert r["max_champion_auprc"] == 0.999


def test_the_reference_must_fire():
    seg = {"C": {"old_saturated_on_every_seed": False,
                 "new_room_on_every_seed": True}}
    s = fs.summary(seg)
    assert not s["reference_can_fire"]
    assert s["finding"].startswith("the reference did not fire")
    seg["C"]["old_saturated_on_every_seed"] = True
    s = fs.summary(seg)
    assert s["reference_can_fire"] and s["new_measure_has_room_on"] == ["C"]


def test_stored_labels_that_differ_stop_the_check():
    y = np.array([0, 1, 0])
    fs.require_same_labels(y, y.copy(), "lightgbm/42")
    import pytest
    with pytest.raises(RuntimeError, match="stored labels differ"):
        fs.require_same_labels(np.array([0, 0, 1]), y, "lightgbm/42")


def _segment_with(n):
    return {"per_seed": [{"old_saturated": True, "new_room": True,
                          "champion_auprc": 0.5}] * n,
            "old_saturated_on_every_seed": True,
            "new_room_on_every_seed": True}


def test_a_result_short_of_a_seed_is_refused():
    import pytest
    ok = fs.saturation_doc({"C": _segment_with(2)}, [{}, {}], 2)
    assert ok["complete"] is True
    for segs, blocks in (({"C": _segment_with(1)}, [{}, {}]),
                         ({"C": _segment_with(2)}, [{}]),
                         ({}, [{}, {}])):
        with pytest.raises(RuntimeError, match="not complete"):
            fs.saturation_doc(segs, blocks, 2)


def test_an_argument_is_refused():
    import pytest
    with pytest.raises(SystemExit, match="usage: f197_saturation.py"):
        fs.main(["--run"])


def test_each_term_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    for old, new, test, label in (
            ("    if not np.array_equal(stored, rebuilt):\n",
             "    if False:\n",
             "test_stored_labels_that_differ_stop_the_check",
             "differing labels pass"),
            ("    if argv:\n        raise SystemExit(f\"usage: f197",
             "    if False:\n        raise SystemExit(f\"usage: f197",
             "test_an_argument_is_refused",
             "an argument is ignored"),
            ("    if (not segments or n_seeds == 0 or len(blocks) != n_seeds\n",
             "    if (False\n",
             "test_a_result_short_of_a_seed_is_refused",
             "a short result marked complete"),
            ("    return e5.recall_at_budget(y, s, idx) >= most_recall(y, idx)\n",
             "    return True\n",
             "test_a_random_score_does_not_saturate_the_old_measure",
             "every segment read as saturated"),
            ("    return auprc <= 1.0 - MIN_EDGE\n", "    return auprc <= 1.0\n",
             "test_room_is_one_minus_the_minimum_edge",
             "room read without the minimum edge"),
            ('    return {"old_saturated_on_every_seed": all(r["old_saturated"]\n',
             '    return {"old_saturated_on_every_seed": any(r["old_saturated"]\n',
             "test_a_segment_saturates_only_when_every_seed_does",
             "one seed read as every seed"),
            ("    can_fire = bool(old)\n", "    can_fire = True\n",
             "test_the_reference_must_fire", "a reference that cannot fail")):
        assert_can_fail([Mutation(MODULE, old, new, expect_occurrences=1)],
                        lambda test=test: run_pytest(f"{THIS}::{test}", ROOT),
                        label)
