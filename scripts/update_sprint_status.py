"""Update `.claude/sprint_status.json` without hand-editing it.

Converted from PowerShell 2026-09-17 (F78, Sprint 16).

Hand-editing that file is how it went stale twice: Sprint 12 ran with
`phase_4_execution` and `pr: null` against a sprint that had already merged two
PRs, and an automated reviewer quoted the stale value. Sprint 16 had
`plan_approved: true` with `pr: null` and an empty `github_issues` while ten
issues existed, caught by the close-out hook rather than by inspection.

Usage:
    python scripts/update_sprint_status.py --set status=phase_6_push
    python scripts/update_sprint_status.py --set pr=120 --set plan_approved=true
    python scripts/update_sprint_status.py --set last_completed_sprint.number=15
    python scripts/update_sprint_status.py --new-sprint 17 \\
        --name "The Next Thing" --branch feature/20260918_Sprint_17 \\
        --plan-doc docs/sprints/SPRINT_17_PLAN.md
    python scripts/update_sprint_status.py --start-task C
    python scripts/update_sprint_status.py --finish-task C
    python scripts/update_sprint_status.py --add-issue 19 --task C
    python scripts/update_sprint_status.py --review-task J

`--add-issue` appends an issue number to `github_issues`, once, keeping the
list sorted (Sprint 25 IMP-4: a task added at Manual Validation opened #19,
and `--set` cannot append to a list, so the file fell out of step).
With `--task X` it also records the issue under task X in `task_issues`,
which `.githooks/commit-msg` reads: a feat or fix commit is admitted only
while the task that owns its named issue is timed (F173, Sprint 30: the
hook accepted any running timer, so Task C's commit 5348add, #66, would
have passed while only D's and H's timers ran). `--review-task X` names
the task whose timer a "PR n review" commit needs, as Sprint 29's Task J
was.

`--pause-task X` and `--resume-task X` keep a wait, such as a metered stop
awaiting approval, out of the actual. `--start-task` refuses while another
task is being timed unless `--parallel` is passed, which is recorded in
`task_parallel` (Sprint 26 IMP-2).

`--start-task` stamps the task's start time in `task_started`. `--finish-task`
computes the actual from that stamp and writes it to `task_actuals` in whole
minutes, rounded up. A finish with no recorded start is refused (F136, Sprint
23 IMP-3): Sprint 23 Task A's "20 minutes" was judged at completion with no
start time, so the actual was an estimate of an actual.

Values are typed: `true`/`false` become booleans, `null` becomes null, digits
become integers, everything else stays a string. A bare key targets
`current_sprint`; a dotted key names its section.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import date, datetime
from pathlib import Path

STATUS = Path(__file__).resolve().parents[1] / ".claude" / "sprint_status.json"


def typed(value: str):
    low = value.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    if low == "null":
        return None
    if value.isdigit():
        return int(value)
    return value


def apply_set(doc: dict, assignment: str) -> str:
    if "=" not in assignment:
        raise SystemExit(f"--set needs key=value, got {assignment!r}")
    key, raw = assignment.split("=", 1)
    key = key.strip()

    section_name = "current_sprint"
    if "." in key:
        section_name, key = key.split(".", 1)

    if section_name not in doc:
        raise SystemExit(
            f"Unknown section {section_name!r} in {assignment!r}. "
            f"Sections: {', '.join(doc)}")

    section = doc[section_name]
    if not isinstance(section, dict):
        raise SystemExit(f"Section {section_name!r} is not an object")

    # An UNKNOWN KEY IS A HARD ERROR, never a silent add. Carried from the
    # PowerShell original, whose header stated it explicitly, and dropped by
    # mistake in the Sprint 16 conversion. Found by Copilot on PR #120.
    #
    # Why this matters more than catching a typo: `--set stauts=phase_6_push`
    # returned 0, created a bogus `stauts` field, and left the REAL status
    # stale. That is precisely the went-stale-twice failure this tool exists to
    # prevent, so a silent add makes the tool an instance of its own problem.
    if key not in section:
        raise SystemExit(
            f"Unknown key {key!r} in section {section_name!r} ({assignment!r}). "
            f"Known keys: {', '.join(sorted(section))}")

    before = section[key]
    section[key] = typed(raw)
    return f"  {section_name}.{key}: {before!r} -> {section[key]!r}"


def add_issue(doc: dict, number: int, task: str = "") -> str:
    if number <= 0:
        raise SystemExit(f"Issue number must be positive, got {number}.")
    cur = doc.setdefault("current_sprint", {})
    issues = cur.setdefault("github_issues", [])
    if number in issues:
        line = f"  current_sprint.github_issues: #{number} already listed"
    else:
        issues.append(number)
        issues.sort()
        line = f"  current_sprint.github_issues: added #{number} -> {issues}"
    if task:
        owners = cur.setdefault("task_issues", {})
        other = [t for t, ns in owners.items() if number in ns and t != task]
        if other:
            # One owner per issue, or the hook cannot tell whose timer a
            # commit naming it needs.
            raise SystemExit(f"Issue #{number} already belongs to task "
                             f"{other[0]}.")
        mine = owners.setdefault(task, [])
        if number not in mine:
            mine.append(number)
            mine.sort()
        line += f"; task_issues.{task}: {mine}"
    return line


def open_tasks(cur: dict) -> list[str]:
    """Tasks started, not finished and not paused: the ones being timed."""
    return sorted(t for t in cur.get("task_started", {})
                  if t not in cur.get("task_actuals", {})
                  and t not in cur.get("task_paused", {}))


def start_task(doc: dict, task: str, now: datetime,
               parallel: bool = False) -> str:
    """Stamp the start. A second start is refused: silently moving the stamp
    would shorten the measured actual.

    A start while another task is still being timed is refused unless
    `parallel` is passed, and then it is recorded in `task_parallel`
    (Sprint 26 IMP-2: six tasks were started within 12 minutes and ran at
    once, so their actuals measured stamp gaps, not work)."""
    cur = doc["current_sprint"]
    started = cur.setdefault("task_started", {})
    if task in started:
        raise SystemExit(
            f"Task {task} already started at {started[task]}. A second start "
            "would move the stamp and shorten the actual.")
    running = open_tasks(cur)
    if running and not parallel:
        raise SystemExit(
            f"Task(s) {', '.join(running)} are still being timed. Finish or "
            f"--pause-task them first, or pass --parallel to time {task} "
            "alongside them; a parallel start is recorded so the actuals "
            "are read as overlapping.")
    started[task] = now.isoformat(timespec="seconds")
    line = f"  current_sprint.task_started.{task}: {started[task]}"
    if running:
        cur.setdefault("task_parallel", {})[task] = running
        line += f" (parallel with {', '.join(running)})"
    return line


def pause_task(doc: dict, task: str, now: datetime) -> str:
    """Stop the clock, for example while a metered stop awaits approval."""
    cur = doc["current_sprint"]
    if task not in cur.get("task_started", {}):
        raise SystemExit(f"Task {task} has not started.")
    if task in cur.get("task_actuals", {}):
        raise SystemExit(f"Task {task} is already finished.")
    paused = cur.setdefault("task_paused", {})
    if task in paused:
        raise SystemExit(f"Task {task} is already paused since {paused[task]}.")
    paused[task] = now.isoformat(timespec="seconds")
    return f"  current_sprint.task_paused.{task}: {paused[task]}"


def resume_task(doc: dict, task: str, now: datetime) -> str:
    """Restart the clock; the paused time is kept out of the actual."""
    cur = doc["current_sprint"]
    paused = cur.get("task_paused", {})
    if task not in paused:
        raise SystemExit(f"Task {task} is not paused.")
    began = paused.pop(task)
    gap = (now - datetime.fromisoformat(began)).total_seconds()
    if gap < 0:
        raise SystemExit(f"Task {task} resumes before it paused.")
    total = cur.setdefault("task_paused_s", {})
    total[task] = total.get(task, 0) + int(gap)
    # The span itself, so --finish-task does not subtract a pause twice
    # when it also has no activity (F175).
    cur.setdefault("task_pause_spans", {}).setdefault(task, []).append(
        [began, now.isoformat(timespec="seconds")])
    return (f"  current_sprint.task_paused_s.{task}: {total[task]} s paused "
            "in all")


IDLE_GAP_S = 30 * 60


def activity(log: Path) -> list[datetime] | None:
    """The activity log's timestamps, or None when there is no log."""
    if not log.exists():
        return None
    out = []
    for line in log.read_text(encoding="utf-8").splitlines():
        try:
            out.append(datetime.fromisoformat(line.strip()))
        except ValueError:
            continue
    return out


