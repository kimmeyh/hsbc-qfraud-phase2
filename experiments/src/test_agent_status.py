"""`scripts/agent_status.py` reports each state from files (F168 part 5).

Every case runs on a scratch tree; the script stores nothing.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "agent_status.py"
THIS = Path(__file__).relative_to(ROOT).as_posix()
sys.path.insert(0, str(ROOT / "scripts"))
import agent_status as ags  # noqa: E402

SHA = "a" * 64
RID = "0" * 32


def _tree(tmp_path: Path) -> Path:
    claude = tmp_path / ".claude"
    (claude / "agent_progress").mkdir(parents=True)
    (claude / "sprint_status.json").write_text(json.dumps({"current_sprint": {
        "number": 30, "status": "phase_4_execution",
        "task_started": {"A": "t", "C": "t", "D": "t"},
        "task_actuals": {"A": 10}, "task_paused": {"D": "t"}}}),
        encoding="utf-8")
    prog = claude / "agent_progress"
    (prog / "fresh").mkdir()
    for name, lines in {"bare": ["started t"],
                        "half": ["started t", "unit 1 t f.md",
                                 "unit 2 t g.md"],
                        "done": ["started t", "unit 1 t f.md", "DONE"]}.items():
        (prog / name).mkdir()
        (prog / name / "progress.md").write_text("\n".join(lines) + "\n",
                                                 encoding="utf-8")
    res = tmp_path / "experiments" / "phase2" / "results"
    (res / "device_samples" / "intents").mkdir(parents=True)
    for name, doc in {"whole.json": {"complete": True},
                      "running.json": {"complete": False,
                                       "provenance": {"run_id": RID}},
                      "orphan.json": {"complete": False,
                                      "provenance": {"run_id": RID}},
                      "legacy.json": {"rows": []}}.items():
        (res / name).write_text(json.dumps(doc), encoding="utf-8")
    (res / "running.json.run_id").write_text(RID + "\n", encoding="utf-8")
    (res / "device_samples" / "intents" / f"{SHA}_f999_u1.json").write_text(
        "{}", encoding="utf-8")
    (res / "device_samples" / "b4_backfill.json").write_text(
        json.dumps({"job_id": "x"}), encoding="utf-8")
    return tmp_path


def test_each_state_is_reported(tmp_path):
    lines = ags.report(_tree(tmp_path))
    text = "\n".join(lines)
    assert ("sprint 30: phase_4_execution; finished ['A']; timed ['C']; "
            "paused ['D']") in text
    assert "agent fresh: not started" in text
    assert "agent bare: started, nothing saved" in text
    assert "agent half: in progress, 2 unit(s); last: unit 2 t g.md" in text
    assert "agent done: finished, 1 unit(s)" in text
    assert "run running.json: in progress, resumable" in text
    assert "run orphan.json: not complete and NOT resumable" in text
    assert "legacy.json" not in text and "whole.json" not in text
    assert "runs: 1 complete" in text
    assert f"device {SHA}_f999_u1.json: sent, NO response saved" in text
    assert "1 response file(s) with no problem hash" in text


def test_a_saved_response_clears_its_intent(tmp_path):
    root = _tree(tmp_path)
    store = root / "experiments" / "phase2" / "results" / "device_samples"
    (store / "f999_u1_job.json").write_text(
        json.dumps({"problem_sha256": SHA}), encoding="utf-8")
    text = "\n".join(ags.report(root))
    assert "NO response saved" not in text
    assert "1 problem(s) with a saved response" in text


def test_it_stores_nothing(tmp_path):
    root = _tree(tmp_path)
    before = sorted((p.relative_to(root), p.stat().st_mtime_ns)
                    for p in root.rglob("*"))
    ags.main(["--root", str(root)])
    after = sorted((p.relative_to(root), p.stat().st_mtime_ns)
                   for p in root.rglob("*"))
    assert before == after


def test_a_missing_status_file_is_said():
    assert "status file missing" in ags.sprint(Path("/nonexistent"))[0]


def test_the_states_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    run = lambda: run_pytest(f"{THIS}::test_each_state_is_reported",  # noqa: E731
                             ROOT)
    assert_can_fail([Mutation(SCRIPT, '        if units and units[-1] == '
                              '"DONE":\n', "        if False:\n",
                              expect_occurrences=1)],
                    run, "a finished agent reported as in progress")
    assert_can_fail([Mutation(SCRIPT, "        if run_id and first and "
                              "first[0].strip() == run_id:\n",
                              "        if run_id:\n", expect_occurrences=1)],
                    run, "a run with no sidecar reported as resumable")
    assert_can_fail([Mutation(SCRIPT, "        if sha not in hashed:\n",
                              "        if False:\n", expect_occurrences=1)],
                    run, "a sent job with no response not reported")
