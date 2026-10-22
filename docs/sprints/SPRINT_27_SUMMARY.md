# Sprint 27 Summary: Gates Before Reporting, and the Screens That Need No Device

**Sprint**: 27 | **Dates**: 2026-10-18 to 2026-10-19
**Branch**: `feature/20261018_Sprint_27`
**PR**: #32 to `develop`, merged 2026-10-19. Released to `main` by PR #45.
**Issues**: #33-44 (Tasks A-L)
**Cards**: F149, F104, F102 (section 7; the card stays open), F112, F130,
F103, F109, F6, F106, F107, F108, F146 (the QCi question draft; the card
is a permanent HOLD and stays open)
**Metered seconds**: **0**. No Dirac, Braket or other paid service was
called.

Sources: `SPRINT_27_PLAN.md`, `SPRINT_27_VALIDATION.md`,
`SPRINT_27_RETROSPECTIVE.md`, git history `3dced65..220a461`, PR #32.
Written at Sprint 28 Phase 3.2.1. The master plan is not a source.

## The objective, and where it stands

**Build the gates that every Phase 2 result has to pass, and run the
screens that need no device.** Done. The resolution gate is public and
tested, the Phase 2 draft's section 7 items are closed or dated, and all
nine screens ran with zero metered seconds. Three of them left open
findings that bind later cards: F150, F151 and F114.

## What was delivered

- **Task A (F149, #33)**: the F142 pre-submit guard tested through the
  real library, with a fake at `requests.Session.request`; the runner's
  stop loop extracted to `_run_stop` and tested, codes 4 and 6 included.
- **Task B (F104, #34)**: `device_resolution.resolution_gate`, used by the
  F142 runner; it flags a seeded rebuild of B2's configuration and passes
  B4 oilgas.
- **Task C (F102, #35)**: the Phase 2 draft's section 7. New sections 2a
  (one Bonferroni family per experiment) and 2b (equivalence against a
  margin, default 0.005 AUPRC); section 5 recomputed by code; Experiment
  1's entry written before its intervals.
- **Task D (F112, #36)**: Experiment 1's paired intervals. P1 holds; P2 is
  equivalent within 0.005.
- **Task E (F130, #37)**: three lever screens on the proxy, with an opt-in
  `pair_count` in `qubo_proxy.build_pool`. No lever beats HGB on SPECTRA.
  ULB's HGB comparator is unstable under every setting tried, so ULB's
  reading is void.
- **Task F (F103, #38)**: SPECTRA Tier 1 reimplemented from the paper. It
  passes on the real target and the sparse pocket; the dense substrate
  misses.
- **Task G (F109, #39)**: Tier 1 on six datasets. The g4 prediction is not
  falsified.
- **Task H (F6, #40)**: the gate-based arm analysis. Pursue in simulation
  only.
- **Task I (F106, #41)**: the circuit against its classical twins.
  Inconclusive: no twin is shown to match the circuit, and the circuit
  does not beat every twin.
- **Task J (F107, #42)**: the shot budget. About 10,000 shots per row or
  more to stay within 0.005 AUPRC of exact.
- **Task K (F108, #43)**: a clean-room fraud simulator with a known
  ceiling. No ceiling method is validated.
- **Task L (F146, #44)**: the QCi question draft, kept in the gitignored
  `docs/qci_package/`. The team lead sent it on 2026-10-18.
- **Retrospective improvements (team lead, 2026-10-19)**: IMP-3 (every
  Phase 2 script is named by a test) and IMP-6 (`edb_query.py` prints
  UTF-8 on any console) applied; IMP-7 carded as F151; IMP-1, IMP-2,
  IMP-4 and IMP-5 skipped.

## What the reviews found

- **Code review**: findings on F108 (a stopped seed now counts as a miss),
  F104 (the exit code checks each row's matrix), F103, F106 and F112 (it
  had no test). All fixed before Manual Validation.
- **Fresh-eyes review of the interpretive documents**: 14 findings, each
  verified, then applied.
- **PR #32**: no review was posted on the PR.

## Decisions

- **At approval**: Decision 1 option 2 (the paper's substrates rebuilt;
  F150 carded for the authors' construction); Decision 2 option 1;
  Decision 3 set by the team lead (pair counts 30, 60, 90 and 119);
  Decision 4 not answered, so option 1 applied; Decision 5 option 1.
- **At Manual Validation**: validation complete; no minor updates, no
  backlog additions, no open questions.
- **At the retrospective**: see the improvements above.

## Effort

The plan estimated 1,470 minutes. The recorded actuals are in the Sprint
27 rows of `docs/VELOCITY_LOG.md`. They do not sum to a measure of work:
10 of 12 tasks ran with another task's timer open, six actuals are stamp
gaps and three are elapsed background-run time (retrospective category 3).

## Next sprint readiness

Sprint 28 runs on `feature/20261019_Sprint_28`, cut from this sprint's
branch. Open from this sprint: F150 waits on the SPECTRA authors'
construction; F151 must explain the ULB HGB comparator before any "beats
HGB on ULB" reading stands; F114 has no validated ceiling method to run.
QCi answered the questions on 2026-10-20, except P1.
