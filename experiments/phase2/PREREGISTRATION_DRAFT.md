# Phase 2 Preregistration Framework: DRAFT

**Status: DRAFT. Not filed. Not binding.** First draft written 2026-10-13
(Sprint 25 Task C, card F102). This document is revised across later
sprints until Phase 2 is approved and a filing date is set (team lead,
2026-10-13). It binds only from its filing, and only for the experiments it
names at that date. Until then it may be changed freely, and each change is
recorded in the revision log at the bottom.

**Relationship to Phase 1.** `experiments/PREREGISTRATION.md` is FROZEN and
governs Phase 1 claims only. This draft does not amend it, and nothing here
changes a Phase 1 gate, cell or figure. Every Phase 2 result is a dated,
post-submission row (F138, question 6).

**Who reads this, and what they decide.** The team lead, and at filing the
Phase 2 reviewers: what each experiment will claim, how it will be tested,
and what result would count against it, all fixed before any Phase 2 result
is seen.

## 1. Per-experiment template

Every Phase 2 experiment gets one entry in section 6 with these fields,
complete before its first result is computed. An experiment with an empty
field does not run.

- **ID and card**: the experiment number and its backlog card.
- **Question**: one sentence.
- **Hypothesis and prediction**: the direction and size of the expected
  effect.
- **Falsifier**: the specific observation that would show the hypothesis is
  wrong (`docs/SPRINT_PLANNING.md`, premise falsifiers).
- **Data and splits**: dataset, protocol (stratified or temporal), fold
  layout, seeds.
- **Arms**: every model or solver compared, each with its configuration.
- **Primary metric and test**: from section 2.
- **Multiplicity**: the family of tests it belongs to and the correction.
- **Device**: none, Dirac-3 or Dirac-3S (section 4), with the
  configuration, call count and seconds cap.
- **Stopping rules**: when a run stops early, and what is reported if it
  does.
- **What is reported whatever the result**: nulls and failures included.

## 2. Reporting standard (every Phase 2 result)

- **Validation**: nested cross-validation where tuning and evaluation share
  data, so no reported score comes from the folds that chose its
  configuration.
- **Paired comparisons**: Wilcoxon signed-rank across seeds or folds, with
  the paired difference and its bootstrap interval reported beside the
  p-value.
- **Multiplicity**: Bonferroni within each experiment's stated family.
- **Seeds set from the test, not by habit.** An exact two-sided Wilcoxon
  test on k paired seeds cannot give a p-value below 2 / 2^k: 0.0625 at 5
  seeds, 0.031 at 6, 0.0156 at 7. So a Wilcoxon comparison needs at least 6
  seeds at alpha 0.05, and at least 7 under Bonferroni with 3 tests. Where
  only 5 seeds are affordable (the SPECTRA cells), the primary test is a
  paired bootstrap over transactions within seeds, and the Wilcoxon result
  is reported as secondary. Each section 6 entry states its seed count and
  shows it can reach its alpha.
- **Seed sensitivity**: every headline figure reported over at least 5 seeds
  as mean and spread, never a single run.
- **Metrics**: AUPRC normalized by its floor, `(AUPRC - p) / (1 - p)`, where
  `p` is the test prevalence (the AUPRC of a random ranking), with raw
  AUPRC and AUROC beside it. Recall at the 0.5% alert budget wherever an
  operating point is claimed.
- **Outcomes recorded** (team lead, 2026-10-22; F154): every Phase 2
  result that holds a test score, ML or QML, also records the confusion
  counts (TN, FP, FN, TP) at the 0.5% alert budget, at the
  validation-chosen operating points where a validation fold exists, and
  at the experiment's own threshold where it has one; and saves its
  per-row test scores with their SHA-256, so any two models can be
  compared case by case. `experiments/phase2/src/outcome_record.py`
  builds the block; `experiments/src/test_outcome_record_required.py`
  fails a new result file without one.
- **Train-test gap** beside every win (Sprint 21: SPECTRA's wins came with
  large gaps).
- **Every bottom-line claim carries a label** (Sprint 25 IMP-1), the same
  labels `docs/phase2/DIRAC_UNDERSTANDINGS.md` uses: **Measured** (cites the
  result file and the field), **Inferred** (says what it rests on), or
  **Unverified** (says what would settle it). **An inferred mechanism names
  the leading alternative it did not rule out**, and the evidence already on
  record about that alternative. Applies to every Phase 2 write-up from its
  first commit, not only to this document's experiments. (Sprint 25's
  example here, F29's "pinned by the ridge", was itself corrected the wrong
  way: the "uniform at lambda = 0" finding it relied on had been withdrawn
  by amendment A27, and the ridge is what selects the near-uniform answer.
  Corrected 2026-10-14. The rule stands, and the example shows a second
  lesson: check a cited finding against the amendment log before relying
  on it.)
