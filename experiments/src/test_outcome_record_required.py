"""F154's standing rule: a Phase 2 result that holds a test score records
its outcomes (Sprint 28 Task F, #47).

The team lead, 2026-10-22: every experiment, ML or QML, this sprint and
later, computes and records the confusion counts and where each model wins.
`experiments/phase2/src/outcome_record.py` builds the block; this guard fails
any result file under `experiments/phase2/results/` that:
  - holds a score key (AUPRC, AUC, recall or precision, by name) and no
    complete block;
  - holds a scored entry for a seed (the entry's own `seed`, or its nearest
    ancestor's) with no block anywhere in the file for that seed; or
  - declares an `outcome_backfill` whose `n_blocks` differs from the blocks
    the file holds.

What the per-seed rule does not catch: once one block exists for a seed,
every other scored entry for that seed passes, so a file that records one
lane of several on each seed is not caught. Closing that needs each file to
declare its lane coverage; f112, f113 and f154 list their blocks away from
the scored rows, and result files are not edited to add it (PR #46 review).
Entries a file copies from another result are skipped only when named in
`CITED_ENTRIES` and in the file's own `outcome_backfill.uncovered_lanes`.

The files that existed when the rule landed are listed by name below. The
list can only shrink: a new result file is never added to it, and a file
brought under the rule is removed from it. `ORIGINAL_EXEMPT_2026_10_22` is
the list as frozen, and the tests pin the current list to a subset of it at
its exact current size. There is no other exemption and no flag that
switches the guard off.

The same file also holds D4 part 3's rule (2026-10-23): every new top-level
result file carries a `provenance` block. Its exemption is a frozen list of
the 47 files that existed then, pinned by a hash of its names, less the
files backfilled since.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "experiments" / "phase2" / "results"
THIS = Path(__file__).relative_to(ROOT).as_posix()
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "src"))

import outcome_record as orec  # noqa: E402

SCORE_KEY = re.compile(r"auprc|auc|recall|precision|average_precision", re.I)

# Scored result files from before the rule (30 on 2026-10-22) not yet
# backfilled. Never add to this.
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
# The exact current size. Lower it by hand when a file leaves the list.
EXEMPT_COUNT_NOW = 16

# The list as frozen when the rule landed (commit 12e7794). Never edit.
ORIGINAL_EXEMPT_2026_10_22 = frozenset((
    "f102_downsized_pair.json", "f103_tier1.json", "f103_tier1_pilot.json",
    "f105_full_audit.json", "f105_pilot.json", "f106_dequant.json",
    "f106_dequant_pilot.json", "f107_shots.json", "f108_ceiling.json",
    "f108_ceiling_pilot.json", "f109_ladder.json", "f109_ladder_pilot.json",
    "f112_intervals.json", "f113_oracle_gap.json",
    "f124_lever_confirm_energy_steel.json", "f124_lever_screen.json",
    "f124_lever_stack_energy_steel.json", "f128_leaf_sweep.json",
    "f130_levers.json", "f130_ulb_hgb_check.json",
    "f142_dirac3s_verify.json", "f142_readout.json", "f144_proxy_twin.json",
    "f17_emulator_validation.json", "f20_multisample_ensemble.json",
    "f20_multisample_ensemble_emulated.json", "f20_soft_votes.json",
    "f20_soft_vs_classical.json", "f29_sample_size.json", "f94_controls.json",
))
# Pins the literal above (Sprint 28 IMP-1, `frozen_list.check`).
ORIGINAL_EXEMPT_SHA256 = (
    "01004173571686d6d23b34d50963f41aa58aeb42343548a515d7df57f1054a61")
BACKFILL_KEY = "outcome_backfill"

# Scored entries a file copies from another result, which carries their
# blocks. Each must be named in the file's own outcome_backfill
# uncovered_lanes (checked below). Found when the per-seed rule landed
# (PR #46 review): the f109 pilot ran seed 42 only, and its energy_steel
# rows, copied from f103_tier1.json for seeds 42-46, are the only scored
# entries for seeds 43-46. Never add without that record in the file.
CITED_ENTRIES = {
    ("f109_ladder_pilot.json", ("datasets", "energy_steel")):
        "energy_steel",
}

# Sprint 28 D4 part 3 (team lead, 2026-10-23): every new top-level result
# file, of every run type (ML, QML, optimization, tensor), scored or not,
# carries `provenance` (generator, commit, clean flag, seeds, versions;
# build it with provenance.record). The 47 files that existed when the rule
# landed are listed below, never edited: the test pins the list to a SHA-256
# of its sorted names, so a name added to it fails whatever counts are
# changed. A file that gains a complete block moves to PROVENANCE_BACKFILLED.
# Subfolders (call_logs, device_samples, pools) are records a run writes,
# not results, and are not checked here; device_store's guard covers
# device_samples.
ORIGINAL_PROVENANCE_EXEMPT_2026_10_23 = frozenset((
    "f102_downsized_pair.json", "f103_tier1.json", "f103_tier1_pilot.json",
    "f104_gate_check.json", "f105_full_audit.json", "f105_pilot.json",
    "f106_dequant.json", "f106_dequant_pilot.json", "f107_shots.json",
    "f108_ceiling.json", "f108_ceiling_pilot.json", "f109_ladder.json",
    "f109_ladder_pilot.json", "f110_scaling.json", "f111_loke_protocol.json",
    "f112_intervals.json", "f113_oracle_gap.json",
    "f114_calibrated_plugin.json", "f114_calibrated_plugin_pilot.json",
    "f115_cost_scaling.json", "f124_lever_confirm_energy_steel.json",
    "f124_lever_screen.json", "f124_lever_stack_energy_steel.json",
    "f126_sparsity_rule.json", "f128_leaf_sweep.json", "f130_levers.json",
    "f130_ulb_hgb_check.json", "f142_dirac3s_verify.json",
    "f142_dry_run.json", "f142_readout.json", "f144_proxy_twin.json",
    "f145_build_drift.json", "f151_hgb_cause.json", "f152_exp2.json",
    "f152_exp2_pilot.json", "f153_exp3_design.json", "f154_confusion.json",
    "f162_in_pocket.json", "f17_emulator_sparsity.json",
    "f17_emulator_validation.json", "f20_multisample_ensemble.json",
    "f20_multisample_ensemble_emulated.json", "f20_soft_votes.json",
    "f20_soft_vs_classical.json", "f29_sample_size.json",
    "f94_controls.json", "qpu_cost_ledger_phase2.json",
))
ORIGINAL_PROVENANCE_SHA256 = (
    "705c7aa95dc9ed0f30ae6946cbe89969385a370f73759cb7e759e0724d5cad77")
# Listed files brought under the rule since. Only grows.
PROVENANCE_BACKFILLED: frozenset = frozenset()
PROVENANCE_EXEMPT = ORIGINAL_PROVENANCE_EXEMPT_2026_10_23 - PROVENANCE_BACKFILLED

import provenance as prov  # noqa: E402
import frozen_list as fl  # noqa: E402


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


def _scalar(v) -> bool:
    return not isinstance(v, (dict, list))


def seeded_scores(o, seed=None, path=()):
    """(path, seed) of every non-block object holding a score-named scalar,
    the seed taken from the object's own `seed` or its nearest ancestor's.
    An entry with no seed (a mean over seeds) yields nothing."""
    if isinstance(o, dict):
        if orec.is_block(o):
            return
        if _scalar(o.get("seed")) and o.get("seed") is not None:
            seed = o["seed"]
        if seed is not None and any(SCORE_KEY.search(str(k)) and _scalar(v)
                                    for k, v in o.items()):
            yield path, seed
        for k, v in o.items():
            yield from seeded_scores(v, seed, path + (k,))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from seeded_scores(v, seed, path + (i,))


def holds_score(doc) -> bool:
    return any(SCORE_KEY.search(str(k)) for k in _keys(doc))


def file_violations(rel: str, doc) -> list[str]:
    if not holds_score(doc):
        return []
    blocks = list(_blocks(doc))
    if not blocks:
        return [rel]
    bad = []
    have = {str(b["seed"]) for b in blocks}
    missing: dict = {}
    cited = [p for (name, p) in CITED_ENTRIES if name == rel]
    for path, seed in seeded_scores(doc):
        if any(path[:len(p)] == p for p in cited):
            continue
        if str(seed) not in have:
            missing.setdefault(str(seed), path)
    for seed, path in sorted(missing.items()):
        bad.append(f"{rel} (no block for seed {seed}; first scored entry "
                   f"at {'.'.join(map(str, path))})")
    meta = doc.get(BACKFILL_KEY)
    if isinstance(meta, dict) and meta.get("n_blocks") != len(blocks):
        bad.append(f"{rel} ({BACKFILL_KEY}.n_blocks {meta.get('n_blocks')} "
                   f"but {len(blocks)} blocks in the file)")
    return bad


def violations(results_dir: Path = RESULTS,
               exempt: frozenset = EXEMPT_BEFORE_RULE) -> list[str]:
    bad = []
    for f in sorted(results_dir.rglob("*.json")):
        rel = f.relative_to(results_dir).as_posix()
        if rel in exempt:
            continue
        bad += file_violations(rel, json.loads(f.read_text(encoding="utf-8")))
    return bad


def provenance_violations(results_dir: Path = RESULTS,
                          exempt: frozenset = PROVENANCE_EXEMPT) -> list[str]:
    bad = []
    for f in sorted(results_dir.glob("*.json")):
        if f.name in exempt:
            continue
        doc = json.loads(f.read_text(encoding="utf-8"))
        block = doc.get("provenance") if isinstance(doc, dict) else None
        bad += [f"{f.name} ({p})" for p in prov.problems(block)]
    return bad


def check_hashes(results_dir: Path = RESULTS,
                 root: Path = ROOT) -> tuple[list[str], set[str], set[str]]:
    """(stale entries, block paths verified, every block path).

    Only per-row files present on THIS machine are verified; most live in
    the gitignored predictions folder, so a CI clone verifies only the
    tracked ones. `root` is where the blocks' relative paths resolve."""
    bad, verified, named = [], set(), set()
    sha: dict = {}
    for f in sorted(results_dir.rglob("*.json")):
        for b in _blocks(json.loads(f.read_text(encoding="utf-8"))):
            rel = b["test_scores"]["path"]
            named.add(rel)
            p = root / rel
            if p.exists():
                verified.add(rel)
                if rel not in sha:
                    sha[rel] = orec.sha256_of(p)
                if sha[rel] != b["test_scores"]["sha256"]:
                    bad.append(f"{f.name}: {rel}")
    return bad, verified, named


