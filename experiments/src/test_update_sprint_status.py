"""Task actuals are measured from a recorded start, never judged at the end.

F136 (Sprint 23 retrospective IMP-3). Sprint 23 Task A's "20 minutes" was
written at completion with no start time recorded, so the velocity log
carried an estimate of an actual. `update_sprint_status.py --start-task` and
`--finish-task` record the start and compute the actual from it. These tests
work on a copy of the status file, never the real one.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import update_sprint_status as uss  # noqa: E402

T0 = datetime(2026, 10, 9, 12, 0, 0, tzinfo=timezone(timedelta(hours=-4)))


@pytest.fixture
def status(tmp_path):
    p = tmp_path / "sprint_status.json"
    p.write_text(json.dumps({
        "current_sprint": {"number": 99, "status": "phase_4_execution",
                           "task_actuals": {}},
    }), encoding="utf-8")
    return p


def _cur(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))["current_sprint"]


def test_start_then_finish_records_the_measured_minutes(status):
    uss.main(["--path", str(status), "--start-task", "C"], now=T0)
    assert _cur(status)["task_started"]["C"] == T0.isoformat(timespec="seconds")
    uss.main(["--path", str(status), "--finish-task", "C"],
             now=T0 + timedelta(minutes=41, seconds=10))
    assert _cur(status)["task_actuals"]["C"] == 42, "rounded up to the minute"


def test_a_finish_with_no_recorded_start_is_refused(status):
    """The defect this exists for: an actual with no start is a guess."""
    with pytest.raises(SystemExit, match="no recorded start"):
        uss.main(["--path", str(status), "--finish-task", "C"], now=T0)
    assert "C" not in _cur(status)["task_actuals"]


def test_a_second_start_is_refused(status):
    """Moving the stamp later would shorten the measured actual."""
    uss.main(["--path", str(status), "--start-task", "C"], now=T0)
    with pytest.raises(SystemExit, match="already started"):
        uss.main(["--path", str(status), "--start-task", "C"],
                 now=T0 + timedelta(minutes=30))
    assert _cur(status)["task_started"]["C"] == T0.isoformat(timespec="seconds")


def test_a_second_finish_is_refused(status):
    uss.main(["--path", str(status), "--start-task", "C"], now=T0)
    uss.main(["--path", str(status), "--finish-task", "C"],
             now=T0 + timedelta(minutes=5))
    with pytest.raises(SystemExit, match="already has an actual"):
        uss.main(["--path", str(status), "--finish-task", "C"],
                 now=T0 + timedelta(minutes=50))
    assert _cur(status)["task_actuals"]["C"] == 5


def test_a_new_sprint_starts_with_an_empty_start_record(status):
    uss.main(["--path", str(status), "--new-sprint", "100", "--name", "x",
              "--branch", "b", "--plan-doc", "p"], now=T0)
    assert _cur(status)["task_started"] == {}


def _issues_behave(path: Path) -> bool:
    """--add-issue appends once, keeps the list sorted, refuses nonsense."""
    path.write_text(json.dumps({"current_sprint": {
        "number": 99, "github_issues": [13, 18]}}), encoding="utf-8")
    uss.main(["--path", str(path), "--add-issue", "19", "--add-issue", "15"])
    uss.main(["--path", str(path), "--add-issue", "19"])
    if _cur(path)["github_issues"] != [13, 15, 18, 19]:
        return False
    try:
        uss.main(["--path", str(path), "--add-issue", "0"])
    except SystemExit:
        return _cur(path)["github_issues"] == [13, 15, 18, 19]
    return False


def test_add_issue_appends_once_sorted_and_refuses_nonsense(status):
    """Sprint 25 IMP-4: `--set` cannot append, so #19 was never recorded."""
    assert _issues_behave(status)


def test_add_issue_guard_can_fail(tmp_path):
    import importlib

    from injection import Mutation, assert_can_fail
    src = ROOT / "scripts" / "update_sprint_status.py"
    target = tmp_path / "s.json"

    def run() -> bool:
        # The mutation edits the source file; reload so the run sees it.
        importlib.reload(uss)
        return _issues_behave(target)

    try:
        assert_can_fail(
            [Mutation(src, "    if number in issues:\n",
                      "    if False:\n", expect_occurrences=1)],
            run, "a duplicate issue is appended twice")
        assert_can_fail(
            [Mutation(src, "        issues.sort()\n", "",
                      expect_occurrences=1)],
            run, "the list is left unsorted")
        assert_can_fail(
            [Mutation(src, "    if number <= 0:\n", "    if False:\n",
                      expect_occurrences=1)],
            run, "a nonpositive issue number is accepted")
    finally:
        importlib.reload(uss)


