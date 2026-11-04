# Agent launch prompts

These are the kept launch prompts for the agents this repository starts
(F168, Sprint 30). Copy the file for the agent kind, fill in each
`<...>` field, and send it as the agent's prompt. Do not write a launch
prompt inline.

The reason is a usage limit. A 5-hour or weekly limit stops an agent
mid-task. The team lead asked, on 2026-10-26: "can we make future agent
runs setup to not loose anything if we cross current or weekly session
limits and can re-start them so that they know what was done and what was
not done and can pickup with minimal interruption". Each prompt here has
a **Progress and restart** section, so the same agent, a new agent or a
new session can continue from the last finished unit.
`experiments/src/test_agent_prompts.py` fails a prompt that loses it.

| File | Agent | Launched at |
|---|---|---|
| `ci_fix.md` | CI failure fix, in the background | 3.3.2 and 7.0 (`SPRINT_EXECUTION_WORKFLOW.md`) |
| `review.md` | Code or document review, findings to a file | Phase 5, PR review rounds |
| `fresh_eyes.md` | Fresh-context evidence review | Phase 5, before a metered result's interpretation |
| `research.md` | Research or analysis task with several units | Phase 4, any task handed to an agent |

## The progress folder

Each agent has a folder at `.claude/agent_progress/<name>/`. The folder
is gitignored and is outside the results tree. Its `progress.md` holds
one line per finished unit, and `DONE` as the last line when the agent
finishes. `scripts/agent_status.py` reads these folders and reports each
agent's state. It stores nothing.

## Long runs are not agents

A long classical or simulated run is a Python process, not an agent. A
usage limit stops Claude, not that process. The run keeps its finished
units in its own result file (`complete: false`) and resumes through
`provenance.start` (Sprint 30 D2). A module that does this declares
`LONG_RUN = True` (`experiments/src/test_long_run_resume.py`).
