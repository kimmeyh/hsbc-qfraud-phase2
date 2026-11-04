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

**Answer (team lead, 2026-10-31): 1.** "Sprint plan approved as amended
(with any comments I provided), proceed with execution. All Sprint tasks
and sub-tasks are approved."

---

## D7. F171: which alert budget does the IEEE-CIS missed-by-all count use?

Asked 2026-10-31 at Phase 4 execution, after F171's run. The team lead's
words: "can we change the 0.5% budget to 3.5% - the resulting user can
always lower, but I think we want to consider higher for our
investigations. What do you think?"

**What.** F171's entry, written before the run, counts a fraud as missed
by all when no family flags it at the 0.5% alert budget (F154's standard
budget). The run is recorded: 81.5% of IEEE-CIS (month, seed, fraud)
pairs are missed by all four families, against 11.2% on ULB (F158 step 3).
The budget explains much of that gap:
- ULB test split (seed 42): 56,746 rows and 95 frauds (0.167%). A 0.5%
  budget is 284 alerts, about 3.0 times the frauds.
- IEEE-CIS month 4: 85,302 rows and 2,962 frauds (3.47%). A 0.5% budget
  is 426 alerts, 0.14 times the frauds. One family can flag at most 14%
  of the frauds. Four families with no overlap can flag at most 1,704,
  so at least 1,258 frauds (42%) are missed by all before any model is
  scored.

**Why it matters.** At 0.5% the IEEE-CIS count measures mostly the
budget, not the models, so F171's question (do richer features shrink the
missed group?) is not answered by it. The 0.5% figure was preregistered
and has been seen, so replacing it now would change a rule after its
result is known. A second budget added as a dated, post hoc amendment
keeps the recorded result and labels the new figures as exploratory.
Two higher budgets answer different questions:
- 3.5%: about IEEE-CIS's fraud rate, one alert per fraud. On ULB 3.5% is
  about 21 times the frauds, so it is not the same strictness there.
- Prevalence-matched: each dataset's budget is 3.0 times its own test
  fraud rate, the ratio ULB's 0.5% has. About 10.4% on IEEE-CIS and 0.5%
  on ULB. Only this one makes the ULB comparison like for like.

**Options, with Kind and Cost.**
- Option 1: keep 0.5% as F171's recorded result. Add a dated post hoc
  amendment to the F171 entry and a new module
  `f171_budgets.py` writing `f171_budgets.json`: missed-by-all on both
  datasets at 3.5% and at 3.0 times each test fraud rate. Kind:
  Prevention (cross-dataset reads use a budget tied to the base rate).
  Cost: about 30 minutes, 0 metered seconds, 4 files (entry, module,
  test, result), plus the F171 write-up.
- Option 2: keep 0.5% as recorded; add only 3.5%, on both datasets, by
  the same amendment route. Kind: Workaround (one more fixed budget; the
  ULB comparison stays unmatched). Cost: about 20 minutes, 0 metered
  seconds, 4 files.
- Option 3: replace 0.5% with 3.5% as F171's primary budget and rerun F171
  over its recorded result (`replace=` with the reason). Kind:
  Workaround. Cost: about 15 minutes, 0 metered seconds, 3 files. It
  changes a preregistered rule after its result is seen.
- Option 4: no change. The F171 write-up states the budget's capacity
  limit with the figures above. Kind: Workaround. Cost: no added minutes.

**Recommendation: 1.** It keeps the preregistered figure, adds the 3.5%
the team lead asked for, and adds the one budget that makes the ULB
comparison fair. Option 3 is not chosen because it would edit a
preregistered rule after its result was seen. The repository-wide 0.5%
in every outcome block (F154) is a separate rule and is not changed by
any option here.

**Options.**

1. Keep 0.5% as recorded; add a post hoc amendment and `f171_budgets.py`
   with 3.5% and 3.0 times each test fraud rate (about 10.4% on IEEE-CIS,
   0.5% on ULB), on both datasets. About 30 minutes.
2. Keep 0.5% as recorded; add a post hoc amendment and `f171_budgets.py`
   with 3.5% only, on both datasets. About 20 minutes.
3. Replace 0.5% with 3.5% as F171's primary and rerun F171 over its
   recorded result. About 15 minutes.
4. No change; the write-up states the capacity limit. No added minutes.

**Answer (team lead, 2026-10-31): 1.** Keep 0.5% as recorded; add a post
hoc amendment and `f171_budgets.py` with 3.5% and 3.0 times each test
fraud rate (about 10.4% on IEEE-CIS, 0.5% on ULB), on both datasets.

**Changed since asked (2026-10-31, after the budget run).** The budget
rounds up: a 0.5% budget on month 4's 85,302 rows is 427 alerts, not
426. Four families can then flag at most 1,708 frauds, so the capacity
floor is 1,254 (42%), not 1,258. The reading and the recommendation do
not change.

