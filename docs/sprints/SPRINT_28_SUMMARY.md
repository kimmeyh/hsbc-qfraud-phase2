# Sprint 28 Summary: Experiment Entries First, Then Their First Measurements

**Sprint**: 28 | **Dates**: 2026-10-22 to 2026-10-25 (planned 2026-10-21)
**Branch**: `feature/20261019_Sprint_28`
**PR**: #46 to `develop`, merged 2026-10-25. Released to `main` by PR #62.
**Issues**: #47-59 (Tasks F, A-M), #60 (D4), #61 (retrospective improvements)
**Cards**: F154, F151, F152, F153, F111, F110, F162 (added at Manual
Validation), F115, F114 (still blocked), F150 (still blocked), F13 (the
skeleton; the card stays open), F146 (an update; the card is a permanent
HOLD and stays open)
**Metered seconds**: **0**. No Dirac, Braket or other paid service was
called.

Sources: `SPRINT_28_PLAN.md`, `SPRINT_28_VALIDATION.md`,
`SPRINT_28_RETROSPECTIVE.md`, git history `220a461..346fbfd`, PR #46.
Written at Sprint 29 Phase 3.2.1. The master plan is not a source.

## The objective, and where it stands

**Write the Phase 2 entries for Experiments 2, 3, 4 and 6 before the
November filing, and take each one's first zero-metered measurement.**
Done. Each entry was committed before its first score. Experiment 3's
proxy design failed its own falsifier, and the two blocked cards stayed
blocked after the step that could have unblocked them.

## What was delivered

- **Task F (F154, #47)**: confusion counts for every saved result, and
  the standing rule that every Phase 2 result records its confusion
  counts and per-row test scores (`outcome_record.py`, a guard, and the
  rule in `CLAUDE.md` and `docs/SPRINT_PROCESS.md`). No subset where one
  model is reliably better was found.
- **Task A (F151, #48)**: the ULB HGB comparator's instability is HGB's
  default `l2_regularization=0`; 1.0 alone closes the spread.
- **Task B (F152, #49)**: Experiment 2 on IEEE-CIS. P1 holds; P2's change
  mixes drift with training size.
- **Task C (F153, #50)**: Experiment 3's proxy design fails on all six
  instances: no room between greedy and the objective floor.
- **Task D (F111, #51)**: Experiment 4. The protocol does not measurably
  change the KNN lane, and its mean is not consistent with the paper's
  figure. The stable HGB beats the lane under both protocols.
- **Task E (F110, #52)**: Experiment 6. P1 is false; P2 holds at 833
  variables. The serial pool build is the cost.
- **Task G (F114, #53)**: a calibrated plug-in does not move the ceiling
  estimate. F114 stays blocked.
- **Task H (F150, #54)**: the construction request to the SPECTRA authors,
  drafted in the gitignored `docs/spectra_package/`.
- **Task I (F115, #55)**: integer cost scaling stated correctly in a new
  document, with the fit computed by code.
- **Task J (F13, #56)**: the PoC plan skeleton, dates from the program
  roadmap page.
- **Task K (F146, #57)**: QCi records updated and a reply drafted.
- **Task L (#58)**: pypdf 6.20.0 to 6.21.1.
- **Task M (F162, #59)**, added at Manual Validation: inside the SPECTRA
  pocket the CVQBoost proxy is not reliably above HGB or XGBoost on any
  cell.
- **D4 (#60)**, added at Manual Validation: `device_store.py` stores every
  device job in full; every new Phase 2 result carries a provenance block
  (`provenance.py`).
- **Retrospective improvements (#61)**: IMP-1 (content pins for every
  shrink-only list), IMP-2 (text guards read code only), IMP-4 (feature
  and fix commits name their issue), IMP-5 (one test per term of a
  compound rule) and IMP-6 (one refusing result writer). IMP-7 carded as
  F164; IMP-3 skipped.

## What the reviews found

- **PR #46**: four review agents and Copilot, on the draft PR. The
  recurring classes were shrink-only lists that could grow, document
  figures their result files do not support (seven), default modes that
  overwrite recorded output, and compound rules without a test per term.
  All fixed; each class has an improvement or a card.
- **Improvement commits**: one short review, five findings, all fixed in
  the same round.
- **CI**: red on eight commits from a text guard tripped by a docstring
  (fixed by IMP-2), and red once on the last review-fix commit from
  pytest's stale rewrite cache in proof mutations (fixed in `injection.py`).
  Green on the merged head.

## Decisions

- **At approval**: Decisions 1-6 and 8 as recorded in the plan; Decision
  7 kept F143 on HOLD and led to card F155.
- **At Manual Validation**: DV1 (F155's probe at 1,300 variables), DV2
  (F111 run as written, above its cap), DV3 (the QCi reply keeps the
  optional F115 paragraph), DV4 (older result files backfilled with
  outcome blocks), DV5 (reviews on the draft PR). F159, F162 and D4 were
  added.
- **At the retrospective**: see the improvements above.

## Effort

The plan estimated 1,030 minutes, plus 90 for F162. The recorded actuals
are in the Sprint 28 rows of `docs/VELOCITY_LOG.md`. They do not sum to a
measure of work: two timers started after the work, two actuals are wall
clock dominated by background runs, and D4 had no timer (retrospective
category 3).

## Next sprint readiness

Sprint 29 runs on `feature/20261025_Sprint_29`, cut from this sprint's
branch. Open from this sprint: F114 waits on a ceiling method that passes
F108's harness (F156 is the candidate); F150 waits on the SPECTRA
authors; F25 stays parked unless F160 finds room on a second dataset; F155
waits on QCi's expansion.
