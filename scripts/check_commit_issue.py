"""A feature or fix commit on a sprint branch names its issue (Sprint 28 IMP-4).

Called by `.githooks/commit-msg` with the message file. Sprint 28's D4 was
added at Manual Validation and built in two commits with no issue and no
timer, although `SPRINT_CHECKLIST.md` Phase 4 requires both; the rule
relied on memory. This makes the issue a condition of the commit.

On a branch named `*Sprint_<n>*`, a commit whose subject starts `feat` or
`fix` must name, anywhere in its message, either an issue `#N` listed in
`.claude/sprint_status.json` `current_sprint.github_issues`, or the sprint
PR's review as `PR <pr> review`; and some task timer must be running, a
task in `task_started` with no `task_actuals` entry and not in
`task_paused` (Sprint 29 IMP-4: Task C's timer was never started, and E
and G were started only when their runs began). The running timer must
be the commit's OWN task's (F173, Sprint 30): each named issue's task is
read from `task_issues` (set by `update_sprint_status.py --add-issue N
--task X`), and a "PR n review" commit's task from `review_task`
(`--review-task X`). Any running timer used to pass, so Task C's commit
5348add (#66) would have passed while only D's and H's timers ran. A
named sprint issue with no task, or a review commit with no review task,
blocks. Other types (docs, chore, test, process), merges and reverts
pass. A status file that is missing, unreadable or for
another branch blocks: "could not tell" is not a pass. No override flag.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

TYPED = re.compile(r"^(feat|fix)(\([^)]*\))?!?:")
SPRINT_BRANCH = re.compile(r"Sprint_\d+")
COMMENT = re.compile(r"#(\s|$)")


def _git(*args: str, cwd: Path) -> str:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True,
                          text=True, check=True).stdout.strip()


def problem(message: str, branch: str, status) -> str | None:
    """Why the commit is refused, or None."""
    lines = []
    for ln in message.splitlines():
        if ln.startswith("#") and ">8" in ln:      # git's scissors line
            break
        # git's own comment lines are "#" or "# ..."; a line that starts
        # "#61" is the message naming an issue and stays.
        if not COMMENT.match(ln):
            lines.append(ln)
    subject = next((ln for ln in lines if ln.strip()), "")
    if subject.startswith(("Merge", "Revert")) or not TYPED.match(subject):
        return None
    if not SPRINT_BRANCH.search(branch):
        return None
    cur = status.get("current_sprint") if isinstance(status, dict) else None
    if not isinstance(cur, dict):
        return ("the sprint status file could not be read; check "
                ".claude/sprint_status.json")
    if cur.get("branch") != branch:
        return ("the sprint status file does not describe this branch "
                f"({branch}); update it with scripts/update_sprint_status.py")
    body = "\n".join(lines)
    issues = {int(n) for n in cur.get("github_issues") or []}
    named = {int(n) for n in re.findall(r"#(\d+)\b", body)}
    pr = cur.get("pr")
    review = pr is not None and re.search(rf"\bPR #?{int(pr)} review", body)
    if not (named & issues or review):
        return ("a feat or fix commit on a sprint branch names its task "
                f"issue (#N from github_issues: {sorted(issues)}) or "
                f"'PR {pr} review'. A task added mid-sprint gets an issue "
                "(gh issue create) and scripts/update_sprint_status.py "
                "--add-issue N first")
    running = timed(cur)
    if not running:
        return ("a feat or fix commit on a sprint branch needs a task "
                "timer running: scripts/update_sprint_status.py "
                "--start-task X (or --resume-task X) first")
    owner = owners(cur)
    unowned = sorted(n for n in named & issues if n not in owner)
    if unowned:
        return (f"issue(s) {unowned} belong to no task in task_issues; "
                "record the owner with scripts/update_sprint_status.py "
                "--add-issue N --task X")
    own = {owner[n] for n in named & issues}
    if review:
        if not cur.get("review_task"):
            return (f"a 'PR {pr} review' commit is timed against the review "
                    "task, and none is set: scripts/update_sprint_status.py "
                    "--review-task X")
        own.add(cur["review_task"])
    if not own & set(running):
        return (f"this commit's task(s) {sorted(own)} are not being timed "
                f"(timed: {running}); --start-task or --resume-task the "
                "commit's own task first")
    return None


def owners(cur: dict) -> dict[int, str]:
    """Issue number -> the task that owns it, from `task_issues`."""
    value = cur.get("task_issues")
    out: dict[int, str] = {}
    for task, numbers in (value.items() if isinstance(value, dict) else ()):
        for n in numbers if isinstance(numbers, list) else ():
            out[int(n)] = task
    return out


def timed(cur: dict) -> list[str]:
    """Tasks started, not finished and not paused: the ones being timed
    (the same rule as `update_sprint_status.open_tasks`)."""
    def part(name: str) -> dict:
        value = cur.get(name)
        return value if isinstance(value, dict) else {}
    return sorted(t for t in part("task_started")
                  if t not in part("task_actuals")
                  and t not in part("task_paused"))


def main(argv: list[str]) -> int:
    msg = Path(argv[1]).read_text(encoding="utf-8")
    root = Path(_git("rev-parse", "--show-toplevel", cwd=Path.cwd()))
    # symbolic-ref answers on an unborn branch, where rev-parse fails; a
    # detached HEAD is on no branch, so no sprint rule applies.
    branch = subprocess.run(["git", "symbolic-ref", "--short", "-q", "HEAD"],
                            cwd=root, capture_output=True,
                            text=True).stdout.strip()
    try:
        status = json.loads((root / ".claude" / "sprint_status.json")
                            .read_text(encoding="utf-8"))
    except (OSError, ValueError):
        status = None
    why = problem(msg, branch, status)
    if why:
        print(f"BLOCKED: {why}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
