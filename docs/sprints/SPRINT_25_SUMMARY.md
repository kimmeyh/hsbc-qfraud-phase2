# Sprint 25 Summary: Learn the New Device, Then Build What Runs on Any Device

**Sprint**: 25 | **Dates**: 2026-10-10 to 2026-10-13
**Branch**: `feature/20261010_Sprint_25`
**PR**: #12 to `develop`, merged 2026-10-13. Released to `main` by PR #20.
**Issues**: #13-18 (Tasks A-F), #19 (Task G, added at Manual Validation)
**Cards**: F138, F139, F102 (first draft; the card stays open), F113, F29,
F94
**Metered Dirac-3 seconds**: **0**

Sources: `SPRINT_25_PLAN.md`, `SPRINT_25_VALIDATION.md`,
`SPRINT_25_RETROSPECTIVE.md`, git history `f543c0d..59d9ed2`, PR #12.
Written at Sprint 26 Phase 3.2.1. The master plan is not a source.

## The objective, and where it stands

**Find out what Dirac-3S changes before any further Dirac-3 seconds are
spent, and meanwhile build the classical work that does not depend on the
answer.** Done. Dirac-3S needs a client bump to reach (F141) and a
measured fit to price (F142). The classical items each reached a finding.

## What was delivered

- **Task A (F138, #13)**: `docs/phase2/DIRAC_3S_RESEARCH.md`. The pinned
  clients cannot reach Dirac-3S. QCi states the same 23 dB resolution for
  both devices. Whether the cloud queue exceeds 949 variables is
  unanswered.
- **Task B (F139, #14)**: `docs/phase2/F139_RERUN_REVIEW.md`. One
  recommendation per Dirac-3 run on record. It carded F141 to F145 and
  recommended closing F129.
- **Task C (F102, #15)**: `experiments/phase2/PREREGISTRATION_DRAFT.md`,
  the first draft. A living draft until Phase 2 is approved and a filing
  date is set.
- **Task D (F113, #16)**: `docs/phase2/F113_ORACLE_GAP.md`. Nothing
  supports a router: almost all of the oracle's gap comes from using the
  label on legitimate rows.
- **Task E (F29, #17)**: `docs/phase2/F29_SAMPLE_SIZE.md`. The card closes.
  It found that the pool build is not reproducible from its seed (F145).
- **Task F (F94, #18)**: `docs/phase2/F94_EXP3_CONTROLS.md`. Exact
  enumeration, greedy, simulated annealing and SCIP. On the training fold
  every selection ties, so F25 must build its Hamiltonian on held-out
  predictions and choose its ridge weight.
- **Task G (#19, added at Manual Validation)**:
  `docs/phase2/DIRAC_UNDERSTANDINGS.md` (F146, a permanent HOLD card),
  `docs/phase2/EDB_PROPOSALS.md`, and the F147 card.
- **Retrospective improvements**: IMP-1, claim labels in the Phase 2
  draft; IMP-2, show each falsifier can fire at plan verification; IMP-3,
  the cross-repo guard matches a folder name, then canonicalizes Windows
  folder names (security-review follow-up); IMP-4,
  `update_sprint_status.py --add-issue`.

## What the reviews found

- **Code review**: 10 findings, all fixed.
- **Fresh-eyes review of Tasks A-E**: 24 findings, all addressed. Four
  changed a conclusion, including F113's falsifier, which could not fire.
- **Fresh-eyes review of F94**: 15 findings, all addressed.

## Decisions

- **D1**: scope; F140 canceled. **D2**: F129 re-scored to 100. **D3**:
  priority numbers unchanged. **D4**: F94's exact solver is SCIP through
  PySCIPOpt. **At Manual Validation**: Task G added; F129 closed. **At
  the retrospective**: IMP-1 to IMP-4 applied ("apply all now").

## Effort

172 measured minutes against 750 estimated. The per-task rows are in
`docs/VELOCITY_LOG.md`. The reviews, their fixes and Task G were not
timed.

## Next sprint readiness

Sprint 26 runs on `feature/20261013_Sprint_26`, cut from this sprint's
branch. F141 leads it, because it gates every Dirac-3S run.
