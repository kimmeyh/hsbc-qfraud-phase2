# Phase 2 PoC Plan (Draft on Stated Assumptions)

**Sprint 29 Task H (#71), card F167.** A draft of what the PoC plan will
look like after finalist notification, written so its shape could be
reviewed. The skeleton, `PHASE2_POC_PLAN.md`, holds the calendar.

**Updated 2026-11-16 (Sprint 33 Task A, card F13): a filing without the
brief.** The Phase 2 brief is not available, and the preregistration is
to be filed without it (team lead, Sprint 33 Q1: "we are going to have to
file without the brief. Make assumptions as best possible"; "We will have
to make assumptions about all missing information"). So the assumption
register at the end is the working basis for the PoC and for the filing,
not a placeholder. Each assumption states its basis and what would
replace it. When the brief arrives, each one it covers is replaced by its
term and dated here. The preregistration
(`experiments/phase2/PREREGISTRATION_DRAFT.md`) cites these assumptions
by number.

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
  today. Getting it ready (F25, now on IEEE-CIS after F160) is the
  critical path. If no design
  passes by the end of the first PoC month, the plan runs without a
  device experiment and says so. Sprint 32's rounding test (F188) makes
  that outcome more likely: at 200:1 resolution (QCi's figure for
  Dirac-3, not measured on Dirac-3S), the rounded problem's best
  selection, scored on the real problem, is worse than classical greedy
  on all six IEEE-CIS instances. That is the amendment's reading, set
  after the first and with no decision rule; the registered reading is
  "kept" on two instances, with gains the rounding made
  (`docs/phase2/F188_ROUNDING.md`). On three of the six the pick is
  greedy's own selection, so that comparison also measures the rounding
  of the weights. F25 stays on HOLD until the release rule in the
  preregistration draft's Experiment 3 is met (team lead, Sprint 32 D4
  option 3, made testable by Sprint 33 D6 option 1): at R = 200, the
  pick delivers a gain of more than 1e-6 against greedy's selection
  solved the same way, on at least one of the six instances. F198's
  other ridge weights and resolutions each need a dated amendment before
  their run.
- Experiments 1, 2, 4 and 6 have proxy or classical results already
  (Experiment 5, below, also ran). In
  the PoC they are re-run on the brief's data and metrics, if the brief
  sets any **[A2]**.
- Experiment 5 ran on the proxy in Sprint 31 (team lead, Sprint 31 D3,
  hold set aside) and accepted no segment
  (`docs/phase2/EXP5_ROUTER.md`). It enters the PoC only with a
  segment measure that does not saturate.

## Stages

Sprint length during the PoC: one sprint per calendar week **[A6]**.
Before notification, sprints have run about two days each (master plan,
Past Sprint Summary). A week allows for review turnaround, device queue
time and the holidays inside the window.

| Stage | Weeks (PoC week 1 starts 17 Nov 2026) | Sprints [A6] | Exit condition |
|---|---|---|---|
| 0. Onboarding | 1-2 | P1-P2 | Brief read; confidentiality applied; data and metrics reconciled with section 2 of the preregistration draft; allocation confirmed |
| 1. Zero-device experiments | 3-7 | P3-P7 | Experiments 1, 2, 4 and 6 re-run on the PoC terms, each from its entry |
| 2. Device experiment | 4-11, overlapping stage 1 | P4-P11 | Experiment 3: the release rule met on the proxy, then a dated amendment fixing the instances, metric, margin, family, call count and seconds cap, then device blocks one at a time, each approved |
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
  entry's falsifier (`docs/phase2/F153_EXP3_DESIGN.md`). F160 (Sprint
  29) found the room on IEEE-CIS: greedy ends 0.096-0.098 above the
  floor on every instance (`f160_room_ieee.json`), so F25's design
  reopens there. F176 (Sprint 30) found selections below greedy on 3
  of the 6 instances, each by under 2e-05
  (`docs/phase2/F176_BELOW_GREEDY.md`). F188 (Sprint 32) found, by its
  amendment's reading, that at 200:1 resolution none of them survives
  as a delivered gain, and at 400:1 one does; its registered reading is
  "kept" on two instances, with gains the rounding made
  (`docs/phase2/F188_ROUNDING.md`). F25 is on HOLD: before
  any device run on this formulation, the release rule in the
  preregistration draft's Experiment 3 must be met (Sprint 32 D4 option
  3; Sprint 33 D6 option 1). F160 passed the registered design falsifier
  on IEEE-CIS (the design did not fail); the release rule is stricter than that falsifier.
