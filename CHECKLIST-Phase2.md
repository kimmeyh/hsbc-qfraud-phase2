# Checklist: Phase 2 (LIVE)

Owners: **H** = Harold (only you can do it), **C** = Claude (I do it), **H+C** = decision or review done together.

**STATUS: LIVE from 2026-10-03.** One checklist for two stages: Stage A, now to
finalist notification (expected mid-November 2026, Guidelines s2), and Stage B,
the PoC sprint (November 2026 to February 2027). Provisional until the Phase 2
brief arrives, and the brief overrides this file.

**`CHECKLIST-Phase2-pre.md` was merged into this file on 2026-10-03 and
deleted** (team lead). Its open items are below; its completed items are the
pointer list at the end; its full text is in git history. `CHECKLIST-Phase1.md`
is CLOSED and still names the old file; that pointer is left as it was.

**Nothing here may touch the submitted documents.** They are a record.

## Change policy (team lead, 2026-09-12)

**THE SIX COMMITTED EXPERIMENTS DO NOT CHANGE.** They are what proposal section
6 promises, in the order it promises them, and the submission was judged on that
commitment. Reordering or dropping one is not a checklist edit; it would be a
departure from a published commitment and needs to be recorded as one.

**Everything else here may grow.** Items may be ADDED, and committed items may be
EXPANDED with detail, sub-steps, acceptance criteria and resourcing as we learn
what Phase 2 actually requires. That is expected and is why this file is not
frozen like Phase 1.

The distinction in one line: **add and elaborate freely; do not alter the six.**

## Correction to the six (team lead approved, 2026-10-03)

Items 5 and 6 were transcribed wrongly when this file was drafted on
2026-09-12, and the policy above cites "section 6" where the list is in
**section 5** of the proposal. The filed proposal commits to 5 = Segment
transfer (H5) and 6 = Scaling claim. Verified 2026-10-03 with `pypdf` against
`docs/paper/out/proposal.pdf`, whose hash is the one
`test_published_artifacts.py` pins as submitted. `HARDWARE_PLAN_PHASE_2.md`, as
sent to QCi, uses the same numbering.

This restores the published commitment; it does not depart from it. The
gate-based arm, which this file listed as 5, is a section 7 commitment and is
listed under "Other commitments in the proposal". B4 and B5, listed as 6, are
not in the proposal's six: B4 is the replication half of Experiment 5 (F90),
and B5 runs inside F90.

## Standing constraints

- [x] **C**: The three submission documents are a RECORD, not a draft. A hook
      refuses edits without recorded approval
- [x] **C**: History is never rewritten and `prereg-freeze` never moves. Two
      commits are cited in judged PDFs that cannot be corrected. A hook refuses
      force-pushes and tag moves
- [ ] **H+C**: Any new experiment is dated post-submission and reported as such,
      never folded back into the submitted claims
- [ ] **H+C**: Each experiment is preregistered BEFORE its result is seen
      (F102). Building a harness before preregistration is allowed; reporting a
      comparison is not

## Stage A: before notification (no metered spend unless a card says so)

Nothing in this stage is time-bound. Schedule on value.

- [ ] **H**: Ask Javier Mancilla for the SPECTRA construction details,
      including how `in_pocket` is built (feeds F101 and F103)
- [x] **H+C**: Bring the off-repository SPECTRA device result into the
      repository with its configuration, fits, seeds and arm (F90, first task).
      **Already satisfied** (2026-10-05): the configuration was brought in
      2026-10-03, and `FROZEN_CELLS` encodes it field by field
- [x] **C**: F100 complete classical bar on identical SPECTRA features.
      Sprint 21: `docs/F100_CLASSICAL_BAR.md`
- [x] **C**: F101 `in_pocket` provenance diagnostic.
      Sprint 21: `docs/F101_IN_POCKET_PROVENANCE.md`
- [x] **C**: F124 SPECTRA lever research before any further device run.
      Sprint 22: `docs/phase2/SPECTRA_IMPROVEMENT_RESEARCH.md`, approved by
      the team lead 2026-10-07; it gates every device run
