"""F157 SPECTRA part (Sprint 31 Task F, #98): the seed rule, the pocket
split of the secondary metric, and F166's grids imported unchanged, each
term proven red.

No model is fit here.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
PHASE2 = ROOT / "experiments" / "phase2" / "src"
SRC = PHASE2 / "f157_spectra_algorithms.py"
THIS = Path(__file__).relative_to(ROOT).as_posix()
sys.path.insert(0, str(PHASE2))

import f157_spectra_algorithms as f157  # noqa: E402
import f166_ulb_algorithms as f166  # noqa: E402


def test_the_seed_count_follows_seed_42s_time_at_60_minutes():
    assert f157.choose_seeds(5.0)["n_seeds"] == 10        # floor 12, cap 10
    assert f157.choose_seeds(10.0)["n_seeds"] == 6        # floor(60 / 10)
    p = f157.choose_seeds(40.0)                            # floor 1.5
    assert (p["n_seeds"], p["over_cap"]) == (3, True)
    assert f157.choose_seeds(10.0)["below_section2_five_seeds"] is False
    assert f157.choose_seeds(15.0)["below_section2_five_seeds"] is True


def test_the_pocket_metric_splits_the_test_rows():
    y = np.array([1, 0, 0, 1, 0, 0, 0, 1])
    p = np.array([0.9, 0.1, 0.2, 0.3, 0.8, 0.1, 0.2, 0.7])
    m = np.array([True, True, True, True, False, False, False, False])
    out = f157.pocket_auprc(y, p, m)
    assert out["in_pocket"] == 1.0
    # Outside: the one positive ranks second, under a negative.
    assert abs(out["out_of_pocket"] - 0.5) < 1e-12
    # A side with no positive has no AUPRC, rather than a fabricated one.
    y2 = np.array([1, 1, 0, 0, 0, 0, 0, 0])
    assert f157.pocket_auprc(y2, p, ~m)["in_pocket"] is None


def test_the_grids_and_datasets_are_the_entrys():
    assert f157.GRIDS is f166.GRIDS and f157.ALGOS == f166.ALGOS
    assert set(f157.DATASETS) == {"energy_steel", "oilgas_gasturbine",
                                  "telecom_churn", "maintenance_ai4i"}


def test_the_rules_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest

    def test(name):
        return lambda: run_pytest(f"{THIS}::{name}", ROOT)
    assert_can_fail([Mutation(SRC, "CAP_MIN = 60.0\n", "CAP_MIN = 120.0\n",
                              expect_occurrences=1)],
                    test("test_the_seed_count_follows_seed_42s_time_at_60_"
                         "minutes"),
                    "F166's 120 minutes kept")
    assert_can_fail([Mutation(SRC, "MAX_SEEDS, MIN_SEEDS = 10, 3\n",
                              "MAX_SEEDS, MIN_SEEDS = 10, 1\n",
                              expect_occurrences=1)],
                    test("test_the_seed_count_follows_seed_42s_time_at_60_"
                         "minutes"),
                    "a seed floor under 3")
    assert_can_fail([Mutation(SRC,
                              "                     if m.any() and 0 < "
                              "y[m].sum() < m.sum() else None)\n",
                              "                     if m.any() else None)\n",
                              expect_occurrences=1)],
                    test("test_the_pocket_metric_splits_the_test_rows"),
                    "an AUPRC on a side with no positive")