def idle_seconds(points: list[datetime], start: datetime, end: datetime,
                 pauses: list[tuple[datetime, datetime]]) -> int:
    """Seconds of [start, end] that are not work: every gap of more than
    IDLE_GAP_S between activity points (the start and end count as points),
    and every recorded pause. Their union, so a pause with no tool calls in
    it is subtracted once."""
    pts = [start, *sorted(p for p in points if start < p < end), end]
    spans = [(a, b) for a, b in zip(pts, pts[1:])
             if (b - a).total_seconds() > IDLE_GAP_S]
    spans += [(max(a, start), min(b, end)) for a, b in pauses
              if min(b, end) > max(a, start)]
    total, reach = 0.0, None
    for a, b in sorted(spans):
        if reach is not None and a < reach:
            a = reach
        if b > a:
            total += (b - a).total_seconds()
        reach = b if reach is None else max(reach, b)
    return int(total)


def finish_task(doc: dict, task: str, now: datetime,
                log: Path | None = None) -> str:
    """Compute the actual from the recorded start, in whole minutes, less
    any time paused and, when there is an activity log, any gap of more
    than 30 minutes with no tool call (F175, Sprint 30). The elapsed
    minutes are kept beside it in `task_elapsed`."""
    cur = doc["current_sprint"]
    stamp = cur.get("task_started", {}).get(task)
    if not stamp:
        raise SystemExit(
            f"Task {task} has no recorded start in task_started. An actual "
            "judged at completion is an estimate of an actual (Sprint 23 "
            "IMP-3); record the start with --start-task when the task begins.")
    actuals = cur.setdefault("task_actuals", {})
    if task in actuals:
        raise SystemExit(f"Task {task} already has an actual: {actuals[task]}")
    if task in cur.get("task_paused", {}):
        raise SystemExit(f"Task {task} is paused; --resume-task it first, so "
                         "the pause is measured rather than guessed.")
    start = datetime.fromisoformat(stamp)
    elapsed = (now - start).total_seconds()
    if elapsed < 0:
        raise SystemExit(f"Task {task} finishes before it started ({stamp}).")
    paused_s = cur.get("task_paused_s", {}).get(task, 0)
    points = activity(log) if log is not None else None
    if points is None:
        idle, how = paused_s, "no activity log: elapsed less pauses"
    else:
        spans = [(datetime.fromisoformat(a), datetime.fromisoformat(b))
                 for a, b in cur.get("task_pause_spans", {}).get(task, [])]
        idle = idle_seconds(points, start, now, spans)
        # A pause recorded before spans were kept is still subtracted.
        idle = max(idle, paused_s)
        how = "gaps over 30 min and pauses subtracted"
    actuals[task] = max(1, math.ceil((elapsed - idle) / 60))
    cur.setdefault("task_elapsed", {})[task] = max(1, math.ceil(elapsed / 60))
    return (f"  current_sprint.task_actuals.{task}: {actuals[task]} min "
            f"active, {cur['task_elapsed'][task]} elapsed (from {stamp}; "
            f"{how})")


