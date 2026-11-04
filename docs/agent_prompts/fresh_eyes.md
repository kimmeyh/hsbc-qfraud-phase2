# Fresh-eyes evidence review (background agent)

Name: `fresh-eyes-<result>-<date>`

## Task

You have no context on this campaign. Read <the result files and the
document that interprets them>. Describe what is there. Note any useful
observation: a number the document states that the file does not hold, a
claim stronger than the evidence, an interval that crosses its threshold,
a seed or fold that disagrees with the rest.

Label each claim you make Measured, Inferred or Unverified. Do not edit
files.

## Progress and restart

- Your progress folder is `.claude/agent_progress/<name>/`. Read
  `progress.md` there FIRST. If it does not exist, create it and write
  `started <time>` as its first line.
- Each line after the first is one finished unit: a file read and its
  observations written. Skip every file it lists; do not read it again.
- After each file, append its observations to the report file first,
  then append one line to `progress.md`: the file and the time.
- Never send a device call. A device block needs the team lead's
  approval with its call count and seconds (Criterion H).
- When you finish, write `DONE` as the last line of `progress.md`.
- In your final reply, say what you resumed and from which file, or say
  "started fresh", and state the number of observations in the report.

## Report

Write the observations to `<scratchpad>/fresh_eyes_<result>.md`, one
entry per observation with the file, the field and the claim label.
