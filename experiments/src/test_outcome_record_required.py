"""F154's standing rule: a Phase 2 result that holds a test score records
its outcomes (Sprint 28 Task F, #47).

The team lead, 2026-10-22: every experiment, ML or QML, this sprint and
later, computes and records the confusion counts and where each model wins.
`experiments/phase2/src/outcome_record.py` builds the block; this guard fails
any result file under `experiments/phase2/results/` that holds a score key
(AUPRC, AUC, recall or precision, by name) and no complete block.

The files that existed when the rule landed are listed by name below. The
list can only shrink: a new result file is never added to it, and a file
brought under the rule is removed from it. There is no other exemption and no
flag that switches the guard off.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "experiments" / "phase2" / "results"
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))

import outcome_record as orec  # noqa: E402

SCORE_KEY = re.compile(r"auprc|auc|recall|precision|average_precision", re.I)

# Every scored result file on 2026-10-22, before the rule. Never add to this.
EXEMPT_BEFORE_RULE = frozenset({
    "f102_downsized_pair.json",
    "f105_full_audit.json",
    "f105_pilot.json",
    "f124_lever_confirm_energy_steel.json",
    "f124_lever_screen.json",
    "f124_lever_stack_energy_steel.json",
    "f128_leaf_sweep.json",
    "f130_levers.json",
    "f142_dirac3s_verify.json",
    "f17_emulator_validation.json",
    "f20_multisample_ensemble.json",
    "f20_multisample_ensemble_emulated.json",
    "f20_soft_votes.json",
    "f20_soft_vs_classical.json",
    "f29_sample_size.json",
    "f94_controls.json",
})
EXEMPT_COUNT_WHEN_FROZEN = 30


def _keys(o):
    if isinstance(o, dict):
        for k, v in o.items():
            yield k
            yield from _keys(v)
    elif isinstance(o, list):
        for v in o:
            yield from _keys(v)


def _blocks(o):
    if isinstance(o, dict):
        if orec.is_block(o):
            yield o
        for v in o.values():
            yield from _blocks(v)
    elif isinstance(o, list):
        for v in o:
            yield from _blocks(v)


def holds_score(doc) -> bool:
    return any(SCORE_KEY.search(str(k)) for k in _keys(doc))


def violations(results_dir: Path = RESULTS,
               exempt: frozenset = EXEMPT_BEFORE_RULE) -> list[str]:
    bad = []
    for f in sorted(results_dir.rglob("*.json")):
        rel = f.relative_to(results_dir).as_posix()
        if rel in exempt:
            continue
        doc = json.loads(f.read_text(encoding="utf-8"))
        if holds_score(doc) and not any(True for _ in _blocks(doc)):
            bad.append(rel)
    return bad


def stale_hashes(results_dir: Path = RESULTS) -> list[str]:
    """Blocks whose per-row file is on this machine and does not match."""
    bad = []
    for f in sorted(results_dir.rglob("*.json")):
        for b in _blocks(json.loads(f.read_text(encoding="utf-8"))):
            p = ROOT / b["test_scores"]["path"]
            if p.exists() and orec.sha256_of(p) != b["test_scores"]["sha256"]:
                bad.append(f"{f.name}: {b['test_scores']['path']}")
    return bad


def test_every_new_scored_result_records_its_outcomes():
    bad = violations()
    assert not bad, (
        "These Phase 2 result files hold a test score and no outcome block "
        "(F154 standing rule; build one with outcome_record.record): "
        + ", ".join(bad))


def test_recorded_per_row_files_match_their_hashes():
    assert not stale_hashes()


def test_the_exempt_list_only_shrinks():
    assert len(EXEMPT_BEFORE_RULE) <= EXEMPT_COUNT_WHEN_FROZEN
    assert EXEMPT_COUNT_WHEN_FROZEN == 30


def test_a_new_scored_file_without_a_block_is_caught(tmp_path):
    (tmp_path / "new.json").write_text(json.dumps({"rows": [{"test_auprc": 0.8}]}))
    assert violations(tmp_path, frozenset()) == ["new.json"]


def test_a_new_scored_file_with_a_block_passes(tmp_path):
    rng = np.random.default_rng(0)
    y = (rng.random(2000) < 0.02).astype(int)
    p = rng.random(2000) + y
    blk = orec.record("demo", 42, y, p, pred_dir=tmp_path / "pred")
    (tmp_path / "ok.json").write_text(json.dumps({"rows": [{"test_auprc": 0.8,
                                                            "outcome": blk}]}))
    assert violations(tmp_path, frozenset()) == []


def test_an_unscored_file_needs_no_block(tmp_path):
    (tmp_path / "timing.json").write_text(json.dumps({"build_s": 12.5}))
    assert violations(tmp_path, frozenset()) == []


def test_ties_at_the_cut_are_flagged_together_whatever_the_order():
    y = np.zeros(1000, dtype=int)
    s = np.zeros(1000)
    s[[0, 1, 2]] = 2.0
    s[[3, 4, 5, 6]] = 1.0          # budget 5: the cut falls inside this tie
    y[[0, 6]] = 1
    r = orec.at_budget_on_test(y, s)
    assert r["n_budget"] == 5 and r["n_flagged"] == 7
    assert r["confusion"] == {"tn": 993, "fp": 5, "fn": 0, "tp": 2}
    perm = np.random.default_rng(3).permutation(1000)
    assert orec.at_budget_on_test(y[perm], s[perm]) == r


def test_validation_operating_points_come_from_phase1_metrics(tmp_path):
    import metrics
    rng = np.random.default_rng(1)
    y, yv = ((rng.random(3000) < 0.03).astype(int) for _ in range(2))
    p, pv = (rng.random(3000) + y) / 2, (rng.random(3000) + yv) / 2
    blk = orec.record("demo", 1, y, p, y_val=yv, p_val=pv, pred_dir=tmp_path)
    ref = metrics.summarize(y, yv, pv, p)["operating_points"]
    got = blk["operating_points_from_validation"]
    assert [g["confusion"] for g in got] == [r["confusion"] for r in ref]


def test_saved_scores_round_trip_and_hash(tmp_path):
    y = np.array([0, 1, 0, 1]); p = np.array([0.1, 0.9, 0.2, 0.8])
    blk = orec.record("demo", 7, y, p, budget=0.25, pred_dir=tmp_path)
    f = tmp_path / "demo_7.npz"
    assert orec.sha256_of(f) == blk["test_scores"]["sha256"]
    z = np.load(f)
    assert np.array_equal(z["p_test"], p) and np.array_equal(z["y_test"], y)


def test_a_block_must_carry_its_per_row_scores(tmp_path):
    with pytest.raises(ValueError):
        orec.record("demo", 1, [0, 1], [0.1, 0.9], save=False)