- PoC work, in order:
  1. A design that meets the release rule on the proxy. This is the
     critical path. Deadline: end of PoC week 4 **[A8]**. Before any
     device call, a dated amendment to Experiment 3 states the
     instances, the primary metric and margin, the family, the call
     count and the seconds cap.
  2. Device blocks on Dirac-3S, the default device, one at a time. Each
     stops for explicit approval with its call count and expected
     seconds (Criterion H). The block sizes are in
     `docs/HARDWARE_PLAN_PHASE_2.md`, Experiment 3; they are re-sized
     against the allocation the brief confirms **[A4]**.
  3. One block per sprint at most, so each result is read before the
     next is asked for.
- Device: Dirac-3S. F155 (Sprint 31) showed the cloud queue accepts a
  continuous job of 1,350 variables, above the 949 base-module figure
  the skeleton states and within the 9,980 expansion-module figure
  (`docs/phase2/DIRAC_3S_SITE_SWEEP.md`, F14;
  `experiments/phase2/results/f155_variable_ceiling.json`). F143's hold
  condition is met. The pool failed the resolution screen, so the probe
  tests acceptance only, by design; its weights came back near flat
  (0.0007392 to 0.0007409, from the stored response
  `experiments/phase2/results/device_samples/f155_pool_1350_6aec89e4358b23d0cb37424a.json`),
  as a failed screen predicts.
- Released by: the release rule met on the proxy (step 1; Sprint 32 D4,
  Sprint 33 D6), the dated amendment, then the team lead's per-block
  approval (step 2).
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

- Entry: written 2026-11-05 (Sprint 31 Task H). The 2026-10-14 hold
  (Sprint 26 Decision 2) was set aside by Sprint 31 D3 to run it in
  full on the proxy. State: result in `docs/phase2/EXP5_ROUTER.md`. No
  ProductCD segment is accepted, for the proxy or for the HGB
  reference. Segment W cannot be scored. On C, R, H and S recall within
  the segment at the 0.5% budget is already at its maximum, so the
  measure cannot show an edge there.
- PoC work: none planned on this measure. A re-entry needs a segment
  measure that does not saturate (for example a smaller budget or a
  ranking measure), written as a new entry before any score is read.
- Device: none.
- Released by: a new entry, approved by the team lead.

### Experiment 6 (F110): training time against sample count

- Entry: written 2026-10-22. State: proxy result in
  `docs/phase2/F110_SCALING.md`; F159 (Sprint 29) measured the parallel
  pool build.
- PoC work: the proxy timing on the brief's compute, if the brief
  provides AWS compute **[A3]**. A device timing block only if the team
  lead approves it; the hardware plan sizes it.
- Device: proxy first; device only under per-block approval.
- Released by: the stage 0 compute confirmation.

### Work beside the experiments

- **Best achievable result per algorithm per dataset (F157, F166).**
  F166 did ULB, F174 IEEE-CIS and F157 SPECTRA's four datasets
  (Sprints 29-31, below). The brief's data follow in stage 1 **[A2]**.
- **F106's circuit against its twins (F157 QNN part, Sprint 31).**
  Dequantized on IEEE-CIS month 4: GAM and HGB match the circuit within
  the margin (`docs/phase2/F157_QNN_IEEE.md`). No PoC work is planned
  on this circuit.
- **The plug-in ceiling on real data (F114, Sprint 31).** After the
  re-run at learning rate 0.05 (`f114_real_ceiling_lr05.json`,
  `docs/phase2/F114_REAL_CEILING.md`), IEEE-CIS month 4 has an estimate
  of 0.0254 (0.0232 to 0.0276) with a calibration warning. The ULB
  figure, 0.00016, is far below the model's own achieved error and is
  not a usable ceiling. PoC work: none planned. A calibrated plug-in is
  a backlog item, not a PoC dependency.
