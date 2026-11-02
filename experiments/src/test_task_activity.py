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

import update_sprint_status as uss  # noqa: E402


def _load_hook():
    # Loaded by path, as test_hooklib.py loads hooklib: a hook is not a
    # module on any import path, and an `import` of it reads to
    # test_requirements_complete.py as an undeclared package.
    import importlib.util
    spec = importlib.util.spec_from_file_location("log_task_activity", HOOK)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


lta = _load_hook()

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


def test_a_log_with_nothing_in_the_task_falls_back_and_says_so(tmp_path,
                                                               capsys):
    # PR 74 review: a log that exists but holds nothing inside the task (the
    # hook unregistered or failing) made a 3-hour task an actual of 1 minute.
    p = _status(tmp_path)
    _run(p, ["--start-task", "C"], 0)
    _log(p, [-24 * 60])
    _run(p, ["--finish-task", "C"], 180)
    cur = _cur(p)
    assert cur["task_actuals"]["C"] == 180
    assert "no activity logged during the task" in capsys.readouterr().out
    assert "no activity logged" in cur["task_actual_method"]["C"]


def test_a_mostly_idle_task_and_unreadable_lines_are_flagged(tmp_path):
    p = _status(tmp_path)
    _run(p, ["--start-task", "C"], 0)
    (p.parent / "activity.log").write_text(
        "not a time\n" + "".join((T0 + timedelta(minutes=m)).isoformat() + "\n"
                                 for m in (0, 10, 170, 180)),
        encoding="utf-8")
    _run(p, ["--finish-task", "C"], 180)
    how = _cur(p)["task_actual_method"]["C"]
    assert "over half the elapsed time had no tool call" in how
    assert "1 unreadable line(s)" in how


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
    # The error is kept, so --finish-task can say the log may be short.
    assert "FileNotFoundError" in (
        tmp_path / ".claude" / "activity.err").read_text(encoding="utf-8")


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
    assert_can_fail([Mutation(SCRIPT,
                              "    elif not any(start < p < now for p in points):\n",
                              "    elif False:\n", expect_occurrences=1)],
                    test("test_a_log_with_nothing_in_the_task_falls_back_"
                         "and_says_so"),
                    "a stale log making a task one idle gap")
    assert_can_fail([Mutation(SCRIPT,
                              "        if idle - paused_s > elapsed / 2:\n",
                              "        if False:\n", expect_occurrences=1)],
                    test("test_a_mostly_idle_task_and_unreadable_lines_are_"
                         "flagged"),
                    "a mostly idle task left unflagged")
    assert_can_fail([Mutation(HOOK,
                              "            with open(root / \".claude\" / "
                              "\"activity.err\", \"a\",\n",
                              "            with open(root / \".claude\" / "
                              "\"activity.nul\", \"a\",\n",
                              expect_occurrences=1)],
                    test("test_the_hook_never_blocks"),
                    "a hook error left unrecorded")