def stale_hashes(results_dir: Path = RESULTS, root: Path = ROOT) -> list[str]:
    """Blocks whose per-row file is on this machine and does not match."""
    return check_hashes(results_dir, root)[0]


def tracked(paths: set[str]) -> set[str]:
    """The subset of `paths` that git tracks. Raises if git cannot answer:
    "could not tell" must not read as "none tracked"."""
    out = subprocess.run(["git", "-C", str(ROOT), "ls-files", "-z"],
                         capture_output=True, check=True).stdout
    files = set(out.decode("utf-8").split("\0")) - {""}
    return paths & files


# ------------------------------------------------------------ the real files
def test_every_new_scored_result_records_its_outcomes():
    bad = violations()
    assert not bad, (
        "These Phase 2 result files hold a test score without the outcome "
        "blocks it needs (F154 standing rule; build one with "
        "outcome_record.record): " + ", ".join(bad))


def test_recorded_per_row_files_match_their_hashes():
    """Checks the per-row files present on this machine, and at least every
    one git tracks, so a clone cannot pass by verifying none."""
    bad, verified, named = check_hashes()
    assert not bad, bad
    must = tracked(named)
    assert must, "no block names a tracked per-row file; the floor is zero"
    assert must <= verified, sorted(must - verified)[:5]
    assert len(verified) >= len(must)


