# Sprint 30 Manual Validation

**Sprint**: 30
**Branch**: `feature/20261030_Sprint_30` | **PR**: #74 (draft)
**Scope**: F173 (A), F175 (B), F168 (C), F174 (D), F176 (E), F169 (F),
F170 (G), F171 (H), F172 (I), and the Phase 5 review fixes (J).
Issues #75-84.
**Metered seconds**: 0. No Dirac, Braket or other paid service was called.

This file is the durable copy. The same items are listed to the screen at
handover: a pointer to a file is not a handover.

---

## V1. Task A (F173): a commit needs its OWN task's timer

- `update_sprint_status.py --add-issue N --task X` records each issue's
  task in `task_issues`; the commit-msg hook refuses a `feat:` or `fix:`
  commit whose named issue's task is not being timed. A "PR n review"
  commit needs `--review-task X`.
- The card's case is a test: a commit naming #66 while only D's and H's
  timers run is refused; with C's timer it is accepted. Each term proven
  red (`test_commit_msg_hook.py`).
- Used all sprint: every Sprint 30 `feat:` and `fix:` commit passed it.
- **Gap found in use**: the hook checks `feat:` and `fix:` only. The
  `docs:`, `test:` and `ci:` commits this sprint passed with no timer.

## V2. Task B (F175): an actual is work, not elapsed time

- A PostToolUse hook (`.claude/hooks/log_task_activity.py`) appends a
  timestamp per tool call to `.claude/activity.log` (gitignored) while a
  timer runs. `--finish-task` subtracts gaps over 30 minutes and pause
  spans, and records `task_actuals` (active) and `task_elapsed`.
- **Finding, please read**: Sprint 30's actuals are now too LOW, not too
  high. E (2 active, 143 elapsed), F (2 active, 41 elapsed) and G (6
  active, 40 elapsed) were measured correctly, but their result write-ups
  were done while no timer ran (or while another task's ran), so that
  work is in no task's actual. The hook measures what is timed; it cannot
  time what is not started. See V11.

## V3. Task C (F168): agent work and long runs survive a usage limit

- Kept agent prompts in `docs/agent_prompts/`, each with a "Progress and
  restart" section; progress files in `.claude/agent_progress/`
  (gitignored).
- `device_store` writes an intent before it sends and refuses a problem
  hash that has an intent or a response, so a resume never repeats a
  metered call. No metered call was made this sprint.
- Every module that calls `provenance.start` declares `LONG_RUN`; a True
  module must be resumable (`test_long_run_resume.py`).
- `scripts/agent_status.py` and the hourly wake-up (CronCreate ef02e6ad,
  session-only, expires after 7 days). Two wake-ups ran this session and
  reported correctly.
- **Gap found in use**: `agent_status.py` lists a run only once its
  result file exists. F174 wrote nothing for its first 65 minutes, so a
  death in that window would not have shown; its process was checked
  directly instead.

## V4. Task D (F174): best achievable result per algorithm on IEEE-CIS

`docs/phase2/algorithms/IEEE_COMPARISON.md` and its seven pages; result
`experiments/phase2/results/f174_ieee_algorithms.json` (82a418d).

- All 10 seeds (42-51) finished, with no time cap (D4, D5).
- By mean test AUPRC on month 4: LightGBM, HGB, CatBoost, XGBoost, the
  proxy, SVM, logistic regression.
- Four of the six adjacent pairs differ reliably under the entry's rule
  (exact Wilcoxon, Bonferroni 0.05 / 6). HGB against CatBoost and XGBoost
  against the proxy do not, so those two orders are not established.
- **Please read (fresh-eyes review, fixed in Task J)**: XGBoost, SVM and
  logistic regression give the same test AUPRC on every seed. The month
  folds are fixed, and each lane chose one configuration and is
  deterministic, so their 10 seeds are one result. Three of the four
  reliable pairs touch one of these lanes. "SVM above logistic
  regression" is one difference repeated 10 times; "CatBoost above
  XGBoost" and "the proxy above SVM" compare one lane's seeds with a
  fixed value. The pages now say so, in the BLUF and under the pairs. The
  readings stay as the entry's rule gives them; only "LightGBM above
  HGB" has two varying lanes. ULB is not affected: its lanes vary by
  seed.
- **Please read**: at the test month's own 0.5% budget every algorithm's
  recall is between 0.1215 and 0.1389, and no algorithm can exceed 427
  of the month's 2,962 frauds. The budget, not the model, sets most of
  that figure on IEEE-CIS (see V8).
- **Please read**: the 0.5% threshold chosen on the validation month
  flags 256 to 1,035 test rows (the proxy 748 to 1,035), not the 427 the
  budget allows. The per-page tables at that threshold therefore compare
  different alert volumes; the proxy's recall of 0.2810 there is not a
  0.5% budget result. Each page now gives its flagged count.
- The proxy's test scores are heavily tied (tie fraction 0.9365 to
  0.9631), and the score-health check warns on seeds 42 and 44. Its page
  now says so.
