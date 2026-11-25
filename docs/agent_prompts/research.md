# Research or analysis task (background agent)

Name: `<card>-<task>-<date>`

## Task

<The question, the card and its acceptance criteria.> The units are
<the list: sources, files, seeds, folds or lanes>. Read
<the files named in the card>. Report what each source states, with its
link or path, and label each claim Verified, Inferred or Unverified.

Do not write to `experiments/results/` (Phase 1 evidence), to
`docs/paper/`, `docs/submission/` or `experiments/PREREGISTRATION.md`,
or to another repository.

## Progress and restart

- Your progress folder is `.claude/agent_progress/<name>/`. Read
  `progress.md` there FIRST. If it does not exist, create it and write
  `started <time>` as its first line.
- Each line after the first is one finished unit. Skip every unit it
  lists; do not redo it.
- After each unit is finished and checked, write its result to the report
  file first, then append one line to `progress.md`: the unit, the time,
  and where its result is.
- A long run you start is a Python module that resumes through
  `provenance.start`. Do not delete or move a result file marked
  `complete: false`; run the module again and it resumes. Check a run's
  completion marker (`complete: true` and its final `complete` line), not
  the file's presence.
- Never send a device call. A device block needs the team lead's
  approval with its call count and seconds (Criterion H).
- When you finish, write `DONE` as the last line of `progress.md`.
- In your final reply, say what you resumed and from which unit, or say
  "started fresh".

## Refusals (code tasks)

A refusal you add (a condition that raises or refuses) lives in a small
named function (`require_*`, `check_*` or `main(argv)`) that a test
calls in-process with built data. `run()` and the `__main__` block only
call it. Each refusal gets its test and a red proof (`assert_can_fail`,
removing the refusal) in the same commit (`SPRINT_CHECKLIST.md` Phase 4,
Sprint 34 i1).

## Report

Write the result to `<scratchpad>/<card>_<task>.md`. For a code task,
the report lists each new refusal with the function that holds it, its
test and its red-proof mutation.
