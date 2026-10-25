"""New Phase 2 modules write JSON only through `provenance.write_result`.

Sprint 28 IMP-6 (team lead, 2026-10-24). PR #46's review found the same
defect in four places: f110 appended duplicate rows on a rerun, f111 and
f152 overwrote a recorded result in their default mode, and the backfill
replaced a result before checking it. Each was fixed in its own module.
`write_result` makes the safe write the only short one: it adds the
provenance block, refuses to replace another run's result without a stated
reason, and checks the written file before it takes the result's place.

The static rule, per module under `experiments/phase2/src`: a direct JSON
file write is a call to `json.dump(`, or a `.write_text(` or `.write(`
whose argument calls `json.dumps` or a helper whose name ends `_dump`.
Modules from before the rule keep their counted writes; a count may fall,
never rise (`frozen_list.check`), and a module not listed must have none.
The counts include log lines written with `json.dumps`, which are not
results; a new module writes its log lines from text it builds first, or
the count blocks it.

Stated gap: a write whose text was built in an earlier statement
(`text = json.dumps(...)`, then `.write_text(text)` or `fh.write(text)`)
is not counted. `backfill_outcomes.py` writes that way; a module written
to evade the rule could too.
"""
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
PHASE2 = ROOT / "experiments" / "phase2" / "src"
THIS = Path(__file__).relative_to(ROOT).as_posix()
sys.path.insert(0, str(PHASE2))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import frozen_list as fl  # noqa: E402
import provenance as prov  # noqa: E402

GENERATOR = PHASE2 / "provenance.py"

# Direct JSON writes per module on 2026-10-24, before the rule. A count may
# fall when a module moves to write_result; never add a name or raise one.
JSON_WRITES_BEFORE_RULE = {
    "device_store.py": 1, "emulator_sparsity.py": 1, "exp3_controls.py": 1,
    "f102_downsized_pair.py": 1, "f103_tier1.py": 1, "f104_gate_check.py": 1,
    "f106_dequant.py": 1, "f107_shots.py": 1, "f108_ceiling.py": 1,
    "f109_ladder.py": 1, "f110_scaling.py": 1, "f111_loke_protocol.py": 1,
    "f112_intervals.py": 1, "f114_calibrated_plugin.py": 1,
    "f115_cost_scaling.py": 1, "f126_sparsity_rule.py": 2,
    "f130_levers.py": 2, "f142_readout.py": 1, "f144_proxy_twin.py": 2,
    "f145_build_drift.py": 1, "f151_hgb_cause.py": 2,
    "f152_exp2_score.py": 5, "f153_exp3_design.py": 1,
    "f154_confusion.py": 1, "f162_in_pocket.py": 1, "ieee_harness.py": 2,
    "lever_screen.py": 2, "oracle_gap.py": 1,
    "recover_device_samples.py": 1, "run_dirac3s_verify.py": 3,
    "sample_size.py": 1, "soft_votes.py": 1, "validate_emulator.py": 1,
}
# The table as frozen on 2026-10-24, re-frozen 2026-10-25 before the merge
# when the improvement review found the fh.write(json.dumps(...)) shape
# (f152 and ieee_harness log lines). Never edit; lower the table above.
ORIGINAL_JSON_WRITES_2026_10_24 = {
    "device_store.py": 1, "emulator_sparsity.py": 1, "exp3_controls.py": 1,
    "f102_downsized_pair.py": 1, "f103_tier1.py": 1, "f104_gate_check.py": 1,
    "f106_dequant.py": 1, "f107_shots.py": 1, "f108_ceiling.py": 1,
    "f109_ladder.py": 1, "f110_scaling.py": 1, "f111_loke_protocol.py": 1,
    "f112_intervals.py": 1, "f114_calibrated_plugin.py": 1,
    "f115_cost_scaling.py": 1, "f126_sparsity_rule.py": 2,
    "f130_levers.py": 2, "f142_readout.py": 1, "f144_proxy_twin.py": 2,
    "f145_build_drift.py": 1, "f151_hgb_cause.py": 2,
    "f152_exp2_score.py": 5, "f153_exp3_design.py": 1,
    "f154_confusion.py": 1, "f162_in_pocket.py": 1, "ieee_harness.py": 2,
    "lever_screen.py": 2, "oracle_gap.py": 1,
    "recover_device_samples.py": 1, "run_dirac3s_verify.py": 3,
    "sample_size.py": 1, "soft_votes.py": 1, "validate_emulator.py": 1,
}
ORIGINAL_JSON_WRITES_SHA256 = (
    "b1cb963e600675734ffd51d9c189247d450a16728cd798d729924af772992f94")