- F152's adversarial drift control stopped at its 20-round cap on both
  folds (final adversarial AUC 0.9906 and 0.9450). The comparison page
  now says so.
- The proxy chose its `full` configuration on every seed.
- Each page regenerates from the result: `scripts/f174_docs.py --check`,
  and `test_f174_docs.py` fails a committed page that differs, proven
  red. The generator refuses a result its fixed text does not describe.
- **Runtime finding**: seed 42 took 65 minutes, against the plan's
  inferred 30-35. Later seeds took 56 to 60. The SVM lane took about 26
  minutes per seed and the proxy 16-20.

## V5. Task E (F176): can a classical solver get below greedy?

`docs/phase2/F176_BELOW_GREEDY.md`; result
`experiments/phase2/results/f176_below_greedy.json`.

- Below greedy on 3 of 6 instances (42/free, 42/mid, 43/free), each by
  under 2e-05. SCIP did not beat greedy at its 1,200 s cap on any
  instance.
- **Finding to confirm**: the exact check fired (4 cases), but the swap
  search stayed at greedy on 3 of the 7 small cases where greedy is not
  optimal. So "nothing below greedy" on the other three IEEE-CIS
  instances does not show greedy is optimal. The module read the
  amendment's "the swap search must reach it" as "on at least one case".
  On a per-case reading the check fails, on 3 of 7 cases.
- The found gains are far smaller than the room bound (about 0.081 to
  0.097). Whether the device resolves differences that small is not
  tested (F104).

## V6. Task F (F169): the F108 plug-in passes

`docs/phase2/F169_PLUGIN_BINS.md`; result
`experiments/phase2/results/f169_plugin_bins.json`.

- Both estimators pass F108's rule on the main arm: LightGBM with 4,095
  bins on 5 of 5 seeds on every arm; HGB without early stopping on 4 of
  5.
- **Please read the attribution caveat**: the preset reading is "early
  stopping, not bins, was the cause", but HGB without early stopping
  still failed reference seed 44 (estimate 0.00431, Bayes error 0).
- **Please read (fresh-eyes review, fixed in Task J)**: LightGBM's
  reference-arm passes are degenerate. On seeds 42-45 its test AUPRC
  there is 0.0006, the arm's fraud rate: its probabilities are near 0
  everywhere, so its plug-in is near 0 for the wrong reason. The
  document now says so.
- F114's dependency is met. The document still recommends LightGBM with
  4,095 bins as F114's plug-in, now on the main and flip arms only (5 of
  5 on each).

## V7. Task G (F170): missed ULB frauds sit among legitimate rows

`docs/phase2/F170_MISSED_NEIGHBORS.md`; result
`experiments/phase2/results/f170_missed_neighbors.json`.

- The simulator check fired first, so the ULB reading was made.
- All 36 distinct frauds missed by every family have mostly legitimate
  neighbors, against 16.2% of the 370 caught; Mann-Whitney U rejects.
  Consistent with ULB's information limit, measured in the models' own
  30 features; not proof that no model could catch them.
- The neighbor share is in effect a 10-nearest-neighbor score in those
  features, so the result also fits "every model in this space misses
  the same frauds". The document's "What it changes" said "supports"; it
  now says "consistent with" (Task J).

## V8. Task H (F171) and Decision D7: the missed group on IEEE-CIS

`docs/phase2/F171_MISSED_IEEE.md`; results
`experiments/phase2/results/f171_missed_ieee.json` and
`experiments/phase2/results/f171_budgets.json`.

- At the preregistered 0.5% budget: 81.5% of IEEE-CIS pairs missed by
  all, against 11.2% on ULB. That budget alone forces 42.3% on IEEE-CIS.
- Decision D7 option 1 (post hoc, labeled exploratory): at 3.5%, 38.1%
  against 5.4%; at three times each fold's fraud rate, 18.2% against
  11.2%. The entry's reading (a share well below ULB's) is not met.
- ULB has 12 families and IEEE-CIS 4; a 4-family ULB count was not made.
  So the gap is not shown to come from the data. The document's headline
  was "No"; after the fresh-eyes review it is "Not shown" (Task J).
- The 3.5% budget is about one times IEEE-CIS's fraud rate and many
  times ULB's, so that row is tight on one dataset and loose on the
  other. The matched budget is the like-for-like row.
- D7's figure 426 alerts was 427 (the budget rounds up); a dated note
  under D7 records it.