def test_the_exempt_list_only_shrinks():
    bad = fl.check(EXEMPT_BEFORE_RULE, ORIGINAL_EXEMPT_2026_10_22,
                   ORIGINAL_EXEMPT_SHA256)
    assert not bad, bad
    assert len(EXEMPT_BEFORE_RULE) == EXEMPT_COUNT_NOW == 16
    assert len(ORIGINAL_EXEMPT_2026_10_22) == 30


def test_every_new_result_records_its_provenance():
    bad = provenance_violations()
    assert not bad, (
        "These Phase 2 result files lack a complete provenance block (D4; "
        "build one with provenance.record): " + ", ".join(bad))


def test_the_provenance_exempt_list_only_shrinks():
    bad = fl.check(PROVENANCE_EXEMPT, ORIGINAL_PROVENANCE_EXEMPT_2026_10_23,
                   ORIGINAL_PROVENANCE_SHA256)
    assert not bad, bad
    assert PROVENANCE_BACKFILLED <= ORIGINAL_PROVENANCE_EXEMPT_2026_10_23
    for name in sorted(PROVENANCE_EXEMPT):
        f = RESULTS / name
        assert f.exists(), f"{name} is exempt but does not exist"
        doc = json.loads(f.read_text(encoding="utf-8"))
        assert prov.problems(doc.get("provenance")), (
            f"{name} now has a complete provenance block; add it to "
            "PROVENANCE_BACKFILLED")


