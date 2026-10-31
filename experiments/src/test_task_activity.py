"""A task's actual is work, not elapsed time (F175, Sprint 30).

Sprint 29's actuals for four of nine tasks were elapsed time: the timers
ran across overnight breaks and the F159 hang. `.claude/hooks/
log_task_activity.py` writes a timestamp per tool call while a timer runs,
and `update_sprint_status.py --finish-task` subtracts every gap of more
than 30 minutes between them. These tests work on scratch copies only.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / ".claude" / "hooks" / "log_task_activity.py"
SCRIPT = ROOT / "scripts" / "update_sprint_status.py"
THIS = Path(__file__).relative_to(ROOT).as_posix()
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(HOOK.parent))

import log_task_activity as lta  # noqa: E402
import update_sprint_status as uss  # noqa: E402

T0 = datetime(2026, 10, 31, 9, 0, 0, tzinfo=timezone(timedelta(hours=-4)))


def _status(tmp_path: Path, **cur) -> Path:
    (tmp_path / ".claude").mkdir(exist_ok=True)
    p = tmp_path / ".claude" / "sprint_status.json"
    p.write_text(json.dumps({"current_sprint": {"number": 99,
                                                "task_actuals": {}, **cur}}),
                 encoding="utf-8")
    return p


def _log(p: Path, minutes) -> None:
    (p.parent / "activity.log").write_text(
        "".join((T0 + timedelta(minutes=m)).isoformat() + "\n"
                for m in minutes), encoding="utf-8")


def _run(p: Path, args, minutes):
    uss.main(["--path", str(p), *args], now=T0 + timedelta(minutes=minutes))


def _cur(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))["current_sprint"]


def test_an_eight_hour_gap_is_not_work(tmp_path):
    # Work 0-60, an overnight 8 hours with no tool call, work 540-600.
    p = _status(tmp_path)
    _run(p, ["--start-task", "C"], 0)
    _log(p, [*range(0, 61, 5), *range(540, 601, 5)])
    _run(p, ["--finish-task", "C"], 600)
    cur = _cur(p)
    assert cur["task_elapsed"]["C"] == 600
    assert cur["task_actuals"]["C"] == 120


def test_activity_every_ten_minutes_subtracts_nothing(tmp_path):
    p = _status(tmp_path)
    _run(p, ["--start-task", "C"], 0)
    _log(p, range(0, 181, 10))
    _run(p, ["--finish-task", "C"], 180)
    assert _cur(p)["task_actuals"]["C"] == 180


def test_a_gap_of_exactly_thirty_minutes_is_work(tmp_path):
    p = _status(tmp_path)
    _run(p, ["--start-task", "C"], 0)
    _log(p, [0, 30, 60])
    _run(p, ["--finish-task", "C"], 60)
    assert _cur(p)["task_actuals"]["C"] == 60


def test_a_pause_with_no_activity_is_subtracted_once(tmp_path):
    # Paused 10-70 (an approval wait) and no tool call in it: 60 minutes
    # out, not 120.
    p = _status(tmp_path)
    _run(p, ["--start-task", "D"], 0)
    _run(p, ["--pause-task", "D"], 10)
    _run(p, ["--resume-task", "D"], 70)
    _log(p, [0, 5, 10, 70, 75, 80, 85, 90])
    _run(p, ["--finish-task", "D"], 90)
    assert _cur(p)["task_actuals"]["D"] == 30


def test_no_activity_log_falls_back_to_elapsed_and_says_so(tmp_path, capsys):
    p = _status(tmp_path)
    _run(p, ["--start-task", "C"], 0)
    _run(p, ["--finish-task", "C"], 600)
    assert _cur(p)["task_actuals"]["C"] == 600
    assert "no activity log" in capsys.readouterr().out


def test_the_hook_logs_only_while_a_timer_runs(tmp_path):
    log = tmp_path / ".claude" / "activity.log"
    _status(tmp_path, task_started={"A": "t"}, task_actuals={"A": 5})
    assert lta.log(tmp_path, T0) is False and not log.exists()
    _status(tmp_path, task_started={"B": "t"}, task_paused={"B": "t"})
    assert lta.log(tmp_path, T0) is False and not log.exists()
    _status(tmp_path, task_started={"B": "t"})
    assert lta.log(tmp_path, T0) is True
    assert log.read_text(encoding="utf-8") == T0.isoformat() + "\n"


def test_the_hook_never_blocks(tmp_path):
    # No status file at all: the hook exits 0 and writes nothing.
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(tmp_path)}
    (tmp_path / ".claude").mkdir()
    r = subprocess.run([sys.executable, str(HOOK)], input="{}", env=env,
                       capture_output=True, text=True)
    assert r.returncode == 0
    assert not (tmp_path / ".claude" / "activity.log").exists()


def test_the_gap_rule_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest

    def test(name):
        return lambda: run_pytest(f"{THIS}::{name}", ROOT)
    assert_can_fail([Mutation(SCRIPT,
                              "             if (b - a).total_seconds() > "
                              "IDLE_GAP_S]\n",
                              "             if False]\n",
                              expect_occurrences=1)],
                    test("test_an_eight_hour_gap_is_not_work"),
                    "an 8-hour gap counted as work")
    assert_can_fail([Mutation(SCRIPT, "IDLE_GAP_S = 30 * 60\n",
                              "IDLE_GAP_S = 5 * 60\n", expect_occurrences=1)],
                    test("test_activity_every_ten_minutes_subtracts_nothing"),
                    "ordinary work counted as a break")
    assert_can_fail([Mutation(SCRIPT, "            a = reach\n",
                              "            pass\n", expect_occurrences=1)],
                    test("test_a_pause_with_no_activity_is_subtracted_once"),
                    "a pause subtracted twice")
    assert_can_fail([Mutation(HOOK,
                              "    if not timing(claude / "
                              "\"sprint_status.json\"):\n",
                              "    if False:\n", expect_occurrences=1)],
                    test("test_the_hook_logs_only_while_a_timer_runs"),
                    "the hook logging with no timer running")
