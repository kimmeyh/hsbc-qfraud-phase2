# Sprint 29 Summary: Make the Tools Repeatable, Then Find the Best Each Model Can Do

**Sprint**: 29 | **Dates**: 2026-10-26 to 2026-10-30 (planned 2026-10-25)
**Branch**: `feature/20261025_Sprint_29`
**PR**: #63 to `develop`, merged 2026-10-30. Released to `main` by PR #73.
**Issues**: #64-72 (Tasks A-I)
**Cards**: F165, F159, F164, F156, F160, F166, F158, F167, and the pypdf
bump (no card; Decision 2)
**Metered seconds**: **0**. No Dirac, Braket or other paid service was
called.

Sources: `SPRINT_29_PLAN.md`, `SPRINT_29_VALIDATION.md`,
`SPRINT_29_DECISIONS.md`, `SPRINT_29_RETROSPECTIVE.md`, git history
`595f9dd..6242b8a`, PR #63. Written at Sprint 30 Phase 3.2.1. The master
plan is not a source.

## The objective, and where it stands

**Make every new Phase 2 result safe to resume and parallel to build,
check the Phase 2 documents' figures against their evidence, and take the
first measurements of four questions.** Done. All nine tasks met their
acceptance. Four experiments gave a decisive reading: F156 fails, F158's
cascade is below one model, F160 passes, and F166 ranks two adjacent
pairs.

## What was delivered

- **Task A (F165, #64)**: a resumed run keeps its own id, in a gitignored
  sidecar beside the result. After the PR review, `provenance.start`
  decides new, resume or refusal before any work.
- **Task B (F159, #65)**: a spawn-based parallel pool build. Every
  parallel pool equals the serial pool on the validation rows. The first
  resume hung for 9 hours; the build now stops after a time budget, which
  every caller must pass (IMP-3).
- **Task C (F164, #66)**: each figure in `docs/phase2/` resolves against
  the result files its own document names, or is registered with a
  reason (Decision 1 option 1).
- **Task D (F156, #67)**: the Henze-Penrose bound fails on F108's
  harness. F114 stays blocked; F169 carries the next candidate (Manual
  Validation D1 option 2).
- **Task E (F160, #68)**: Experiment 3 has room on IEEE-CIS, so F25's
  design reopens there. No solver has yet beaten greedy.
- **Task F (F166, #69)**: the best result per algorithm on ULB, one page
  per algorithm and a comparison page. Two adjacent pairs differ
  reliably. After the review the pages come from a tracked generator,
  `scripts/f166_docs.py` (IMP-2).
- **Task G (F158, #70)**: the per-type cascade is below one model.
  Step 3 lists the ULB frauds every stored model misses.
- **Task H (F167, #71)**: `docs/phase2/PHASE2_POC_PLAN_DRAFT.md`, on
  labeled assumptions.
- **Task I (#72)**: pypdf 6.21.1 to 6.21.2, for three advisories.
- **Task J**: the PR 63 review fixes (not planned).
- **Task K**: retrospective IMP-1 to IMP-4 and the fixes from their
  review.

## What the reviews found

- **PR #63**: four review agents on the draft PR, and Copilot (an
  overview, no inline comment). The recurring classes were compound rules
  with no test per term and document claims their source does not
  support. Single classes: a refusal after the work (in five modules,
  from one copied line), a guard applied at one call site, and a vacuous
  aggregate. Fixed; the lower-rated test-coverage items became F172.
- **Improvement commits**: one short review, five findings. Four were
  fixed; one became F173 (the timer rule accepts any running timer).
- **CI**: green on the merged head.

## Decisions

- **At planning**: Decision 1 (F164 per-document pools), Decision 2 (the
  pypdf bump), Decision 3 (F166's seed count from seed 42's time),
  Decision 4 (the plan). F168 carded for Sprint 30.
- **At Manual Validation**: D1, option 2 (F169 carded). F170 and F171
  carded.
- **At the retrospective**: D2, option 1 (IMP-1 to IMP-4 applied; IMP-5
  carded as F172). From 2026-10-30 every decision is written in full to
  `SPRINT_n_DECISIONS.md` before it is asked.

## Effort

The plan estimated 1,050 minutes. The recorded actuals are in the Sprint
29 rows of `docs/VELOCITY_LOG.md`. They do not sum to a measure of work:
four timers ran across overnight breaks or the F159 hang, one was never
started, and two started only when their runs began (retrospective
category 3). Only F, I, J and K are as measured.

## Next sprint readiness

Sprint 30 runs on `feature/20261030_Sprint_30`, cut from this sprint's
branch. Open from this sprint: F114 waits on F169; F25's device run waits
on F102's filing, and F176 is its proxy-side next step; F155 waits on
QCi's expansion; F150 waits on the SPECTRA authors.