def test_every_cited_entry_is_declared_uncovered_in_its_file():
    assert len(CITED_ENTRIES) == 1
    for (name, path), lane in CITED_ENTRIES.items():
        doc = json.loads((RESULTS / name).read_text(encoding="utf-8"))
        node = doc
        for k in path:
            node = node[k]
        assert lane in doc[BACKFILL_KEY]["uncovered_lanes"], (name, lane)


def test_every_exempt_file_exists_and_still_holds_no_block():
    for name in sorted(EXEMPT_BEFORE_RULE):
        f = RESULTS / name
        assert f.exists(), f"{name} is exempt but does not exist"
        doc = json.loads(f.read_text(encoding="utf-8"))
        assert holds_score(doc), f"{name} holds no score; drop its exemption"
        assert not any(True for _ in _blocks(doc)), (
            f"{name} now holds a block; remove it from EXEMPT_BEFORE_RULE "
            "and lower EXEMPT_COUNT_NOW")


# ------------------------------------------------------------ synthetic
def _block(tmp_path, seed, name="demo"):
    rng = np.random.default_rng(seed)
    y = (rng.random(2000) < 0.02).astype(int)
    p = rng.random(2000) + y
    return orec.record(name, seed, y, p, pred_dir=tmp_path / "pred")


def _write(tmp_path, name, doc):
    (tmp_path / name).write_text(json.dumps(doc))


def test_a_new_scored_file_without_a_block_is_caught(tmp_path):
    _write(tmp_path, "new.json", {"rows": [{"test_auprc": 0.8}]})
    assert violations(tmp_path, frozenset()) == ["new.json"]


def test_a_new_scored_file_with_a_block_passes(tmp_path):
    _write(tmp_path, "ok.json", {"rows": [{"seed": 42, "test_auprc": 0.8,
                                           "outcome": _block(tmp_path, 42)}]})
    assert violations(tmp_path, frozenset()) == []


def test_a_seed_with_scores_and_no_block_is_caught(tmp_path):
    _write(tmp_path, "part.json", {"rows": [
        {"seed": 42, "test_auprc": 0.8, "outcome": _block(tmp_path, 42)},
        {"seed": 43, "test_auprc": 0.7}]})
    assert violations(tmp_path, frozenset()) == [
        "part.json (no block for seed 43; first scored entry at rows.1)"]


def test_a_nested_entry_inherits_its_rows_seed(tmp_path):
    _write(tmp_path, "nest.json", {"rows": [
        {"seed": 42, "outcome": _block(tmp_path, 42)},
        {"seed": 43, "arm": {"test_auprc": 0.7}}]})
    assert violations(tmp_path, frozenset()) == [
        "nest.json (no block for seed 43; first scored entry at rows.1.arm)"]


def test_blocks_listed_away_from_the_rows_cover_their_seeds(tmp_path):
    # The f112/f113/f154 layout: per-seed deltas, blocks in a list.
    _write(tmp_path, "listed.json", {
        "per_seed": [{"seed": s, "delta_auprc": 0.01} for s in (42, 43)],
        "blocks": [_block(tmp_path, s) for s in (42, 43)],
        "mean_delta_auprc": 0.01})
    assert violations(tmp_path, frozenset()) == []


def test_a_backfill_count_that_disagrees_is_caught(tmp_path):
    _write(tmp_path, "bf.json", {"rows": [
        {"seed": 42, "test_auprc": 0.8, "outcome": _block(tmp_path, 42)}],
        BACKFILL_KEY: {"n_blocks": 2}})
    assert violations(tmp_path, frozenset()) == [
        f"bf.json ({BACKFILL_KEY}.n_blocks 2 but 1 blocks in the file)"]


def test_an_unscored_file_needs_no_block(tmp_path):
    _write(tmp_path, "timing.json", {"build_s": 12.5, "seed": 3})
    assert violations(tmp_path, frozenset()) == []


