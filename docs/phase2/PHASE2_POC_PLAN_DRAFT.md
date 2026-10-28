# Phase 2 PoC Plan (Draft on Stated Assumptions)

**Sprint 29 Task H (#71), card F167.** A draft of what the PoC plan will
look like after finalist notification, written now so its shape can be
reviewed. It is not the plan. The skeleton, `PHASE2_POC_PLAN.md`, and its
card F13 stay as they are; on notification F13 replaces every assumption
below with the brief's terms.

Rules for this draft:

- Every assumption about the brief is labeled **[Assumption An]** and
  listed in the register at the end. Nothing labeled an assumption is a
  fact.
- Every date has a source. The program dates are from the roadmap page
  (`quantumai.thequantuminsider.com/program/`, team lead's screenshot of
  2026-10-22), as in the skeleton.
- No figure is restated that another file owns. Device seconds live in
  `docs/HARDWARE_PLAN_PHASE_2.md`; results live in their result files and
  documents under `docs/phase2/`. This draft points to them.

## BLUF

- The PoC window is 17 Nov 2026 to 28 Feb 2027 (roadmap page). This
  draft splits it into five stages: onboarding, the zero-device
  experiments, the one device experiment, the write-up, and a reserve.
- **Only one experiment is planned to need the integer device:
  Experiment 3.** Its proxy design failed its falsifier in Sprint 28
  (`docs/phase2/F153_EXP3_DESIGN.md`), so it has no ready device block
  today. Getting it ready (F25, F160) is the critical path. If no design
  passes by the end of the first PoC month, the plan runs without a
  device experiment and says so.
- Experiments 1, 2, 4 and 6 have proxy or classical results already. In
  the PoC they are re-run on the brief's data and metrics, if the brief
  sets any **[A2]**.
- Experiment 5 stays on HOLD under its 2026-10-14 condition; it enters
  the PoC only if that condition is met.

## Stages

Sprint length during the PoC: one sprint per calendar week **[A6]**.
Before notification, sprints have run about two days each (master plan,
Past Sprint Summary). A week allows for review turnaround, device queue
time and the holidays inside the window.

| Stage | Weeks (PoC week 1 starts 17 Nov 2026) | Sprints [A6] | Exit condition |
|---|---|---|---|
| 0. Onboarding | 1-2 | P1-P2 | Brief read; confidentiality applied; data and metrics reconciled with section 2 of the preregistration draft; allocation confirmed |
| 1. Zero-device experiments | 3-7 | P3-P7 | Experiments 1, 2, 4 and 6 re-run on the PoC terms, each from its entry |
| 2. Device experiment | 4-11, overlapping stage 1 | P4-P11 | Experiment 3: a design that passes its falsifier on the proxy, then device blocks one at a time, each approved |
| 3. Write-up | 12-14 | P12-P14 | The PoC report; every figure resolves to a result file (F164's check) |
| 4. Reserve | 15 (to 28 Feb) | P15 | Nothing planned; absorbs slippage |

Review and Close follows, 1 Mar to 30 Apr 2027 (roadmap page). This
draft plans no work in it beyond answering questions **[A7]**.

## Experiments

For each: its entry (section 6 of
`experiments/phase2/PREREGISTRATION_DRAFT.md`), where it stands, its
device block, and the decision that releases it.

### Experiment 1 (F112): isolate the confound

- Entry: written 2026-10-18. State: measured, Sprint 27.
- PoC work: re-run on the brief's data if it differs from ours **[A2]**.
- Device: none.
- Released by: the stage 0 data reconciliation.

### Experiment 2 (F152): temporal validity on IEEE-CIS

- Entry: written 2026-10-22. State: result in
  `docs/phase2/F152_EXP2_RESULT.md`.
- PoC work: the same rolling-origin design on the brief's data, if the
  brief gives time-stamped data **[A2]**; otherwise the IEEE-CIS result
  stands as reported.
- Device: none.
- Released by: the stage 0 data reconciliation.

### Experiment 3 (F153, F25, F160): cardinality-constrained selection

- Entry: written 2026-10-22 (design). State: the proxy design fails the
  entry's falsifier (`docs/phase2/F153_EXP3_DESIGN.md`). F160 (this
  sprint) checks whether the room the falsifier requires exists on a
  second dataset.
- PoC work, in order:
  1. A design that passes the falsifier on the proxy. This is the
     critical path. Deadline: end of PoC week 4 **[A8]**.
  2. Device blocks on Dirac-3S, the default device, one at a time. Each
     stops for explicit approval with its call count and expected
     seconds (Criterion H). The block sizes are in
     `docs/HARDWARE_PLAN_PHASE_2.md`, Experiment 3; they are re-sized
     against the allocation the brief confirms **[A4]**.
  3. One block per sprint at most, so each result is read before the
     next is asked for.
- Device: Dirac-3S. The cloud queue's 949-variable limit stands until
  F155 shows it changed (skeleton, standing rules).
- Released by: the falsifier passing on the proxy (step 1), then the team
  lead's per-block approval (step 2).
- If step 1 has not passed by its deadline: the PoC report states that
  no design was found with room for a device to win, with the evidence,
  and stage 2 ends **[A8]**.

### Experiment 4 (F111): replication under the source protocol

- Entry: written 2026-10-22. State: result in
  `docs/phase2/F111_LOKE_PROTOCOL.md`.
- PoC work: none planned unless the brief asks for the source paper's
  protocol **[A2]**.
- Device: none.
- Released by: the stage 0 data reconciliation.

### Experiment 5 (F121): segment transfer

- Entry: to write. State: HOLD until a Phase 2 run, proxy or device,
  shows an in-segment edge over the matched control with an interval
  excluding zero (team lead, 2026-10-14, Sprint 26 Decision 2).
- PoC work: none planned. If the hold condition is met, the entry is
  written and the experiment is placed in stage 1 or 2.
- Device: to be decided.
- Released by: its hold condition.

### Experiment 6 (F110): training time against sample count

- Entry: written 2026-10-22. State: proxy result in
  `docs/phase2/F110_SCALING.md`; F159 (this sprint) measures the parallel
  pool build.
- PoC work: the proxy timing on the brief's compute, if the brief
  provides AWS compute **[A3]**. A device timing block only if the team
  lead approves it; the hardware plan sizes it.
- Device: proxy first; device only under per-block approval.
- Released by: the stage 0 compute confirmation.

### Work beside the experiments

- **Best achievable result per algorithm per dataset (F157, F166).**
  F166 does ULB in this sprint; the other datasets follow in stage 1, on
  the brief's data first **[A2]**.
- **The gate-based arm (F6).** Simulation only, as F6 recommends. A
  Braket hardware run is a new card with its own cost; the AWS credits
  may change that cost **[A3]**.
- **Figures resolve to evidence (F164).** Every PoC document passes the
  check before it goes out (stage 3 exit).

## Before notification (now to 14 Nov 2026)

The skeleton's list stands. This draft adds:

- F25 and F160: a design for Experiment 3 that passes on the proxy,
  started before the window so stage 2 does not start from zero.
- F166 and F157: the per-algorithm reference on ULB, so stage 1 compares
  against tuned lanes.
- F168: agent work and long runs that survive a usage limit, before the
  PoC's long runs start.

## Assumption register

Each assumption is replaced by the brief's term on notification (F13).

- **[A1] Confidentiality.** The brief sets terms for every outward
  document. Assumed: they allow a written PoC report that names the
  methods and datasets. Unknown until the brief arrives.
- **[A2] Data and metrics.** Assumed: the brief may prescribe data or
  metrics; where it does not, our datasets (ULB, IEEE-CIS, the SPECTRA
  substrates) and section 2 of the preregistration draft apply.
- **[A3] Compute.** Assumed: the AWS credits and Classiq tooling named on
  the roadmap page are available from PoC week 1. What they cover is
  **unverified**.
- **[A4] Device seconds.** Assumed: QCi's PoC allocation covers at least
  the Experiment 3 blocks in the hardware plan. Unknown until confirmed.
- **[A5] Dates.** Assumed: the roadmap page's dates hold. Re-checked
  against the brief.
- **[A6] Cadence.** Assumed: one sprint per week during the PoC, 15
  sprints, named P1-P15 here only for placement; real sprints keep this
  repository's numbering.
- **[A7] Review and Close.** Assumed: no new experiments after 28 Feb
  2027; only answers to reviewers.
- **[A8] Experiment 3 deadline.** Assumed: end of PoC week 4 for a design
  that passes on the proxy. This is a proposal for the team lead, not a
  program date.
