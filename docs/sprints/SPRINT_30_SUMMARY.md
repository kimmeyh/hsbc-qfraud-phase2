# Sprint 30 Summary: Measure the Work, Survive the Limits, Then Test the Ceiling and the Room

**Sprint**: 30 | **Dates**: 2026-10-30 to 2026-11-04
**Branch**: `feature/20261030_Sprint_30`
**PR**: #74 to `develop`, merged 2026-11-04. Released to `main` by PR #91.
**Issues**: #75-90 (Tasks A-P)
**Cards**: F173, F175, F168, F174, F176, F169, F170, F171, F172
**Metered seconds**: **0**. No Dirac, Braket or other paid service was
called.

Sources: `SPRINT_30_PLAN.md`, `SPRINT_30_VALIDATION.md`,
`SPRINT_30_DECISIONS.md`, `SPRINT_30_RETROSPECTIVE.md`, git history
`6242b8a..a428b92`, PR #74. Written at Sprint 31 Phase 3.2.1. The master
plan is not a source.

## The objective, and where it stands

**Measure task time as work, let agent work and long runs survive a usage
limit, and take the next readings on the ceiling and on Experiment 3's
room.** Done. All nine planned tasks met their acceptance. Five
experiments gave a reading: F174 ranks the seven IEEE-CIS lanes, F176
finds selections below greedy by under 2e-05, F169 is the first ceiling
method to pass F108's rule, F170 is consistent with ULB's information
limit, and F171 is not shown.

## What was delivered

- **Task A (F173, #75)**: the commit-msg hook admits a `feat:` or `fix:`
  commit only while the named issue's own task is timed.
- **Task B (F175, #76)**: an activity log; `--finish-task` records active
  minutes (gaps over 30 minutes subtracted) and elapsed minutes.
- **Task C (F168, #77)**: agent work and long runs survive a usage limit.
  Kept launch prompts with a restart section, a device intent record
  before each send, `scripts/agent_status.py` and the hourly wake-up
  (Decision D2: the in-file resume pattern is the standard).
- **Task D (F174, #78)**: the best result per algorithm on IEEE-CIS, 10
  seeds (D4, D5). Four of six adjacent pairs differ reliably; three
  lanes are deterministic on fixed months, so their seeds repeat one
  result (found in Task J).
- **Task E (F176, #79)**: below greedy on 3 of 6 IEEE-CIS instances,
  each by under 2e-05. SCIP at 1,200 s did not beat greedy.
- **Task F (F169, #80)**: LightGBM with 4,095 bins passes F108's rule on
  5 of 5 seeds; HGB without early stopping on 4 of 5 (D3).
- **Task G (F170, #81)**: the ULB frauds missed by every model have
  mostly legitimate nearest neighbors.
- **Task H (F171, #82)**: missed by all on IEEE-CIS, 81.5% against ULB's
  11.2% at 0.5%; not shown as a feature-richness effect, because 4
  families are compared with 12 (D7 added two post hoc budgets).
- **Task I (F172, #83)**: tests for the Sprint 29 review's coverage
  gaps, each proven red.
- **Tasks J-P (not planned)**: the Phase 5 fresh-eyes fixes (J); the
  Manual Validation fixes, with TP, FP, TN and FN on the comparison pages
  (K, D8); the per-push CI cut to a push job without the red proofs and a
  full job on ready for review (L, D9); the PR 74 review fixes (M);
  retrospective IMP-1 to IMP-5 (N, D10); the short review's fixes (O);
  and a red proof whose target occurred twice, found by CI's full job (P,
  #90).

## What the reviews found

- **PR #74**: review agents on the draft PR, and Copilot. Recurring
  classes: a refusal or reported state with no test, a state the tool
  cannot read reported as clean, a document claim its source does not
  support, and timing that does not reflect work. Fixed in Task M; the
  rest went to IMP-1 to IMP-5.
- **Improvement commit**: one short review, six findings, fixed in Task
  O. The status-file lock and the review-task order became F179. The
  review ran 14 minutes on an uncapped brief; the Phase 7 checklist now
  caps it.
- **CI**: the full job on the final head, a428b92, concluded success.
  It ran on a degraded GitHub Actions service, which marked it complete
  about 25 minutes after its last step.

## Decisions

- **At planning**: D1 (scope), D2 (F168's resume pattern), D3 (F169's
  arms), D4 and D5 (F174's seeds, no time cap), D6 (the plan).
- **During the sprint**: D7 (F171's budgets), D8 (the comparison pages'
  counts), D9 (CI under 5 minutes per push).
- **At the retrospective**: D10, "do imp-1-5 now". F177, F178, F179 and
  F180 carded.

## Effort

The plan estimated 975 minutes. The recorded actuals are in the Sprint 30
rows of `docs/VELOCITY_LOG.md`, as active and elapsed minutes. Active
ratios run from 0.02 to 0.38 where an estimate exists; four rows are
flagged "cause unverified", and two research rows ran their computation
in the background. The unplanned tasks J-P took more active time than
the nine planned tasks together. F180 is carded to find where the time
goes.

## Next sprint readiness

Sprint 31 runs on `feature/20261104_Sprint_31`, cut from this sprint's
branch. Open from this sprint: F114 is unblocked by F169; F177's local
levers wait on F180; F179 carries the status-file lock; F25's device run
still waits on F102's filing.