- **Seven algorithms on SPECTRA's four datasets (F157 SPECTRA part,
  Sprint 31).** Boosted trees lead on every dataset and the proxy places
  fifth or sixth of seven by mean test AUPRC
  (`f157_spectra_algorithms_rbf.json`, `docs/phase2/algorithms/`). On
  telecom_churn the RBF SVM is reliably above the proxy, 0.8441 against
  0.7254. PoC work: these lanes are the reference a SPECTRA-style
  dataset in the brief is compared against **[A2]**.
- **Relaxation schedule 4 on Dirac-3S (F95, Sprint 31).** No change on
  the two fits with a Dirac-3S schedule-2 twin, whose pools fail the
  resolution screen, so the evidence is weak; the other two fits have
  only a Dirac-3 history and are not compared. About three times the
  device seconds per sample; 67.0 of 120 metered seconds
  (`docs/phase2/F95_SCHEDULE4.md`). There is no evidence for schedule 4,
  so PoC device blocks keep schedule 2.
- **The gate-based arm (F6).** Simulation only, as F6 recommends. A
  Braket hardware run is a new card with its own cost; the AWS credits
  may change that cost **[A3]**.
- **Figures resolve to evidence (F164).** Every PoC document passes the
  check before it goes out (stage 3 exit).
- **Fraud dollars beside fraud counts (F185, Sprint 32).** At the same
  number of alerts as the 0.5% budget, ranking by score times amount
  catches about four times the fraud dollars on IEEE-CIS month 4, and
  fewer frauds (`docs/phase2/F185_COST_BUDGET.md`). PoC work: results
  report both measures where amounts exist **[A2]**.

## Before the PoC window (to 16 Nov 2026), as it ended

The window opens 17 Nov 2026 (roadmap page). What this draft listed as
"before notification":

- F25, a design for Experiment 3 that meets the release rule on the
  proxy: not yet evaluated (no stored result computes the D6
  comparison; it needs no device time). F160 passed the registered
  falsifier; F25 is on HOLD
  under the release rule (Sprint 32 D4, Sprint 33 D6; Experiment 3,
  above).
  Stage 2 starts from F188 and F198, not from a passing design.
- F166, F174 and F157, the per-algorithm reference: done for ULB, IEEE-CIS and
  SPECTRA's four datasets (Sprints 29-31).
- F168, long runs that survive a usage limit: done (Sprint 30).

## Assumption register

Restated 2026-11-16 (Sprint 33 Task A) for a filing without the brief.
Each entry gives the assumption, its basis, and what replaces it. When
the brief or a program notice covers one, its term replaces the
assumption and the date is added here.

- **[A1] Confidentiality.** Assumed: the program allows a written PoC
  report and a filed preregistration that name the methods and the
  public datasets used (ULB, IEEE-CIS, SPECTRA). Basis: the filed Phase 1
  proposal named them, and every dataset is public. Replaced by: the
  brief's confidentiality terms. Until then, no sponsor material enters
  this repository (`CHECKLIST-Phase2.md`, "On notification").
- **[A2] Data and metrics.** Assumed: the program prescribes no dataset
  or metric, so our datasets and section 2 of the preregistration draft
  apply: AUPRC with its floor, ROC-AUC beside it, and the confusion
  counts at the 0.5% alert budget, with the recall cap reported where
  the test prevalence is above 0.5%; there the operating point is F171's
  matched budget, 3.0 times the test prevalence (preregistration draft,
  section 2). Fraud dollars caught at the same
  alert count where amounts exist (F185) is reported beside them; it is
  not a section 2 metric. Basis: no brief; the Phase 1
  submission was judged on these. Replaced by: any data or metric the
  brief prescribes, which then gets its own entry or amendment.