def test_a_changed_per_row_file_is_reported(tmp_path):
    blk = _block(tmp_path, 1)
    blk["test_scores"]["path"] = "pred/demo_1.npz"
    res = tmp_path / "res"
    res.mkdir()
    (res / "r.json").write_text(json.dumps({"rows": [{"outcome": blk}]}))
    assert stale_hashes(res, tmp_path) == []
    f = tmp_path / "pred" / "demo_1.npz"
    raw = bytearray(f.read_bytes())
    raw[-1] ^= 0x01
    f.write_bytes(bytes(raw))
    assert stale_hashes(res, tmp_path) == ["r.json: pred/demo_1.npz"]


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


def test_the_writer_never_replaces_a_score_file(tmp_path):
    """Sprint 31 D13: a name held by different bytes gets the next free
    name; the same bytes reuse the file; nothing recorded is replaced."""
    y = np.array([0, 1, 0, 1]); p = np.array([0.1, 0.9, 0.2, 0.8])
    first = orec.save_test_scores("demo", 7, y, p, pred_dir=tmp_path)
    kept = (tmp_path / "demo_7.npz").read_bytes()
    again = orec.save_test_scores("demo", 7, y, p, pred_dir=tmp_path)
    assert again == first                              # same bytes: reused
    other = orec.save_test_scores("demo", 7, y, p[::-1], pred_dir=tmp_path)
    third = orec.save_test_scores("demo", 7, y, p * 0.5, pred_dir=tmp_path)
    assert (tmp_path / "demo_7.npz").read_bytes() == kept
    assert other["path"].endswith("demo_7_v2.npz")
    assert third["path"].endswith("demo_7_v3.npz")
    assert orec.sha256_of(tmp_path / "demo_7_v2.npz") == other["sha256"]
    assert sorted(f.name for f in tmp_path.iterdir()) == [
        "demo_7.npz", "demo_7_v2.npz", "demo_7_v3.npz"]  # no temp file left


def test_the_writer_guard_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    src = ROOT / "experiments" / "phase2" / "src" / "outcome_record.py"
    old = "            os.link(tmp, f)        # fails if the name exists: never replaces\n"
    # The writer as it was: overwrite the first name, whatever it held.
    new = "            os.replace(tmp, first); tmp.write_bytes(data)\n"
    assert_can_fail([Mutation(src, old, new, expect_occurrences=1)],
                    lambda: run_pytest(
                        f"{THIS}::test_the_writer_never_replaces_a_score_file", ROOT),
                    "the score writer replaces a recorded file")


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


def test_a_new_file_without_provenance_is_caught(tmp_path):
    _write(tmp_path, "opt.json", {"objective": -3.2, "seed": 42})
    assert provenance_violations(tmp_path, frozenset()) == [
        "opt.json (no provenance block)"]


def test_a_recorded_provenance_block_passes(tmp_path):
    _write(tmp_path, "ok.json", {"objective": -3.2, "provenance": prov.record(
        ROOT / "experiments" / "phase2" / "src" / "provenance.py", [42, 43])})
    assert provenance_violations(tmp_path, frozenset()) == []


def test_an_incomplete_provenance_block_is_caught(tmp_path):
    blk = prov.record(SELF, [42])
    blk["generator_commit"] = blk["generator_commit"][:7]
    blk["seeds"] = []
    del blk["versions"]
    _write(tmp_path, "part.json", {"provenance": blk})
    assert provenance_violations(tmp_path, frozenset()) == [
        "part.json (missing versions)",
        "part.json (generator_commit is not a full commit hash)",
        "part.json (seeds is not a non-empty list of integers)"]


def test_subfolders_are_not_results(tmp_path):
    (tmp_path / "call_logs").mkdir()
    _write(tmp_path / "call_logs", "c.json", {"calls": 1})
    assert provenance_violations(tmp_path, frozenset()) == []


def test_record_refuses_no_seeds():
    with pytest.raises(ValueError):
        prov.record(SELF, [])


# ------------------------------------------------------------ guards can fail
# Each proof edits this file and runs one node of it in a subprocess. The
# nodes read only small JSON files or tmp_path, so a broken guard cannot
# start long work.
SELF = Path(__file__)


def _proof(edits, node, label):
    from injection import Mutation, assert_can_fail, run_pytest
    assert_can_fail([Mutation(SELF, old, new, expect_occurrences=1)
                     for old, new in edits],
                    lambda: run_pytest(f"{THIS}::{node}", ROOT), label)


