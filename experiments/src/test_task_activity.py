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
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

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


def test_an_actual_under_a_fifth_of_its_estimate_is_flagged(tmp_path):
    # Sprint 30 IMP-3: A-C read 10, 11 and 15 against 45, 60 and 240.
    p = _status(tmp_path)
    _run(p, ["--start-task", "C", "--estimate", "240"], 0)
    _log(p, range(0, 41, 5))
    _run(p, ["--finish-task", "C"], 40)
    cur = _cur(p)
    assert cur["task_estimates"]["C"] == 240
    assert "under a fifth of its 240-minute estimate" in (
        cur["task_actual_method"]["C"])
    # At a fifth or more, nothing is flagged.
    _run(p, ["--task", "D", "--estimate", "200"], 40)
    _run(p, ["--start-task", "D"], 40)
    _log(p, range(40, 81, 5))
    _run(p, ["--finish-task", "D"], 80)
    assert "estimate" not in _cur(p)["task_actual_method"]["D"]


def test_an_estimate_is_set_once_and_positive(tmp_path):
    p = _status(tmp_path)
    _run(p, ["--task", "C", "--estimate", "60"], 0)
    with pytest.raises(SystemExit, match="already has an estimate"):
        _run(p, ["--task", "C", "--estimate", "600"], 1)
    with pytest.raises(SystemExit, match="positive number"):
        _run(p, ["--task", "D", "--estimate", "-5"], 1)
    # Zero is refused too, not dropped as "no estimate" (Task O review).
    with pytest.raises(SystemExit, match="positive number"):
        _run(p, ["--task", "D", "--estimate", "0"], 1)
    with pytest.raises(SystemExit, match="names two tasks"):
        _run(p, ["--start-task", "D", "--task", "E", "--estimate", "60"], 1)
    with pytest.raises(SystemExit, match="needs --start-task"):
        _run(p, ["--estimate", "60"], 1)


def test_a_repeated_equal_estimate_still_starts_the_timer(tmp_path):
    # Sprint 32 i1: Task A's `--start-task A --estimate N` after
    # `--task A --estimate N` was refused, so the timer never started.
    p = _status(tmp_path)
    _run(p, ["--task", "C", "--estimate", "60"], 0)
    _run(p, ["--start-task", "C", "--estimate", "60"], 1)
    assert "C" in _cur(p)["task_started"]
    assert _cur(p)["task_estimates"]["C"] == 60


def test_a_change_made_during_an_update_is_not_overwritten(tmp_path,
                                                           monkeypatch):
    # PR 74 review (Sprint 30 IMP-5): two updates at once each wrote the
    # whole file, so the second lost the first's change.
    p = _status(tmp_path)
    other = json.dumps({"current_sprint": {"number": 99, "task_actuals": {},
                                           "task_started": {"Z": "t"}}})
    orig = uss.start_task

    def racing(doc, task, now, parallel=False):
        p.write_text(other, encoding="utf-8")      # another update lands
        return orig(doc, task, now, parallel)
    monkeypatch.setattr(uss, "start_task", racing)
    with pytest.raises(SystemExit, match="changed while this update ran"):
        _run(p, ["--start-task", "C"], 0)
    assert p.read_text(encoding="utf-8") == other
    assert not list(p.parent.glob("sprint_status.json*.tmp"))


def test_the_review_task_does_not_move_off_a_running_task(tmp_path):
    p = _status(tmp_path, task_started={"J": T0.isoformat()},
                review_task="J")
    with pytest.raises(SystemExit, match="still running"):
        _run(p, ["--review-task", "M"], 10)
    assert _cur(p)["review_task"] == "J"
    _run(p, ["--finish-task", "J"], 20)
    _run(p, ["--review-task", "M"], 20)
    assert _cur(p)["review_task"] == "M"


def test_one_command_finishes_a_task_and_moves_the_review_task(tmp_path):
    # F179: --review-task ran before --finish-task, so this one command
    # refused, and the move took two commands.
    p = _status(tmp_path, task_started={"J": T0.isoformat()},
                review_task="J")
    _run(p, ["--finish-task", "J", "--review-task", "M"], 20)
    assert _cur(p)["review_task"] == "M"
    assert "J" in _cur(p)["task_actuals"]


