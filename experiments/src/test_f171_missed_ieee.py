"""F171 (Sprint 30 Task H, #82): a stored score file is used only while it
still hashes to its outcome block, and the profile compares the two
groups it is given. Synthetic files only.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PHASE2 = ROOT / "experiments" / "phase2" / "src"
THIS = Path(__file__).relative_to(ROOT).as_posix()
sys.path.insert(0, str(PHASE2))

import f171_missed_ieee as f171  # noqa: E402
import outcome_record as orec  # noqa: E402


def _rec(tmp_path, monkeypatch, sha=None):
    monkeypatch.setattr(f171, "ROOT", tmp_path)
    path = tmp_path / "s.npz"
    np.savez(path, y_test=np.array([0, 1, 1]), p_test=np.array([.1, .9, .2]))
    return {"outcome": {"test_scores": {
        "path": "s.npz", "sha256": sha or orec.sha256_of(path)}}}


def test_a_matching_file_is_read(tmp_path, monkeypatch):
    y, p = f171.stored(_rec(tmp_path, monkeypatch))
    assert list(y) == [0, 1, 1] and list(p) == [.1, .9, .2]


def test_a_changed_file_is_refused(tmp_path, monkeypatch):
    import pytest
    with pytest.raises(ValueError, match="does not match"):
        f171.stored(_rec(tmp_path, monkeypatch, sha="0" * 64))


def test_the_profile_compares_the_groups_given():
    raw = pd.DataFrame({"TransactionAmt": [10.0, 20.0, 300.0, 500.0],
                        "ProductCD": ["W", "W", "C", None]})
    out = f171.profile(raw, pd.Index([0, 1]), pd.Index([2, 3]))
    assert out["TransactionAmt"]["missed_median"] == 15.0
    assert out["TransactionAmt"]["caught_median"] == 400.0
    assert out["ProductCD"]["W"] == {"missed": 1.0, "caught": 0.0}
    assert out["ProductCD"]["(missing)"]["caught"] == 0.5


def test_the_checks_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    src = PHASE2 / "f171_missed_ieee.py"

    def test(name):
        return lambda: run_pytest(f"{THIS}::{name}", ROOT)
    assert_can_fail([Mutation(src, '    if got != ts["sha256"]:\n',
                              "    if False:\n", expect_occurrences=1)],
                    test("test_a_changed_file_is_refused"),
                    "a changed score file used")
    assert_can_fail([Mutation(src, "            m, k = raw.loc[missed, c], "
                              "raw.loc[caught, c]\n",
                              "            m, k = raw.loc[caught, c], "
                              "raw.loc[missed, c]\n", expect_occurrences=1)],
                    test("test_the_profile_compares_the_groups_given"),
                    "the groups swapped")
