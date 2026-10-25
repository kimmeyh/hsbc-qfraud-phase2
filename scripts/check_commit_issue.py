"""A feature or fix commit on a sprint branch names its issue (Sprint 28 IMP-4).

Called by `.githooks/commit-msg` with the message file. Sprint 28's D4 was
added at Manual Validation and built in two commits with no issue and no
timer, although `SPRINT_CHECKLIST.md` Phase 4 requires both; the rule
relied on memory. This makes the issue a condition of the commit.

On a branch named `*Sprint_<n>*`, a commit whose subject starts `feat` or
`fix` must name, anywhere in its message, either an issue `#N` listed in
`.claude/sprint_status.json` `current_sprint.github_issues`, or the sprint
PR's review as `PR <pr> review`. Other types (docs, chore, test, process),
merges and reverts pass. A status file that is missing, unreadable or for
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


def _git(*args: str, cwd: Path) -> str:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True,
                          text=True, check=True).stdout.strip()


def problem(message: str, branch: str, status) -> str | None:
    """Why the commit is refused, or None."""
    lines = [ln for ln in message.splitlines() if not ln.startswith("#")]
    subject = next((ln for ln in lines if ln.strip()), "")
    if subject.startswith(("Merge", "Revert")) or not TYPED.match(subject):
        return None
    if not SPRINT_BRANCH.search(branch):
        return None
    cur = status.get("current_sprint") if isinstance(status, dict) else None
    if not isinstance(cur, dict) or cur.get("branch") != branch:
        return ("the sprint status file does not describe this branch "
                f"({branch}); update it with scripts/update_sprint_status.py")
    body = "\n".join(lines)
    issues = {int(n) for n in cur.get("github_issues") or []}
    named = {int(n) for n in re.findall(r"#(\d+)\b", body)}
    pr = cur.get("pr")
    if named & issues:
        return None
    if pr is not None and re.search(rf"\bPR #?{int(pr)} review", body):
        return None
    return ("a feat or fix commit on a sprint branch names its task issue "
            f"(#N from github_issues: {sorted(issues)}) or 'PR {pr} review'. "
            "A task added mid-sprint gets an issue (gh issue create) and "
            "scripts/update_sprint_status.py --add-issue N first")


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