## D8. How do the comparison pages show TP, FP, TN and FN?

Asked 2026-11-01 at Manual Validation. The team lead's words: "In this
doc, the following does not show TP/TN/FP/FN (confusion matrix) - thought
we added them to all measurements and recording of values?" (on
`IEEE_COMPARISON.md`'s table; "Same observation in ULB_COMPARISON.md").

**What.** The counts are recorded: every lane and seed in
`f174_ieee_algorithms.json` and `f166_ulb_algorithms.json` carries F154's
outcome block, with the confusion counts at the test fold's own 0.5%
budget and at each validation-chosen threshold. Each algorithm page shows
the counts per seed at the two validation-chosen thresholds. Two gaps:
- The comparison pages show no counts at all.
- The comparison table's recall column uses the test fold's own budget,
  and the counts behind it appear on NO page. For example, IEEE-CIS
  LightGBM seed 42 flags 427 rows: TP 415, FP 12, TN 82,328, FN 2,547.

The comparison table has one row per algorithm and 10 seeds behind each
row, so the counts need a form that stays whole numbers. A mean of counts
is a derived decimal. A sum over seeds adds the same IEEE-CIS test month
10 times, and on ULB it adds different test folds.

**Why it matters.** A recall of 0.1389 does not show that the budget lets
an algorithm flag only 427 of 2,962 frauds; the counts do. Without them
the reader cannot check the rate. Each option below adds the same counts;
they differ in how much the comparison table carries.

**Kind and cost.**
- Option 1: Prevention. The two generators render the counts, and each
  generator's test fails a page without them, proven red. About 40
  minutes. Files: `scripts/f174_docs.py`, `scripts/f166_docs.py`, their
  two tests, the 16 pages they render, `CHANGELOG.md`, the validation
  document.
- Option 2: Prevention, the same guard. About 30 minutes, the same files
  except the algorithm pages do not change.
- Option 3: Prevention, the same guard. About 40 minutes, the same files
  as option 1.

**Recommendation: 1.** The comparison row gives each count's range over
the 10 seeds (for example TP 400 to 416), which stays whole numbers and
shows at once where a lane is the same on every seed (XGBoost: 404 to
404). The per-seed counts at the test fold's own budget then go on each
algorithm page, next to the two thresholds it already shows, so every
figure in the row traces to a seed. Option 2 leaves the per-seed counts
behind the recall column on no page. Option 3 puts 70 rows on each
comparison page, which buries the ranking the page exists to show.

**Options.**

1. Comparison table: add TP, FP, TN and FN columns at the test fold's own
   0.5% budget, each the minimum to the maximum over the 10 seeds; each
   algorithm page: add a "0.5% budget on the test fold" column with the
   per-seed counts to its confusion table; a note where the proxy's tied
   scores flag more rows than the budget (IEEE-CIS up to 442 of 427, ULB
   up to 291 of 284). Both datasets.
2. Comparison table only: the same four range columns and the tie note.
   The algorithm pages do not change. Both datasets.
3. Comparison page: a second table with each algorithm's counts for every
   seed (70 rows per dataset) at the test fold's own 0.5% budget; each
   algorithm page: the per-seed column as in option 1. Both datasets.

**Answer (team lead, 2026-11-01): 1.** Comparison table: add TP, FP, TN
and FN columns at the test fold's own 0.5% budget, each the minimum to the
maximum over the 10 seeds; each algorithm page: add a "0.5% budget on the
test fold" column with the per-seed counts to its confusion table; a note
where the proxy's tied scores flag more rows than the budget. Both
datasets.

**Changed since asked (2026-11-01, after the render).** The tie figures in
option 1 came from the first three seeds only. Over all 10 seeds, the
proxy flags up to 297 rows against ULB's budget of 284 (7 of 10 seeds),
not 291, and up to 442 against IEEE-CIS's 427 (8 of 10 seeds). HGB on
IEEE-CIS also flags 428 on 1 of 10 seeds. The pages state the figures
computed from all seeds. The answer and the work do not change.

## D9. The 13-minute CI limit canceled a run whose steps all passed

Asked 2026-11-01 at Manual Validation, after the first runs under the
13-minute limit that the team lead set at V10.

**What.** The three runs on this branch since the change:
- 45a77ee (before the change, 20-minute limit): job 12:36, tests step
  11:36. Success.
- f5313e9 (13-minute limit, a docs-only commit): job 13:02, tests step
  11:59. Every step passed, then the job was canceled at the limit.