- [ ] **C**: F102 Phase 2 preregistration framework
      - **Progress 2026-10-13**: first draft,
        `experiments/phase2/PREREGISTRATION_DRAFT.md` (Sprint 25). A living
        draft until Phase 2 is approved and a filing date is set; its
        section 7 lists what remains
      - **Progress 2026-10-18** (Sprint 27 Task C): section 7 items done,
        sections 2a and 2b added; open: entries for Experiments 2-6 and the
        filing date (team lead)
      - **Progress 2026-10-22/23** (Sprint 28): entries for Experiments 2,
        3, 4 and 6 and for F162 written before their first scores, each with
        its result recorded after (F152, F153, F111, F110, F162). Open: the
        filing date (team lead)
      - **Progress 2026-10-26/28** (Sprint 29): entries for F156, F160,
        F166 and F158 written before their first scores, each with its
        result recorded after. Open: the filing date (team lead)
      - **Progress 2026-10-31** (Sprint 30): entries for F174, F176, F169,
        F170 and F171 written before their first scores, and F171's budget
        amendment before its post hoc count (Decision D7). Open: the filing
        date (team lead)
      - **Progress 2026-11-05** (Sprint 31): entries for F114 (with the
        staged re-run amendment, efe7b88), F157's SPECTRA and QNN parts
        (with the D14 RBF amendment, a25b90a), Experiment 5, F155 and F95
        written before their first scores. Open: the filing date (team
        lead)
      - **Progress 2026-11-09** (Sprint 32): entries for F188 (with its
        amendment, written after the first reading and before the second)
        and F185 written before their first scores. Open: the filing date
        (team lead)
      - **Progress 2026-11-18** (Sprint 33): ready to file and marked
        FINAL, submitted for filing 2026-11-18 (team lead); copied to
        `experiments/phase2/PREREGISTRATION_FINAL.md`; a drift guard,
        `experiments/src/test_phase2_prereg_draft.py`. Open (Sprint 34):
        the filing venue, the lock step in its section 7, and Experiment
        3's release rule
      - **Progress 2026-11-24** (Sprint 34): locked. Post-filing text goes
        in `experiments/phase2/PREREGISTRATION_AMENDMENTS.md` (P2-A1 to
        P2-A8); the sent text is restored as
        `experiments/phase2/PREREGISTRATION_SUBMITTED_2026-11-18.md`;
        `experiments/src/test_phase2_prereg_filed.py` hashes the three
        copies; tag `phase2-prereg-filed` at b8e2c0e. Experiment 3's
        release rule met on one instance (P2-A6 to P2-A8); F25 released
        for Sprint 35 (D8). Experiment 5b entered (P2-A3, P2-A5). Open:
        the filing venue (team lead)
- [x] **C**: F154 every saved test result's confusion counts, and where
      each model wins. Sprint 28: `docs/phase2/F154_WHERE_MODELS_WIN.md`;
      the standing rule that every result records its outcomes (CLAUDE.md),
      and from D4 its provenance
- [x] **C**: F185 a cost-weighted alert budget. Sprint 32:
      `docs/phase2/F185_COST_BUDGET.md`. At the 0.5% alert count, ranking
      by score times amount catches about four times the fraud dollars on
      IEEE-CIS month 4, on all ten seeds, and fewer frauds; on ULB no
      reliable difference
- [x] **C**: F103 SPECTRA Tier 1 known-answer check on the paper's own dataset.
      Sprint 27: `docs/phase2/F103_TIER1_CHECK.md`; the dense substrate
      repeats under F150
- [x] **C**: F6 gate-based arm analysis, then F106 (dequantization check) and
      F107 (shot budget; the Schmidt-rank threshold is undefined for
      classical inputs) if F6 recommends pursue. Sprint 27:
      `docs/phase2/F6_GATE_BASED_ARM.md` (pursue narrowly, simulation only),
      `F106_DEQUANTIZATION.md`, `F107_SHOT_BUDGET.md`. Sprint 31 (F157 QNN
      part): on IEEE-CIS, GAM and HGB are no worse than the circuit within
      the 0.005 margin, so the circuit is dequantized
      (`docs/phase2/F157_QNN_IEEE.md`)
- [x] **C**: F108 ceiling validation harness.
      Sprint 27: `docs/phase2/F108_CEILING_VALIDATION.md`; no method validated.
      Sprint 29 (F156): the Henze-Penrose bound fails on the harness too;
      F169 tries the second named candidate. Sprint 30 (F169): both
      plug-ins pass F108's rule; LightGBM's reference-arm passes are
      degenerate, so the reading rests on the main and flip arms
      (`docs/phase2/F169_PLUGIN_BINS.md`). Sprint 31 (F114): on real data,
      the re-run at learning rate 0.05 passed the shuffled-label check by
      about 0.00001; IEEE-CIS 0.0254 against an achieved 0.0293, with the
      calibration warning; the ULB figure is not a usable ceiling
      (`docs/phase2/F114_REAL_CEILING.md`)