## V9. Task I (F172): the Sprint 29 review's coverage gaps

- Each item from the Sprint 29 retrospective's "Review findings not
  fixed" has a test, each proven red.
- **One code change, please confirm**: F166's proxy now checks its
  training and validation labels against the classical lanes', as it
  checked its test labels. Checked equal on seeds 42 and 43 before the
  change; no recorded result changes.
- `test_the_budget_can_fail` now goes red through its timing assertion,
  and its proof refuses a red for any other reason.
- New `test_resume_loops.py`: F156's, F158's, F159's, F166's, F169's and
  F174's resume loops skip recorded units, at module level.

## V10. CI

- **CI was not green from 5719211 (Task B) to 4b19944.** The real
  failures were two guards in Sprint 30's own changes (a hook import and
  an interpreter path in an agent prompt), fixed in 98f05e5. From
  73a976e every run was canceled at the job's 10-minute limit, which
  reads as neither red nor green, so I missed it until the wake-up check.
- **Change to confirm**: `.github/workflows/ci.yml` raises the job's
  limit from 10 to 20 minutes (88bec13), with the reason in the file.
  The test step now takes about 11 minutes.
- The local full suite had two injection proofs that did not return to
  green (F166's bootstrap rejection, the figure registry); both pass
  alone. The final suite on a quiet tree settles it (V12).

## V11. Timers

- A 10, B 11, C 15, I 14 and H 13 active minutes.
- E 2, F 2 and G 6 active minutes are undercounts; see V2.
- J (the review fixes, added at Phase 5) 12 active minutes.
- D 31 active minutes. Its run ran in the background with D's timer
  paused, so the run's hours are not in the actual, by design.

## V12. Acceptance walk, evidence per task

Each line is the plan's task line, then where its evidence is.

- **A (F173)**: `task_issues` and the hook rule; `test_commit_msg_hook.py`,
  each term proven red. Closed #75.
- **B (F175)**: the activity hook and `--finish-task`'s active and
  elapsed figures; `test_task_activity.py`, proven red. Closed #76.
- **C (F168)**: the seven parts, D2's resume through `provenance.start`,
  the intent record; `test_agent_prompts.py`, `test_long_run_resume.py`,
  `device_store` tests, each proven red. Closed #77.
- **D (F174)**: entry (f74125d) before any score; 10 seeds; the tracked
  generator and eight pages (82a418d). Closed #78.
- **E (F176)**: dated Experiment 3 amendment (f74125d); the six instances
  rebuilt and greedy matched; the n = 20 check run first; SCIP at
  1,200 s and the local searches (76bb6f2). Closed #79.
- **F (F169)**: dated F108 amendment per D3 (f74125d); F108's harness,
  seeds, margin and pass rule; both arms (356893d). Closed #80.
- **G (F170)**: entry (f74125d); the simulator check fired first;
  distinct missed frauds counted (544f7aa, 356893d). Closed #81.
- **H (F171)**: entry (f74125d); F152's four families, months 4-6, seeds
  42-46 (fc966f4); D7's amendment (f2bf34a). Closed #82.
- **I (F172)**: each Sprint 29 gap has a test proven red (73a976e).
  Closed #83.
- **J (added at Phase 5, #84)**: the fresh-eyes review's 47
  observations (4 errors, 9 overclaims, 34 notes). Every error and
  overclaim is fixed in the documents or the F174 generator, except
  F176's lenient check reading, which is left for you to confirm (V5).
  The F174 generator's new statements each have a test, proven red. No
  result file changed.
- **Not met as planned**: the actuals for E, F and G undercount (V2), and
  D's runtime was about double its inferred estimate (V4).

## How to validate (recommended)

1. Read V4, V5, V6, V8 and V9's items marked "please read" or "to
   confirm". These are the findings that change how a result is used.
2. Open `docs/phase2/algorithms/IEEE_COMPARISON.md` and compare it with
   `ULB_COMPARISON.md`.
3. Confirm the CI limit change (V10) and F166's added label check (V9).
4. Optional: run `<venv python> scripts/f174_docs.py --check` and
   `<venv python> scripts/agent_status.py`.

## Results (team lead, 2026-11-01)

- V4, V5, V6, V8 and V9: accepted. V5's lenient reading of F176's exact
  check stands.
- V10: the CI job's limit is 13 minutes, not 20 (4306791).
- `IEEE_COMPARISON.md` and `ULB_COMPARISON.md` showed no TP, FP, TN or
  FN. Decision D8, answer 1: the comparison table gives each count at
  the test fold's own 0.5% budget as its range over the seeds, each
  algorithm page gives them per seed, and a note names the lanes whose
  tied scores flag more rows than the budget. Task K, #85.
