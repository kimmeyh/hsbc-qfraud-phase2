# Sprint 25 Manual Validation

**Sprint**: 25, Learn the New Device, Then Build What Runs on Any Device
**Branch**: `feature/20261010_Sprint_25` | **PR**: #12 (draft)
**Scope**: F138 (A), F139 (B), F102 (C), F113 (D), F29 (E), F94 (F); Task G
(F146, F147) added at Manual Validation.
Issues #13-19.
**Metered Dirac-3 seconds spent: 0.**

This file is the durable copy. The same items are listed to the screen at
handover: a pointer to a file is not a handover.

---

## V1. Task A (F138): what Dirac-3S changes

Read `docs/phase2/DIRAC_3S_RESEARCH.md` (sources traceable in
`docs/phase2/DIRAC_3S_SITE_SWEEP.md`, 71 findings with URLs).

- **Dirac-3S is chosen by name and our code cannot reach it yet.** It needs
  `qci-client` 5.0.3 and `eqc-models` 0.22.1 and one solver argument
  (`sampler_type="dirac-3s"`). Every job so far used the `dirac-3` default.
- **"Nearly 10,000 variables" is the expansion configuration.** The base
  module has Dirac-3's 949. Which one the cloud serves is not stated.
- **Higher orders (3rd-5th) are not new**; Dirac-3 had the same base limits.
- **QCi states the same about 200:1 resolution**, carried over from the
  Dirac-3 guide; Dirac-3S's effective figure is unmeasured.
- **No source compares Dirac-3S with Dirac-3**, and QCi's own benchmark
  report contradicts itself. Cost at our sizes is unmeasured.
- **No Phase 1 preregistration amendment is needed**, if Dirac-3S results
  are Phase 2 rows naming the device.
- **Six questions for QCi** are listed at the end of the note (cloud
  configuration, whether `dirac-3` changed, billing, integer limits, queue
  access, effective resolution). Sending them is yours if you want them.

## V2. Task B (F139): which runs to repeat

Read `docs/phase2/F139_RERUN_REVIEW.md`. **Revised after the fresh-eyes
review**; its last section lists what changed.

- **Recommended: F142, three small verify runs, about 172 s at Dirac-3
  rates, cap 360 s.** B1 2 fits (first cost and queue point), B2 1 fit
  (cost at 833 variables, all samples stored), B4 oilgas 2 fits (the only
  meaningful fidelity twin: its Hamiltonians are resolvable).
- **No full re-run.** B2's gain is a pool effect, not a device effect: the
  classical `deep` proxy reaches 0.7926 against B2's 0.7928. F144 (B2's own
  proxy twin, zero metered) comes before any B2 comparison.
- **F129: recommend closing it.** B4's twin answers its question better.
  Closing it leaves F121's hold condition unmeetable. **Decided
  2026-10-13 (team lead): closed.** F121's new condition is due at the
  Sprint 26 refinement.
