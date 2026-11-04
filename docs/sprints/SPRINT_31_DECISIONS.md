# Sprint 31 Decisions

Every decision or question asked of the team lead in this sprint, in full,
as first asked. A question asked again is pasted from here unchanged: same
ID, same wording, same option numbers. If facts change after it is asked, a
dated "Changed since asked" note goes below the original; the original is
never edited. The answer is recorded under each entry.

---

## D1. Which cards make up Sprint 31?

Asked 2026-11-04 at backlog refinement Pass 2 (Phase 8.4).

**What.** Sprint 31's scope, from the 2026-11-04 slate in
`docs/ALL_SPRINTS_MASTER_PLAN.md`.

**Why it matters.**
- Testing time is now the largest cost in a sprint. In Sprint 30, the
  approval of D10 was followed by about 87 minutes before `gh pr ready`,
  against the team lead's target of development time plus about 15. A
  local full suite took 48.9 minutes (F177's measurement). F180 finds
  where that time goes and what can be cut without losing a guard; F177
  then makes the cuts. F180 comes first, because its findings choose
  F177's levers.
- The status file can still lose an update when two commands write at
  once (F179). It is the record the commit hook and the task timers read.
- F178's first versions have not been written. Its card puts its update
  step before Manual Validation every sprint, so the step has nothing to
  update until the first versions exist.
- F114 is unblocked. F169 is the first ceiling method to pass F108's
  rule, so the real-data step can run. It is the result the F169, F170
  and F171 work was for.

**Cards.** Minutes are card estimates; 0 metered seconds unless stated.
File counts are estimates.
- F180, deep analysis of all testing: 180m; about 5 files (the analysis
  document, the inventory script, its test, the checklist, this file).
  Prevention.
- F177, the full suite in about 5 minutes: up to 240m; about 10 files.
  Prevention. Its levers are chosen by a decision written from F180's
  findings, mid-sprint; a lever not chosen is not built, so 240m is a
  ceiling.
- F179, the status file's lock and the review-task order: 45m; 3 files.
  Prevention.
- F178, three learning documents, first versions: 180m; about 5 files
  (three documents, a link-and-claim test, the checklist step). A
  deliverable, neither Prevention nor Workaround. The first versions exist
  by Sprint 31 Phase 5, so the per-sprint update step runs from Sprint 32.
- F114, ceiling estimate on real data with F169's method: 90m (the
  real-data step; the validation step is spent); about 4 files.
- F155, the 1,300-variable Dirac-3S ceiling probe: 30m; about 4 metered
  seconds (a floor, not a bound); 3 files. It stops for its own
  per-block approval (Criterion H).

**Kind per option.** Options 1, 2 and 3 carry the same three Preventions
(F180, F177, F179). Options 1 and 3 add F178 (a deliverable) and F114
(research). No option carries a Workaround.

**Cost per option.**
- Option 1: 735 minutes by card estimate; 0 metered seconds; about 27
  files.
- Option 2: 465 minutes; 0 metered seconds; about 18 files.
- Option 3: 765 minutes; about 4 metered seconds behind their own approval
  stop; about 30 files.
- Option 4: whatever set is named.

**Estimate accuracy, measured.** Sprint 30's active-minute ratios (actual
over estimate, `docs/VELOCITY_LOG.md`) run from 0.02 to 0.38 across the
twelve rows that have an estimate. Four rows are flagged "cause
unverified"; two research rows ran their computation in the background,
so their active minutes leave the run time out. Only three tasks were
taken with `--estimate`. These ratios are not converted into a work
forecast here: F180 parts 3 and 4 measure where the time goes, and that is
what settles the cause. The card totals above are the estimates as carded.

**Recommendation: 1.** It gives:
- the testing analysis and its cuts, which is the team lead's stated
  priority after Sprint 30, in the right order (F180, then F177);
- the status-file lock that the timers and the commit hook rely on;
- the first versions of the learning documents, so their per-sprint step
  can start;
- the ceiling result the last two sprints built toward.

All of it at zero metered seconds. F155 is not in it: QCi said the
expansion would come "in the coming weeks" on 2026-10-21, and no newer
word is recorded here, so the probe is better run when QCi says it is
live. F102 is not a card in it: each selected experiment writes its own
entry, and the filing date is the team lead's. F13's content waits for
the finalist notification.

**Options.**

1. As recommended: F180, F177, F179, F178 and F114 (735 minutes, 0
   metered seconds). F177's levers are chosen by a decision written from
   F180's findings.
2. Testing and tooling only: F180, F177 and F179 (465 minutes, 0 metered
   seconds). F178 and F114 stay in the backlog at priorities 12 and 16.
3. Option 1 plus F155, the 1,300-variable probe (765 minutes; about 4
   metered seconds, asked for separately with its call count and seconds
   before it runs).
4. A different set: reply 4 followed by the F numbers to include.