- **Source for the statistical standard**: arXiv:2604.18837 (Kakavand,
  Strohmeyer and Schlotter, "Benchmarking Quantum Kernel Support Vector
  Machines Against Classical Baselines on Tabular Data", v1, 2026-04-20),
  re-read against its text 2026-10-18 (Sprint 27 Task C). What this
  section takes from it, and what it adds:
  - **From the paper**: stratified nested cross-validation (5 outer, 3 or
    5 inner folds); the two-sided Wilcoxon signed-rank test on paired
    folds, and on paired seeds in its seed study (16 seeds); Bonferroni,
    which it applies once, across its seven per-dataset seed comparisons;
    the floor "p = 0.0625" for an exact Wilcoxon test on 5 pairs, which it
    states itself; and its recommendations to "report confidence
    intervals, not just point estimates" and to claim an advantage only if
    it is significant, substantial, "consistent across seeds" and
    "observed on multiple datasets".
  - **Added here, not from the paper**: the bootstrap interval (the paper
    reports none, and names bootstrap resampling "the ideal approach" in
    its limitations); Bonferroni for every family (section 2a); the
    floor-normalized AUPRC (its primary metric is balanced accuracy); and
    the equivalence margin (section 2b). Its "substantial (>5 pp)" is a
    balanced-accuracy threshold and is not carried over to AUPRC.

## 2a. Multiplicity families

- **One family per experiment.** Each section 6 entry lists its
  **primary** tests; they form its family, corrected by Bonferroni at
  alpha 0.05 / m for m primary tests. Every other test in the entry is
  **secondary**: reported, labeled secondary, uncorrected, and never the
  basis of a headline claim.
- **No family spans experiments.** A claim that needs two experiments
  (for example a device effect that needs a twin to match and a device to
  differ) states its combination rule in the entry that makes the claim.
- **Seed count against the family.** An exact two-sided Wilcoxon test on k
  pairs reaches at best 2 / 2^k, so a family of m primary Wilcoxon tests
  needs 2 / 2^k <= 0.05 / m: k = 6 for m = 1, k = 7 for m = 2 or 3, k = 8
  for m = 4 to 6. Below that seed count the primary test is the paired
  bootstrap over transactions within seeds (section 2), and the Wilcoxon
  result is secondary.

## 2b. Equivalence margins

- **A "no difference" hypothesis is tested against a margin, not by a
  failure to reject.** An entry whose hypothesis is that two arms agree
  (a drift reference, a twin, a null main effect) states a margin delta
  before its run. It claims equivalence only if the 95% interval on the
  paired difference lies inside [-delta, +delta]. An interval that spans
  zero but leaves the margin is reported as **inconclusive**, not as
  agreement (F144's lesson: its drift reference's mean is zero by
  construction, so a test of bias could not measure the drift's size).
- **The default AUPRC margin is 0.005**, the smallest change the Sprint 27
  plan counts as moving AUPRC (set 2026-10-18, before F130's runs). An
  entry may set another margin, with its reason, before its run.

## 3. Two meanings of "order 3"

They are different things, and every document states which it means:

- **Pool order**: weak learners built over feature triples (weak-classifier
  schedule 3). This happens classically, before the device sees anything.
- **Objective order**: the degree of the polynomial the device minimizes.
  CVQBoost's objective is quadratic by construction, whatever the pool
  order. Dirac-3 and Dirac-3S both accept degrees up to 5 (F138), but no
  experiment in this draft uses a degree above 2.

## 4. Device rules

- **The default device is Dirac-3S** (team lead, Sprint 26 Decision 11,
  2026-10-16, after F142). An entry that uses Dirac-3 says why, for
  example a Dirac-3 against Dirac-3S comparison. In code, Phase 2 runners
  pass `eqc_submit.PHASE2_DEVICE`, or name the device on a line marked
  with the reason (`test_phase2_device_default.py`).
- **Every hardware row names its device** (`dirac-3` or `dirac-3s`) and
  carries its `job_id` and every returned sample (F133; F141 adds the
  device field).
- **A Dirac-3 against Dirac-3S comparison is a Phase 2 result** with its
  own entry in section 6. It is never reported as a new cell of a Phase 1
  gate; under the frozen preregistration's section 11 that would be a
  deviation (F138, question 6).
- **The resolution screen gates every metered block** (F104): before any
  call, the job's coefficient DIFFERENCES are tested against the device's
  stated 200:1 (23 dB) resolution, as A31 tested them: each spread must
  reach the largest coefficient divided by 200. A max-over-min ratio in dB
  is not this test; a CVQBoost Hamiltonian can sit far under 23 dB and
  still be unresolvable (F142's dry run, 2026-10-14). QCi states the same figure for both devices;
  Dirac-3S's effective resolution is unmeasured (F138). A job that fails
  the screen does not run **as an accuracy experiment**.
- **The one exception**: a run whose stated purpose is cost, queue time or
  a twin of a Phase 1 Hamiltonian (F142's B1 and B2 fits) may run although
  it fails the screen. Its entry says so before it runs, its result is
  reported as cost or fidelity evidence only, and the failed screen is
  reported beside it.
- **Per-block approval** (Criterion H): call count and expected seconds
  stated first, the runner idempotent, retries per the frozen protocol.

## 5. The in-segment control: a downsized matched pair

Applies to every in-segment result (Experiment 5 and any SPECTRA cell).

- **The problem.** Phase 1's H5(ii) control draws a random segment of the
  same size and positive rate from the complement of the in-segment pocket.
  On energy_steel this is arithmetically impossible on all five seeds: the
  pocket holds 918-950 of the test fold's positives while the complement
  holds 832-864 (`docs/SPECTRA_CONTROL_FEASIBILITY.md`).
- **The design.** Downsize **both** sides to what the complement supports,
  keeping size and rate matched on each: positives per side are the
  smaller of the segment's and the complement's, and negatives per side
  keep the segment's own rate. On energy_steel seed 42 that is 855
  positives plus 278 negatives per side. Across the five seeds it keeps
  88-94% of the pocket's positives, and the AUC interval is 3-7% wider
  (4% on seed 42; the Hanley-McNeil leading term, an approximation).
  Feasible on all five seeds. telecom_churn and oilgas_gasturbine need no
  downsizing on any seed: their complements already hold more positives
  than their pockets. (Recomputed by code 2026-10-18, Sprint 27 Task C:
  `experiments/phase2/src/f102_downsized_pair.py`,
  `experiments/phase2/results/f102_downsized_pair.json`. The card's seed
  42 figures reproduce exactly; its "about 4% wider" holds for seed 42
  only.)
- **Repeated draws.** Both sides are then random draws, so the comparison
  is repeated, about 20 times, and reported as a mean with its spread. A
  single draw cannot separate a real in-segment effect from one that
  depends on which rows were drawn. Repeating costs nothing: it is
  classical computation over device output already paid for.
- **Why this is a Phase 2 design and not a Phase 1 amendment.** The frozen
  preregistration forbids an amendment that changes a gate's pass/fail
  criterion, and H5(ii)'s control is that criterion. Phase 1 reports
  energy_steel as `unscoreable`. The design follows from a structural
  property of the dataset: the positive counts in the complement. It was
  written after Phase 1 SPECTRA results on these cells had been seen
  (`docs/SPECTRA_CONTROL_FEASIBILITY.md`, `docs/B4_B5_HARDWARE_RESULT.md`),
  and no Phase 2 SPECTRA result exists yet.

## 6. Experiments

Entries are filled in as each experiment's card reaches readiness. Status
on 2026-10-23:

| # | Experiment | Card(s) | Device | Entry |
|---|---|---|---|---|
| 1 | Isolate the confound: the k=17 decomposition | F112 | none | Written 2026-10-18, below |
| 2 | Temporal validity on IEEE-CIS rolling-origin folds | F105, F152 | none | Written 2026-10-22, below |
| 3 | Cardinality-constrained selection on the integer solver | F94 (controls, built Sprint 25), F153, F25 | Dirac-3S, after F141 and F142 | Written 2026-10-22 (design), below |
| 4 | Replication under the source protocol (Loke et al.) | F111 | none | Written 2026-10-22, below |
| 5 | Segment transfer (H5), with the section 5 control | F121 | to be decided | To write; F121 is on HOLD |
| 6 | Scaling claim: training time against sample count | F110 | proxy first | Written 2026-10-22, below |
| - | Dirac-3S verify runs: B1 and B2 (cost), B4 (fidelity twin) | F142 | Dirac-3S | Written 2026-10-14, below |
| - | The proxy twin of B2's pool (k=17, order 3) | F144 | none | Written 2026-10-14, below |
| - | SPECTRA Tier 1 known-answer check (verification, not a claim) | F103 | none | Written 2026-10-18, below |
| - | Gate-based arm: dequantization check (F6 recommended pursue narrowly) | F106 | none (NumPy statevector) | Written 2026-10-18, below |
| - | Gate-based arm: the F106 circuit's shot budget | F107 | none (NumPy statevector) | Written 2026-10-18, below |
| - | Ceiling validation on a simulator with hidden state (verification) | F108 | none | Written 2026-10-18, below |
| - | Tier 1 across the six datasets on disk | F109 | none | Written 2026-10-18, below |
| - | Where each model wins, on the stored ULB predictions | F154 | none | Written 2026-10-22, below |
| - | In-pocket head-to-head on SPECTRA: CVQBoost proxy against HGB and XGBoost | F162 | none | Written 2026-10-23, below |
| - | Fraud types: per-type detectors against one model, on F108's simulator | F158 | none | Written 2026-10-26, below |
| - | Best achievable result per algorithm on ULB, classical and proxy lanes | F166 (F157 part 1) | none | Written 2026-10-27, below |
| - | Best achievable result per algorithm on IEEE-CIS, classical and proxy lanes | F174 (F157 part 2) | none | Written 2026-10-31, below |
| - | ULB frauds missed by every model: nearest neighbors | F170 | none | Written 2026-10-31, below |
| - | F158 step 3 on IEEE-CIS | F171 | none | Written 2026-10-31, below |

### Experiment 1 (F112): the k=17 decomposition, with paired intervals

Written 2026-10-18 (Sprint 27 Task C), before any interval below is
computed (Task D computes them).

- **What was already seen.** F64 and F91 (2026-09-22 and 23) reported the
  point estimates and seed-mean t-intervals this entry re-tests: the k
  effect +0.0001 [-0.0024, +0.0026] and the order effect +0.0245
  [+0.0187, +0.0302] (`docs/F64_LADDER_DECOMPOSITION.md`). So this is a
  re-analysis with a known direction. What it adds is the interval method
  section 2 requires, and an equivalence test the t-interval did not make.
  Its result is evidence of precision, not of a new prediction.
- **ID and card**: Experiment 1, F112.
- **Question**: on the ULB proxy, does subset order (2 to 3) carry the
  k=17 configuration's AUPRC gain, while feature count (13 to 17) adds
  nothing measurable?
- **Hypothesis and prediction**: (P1) the order effect at k=13 is
  positive, about +0.025 AUPRC. (P2) the k effect at order 2 is equivalent
  to zero within the default margin, 0.005 (section 2b).
- **Falsifier**: P1 fails if its interval reaches zero or the Wilcoxon
  test does not reject. P2 fails if its interval leaves [-0.005, +0.005]
  on either side; an interval that spans zero but leaves the margin is
  reported inconclusive, not as support.
- **Data and splits**: ULB, stratified protocol, seeds 42-51 (10 paired
  seeds), the stored Phase 1 proxy predictions in
  `experiments/results/predictions/`: `free` (k=13, order 2, 91 variables,
  config hash `640ed4cf9c46ea4b`), `mid` (k=17, order 2, 153,
  `1e6bf03caab3676b`) and `deep` (k=13, order 3, 377, `47012b1404d5d4de`),
  all `cvqboost_proxy`, full-pair builds. Read only; no pool is rebuilt and
  no Phase 1 row is written.
- **Arms**: the three corners above. Order effect = `deep` minus `free`;
  k effect = `mid` minus `free`; same test rows, same seed.
- **Primary metric and test**: test AUPRC. P1: the exact two-sided
  Wilcoxon signed-rank test on the 10 per-seed deltas, and the paired
  bootstrap interval on the across-seed mean delta (each replicate
  resamples every seed's test rows, stratified by label, with the same
  indices for both arms; 2,000 replicates; percentile). P2: the same
  interval against the margin.
- **Multiplicity**: one family, m = 2 (P1 and P2), Bonferroni: each at
  alpha 0.025, so the intervals are 97.5%. Ten seeds reach that alpha (the
  exact Wilcoxon floor at 10 pairs is 2 / 1,024, about 0.002; section 2a
  asks for 7).
- **Secondary, uncorrected**: each seed's paired BCa interval
  (`metrics.paired_delta_ci`); the same deltas in floor-normalized AUPRC
  and in AUROC; the train-test gap where the rows carry it. The
  interaction against the fourth corner uses F144's twin (k=17, order 3,
  833 variables): it is seed-level only (F144 stored AUPRC, not
  predictions) and its pools were seeded while the three corners' were
  not (section 7, F145), so it is labeled Inferred, with that drift as the
  named alternative.
- **Device**: none.
- **Stopping rules**: none needed; all inputs exist. If a prediction file
  is missing or its labels differ between arms on a seed, that seed is
  reported and excluded, and the family's seed count is re-checked
  against section 2a before any claim.
- **What is reported whatever the result**: both primary intervals and
  the Wilcoxon p-value, the per-seed table, and the `Proxy cell used:`
  line of `score_gates.py` before and after (F112's card; this experiment
  writes no Phase 1 row, so it must not change).
- **Result, added 2026-10-18 after the run (Sprint 27 Task D;
  `experiments/phase2/results/f112_intervals.json`, `f112_intervals.py`).**
  All 10 seeds present, labels identical across arms on every seed.
  - **P1 holds.** Order effect +0.0245 AUPRC, 97.5% interval [+0.0184,
    +0.0304]; exact Wilcoxon p = 0.00195 (the floor), 10 of 10 seeds
    positive. Floor-normalized AUPRC gives the same, AUROC +0.0145.
  - **P2 holds.** k effect +0.0001 AUPRC, 97.5% interval [-0.0034,
    +0.0037], inside [-0.005, +0.005]: equivalent to zero at the margin.
  - **Secondary (Inferred).** Interaction against F144's twin, mean
    -0.0001, seed SD 0.0043.
  - **`Proxy cell used:`** reads `cvqboost_proxy/deep/dct/full` in
    `experiments/results/gate_report.md` line 48, unchanged, and
    `experiments/results/` has no change in git. It was read, not
    regenerated: `score_gates.py` rewrites the report on any invocation.
  - Consistent with the point estimates already seen; this is a
    re-analysis, as stated above, and its evidence is precision.

### Experiment 2 (F152): temporal validity on IEEE-CIS rolling-origin folds

Written 2026-10-22 (Sprint 28 Task B, #49), before any Phase 2 score on
IEEE-CIS. Not filed; part of this draft.

- **What was already seen.** Phase 1 scored XGBoost, LightGBM and CatBoost
  on the same three folds with one seed (`experiments/results/
  ieee_classical.json`). So the direction of the lane ordering is known in
  part. What this entry adds is section 2's standard: five seeds,
  floor-normalized AUPRC, paired intervals, a written drift treatment, and
  two lanes Phase 1 did not run on IEEE-CIS (HGB, logistic regression).
- **ID and card**: Experiment 2, F152 (harness F105).
- **Question**: does the ULB ordering of model families hold when every
  model is trained on earlier months and scored on a later one, and how
  much does a strong lane lose from one month to the next?
- **Hypotheses and predictions**: (P1) XGBoost beats logistic regression
  on floor-normalized AUPRC on each full evaluation month (4 and 5), as on
  ULB. (P2) none directional: XGBoost's floor-normalized AUPRC changes
  from month 4 to month 5; the size and its interval are the result.
- **Falsifier**: P1 is false if, on either full month, the interval on
  XGBoost minus logistic regression reaches zero. P2 reports a change only
  if its interval excludes zero.
- **Data and splits**: IEEE-CIS train, exact duplicates removed
  (`ieee_loader.dedupe_ieee`), the harness's three rolling-origin folds
  (evaluation months 4, 5, 6; each trained on every earlier month), with
  the leakage assertion run on every build. Features from
  `ieee_harness.build_fold`, unchanged.
- **Month 6**: a partial bucket, 8,111 rows, about a tenth of a full fold.
  It is scored and reported, labeled secondary, and is not in P1 or P2.
- **Drift treatment: a stated limit.** The adversarial control runs as in
  Phase 1 (`ieee_controls.apply_item4_controls`, its round cap of 20,
  controls seed 42 for every model seed, so all lanes and seeds see the
  same features per fold). It stops at the cap with early-versus-late AUC
  far above target (F105). No higher cap and no group drop: either would
  change the estimator from Phase 1's and remove features chosen for
  drift, not for leakage. The per-fold early-versus-late AUC is reported
  beside every score, and every claim from this entry carries the limit
  "trained on drifting features".
- **Lanes** (all on the same features per fold):
  1. XGBoost, Phase 1's IEEE-CIS configuration (`run_ieee.ARMS`, with its
     per-fold `scale_pos_weight`).
  2. LightGBM, the same.
  3. HGB with F151's stable setting (`l2_regularization=1.0`, other
     settings default), no class weight.
  4. Logistic regression: median imputation fitted on training rows,
     standard scaling, `class_weight="balanced"`, `max_iter=2000`.
  GAM, GA2M and the JOINT twin stay on the card (unsized on 180-plus
  features). No CVQBoost proxy lane (Decision 2).
- **Seeds**: 42-46 (model seeds; the folds are fixed). Before the full
  run, one lane on two seeds: the paired interval between the two seeds
  must include zero, or the interval method is too narrow for seed noise.
- **Primary metric**: floor-normalized AUPRC, `(AUPRC - p) / (1 - p)`,
  with `p` the evaluation month's prevalence; raw AUPRC and AUROC beside
  it.
- **Test**: the paired stratified bootstrap over evaluation transactions
  (section 2): each of 1,000 replicates resamples the month's rows by
  label, with the same indices for both lanes and all five seeds, and
  computes the across-seed mean difference; percentile interval. For P2
  the two months are independent samples, each resampled on its own.
- **Multiplicity**: one family. P1 is two intervals that must both exclude
  zero (an intersection-union test, which needs no correction across its
  two parts) and P2 is one; m = 2, Bonferroni, so 97.5% intervals. Three
  folds cannot support a Wilcoxon test (its floor is 0.25), so the
  bootstrap is primary (section 2a).
- **Secondary, uncorrected**: every other lane pair per month; month 6;
  the per-seed spread; the shuffled-label control is not re-run (Phase 1
  ran it on these folds).
- **Recording**: every lane, month and seed carries an outcome block
  (section 2, "Outcomes recorded").
- **Limits stated now**: the drift limit above; one dataset; three folds
  from one six-month file.

### Experiment 3 (F153, F25): cardinality-constrained selection, proxy design first

Written 2026-10-22 (Sprint 28 Task C, #50), before any Hamiltonian below
is built. Not filed; part of this draft. This sprint runs the proxy
design only; the device arm is F25 and needs its own per-block approval.

- **What was already seen.** F94 (`docs/phase2/F94_EXP3_CONTROLS.md`):
  on the training fold every method reaches the objective floor; on the
  validation fold the best found is within 0.0016-0.0026 of it, and the
  ridge term carries over 99.67% of the objective at `lambda = 2` (in
  `exp3_controls.problem`'s scaled units). So a device could gain almost
  nothing on F94's Hamiltonian. This entry changes the ridge before any
  device time is asked for.
- **ID and card**: Experiment 3, F153 (design), F25 (device run).
- **Question**: is there a ridge weight at which the selection problem
  leaves room between greedy and the floor, and that the device can
  resolve? Only then is a device comparison worth its seconds.
- **Hypothesis and prediction**: none directional for the design. For the
  later device arm (F25): the device's objective beats greedy's, or
  matches it faster, on the chosen Hamiltonian.
- **Falsifier (design)**: the design fails, and no device quote is
  carried forward as ready, if at the chosen ridge weight the gap between
  greedy and the floor is below 0.01 on every instance, or the chosen
  Hamiltonian fails both resolution checks below.
- **Instances**: F94's, unchanged: ULB, seeds 42-44, sequential `dct`
  pools; the first 60 `free` learners choose 10, and the 136 `mid`
  learners choose 25. Built on the **validation fold** (held-out
  predictions); the test fold is never optimized on.
- **Objective**: `exp3_controls.problem(H, y, lam_mult)`, weights on the
  simplex. Its floor is `-1 + lam_mult / m` (the data term is never
  negative, and `||w||^2 >= 1/m` with m learners).
- **Ridge sweep, fixed now**: `lam_mult` in {2, 0.2, 0.02, 0.002}. Greedy
  on every instance at every value. **The chosen value** is the largest
  whose greedy solution has a data term of at least 10% of the
  objective's absolute value on all six instances; if none qualifies,
  the smallest, labeled as such.
- **Controls at the chosen value**: greedy, simulated annealing (F94's
  3,000 iterations) and SCIP (300 s cap, a change from F94's 600 s to fit
  the sprint; the cap is reported beside every SCIP figure). The first
  instance is checked for a gap between greedy and the floor before any
  method is compared.
- **Reported per instance**: each method's objective, the floor, the gap
  from the best found to the floor, the data-term share, and test AUPRC
  for context only (three seeds, no interval).
- **Resolution, both checks (Decision 1)**: F104's gate
  (`device_resolution.resolution_gate`, unchanged) and the guide's
  section 5.3 check (`device_resolution.resolution_check_guide`, new and
  opt-in): the max/min ratio of the nonzero coefficients against 200, and
  the share of coefficient pairs whose difference reaches max / 200
  (eq. 5). Both are reported; the gate's verdict is not replaced.
- **Device quote, not a run**: F139's two integer probes priced for
  Dirac-3S as a bracket, labeled inferred, for a separate approval.
- **Multiplicity**: the design makes no claim tested at alpha; the device
  arm's family is set in F25's amendment to this entry before its run.
- **Recording**: test AUPRC rows carry outcome blocks (section 2,
  "Outcomes recorded").
- **Amendment, 2026-10-26 (Sprint 29 Task E, F160, #68), written before
  its module exists or any IEEE-CIS pool is built.** The design failed on
  ULB (`docs/phase2/F153_EXP3_DESIGN.md`). This amendment asks whether
  the room the falsifier requires exists on a second dataset. The rule,
  sweep, ridge choice, floor, resolution checks and controls above are
  unchanged.
  - **Why another dataset, stated before any run (inferred).** The data
    term is `||H'w - y||^2 / n`. Learners that predict "legitimate" on
    every row reach `4 x fraud rate`. On ULB (fraud rate about 0.17%)
    that is about 0.007, below the 0.01 the falsifier requires, which
    fits F153's largest recorded gap (0.0026). On IEEE-CIS (about 3.5%)
    it is about 0.14, so the rule can pass there in principle.
  - **Positive control, first.** At both instance sizes and on each
    IEEE-CIS instance's own labels, H from learners with random signs
    (seeded), so no subset fits the labels. The greedy gap should be far
    above 0.01. If the control shows no room on every instance, the rule
    cannot pass, and no IEEE-CIS reading is made.
  - **Data**: IEEE-CIS train, deduplicated (`ieee_loader.dedupe_ieee`);
    the first rolling-origin fold of `ieee_harness.folds_for`; its
    features from `ieee_harness.build_fold` (fit on the training months
    only), numeric, missing values filled with the training medians.
  - **Features**: the top k by mutual information (`data.top_k_features`)
    on a stratified 50,000-row subsample of the fold's training rows,
    drawn with the seed; k = 13 (`free`) and 17 (`mid`), as F94's configs.
  - **Pools**: `qubo_proxy.build_pool`, sequential, `dct`, with
    `seeded_weak_params(seed)`, on all the fold's training rows. The
    instances are F94's sizes (the first 60 `free` learners choose 10;
    the first 136 `mid` learners choose 25); a smaller pool is refused
    and recorded. H on the evaluation month's rows (held out), with their
    labels in {-1, +1}. Seeds 42-44.
  - **Methods at the chosen weight**: greedy and SCIP (300 s cap), the
    floor, and both resolution checks. Annealing is dropped to fit the
    sprint; the falsifier reads greedy alone.
  - **Consequence, set here**: if the design does not fail on IEEE-CIS
    (greedy's gap at least 0.01 on some instance, and a chosen
    Hamiltonian passing a resolution check), F25's design reopens on
    IEEE-CIS as a new card, not in this sprint. If it fails, Experiment
    3's proxy design has no room on either dataset, recorded on F25.
  - **Reported whatever the result**: per instance, the fraud rate, the
    ridge sweep, the chosen weight, each method's objective, the floor,
    both gaps, the data share, both resolution checks, and run times.
    No test score is computed, so no outcome block is needed.
- **Amendment, 2026-10-31 (Sprint 30 Task E, F176, #79), written before
  its module exists or any solver runs.** F160 measured the room only to
  the floor, a bound: greedy ended about 0.097 above it on all six
  IEEE-CIS instances, and SCIP stopped at its 300 s cap without beating
  greedy. This asks whether any classical method finds a selection below
  greedy on the same six instances.
  - **Instances**: F160's, rebuilt from its seeded pools with its code
    (`f160_room_ieee.ieee_fold`, `ieee_instances`), because F160 stored
    rows, not Hamiltonians. At F160's chosen weight (lambda 2.0). Before
    any solver runs, each rebuilt greedy objective must match F160's
    recorded one within 1e-9, or the run stops.
  - **Check first, that "below greedy" can fire**: instances of 20
    learners choosing 4 (F94's exact-check size), solved exactly by
    enumeration: the first 20 learners of each of the six instances, and
    20 seeded random-sign instances. On a case where greedy is above the
    exact optimum, the swap search must reach it. If no case has greedy
    above the optimum, the reading is stated as unable to fire.
  - **Methods per instance**: greedy; a best-improvement swap search from
    greedy's support (every swap of one chosen learner for one unchosen,
    until no swap improves by more than 1e-6, at most 100 passes);
    simulated annealing from greedy's support (`exp3_controls`, 3,000
    iterations, seeds 42-44); SCIP with a 1,200 s cap (4 x F160's), with
    its dual bound.
  - **Reading**: "below greedy" when the best objective found is more
    than 1e-6 below greedy's. Below greedy on some instance shows the
    room can be reached, and the device question becomes whether
    Dirac-3S reaches it faster or further. None below greedy within the
    caps leaves the room unshown, and is reported as that. SCIP's dual
    bound, where above the floor, bounds the room more tightly than the
    floor; the room bound is greedy minus the larger of the two.
  - **Reported whatever the result**: per instance, each method's
    objective, support and time, the best found, its gap to greedy and
    to the floor, SCIP's status and dual bound; and the check's cases.
    No test score is computed, so no outcome block is needed.

### Experiment 4 (F111): the CVQBoost-KNN lane under the source protocol and ours

Written 2026-10-22 (Sprint 28 Task D, #51), before the harness exists or
any lane below is fit. Not filed; part of this draft. No device.

- **What was already seen.** Loke et al. (ICAART 2026, DOI
  10.5220/0014628400004052) report CVQBoost-KNN at AUC-PR **0.8108**,
  mean of 10 runs, on ULB (Tables 3 and 4). Under our protocol, lanes that
  are not their method already sit within 0.03 of it: the CVQBoost proxy
  dct cell (0.793) and XGBoost (0.802, 0.830). F130's KNN proxy (k = 5,
  13 features, 78 sequential learners, our split) reached 0.7772. So a
  value near 0.81 cannot show that the protocol matters; the paired
  difference below is the result.
- **Sources for the source protocol.** The paper (section 2, Tables 1-2)
  and the first author's repository, read only: commit `0092a38`
  (2026-05-22), the version nearest the paper; upstream `main` and the
  October branch read through the GitHub API. The code postdates the
  paper and compares XGBoost with hybrid XGBoost, so it shows the
  author's practice, not proof of the paper's settings.
- **ID and card**: Experiment 4, F111.
- **Question**: on the same lane, how much does the source protocol
  change test AUC-PR against our protocol? Is the lane, under the source
  protocol, consistent with 0.8108?
- **The lane, identical under both protocols**:
  - All 30 ULB columns (Time, V1-V28, Amount). The paper names no
    feature selection, and the code drops only the label. The 13
    mutual-information features of our `free` cell are a lane choice,
    not a protocol choice, and are not used here.
  - `MinMaxScaler` fit on the training rows only (paper: "scaled to
    [0, 1]"; code: fit on train). KNN is scale-sensitive, so the scaler
    is part of the lane on both sides.
  - KNN weak learners, `n_neighbors=15`, other settings scikit-learn's
    defaults (uniform weights, Minkowski p = 2, leaf size 30: Table 1).
  - Weak-classifier schedule 2, full-pair: 30 singles and 435 pairs, 465
    learners. The code's `weak_cls_strategy="multi_processing"` is the
    full-pair builder; it needs `fork`, so the pool is built by
    `experiments/phase2/src/full_pair_pool.py` (same learners, same
    order; checked equal to the library's under `fork`, 2026-10-22).
  - lambda = 0 (paper and code), solved classically on the simplex by
    `qubo_proxy.solve_simplex_qp`, the Hamiltonian eqc-models sends (QCi
    confirmed it on 2026-10-21). Score: w . H, the code's `predict_raw`.
- **Protocol A, the source's**: `load_ulb()`, `dropna()` (ULB has no
  missing values, so it removes nothing), **no deduplication**.
  `train_test_split(test_size=0.3, stratify=y, random_state=seed)`. The
  test fold split again, `test_size=0.67`, stratified, `random_state=seed`:
  33% validation, 67% evaluation (the code's choice; the paper says only
  "randomly split"). SMOTETomek on the training rows only, after scaling:
  `sampling_strategy` 0.02 (the minority-to-majority ratio after
  resampling; the code's May value), SMOTE `k_neighbors =
  max(1, min(10, positives - 1))`, `random_state=seed`. AUC-PR on the
  evaluation part.
- **Protocol B, ours**: deduplicated, `data.stratified_split(df, seed)`
  (60/20/20 stratified), no resampling. AUC-PR on the test fold; the
  validation fold sets the threshold.
- **Seeds**: 42-51. The paper's seeds are unrecoverable: the code draws
  each run's seed with `random.randint(0, 100000)` and logs it.
- **Reference lane**: F151's stable HGB (`l2_regularization=1.0`,
  `random_state=seed`), on the same scaled features and the same training
  rows (resampled under A) as the KNN lane, under both protocols.
- **Primary result**: per seed, KNN lane AUC-PR under A minus under B;
  the mean over 10 seeds with its 95% t interval (9 degrees of freedom).
  One interval, so no multiplicity family. **Secondary, reported**: the
  same difference for the HGB lane; within each protocol, KNN minus HGB
  with its interval.
- **Consistency with 0.8108**: "consistent" if the KNN lane's mean under
  A is within 0.03 of 0.8108. The tolerance cannot separate lanes
  (above), so the result is never stated as "reproduces".
- **Sensitivity, reported, not decisive**: SMOTETomek ratio 0.05 (the
  October value) under A, seeds 42-44, KNN and HGB.
- **Named in advance**: without deduplication, an evaluation row can have
  an exact copy in the training rows, and a 15-neighbor learner on a pair
  of columns will find it. Reported per seed under A: the count of
  evaluation rows with an exact duplicate (all 30 columns and the label)
  among the training rows.
- **Size rule**: a pilot at seed 42 on a stratified 10% sample of the
  training and scored rows, both protocols, KNN lane. Projection: pilot
  seconds x (full training rows / pilot training rows) x (full query rows
  / pilot query rows), F130's formula. If the 10-seed A and B runs plus
  the sensitivity rows project at **120 minutes or less**, they run.
  Otherwise the pilot and its projection are recorded and the seed count
  goes to the team lead at Manual Validation; no silent cut. The full run
  starts only after Experiment 6's timing has finished, so the two do not
  share the processor.
- **Seed count decided, 2026-10-23, after the pilot and before any
  full-size row.** The pilot projected 824.6 minutes. The team lead
  approved the run as written (10 seeds on A and B, plus the sensitivity
  rows) above the cap (Sprint 28 Manual Validation, DV2). No other part of
  the entry changes. The approval is recorded in the result file's pilot
  block (`over_cap_approval`), and `run` reads it there.
- **Comparator**: CAD (0.7423, Gao et al. 2025) is cited, not run; it was
  not run on their split either.
- **Recording**: every row carries an outcome block (section 2,
  "Outcomes recorded"), with the validation part as `y_val`, `p_val`.
- **Reported whatever the result**: per seed and protocol, both lanes'
  AUC-PR and ROC-AUC, the resampled class counts, the duplicate count,
  the pilot timing and projection, and the primary interval.

### Experiment 6 (F110): training time against sample count, proxy first

Written 2026-10-22 (Sprint 28 Task E, #52), before any timing below.
Not filed; part of this draft. The device arm needs its own per-block
approval and is not part of this sprint.

- **What was already seen.** No row-count timing exists. F29 built its
  pools once, at full rows. The hardware plan's "about 12 minutes of CPU
  per fit" at 833 variables comes from one 735.4 s build
  (`SPRINT_12_PLAN.md`); whether that build was sequential or full-pair is
  unverified. The QCi paper reports CVQBoost at about 2 s end to end
  (Dirac-3 solve about 1.3 s) at 150,000 rows
  (`docs/evidence-inventory.md`, section 3a).
- **ID and card**: Experiment 6, F110.
- **Question**: how does each part of CVQBoost training (weak-learner pool
  build, Hamiltonian construction, solve) grow with the number of training
  rows, at 91 and at 833 variables?
- **Predictions, stated now**: (P1) the pool build is the largest part at
  every row count and grows close to linearly in rows (log-log slope
  between 0.7 and 1.3). (P2) the solve does not grow with rows (slope
  between -0.2 and +0.2), because it works on the variables-by-variables
  matrix only. Hamiltonian construction is reported, with no prediction.
- **Falsifier**: P1 is false if the build is not the largest part at
  every fraction, or its slope interval leaves [0.7, 1.3]; P2 is false if
  the solve slope interval leaves [-0.2, +0.2].
- **Data**: ULB, F130's preparation (`qubo_proxy._prep`); training rows
  subsampled to 10%, 25%, 50% and 100%, stratified by label with the seed.
- **Cells**: `free` (k=13, schedule 2, full-pair, 91 variables) and
  `full` (k=17, schedule 3, full-pair, 833 variables), `dct` weak
  learners seeded per F145 (`qubo_proxy.seeded_weak_params`).
- **Timed parts**: `qubo_proxy.build_pool`; `h_matrix` plus `hamiltonian`
  (construction); `solve_simplex_qp` (solve; it rebuilds J once, so the
  construction time is subtracted and both are reported). Wall clock on
  this machine; the core count is recorded.
- **Seeds**: `free` 42-46. `full`: a one-seed pilot at all four fractions
  first; five seeds only if the pilot projects the five-seed run at 120
  minutes or less. Otherwise the pilot is the result, labeled one seed.
- **Test**: per part and cell, least squares of log time on log rows over
  all runs; the slope's 95% interval (t, residual degrees of freedom).
  m = 2 predictions, Bonferroni, so 97.5% intervals for P1 and P2.
- **Reported beside it**: the build at 833 variables against the
  hardware plan's 12 minutes, and the end-to-end time at about 150,000
  rows against the paper's 2 s.
- **Recording**: timing only, no test score, so no outcome block is
  required (section 2, "Outcomes recorded").
- **Implementation note, 2026-10-22, before any timing.** The library's
  full-pair builder (`build_pool(..., "full")`) forces `fork`, which does
  not exist on Windows, and the only Linux venv on this machine does not
  match the lock (numpy 2.5.2 against 1.26.4), so a result from it would
  not be comparable (`docs/ENVIRONMENT.md`). The pool is therefore built
  by `experiments/phase2/src/full_pair_pool.py`: the same learners, in the
  library's order, trained one after another by the library's own
  `WeakClassifier`. It was checked equal to the library's builder (same
  order, identical H) under `fork` on 2026-10-22, and
  `test_full_pair_pool.py` repeats that check on Linux CI. **Consequence
  for the reading**: "build" is a serial build. Set beside the hardware
  plan's 12 minutes it is like for like only if that build was serial
  too, which is unverified (above). The library's parallel build would be
  faster by up to its worker count; the slopes (P1, P2) are about growth
  with rows and are read the same way.
- **Correction, 2026-10-22, after two timing rows and before any slope.**
  "The construction time is subtracted" is narrowed to what the reason
  given for it covers: `solve_simplex_qp` rebuilds J, not H, so only the J
  build is subtracted from the solver's time. The first version subtracted
  H as well; the solve went negative and was clamped to zero on both rows.
  Those two rows were discarded and the run restarted. A row whose solve
  is still clamped is flagged (`solve_clamped`) and reported.
- **Note, 2026-10-23, after the run (PR review).** The code projected
  the remaining four seeds (43-46), not the five-seed run the Seeds line
  states: 79.4 minutes. With the pilot's own time added, the five-seed
  figure is also under the 120-minute cap (about 99 minutes), so the
  decision is the same under either reading.

### F103: SPECTRA Tier 1 known-answer check on UCI Steel

Written 2026-10-18 (Sprint 27 Task F, Decisions 1 option 2 and 2 option
1), before the module's first run. It is a verification of our own
reimplementation, not a Phase 2 claim about fraud data.

- **ID and card**: F103 (cross-domain study, step 1); new card F150
  repeats the substrate checks on the authors' construction.
- **Question**: does our reimplementation of the Fourier Wall paper's
  Tier 1 (arXiv:2607.15815, Algorithm 1) reproduce the values the paper
  publishes on UCI Steel and its two substrates?
- **Sources read**: the paper (sections 3-6, Algorithm 1, section 6.4's
  construction) and the two `spectra-tier1-spec.md` files in the Phase 1
  project's planning folders (identical, 238 lines, read-only). The spec
  files add nothing beyond the paper's section 6.4 and Algorithm 1.
  SPECTRA's code is proprietary; none of it is used.
- **Known answers and tolerances** (ROC-AUC on held-out rows, mean over
  seeds):
  1. **Gating value**: real target, g2's Fourier classifier = 0.94,
     tolerance 0.03. **Task G (F109) runs if and only if this holds.**
  2. Reported, pass or fail, not gating: sparse pocket JOINT minus GA2M =
     +0.37; dense substrate HGB minus GAM = +0.15 and JOINT minus GA2M =
     +0.00; tolerance 0.05 each. A failure is carried to F150 with its
     cause.
  3. **Not checked**: the paper's "joint ratio 9.9" is not defined in its
     text, so no ratio is computed against it (Unverified).
  4. Implementation check, before any substrate AUC is read: on the sparse
     pocket, JOINT's scan recovers the planted frequencies (3.7, 5.1, 6.8)
     within 0.05 each, up to a global sign; the paper reports (3.67, 5.13,
     6.83). If it does not, JOINT is wrong and no JOINT value is reported
     as a check.
- **Phases.** The SPECTRA release's phase columns are the paper's recipe
  plus zero-mean jitter (SD about 0.02 rad on four phases and 0.17 rad
  on the reactive phase, which departs by up to 0.69 rad), measured 2026-10-18 against the raw fields in the same
  file. So the phases are rebuilt from the raw fields by the paper's
  recipe: rank phase `2 pi (rank(v) - 1/2) / n - pi` of the log magnitude
  for active and lagging reactive power; time of day `2 pi NSM / 86400 -
  pi`; season `2 pi day_of_year / 365 - pi`; day of week `2 pi dow_num / 7
  - pi`. Ranks use all rows, covariates only (the paper's construction).
- **Real target.** `target_real` (base rate 0.2075, which matches the
  paper's 0.21 for `Load_Type == Maximum`; the file has no `Load_Type`, so
  this is Inferred). The five native phases above, all five in every lane.
- **Splits and seeds.** Stratified 70/30 train/test per seed, seeds 42-46;
  each value is the mean over the five seeds, with its SD.
- **Lanes** (identical phases and splits in every lane):
  - **GAM (g2's Fourier classifier)**: one trained frequency per phase,
    chosen on training rows by the least-squares (Lomb-Scargle)
    periodogram of the centered label (coarse grid 0.25-8.0 step 0.05,
    then step 0.005 within 0.05 of the maximum; changed from the plain
    periodogram before any run, because a synthetic test showed the plain
    one biased by 0.05 at a non-integer frequency on a bounded interval);
    features cos and sin of that frequency; logistic regression (lbfgs,
    C = 1.0). Secondary only: 2 and 3 harmonics per phase.
    (Noted 2026-10-18, after the run, from the Sprint 27 code review:
    every logistic regression lane, here and in GA2M and JOINT, first
    standardizes its basis on the training rows (`StandardScaler`). The
    code did this in the entry's commit, `a05ae94`; the text omitted it.)
  - **GA2M**: the GAM basis plus all pairwise products of the per-feature
    cos and sin terms; logistic regression.
  - **HGB**: scikit-learn defaults, `random_state` = seed.
  - **JOINT**: the GA2M basis plus up to 6 joint terms (the paper's default
    budget), each `cos(u)` and `sin(u)` of `u = sum f_j phi_j` over a
    3-way subset. Each term is chosen greedily on the training rows: the
    subset and frequency vector maximizing the periodogram of the current
    residual, on a coarse grid (0.5-8.0 step 0.5 on the first axis, plus
    or minus the same on the others), then step 0.05 within 0.5 of the
    coarse maximum; logistic regression refit after each term.
- **Gates.** g1: the fraction of 1-D periodogram mass (each phase,
  frequencies 0.05-8.0 step 0.05) farther than 0.1 from an integer;
  exploratory (no published value), threshold 0.3. g2: GAM AUC > 0.5.
  g3: HGB minus GAM > 0. g4: JOINT minus GA2M > 0. g5: d x q <= 14 with
  q = 1 (q = 2 reported beside it).
- **Sparse pocket** (section 6.4): the time-of-day, load and reactive
  phases, PCA-whitened and each component re-ranked to a uniform phase;
  z by Eq. 6 with w = 0.25, f = (3.7, 5.1, 6.8), the four offsets drawn
  uniform on [0, 2 pi) from the seed; tau = median z; y ~ Bernoulli(
  sigmoid(6 (z - tau))); 1% of labels flipped. All 35,040 rows (the paper
  states no row count for this substrate).
- **Dense substrate** (section 6.4): the seven fields that pass the > 50
  distinct-value screen (NSM 96, log active power, log lagging reactive
  power, day of year, leading reactive power 768, both power factors; CO2
  has 8 and is dropped), rank-phased, PCA-whitened and re-ranked; 6,000
  rows drawn without replacement from the seed. H(phi) = sum_k J_k (XX +
  YY + ZZ)_{k,k+1} + sum_i phi_i Z_i, J_k ~ U[0.5, 1.5] from the seed;
  |+>^7 evolved to t = 3 by three first-order Trotter steps (dt = 1; each
  step applies the six bond terms in order k = 1..6, then the field term);
  y = 1[<sum_i Z_i Z_{i+1}> > median]. Exact 128-dimensional statevector.
- **Reference first**: the permuted-label run (labels shuffled, seed 42)
  runs before the real target; every lane should sit near 0.5 and every
  difference near 0.
- **Device**: none. **Stopping rules**: a one-seed pilot times each lane
  before the five-seed run. **Reported whatever the result**: every lane's
  AUC per seed, every gate, the recovered frequencies, the pilot timing,
  the phase-jitter finding, and each check's pass or fail.

### F106: dequantization check of a sandwich-encoded circuit on ULB

Written 2026-10-18 (Sprint 27 Task I), before the module exists or any
lane is fit. The design comes from `docs/phase2/F6_GATE_BASED_ARM.md`
section 5; this entry fixes the lambda count, the readout, the phase
pipeline, the C threshold and the seed count (eight, from section 2a),
and governs wherever the two differ.

- **ID and card**: F106 (gate-based arm; F6 recommended pursue narrowly,
  simulation only).
- **Question**: on identical phase features, does any classical twin match
  a phase-active encoded circuit's test AUPRC on ULB within the margin?
- **Hypothesis and prediction**: dequantized. The Fourier Wall paper
  predicts payments data refuses its gates, and ULB's HGB is strong; the
  prediction is that HGB, the JOINT twin or both match or beat the
  circuit.
- **Falsifier**: every twin's interval lies wholly below zero (the circuit
  beats the complete bar). Separately, the encoding is reported as built
  wrong, and the circuit result does not count as a test of a phase-active
  encoding, if its phase complexity C < 0.01.
- **Data and splits**: ULB, `data.stratified_split` (60/20/20), seeds
  42-49. Features: `data.top_k_features(X_train, y_train, 8, seed)`.
  Training rows: every training positive plus 6,000 training negatives
  drawn from the seed; every lane trains on exactly these rows. The
  validation fold picks the RFF bandwidth only. The test fold is used
  whole.
- **Phases** (the Fourier Wall recipe, section 6.4, fit on training rows
  only): each feature's rank phase 2 pi F(v) - pi, with F the training
  rows' mid-rank empirical CDF, interpolated for other rows; the 8-phase
  block PCA-whitened by the training rows' covariance, then rank-phased
  again by the same rule. Every lane receives these 8 phases.
- **Arms**:
  - **Circuit**: 8 qubits, NumPy statevector, three layers. Each layer
    applies RY(phi_q / 2) on every qubit, exp(-i lambda_l sum_q Z_q
    Z_{q+1}) on the ring, RY(phi_q / 2) again, then trainable RY and RZ on
    every qubit. Readout logit b + sum_q w_q <Z_q>. 60 parameters: three
    lambda (start 0.5), 48 rotations and 8 weights (start uniform on
    [-0.1, 0.1] from the seed), and b (start at the training base rate's
    logit). Binary cross-entropy, Adam at learning rate 0.05, 1,500 steps
    of 512-row minibatches drawn from the seed. Exact gradients by the
    adjoint method, checked against finite differences in its test. No
    early stopping and no tuning.
  - **Twins** (F103's code where it exists): logistic regression on cos
    and sin of each phase; F103's trained-frequency GAM and GA2M; HGB on
    the phases (`random_state` = seed); F103's JOINT (six greedy 3-way
    terms); an RFF surrogate, `RBFSampler(n_components=1000)` on cos and
    sin of each phase, gamma from {0.05, 0.2, 0.8} by validation AUPRC,
    then logistic regression.
  - (Noted 2026-10-18, before the eight-seed run, from the Sprint 27 code
    review: the twins that reuse F103's `_lr` (logistic regression, GAM,
    GA2M, JOINT) standardize their basis on training rows. The RFF twin
    does not: its features feed `RBFSampler` and then an unscaled logistic
    regression, as in the entry's commit, `de63c40`. Cos and sin are
    bounded in [-1, 1], so this is recorded, not changed.)
- **Primary metric and test**: test AUPRC. For each twin T, the paired
  stratified bootstrap interval on the across-seed mean of (T minus
  circuit), as in Experiment 1 (2,000 replicates, the same row indices for
  both arms). **Dequantized** if any twin's interval lower bound exceeds
  -0.005 (section 2b's default margin): that twin is no worse than the
  circuit within the margin. **Circuit ahead** if every twin's upper bound
  is below 0. Anything else is **inconclusive**.
- **Multiplicity**: one family, m = 6 (one test per twin), Bonferroni:
  alpha 0.05 / 6 each, so 99.17% intervals. Eight seeds meet section 2a's
  Wilcoxon floor for m = 6; the exact Wilcoxon p-value per twin is
  reported beside its interval.
- **Secondary, uncorrected**: AUROC and floor-normalized AUPRC for every
  lane; the encoding diagnostics of the IBR paper (section 6.4 there) on
  the first layer alone at the trained lambda_1, over 100 training rows:
  phase complexity C, Berry connection magnitude |A| (central finite
  difference, step 1e-4) and the summed single-qubit von Neumann entropy;
  the trained lambdas.
- **Device**: none. Zero metered seconds; no Braket service is called.
- **Stopping rules**: a one-seed pilot times every lane first. The
  eight-seed run follows if it projects to 3 hours or less; otherwise the
  step count is cut to fit and the cut is recorded here before the run.
  - **Cut applied (2026-10-18, before the eight-seed run).** The pilot
    (seed 42, `experiments/phase2/results/f106_dequant_pilot.json`) took
    2,239 s: circuit training 1,865 s for 1,500 steps (1.243 s a step,
    with the F109 run sharing the CPU) and 374 s for prediction and the
    twins. It projected 17,913 s for eight seeds, over the limit. The
    limit allows 1,350 s a seed, so about 785 steps; the run uses **750
    steps**, projected 8 x (750 x 1.243 + 374) = 10,453 s. Nothing else
    changes. The pilot's lane values were seen before the cut; the cut
    is set by timing alone, from the rule above. The pilot ran 1,500
    steps, so its seed 42 row is not a row of the eight-seed run.
- **What is reported whatever the result**: every lane's AUPRC and AUROC
  per seed, every interval and Wilcoxon p-value, the outcome word, C, |A|,
  the entropy, the lambdas and the pilot timing.

### F107: shot budget of the F106 circuit, and what the Schmidt-rank threshold does not cover

Written 2026-10-18 (Sprint 27 Task J), before the module exists or any
shot is sampled.

- **Source finding first.** The card's "G1 Schmidt-rank threshold" is
  the evidence library's `entangled-data-schmidt-rank-threshold`, from
  Wang et al., "Transition role of entangled data in quantum machine
  learning", arXiv:2306.03481v2 (Nat. Commun. 2024), read 2026-10-18. Its
  r is the Schmidt rank of entangled *training states* shared with a
  reference system, for learning a target unitary under the projective
  observable (|0><0|)^n, at n = 4 (critical r = 3 at m = 10, r = 4 at
  m = 100). The F106 classifier has classical inputs, no reference
  system, no target unitary, and the readout sum_q w_q <Z_q>. So "the
  critical rank per shot budget for our feature count" has no defined
  meaning here, and this entry does not construct one.
- **What transfers (Inferred).** The paper's mechanism: information per
  measurement falls as entanglement rises. For a readout <Z_q>, the shot
  variance is (1 - <Z_q>^2) / m, largest when <Z_q> is near 0. A mixed
  reduced state, which entanglement across a cut produces, gives that;
  so does a pure equatorial state, the named alternative.
- **ID and card**: F107.
- **Question**: how many shots per row does the F106 circuit need before
  its test AUPRC is within 0.005 of the exact statevector's?
- **Hypothesis and prediction**: a budget between 100 and 10,000 shots;
  no direction is claimed for its relation to entanglement.
- **Falsifier**: none in the hypothesis sense; this is a measurement. It
  is reported invalid if the shot estimator does not converge to the
  exact <Z_q> in its test.
- **Data and arms**: F106's eight trained circuits (parameters saved in
  `f106_dequant.json`) on F106's test folds, rebuilt by F106's code with
  the same seeds. Arms: exact, and m in {10, 100, 1,000, 10,000} shots
  per row. Each shot draws one 8-bit outcome from |psi|^2 (a multinomial
  over the 256 outcomes, from the seed), so qubit correlations are kept;
  <Z_q> is the outcome average.
- **Primary metric**: per seed, the critical shot budget, the smallest m
  in the grid whose AUPRC is within 0.005 of exact (or "above 10,000").
  No multiplicity correction: no test is made.
- **Measured beside it**: per seed, the effective Schmidt rank of the
  circuit's output state across the qubits 0-3 | 4-7 cut (exp of the
  entanglement entropy from the SVD of the 16 x 16 amplitude matrix,
  averaged over 500 test rows), and the distribution of |<Z_q>|.
- **Not run, and why**: a critical *rank* curve needs circuits at several
  entanglement levels, which is F116's ON-against-OFF ablation, on HOLD
  until F106 shows the circuit is not dequantized.
- **Device**: none. Zero metered seconds.
- **Stopping rules**: runs after F106's eight-seed run; none otherwise.
  - (Noted 2026-10-18, before any F107 result: the first run refused on
    seed 42, its rebuilt exact AUPRC 0.70514 against F106's 0.70530.
    Cause: F107 evaluated the circuit in 4,096-row chunks and F106 in
    8,192; the scores differ by at most 4e-14, but that reorders
    near-tied rows. At 8,192 the exact value matches F106's bit for bit,
    so F107 now uses F106's chunk size. Nothing else changes. The shot
    draws depend on the chunking, so they are drawn under the new size.)
- **What is reported whatever the result**: AUPRC per seed at every m,
  the critical budget, the effective Schmidt rank and |<Z_q>| summary.

### F108: ceiling validation on a simulator with hidden state

Written 2026-10-18 (Sprint 27 Task K), before the module exists or any
transaction is generated.

- **ID and card**: F108 (ceiling methodology; enables F114).
- **Question**: on transactions whose Bayes error is known exactly, does
  any ceiling method recover the ceiling?
- **Generator** (clean room, from the Fraud Detection Handbook's prose,
  Le Borgne et al., chapter 3 "Simulated dataset", CC BY-SA 4.0; its
  GPL-3.0 code is not read or copied). 5,000 customers and 10,000
  terminals on a 100 x 100 grid; customer mean amount U[5, 100], SD half
  of it, daily rate U[0, 4]; available terminals within radius 5; 183
  days; per customer-day a Poisson count; time N(43,200 s, 20,000 s),
  outside the day discarded; amount N(mean, SD), a negative draw replaced
  by U[0, 2 mean]; terminal uniform over the available ones. Amounts are
  not rounded. Scenario 2: each day 2 distinct terminals are drawn; every
  transaction on them that day and the next 27 is fraud. Scenario 3: each
  day 3 distinct customers are drawn; for that day and the next 13, each
  of their transactions is selected with probability 1/3 (a Bernoulli
  draw, where the handbook selects a third; this keeps the posterior
  exact), its amount multiplied by 5, and marked fraud.
- **Two label sets.** Main: scenarios 2 and 3; the compromised-terminal
  and compromised-customer state is withheld. Zero-ceiling reference:
  scenario 1 alone (fraud iff amount > 220), deterministic in a visible
  feature, so its Bayes error is 0.
- **Observed features**: amount, the customer's mean amount, time of
  day. Hidden: everything else.
- **The known ceiling.** On days with both windows full (d >= 27), a
  transaction's terminal is compromised with probability pi_T and it is
  a scenario 3 selection with probability q. With g the amount density
  (normal on [0, inf) plus the fallback's uniform mass), the posterior is
  eta = 1 - (1 - pi_T)(1 - s), s = q g(a/5)/5 / (q g(a/5)/5 + (1 - q)
  g(a)). pi_T and q are the **realized** rates on the test rows (the
  fractions with the hidden scenario 2 and scenario 3 state), because the
  schedule is drawn once per world and its rates scatter around the
  closed-form priors, 1 - (1 - 2/10,000)^28 and (1 - (1 - 3/5,000)^14) /
  3, far more than a row-level binomial allows. So the ceiling is that of
  a row-wise classifier that knows the world's rates; the priors and the
  training rows' rates are reported beside it. (Revised before any run,
  after the generator test showed a closed-form check fails by design.) The Bayes error is the test mean of min(eta, 1 - eta); the
  Bayes AUPRC is the test AUPRC of eta. **The generator is checked
  against eta before any method is scored**: the Bayes classifier's
  realized error must lie within 3 binomial SDs of the Bayes error, and
  the mean of eta within 3 SDs of the fraud rate; otherwise the run stops
  as a generator defect.
- **Label noise** (FeeBee-style, Renggli et al. 2021), known rates: arms
  none, and fraud-to-legitimate 0.05 with legitimate-to-fraud 0.0005,
  applied to the main labels. The noisy posterior is (1 - 0.05) eta +
  0.0005 (1 - eta), so its ceiling is known too.
- **Splits**: train days 28-119, test days 120-182 (both windows full
  throughout, so eta does not depend on the day). Seeds 42-46.
- **Ceiling methods** (each scored on every arm):
  - plug-in: test mean of min(p, 1 - p) with p HGB's probabilities
    (default settings, `random_state` = seed);
  - learning-curve floor: HGB on the first 1/32, 1/16, 1/8, 1/4, 1/2 and
    all of the training rows (shuffled once by the seed); `a N^(-b) + c`
    fit to test error rate against training positives, and separately to
    1 - AUPRC; c is the floor (F114's method);
  - Cover-Hart: the 1-NN test error e on standardized features (100,000
    test rows from the seed) bounds the Bayes error to [(1 - sqrt(1 -
    2e)) / 2, e].
- **Margin, set here**: a Bayes-error estimate recovers the ceiling if
  within max(0.0005, 10% of the true value); an AUPRC ceiling if within
  0.01; the Cover-Hart interval if it contains the true value.
- **Primary metric**: per arm and method, recovered in at least 4 of 5
  seeds. No multiplicity correction: these are checks, not tests.
- **Added after the run, 2026-10-18 (a reading, not part of the entry
  as written).** The entry states no rule combining the arms. The
  result document reads "validated" as recovered on the main no-noise
  arm, because the noise arm moves the true ceiling toward the model and
  the reference arm's ceiling is 0, where the absolute margin alone
  decides. Under the entry as written, the plug-in meets the 4-of-5 rule
  on the noise and reference arms and fails it on the main arm.
- **Amendment, 2026-10-22 (Sprint 28 Task G, Decision 3 option 1),
  written before its module exists or any calibrated model is fit.** One
  new plug-in variant, scored on F108's generator, posterior, splits,
  seeds, arms and margin, all unchanged (`f108_ceiling` is imported, not
  edited):
  - **Model**: `HistGradientBoostingClassifier(l2_regularization=1.0,
    random_state=seed)`, other settings default. This is F151's stable
    reference (`docs/phase2/F151_HGB_COMPARATOR.md`), where 1.0 alone
    closed the spread. The Sprint 28 plan also listed
    `early_stopping=False` as a candidate; F151 found it unneeded, so it
    is not used here.
  - **Calibration**: the training rows are split once by the seed, 75%
    to fit HGB and 25% held out (stratified on the label). Isotonic
    regression (`IsotonicRegression(out_of_bounds="clip")`) maps HGB's
    held-out probabilities to the held-out labels; the test plug-in is
    the test mean of min(p, 1 - p) with p the calibrated probability.
  - **Reported beside it, not decisive**: the same 75% model's
    uncalibrated plug-in, which separates the effect of calibration from
    the effect of the regularization and the smaller fitting set.
  - **Rule**: F108's margin and 4-of-5 rule, decided on the **main
    no-noise arm** (the reading above, now written as the rule for this
    variant). The noise and reference arms are reported.
  - **Consequence, set here**: if the calibrated plug-in recovers on the
    main arm, F114's real-data run (ULB and IEEE-CIS, about 90 minutes)
    becomes eligible with this plug-in. If not, F114 stays blocked and
    the result is recorded on its card with the miss per seed.
  - **Reported whatever the result**: per seed and arm, the Bayes error,
    the calibrated and uncalibrated estimates, recovered or not, and the
    run time.
- **Amendment, 2026-10-26 (Sprint 29 Task D, F156), written before its
  module exists or any bound is computed.** One estimator not tied to a
  fitted model, on F108's generator, posterior, splits, seeds, arms and
  margin, all unchanged (`f108_ceiling` is imported, not edited):
  - **Estimator**: the Henze-Penrose bound of Berisha, Wisler, Hero and
    Spanias (IEEE TSP 2016, arXiv:1412.6534, Theorems 1 and 2, checked
    against the paper 2026-10-26). On a Euclidean minimum spanning tree
    of the pooled rows, C is the number of edges joining a fraud row to a
    legitimate row; with m fraud rows and n legitimate rows,
    D = 1 - C (m + n) / (2 m n), p = m / (m + n), q = 1 - p, and
    u = 4 p q D + (p - q)^2. The bound is
    [1/2 - sqrt(u)/2, 1/2 - u/2].
  - **Subsample**: the tree is built on a stratified random subsample of
    the training rows that keeps the class share, because the theorem's
    prior p is the sample's share (the Sprint 29 plan said "all training
    positives and a stated number of negatives"; that would bound the
    error at a different prior, so it is not used). Size: 60,000 rows,
    drawn with the seed. Features standardized with the training means
    and SDs, as F108's Cover-Hart method does. The tree is exact: it is
    taken from the edges of the Delaunay triangulation (which contains
    every Euclidean minimum spanning tree), with `scipy`.
  - **Pilot first**: seed 42, main arm, to time the build; if one seed
    takes over 10 minutes, the size is halved before any other seed and
    the change is recorded.
  - **Rule, both terms, main no-noise arm, 4 of 5 seeds**: (1) the
    interval contains the true Bayes error; (2) its width is at most
    2 x max(0.0005, 0.10 x Bayes error), twice F108's point margin (the
    Sprint 29 plan's width term: without it, the trivial interval
    [0, fraud rate] passes F108's containment rule on 5 of 5 seeds).
  - **Shown before any bound is computed: the two terms cannot both hold
    for this bound here.** With d = 1 - u, the upper end is d/2 and the
    lower end is (1 - sqrt(1 - d))/2, which is at most d/4 + d^2/8 for
    small d. So the width is at least d/4 - d^2/8. Containment needs
    d/2 >= Bayes error, about 0.0060-0.0063 on the main arm
    (`f108_ceiling.json`), so the width is at least about 0.0030; the
    width cap is about 0.0012-0.0013. **The rule therefore fails whatever
    the data**, and F114 stays blocked by this estimator. The run is kept
    because it is cheap and answers a separate question, reported and not
    decisive: is the bound valid (term 1) at a 0.8% fraud rate on 60,000
    rows, so that its upper end could serve as a conservative ceiling?
  - **Reported whatever the result**: per seed and arm, m, n, C, D, u,
    both ends, width, the Bayes error, each term's outcome, and the run
    time.
- **Amendment, 2026-10-31 (Sprint 30 Task F, F169, #80; Sprint 30 D3
  option 1), written before its module exists or any model is fit.** The
  plug-in with two estimators set for extreme imbalance, on F108's
  generator, posterior, splits, seeds 42-46, arms and margin, all
  unchanged (`f108_ceiling` is imported, not edited). Why two: F108's
  inferred cause of HGB failing the reference arm is that 255 quantile
  bins put a top-0.05% threshold inside one bin, possibly with early
  stopping on few positives. In scikit-learn 1.9.0, HGB's `max_bins`
  accepts 2-255 and 255 is the default (probed 2026-10-30: 256 raises),
  so HGB cannot take more bins.
  - **`hgb_no_es`**: `HistGradientBoostingClassifier(random_state=seed,
    early_stopping=False)`, every other setting F108's. (HGB's default
    `early_stopping="auto"` is on above 10,000 rows, so it was on in
    F108.)
  - **`lgbm_bins`**: `LGBMClassifier` in HGB's shape, 100 trees,
    learning rate 0.1, 31 leaves, 20 rows per leaf, `max_bin` 4095 (each
    bin then holds about 0.024% of the rows, under the reference
    threshold's 0.05%), no early stopping, `random_state=seed`.
  - **Method**: F108's plug-in, the mean of min(p, 1 - p) on the test
    window, fitted on the full training window, against the Bayes error.
    The learning curve and the other methods are not rerun.
  - **Rule, unchanged**: an estimator passes if its plug-in is recovered
    (within max(0.0005, 0.10 x Bayes error)) on 4 of 5 seeds on the main,
    no-noise arm; a stopped seed counts as a miss. The noise and
    reference arms are reported, not decisive.
  - **Attribution, set here**: both pass, early stopping was the cause;
    only `lgbm_bins` passes, the bins mattered; only `hgb_no_es` passes,
    early stopping alone suffices; neither passes, no plug-in is
    validated and F114 stays blocked.
  - **Reported whatever the result**: per seed, arm and estimator, the
    estimate, the Bayes error, their ratio, recovered or not, the test
    AUPRC against the Bayes AUPRC, the fit time, and an outcome block.
- **Device**: none. Zero metered seconds.
- **Stopping rules**: the generator check above. A method that does not
  recover is recorded as failing and is not used on real data (F114).
- **What is reported whatever the result**: per seed and arm, the fraud
  rate, the Bayes error and AUPRC, every estimate, the fitted (a, b, c),
  the generator check, and each method's recovered or failed.

### F109: Tier 1 across the six datasets on disk, and the IEEE-CIS aggregation

Written 2026-10-18 (Sprint 27 Task G), after F103's check passed and
before this module exists or any lane is fit here.

- **ID and card**: F109 (cross-domain study, steps 2-3).
- **Question**: which of the six datasets on disk does Tier 1 pass as a
  candidate, and does the IEEE-CIS UID aggregation change any gate?
- **Hypothesis and prediction**: the Fourier Wall spec predicts `refuse`
  for fraud. Tier 1 is permissive (F103), so the prediction here is
  narrower: on ULB, IEEE-CIS before aggregation and IEEE-CIS after, g4
  (JOINT - GA2M) is small, under 0.02. g3 is reported, with no
  prediction. (Revised 2026-10-18 after the fresh-eyes review, while the
  timing pilot ran and before any of its output was read: a "large
  margin" on g3 had no threshold, and the IEEE-CIS set was unnamed.)
- **Falsifier**: g4 >= 0.02 in at least 3 of 5 seeds on any one of the
  three sets.
- **Code**: F103's Tier 1 unchanged (`f103_tier1.run_target`: its 70/30
  stratified split, lanes, gates g1-g5), so these values are comparable
  with F103's.
- **Datasets and phases**:
  - **UCI Steel** (`target_real`): F103's five rows, cited, not rerun.
  - **ai4i, oilgas, telecom** (`target_real`): each release's `*_phase`
    columns, PCA-whitened and re-ranked (`f103_tier1.whiten_rerank`).
    F103 found the Steel release's phases carry small jitter; these are
    used as released and the check is not repeated.
  - **ULB** (`Class`) and **IEEE-CIS** (`isFraud`): a subsample of 30,000
    rows from the seed, every positive up to 3,000 and the rest
    negatives (ULB 492 + 29,508; IEEE-CIS 3,000 + 27,000; AUC does not
    depend on the base rate). Features: the top 6 by mutual information
    on the seed's training rows (6 keeps JOINT's 3-way search at 20
    subsets). Missing values become -999 before ranking. Phases: the rank
    phase on all rows (covariates only, the paper's recipe), whitened and
    re-ranked.
  - **IEEE-CIS before and after aggregation.** Before: the raw numeric
    columns less `TransactionID` and `TransactionDT`. After: Phase 1's
    `ieee_features.IEEEFeaturePipeline` (D-normalization, the UID
    aggregates, frequency encodings, V-reduction), **fit on every
    IEEE-CIS row except the subsample's test rows** and applied to the
    subsample. Its features use no labels, so the extra unlabeled rows
    are legitimate, and they keep the UID groups populated, which a fit
    on 21,000 subsample rows would not; the test rows never contribute.
    The UID key is not a feature. Each set takes its own top 6.
- **Seeds**: 42-46.
- **Primary metric**: every gate value per dataset and seed, and the
  Tier 1 word. No test is made, so no correction.
- **Device**: none. Zero metered seconds.
- **Stopping rules**: a one-seed pilot on a 10% time-ordered sample of
  IEEE-CIS (`ieee_harness.time_sample`) times the pipeline first. The
  five-seed run follows if it projects to 3 hours or less; otherwise the
  subsample shrinks to fit and the change is recorded here first.
- **What is reported whatever the result**: each dataset's lane AUCs,
  gates and word per seed; the chosen features per seed; the IEEE-CIS
  before-and-after pair.

### F142: the first Dirac-3S fits

Written 2026-10-14 (Sprint 26 Task D), before any Dirac-3S call. Not
filed; part of this draft.

- **ID and card**: unnumbered verify entry; F142.
- **Question**: what does a Dirac-3S fit cost and wait at our sizes, and
  does Dirac-3S return the same weights as Dirac-3 on a Hamiltonian whose
  coefficient spreads pass A31's test? (B4 passes that test. Its exact
  optimum's weights, about 0.0018, are below the about 0.005 weight
  resolution, A31's second half, so both devices return a sparser vector
  than the optimum, as on B2. The comparison is of the two devices in that
  regime, not a fidelity test on a fully resolvable problem.)
- **Hypothesis and prediction**: none directional. QCi's "much better
  results" has no published like-for-like basis
  (`docs/phase2/DIRAC_UNDERSTANDINGS.md`).
- **Falsifier**: "Dirac-3S behaves as Dirac-3 on B4" is contradicted if a
  Dirac-3S oilgas fit's weight cosine against the exact solve falls
  outside [0.8832, 0.9095]: Dirac-3's range over seeds 42-46 (0.8920-0.9007),
  widened on each side by its own width, so that leave-one-out it fires on
  none of Dirac-3's own seeds (`docs/sprints/SPRINT_26_PLAN.md`). With 2
  fits this is descriptive, not a test.
- **Data and splits**: B1 and B2 on ULB, B4 on oilgas_gasturbine; Phase 1
  stratified splits, unchanged.
- **Arms**: Dirac-3S fits through `eqc-models` 0.22.1 with
  `sampler_type="dirac-3s"`, in Phase 1's configurations (B1 `free`, 91
  variables; B2 `full`, 833; B4 frozen cell, 560), with F145's seeded
  weak learners. Compared with: Dirac-3's rows for the same cell and seed,
  read from `experiments/results/`; and the exact proxy solve of the same
  Hamiltonian.
- **Measures**: metered seconds (allocation balance before minus after),
  wall time including queue, weight cosine against the exact solve,
  objective gap to the exact optimum, exact-zero fraction, and test AUPRC
  and in-pocket AUPRC (B4) as Phase 1 scored them. Every returned sample
  is stored with the job id and device name.
- **Resolution screen**: B4 jobs must pass A31's test, measured on the
  Hamiltonian that is sent (seeded build, hash checked) before submission:
  the off-diagonal and linear spreads must each reach the largest
  coefficient divided by 200. The library's `get_dynamic_range` (largest
  over smallest coefficient, in dB) is recorded but is not the test: it
  passes B1 at 4.8 dB although no coefficient difference in B1 is
  resolvable (corrected 2026-10-14, before any call, at the dry run).
  The spread test is necessary, not sufficient: a spread of 37 steps means
  at most about 37 levels. The weight-resolution half of A31 (median exact
  weight against 1/200 of the sum constraint) is reported beside it, not
  enforced. Figures: `experiments/phase2/results/f142_dry_run.json`.
  B1 and B2 run under section 4's exception: their purpose is cost and
  queue time, their screen result is reported beside them, and they are
  never read as accuracy.
- **Multiplicity**: none; no test is run on 5 fits.
- **Device**: Dirac-3S. Three stops, each approved separately with its
  call count and seconds: B1 seed 42 (1 call, cap 60 s); B1 seed 43 and
  B2 seed 42 (2 calls, cap 150 s); B4 oilgas seeds 42 and 43 (2 calls, cap
  150 s). Later stops are re-quoted from stop 1's measured cost.
- **Stopping rules**: one attempt per unit, never retried by the runner,
  so a stop's approved call count is its ceiling. A stop ends at its cap
  (checked between units; a running call cannot be stopped) or at a failed
  unit. A Hamiltonian that differs from the screened one, or a B4 unit
  that fails the screen, is refused before anything is sent. A unit with
  any recorded attempt is never submitted again without a human decision.
  A balance that does not fall on a successful call is charged 10 s
  (Dirac-3S's billing source is unverified).
- **What is reported whatever the result**: every fit's cost, wait,
  device name and job id, failures included; the screen result beside
  each; the statement that 5 fits support no test.
- **Notes written AFTER the result (2026-10-15, Sprint 26 Task D). The
  text above is left as it stood before the first call.**
  1. The question's parenthesis predicted that both devices return a
     sparser vector than the optimum on B4. Dirac-3S did not: it zeroed
     the same 3 learners the optimum zeroes, against Dirac-3's 14-16%.
  2. The band falsifier fires on both seeds (cosine 0.999993 and
     0.9999999, in all 8 samples). Because B4's optimum is near-uniform,
     a uniform vector already scores 0.993, and one uniform except at the
     optimum's zeros scores 0.9957 and 0.9953 with a deviation correlation
     of 0.62 and 0.60. The device's departures from uniform correlate
     0.99976 and 0.99999. Both baselines were added after the result. A
     future twin entry should state such baselines before the run.
  3. "The exact solve" is a reference QP solve, not exact at this
     precision: the device's objective is slightly lower on both seeds,
     and the reference is less converged on seed 42 (gradient spread on
     the support 16, against 1.1). Reported energies are single precision
     and cannot rank the samples; the lowest-energy sample was read, and
     every sample gives the same reading.
  Reported in `docs/phase2/F142_DIRAC3S_VERIFY.md`; figures in
  `experiments/phase2/results/f142_readout.json`.

### F144: the proxy twin of B2's configuration

Written 2026-10-14 (Sprint 26 Task C), before any twin pool was built or
scored. Not filed; part of this draft.

- **ID and card**: unnumbered verify entry; F144.
- **Question**: does Dirac-3 beat an exact classical solve of its own
  Hamiltonian on B2's configuration, by more than the pool build's own
  run-to-run drift?
- **Hypothesis and prediction**: none directional. B2's device rows are the
  campaign's only positive result at scale; the twin says whether the
  device or the configuration produced it. Either answer is reported.
- **Falsifier**: "the device beats its proxy" is false if the test below
  does not reject, or if the drift reference rejects (then no device
  comparison is read).
- **Data and splits**: ULB credit-card, Phase 1 stratified protocol, seeds
  42-51, through `qubo_proxy._prep`, unchanged.
- **Arms**:
  1. **Device**: B2's 10 `hw_b2_full` rows in `experiments/results/
     results.json` (Dirac-3, September 2026). Read, never written.
  2. **Twin**: `full` config (k=17, weak-classifier schedule 3, full pair,
     833 variables, `dct`), lambda = 2 x n_train, exact simplex solve
     (`solve_simplex_qp`), with F145's seeded weak learners. It twins B2's
     configuration, not its pools, which were never stored.
  3. **Drift reference**: the 10 stored `h_*_free_dct_full` pools against
     fresh unseeded rebuilds of the same configuration (91 variables), both
     solved exactly. The true difference is zero by construction.
- **Primary metric and test**: test-fold AUPRC, scored as Phase 1 scored
  the proxy (`(w @ H_te + 1) / 2`, clipped). Exact two-sided Wilcoxon
  signed-rank on the 10 per-seed paired differences, alpha 0.05 (10 seeds
  reach p = 0.002). Reported beside it: the mean difference with a
  bootstrap 95% interval over seeds, the Phase 1 t-interval
  (`metrics.seed_mean_t_interval`), the floor-normalized AUPRC and AUROC.
- **Order of reading**: the drift reference first. If it rejects at
  alpha 0.05, the device comparison is reported as not readable, with the
  reason.
- **Multiplicity**: a family of two tests (reference, then device against
  twin), read in that fixed order, so no correction: the second is read
  only if the first does not reject.
- **Device**: none. Zero metered seconds.
- **Stopping rules**: none; 20 pool builds (10 twin, 10 reference) under
  WSL, about 15 and 2 minutes.
- **What is reported whatever the result**: every seed's three AUPRC
  values, both tests, and the statement that B2's pools were not stored.
- **Corrections written AFTER the result (2026-10-14, Sprint 26 fresh-eyes
  review). The text above is left as it stood before the run.**
  1. "Its own Hamiltonian" in the question is wrong: the twin solves a
     rebuilt pool of the same configuration.
  2. The falsifier is one-directional and the test two-sided: only a
     rejection with a positive mean would support "the device beats its
     proxy".
  3. The drift reference's true mean is zero by construction, so its
     Wilcoxon detects a systematic bias, not the size of the drift. Its
     per-seed spread (SD 0.0027) matches the device-twin spread (SD 0.0022).
  4. The multiplicity sentence reasons the wrong way round. A device claim
     needs the second test to reject and the first not to, so it is held
     at alpha; but that is the reason, not the one stated.
  The result is reported in `docs/phase2/F144_PROXY_TWIN.md` with these
  limits, and with a same-pool comparison that needs no rebuild.

### F154: where each model wins, on the stored ULB predictions

Written 2026-10-22 (Sprint 28 Task F, #47), before any pairwise or subset
count was computed. Not filed; part of this draft.

- **ID and card**: unnumbered analysis entry; F154.
- **Question**: is any stored model (classical, CVQBoost proxy, Dirac-3)
  reliably better than another on a subset of ULB test rows, so that an
  ensemble could use it?
- **Hypothesis and prediction**: none directional. F113 found no
  CVQBoost-specific complementarity with XGBoost on these files; this widens
  it to every pair and to two subsets. A null is reported as plainly as a
  find.
- **Data**: the stored per-row predictions in
  `experiments/results/predictions/` (read, never written), stratified
  protocol, seeds 42-51. Every family with all ten seeds is in. A family
  whose test labels differ from the others on any seed is reported and
  left out of the pairs. The test rows are matched to ULB features by
  deduplicating first, then `data.stratified_split(df, seed)`; the match is
  checked label for label on every seed before any subset is read.
- **Operating point**: the 0.5% alert budget on the test rows: every row at
  or above the ceil(0.005 x n)th highest score is flagged
  (`outcome_record.flagged_at_budget`; tied rows are flagged together).
  Recall in a subset is the share of that subset's frauds flagged.
- **Subsets**, fixed now: **amount**, a test row's `Amount` above the test
  fold's median `Amount` against at or below it; **day**, `Time` below
  86,400 s (day 1) against at or above it (day 2).
- **Primary test**: per pair (A, B), subset S and seed, the interaction
  I = [recall_A(S) - recall_B(S)] - [recall_A(not S) - recall_B(not S)].
  A subset claim needs the t interval of I over the ten seeds to exclude
  zero. The plain in-subset difference is not the test: on XGBoost full
  against matched13 it fired on day 1 because the overall difference
  carries into the subset, and it fired on 31.2% of random half-splits;
  the interaction fired on 3.8% (Sprint 28 plan, "Show each threshold can
  fire").
- **Multiplicity**: one family, m = (pairs) x 2 subsets, Bonferroni at
  0.05 / m, so each interval is at 1 - 0.05 / m. With 13 families,
  m = 156. Ten seeds give a t interval at any level, so section 2a's
  Wilcoxon floor does not bind.
- **Secondary, uncorrected**: the confusion counts for every stored result
  at both validation-chosen operating points; per pair and seed, the
  frauds A flags that B misses, the reverse, and those both flag; the
  in-subset differences.
- **Falsifier**: "some model is reliably better on a subset" is false for
  these files if no interaction interval excludes zero.
- **Recording**: the result file carries an `outcome_record` block per
  family and seed, pointing at the stored file and its SHA-256 (section 2,
  "Outcomes recorded").

### F162: in-pocket head-to-head on SPECTRA

Written 2026-10-23 (Sprint 28 Task M, #59), before any score. Not filed;
part of this draft.

- **ID and card**: unnumbered analysis entry; F162.
- **Question**: inside the SPECTRA pocket (`in_pocket` = 1), does the
  CVQBoost proxy rank the test rows better than HGB and XGBoost, paired by
  seed? Phase 1's H5 compared CVQBoost inside the pocket with a matched
  random segment outside it, which asks whether the pocket is special for
  CVQBoost. This asks the head-to-head the FourierWall2 in-pocket wins
  rested on (one seed, one stochastic run, never repeated).
- **Hypothesis and prediction**: the prior single-run evidence points to
  the proxy above XGBoost in the pocket on all three cells; F100 found HGB
  above the proxy overall on all three. No direction is predicted; a null
  is reported as plainly as a find.
- **Protocol** (the SPECTRA authors' recommendation, 2026-10-23):
  covariates plus phases only; `target`, `target_real` and `in_pocket`
  are never features (`spectra_segment._prep_spectra`, which asserts it;
  telecom_churn also drops `age`, as the frozen cell does); label
  `target`; `spectra_segment.spectra_split` (60/20/20 stratified on
  `target`); features through `coerce_features_to_numeric`.
- **Cells**: the three frozen cells (`spectra_segment.FROZEN_CELLS`):
  telecom_churn, energy_steel and oilgas_gasturbine. energy_steel is in:
  this comparison needs no matched control, so the infeasibility in
  `docs/SPECTRA_CONTROL_FEASIBILITY.md` does not apply.
- **Lanes**, all fitted on the training fold only:
  - **proxy**: the frozen cell's CVQBoost configuration (weak-classifier
    schedule 3, `dct` learners, sequential build, lambda = 2 x n_train),
    the pool seeded (`qubo_proxy.seeded_weak_params(seed)`), weights from
    `qubo_proxy.solve_simplex_qp`, score `(w @ H + 1) / 2` clipped to
    [0, 1], as `spectra_segment.proxy_dry_run_cell` scores.
  - **hgb**: `HistGradientBoostingClassifier(l2_regularization=1.0,
    random_state=seed)`, F151's stable setting.
  - **xgboost**: `XGBClassifier` at library defaults (xgboost 3.4.1) with
    `random_state=seed`. The Phase 1 tuned parameters were tuned on ULB and
    are not carried over. The FourierWall2 XGBoost settings are not on
    record here.
- **Seeds**: 42-51 (10). Section 2a: m = 6 primary tests need k = 8 for an
  exact Wilcoxon test to reach 0.05 / 6. Seed 42 runs first and is timed;
  if it projects the ten seeds above 120 minutes, the run is cut to 8
  seeds (42-49), decided from the time alone before any score is read.
- **No in-pocket positive floor.** Phase 1's 50-positive floor protected
  an unpaired comparison with a separately drawn control. Here every lane
  is scored on the identical pocket rows, so the pair shares the noise.
  Every seed counts; each seed's pocket size and positive count are
  reported.
- **Primary tests** (one family, m = 6): for each cell, proxy minus hgb
  and proxy minus xgboost in in-pocket AUPRC, per seed. Each test is the
  exact two-sided Wilcoxon signed-rank test on the per-seed differences at
  alpha 0.05 / 6, with the mean difference and its t interval at
  1 - 0.05 / 6 reported beside it. A cell's comparison is "proxy above"
  or "proxy below" only if the Wilcoxon test rejects and the interval
  excludes zero on the same side; otherwise "no reliable difference".
- **Secondary, uncorrected**: in-pocket ROC-AUC differences; in-pocket
  floor-normalized AUPRC (section 2); overall AUPRC and ROC-AUC per lane;
  hgb minus xgboost in the pocket; per-seed paired bootstrap intervals
  (`metrics.paired_delta_ci`) on the in-pocket AUPRC differences; each
  lane's train-test AUPRC gap (section 2).
- **Falsifier**: "the proxy is better than a classical model inside the
  pocket" is false on a cell if neither primary comparison there reads
  "proxy above".
- **What follows**: a "proxy above" on a cell is what would justify a
  device block there (F161 or a new card, under its own approval). Not
  run on any device here.
- **Recording**: every lane, cell and seed carries an outcome block
  (section 2), with validation scores for the validation-chosen operating
  points. Result `experiments/phase2/results/f162_in_pocket.json`
  (evidence tag `SIM`), generator `experiments/phase2/src/f162_in_pocket.py`.

### F158: fraud types, per-type detectors against one model

Written 2026-10-26 (Sprint 29 Task G, #70), before any model below is
fit. Not filed; part of this draft. No device.

- **ID and card**: unnumbered analysis entry; F158.
- **Question**: if each fraud type gets its own detector, do the
  detectors together catch more fraud than one model on everything, at
  the same alert budget?
- **Hypothesis and prediction**: none directional. Gradient boosting
  already concentrates on hard rows, so the gain may be small (the
  card's named risk).
- **Data**: F108's generator (`f108_ceiling.generate`, imported, not
  edited), main labels, no noise; train days 28-119, test days 120-182.
  The generator records each fraud's type: S2 (a compromised terminal)
  and S3 (a compromised customer, amount x5). Every fraud is S2, S3 or
  both, so after both types are found no untyped fraud remains: on the
  simulator the cascade is the two detectors, and "predict the rest"
  has nothing to predict. A row of both types is positive for both.
- **Features, the same for every model**: amount, the customer's mean
  amount and the time of day (F108's three), the amount over the
  customer's mean, the customer's transaction count on the previous day,
  and, with a 7-day label delay (the Fraud Detection Handbook's
  convention: a label is known 7 days after its day), the terminal's
  known-fraud count and transaction count over days d-14 to d-8 and
  d-35 to d-8, and the customer's known-fraud count over d-35 to d-8.
  F108's three features cannot see terminal fraud, so F108's Bayes
  posterior does not bound these models and is not used.
- **Models**, each `HistGradientBoostingClassifier(l2_regularization=
  1.0, random_state=seed)` (F151's setting), fit on the training days:
  - **single**: target fraud (S2 or S3);
  - **cascade**: one detector with target S2, one with target S3; a row's
    score is the larger of the two probabilities;
  - **shuffled reference**: the cascade with the type labels shuffled
    among the training frauds (fraud labels unchanged; seed-drawn). It
    should not beat the single model; if it does, a gain is not from the
    types.
- **Alert budget**: the top 0.5% of test rows by score. **Primary metric**:
  recall of all test fraud within the budget.
- **Seeds**: 42-49 (8), one simulated world each. One primary test, so
  an exact two-sided Wilcoxon test on 8 paired seeds can reach 0.05
  (smallest p 0.0078, section 2).
- **Primary test**: cascade minus single, recall at the budget, per seed;
  exact two-sided Wilcoxon at 0.05, with the mean difference and its 95%
  t interval beside it. "Cascade above" or "below" only if the test
  rejects and the interval excludes zero on the same side; otherwise "no
  reliable difference".
- **Secondary, uncorrected**: shuffled reference minus single, the same
  way; AUPRC per model; recall per type within the budget.
- **Step 2 (ULB and IEEE-CIS clustering)**: run only if the primary test
  reads "cascade above" and the shuffled reference does not; otherwise
  not run, with the reason recorded.
- **Step 3, descriptive**: the ULB test frauds that every model in F154's
  stored set misses at the 0.5% budget, counted per seed and compared
  with the caught frauds feature by feature (mean and SD), from F154's
  stored per-row scores. No test.
- **Recording**: every model and seed carries an outcome block (section
  2). Result `experiments/phase2/results/f158_fraud_types.json` (evidence
  tag `SIM`), generator `experiments/phase2/src/f158_fraud_types.py`.

### F166: best achievable result per algorithm on ULB (F157 part 1)

Written 2026-10-27 (Sprint 29 Task F, #69), before any score below.
Not filed; part of this draft. No device. Descriptive: no pass or fail.

- **ID and card**: unnumbered analysis entry; F166, the ULB part of F157.
  Device lanes (CVQBoost on hardware, QSVM) and QNN are out of this part.
- **Question**: tuned under one protocol, how well does each of seven
  algorithms do on ULB, and which differences between them are reliable?
- **Data and split**: ULB, duplicates dropped (`data.load_ulb().
  drop_duplicates()`), `data.stratified_split(df, seed)` (60/20/20), the
  split every Phase 2 ULB result uses. Tuning reads the training and
  validation folds only; every reported score is on the test fold, so no
  score comes from the rows that chose its configuration (section 2).
- **Features**: the classical lanes use all 30 columns; logistic
  regression and the SVM standardize them on the training fold. The proxy
  uses each configuration's own top-k features (`qubo_proxy._prep`).
- **The seven algorithms and their configurations**, named before any
  score. Selection per seed: the configuration with the highest
  validation AUPRC (ties: the first listed).
  - **HGB** (`HistGradientBoostingClassifier`, `random_state=seed`):
    `l2_regularization` {0, 1} x `learning_rate` {0.05, 0.1} x
    `max_leaf_nodes` {15, 31}. 8.
  - **LightGBM** (`LGBMClassifier`, 300 trees, `random_state=seed`):
    `num_leaves` {15, 63} x `learning_rate` {0.05, 0.1} x `reg_lambda`
    {0, 1}. 8.
  - **XGBoost** (`XGBClassifier`, `random_state=seed`): `max_depth` {3, 6}
    x `learning_rate` {0.1, 0.3} x `n_estimators` {100, 300}; the library
    default (6, 0.3, 100) is one of the 8.
  - **CatBoost** (`CatBoostClassifier`, 500 iterations,
    `random_seed=seed`): `depth` {4, 6} x `learning_rate` {0.05, 0.1} x
    `l2_leaf_reg` {3, 10}. 8.
  - **Logistic regression** (`LogisticRegression`, `max_iter=2000`):
    `C` {0.01, 0.1, 1, 10} x `class_weight` {none, balanced}. 8.
  - **SVM**: a linear SVM (`LinearSVC`, scores from
    `decision_function`) on all training rows, `C` {0.001, 0.01, 0.1, 1}
    x `class_weight` {none, balanced}. 8. **Alternative tried**: an RBF
    SVM (`SVC`, `gamma="scale"`, `C` {1, 10}) on a stratified 20,000-row
    subsample of the training fold, because an RBF kernel on about
    170,000 rows is quadratic. It is kept as the lane's form only if its
    best validation AUPRC beats the linear form's on a majority of seeds;
    the reason either way is recorded.
  - **CVQBoost proxy**: the three `qubo_proxy` configurations, free
    (k 13, order 2), mid (k 17, order 2) and full (k 17, order 3), with
    the full-pair pool, dct learners seeded by
    `qubo_proxy.seeded_weak_params(seed)` and `lambda = 2 x n_train`.
    **3 configurations, the stated exception to 8**: the proxy's design
    space is the frozen ladder. The full cell uses F159's parallel build
    only if F159's result records equal pools on held-out rows at every
    fraction; otherwise the serial build.
- **Metrics, test fold, for each algorithm's chosen configuration**:
  `metrics.summarize` (AUPRC and ROC-AUC with BCa intervals, and the two
  validation-chosen operating points: the max-F1 threshold and the 0.5%
  alert budget); AUPRC normalized by its floor; at each operating point
  TP, FP, TN, FN, precision, recall, specificity, F1, MCC and balanced
  accuracy (sklearn's `matthews_corrcoef` and `balanced_accuracy_score`);
  recall at the 0.5% budget on the test fold; the train-test AUPRC gap.
  Every chosen configuration and seed carries an outcome block (section
  2) with its validation scores; every tried configuration records its
  validation AUPRC and fit seconds.
- **Seeds, from seed 42's time** (Decision 3, option 1): seed 42 runs
  first, all seven algorithms, timed as `t42` minutes. The seed count is
  `n = min(10, floor(120 / t42))`, at least 3, seeds 42 to 41 + n. Below
  5 seeds the headline figures fall short of section 2's five-seed
  standard, and every page says so; a run that the minimum of 3 takes
  past 120 minutes records the overrun.
- **Intervals over seeds**: mean, SD and a 95% t interval of each metric.
- **Rankings** (the comparison page): algorithms are listed by mean test
  AUPRC. "A above B" is written only for an adjacent pair in that order
  whose primary test rejects at Bonferroni 0.05 / 6 (6 adjacent pairs).
  The primary test is chosen by n before any score: at 8 seeds or more,
  the exact two-sided Wilcoxon signed-rank test on per-seed AUPRC
  differences (the smallest p at 8 seeds, 0.0078, is below 0.0083); below
  8, a paired bootstrap of the seed-mean AUPRC difference (test rows
  resampled within each seed, stratified, the same rows for both
  algorithms, 2,000 draws, percentile interval at 1 - 0.05 / 6) rejects
  when its interval excludes zero, with the Wilcoxon result secondary.
  Otherwise the pair reads "no reliable difference".
- **Output**: `experiments/phase2/results/f166_ulb_algorithms.json`
  (evidence tag `SIM`), generator `experiments/phase2/src/f166_ulb_algorithms.py`,
  resumable by seed. One document per algorithm under
  `docs/phase2/algorithms/` and one ULB comparison page, each naming the
  result file, so `test_phase2_figures_resolve.py` checks their figures.

### F174: best achievable result per algorithm on IEEE-CIS (F157 part 2)

Written 2026-10-31 (Sprint 30 Task D, #78), before any score below.
Not filed; part of this draft. No device. Descriptive: no pass or fail.
Everything not stated here is as in the F166 entry above.

- **ID and card**: unnumbered analysis entry; F174, the IEEE-CIS part of
  F157. Device lanes and QNN are out of this part.
- **Question**: tuned under F166's protocol, how well does each of the
  same seven algorithms do on IEEE-CIS, and which differences between
  them are reliable?
- **Data and folds**: IEEE-CIS training data, exact duplicates removed
  (`ieee_loader.dedupe_ieee`), the rolling-origin month folds of F105's
  harness (`ieee_splits.rolling_origin_folds`, the leakage assertion run
  on every build). IEEE-CIS is split by time, not at random, so the
  validation and test rows are two months, not a 60/20/20 draw:
  - **Validation**: the month-3 fold. Every configuration is fitted on
    months 0-2 and scored on month 3.
  - **Test**: the month-4 fold, F152's first scored month. Each
    algorithm's chosen configuration is fitted again on months 0-3 and
    scored once on month 4. No score comes from rows that chose its
    configuration (section 2).
  - Features for each fold come from `ieee_harness.build_fold`, fitted
    on that fold's training months only, then the item-4 controls
    (`ieee_controls.apply_item4_controls`, seed 42, as F152), each on its
    own fold's training rows.
- **What a seed varies**: the folds are fixed, so a seed changes only
  each model's random state and the proxy's feature-ranking subsample.
  The spread over seeds is model randomness, not split randomness, and
  every page says so. A deterministic configuration gives the same score
  on every seed; its pair differences can be all zero, which the
  Wilcoxon test reads as "no reliable difference".
- **Algorithms and configurations**: F166's seven, with its grids,
  unchanged. Two changes, both forced by the data:
  - Logistic regression, the linear SVM, the RBF alternative and the
    proxy fill missing values with the training months' median
    (`SimpleImputer`, as F152's logistic lane); the four tree libraries
    take the missing values as they are.
  - **The proxy** uses each configuration's own top-k features ranked
    by `data.top_k_features` on a stratified 50,000-row subsample of the
    fitting rows (seeded by the seed, as F160), and the serial full-pair
    build. F159's parallel build is checked on ULB rows only, so it is
    not used here.
- **Metrics**: F166's, on the month-4 test rows, with an outcome block
  per algorithm and seed.
- **Seeds**: 10, seeds 42-51, with no time cap (Sprint 30 D4 and D5,
  team lead, 2026-10-31). Seed 42 runs first; its time is recorded and
  reported, and it does not change the count. At 10 seeds the primary
  test of an adjacent pair is the exact two-sided Wilcoxon signed-rank
  test at 0.05 / 6, with F166's bootstrap secondary.
- **Rankings**: as F166.
- **Output**: `experiments/phase2/results/f174_ieee_algorithms.json`
  (evidence tag `SIM`), generator
  `experiments/phase2/src/f174_ieee_algorithms.py`, resumable by seed
  (`LONG_RUN`). One page per algorithm and an IEEE-CIS comparison page
  under `docs/phase2/algorithms/`, from a tracked generator, each naming
  the result file, so `test_phase2_figures_resolve.py` checks their
  figures.

### F170: ULB frauds missed by every model, are their nearest neighbors legitimate?

Written 2026-10-31 (Sprint 30 Task G, #81), before its module exists or
any neighbor is computed. Not filed. No device.

- **Question**: F158 step 3 found 106 of 950 (seed, test fraud) pairs,
  seeds 42-51, missed at the 0.5% alert budget by every on-split family,
  comparing group means only. Row by row: do missed frauds sit among
  more legitimate training rows than caught frauds?
- **Data**: ULB, duplicates dropped, `data.stratified_split(df, seed)`,
  seeds 42-51; the stored families and the on-split check of F158 step 3
  (`f154_confusion.load`, `f158_fraud_types.on_split`), read only from
  `experiments/results/predictions/`.
- **Measure**: for each test fraud, the share of legitimate rows among
  its k = 10 nearest training rows, Euclidean distance on the 30
  features standardized with the training means and SDs.
- **Units**: distinct frauds. A row is in several seeds' test folds; its
  share is the mean over its appearances. It is "missed" if missed in
  every appearance, "caught" if caught in every one, and "mixed"
  otherwise (counted, not tested). Each missed row's identity is
  recorded, so the distinct frauds are counted.
- **Test**: two-sided Mann-Whitney U, missed against caught, alpha 0.05
  (two independent groups, no pairing). Secondary: the same test on all
  (seed, fraud) pairs, reported, not decisive.
- **Check first, on F108's simulator** (seed 42, main labels, its
  three features): frauds whose posterior is below 0.5 against the
  rest, the same measure and test. There the answer is known: frauds the
  Bayes classifier calls legitimate must sit among more legitimate rows.
  If the test does not find "higher" there, no ULB reading is made.
- **Reading, set here**: missed higher than caught, with a median share
  above 0.5, is consistent with ULB's information limit (the ceiling
  F169 estimates); otherwise a model weakness remains open.
- **Output**: `experiments/phase2/results/f170_missed_neighbors.json`,
  generator `experiments/phase2/src/f170_missed_neighbors.py`. No model
  is fit and no test score is computed, so no outcome block is needed.

### F171: F158 step 3 on IEEE-CIS, does the group every model misses shrink?

Written 2026-10-31 (Sprint 30 Task H, #82), before its module exists or
any count is made. Not filed. No device. Descriptive: no test.

- **Question**: ULB's features cannot grow; IEEE-CIS carries raw card,
  address, device and email fields. Is the share of test frauds missed
  by every stored family smaller there, counted as F158 step 3 counts?
- **Data**: F152's four stored families (xgboost, lightgbm, hgb,
  logistic), its rolling-origin months 4-6, seeds 42-46, from
  `f152_exp2.json`'s outcome blocks. Each score file must hash to its
  block's SHA-256, and its labels must equal the fold's own evaluation
  labels in order (`ieee_harness.folds_for` on the deduplicated data),
  or the run stops.
- **Count**: a (month, seed, test fraud) is missed by all when no family
  flags it at the 0.5% alert budget (`outcome_record.flagged_at_budget`).
  The share of such pairs, overall and per month, beside F158 step 3's
  ULB share read from `f158_fraud_types.json`; and the distinct missed
  rows.
- **Profile**: missed against caught rows on raw fields: the medians and
  missing shares of TransactionAmt, dist1, C1, C13 and D1, and the
  leading values of ProductCD, card4, card6, P_emaildomain and
  DeviceType. A row missed in one seed and caught in another is in both
  groups.
- **Reading, set here**: a share well below ULB's is consistent with
  richer information catching frauds a transform of ULB's features
  cannot. The datasets differ in more than feature richness (fraud rate,
  time split, labeling), so the comparison is descriptive, not causal.
- **Output**: `experiments/phase2/results/f171_missed_ieee.json`,
  generator `experiments/phase2/src/f171_missed_ieee.py`. No new test
  score is computed, so no outcome block is needed.

**Amendment 2026-10-31 (Sprint 30 Decision D7, option 1). POST HOC:
written after the 0.5% result above was seen.** The 0.5% count stays
F171's recorded result and is not replaced. At 0.5% one IEEE-CIS family
has 426 alerts for a month's 2,962 frauds, so the count measures the
budget more than the models; on ULB the same budget is about 3.0 times
the test frauds. Added, as exploratory figures:

- **Budgets**: `fixed_3.5`, a 3.5% budget (about IEEE-CIS's fraud
  rate); and `matched`, 3.0 times each fold's own test fraud rate (about
  10.4% on IEEE-CIS, 0.5% on ULB).
- **Data**: IEEE-CIS on this entry's families, months, seeds and checks;
  ULB on F158 step 3's on-split families and seeds.
- **Check first**: the 0.5% count is recomputed on both datasets and must
  equal the recorded F171 and F158 step 3 counts, or the run stops.
- **Also reported**: the capacity floor, the frauds that f families with
  k alerts each cannot flag (frauds - f x k, at least 0), so a share is
  read against what the budget allows.
- **Reading**: descriptive, no test. Only the `matched` budget compares
  the datasets at the same strictness.
- **Output**: `experiments/phase2/results/f171_budgets.json`, generator
  `experiments/phase2/src/f171_budgets.py`.

## 7. Open items before filing

- ~~Re-read arXiv:2604.18837 and confirm section 2 matches it.~~ Closed
  2026-10-18 (Sprint 27 Task C): section 2's source bullet now separates
  what is from the paper and what is added here.
- ~~Recompute section 5's downsized-pair figures from code, on all five
  seeds.~~ Closed 2026-10-18: section 5, `f102_downsized_pair.json`.
- Fill one section 6 entry per experiment that will run. **Open
  (2026-10-18)**: Experiment 1 is written; Experiments 2-6 wait on their
  cards (F105's adversarial-control decision, F25, F111, F121 on HOLD,
  F110), and each is written when its card is selected.
- ~~Set the multiplicity families, and each entry's seed count against
  them.~~ Closed 2026-10-18: section 2a. Each later entry applies it.
- **Pool build drift (F145): fixed for Phase 2 builds, a known limit for
  Phase 1 pools.** Decided 2026-10-14 (Sprint 26 Task B). Phase 2 builds pass
  `qubo_proxy.seeded_weak_params(seed)` (`build --seeded-learners`); two
  such builds of seed 42's `free` sequential pool are byte-identical on all
  three folds (`f145_build_drift.json`, `seeded`; corrected 2026-10-17: this
  said full-pair, and no seeded full-pair comparison is on record). Phase 1 pools were built unseeded and stay so: two seed-42
  `free` sequential builds share their training rows and differ on 64 of
  78 learners, 347 of 4,426,188 test cells
  (`experiments/phase2/results/f145_build_drift.json`; the counts vary from
  run to run, because the drift is random tie-breaking; ULB only, no other
  dataset is measured). Any Phase 2 comparison against a Phase 1 pool or
  device row carries that drift; F144's reference arm measures it at 91
  variables.
- ~~**Equivalence margins for verify entries.**~~ Closed 2026-10-18:
  section 2b (default AUPRC margin 0.005).
- Confirm the filing date and the filing venue with the team lead.
  **Open (2026-10-18)**: the team lead's decision; it is not taken here.

## Revision log

- 2026-10-13: first draft (Sprint 25, F102).
- 2026-10-13: revised after the Sprint 25 fresh-eyes review: seed counts
  set from the test's attainable p-value; the resolution-screen exception
  for cost and twin runs; the section 5 wording on when the design was
  written; F144 added.
- 2026-10-13: section 2 gains the claim-label rule (Sprint 25 IMP-1).
- 2026-10-14: section 6 gains the F144 entry, before any twin result
  (Sprint 26 Task C, Decision 1).
- 2026-10-14: section 7's F145 item decided: seeded for Phase 2 builds,
  reported for Phase 1 pools (Sprint 26 Task B).
- 2026-10-14: section 6 gains the F142 entry, before any Dirac-3S call
  (Sprint 26 Task D, Decision 1). Its screen, and section 4's, corrected
  from a dB ratio to A31's spread test after the dry run showed the ratio
  passes B1.
- 2026-10-14: after the Sprint 26 code review and fresh-eyes review, before
  any Dirac-3S call: F142's question scoped (B4 is in the weight-resolution
  regime), its falsifier band given to four places, its stopping rules
  tightened (one attempt per unit, pre-submit refusal); F144 gains a dated
  post-result correction note below its unchanged entry; section 7's F145
  figures cite a results file; equivalence margins added as an open item.
- 2026-10-15: F142 gains a dated post-result note below its unchanged
  entry (Sprint 26 Task D, after stop 3), revised after the F142
  fresh-eyes review the same day.
- 2026-10-18 (Sprint 27 Task C, F102): section 2's source re-read and
  attributed; sections 2a (multiplicity families) and 2b (equivalence
  margins) added; section 5 recomputed by code; section 6 gains the
  Experiment 1 (F112) entry, before its intervals are computed; section 7
  items closed or dated.
- 2026-10-18: section 6 gains the F103 entry, before its first run
  (Sprint 27 Task F); Experiment 1 gains its dated result note (Task D);
  section 6 gains the F106 entry, before its module exists (Task I).
- 2026-10-18: section 6 gains the F107 entry (Task J), the F108 entry
  (Task K; its ceiling definition revised before any run, after the
  generator test showed a closed-form check fails by design; a dated
  post-run reading of its arms) and the F109 entry (Task G; its
  prediction tightened after the fresh-eyes review, before any output was
  read). The section 6 table gains rows for F106-F109.
- 2026-10-22: section 2 gains "Outcomes recorded" (F154 standing rule,
  team lead); section 6 gains the F154 entry (Sprint 28 Task F), written
  before any pairwise or subset count, and its table row.
- 2026-10-22: section 6 gains the Experiment 2 entry (F152, Sprint 28
  Task B), written before any Phase 2 score on IEEE-CIS.
- 2026-10-22: section 6 gains the Experiment 3 entry (F153, Sprint 28
  Task C), written before any Hamiltonian is built.
- 2026-10-22: section 6 gains the Experiment 6 entry (F110, Sprint 28
  Task E), written before any timing.
- 2026-10-22: the F108 entry gains a dated amendment (F114, Sprint 28
  Task G): an isotonic-calibrated plug-in on F151's stable HGB, written
  before its module exists.
- 2026-10-22: section 6 gains the Experiment 4 entry (F111, Sprint 28
  Task D), written before its harness exists; the Experiment 6 entry
  gains an implementation note (serial full-pair build), before any
  timing.
- 2026-10-22: the Experiment 6 entry gains a dated timing correction
  (only the J build is subtracted), after two timing rows and before any
  slope.
- 2026-10-23: the Experiment 4 entry gains its seed-count decision (the
  run as written, above the cap; Sprint 28 Manual Validation DV2), after
  the pilot and before any full-size row.
- 2026-10-23: the Experiment 6 entry gains a post-run note: the pilot
  projected four remaining seeds, not five; the decision is unchanged
  (PR review). The section 6 status date updated.
- 2026-10-23: section 6 gains the F162 entry (Sprint 28 Task M, #59),
  written before any score, and its table row.
- 2026-10-26: the F108 entry gains a dated amendment (F156, Sprint 29
  Task D): the Henze-Penrose bound with the containment and width terms,
  and the arithmetic showing the two cannot both hold here, written
  before its module exists.
- 2026-10-26: the Experiment 3 entry gains a dated amendment (F160,
  Sprint 29 Task E): the room check on IEEE-CIS with a positive control
  first, written before its module exists.
- 2026-10-26: section 6 gains the F158 entry (Sprint 29 Task G), written
  before any model is fit, and its table row.
- 2026-10-27: section 6 gains the F166 entry (Sprint 29 Task F), written
  before any score, and its table row.
- 2026-10-31: section 6 gains the F174 entry (Sprint 30 Task D), written
  before any score, and its table row.
- 2026-10-31: section 6 gains the F170 and F171 entries (Sprint 30 Tasks
  G and H) and their table rows; the F108 entry gains its F169
  amendment (Task F) and the Experiment 3 entry its F176 amendment
  (Task E); each written before its module exists.
- 2026-10-31: the F171 entry gains a post hoc budget amendment (Sprint 30
  Decision D7), written after F171's 0.5% result was seen and before the
  new budgets were counted.