- **[A3] Compute.** Assumed: the AWS credits and Classiq tooling named on
  the roadmap page are available from PoC week 1. What they cover is
  **unverified**. Until confirmed, every planned run uses this
  workstation and the QCi allocation only. Basis: the roadmap page.
  Replaced by: the brief's compute terms.
- **[A4] Device seconds.** Assumed: QCi's PoC allocation covers at least
  the Experiment 3 blocks in `docs/HARDWARE_PLAN_PHASE_2.md`, on
  Dirac-3S (team lead, Sprint 31 D5). Every block still stops for
  per-block approval (Criterion H). Basis: the hardware plan sent to QCi.
  Replaced by: QCi's confirmed allocation.
- **[A5] Dates.** Assumed: PoC 17 Nov 2026 to 28 Feb 2027; Review and
  Close 1 Mar to 30 Apr 2027. Basis: the roadmap page (team lead's
  screenshot, 2026-10-22). Replaced by: the brief's dates.
- **[A6] Cadence.** Assumed: one sprint per week during the PoC, 15
  sprints, named P1-P15 here only for placement; real sprints keep this
  repository's numbering. Basis: review turnaround and device queue
  time. Replaced by: the team lead's schedule.
- **[A7] Review and Close.** Assumed: no new experiments after 28 Feb
  2027; only answers to reviewers. Basis: the roadmap page's stage
  names. Replaced by: the brief's terms for that stage.
- **[A8] Experiment 3 deadline.** Assumed: end of PoC week 4 for a design
  that meets the release rule on the proxy (Sprint 32 D4, made testable
  by Sprint 33 D6), and, before any device block, a dated amendment to
  Experiment 3 (the preregistration draft's "What filing commits to"). A proposal
  for the team lead, not a program date. Replaced by: the team lead's
  decision.
- **[A9] Preregistration filing venue and date.** Not set. Left blank
  and changeable until the team lead is notified otherwise (team lead,
  Sprint 33 Q2: "don't know yet. leave blank and changable until
  notified otherwise"). Replaced by: the team lead's notice.
- **[A10] Proceeding to the PoC.** Assumed: the team proceeds to the PoC,
  and the preregistration and this plan are prepared on that basis.
  Whether the team was selected is not recorded in this repository.
  Basis: the team lead's instruction to file (Sprint 33). Replaced by:
  the outcome, recorded in `docs/submission/` (`CHECKLIST-Phase2.md`).
- **[A11] The brief at filing.** Assumed: the preregistration is filed
  without the brief (team lead, Sprint 33 Q1). If the brief differs from
  an assumption here, the change is made by a dated amendment to the
  filed document, and an entry already run is not rewritten. Basis: the
  team lead's decision. Replaced by: the brief.
- **[A12] The reader of the filing.** Assumed: a reader of the filed
  preregistration can open this repository, so its card numbers (F112)
  and sprint numbers (Sprint 31) resolve in
  `docs/ALL_SPRINTS_MASTER_PLAN.md` and `docs/sprints/`. Basis: the
  venue is not set (A9). Replaced by: the venue; a reader without
  repository access would need a rewrite without those identifiers.

## Revision log

- 2026-10-30: written (Sprint 29 Task H, F167).
- 2026-11-05: Sprint 31 results added (Sprint 31 Task L, F13).
- 2026-11-16: assumptions restated for a filing without the brief;
  [A9]-[A12] added; Sprint 32's results (F188, D4, F185) added; the
  "before notification" list closed (Sprint 33 Task A, F13).
- 2026-11-17: after an outside adversarial review of the preregistration
  draft (Sprint 33 Task F, #128). Experiment 3's release rule (Sprint 33
  D6) and the dated amendment before any device call replace "F188's
  delivered reading beats greedy at 200:1"; F160 is said to have met the
  registered falsifier. Experiment 5 names four saturated segments. The
  per-algorithm reference names F174 for IEEE-CIS. [A2] reports the
  recall cap and says fraud dollars are reported beside section 2's
  metrics.
- 2026-11-18: after the draft's claim audit (Sprint 33 D9). F160
  "passed" the registered design falsifier, in the BLUF and stage 2.