def test_a_held_lock_refuses_and_names_the_lock(tmp_path, monkeypatch):
    p = _status(tmp_path)
    before = p.read_text(encoding="utf-8")
    lock = p.with_name(p.name + ".lock")
    lock.write_text("pid 1, earlier", encoding="utf-8")
    monkeypatch.setattr(uss, "LOCK_WAIT_S", 0.2)
    with pytest.raises(SystemExit, match="is locked by another update") as e:
        _run(p, ["--add-issue", "5"], 0)
    assert str(lock) in str(e.value) and "stale" in str(e.value)
    assert p.read_text(encoding="utf-8") == before
    # Another update's lock is never removed by the one it refused.
    assert lock.exists()


def test_a_refused_replace_writes_nothing_and_leaves_no_tmp(tmp_path,
                                                            monkeypatch):
    # Sprint 30: a running suite held the file open, os.replace raised
    # PermissionError twice, and each left a tmp file behind.
    p = _status(tmp_path)
    before = p.read_text(encoding="utf-8")

    def held(src, dst):
        raise PermissionError(13, "Access is denied")
    monkeypatch.setattr(uss.os, "replace", held)
    with pytest.raises(SystemExit, match="could not be replaced"):
        _run(p, ["--add-issue", "5"], 0)
    assert p.read_text(encoding="utf-8") == before
    assert not list(p.parent.glob("sprint_status.json*.tmp"))
    assert not p.with_name(p.name + ".lock").exists()


def test_two_updates_at_once_both_land(tmp_path):
    # F179: two processes. The first holds its update open; the second
    # starts inside that window. Both must succeed and both changes stay.
    p = _status(tmp_path)
    ready = tmp_path / "ready"
    driver = tmp_path / "slow_update.py"
    driver.write_text(
        "import sys, time\n"
        "from pathlib import Path\n"
        f"sys.path.insert(0, {str(SCRIPT.parent)!r})\n"
        "import update_sprint_status as uss\n"
        "orig = uss.add_issue\n"
        "def slow(doc, number, task=''):\n"
        # Held until the file changes or 5 s pass: with the lock, the
        # second update cannot change it, so this waits out the 5 s;
        # without it, the second writes and this one goes on at once.
        # Process start-up time cannot close the window early.
        f"    status = Path({str(p)!r})\n"
        "    raw = status.read_text(encoding='utf-8')\n"
        f"    Path({str(ready)!r}).write_text('x')\n"
        "    end = time.monotonic() + 5\n"
        "    while time.monotonic() < end and "
        "status.read_text(encoding='utf-8') == raw:\n"
        "        time.sleep(0.05)\n"
        "    return orig(doc, number, task)\n"
        "uss.add_issue = slow\n"
        f"sys.exit(uss.main(['--path', {str(p)!r}, '--add-issue', '5']))\n",
        encoding="utf-8")
    first = subprocess.Popen([sys.executable, str(driver)],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             text=True)
    for _ in range(600):
        if ready.exists() or first.poll() is not None:
            break
        time.sleep(0.05)
    assert ready.exists(), first.communicate()
    second = subprocess.run([sys.executable, str(SCRIPT), "--path", str(p),
                             "--add-issue", "7"],
                            capture_output=True, text=True, timeout=60)
    out, err = first.communicate(timeout=60)
    assert first.returncode == 0, err
    assert second.returncode == 0, second.stderr
    assert _cur(p)["github_issues"] == [5, 7]


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
    assert_can_fail([Mutation(SCRIPT,
                              "    if est and actuals[task] * 5 < est:\n",
                              "    if False:\n", expect_occurrences=1)],
                    test("test_an_actual_under_a_fifth_of_its_estimate_is_"
                         "flagged"),
                    "a low actual left unflagged")
    assert_can_fail([Mutation(SCRIPT, "    if task in estimates:\n",
                              "    if False:\n", expect_occurrences=1)],
                    test("test_an_estimate_is_set_once_and_positive"),
                    "an estimate moved after the work")
    assert_can_fail([Mutation(SCRIPT,
                              "    if estimates.get(task) == minutes:\n",
                              "    if False:\n", expect_occurrences=1)],
                    test("test_a_repeated_equal_estimate_still_starts_the_"
                         "timer"),
                    "an equal estimate refused, the timer not started")
    assert_can_fail([Mutation(SCRIPT, "    if minutes <= 0:\n",
                              "    if False:\n", expect_occurrences=1)],
                    test("test_an_estimate_is_set_once_and_positive"),
                    "a negative estimate accepted")
    assert_can_fail([Mutation(SCRIPT,
                              "        if args.start_task and args.task and "
                              "args.start_task != args.task:\n",
                              "        if False:\n", expect_occurrences=1)],
                    test("test_an_estimate_is_set_once_and_positive"),
                    "an estimate given two tasks")
    assert_can_fail([Mutation(SCRIPT, "    if args.estimate is not None:\n",
                              "    if args.estimate:\n",
                              expect_occurrences=1)],
                    test("test_an_estimate_is_set_once_and_positive"),
                    "an estimate of 0 dropped silently")
    assert_can_fail([Mutation(SCRIPT, "        if not owner:\n",
                              "        if False:\n", expect_occurrences=1)],
                    test("test_an_estimate_is_set_once_and_positive"),
                    "an estimate with no task accepted")
    assert_can_fail([Mutation(SCRIPT,
                              "    if path.read_text(encoding=\"utf-8\") "
                              "!= raw:\n",
                              "    if False:\n", expect_occurrences=1)],
                    test("test_a_change_made_during_an_update_is_not_"
                         "overwritten"),
                    "a concurrent change overwritten")
    assert_can_fail([Mutation(SCRIPT,
                              "        if before and before != "
                              "args.review_task and before in "
                              "open_tasks(cur):\n",
                              "        if False:\n", expect_occurrences=1)],
                    test("test_the_review_task_does_not_move_off_a_running_"
                         "task"),
                    "the review task moved off a running task")