def main(argv: list[str] | None = None,
         now: datetime | None = None) -> int:
    # `now` is a parameter for tests, not a command-line flag: a flag that
    # sets the clock would let an actual be typed in after all.
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--set", action="append", default=[], metavar="KEY=VALUE",
                    help="assign a field; repeatable")
    ap.add_argument("--new-sprint", type=int, default=0,
                    help="roll to this sprint number")
    ap.add_argument("--name", default="")
    ap.add_argument("--branch", default="")
    ap.add_argument("--plan-doc", default="")
    ap.add_argument("--start-task", default="", metavar="TASK",
                    help="record the task's start time")
    ap.add_argument("--finish-task", default="", metavar="TASK",
                    help="compute the task's actual from its start time")
    ap.add_argument("--parallel", action="store_true",
                    help="with --start-task: time it alongside open tasks")
    ap.add_argument("--pause-task", default="", metavar="TASK",
                    help="stop the task's clock (an approval wait)")
    ap.add_argument("--resume-task", default="", metavar="TASK",
                    help="restart a paused task's clock")
    ap.add_argument("--add-issue", type=int, action="append", default=[],
                    metavar="N", help="append an issue number; repeatable")
    ap.add_argument("--task", default="", metavar="TASK",
                    help="with --add-issue: the task that owns the issue(s)")
    ap.add_argument("--review-task", default="", metavar="TASK",
                    help="the task a 'PR n review' commit is timed against")
    ap.add_argument("--path", default=str(STATUS),
                    help="status file (tests override this)")
    args = ap.parse_args(argv)

    path = Path(args.path)
    if not path.exists():
        raise SystemExit(f"{path} does not exist")

    doc = json.loads(path.read_text(encoding="utf-8"))
    changes: list[str] = []

    if args.new_sprint > 0:
        cur = doc.get("current_sprint", {})
        doc["last_completed_sprint"] = {
            "number": cur.get("number"),
            "merged_pr": cur.get("pr"),
            "main_merge_pr": None,
            # Deliberately False: the triad is not complete until the
            # retrospective and summary exist, and claiming otherwise here is
            # what let Sprint 15 merge without a retrospective.
            "docs_triad_complete": False,
        }
        doc["current_sprint"] = {
            "number": args.new_sprint,
            "name": args.name,
            "branch": args.branch,
            "status": "phase_1_backlog_refinement",
            "plan_doc": args.plan_doc,
            "pr": None,
            "plan_approved": False,
            "github_issues": [],
            # IMP-1 (Sprint 18 retrospective): SPRINT_PLANNING.md has required
            # "record actuals at task completion" since it was written, and
            # three consecutive sprints reported an estimate with no actual to
            # compare -- because nothing prompted it. The field exists so the
            # omission is visible in the status file rather than discovered at
            # the retrospective. {"A": 90, "B": 25, ...} in minutes.
            "task_actuals": {},
            # F136 (Sprint 23 IMP-3): the start stamps the actuals come from.
            "task_started": {},
            # F173 (Sprint 30): the issues each task owns, and the task a
            # "PR n review" commit is timed against.
            "task_issues": {},
            "review_task": None,
        }
        changes.append(f"  rolled to sprint {args.new_sprint} "
                       f"(previous: {doc['last_completed_sprint']['number']})")

    for assignment in args.set:
        changes.append(apply_set(doc, assignment))
    if args.task and not args.add_issue:
        raise SystemExit("--task names the owner of an --add-issue issue; "
                         "pass --add-issue N with it")
    for number in args.add_issue:
        changes.append(add_issue(doc, number, args.task))
    if args.review_task:
        cur = doc["current_sprint"]
        before = cur.get("review_task")
        cur["review_task"] = args.review_task
        changes.append(f"  current_sprint.review_task: {before!r} -> "
                       f"{args.review_task!r}")

    clock = now or datetime.now().astimezone()
    if args.pause_task:
        changes.append(pause_task(doc, args.pause_task, clock))
    if args.resume_task:
        changes.append(resume_task(doc, args.resume_task, clock))
    if args.start_task:
        changes.append(start_task(doc, args.start_task, clock, args.parallel))
    if args.finish_task:
        changes.append(finish_task(doc, args.finish_task, clock,
                                   path.parent / "activity.log"))

    if not changes:
        print("nothing to do; pass --set or --new-sprint")
        return 0

    # The original stamped this on every write, and the conversion dropped it.
    # Found while verifying Copilot's finding against the retired script, so it
    # is a SECOND regression from the same conversion. A status file nobody can
    # date is one nobody can tell is stale, which is the failure that put
    # `phase_4_execution` against a sprint with two merged PRs.
    doc["updated"] = date.today().isoformat()

    path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")

    # Re-read and re-parse rather than trusting the write.
    json.loads(path.read_text(encoding="utf-8"))

    print(f"{path}:")
    for line in changes:
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
