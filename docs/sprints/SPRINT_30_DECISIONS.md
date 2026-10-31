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

---

## D2. F168 part 2: where does a long run keep its finished units?

Asked 2026-10-30 at Phase 3 planning (plan verification).

**What.** F168's card says a long run checkpoints each finished unit to a
scratch folder, and only the final result goes to
`experiments/phase2/results/`. The repository already does it another
way: F110, F162, F166 and every Sprint 29 module keep their finished units
in the result file itself, marked `complete: false`. `provenance.start`
resumes only such a file, and only when its run id matches the sidecar.

**Why it matters.** Two patterns for one job means every new module
chooses, and a guard (F168 part 7) can only check one. The in-file
pattern is already guarded by `provenance.start` and
`test_result_writer_required.py`. The scratch-folder pattern keeps
partial results out of the results tree, so nothing half-done is ever
committed by mistake.

**Options, with Kind and Cost.**
- Option 1: Kind Prevention (one pattern, already guarded, extended to
  every long run). Cost: about 240 minutes (the card's), 0 metered
  seconds, about 10 files.
- Option 2: Kind Prevention (one new pattern), with every existing module
  left on the old one until it is next changed. Cost: about 300 minutes
  (the card's plus about 60 for a second writer path and its guard), 0
  metered seconds, about 12 files.
- Option 3: Kind Workaround (both patterns allowed; the guard accepts
  either). Cost: about 260 minutes, 0 metered seconds, about 11 files.

**Recommendation: 1.** It makes the pattern the repository already uses,
and already guards, the standard. A partial result is safe in the tree:
its `complete: false` flag and run id stop it from being read as a
result or replaced by another run. Option 2 adds a second writer path for
no new protection. Option 3 is a workaround: the guard could not tell a
module with no resume from one with either.

**Options.**

1. The in-file pattern is the standard: finished units go into the
   result file with `complete: false`, resumed through
   `provenance.start`. Part 2 writes this into the process docs and part
   7's guard checks it. Task C stays 240 minutes.
2. The card as written: checkpoints in a gitignored scratch folder, only
   the final result in `experiments/phase2/results/`; existing modules
   unchanged. Task C becomes 300 minutes; the sprint 1,035.
3. Both patterns allowed; part 7's guard accepts either. Task C becomes
   260 minutes; the sprint 995.

**Answer (team lead, 2026-10-31): 1.** The in-file pattern is the
standard. Task C stays 240 minutes.

---

## D3. F169: HGB cannot take more bins. What does the entry test?

Asked 2026-10-30 at Phase 3 planning (plan verification).

**What.** F169 tests "an HGB with `max_bins` and early stopping set for
extreme imbalance" under F108's plug-in. In scikit-learn 1.9.0, HGB's
`max_bins` accepts 2-255, and 255 is already the default (probed: 256
raises an error). F108's inferred cause of HGB's failure on its reference
arm is that 255 quantile bins put a top-0.05% threshold inside one bin.
HGB can turn early stopping off; it cannot add bins. LightGBM's
`max_bin` has no such limit.

**Why it matters.** As carded, the run would test early stopping only,
under a title that says bins. F114 waits on a validated estimator, so a
run that cannot test the inferred cause spends a sprint slot and leaves
F114 blocked for an untested reason.

**Options, with Kind and Cost.** Kind does not apply: each is a
measurement design for one card, not a fix to a recurring problem.
- Option 1: two arms, each an F108 plug-in: HGB with early stopping off,
  and LightGBM with `max_bin` raised (the value set in the entry) and
  early stopping off. 120 minutes, 0 metered seconds, about 4 files.
- Option 2: LightGBM with `max_bin` raised and early stopping off only.
  90 minutes, 0 metered seconds, about 4 files.
- Option 3: HGB with early stopping off only, as close to the card as
  scikit-learn allows. 90 minutes, 0 metered seconds, about 4 files.

**Recommendation: 1.** It tests both parts of the inferred cause and can
attribute a pass: if only LightGBM passes, bins mattered; if both pass,
early stopping did. The cost is 30 minutes more than either single arm.

**Options.**

1. Two arms, HGB with early stopping off and LightGBM with `max_bin`
   raised and early stopping off, each under F108's pass rule. Task F is
   120 minutes; the sprint 975.
2. LightGBM with `max_bin` raised and early stopping off only. Task F is
   90 minutes; the sprint 945.
3. HGB with early stopping off only. Task F is 90 minutes; the sprint
   945.

**Answer (team lead, 2026-10-31): 1.** Two arms, HGB with early stopping
off and LightGBM with `max_bin` raised and early stopping off. Task F is
120 minutes.

---

## D4. F174: how many seeds on IEEE-CIS?

Asked 2026-10-30 at Phase 3 planning (plan verification).

**What.** F166 set its seed count from seed 42's time under a 120-minute
cap (Sprint 29 Decision 3). On ULB that gave 10 seeds. IEEE-CIS trains
on 410,600 rows and 181 features against ULB's about 170,000 and 30.
Scaled from F166's lane times (inferred, not timed), seed 42 takes about
30-35 minutes, so the same cap gives 3 seeds. Section 2's Wilcoxon test
needs 8 seeds to reach 0.05 / 6.

**Why it matters.** With 3 seeds no pair can be called different by the
primary test, so the IEEE-CIS page could rank nothing that Experiments 2
and 3 and F171 are meant to read against. Runtime runs in the background
and does not change the work estimate.

**Options, with Kind and Cost.** Kind does not apply: each is a runtime
rule for one run.
- Option 1: 8 seeds minimum, 10 if seed 42 takes 30 minutes or less;
  about 4-6 hours of background runtime (inferred), 0 metered seconds,
  no added work minutes.
- Option 2: F166's rule unchanged (120-minute cap, at least 3 seeds);
  about 2 hours of runtime; the paired bootstrap is primary and the
  Wilcoxon test cannot reach its level.
- Option 3: 8 seeds on a stated stratified subsample of the training rows
  (about half), about 2-3 hours; the IEEE-CIS page then is not on the
  same rows as F152's lanes.

**Recommendation: 1.** It keeps F166's protocol and test, so the two
datasets' pages are read the same way, and its cost is background time
only. Seed 42 is timed first; if it takes more than 45 minutes, the run
stops before seed 43 and the count is asked again with the measured time.

**Options.**

1. Seed 42 timed first; then 10 seeds if it took 30 minutes or less, 8
   if it took up to 45; if it took more than 45 minutes, the run stops
   and this decision is asked again with the measured time.
2. F166's rule: the seed count from seed 42's time under a 120-minute
   cap, at least 3 seeds; the paired bootstrap is primary.
3. 8 seeds on a stratified half of each seed's training rows, stated in
   the entry.

**Answer (team lead, 2026-10-31): none of the listed options.** Verbatim:
"whatever seeds are needed, no time cap". Recorded as: no time cap on
F174's run. "Needed" does not name a count, so the count is asked as D5.

---

## D5. F174: with no time cap, how many seeds on IEEE-CIS?

Asked 2026-10-31 at Phase 3 planning, after D4's answer.

**What.** D4's answer removes the time cap and asks for the seeds that
are needed. Two counts meet a stated need. 8 is the smallest count at
which section 2's Wilcoxon signed-rank test can reach 0.05 / 6 = 0.0083:
with 8 seeds that all agree, the exact two-sided p is 2 / 2^8 = 0.0078;
with 7 it is 2 / 2^7 = 0.0156, which can never pass. 10 is the count F166
used on ULB.

**Why it matters.** With 8 seeds, a pair is called different only if all
8 seeds agree, so one disagreeing seed hides a real difference. With 10
seeds, one seed can disagree and the pair can still be called different,
if that seed's difference is one of the two smallest (exact rank sum 2 or
less; p = 2 x 3 / 2^10 = 0.0059). The IEEE-CIS page then also has the same seeds (42-51) as the
ULB page, so the two are read the same way. Each extra seed costs only
background runtime (inferred about 30-35 minutes per seed, not timed).

**Options, with Kind and Cost.** Kind does not apply: each is a sample
size for one run.
- Option 1: 10 seeds, 42-51. About 5-6 hours of background runtime
  (inferred), 0 metered seconds, no added work minutes (Task D stays
  240).
- Option 2: 8 seeds, 42-49. About 4-5 hours of background runtime
  (inferred), 0 metered seconds, no added work minutes.

**Recommendation: 1.** It matches F166's ULB seeds, so the two datasets'
pages compare seed for seed, and it lets the test tolerate one
disagreeing seed with a small difference. The extra cost is about one hour of background time
and no work.

In both options there is no time cap. Seed 42 is still timed first and
its time is reported, but the time does not stop the run. If the run is
interrupted, it resumes through `provenance.start` (D2).

**Options.**

1. 10 seeds, 42-51, no time cap. Task D stays 240 minutes.
2. 8 seeds, 42-49, no time cap. Task D stays 240 minutes.

**Answer (team lead, 2026-10-31): 1.** 10 seeds, 42-51, no time cap.
Task D stays 240 minutes.

---

## D6. Is the Sprint 30 plan approved?

Asked 2026-10-31 at Phase 3 planning, after D2-D5.

**What.** `SPRINT_30_PLAN.md` at `bfd73fc`: Tasks A-I (F173, F175,
F168, F174, F176, F169, F170, F171, F172), 975 minutes of work, 0
metered seconds, in the order A, B, C, D (seed 42 timed, then the run in
the background), E-H while D runs, then I.

**Why it matters.** Execution starts only on approval. On approval, one
GitHub issue per task is created and mapped to its task, the approval is
recorded in the status file, and the draft PR body is updated; the two
Phase 3 checks now red in CI then pass.

**Options, with Kind and Cost.** Kind does not apply: this is an
approval, not a fix.
- Option 1: about 10 minutes of records (9 issues, status, PR body), then
  975 minutes of work, 0 metered seconds.
- Option 2: no cost until the changes are named.

**Recommendation: 1.** Each card was checked against the repository, and
each card that could not run as carded was decided (D2-D5).

**Options.**

1. Approved as written: create the 9 issues, record the approval, start
   Task A.
2. Not approved: reply 2 followed by the change wanted; the plan is
   revised and this decision is asked again.