ADD_AT_TOP = ('    "f102_downsized_pair.json",\n    "f105_full_audit.json",\n',
              '    "f102_downsized_pair.json",\n    "NAME",\n'
              '    "f105_full_audit.json",\n')
RAISE_COUNT = ("EXEMPT_COUNT_NOW = 16\n", "EXEMPT_COUNT_NOW = 17\n")


def _add(name):
    return (ADD_AT_TOP[0], ADD_AT_TOP[1].replace("NAME", name))


def test_a_new_exempt_name_is_caught_even_with_the_count_raised():
    _proof([_add("f153_exp3_design.json"),
            (RAISE_COUNT[0], RAISE_COUNT[1]),
            ("== EXEMPT_COUNT_NOW == 16\n", "== EXEMPT_COUNT_NOW == 17\n")],
           "test_the_exempt_list_only_shrinks", "a new exempt name")


def test_a_name_added_to_the_original_too_is_caught_by_its_hash():
    # Every count raised to match, so only the content pin can fire.
    _proof([_add("f153_exp3_design.json"),
            (RAISE_COUNT[0], RAISE_COUNT[1]),
            ("== EXEMPT_COUNT_NOW == 16\n", "== EXEMPT_COUNT_NOW == 17\n"),
            ('"f94_controls.json",\n))\n# Pins',
             '"f94_controls.json",\n    "f153_exp3_design.json",\n))\n# Pins'),
            ("assert len(ORIGINAL_EXEMPT_2026_10_22) == 30\n",
             "assert len(ORIGINAL_EXEMPT_2026_10_22) == 31\n")],
           "test_the_exempt_list_only_shrinks",
           "a name added to the list and its original")


def test_a_backfilled_name_put_back_is_caught_by_the_count():
    _proof([_add("f103_tier1.json")],
           "test_the_exempt_list_only_shrinks", "a backfilled name re-added")


def test_a_backfilled_name_put_back_is_caught_by_its_block():
    _proof([_add("f103_tier1.json")],
           "test_every_exempt_file_exists_and_still_holds_no_block",
           "an exempt file that holds a block")


def test_the_per_seed_rule_can_fail():
    _proof([("        if str(seed) not in have:\n", "        if False:\n")],
           "test_a_seed_with_scores_and_no_block_is_caught",
           "a seed with no block")


def test_the_backfill_count_rule_can_fail():
    _proof([('meta.get("n_blocks") != len(blocks):\n',
             'meta.get("n_blocks") != meta.get("n_blocks"):\n')],
           "test_a_backfill_count_that_disagrees_is_caught",
           "a backfill count that disagrees")


def test_the_hash_comparison_can_fail():
    _proof([('if sha[rel] != b["test_scores"]["sha256"]:\n',
             "if False:\n")],
           "test_a_changed_per_row_file_is_reported", "a changed .npz")


def test_a_new_provenance_exempt_name_is_caught():
    _proof([('    "f94_controls.json", "qpu_cost_ledger_phase2.json",\n',
             '    "f94_controls.json", "f99_new.json",\n'
             '    "qpu_cost_ledger_phase2.json",\n')],
           "test_the_provenance_exempt_list_only_shrinks",
           "a new provenance exempt name")


def test_the_provenance_rule_can_fail():
    _proof([("        bad += [f\"{f.name} ({p})\" for p in "
             "prov.problems(block)]\n",
             "        bad += []\n")],
           "test_a_new_file_without_provenance_is_caught",
           "a result with no provenance")


def test_the_verified_floor_can_fail():
    _proof([("            if p.exists():\n", "            if False:\n")],
           "test_recorded_per_row_files_match_their_hashes",
           "zero per-row files verified")