def _timers_behave(path: Path) -> bool:
    """Sprint 26 IMP-2: a pause stays out of the actual; a second open task
    needs --parallel, which is recorded."""
    path.write_text(json.dumps({"current_sprint": {
        "number": 99, "task_actuals": {}}}), encoding="utf-8")
    m = lambda a, t: uss.main(["--path", str(path)] + a,  # noqa: E731
                              now=T0 + timedelta(minutes=t))
    m(["--start-task", "D"], 0)
    m(["--pause-task", "D"], 10)
    m(["--resume-task", "D"], 70)              # an hour awaiting approval
    try:
        m(["--start-task", "E"], 71)
        return False                           # D is open: must be refused
    except SystemExit:
        pass
    m(["--start-task", "E", "--parallel"], 71)
    m(["--finish-task", "D"], 75)
    cur = _cur(path)
    return (cur["task_actuals"]["D"] == 15
            and cur.get("task_parallel") == {"E": ["D"]})


def test_pause_and_parallel_are_measured(tmp_path):
    assert _timers_behave(tmp_path / "s.json")


def test_a_paused_task_cannot_finish(status):
    uss.main(["--path", str(status), "--start-task", "D"], now=T0)
    uss.main(["--path", str(status), "--pause-task", "D"], now=T0)
    with pytest.raises(SystemExit, match="is paused"):
        uss.main(["--path", str(status), "--finish-task", "D"],
                 now=T0 + timedelta(minutes=5))


def test_timer_guards_can_fail(tmp_path):
    import importlib

    from injection import Mutation, assert_can_fail
    src = ROOT / "scripts" / "update_sprint_status.py"
    target = tmp_path / "s.json"

    def run() -> bool:
        importlib.reload(uss)
        return _timers_behave(target)

    try:
        assert_can_fail(
            [Mutation(src, "        idle, how = paused_s, ",
                      "        idle, how = 0, ", expect_occurrences=1)],
            run, "the pause counted as work")
        assert_can_fail(
            [Mutation(src, "    if running and not parallel:\n",
                      "    if False:\n", expect_occurrences=1)],
            run, "a second open task started silently")
        assert_can_fail(
            [Mutation(src, "        cur.setdefault(\"task_parallel\", {})"
                      "[task] = running\n", "        pass\n",
                      expect_occurrences=1)],
            run, "a parallel start not recorded")
    finally:
        importlib.reload(uss)


def test_the_clock_cannot_be_set_from_the_command_line():
    """`now` is for tests only. A flag that sets the clock would let an
    actual be typed in after all."""
    src = (ROOT / "scripts" / "update_sprint_status.py").read_text(
        encoding="utf-8")
    assert '"--now"' not in src and "'--now'" not in src


# F173 (Sprint 30): each issue's task, read by the commit-msg hook.

def test_add_issue_with_a_task_records_its_owner(status):
    uss.main(["--path", str(status), "--add-issue", "75", "--add-issue",
              "84", "--task", "A"], now=T0)
    cur = _cur(status)
    assert cur["github_issues"] == [75, 84]
    assert cur["task_issues"] == {"A": [75, 84]}
    # An issue already listed can still be given its owner.
    uss.main(["--path", str(status), "--add-issue", "76"], now=T0)
    uss.main(["--path", str(status), "--add-issue", "76", "--task", "B"],
             now=T0)
    assert _cur(status)["task_issues"]["B"] == [76]


def test_an_issue_cannot_have_two_owners(status):
    uss.main(["--path", str(status), "--add-issue", "75", "--task", "A"],
             now=T0)
    with pytest.raises(SystemExit, match="already belongs to task A"):
        uss.main(["--path", str(status), "--add-issue", "75", "--task", "B"],
                 now=T0)
    assert _cur(status)["task_issues"] == {"A": [75]}


def test_a_task_without_an_issue_is_refused(status):
    with pytest.raises(SystemExit, match="--add-issue"):
        uss.main(["--path", str(status), "--task", "A"], now=T0)


def test_the_review_task_is_recorded(status):
    uss.main(["--path", str(status), "--review-task", "J"], now=T0)
    assert _cur(status)["review_task"] == "J"


def test_a_new_sprint_starts_with_no_owners(status):
    uss.main(["--path", str(status), "--new-sprint", "100"], now=T0)
    cur = _cur(status)
    assert cur["task_issues"] == {} and cur["review_task"] is None


def test_the_one_owner_rule_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    src = ROOT / "scripts" / "update_sprint_status.py"
    this = Path(__file__).relative_to(ROOT).as_posix()
    assert_can_fail(
        [Mutation(src, "        if other:\n", "        if False:\n",
                  expect_occurrences=1)],
        lambda: run_pytest(f"{this}::test_an_issue_cannot_have_two_owners",
                           ROOT),
        "an issue given a second owner")
