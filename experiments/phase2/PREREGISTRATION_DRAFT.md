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
on 2026-10-18:

| # | Experiment | Card(s) | Device | Entry |
|---|---|---|---|---|
| 1 | Isolate the confound: the k=17 decomposition | F112 | none | Written 2026-10-18, below |
| 2 | Temporal validity on IEEE-CIS rolling-origin folds | F105 | none | To write |
| 3 | Cardinality-constrained selection on the integer solver | F94 (controls, built Sprint 25), F25 | Dirac-3S, after F141 and F142 | To write; F94's result informs it |
| 4 | Replication under the source protocol (Loke et al.) | F111 | none | To write |
| 5 | Segment transfer (H5), with the section 5 control | F121 | to be decided | To write; F121 is on HOLD |
| 6 | Scaling claim: training time against sample count | F110 | proxy first | To write |
| - | Dirac-3S verify runs: B1 and B2 (cost), B4 (fidelity twin) | F142 | Dirac-3S | Written 2026-10-14, below |
| - | The proxy twin of B2's pool (k=17, order 3) | F144 | none | Written 2026-10-14, below |
| - | SPECTRA Tier 1 known-answer check (verification, not a claim) | F103 | none | Written 2026-10-18, below |
| - | Gate-based arm: dequantization check (F6 recommended pursue narrowly) | F106 | none (NumPy statevector) | Written 2026-10-18, below |
| - | Gate-based arm: the F106 circuit's shot budget | F107 | none (NumPy statevector) | Written 2026-10-18, below |
| - | Ceiling validation on a simulator with hidden state (verification) | F108 | none | Written 2026-10-18, below |
| - | Tier 1 across the six datasets on disk | F109 | none | Written 2026-10-18, below |

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