# ------------------------------------------------- the 0.1% budget (F201)
# Sprint 34 Task A (#135). The filed preregistration (section 2; Sprint 33
# D10): from filing on, 2026-11-18, recall at the 0.1% alert budget is
# reported beside the 0.5% figure for every scored result; results recorded
# before filing are not recomputed. `outcome_record.record` writes it as
# `at_low_budget_on_test`. Every result file that held a block at filing is
# listed below by name (none changed after 2026-11-09). The list may only
# shrink; a new result file is never added to it.
ORIGINAL_SCORED_BEFORE_FILING_2026_11_18 = frozenset((
    "exp5_router.json", "f103_tier1.json", "f103_tier1_pilot.json",
    "f106_dequant.json", "f106_dequant_pilot.json", "f107_shots.json",
    "f108_ceiling.json", "f108_ceiling_pilot.json", "f109_ladder.json",
    "f109_ladder_pilot.json", "f111_loke_protocol.json",
    "f112_intervals.json", "f113_oracle_gap.json", "f114_real_ceiling.json",
    "f114_real_ceiling_lr05.json", "f130_ulb_hgb_check.json",
    "f142_readout.json", "f144_proxy_twin.json", "f151_hgb_cause.json",
    "f152_exp2.json", "f152_exp2_pilot.json", "f153_exp3_design.json",
    "f154_confusion.json", "f157_qnn_ieee.json", "f157_qnn_ieee_pilot.json",
    "f157_spectra_algorithms.json", "f157_spectra_algorithms_rbf.json",
    "f158_fraud_types.json", "f162_in_pocket.json",
    "f166_ulb_algorithms.json", "f169_plugin_bins.json",
    "f169_plugin_bins_lr05.json", "f174_ieee_algorithms.json",
    "f185_cost_budget.json",
))
ORIGINAL_SCORED_BEFORE_FILING_SHA256 = (
    "53af82d697840649e195be40d31d717eaff05bbcc9d8e8adca6ebf1f5e6d74b6")
SCORED_BEFORE_FILING_EXEMPT = ORIGINAL_SCORED_BEFORE_FILING_2026_11_18


def low_budget_problem(block) -> str | None:
    """Why a block lacks the 0.1% figures, or None when it has them."""
    low = block.get(orec.LOW_BUDGET_KEY)
    if not isinstance(low, dict):
        return f"no {orec.LOW_BUDGET_KEY}"
    if low.get("budget") != orec.LOW_BUDGET:
        return f"{orec.LOW_BUDGET_KEY} at budget {low.get('budget')}"
    if "confusion" not in low:
        return f"{orec.LOW_BUDGET_KEY} has no confusion counts"
    if "recall" not in low:
        return f"{orec.LOW_BUDGET_KEY} has no recall"
    return None


def low_budget_violations(results_dir: Path = RESULTS,
                          exempt: frozenset = SCORED_BEFORE_FILING_EXEMPT
                          ) -> list[str]:
    bad = []
    for f in sorted(results_dir.rglob("*.json")):
        rel = f.relative_to(results_dir).as_posix()
        if rel in exempt:  # scored before filing
            continue
        for b in _blocks(json.loads(f.read_text(encoding="utf-8"))):
            why = low_budget_problem(b)
            if why:
                bad.append(f"{rel} ({b['name']} seed {b['seed']}: {why})")
    return bad


def test_every_scored_result_after_filing_reports_the_low_budget():
    bad = low_budget_violations()
    assert not bad, (
        "These Phase 2 result files, written after filing (2026-11-18), "
        "hold an outcome block without the 0.1% budget's counts and recall "
        "(filed section 2; build blocks with outcome_record.record): "
        + ", ".join(bad))


def test_the_scored_before_filing_list_only_shrinks():
    bad = fl.check(SCORED_BEFORE_FILING_EXEMPT,
                   ORIGINAL_SCORED_BEFORE_FILING_2026_11_18,
                   ORIGINAL_SCORED_BEFORE_FILING_SHA256)
    assert not bad, bad
    assert len(ORIGINAL_SCORED_BEFORE_FILING_2026_11_18) == 34
    for name in sorted(SCORED_BEFORE_FILING_EXEMPT):
        assert (RESULTS / name).exists(), f"{name} is listed but does not exist"


def test_a_new_block_records_the_low_budget_and_recall(tmp_path):
    y = np.zeros(2000, dtype=int)
    y[:40] = 1
    p = np.linspace(0, 1, 2000)[::-1].copy()   # the first rows score highest
    blk = orec.record("demo", 5, y, p, pred_dir=tmp_path)
    low = blk[orec.LOW_BUDGET_KEY]
    assert low["budget"] == 0.001 and low["n_budget"] == 2
    assert low["confusion"] == {"tn": 1960, "fp": 0, "fn": 38, "tp": 2}
    assert low["recall"] == pytest.approx(2 / 40)
    assert blk["at_budget_on_test"]["recall"] == pytest.approx(10 / 40)
    assert low_budget_problem(blk) is None


