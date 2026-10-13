# Sprint 24 Summary: Close the Boundary, Fix the Tooling, Sweep the Lever

**Sprint**: 24 | **Dates**: 2026-10-09 to 2026-10-10
**Ran in**: this repository, `kimmeyh/hsbc-qfraud-phase2`. It was the first
sprint here.
**Branch**: `feature/20261008_Sprint_24`
**PR**: #2 to `develop`, merged 2026-10-10. Released to `main` by PR #11.
**Issues**: #3-10 (Tasks A-H), closed in the Phase 8 Pass 1 sweep
**Cards**: F131, F136, F132, F134, F133, F135, F128, F137
**Metered Dirac-3 seconds**: **0**

Sources: `SPRINT_24_PLAN.md`, `SPRINT_24_VALIDATION.md`,
`SPRINT_24_RETROSPECTIVE.md`, git history `9970ca7..1bf0e18`, PR #2.
Written at Sprint 25 Phase 3.2.1. The master plan is not a source.

## The objective, and where it stands

**Make this repository stand on its own, then take the first Phase 2
measurement in it.** Done. No live file names the Phase 1 repository, four
inherited tooling defects are fixed, Sprint 23's three improvements are
applied, and the first Phase 2 measurement (F128) ran here.

The merge to `develop` also released the Phase 1 repository's restore
commit (Sprint 23 D6). That is the Phase 1 session's work.

## What was delivered

- **Task A (F131, #3)**: `test_ci_status.py` stubs a copy of
  `check_ci_status.py` and never writes the tracked file.
- **Task B (F136, #4)**: each task's start time is recorded, and its actual
  is computed from it. Sprint 24 is the first sprint with measured actuals.
- **Task C (F132, #5)**: no live reference to the Phase 1 repository. The
  cross-repo guard forbids it, and `test_phase1_boundary.py` fails on any
  tracked file outside the approved list that names it.
- **Task D (F134, #6)**: the pre-commit hook blocks when its pattern file is
  missing or empty.
- **Task E (F133, #7)**: every Phase 2 device row, and every device-sample
  file, must carry a `job_id`.
- **Task F (F135, #8)**: `CLAUDE.md` requires every decision option to name
  its concrete values.
- **Task G (F128, #9)**: the leaf-regularization sweep on the proxy. **Its
  premise falsifier fired**: no `min_samples_leaf` value beats HGB with a CI
  that excludes zero on any dataset. The record is
  `docs/phase2/SPECTRA_IMPROVEMENT_RESEARCH.md` section 6.
- **Task H (F137, #10)**: pypdf 6.17.0 to 6.20.0 in the lock file.
- **Retrospective improvements**: IMP-1, one owner for the Dirac-3 balance
  (`experiments/results/allocation_reads.json`, guarded by
  `test_allocation_single_source.py`); IMP-4, a `TROUBLESHOOTING.md` entry
  for the cross-repo hook's false positive. IMP-2 and IMP-3 skipped.

## What the reviews found

- **Code review**: 6 real defects, all fixed in-sprint. One changed a
  label: F128's top value was called "best" though it was chosen on the
  splits it is reported on.
- **Fresh-eyes evidence review**: 8 interpretation overclaims in the F128
  write-up, all corrected. One was "parity" on energy_steel for what was a
  3-loss, 2-win split across seeds.

## Added during the sprint

- **The Dirac-3 balance** read 8,522 s on 2026-10-10, from QCi's grant of
  2026-10-09. The figure is owned by `allocation_reads.json`.
- **F138** (Dirac-3S research) and **F139** (the re-run review), carded by
  the team lead to run before any further Dirac-3 seconds.

## Decisions

- **D1**: scope. **D2**: F132's exceptions. **D3**: this repository renamed
  `hsbc-qfraud-phase2`. **D4**: `develop` is the GitHub default branch. It
  was briefly `main` on 2026-10-10 and is `develop` again (team lead:
  `develop` integrates features, `main` is the release branch). **D5**:
  F137 added. **D6**: the F132 guard allows the record files as a whole.
  **D7**: plan approved.

## Effort

84 measured minutes against 290 estimated. The per-task rows are in
`docs/VELOCITY_LOG.md`. The two reviews and their fixes were not timed.

## Next sprint readiness

Sprint 25 runs on `feature/20261010_Sprint_25`, cut from this sprint's
branch. F138 then F139 lead it and gate every card that spends Dirac-3
seconds.
