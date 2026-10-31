# CI failure fix (background agent)

Name: `ci-fix-<pr>-<run id>`

## Task

CI is red on PR #<pr>, run <run id>, head <sha>. Find the cause of each
failed test and fix it on branch `<branch>`. The sprint continues while
you work; do not edit a file named in the sprint's current task
(<task files>).

- Read the failed job's log: `gh run view <run id> --log-failed`.
- Run the failed tests locally with `.venv/Scripts/python.exe -m pytest`.
- A test that cannot fail locally (for example one that depends on the
  branch name or the OS) is fixed so it can, and proven red with
  `injection.assert_can_fail`.
- Commit each fix with `fix: ... (PR <pr> review)` after
  `scripts/update_sprint_status.py --review-task <task>` names your task.
- Do not review or edit `experiments/results/*.json`,
  `experiments/results/gate_report.md` or
  `experiments/phase2/results/**/*.json`.

## Progress and restart

- Your progress folder is `.claude/agent_progress/<name>/`. Read
  `progress.md` there FIRST. If it does not exist, create it and write
  `started <time>` as its first line.
- Each line after the first is one finished unit. Skip every unit it
  lists; do not redo it.
- After each unit is finished and checked, append one line: the unit,
  the time, and the commit or file that holds it.
- Never send a device call. A device block needs the team lead's
  approval with its call count and seconds (Criterion H).
- When you finish, write `DONE` as the last line of `progress.md`.
- In your final reply, say what you resumed and from which unit, or say
  "started fresh".

## Report

Write the report to `<scratchpad>/ci_fix_<run id>.md`: one entry per
failed test with the cause, the fix, the commit and the red proof.