def test_the_lock_and_the_order_can_fail():
    # F179 (Sprint 31): the lock, the replace refusal and the order. A
    # function of its own, so these proofs run without the ones above.
    from injection import Mutation, assert_can_fail, run_pytest

    def test(name):
        return lambda: run_pytest(f"{THIS}::{name}", ROOT)
    assert_can_fail([Mutation(SCRIPT,
                              "os.open(lock, os.O_CREAT | os.O_EXCL | "
                              "os.O_WRONLY)",
                              "os.open(lock, os.O_CREAT | os.O_WRONLY)",
                              expect_occurrences=1)],
                    test("test_two_updates_at_once_both_land"),
                    "a lock two updates can hold at once")
    assert_can_fail([Mutation(SCRIPT,
                              "        lock.unlink(missing_ok=True)\n",
                              "        pass\n", expect_occurrences=1)],
                    test("test_a_refused_replace_writes_nothing_and_leaves_"
                         "no_tmp"),
                    "a lock left behind by a refused update")
    assert_can_fail([Mutation(SCRIPT,
                              "lock is stale: delete that file and run "
                              "again.",
                              "run again.", expect_occurrences=1)],
                    test("test_a_held_lock_refuses_and_names_the_lock"),
                    "a held lock refused without saying it may be stale")
    assert_can_fail([Mutation(SCRIPT, "    except PermissionError as exc:\n",
                              "    except FileNotFoundError as exc:\n",
                              expect_occurrences=1)],
                    test("test_a_refused_replace_writes_nothing_and_leaves_"
                         "no_tmp"),
                    "a refused replace raised as a traceback")
    assert_can_fail([Mutation(SCRIPT,
                              "        tmp.unlink(missing_ok=True)\n"
                              "        raise SystemExit(f\"{path.name} could "
                              "not be replaced",
                              "        pass\n"
                              "        raise SystemExit(f\"{path.name} could "
                              "not be replaced", expect_occurrences=1)],
                    test("test_a_refused_replace_writes_nothing_and_leaves_"
                         "no_tmp"),
                    "a refused replace leaving its tmp file")
    assert_can_fail([Mutation(SCRIPT,
                              "    clock = now or datetime.now()."
                              "astimezone()\n",
                              "    clock = (now or datetime.now()."
                              "astimezone())\n"
                              "    _c = doc[\"current_sprint\"]\n"
                              "    if args.review_task and _c.get("
                              "\"review_task\") in open_tasks(_c):\n"
                              "        raise SystemExit(\"still running\")\n",
                              expect_occurrences=1)],
                    test("test_one_command_finishes_a_task_and_moves_the_"
                         "review_task"),
                    "the review task checked before the finish")