- [x] **C**: F109 SPECTRA domain ladder and aggregation experiments.
      Sprint 27: `docs/phase2/F109_TIER1_LADDER.md`
- [x] **H**: Goal ordering for prioritization: field advancement leads if it
      conflicts with the track outcome (team lead, 2026-10-03). The backlog
      priorities follow this

## On notification

- [ ] **H**: Record the outcome and the date in `docs/submission/`
- [ ] **H**: T&C s7 binds only on receiving sponsor problem statements,
      technical briefings, compute resources or other non-public material. From
      that point, treat all of it as confidential and keep it OUT of this public
      repository
- [x] **H+C**: Decide where Phase 2 work lives. The public repository is a
      Phase 1 asset; Phase 2 may need a private one. **Decided 2026-10-07**
      (team lead, Sprint 22): a new private repository; this one is restored
      as filed and archived (F127, `docs/PHASE_SEPARATION.md` section 9).
      **Done**: the Phase 1 repository's `as-filed` tag is at 4aa17d2 and the
      repository is archived (verified read-only 2026-10-13)
- [ ] **H+C**: If selected, start F13 (Phase 2 PoC sprint planning). If not
      selected, the repository stands as the public record of a null reported
      honestly
      - **Progress 2026-10-22** (Sprint 28 Task J): skeleton
        `docs/phase2/PHASE2_POC_PLAN.md`, dates cited to the program
        roadmap; the content after notification stays open
      - **Progress 2026-10-27** (Sprint 29, F167): a draft of the full plan
        on labeled assumptions, `docs/phase2/PHASE2_POC_PLAN_DRAFT.md`; F13
        replaces each assumption with the brief's terms on notification
      - **Progress 2026-11-16** (Sprint 33 Task A): the draft restated for
        a filing without the brief; assumptions A1-A12, each with its
        basis and what replaces it, confirmed by the team lead 2026-11-17

## The six experiments, in the order the proposal commits to (section 5)

- [ ] **C**: 1. Isolate the confound -- the 153-variable ULB cell at k=17,
      subset order 2. Zero device seconds
      - Run as post-submission proxy work in Sprint 18 (F64, then F91's fourth
        corner): `docs/F64_LADDER_DECOMPOSITION.md`. The interval on the
        decomposition is done (F112, Sprint 27): P1 holds and P2 is
        equivalent within 0.005, on the proxy
        (`experiments/phase2/results/f112_intervals.json`)
- [ ] **C**: 2. Temporal validity -- IEEE-CIS rolling-origin folds supply the
      test ULB's two-day span cannot. No configuration is recommended for a
      production path until this is settled
      - Backlog: F105 (folds, entity reconstruction, leakage audit)
      - **Progress 2026-10-14**: F105's harness built
        (`docs/phase2/F105_IEEE_HARNESS.md`): every leakage audit passes on
        all three folds; the adversarial control hits its round cap, and
        month 6 is a partial bucket, which Experiment 2's entry must decide.
        No score reported
      - **Progress 2026-10-22** (Sprint 28, F152): entry first, then the
        first rolling-origin score. P1 holds (XGBoost above logistic
        regression on months 4 and 5); P2's month-4-to-5 change mixes drift
        with training size (`docs/phase2/F152_EXP2_RESULT.md`)