- a3a0af3 (13-minute limit, with Task K's five added red proofs): job
  12:48, tests step 11:47. Success.

The job is about 50 seconds of setup and install plus the tests step. A
docs-only commit took longer than the commit that added tests, so the
spread is the runner's speed, not this sprint's changes. At 13 minutes
the margin is a few seconds, and one of the two runs was canceled. A
canceled run reads as neither red nor green, which is the state that hid
CI from 73a976e to 4b19944 (V10).

**Why it matters.** Each canceled run is a commit with no CI verdict.
The close-out hook blocks the completion claim when CI is not green, so
a cancel at the final HEAD also stops the PR going ready until a rerun
passes.

**Kind and cost.**
- Option 1: Workaround. One line in `.github/workflows/ci.yml` and a
  CHANGELOG entry, about 5 minutes. About 2 minutes of margin on the
  runs seen.
- Option 2: Workaround. The same files, about 5 minutes. About 1 minute
  of margin.
- Option 3: Workaround. No change. Cancels continue at about the rate
  seen until F177 (Sprint 31) cuts the suite.
- The Prevention is F177, the full suite in about 5 minutes. It is
  carded for Sprint 31, not this sprint, because it is about 240 minutes
  of work.

**Recommendation: 1.** It keeps a stop for a hung job well under the
earlier 20 minutes, and its margin covers the spread seen. F177 then
sets the limit to its new suite time. Option 2's minute is about the
spread already seen between two runs, so it would still cancel
sometimes.

**Options.**

1. Set the CI job's limit to 15 minutes until F177 lands; F177's
   acceptance sets it from the new suite time.
2. Set the CI job's limit to 14 minutes until F177 lands.
3. Keep 13 minutes; rerun a canceled run by hand until F177 lands.

**Answer (team lead, 2026-11-01): none of the options.** The team lead's
words: "There is WAY TOO MUCH going on in the CI if it is taking > 13
minutes. The D9 answer is find what does not need to be in there and
remove it, then optimize everything in there so that it runs as fast as
possible. Target is < 5 minutes." This brings F177's CI part into Sprint
30 as Task L (#86).

## D10. Sprint 30 retrospective: how is each improvement disposed?

Asked 2026-11-03, retrospective step 6. The proposals are in full in
`SPRINT_30_RETROSPECTIVE.md`, "Improvements proposed".

**What.** Five improvements from the combined feedback and the PR 74
review findings:

- IMP-1: the close-out hook requires CI's full job green, not only the
  push job (`verify_closeout_complete.py` calls `ci.evaluate(sha,
  require_job="full")`; one more `gh` call, 31s worst case to 34s inside
  its 35s budget). Prevention. 30 minutes.
- IMP-2: the Phase 4 and Phase 5 per-term items in `SPRINT_CHECKLIST.md`
  name every refusal and every reported state as a term, not only
  compound decision rules. Prevention. 10 minutes.
- IMP-3: `--finish-task` flags an active actual under a fifth of the
  task's estimate, so a low reading is checked when it is recorded.
  Detection, because the cause of A-C's low readings is unverified.
  20 minutes.
- IMP-4: the Phase 5 full-suite item says the output goes to a file with
  `-rf`, never to a tail, with a `docs/TROUBLESHOOTING.md` entry.
  Prevention. 10 minutes.
- IMP-5: the deferred review findings (provenance commit on resume, the
  status-file lock and shared `review_task`, the two tests rated 3) go
  to the backlog as F179, priority 40. Prevention. About 90 minutes.

**Why it matters.** IMP-1 closes the one review finding that lets the
sprint be called complete before the red proofs have run on CI. IMP-2
and IMP-4 stop two recurring classes at the point they start. IMP-3
makes a wrong actual visible when it is written, not at the
retrospective. Applying IMP-1 to IMP-4 now costs about 70 minutes and
one CI run; deferring them leaves each class open for Sprint 31.

**Kind and cost.** As listed per improvement above. All four now-items
touch 4 files: the close-out hook and its test, `update_sprint_status.py`
and its test, `SPRINT_CHECKLIST.md` and `TROUBLESHOOTING.md`. Zero
metered seconds.

**Recommendation: 1.** IMP-1 to IMP-4 are small and each extends an
existing prevention. IMP-5 is larger and changes no current result, so
it waits for refinement.

**Options.**

1. As recommended: IMP-1, IMP-2, IMP-3 and IMP-4 now, timed as task N;
   IMP-5 to the backlog as F179, priority 40.
2. All five to the backlog: IMP-1 to IMP-4 as F179, IMP-5 as F180, both
   priority 40; nothing applied this sprint.
3. IMP-1 now, timed as task N; IMP-2, IMP-3, IMP-4 and IMP-5 to the
   backlog as F179, priority 40.

**Changed since asked (2026-11-03).** "Kind and cost" says the four
now-items touch 4 files and then lists 6. The count is 6: the close-out
hook and its test, `update_sprint_status.py` and its test,
`SPRINT_CHECKLIST.md` and `docs/TROUBLESHOOTING.md`. The options are
unchanged.

**Answer (team lead, 2026-11-04): none of the listed options.** Verbatim:
"do imp-1-5 now". IMP-1 to IMP-5 are applied on this branch, timed as
task N; nothing goes to the backlog.
