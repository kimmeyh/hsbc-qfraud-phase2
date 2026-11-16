# Sprint 31 Summary: Make Testing Fast and Sure, Then Read the Ceiling, the Segments and Dirac-3S

**Sprint**: 31 | **Dates**: 2026-11-04 to 2026-11-07
**Branch**: `feature/20261104_Sprint_31`
**PR**: #92 to `develop`, merged 2026-11-08. Released to `main` by PR #109.
**Issues**: #93-108 (Tasks A-P)
**Cards**: F179, F180, F177, F114, F157 (SPECTRA and QNN parts), F121,
F155, F95, F178, F13, and the pypdf bump (D6)
**Metered seconds**: **73.0**, all on Dirac-3S: F155 6.0 (D9) and F95
67.0 (D10, D12). One attempt per call; none retried.

Sources: `SPRINT_31_PLAN.md`, `SPRINT_31_VALIDATION.md`,
`SPRINT_31_DECISIONS.md`, `SPRINT_31_RETROSPECTIVE.md`, git history
`f6f25ed..c9da7a4`, PR #92. Written at Sprint 32 refinement, before
planning (3.2.1), because the close-out hook requires it. The master plan
is not a source.

## The objective, and where it stands

**Make testing fast and sure, then read the ceiling, the segments and
Dirac-3S.** Done. The twelve planned tasks met their acceptance. Testing
now runs by risk: CI's push job fails only on an untested changed
refusal, and the full job runs the red proofs of the changed files plus
a 5% rotating sample. Four experiments gave a reading: F114 puts the
IEEE-CIS ceiling near the achieved error, F157 ranks the SPECTRA lanes
and finds the QNN circuit dequantized, Experiment 5 accepts no segment,
and Dirac-3S accepts 1,350 variables and shows no schedule-4 effect.

## What was delivered

- **Task A (F179, #93)**: an exclusive lock around the status file's
  read, change and write; the review task follows pause and finish.
- **Task B (F180, #94)**: the testing analysis and a script-generated
  inventory of every test file (`docs/testing/`).
- **Task C (F177, #95)**: the levers chosen by D8, and the Manual
  Validation decisions D16-D18: the refusal gate in the push job, the
  selected and sampled proofs in the full job, cards F184-F192.
- **Task D (D6, #96)**: pypdf 6.21.2 to 6.21.4 in the lock.
- **Task E (F114, #97)**: IEEE-CIS month 4, 0.0254 (0.0232 to 0.0276)
  against an achieved 0.0293, with a calibration warning; the ULB figure
  is not usable. D11 and D13 set the estimator and the repair of
  overwritten score files.
- **Task F (F157, #98)**: the SPECTRA part. Boosted trees first on all
  four datasets; the proxy fifth or sixth of seven. The RBF SVM scored
  under D14.
- **Task G (F157, #99)**: the QNN part on IEEE-CIS. The circuit is
  dequantized.
- **Task H (F121, #100)**: Experiment 5 in full on the proxy. No segment
  accepted; recall at the 0.5% budget saturates on three segments.
- **Task I (F155, #101)**: the cloud `dirac-3s` queue accepted a
  1,350-variable job.
- **Task J (F95, #102)**: four schedule-4 fits on Dirac-3S, no change on
  any fit.
- **Task K (F178, #103)**: the three learning documents, first
  versions, with their link, acronym and claim test.
- **Task L (F13, #104)**: the Phase 2 plan draft and the backlog updated
  from the results.
- **Tasks M-P**: the Phase 5 fresh-eyes fixes (M); CI red on dfb1694,
  a defect this sprint introduced (N, not planned); the learning
  documents after the team lead's A1 review (O); the PR 92 review fixes
  and retrospective i1-i3 (P).

## What the reviews found

- **PR #92**: Copilot and three pr-review-toolkit agents. Recurring
  classes: a refusal or rule with no test or no proof; a result marked
  complete without a check that it is. Six findings fixed in Task P;
  the classes became i1-i3.
- **Improvement commits**: one short review. The shrink-only list was
  checked against itself, and one proof went red for another rule's
  reason; both fixed in 69e9bdd. Branch coverage and print prefixes went
  to refinement as F194.
- **CI**: green on c9da7a4, the full job included.

## Decisions

- **At planning**: D1 (scope), D2 (F157's parts), D3 (Experiment 5 in
  full), D4 (F150 delayed), D5 (every device run on Dirac-3S), D6
  (pypdf), D7 (the plan).
- **During the sprint**: D8 (F177's levers), D9, D10 and D12 (metered
  stops), D11 and D13 (F114), D14 (the RBF SVM).
- **At Manual Validation**: D15-D18.
- **At the retrospective**: D19-D21. i1, i2 b and i3 b applied; i4 and
  i5 skipped; i6 and i7 skipped and tracked.

## Effort

The plan's thirteen estimated tasks totaled 1,614 minutes; their
recorded active minutes total 2,613, a ratio of 1.62, ranging from 0.04
to 4.75 by task. Rows are in `docs/VELOCITY_LOG.md`. The sprint ran far
past the team lead's 1-2 hour target.

## Next sprint readiness

Sprint 32 runs on `feature/20261108_Sprint_32`, cut from this sprint's
branch. Open from this sprint: F150's request (Sprint 32 D2); F194, F195,
F196 and F197 carded from open items; F143's hold condition met; F25's
IEEE-CIS case to be tested by F188.
