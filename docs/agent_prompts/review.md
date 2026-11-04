# Review (background agent)

Name: `review-<scope>-<date>`

## Task

Review <scope: the diff `origin/develop...HEAD`, or the files listed> for
<aspect: correctness, error handling, tests, comments>. Report findings
only; do not edit files.

Out of review scope (CLAUDE.md): `experiments/results/*.json`,
`experiments/results/gate_report.md` and
`experiments/phase2/results/**/*.json`. Review the code that produces
evidence and the documents that interpret it.

## Progress and restart

- Your progress folder is `.claude/agent_progress/<name>/`. Read
  `progress.md` there FIRST. If it does not exist, create it and write
  `started <time>` as its first line.
- Each line after the first is one finished unit: a file reviewed. Skip
  every file it lists; do not review it again.
- After each file is reviewed, append its findings to the report file
  first, then append one line to `progress.md`: the file and the time.
- Never send a device call. A device block needs the team lead's
  approval with its call count and seconds (Criterion H).
- When you finish, write `DONE` as the last line of `progress.md`.
- In your final reply, say what you resumed and from which file, or say
  "started fresh", and state the number of findings in the report.

## Report

Write the findings to `<scratchpad>/review_<scope>.md`: one entry per
finding with title, file, line, failure and fix (IMP-5, Sprint 22). The
final reply is a summary, not the record.