- [ ] **H+C**: 3. Cardinality-constrained selection on Dirac-3's integer solver,
      against a time-capped MIQP, greedy, and simulated annealing. **A win
      against a certified-optimal classical solve is a result; a win against no
      control is not**
      - Backlog: F94 (controls), F104 (resolution screen), F17 (simulator),
        F25 (device run, HOLD). Needs 3,070 s; see Resourcing
      - **Progress 2026-10-07**: F17's emulator was built (Sprint 22). It
        does not reproduce the device's sparsity, so it cannot size this
        experiment yet; follow-up F126
      - **Progress 2026-10-13**: F94's controls built and run
        (`docs/phase2/F94_EXP3_CONTROLS.md`): exact enumeration, greedy,
        simulated annealing and SCIP (certified on small checks). On the
        training fold every selection ties, so the experiment must build
        its Hamiltonian on held-out predictions; on the validation fold,
        greedy is the bar to beat
      - **Progress 2026-10-15/16**: F126's sparsity rule fails; F142 found
        Dirac-3S returns B4's optimum without Dirac-3's forced sparsity
        (`docs/phase2/F142_DIRAC3S_VERIFY.md`). Dirac-3S is now the Phase 2
        default device (Sprint 26 Decision 11); the experiment's sizing is
        a Dirac-3 figure to re-price
      - **Progress 2026-10-22** (Sprint 28, F153): the entry's proxy design
        fails on all six instances: the gap to the floor is 0.0016-0.0026,
        below 0.01, and both resolution checks fail
        (`docs/phase2/F153_EXP3_DESIGN.md`). F160 repeats the room check on
        a second dataset
      - **Progress 2026-10-28** (Sprint 29, F160): on IEEE-CIS the room
        check passes after its positive control, so F25's design reopens
        there (`experiments/phase2/results/f160_room_ieee.json`). SCIP did
        not beat greedy within its cap, so no solver has yet been shown to
        beat greedy
      - **Progress 2026-10-31** (Sprint 30, F176): a selection below greedy
        on 3 of the 6 instances, each by under 2e-05; SCIP did not beat
        greedy at its 1,200 s cap, and the swap search missed the optimum
        on 3 of the 7 check cases where greedy is not optimal
        (`docs/phase2/F176_BELOW_GREEDY.md`)
      - **Progress 2026-11-09** (Sprint 32, F188): at 200:1 resolution the
        rounded problem's best selection, scored on the real problem, is
        worse than greedy on all six instances
        (`docs/phase2/F188_ROUNDING.md`). F25 stays on HOLD: before any
        device run, F188's delivered reading must beat greedy at 200:1
        (D4 option 3, 2026-11-13). F198 extends F188
      - **Progress 2026-11-23** (Sprint 34, F200 and F198): the filed
        release rule is met on 42/mid only, by about 6 parts per million
        of the objective (P2-A6 to P2-A8,
        `experiments/phase2/results/f188_release_rule.json`); F198's
        extension is `docs/phase2/F198_EXTENDED.md`. F25 released by the
        team lead 2026-11-24, to run in Sprint 35 (D8 option 1)
- [ ] **C**: 4. Replication under source protocol -- H1a reproduces Loke et al.
      under their split and comparator, target AUC-PR 0.80, then re-evaluates
      under ours
      - Backlog: F111
      - **Progress 2026-10-23** (Sprint 28, F111, on the CVQBoost-KNN
        proxy): the KNN lane's mean under their protocol is 0.760, not
        consistent with 0.8108; their protocol does not measurably change
        the lane; the stable HGB beats it under both
        (`docs/phase2/F111_LOKE_PROTOCOL.md`)
- [ ] **H+C**: 5. Segment transfer (H5) -- replicate a prior Dirac-3 campaign's
      in-segment wins with seeds and intervals, then test transfer to fraud
      segments against a matched random-segment control. **A failure of H5 is
      the third condition that retires the approach** (proposal section 5)
      - Backlog: F90 (replication half), F100 and F101 (make F90 readable),
        F121 (transfer half and router acceptance, HOLD)
      - **Progress 2026-10-06**: the replication half ran on Dirac-3 (B4,
        10 feasible cells). The in-segment edge is negative on all 8
        scoreable cells; energy_steel is unscoreable. Transfer half not
        started. `docs/B4_B5_HARDWARE_RESULT.md`
      - **Progress 2026-10-23** (Sprint 28, F162, classical proxy, ten
        seeds): inside the pocket the proxy is not reliably above HGB or
        XGBoost on any cell, and XGBoost is reliably above it on
        energy_steel and oilgas_gasturbine (`docs/phase2/F162_IN_POCKET.md`).
        F161, the B4 re-run on Dirac-3S, is carded with its run condition
      - **Progress 2026-11-05** (Sprint 31, Experiment 5, classical): no
        ProductCD segment is accepted, for the proxy or for HGB; on every
        segment that can be scored, the champion's recall is already at the
        0.5% budget's maximum, so the measure cannot show an edge
        (`docs/phase2/EXP5_ROUTER.md`)
- [ ] **C**: 6. Scaling claim -- end-to-end training time against sample count,
      including Hamiltonian construction
      - Backlog: F110
      - **Progress 2026-10-22** (Sprint 28, F110, proxy): P1 is false (the
        pool build grows with a slope of about 1.4 in rows); P2 holds at
        833 variables and fails under the rule at 91, where the subtracted
        J build exceeds the solve (`docs/phase2/F110_SCALING.md`). Device
        arm not run
      - **Progress 2026-10-28** (Sprint 29, F159): the pool build runs in
        parallel and gives the same pool as the serial build on the
        validation rows at every fraction and worker count
        (`experiments/phase2/results/f159_parallel_pool.json`)

