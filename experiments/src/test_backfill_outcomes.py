"""Sprint 28 DV4: the outcome backfill's refusals and its record.

`experiments/phase2/src/backfill_outcomes.py` adds F154 outcome blocks to
older Phase 2 result files. These tests drive its core with synthetic scores
and a stub plan in a temporary directory: no dataset is loaded, no adapter
runs and no real result file is touched. The injection tests break each
guard in the module's source and run only these synthetic tests, so a broken
guard cannot launch real work.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "src"))

import backfill_outcomes as bo                     # noqa: E402
import outcome_record as orec                      # noqa: E402
from test_outcome_record_required import violations  # noqa: E402

THIS = Path(__file__).relative_to(ROOT).as_posix()


def _scores(seed=0, n=3000):
    rng = np.random.default_rng(seed)
    y = (rng.random(n) < 0.03).astype(int)
    return y, rng.random(n) + y


def _write_doc(tmp_path, stored, eol="\n", indent=1):
    doc = {"generator": "demo.py", "rows": [{"seed": 42, "test_auprc": stored,
                                             "note": "kept"}]}
    path = tmp_path / "res" / "demo.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    text = (json.dumps(doc, indent=indent) + "\n").replace("\n", eol)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    return path, text


def _plan(y, p, stored, **kw):
    return bo.Plan(
        lanes=[bo.Lane("demo_lane", 42, y, p, place=("rows", 0))],
        checks=[bo.Check("rows[0].test_auprc", stored, lambda: bo.ap(y, p),
                         **kw)],
        covered=["demo lane, seed 42"],
        uncovered={"other lane": "no per-row score"})


def _read(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return fh.read()


# ------------------------------------------------------------ the record
def test_writes_blocks_metadata_and_coverage(tmp_path):
    y, p = _scores()
    path, before = _write_doc(tmp_path, bo.ap(y, p))
    bo.apply(path, _plan(y, p, bo.ap(y, p)), pred_dir=tmp_path / "pred")
    doc = json.loads(_read(path))
    meta = doc["outcome_backfill"]
    assert meta["date"] == "2026-10-23"
    assert meta["generator"] == "experiments/phase2/src/backfill_outcomes.py"
    assert meta["decision"] == "Sprint 28 Manual Validation DV4"
    assert meta["covered_lanes"] == ["demo lane, seed 42"]
    assert meta["uncovered_lanes"] == {"other lane": "no per-row score"}
    assert meta["metric_check"]["n_checks"] == 1
    blk = doc["rows"][0]["outcome"]
    assert orec.is_block(blk) and blk["n_test"] == len(y)
    assert violations(path.parent, frozenset()) == []
    saved = np.load(tmp_path / "pred" / "demo_lane_42.npz")
    assert np.array_equal(saved["p_test"], p)


def test_old_values_and_format_are_kept_byte_for_byte(tmp_path):
    y, p = _scores()
    path, before = _write_doc(tmp_path, bo.ap(y, p), eol="\r\n", indent=2)
    bo.apply(path, _plan(y, p, bo.ap(y, p)), pred_dir=tmp_path / "pred")
    after = _read(path)
    assert bo.detect_format(after) == (2, "\r\n", True)
    new = json.loads(after)
    del new["rows"][0]["outcome"], new["outcome_backfill"]
    assert bo.dumps(new, (2, "\r\n", True)) == before


# ------------------------------------------------------------ refusals
def test_refuses_on_a_metric_mismatch(tmp_path):
    y, p = _scores()
    path, before = _write_doc(tmp_path, bo.ap(y, p) + 1e-6)
    with pytest.raises(bo.BackfillRefused, match="metric mismatch"):
        bo.apply(path, _plan(y, p, bo.ap(y, p) + 1e-6),
                 pred_dir=tmp_path / "pred")
    assert _read(path) == before
    assert not (tmp_path / "pred").exists()      # no per-row file either


def test_stored_rounding_is_the_tolerance_and_no_more(tmp_path):
    y, p = _scores()
    r4 = round(bo.ap(y, p), 4)
    path, _ = _write_doc(tmp_path, r4)
    bo.apply(path, _plan(y, p, r4, tol=bo.rounded(4)),
             pred_dir=tmp_path / "pred")
    path2, _ = _write_doc(tmp_path / "b", r4 + 2e-4)
    with pytest.raises(bo.BackfillRefused, match="metric mismatch"):
        bo.apply(path2, _plan(y, p, r4 + 2e-4, tol=bo.rounded(4)),
                 pred_dir=tmp_path / "pred2")


def test_refuses_when_an_old_value_would_change():
    old = {"rows": [{"test_auprc": 0.8, "n": 3}]}
    new = {"rows": [{"test_auprc": 0.8000000001, "n": 3}],
           "outcome_backfill": {}}
    with pytest.raises(bo.BackfillRefused, match="pre-existing"):
        bo.check_leaves(old, new, [("outcome_backfill",)])


def test_refuses_a_new_value_outside_the_added_keys():
    old = {"rows": [{"test_auprc": 0.8}]}
    new = {"rows": [{"test_auprc": 0.8, "stray": 1}], "outcome_backfill": {}}
    with pytest.raises(bo.BackfillRefused, match="outside"):
        bo.check_leaves(old, new, [("outcome_backfill",)])


def test_refuses_to_overwrite_an_existing_key(tmp_path):
    y, p = _scores()
    path, before = _write_doc(tmp_path, bo.ap(y, p))
    plan = _plan(y, p, bo.ap(y, p))
    plan.lanes[0].key = "note"
    with pytest.raises(bo.BackfillRefused, match="already exists"):
        bo.apply(path, plan, pred_dir=tmp_path / "pred")
    assert _read(path) == before


def test_refuses_a_second_backfill(tmp_path):
    y, p = _scores()
    path, _ = _write_doc(tmp_path, bo.ap(y, p))
    bo.apply(path, _plan(y, p, bo.ap(y, p)), pred_dir=tmp_path / "pred")
    once = _read(path)
    with pytest.raises(bo.BackfillRefused, match="second backfill"):
        bo.apply(path, _plan(y, p, bo.ap(y, p)), pred_dir=tmp_path / "pred")
    assert _read(path) == once


def test_refuses_a_plan_with_no_metric_check(tmp_path):
    y, p = _scores()
    path, before = _write_doc(tmp_path, bo.ap(y, p))
    plan = _plan(y, p, bo.ap(y, p))
    plan.checks = []
    with pytest.raises(bo.BackfillRefused, match="no metric check"):
        bo.apply(path, plan, pred_dir=tmp_path / "pred")
    assert _read(path) == before


def test_refuses_a_format_it_cannot_reproduce(tmp_path):
    path = tmp_path / "odd.json"
    path.write_text('{"rows":[{"test_auprc": 0.8}]}', encoding="utf-8")
    with pytest.raises(bo.BackfillRefused, match="round-trip"):
        bo.detect_format(_read(path))


def test_dry_run_writes_nothing(tmp_path):
    y, p = _scores()
    path, before = _write_doc(tmp_path, bo.ap(y, p))
    meta = bo.apply(path, _plan(y, p, bo.ap(y, p)), write=False,
                    pred_dir=tmp_path / "pred")
    assert meta["n_blocks"] == 1 and _read(path) == before


def test_rounding_tolerance_reads_the_stored_digits():
    assert bo.rounding_tol(0.1234) == pytest.approx(5e-5)
    assert bo.rounding_tol(0.12345678901234567) == bo.FULL_PRECISION_TOL
    assert bo.rounding_tol(1e-7) == bo.FULL_PRECISION_TOL


# ------------------------------------------------------------ guards can fail
SRC = Path(bo.__file__)


def _proof(old, new, node, label):
    from injection import Mutation, assert_can_fail, run_pytest
    assert_can_fail([Mutation(SRC, old, new, expect_occurrences=1)],
                    lambda: run_pytest(f"{THIS}::{node}", ROOT), label)


def test_metric_guard_can_fail():
    _proof("        if not diff <= tol:\n",
           "        if False:\n",
           "test_refuses_on_a_metric_mismatch", "metric mismatch ignored")


def test_old_leaf_guard_can_fail():
    _proof("    changed = [p for p, v in lo.items() if ln.get(p) != v]\n",
           "    changed = []\n",
           "test_refuses_when_an_old_value_would_change",
           "a changed old value ignored")


def test_metadata_record_can_fail():
    _proof('"decision": DECISION,', '"decision": "",',
           "test_writes_blocks_metadata_and_coverage",
           "the decision not recorded")
