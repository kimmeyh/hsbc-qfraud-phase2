"""PostToolUse hook: log a timestamp while a task timer runs (F175, Sprint 30).

Sprint 29's actuals for four of nine tasks were elapsed time, not work: the
timers ran across overnight breaks and the F159 hang. A timer cannot tell
work from a break by itself. This hook writes one ISO timestamp per tool
call to `.claude/activity.log` (gitignored) while any task is being timed;
`update_sprint_status.py --finish-task` subtracts every gap of more than 30
minutes between them, so a break with no tool call is not counted as work.

Never blocks: it always exits 0, and any error leaves the log as it was. A
missing log makes `--finish-task` fall back to elapsed time and say so, so
a failure here is visible in the record rather than silent.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hooklib import repo_root  # noqa: E402


def timing(status: Path) -> bool:
    """True when some task is started, not finished and not paused."""
    cur = json.loads(status.read_text(encoding="utf-8")).get("current_sprint")
    if not isinstance(cur, dict):
        return False

    def part(name: str) -> dict:
        value = cur.get(name)
        return value if isinstance(value, dict) else {}
    return any(t not in part("task_actuals") and t not in part("task_paused")
               for t in part("task_started"))


def log(root: Path, now: datetime) -> bool:
    """Append `now` to the activity log if a timer runs; True if written."""
    claude = root / ".claude"
    if not timing(claude / "sprint_status.json"):
        return False
    with open(claude / "activity.log", "a", encoding="utf-8") as f:
        f.write(now.isoformat(timespec="seconds") + "\n")
    return True


def main() -> int:
    try:
        sys.stdin.read()
        root = repo_root()
        log(root, datetime.now().astimezone())
    except Exception as exc:  # noqa: BLE001 -- a logging hook never blocks a tool
        # Kept, so `--finish-task` can say the log may be incomplete
        # (PR 74 review: a swallowed error was invisible).
        try:
            with open(root / ".claude" / "activity.err", "a",
                      encoding="utf-8") as f:
                f.write(f"{datetime.now().astimezone().isoformat()} "
                        f"{type(exc).__name__}: {exc}\n")
        except Exception:  # noqa: BLE001
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