## Other commitments in the proposal

- [ ] **H+C**: The gate-based arm on Amazon Braket or Classiq, against a matched
      classical baseline, **reported whatever the outcome** (proposal section 7:
      hands-on Braket "makes a Phase 2 gate-based arm a commitment")
      - Backlog: F6, F106, F107, F116 (HOLD), F117 (HOLD)
- [ ] **H+C**: Router acceptance -- at least one point of recall at the 0.5%
      budget above the classical champion alone, out of time, on prespecified
      segments, against a matched random-segment control (proposal section 5,
      Metrics)
      - Backlog: F121 (HOLD)
      - **Progress 2026-10-13**: F113's in-time bound
        (`docs/phase2/F113_ORACLE_GAP.md`). The oracle beats XGBoost by
        5.0 points, but two XGBoost configurations give 3.6, almost all of
        the gap is the oracle using the label on legitimate rows, and
        label-free combinations do worse than XGBoost. Nothing here
        supports a router
- [x] **H+C**: Hardware block B5 (QSVM sign-augmented, 12 fits, about 15 s).
      **Ran 2026-10-06**: 12 fits, 13 s (`docs/B4_B5_HARDWARE_RESULT.md`).
      Not one of the six; it runs first inside F90 because it is cheap and
      exercises the approval and ledger path

## Resourcing, per proposal section 3

- [ ] **H**: Confirm what compute the PoC sprint provides. T&C s1 promises
      "access to compute resources, tooling, and expert support" to finalists
      and s9 disclaims all warranties over it
- [x] **H**: Dirac-3 allocation for Phase 2. **The current balance is in
      `experiments/results/allocation_reads.json`** (Sprint 24 IMP-1; no
      document restates it). History: of the 3,000 granted, 1,039 were
      drawn in the Phase 1 campaign and 280 by the 2026-09-23 integer
      probes (`HARDWARE_PLAN_PHASE_2.md` owns that table). The device read
      1,675 s on 2026-10-05 before any Sprint 21 call -- 6 s below 1,681,
      not yet explained -- and fell to 1,022 s after B5 and B4 (653 s).
- [x] **H**: The additional 7,500 s asked of QCi in the hardware plan.
      **Granted 2026-10-09** (`docs/QPU_RECONCILIATION.md`, grants).
      Experiment 3, sized at 3,070 s, is no longer blocked by the
      allocation. F138 and F139 reported 2026-10-13: any Dirac-3S run
      first needs F141 (client support) and F142's measured cost.
      **Both done in Sprint 26** (2026-10-15): F142 spent 86.0 s over 5
      Dirac-3S fits
      (`docs/phase2/F139_RERUN_REVIEW.md`). Sprint 31 (F155, F95): 73.0 s
      over 5 Dirac-3S calls, none retried. F155 accepted 1,350 variables;
      F95 found no evidence for schedule 4, so device plans stay at
      schedule 2 (`docs/phase2/F95_SCHEDULE4.md`)
- [ ] **H+C**: Latency benchmark (p50/p95/p99) against the 100-300 ms envelope,
      which Phase 1 states as a target rather than a measurement (D10). F118
- [ ] **H+C**: Calibration layer fitted, which Phase 1 specifies but does not
      fit (D1). F119

## Deliverable

- [ ] **C**: Preregister the Phase 2 protocol BEFORE any result is seen, as
      Phase 1 did (F102). It is the thing this project does best and the reason
      the null is credible

## Completed before selection (record; detail in the sprint summaries)

Carried from `CHECKLIST-Phase2-pre.md` when it was merged, 2026-10-03.

- [x] README rebuilt for a public reader, and its reproduce steps executed
      against a fresh clone (Sprint 14)
- [x] CHANGELOG backfilled and wired into the delivery cycle (Sprint 14)
- [x] F67 -- the pool-mechanism guard runs on a fresh clone (Sprint 14)
- [x] F39 ADR-0014 and F72 ADR-0015 accepted (Sprint 14). F77 moved to
      `github.com/kimmeyh/EvidenceBasedDB` 2026-09-16 and is tracked there
- [x] F73 -- the submission explained at an 8th-grade level (Sprint 15)
- [x] F64 -- the k=17 order-2 cell, completed by F91's fourth corner
      (Sprint 18)
- [x] F87 -- the Dirac-3 integer path built and sized, five measured points
      (Sprint 18)
- [x] F92 -- the QCi package sent 2026-09-25 (Sprint 19)
- [x] The optional free-platform gate-based groundwork item is now F6