- **New cards**: F141 (client support, gates F142), F142, F143
  (telecom_churn with all 18 features, HOLD on QCi's answer), F144, F145
  (pool-build drift). Priorities 7, 8, 9 and 11 follow the 5 and 6 you kept
  for F138 and F139; F143 is HOLD.

## V3. Task D (F113): could a router beat XGBoost?

Read `docs/phase2/F113_ORACLE_GAP.md`. Source:
`experiments/phase2/results/f113_oracle_gap.json`.

- **The falsifier did not fire, but it could not have.** The oracle beats
  XGBoost by 5.0 points of recall at the 0.5% budget; two XGBoost
  configurations give 3.6.
- **Almost none of it is fraud CVQBoost catches**: the fraud half adds 0.1
  points, the legitimate half 4.4. The oracle uses the label to drop
  XGBoost's false positives.
- **Label-free combinations do worse than XGBoost alone** (83.7% and 85.3%
  against 85.6%).
- **Nothing here supports a router.** This bears on F121.

## V4. Task E (F29): sample size

Read `docs/phase2/F29_SAMPLE_SIZE.md`.

- **The optimum does not move, because it is uniform** to one part in a
  million at every sample size: the learners agree on almost every row
  (Sprint 4's finding at lambda = 0). F29 closes.
- **The pool build is not reproducible from its seed**: seed 42's AUPRC was
  0.8056, 0.8049 and 0.8043 on three runs. Carded as F145.

## V5. Task F (F94): Experiment 3's controls

Read `docs/phase2/F94_EXP3_CONTROLS.md`. Source:
`experiments/phase2/results/f94_controls.json`.

- **Built and correct**: enumeration, greedy, annealing and SCIP (certified
  and matching enumeration on all 6 small checks).
- **On the training fold, as every device run builds it, every selection
  ties.** The learners memorize the fold. Experiment 3 built that way could
  not tell a device from a greedy loop. **F25 must build its Hamiltonian on
  held-out predictions.**
- **The objective has a floor, `-1 + 2/m`** (found by the F94 fresh-eyes
  review). On the training fold every method reaches it; on the validation
  fold the best selection is within 0.0016-0.0026 of it. That is all any
  method, a device included, could still gain.
- **On the validation fold, greedy is the bar** (equivalent to annealing,
  in seconds). SCIP did not certify within 600 s; its reported 0.25 and
  0.11 gaps reflect its weak bounds, not room left.
- **The ridge carries the objective**: with `lambda = 2 * rows` the data
  term is at most 0.33% of it. **F25 must choose its ridge weight** so the
  fit to the labels matters, and build on held-out predictions.
- **Deviation**: the validation-fold instances were added during the run,
  after the first run showed the ties. Recorded in the note.

## V6. Task C (F102): the Phase 2 preregistration draft

Read `experiments/phase2/PREREGISTRATION_DRAFT.md`. A living draft, not
filed.

- Template, reporting standard, the two meanings of "order 3", device rules,
  the downsized matched-pair control, the status of every experiment, and
  the open items before filing.
- **Revised after review**: seed counts now follow from the test (an exact
  Wilcoxon cannot reach p < 0.05 on 5 seeds); a stated exception lets
  F142's cost runs proceed through a failed resolution screen.

## V7. What the code review found (10 findings, all fixed)

- **Ties at the alert cut** were broken by row order; the oracle's tied
  group held a fraud on two seeds. Now fractional credit. (medium)
- **F29's cosine** could not separate "unchanged" from "different near
  uniform". Centered measures added. (medium)
- **SCIP could pass its check uncertified.** Now requires status optimal.
  (medium)
- Seven low: SCIP's support read from its binaries; SCIP excluded from
  ranking if it fails a check; a fixed baseline for the oracle gap; the
  family list derived and checked; a small pool refused; tests that could
  not catch a broken annealing or greedy, now proven red; the oracle's
  claim narrowed.

Every new guard was proven red with `assert_can_fail` before it was
trusted.

## V8. What the fresh-eyes reviews found

24 findings on Tasks A-E (9 high, 9 medium, 6 low), all addressed in
`73b6137`. The ones that changed a conclusion:

- F113: the falsifier could not fire, and the gap is label-driven (V3).
- F29: the cause was the learners' agreement, not the ridge (V4).
- F139: B2's rationale, B1's fidelity claim, B4's role and F143's size
  (V2).
- The draft: Wilcoxon seed counts; the screen would have blocked F142 (V6).
- F138: sources made traceable; resolution stated as QCi's figure.

A separate fresh-eyes review of F94 is recorded in the next section.

## V9. Fresh-eyes review of F94 (15 findings, all addressed)

2 high, 8 medium, 5 low. The high ones changed the reading, not the data:

- **SCIP's relative gap is not the open gap.** The true open gap, to the
  provable floor, is 40 to 115 times smaller. Rewritten.
- **The F25 advice missed the ridge.** The data term is at most 0.33% of
  the objective; the ridge weight is now the first F25 design decision
  (note and F25 card).
- Medium and low: the tie statement narrowed to "every method reaches the
  floor"; the `best_method` rounding explained; correlations converted to
  row fractions; SCIP's shortfall range corrected; "greedy is strongest"
  replaced by "greedy and annealing are equivalent"; the AUPRC spread
  stated per instance; resolution stated as a coefficient limit; the
  generator comment's counts identified as an uncommitted check. No number
  in the result file was wrong; no re-run was needed.

## V10. Task G (added at Manual Validation, #19): Dirac understandings and the evidence-library tool

Read `docs/phase2/DIRAC_UNDERSTANDINGS.md` (F146, permanent HOLD).

- **Understandings for both devices**, each item labeled Measured, QCi
  states, Independent, Inferred or Unverified, with EvidenceBasedDB record
  ids where the library holds the same item.
- **QCi's request of 2026-09-25 is a standing constraint**: our device
  interpretations are described as independent findings, not validated by
  QCi.
- **Nine suggested Dirac-3S improvements.** Two Phase 1 feedback items are
  still open in `eqc-models` 0.22.1, checked against the wheel: no named
  billed-seconds field, and `fork` still forced.
- **Questions**: two pending since 2026-09-25 (the Hamiltonian reading and
  the 200:1 reading, under QCi review) and twelve not yet sent (A1-A6 from
  F138, A7-A12 new). Nothing was sent.
- **F147** (next sprint, priority 10): a read-only query tool over the
  evidence library. **`docs/phase2/EDB_PROPOSALS.md`** holds three
  proposals for a session in EvidenceBasedDB: a stale allocation record,
  two records missing QCi's requested framing, six Sprint 25 findings with
  no record.
- **Guard false positive found**: `block_cross_repo_write.py` blocked a
  file in this repository because its name contained "EvidenceBasedDB".
  Recorded on F147.

## Acceptance criteria, walked

- **F138**: every question answered with a source or marked not stated;
  each Dirac-3 card re-checked (F95, F104, F25, F30, F129); the cards it
  changes listed. **Met.**
- **F139**: a table of every run with recommendation, reason and seconds;
  the total; new cards with F numbers; Phase 2 plan changes listed. **Met.**
- **F102**: template committed; the downsized-pair control and repeated
  draws written in with the arithmetic and the reason it is not a Phase 1
  amendment; the frozen preregistration untouched. **Met** (first draft).
- **F113**: matched operating point, rank correlation, oracle gap, the
  falsifier stated before the run. **Met.**
- **F29**: the 3 x 4 grid, cosine to the full-fold weights, the falsifier
  stated before the run; the card closes. **Met.**
- **F94**: each control returns a cardinality-feasible selection and
  objective at both sizes with seeds recorded; exact agrees with
  enumeration where both run; dated Phase 2 rows; no Phase 1 claim
  touched; `pyscipopt` declared and covered by the requirements guard.
  **Met**, with the source deviation in V5.

## Effort, measured

From `.claude/sprint_status.json` `task_actuals` (minutes): A 16, B 5,
C 5, D 5, E 12, F 129. Total 172 against 750 estimated. Background run
time overlapped the writing tasks, and the review fixes after Phase 5
began were not task-timed.
