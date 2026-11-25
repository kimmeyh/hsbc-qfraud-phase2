"""F198 (Sprint 34 Task F): the extended readings' assembly and
completeness, on small built problems. Each term proven red."""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import f198_extended as fx  # noqa: E402

MODULE = ROOT / "experiments" / "phase2" / "src" / "f198_extended.py"
THIS = Path(__file__).relative_to(ROOT).as_posix()

J2 = np.eye(2)
C2 = np.array([-0.40, -0.41])


def test_a_setting_row_carries_all_three_readings():
    s = fx.setting_row(J2, C2, [0], {"other": [1]}, math.inf)
    assert s["kept"] and s["delivers"] and s["release_passes"]
    assert s["release_pick"] == "other"
    coarse = fx.setting_row(J2, C2, [0], {"other": [1]}, 2.0)
    assert not coarse["kept"] and not coarse["release_passes"]


def _row(factor=1.0, n_r=len(fx.RANGES), passes=False):
    return {"seed": 42, "instance": "free", "weight_factor": factor,
            "settings": [{"R": R, "kept": False, "delivers": False,
                          "release_passes": passes and R == 800.0}
                         for R in fx.RANGES[:n_r]]}


def test_the_summary_names_where_a_reading_holds():
    s = fx.summary([_row(10.0, passes=True), _row(0.1)])
    assert s["release_passes_at"] == ["10.0/800/42/free"]
    assert s["kept_at"] == [] and s["delivers_at"] == []


def test_a_result_short_of_a_weight_is_refused():
    with pytest.raises(RuntimeError, match="not complete"):
        fx.extended_doc([_row(f) for f in fx.WEIGHT_FACTORS[:2]], {}, 1)


def test_a_result_short_of_an_r_is_refused():
    rows = [_row(f) for f in fx.WEIGHT_FACTORS]
    rows[1] = _row(1.0, n_r=4)
    with pytest.raises(RuntimeError, match="not complete"):
        fx.extended_doc(rows, {}, 1)


def test_a_complete_result_is_marked_complete():
    doc = fx.extended_doc([_row(f) for f in fx.WEIGHT_FACTORS], {}, 1)
    assert doc["complete"] is True and doc["ranges"] == list(fx.RANGES)
    with pytest.raises(RuntimeError, match="not complete"):
        fx.extended_doc([], {}, 0)


def test_an_argument_is_refused():
    with pytest.raises(SystemExit, match="usage: f198_extended.py"):
        fx.main(["--run"])


def test_each_term_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    for old, new, test, label in (
            ("    if argv:\n        raise SystemExit(f\"usage: f198",
             "    if False:\n        raise SystemExit(f\"usage: f198",
             "test_an_argument_is_refused",
             "an argument is ignored"),
            ('    if n_instances == 0 or len(rows) != want or any(\n',
             '    if n_instances == 0 or any(\n',
             "test_a_result_short_of_a_weight_is_refused",
             "a missing weight marked complete"),
            ('            len(r["settings"]) != len(RANGES) for r in rows):\n',
             '            False for r in rows):\n',
             "test_a_result_short_of_an_r_is_refused",
             "a missing R marked complete"),
            ("                for r in rows for s in r[\"settings\"] if s[key]]\n",
             "                for r in rows for s in r[\"settings\"]]\n",
             "test_the_summary_names_where_a_reading_holds",
             "every setting listed as holding")):
        assert_can_fail([Mutation(MODULE, old, new, expect_occurrences=1)],
                        lambda test=test: run_pytest(f"{THIS}::{test}", ROOT),
                        label)