def _calls_dumps(node) -> bool:
    for n in ast.walk(node):
        if isinstance(n, ast.Call):
            f = n.func
            name = f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", "")
            if name == "dumps" or name.endswith("_dump"):
                return True
    return False


def json_writes(src: str) -> int:
    n = 0
    for node in ast.walk(ast.parse(src)):
        if not isinstance(node, ast.Call):
            continue
        f = node.func
        if isinstance(f, ast.Attribute) and f.attr == "dump" \
                and isinstance(f.value, ast.Name) and f.value.id == "json":
            n += 1
        elif isinstance(f, ast.Attribute) and f.attr in ("write_text", "write") \
                and node.args and _calls_dumps(node.args[0]):
            n += 1
    return n


def counts(src_dir: Path = PHASE2) -> dict[str, int]:
    out = {}
    for p in sorted(src_dir.glob("*.py")):
        n = json_writes(p.read_text(encoding="utf-8"))
        if n:
            out[p.name] = n
    return out


def problems(src_dir: Path = PHASE2) -> list[str]:
    now = counts(src_dir)
    return [f"{name}: {n} direct JSON writes, "
            f"{JSON_WRITES_BEFORE_RULE.get(name, 0)} allowed"
            for name, n in sorted(now.items())
            if n > JSON_WRITES_BEFORE_RULE.get(name, 0)]


# ------------------------------------------------------------ the real tree
def test_new_json_writes_go_through_write_result():
    bad = problems()
    assert not bad, ("write results with provenance.write_result "
                     f"(Sprint 28 IMP-6): {bad}")


def test_the_frozen_table_only_shrinks():
    bad = fl.check(JSON_WRITES_BEFORE_RULE, ORIGINAL_JSON_WRITES_2026_10_24,
                   ORIGINAL_JSON_WRITES_SHA256)
    assert not bad, bad
    for name in JSON_WRITES_BEFORE_RULE:
        assert (PHASE2 / name).exists(), f"{name} is gone; remove it"


def test_the_scan_counts_each_shape():
    src = "\n".join(["OUT.write_text(json.dumps(doc, indent=1))",
                     "json.dump(doc, fh)",
                     "P.write_text(_dump(res), encoding='utf-8')",
                     "fh.write(json.dumps(doc))",
                     "LOG.write_text('plain text')",
                     "fh.write('plain text')",
                     "print(json.dumps(doc))"])
    assert json_writes(src) == 4


def test_the_scan_flags_a_new_writer(tmp_path):
    (tmp_path / "f170_new.py").write_text(
        "OUT.write_text(json.dumps({'auprc': 1}))", encoding="utf-8")
    assert problems(tmp_path) == [
        "f170_new.py: 1 direct JSON writes, 0 allowed"]


# ------------------------------------------------------------ write_result
RUN1, RUN2 = "a" * 32, "b" * 32


def _write(tmp_path, run, replace=None, doc=None):
    return prov.write_result(tmp_path / "r.json", doc or {"auprc": 0.5},
                             GENERATOR, [42], run, replace=replace)


def test_a_new_result_carries_a_complete_block(tmp_path):
    out = _write(tmp_path, RUN1, doc={"n": np.int64(3), "ok": np.bool_(True)})
    back = json.loads((tmp_path / "r.json").read_text(encoding="utf-8"))
    assert back == out and back["n"] == 3 and back["ok"] is True
    assert prov.problems(back["provenance"]) == []
    assert back["provenance"]["run_id"] == RUN1


def test_the_same_run_may_rewrite_its_own_file(tmp_path):
    _write(tmp_path, RUN1)
    _write(tmp_path, RUN1, doc={"auprc": 0.6})
    back = json.loads((tmp_path / "r.json").read_text(encoding="utf-8"))
    assert back["auprc"] == 0.6 and "replaces" not in back["provenance"]


def test_another_runs_result_is_refused_and_left_alone(tmp_path):
    _write(tmp_path, RUN1)
    before = (tmp_path / "r.json").read_bytes()
    with pytest.raises(FileExistsError):
        _write(tmp_path, RUN2, doc={"auprc": 0.1})
    assert (tmp_path / "r.json").read_bytes() == before
    assert sorted(p.name for p in tmp_path.iterdir()) == ["r.json"]


def test_a_result_from_before_the_rule_is_refused(tmp_path):
    (tmp_path / "r.json").write_text('{"auprc": 0.9}', encoding="utf-8")
    with pytest.raises(FileExistsError):
        _write(tmp_path, RUN1)


