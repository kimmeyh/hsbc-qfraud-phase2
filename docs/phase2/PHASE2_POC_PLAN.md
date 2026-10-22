# Phase 2 PoC Plan (Skeleton)

**Sprint 28 Task J (#56), card F13.** A skeleton, built before finalist
notification. Its content changes when the brief arrives. It restates no
figure that another file owns; it points to the owner.

## Calendar

Source: the program roadmap page, `quantumai.thequantuminsider.com/program/`,
from the team lead's screenshot of 2026-10-22. Re-check the page on
notification; a program can move its dates.

| Stage | Dates | What happens |
|---|---|---|
| Phase I review | 16 Sep - 14 Nov 2026 | Proposals reviewed; finalists selected |
| **Phase II PoC** | **17 Nov 2026 - 28 Feb 2027** | Selected teams build the PoC; the page lists AWS compute credits, Classiq tooling and expert office hours |
| Review and Close | 1 Mar - 30 Apr 2027 | PoC results benchmarked; winners announced 30 April 2027 |

- The PoC window is about 15 weeks. Our sprints have run about two days
  each (`docs/ALL_SPRINTS_MASTER_PLAN.md`, Past Sprint Summary), so the
  window holds many sprints. The binding limits are metered device
  seconds and review turnaround, not sprint count.
- Everything that must exist before 17 Nov is listed under "Before
  notification" below.

## Experiments

One row per experiment. The entry is the section 6 entry in
`experiments/phase2/PREREGISTRATION_DRAFT.md`. Quoted device seconds are
owned by `docs/HARDWARE_PLAN_PHASE_2.md` (the request sent to QCi) and are
not restated here.

| # | Experiment | Card(s) | Entry | Device | Seconds | State on 2026-10-22 |
|---|---|---|---|---|---|---|
| 1 | Isolate the confound (k=17 decomposition) | F112 | Written | none | none | Measured (Sprint 27) |
| 2 | Temporal validity, IEEE-CIS rolling origin | F105, F152 | Sprint 28 Task B | none | none | Harness built (F105); first score this sprint |
| 3 | Cardinality-constrained selection, integer solver | F94, F25, F153 | Sprint 28 Task C | Dirac-3S | Hardware plan, Experiment 3 rows | Controls built (F94); entry and proxy design this sprint; device runs need per-block approval |
| 4 | Replication under the source protocol (Loke et al.) | F111 | Sprint 28 Task D | none | none | Entry and proxy replication this sprint |
| 5 | Segment transfer (H5) | F121 | To write | to be decided | Hardware plan, Experiment 5 row | HOLD |
| 6 | Scaling claim: time against sample count | F110 | Sprint 28 Task E | proxy first | Hardware plan, Experiment 6 row | Proxy timing this sprint; device only under per-block approval |

Verification entries that are not experiments (F103, F106-F109, F142,
F144, F154) are listed in section 6 of the draft.

## Standing rules that bind the PoC

- **Dirac-3S is the default device** for Phase 2 runs (team lead, Sprint
  26; `docs/phase2/DIRAC_UNDERSTANDINGS.md`, section 2). The cloud
  `dirac-3s` queue is currently limited to 949 variables while the
  expansion unit is not fully implemented (team lead, 2026-10-22); F143
  waits on that, and F155 is the probe that detects the change.
- **Every metered block stops for explicit per-block approval** with call
  count and expected seconds (Criterion H). Plan approval never covers a
  metered call.
- **Every result records its outcomes**: confusion counts and per-row test
  scores (F154 rule, 2026-10-22; `outcome_record.py`).
- **Every entry is written before its run** and is revisable until the
  filing.

## The gate-based arm

F6 (`docs/phase2/F6_GATE_BASED_ARM.md`) recommends **pursue narrowly,
simulation only**. F106 (dequantization) and F107 (shot budget) are its
first two results. Any Braket hardware run is a new card with its own
cost and approval; the PoC credits named on the program page may change
that cost, **unverified** until the brief states them.

## Before notification (now to 14 Nov)

- The four entries this sprint writes (Experiments 2, 3, 4 and 6).
- F150's construction request to the SPECTRA authors (drafted this
  sprint; the send is the team lead's).
- F146's open item P1 with QCi's eqc-models contact.
- Section 7 of the Phase 2 draft ("Open items before filing").

## On notification

These wait for the brief, because their content depends on it:

- **Confidentiality**: read the brief's terms on receipt and apply them to
  every outward document before anything is sent. The terms are
  **unknown** until the brief arrives.
- **Datasets and evaluation**: whether the PoC prescribes data or metrics
  beyond ours; reconcile with section 2 of the draft.
- **Compute**: what the AWS credits and Classiq tooling cover, and whether
  that changes the gate-based arm's cost.
- **Device seconds**: QCi's allocation for the PoC against the hardware
  plan's request.
- **Dates**: confirm the calendar above against the brief.

## Cadence during the PoC

- Sprints as now: plan, approval, execution, Manual Validation,
  retrospective; one PR per sprint into `develop`.
- One experiment's device block per sprint at most, so each block's result
  is read before the next is requested.
- A checkpoint against the calendar at each sprint plan: weeks left,
  device seconds left, entries still to run.
