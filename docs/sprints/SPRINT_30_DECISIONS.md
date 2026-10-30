# Sprint 30 Decisions

Every decision or question asked of the team lead in this sprint, in full,
as first asked. A question asked again is pasted from here unchanged: same
ID, same wording, same option numbers. If facts change after it is asked, a
dated "Changed since asked" note goes below the original; the original is
never edited. The answer is recorded under each entry.

---

## D1. Which cards make up Sprint 30?

Asked 2026-10-30 at backlog refinement Pass 2 (Phase 8.4).

**What.** Sprint 30's scope. F168 is already assigned to Sprint 30 by the
team lead (2026-10-26) and is in every option. The other candidates come
from the 2026-10-30 slate in `docs/ALL_SPRINTS_MASTER_PLAN.md`.

**Why it matters.**
- Effort accuracy has been unmeasured for two sprints. Four of Sprint 29's
  nine actuals are elapsed time across breaks, and the commit-msg hook
  accepts any running timer. Until F173 and F175 ship, the estimates in
  this decision rest on three usable ratios: 0.38, 0.44 and 0.66 (actual
  over estimate, `docs/VELOCITY_LOG.md`).
- F114 has no validated ceiling estimator. F169 is the next candidate.
  F170 and F171 test, row by row and on a second dataset, the reading that
  the frauds every model misses are an information limit.
- Experiment 3 is the critical path in F167's PoC plan draft. F160 showed
  room on IEEE-CIS only to a bound. F176 asks whether any classical solver
  reaches below greedy.
- Every later IEEE-CIS claim needs a tuned reference. F174 is F166's
  protocol on IEEE-CIS.

**Cards.** Minutes are card estimates; 0 metered seconds unless stated.
File counts are estimates.
- F168, agent work and long runs survive a usage limit: 240m; about 10
  files. Prevention.
- F173, the commit-msg hook checks the commit's own task timer: 45m; 3
  files. Prevention.
- F175, task timers stop counting breaks: 60m; 3 files. Prevention. Same
  files as F173, so it runs after F173.
- F172, tests for the Sprint 29 review's coverage gaps: 90m; 4 files.
  Workaround (detection for that code only).
- F176, Experiment 3 on IEEE-CIS, a classical solver below greedy: 90m; 4
  files.
- F169, ceiling estimator, HGB set for extreme imbalance: 90m; 4 files.
- F170, ULB missed frauds' nearest neighbors: 30m; 3 files.
- F171, F158 step 3 on IEEE-CIS: 60m; 3 files. It uses F152's four stored
  families; F174's families are not needed.
- F174, F157 part 2, best result per algorithm on IEEE-CIS: 240m; about
  12 files.
- F155, the 1,300-variable Dirac-3S ceiling probe: 30m; about 4 metered
  seconds (a floor, not a bound); 3 files. It stops for its own
  per-block approval (Criterion H).

**Kind per option.** Options 1, 2 and 3 carry the same three Preventions
(F168, F173 and F175) and the same Workaround (F172). They differ only in
experiment scope and metered spend.

**Cost per option.**
- Option 1: 945 minutes by card estimate; 0 metered seconds; about 46
  files.
- Option 2: 705 minutes; 0 metered seconds; about 34 files.
- Option 3: 975 minutes; about 4 metered seconds behind their own approval
  stop; about 49 files.
- Option 4: whatever set is named.

**Recommendation: 1.** It gives:
- the assigned card;
- both preventions for the timer class, which has made two sprints'
  actuals unusable;
- the ceiling cards the team lead added at Sprint 29 Manual Validation;
- both IEEE-CIS items that the Experiment 3 critical path and later claims
  need.

All of it at zero metered seconds. Sprint 28 and Sprint 29's usable
ratios put the 945 minutes at about 360-620 minutes of work. F155 is not
in it: it spends metered seconds to detect a change that QCi said would
come "in the coming weeks", and its run is better asked for when QCi says
the expansion is live. F102 is not a card in it: each selected experiment
card writes its own entry, and the filing date is the team lead's.

**Options.**

1. As recommended: F168, F173, F175, F172, F176, F169, F170, F171 and
   F174 (945 minutes, 0 metered seconds).
2. Option 1 without F174 (705 minutes, 0 metered seconds). F174 stays in
   the backlog at priority 30.
3. Option 1 plus F155, the 1,300-variable probe (975 minutes; about 4
   metered seconds, asked for separately with its call count and seconds
   before it runs).
4. A different set: reply 4 followed by the F numbers to include (F168
   is included in any set).

**Answer (team lead, 2026-10-30): 1.** Sprint 30 is F168, F173, F175,
F172, F176, F169, F170, F171 and F174 (945 minutes by card estimate, 0
metered seconds).