def test_recall_with_no_positive_is_refused():
    with pytest.raises(ValueError, match="no positive"):
        orec.recall({"tn": 5, "fp": 0, "fn": 0, "tp": 0})


def _low_doc(tmp_path, drop=None, **change):
    blk = _block(tmp_path, 42)
    low = blk[orec.LOW_BUDGET_KEY]
    low.update(change)
    if drop:
        low.pop(drop)
    return {"rows": [{"seed": 42, "test_auprc": 0.8, "outcome": blk}]}


def test_a_block_without_the_low_budget_is_caught(tmp_path):
    doc = _low_doc(tmp_path)
    del doc["rows"][0]["outcome"][orec.LOW_BUDGET_KEY]
    _write(tmp_path, "new.json", doc)
    assert low_budget_violations(tmp_path, frozenset()) == [
        f"new.json (demo seed 42: no {orec.LOW_BUDGET_KEY})"]


def test_a_low_budget_at_another_budget_is_caught(tmp_path):
    _write(tmp_path, "new.json", _low_doc(tmp_path, budget=0.005))
    assert low_budget_violations(tmp_path, frozenset()) == [
        f"new.json (demo seed 42: {orec.LOW_BUDGET_KEY} at budget 0.005)"]


def test_a_low_budget_without_counts_is_caught(tmp_path):
    _write(tmp_path, "new.json", _low_doc(tmp_path, drop="confusion"))
    assert low_budget_violations(tmp_path, frozenset()) == [
        f"new.json (demo seed 42: {orec.LOW_BUDGET_KEY} has no confusion counts)"]


def test_a_low_budget_without_recall_is_caught(tmp_path):
    _write(tmp_path, "new.json", _low_doc(tmp_path, drop="recall"))
    assert low_budget_violations(tmp_path, frozenset()) == [
        f"new.json (demo seed 42: {orec.LOW_BUDGET_KEY} has no recall)"]


def test_a_complete_new_block_and_a_listed_file_pass(tmp_path):
    _write(tmp_path, "new.json", _low_doc(tmp_path))
    old = _low_doc(tmp_path)
    del old["rows"][0]["outcome"][orec.LOW_BUDGET_KEY]
    _write(tmp_path, "old.json", old)
    assert low_budget_violations(tmp_path, frozenset({"old.json"})) == []


def test_each_low_budget_term_can_fail():
    for old, new, node, label in (
            ("    if not isinstance(low, dict):\n", "    if False:\n",
             "test_a_block_without_the_low_budget_is_caught",
             "a block with no 0.1% entry"),
            ('    if low.get("budget") != orec.LOW_BUDGET:\n', "    if False:\n",
             "test_a_low_budget_at_another_budget_is_caught",
             "a 0.1% entry at another budget"),
            ('    if "confusion" not in low:\n', "    if False:\n",
             "test_a_low_budget_without_counts_is_caught",
             "a 0.1% entry with no counts"),
            ('    if "recall" not in low:\n', "    if False:\n",
             "test_a_low_budget_without_recall_is_caught",
             "a 0.1% entry with no recall"),
            ("        if rel in exempt:  # scored before filing\n",
             "        if False:\n",
             "test_a_complete_new_block_and_a_listed_file_pass",
             "a file scored before filing read as new")):
        _proof([(old, new)], node, label)


def test_the_writer_records_the_low_budget_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    src = ROOT / "experiments" / "phase2" / "src" / "outcome_record.py"
    assert_can_fail([Mutation(
        src, "           LOW_BUDGET_KEY: at_budget_on_test(y, p, LOW_BUDGET)}\n",
        "           }\n", expect_occurrences=1)],
        lambda: run_pytest(
            f"{THIS}::test_a_new_block_records_the_low_budget_and_recall", ROOT),
        "the writer leaves out the 0.1% budget")


def test_a_new_name_in_the_scored_before_filing_list_is_caught():
    _proof([('    "f185_cost_budget.json",\n))\nORIGINAL_SCORED_BEFORE_FILING_SHA256',
             '    "f185_cost_budget.json", "f200_new.json",\n))\n'
             'ORIGINAL_SCORED_BEFORE_FILING_SHA256')],
           "test_the_scored_before_filing_list_only_shrinks",
           "a name added to the scored-before-filing list")
