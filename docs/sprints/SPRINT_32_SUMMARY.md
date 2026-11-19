# Sprint 32 Summary: Close a Device Question, State Results in Dollars, Tighten Two Guards

**Sprint**: 32 | **Dates**: 2026-11-08 to 2026-11-16
**Branch**: `feature/20261108_Sprint_32`
**PR**: #116 to `develop`, merged 2026-11-16. Released to `main` by PR #121.
**Issues**: #110-#115, #117-#120 (Tasks A-J)
**Cards**: F188, F181, F185, F194, the F178 update, and the F150 and F111
drafts updated (not sent)
**Metered seconds**: **0**. No task called a device or a paid service.

Sources: `SPRINT_32_PLAN.md`, `SPRINT_32_VALIDATION.md`,
`SPRINT_32_DECISIONS.md`, `SPRINT_32_RETROSPECTIVE.md`, git history
`88f81ce..e4e61c3`, PR #116. Written at Sprint 33 refinement, before
planning (3.2.1). The master plan is not a source.

## The objective, and where it stands

**Close a device question, state results in dollars, tighten two
guards.** Done. The seven planned tasks met their acceptance. F188 shows
that at 200:1 resolution the rounded selection problem's answer, scored
on the real problem, is worse than greedy on all six IEEE-CIS instances,
so F25 stays on HOLD with a stated condition (D4). F185 states a result
in dollars: at the 0.5% alert count, ranking by expected loss catches
about four times the fraud dollars on IEEE-CIS month 4. The device guard
refuses Dirac-3 in every form, and the refusal gate measures branches.

## What was delivered

- **Task A (F181, #110)**: every Phase 2 module that names Dirac-3 is
  refused, marker or not (Sprint 31 D5).
- **Task B (F194, #111)**: the refusal gate measures branches and reads
  every print prefix.
- **Task C (F188, #112)**: the registered reading and the amendment's
  reading (`docs/phase2/F188_ROUNDING.md`).
- **Task D (F185, #113)**: the cost-weighted alert budget
  (`docs/phase2/F185_COST_BUDGET.md`).
- **Task E (F178, #114)**: the three learning documents at version 1.3.
- **Tasks F and G (F150, F111; #115, #117)**: the two gitignored drafts
  updated with this sprint's and earlier results. Neither was sent.
- **Task H (#118)**: the PR 116 review fixes. The Dirac-3 rule missed a
  held literal, a keyword and an import; all three are now refused.
- **Task I (#119)**: retrospective i1 to i4.
- **Task J (#120)**: the short review's two findings on the new pre-push
  hook, and CI red on 0fdcb67 (three failures, one from Task H).

## What the reviews found

- **PR #116**: Copilot (two small findings) and the pr-review-toolkit
  agents (three material findings, all fixed in Task H). Classes: a scan
  guard tested only against the form its author wrote; a cause stated as
  a finding without a test.
- **Improvement commits**: one short review, two findings at or above
  its bar, both fixed in Task J.
- **CI**: red on 0fdcb67 (a duplicate proof from Task H, a hook test that
  passed only on Windows, a missing inventory row); green on e4e61c3, the
  full job included.

## Decisions

- **At planning**: D1 (all five cards), D2 (option 3: the F150 request
  is not sent), D3 (the plan approved as amended, Task G added).
- **At Manual Validation**: D4 (option 3: F25 on HOLD until F188's
  delivered reading beats greedy at R = 200; F198 carded).
- **At the retrospective**: "i1. a i2. a i3. a i4. a i5. e". i1 to i4
  applied; i5 tracked.

## Effort

The ten timed tasks were estimated at 345 minutes; their recorded active
minutes total 188. That figure understates the work: Tasks A, F, G, H and
I each record time only after their timers started, and i1 now fixes the
cause of Task A's. Rows are in `docs/VELOCITY_LOG.md`.

## Next sprint readiness

Sprint 33 runs on `feature/20261116_Sprint_33`, cut from this sprint's
branch. Open from this sprint: F198 (F188 extended), F25's condition,
i5 (tracked in the retrospective), and the status tool's one wrong
"Nothing was written" message (noted in the retrospective, not carded).
