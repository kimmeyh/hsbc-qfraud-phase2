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


def test_the_clock_cannot_be_set_from_the_command_line():
    """`now` is for tests only. A flag that sets the clock would let an
    actual be typed in after all."""
    src = (ROOT / "scripts" / "update_sprint_status.py").read_text(
        encoding="utf-8")
    assert '"--now"' not in src and "'--now'" not in src
