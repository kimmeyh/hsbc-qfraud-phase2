# Sprint 26 Summary: Reach Dirac-3S, Measure It, and Make the Proxy Repeatable

**Sprint**: 26 | **Dates**: 2026-10-13 to 2026-10-17
**Branch**: `feature/20261013_Sprint_26`
**PR**: #21 to `develop`, merged 2026-10-18. Released to `main` by PR #31.
**Issues**: #22-29 (Tasks A-H), #30 (Task I, added at Manual Validation)
**Cards**: F141, F145, F144, F142, F147, F126, F105, F146 (two updates;
the card is a permanent HOLD and stays open)
**Metered Dirac-3S seconds**: **86.0** over 5 fits, in three stops, each
approved separately (Decisions 7, 8 and 9), against about 172 planned and
a cap of 360

Sources: `SPRINT_26_PLAN.md`, `SPRINT_26_VALIDATION.md`,
`SPRINT_26_RETROSPECTIVE.md`, git history `6649053..e126dbd`, PR #21.
Written at Sprint 27 Phase 3.2.1. The master plan is not a source.

## The objective, and where it stands

**Take the first Dirac-3S measurements, and make the classical proxy they
are compared against repeatable.** Done. Dirac-3S is reachable, priced at
three sizes, and on the one resolvable Hamiltonian it returned the
reference optimum where Dirac-3 did not. A pool build is now repeatable
from its seed for Phase 2 builds.

## What was delivered

- **Task A (F141, #22)**: `qci-client` 5.0.3 and `eqc-models` 0.22.1 in
  the lock, the Windows venv and the WSL venv; `eqc_submit.device("dirac-3s")`;
  `device_type` required on Phase 2 hardware rows.
- **Task B (F145, #23)**: opt-in seeded weak learners. Two seeded builds
  are byte-identical. Phase 1's path is unchanged.
- **Task C (F144, #24)**: the proxy twin of B2's configuration, 10 seeds.
  Dirac-3 does not beat its own proxy on B2 (+0.0002, p = 0.92).
- **Task D (F142, #25)**: the Dirac-3S verify block, B1 2 fits, B2 1, B4
  2. On B4, Dirac-3S returned the reference optimum in every sample
  (weight cosine 0.999993 and 0.9999999, against Dirac-3's 0.895 and
  0.901); same-pool test AUPRC unchanged. Cost: 6 s at 91 variables, 21-22
  s at 560, 31 s at 833.
- **Task E (F147, #26)**: `scripts/edb_query.py`, a read-only query tool
  over the evidence library, and a proposal note.
- **Task F (F126, #27)**: the sparsity rule fixed before the fit fails one
  direction (held-out error 0.847 against the 0.05 tolerance).
- **Task G (F105, #28)**: the IEEE-CIS rolling-origin harness. Every
  leakage audit passes. No score is reported until F102 names its entry.
- **Task H (F146, #29)**: `docs/phase2/DIRAC_UNDERSTANDINGS.md` updated
  after Task A and after each F142 stop.
- **Task I (#30, added at Manual Validation, Decision 10)**: the
  cross-repo guard blocks Edit and Write into a forbidden repository's
  Claude Code project directory; EvidenceBasedDB is read freely, its store
  read-only.
- **Decision 11 (at Manual Validation)**: Dirac-3S is the default device
  for Phase 2 runs (`eqc_submit.PHASE2_DEVICE`); the shared default stays
  Dirac-3.
- **Retrospective improvements, all five applied (Decision 12)**: IMP-1,
  one QCi credential loader (`qci_env.py`); IMP-2, task timers that can
  pause and refuse a second open task; IMP-3, a metered result's
  interpretation waits for its fresh-eyes review; IMP-4,
  `check_ci_status.py` timeouts and a retry; IMP-5,
  `qpu_cost_model.quote()` from Dirac-3S per-sample times.

## What the reviews found

- **Code review**: 16 findings. **Fresh-eyes evidence review**: 16. **F142
  fresh-eyes review**: 9. Each was verified before acting. The evidence
  review found a Sprint 25 error that six documents carried; the F142
  review withdrew a claim before handover.
- **PR review (2026-10-17)**: Copilot gave an overview with no inline
  comments. The Claude PR review's findings (silent failures, code, tests,
  comments) were all fixed in the PR, except two test gaps that became
  card F149 for Sprint 27.

## Decisions

- **D1-D3 at approval**: option 1 each (F142 meets the F102 and F104
  dependencies inside its tasks; F121 holds until a Phase 2 run shows an
  in-segment edge with an interval excluding zero; the plan at 700
  minutes). **D5**: the Phase 1 boundary as five rules in CLAUDE.md.
  **D7-D9**: the three metered stops. **D10**: Task I. **D11**: Dirac-3S
  as the Phase 2 default. **D12**: all five improvements now.

## Effort

The plan estimated 700 minutes. The recorded actuals are in
`.claude/sprint_status.json` and the per-task rows in
`docs/VELOCITY_LOG.md`. They do not sum to a measure of work: six tasks
started within 12 minutes of each other and several ran at once, and
Task D's actual is elapsed time through three approval waits
(retrospective category 3; IMP-2 is the fix).

## Next sprint readiness

Sprint 27 runs on `feature/20261018_Sprint_27`, cut from this sprint's
branch. Open from this sprint: QCi question A6 (output resolution) and
the other unsent questions, which Sprint 27 drafts for the team lead to
send; F126 and F25 read against Dirac-3S not returning forced sparsity.
