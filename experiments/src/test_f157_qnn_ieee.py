"""F157 QNN part (Sprint 31 Task G, #99): the rows the entry sets, the
seed plan, and F106's rules imported unchanged, each term proven red.

No circuit is trained here: the row draw runs on a synthetic label
vector.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
PHASE2 = ROOT / "experiments" / "phase2" / "src"
SRC = PHASE2 / "f157_qnn_ieee.py"
THIS = Path(__file__).relative_to(ROOT).as_posix()
sys.path.insert(0, str(PHASE2))

import f106_dequant as f106  # noqa: E402
import f157_qnn_ieee as g  # noqa: E402


def _labels(n=100_000, rate=0.035, seed=0):
    y = np.zeros(n, dtype=int)
    y[np.random.default_rng(seed).choice(n, int(n * rate), replace=False)] = 1
    return y


def test_the_training_and_validation_rows_are_the_entrys():
    y = _labels()
    tr, va = g.draw_rows(y, 42)
    assert (int(y[tr].sum()), int((y[tr] == 0).sum())) == (295, 6000)
    assert len(va) == 20_000
    assert not set(tr) & set(va)
    # Stratified: the validation rate is the rest's rate, to one row.
    rest = np.setdiff1d(np.arange(len(y)), tr)
    assert abs(int(y[va].sum()) - 20_000 * y[rest].mean()) <= 1
    # Seeded: the same seed draws the same rows, another seed does not.
    assert np.array_equal(g.draw_rows(y, 42)[0], tr)
    assert not np.array_equal(g.draw_rows(y, 43)[0], tr)


def test_the_seed_plan_keeps_eight_under_four_hours():
    assert g.seed_plan(1_000.0)["n_seeds"] == 8        # 8,000 s
    cut = g.seed_plan(2_500.0)                           # 20,000 s
    assert (cut["n_seeds"], cut["cut"]) == (5, True)     # floor 5.76
    assert g.seed_plan(4_000.0)["n_seeds"] == 5          # floor 3, raised


def test_f106s_rules_are_imported_unchanged():
    assert g.SEEDS == f106.SEEDS == tuple(range(42, 50))
    assert (f106.MARGIN, f106.STEPS, f106.N_QUBITS) == (0.005, 750, 8)
    assert g.N_NEG_TRAIN == 6000


def test_the_rules_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest

    def test(name):
        return lambda: run_pytest(f"{THIS}::{name}", ROOT)
    assert_can_fail([Mutation(SRC, "N_POS_TRAIN, N_NEG_TRAIN = 295, "
                                   "f106.N_NEG_TRAIN\n",
                              "N_POS_TRAIN, N_NEG_TRAIN = 300, "
                              "f106.N_NEG_TRAIN\n", expect_occurrences=1)],
                    test("test_the_training_and_validation_rows_are_the_"
                         "entrys"),
                    "a training size other than F106's")
    assert_can_fail([Mutation(SRC,
                              "    rest = np.setdiff1d(np.arange(len(y)), "
                              "tr)\n",
                              "    rest = np.arange(len(y))\n",
                              expect_occurrences=1)],
                    test("test_the_training_and_validation_rows_are_the_"
                         "entrys"),
                    "validation rows that overlap training")
    assert_can_fail([Mutation(SRC, "LIMIT_S = 4 * 3600\n",
                              "LIMIT_S = 8 * 3600\n", expect_occurrences=1)],
                    test("test_the_seed_plan_keeps_eight_under_four_hours"),
                    "a limit other than 4 hours")
    assert_can_fail([Mutation(SRC, "MIN_SEEDS = 5\n", "MIN_SEEDS = 3\n",
                              expect_occurrences=1)],
                    test("test_the_seed_plan_keeps_eight_under_four_hours"),
                    "a seed floor under 5")