def test_a_stated_replacement_is_recorded(tmp_path):
    _write(tmp_path, RUN1)
    out = _write(tmp_path, RUN2, replace="the full run replaces the pilot")
    assert out["provenance"]["replaces"] == {
        "reason": "the full run replaces the pilot", "previous_run_id": RUN1}
    # A later write of the same run keeps the record of what it replaced.
    out = _write(tmp_path, RUN2, doc={"auprc": 0.7})
    assert out["provenance"]["replaces"]["previous_run_id"] == RUN1


def test_a_blank_reason_or_run_id_is_refused(tmp_path):
    with pytest.raises(ValueError):
        _write(tmp_path, RUN1, replace="  ")
    with pytest.raises(ValueError):
        _write(tmp_path, "")
    assert not (tmp_path / "r.json").exists()


def test_a_constant_run_id_is_refused(tmp_path):
    # A runner passing a fixed name would rewrite its earlier result on
    # every rerun with no reason recorded (improvement review).
    with pytest.raises(ValueError):
        _write(tmp_path, "f170")
    assert not (tmp_path / "r.json").exists()
    assert prov.RUN_ID.fullmatch(prov.new_run_id())


def test_an_unknown_type_stops_the_write(tmp_path):
    with pytest.raises(TypeError):
        _write(tmp_path, RUN1, doc={"x": object()})
    assert list(tmp_path.iterdir()) == []


def test_a_file_that_does_not_read_back_is_refused(tmp_path, monkeypatch):
    _write(tmp_path, RUN1)
    before = (tmp_path / "r.json").read_bytes()
    real = Path.write_text

    def corrupting(self, text, *a, **kw):
        return real(self, text.replace('"auprc": 0.6', '"auprc": 0.4'),
                    *a, **kw)
    monkeypatch.setattr(Path, "write_text", corrupting)
    with pytest.raises(OSError):
        _write(tmp_path, RUN1, doc={"auprc": 0.6})
    assert (tmp_path / "r.json").read_bytes() == before
    assert sorted(p.name for p in tmp_path.iterdir()) == ["r.json"]


# ------------------------------------------------------------ rules can fail
SELF = Path(__file__)
WRITER = PHASE2 / "provenance.py"


def _fails(path, old, new, node, label):
    from injection import Mutation, assert_can_fail, run_pytest
    assert_can_fail([Mutation(path, old, new, expect_occurrences=1)],
                    lambda: run_pytest(f"{THIS}::{node}", ROOT), label)


def test_the_refusal_can_fail():
    _fails(WRITER, "            if replace is None:\n",
           "            if False:\n",
           "test_another_runs_result_is_refused_and_left_alone",
           "another run's result replaced")


def test_the_run_id_shape_check_can_fail():
    _fails(WRITER, "    if not isinstance(run_id, str) or not "
                   "RUN_ID.fullmatch(run_id):\n",
           "    if not run_id:\n",
           "test_a_constant_run_id_is_refused", "a constant run id")


def test_the_read_back_check_can_fail():
    _fails(WRITER, "        if back != json.loads(text):\n",
           "        if False:\n",
           "test_a_file_that_does_not_read_back_is_refused",
           "a file that does not read back")


def test_the_module_scan_can_fail():
    _fails(SELF, "            if n > JSON_WRITES_BEFORE_RULE.get(name, 0)]\n",
           "            if False]\n",
           "test_the_scan_flags_a_new_writer", "a new direct writer")


def test_the_frozen_table_can_fail():
    _fails(SELF, '    "f152_exp2_score.py": 5, "f153_exp3_design.py": 1,\n'
                 '    "f154_confusion.py": 1, "f162_in_pocket.py": 1, '
                 '"ieee_harness.py": 2,\n    "lever_screen.py": 2, '
                 '"oracle_gap.py": 1,\n    "recover_device_samples.py": 1, '
                 '"run_dirac3s_verify.py": 3,\n    "sample_size.py": 1, '
                 '"soft_votes.py": 1, "validate_emulator.py": 1,\n}\n# The',
           '    "f152_exp2_score.py": 5, "f153_exp3_design.py": 1,\n'
           '    "f154_confusion.py": 1, "f162_in_pocket.py": 2, '
           '"ieee_harness.py": 2,\n    "lever_screen.py": 2, '
           '"oracle_gap.py": 1,\n    "recover_device_samples.py": 1, '
           '"run_dirac3s_verify.py": 3,\n    "sample_size.py": 1, '
           '"soft_votes.py": 1, "validate_emulator.py": 1,\n}\n# The',
           "test_the_frozen_table_only_shrinks", "a count raised")
