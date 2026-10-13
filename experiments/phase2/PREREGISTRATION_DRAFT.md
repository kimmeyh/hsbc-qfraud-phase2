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
  first commit, not only to this document's experiments. (Sprint 25: F29's
  first write-up said the ridge pinned the weights at uniform. Sprint 4 had
  already found them uniform at lambda = 0, which rules that out; naming
  the alternative would have surfaced it before the commit.)
- **Source for the statistical standard**: arXiv:2604.18837, as cited on the
  F102 card. To be re-read against its text before filing.

## 3. Two meanings of "order 3"

They are different things, and every document states which it means:

- **Pool order**: weak learners built over feature triples (weak-classifier
  schedule 3). This happens classically, before the device sees anything.
- **Objective order**: the degree of the polynomial the device minimizes.
  CVQBoost's objective is quadratic by construction, whatever the pool
  order. Dirac-3 and Dirac-3S both accept degrees up to 5 (F138), but no
  experiment in this draft uses a degree above 2.

## 4. Device rules

- **Every hardware row names its device** (`dirac-3` or `dirac-3s`) and
  carries its `job_id` and every returned sample (F133; F141 adds the
  device field).
- **A Dirac-3 against Dirac-3S comparison is a Phase 2 result** with its
  own entry in section 6. It is never reported as a new cell of a Phase 1
  gate; under the frozen preregistration's section 11 that would be a
  deviation (F138, question 6).
- **The resolution screen gates every metered block** (F104): before any
  call, the job's coefficient range is tested against the device's stated
  200:1 (23 dB) resolution. QCi states the same figure for both devices;
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
  keeping size and rate matched on each. On seed 42 that is 855 positives
  plus 278 negatives per side, keeping 88-94% of the pocket's positives,
  with the AUC interval about 4% wider. Feasible on all five seeds
  (figures from the F102 card, 2026-10-05; to be recomputed by code before
  filing).
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
on 2026-10-13:

| # | Experiment | Card(s) | Device | Entry |
|---|---|---|---|---|
| 1 | Isolate the confound: the k=17 decomposition | F112 | none | To write |
| 2 | Temporal validity on IEEE-CIS rolling-origin folds | F105 | none | To write |
| 3 | Cardinality-constrained selection on the integer solver | F94 (controls, built Sprint 25), F25 | Dirac-3S, after F141 and F142 | To write; F94's result informs it |
| 4 | Replication under the source protocol (Loke et al.) | F111 | none | To write |
| 5 | Segment transfer (H5), with the section 5 control | F121 | to be decided | To write; F121 is on HOLD |
| 6 | Scaling claim: training time against sample count | F110 | proxy first | To write |
| - | Dirac-3S verify runs: B1 and B2 (cost), B4 (fidelity twin) | F142 | Dirac-3S | To write before F142 runs |
| - | The proxy twin of B2's pool (k=17, order 3) | F144 | none | To write before any B2 comparison |
| - | Gate-based arm | F6, F106, F107 | Braket | To write if F6 recommends pursuing |

## 7. Open items before filing

- Re-read arXiv:2604.18837 and confirm section 2 matches it.
- Recompute section 5's downsized-pair figures from code, on all five
  seeds.
- Fill one section 6 entry per experiment that will run.
- Set the multiplicity families, and each entry's seed count against them
  (section 2).
- Decide whether the pool build's run-to-run drift (F145) must be fixed or
  only reported.
- Confirm the filing date and the filing venue with the team lead.

## Revision log

- 2026-10-13: first draft (Sprint 25, F102).
- 2026-10-13: revised after the Sprint 25 fresh-eyes review: seed counts
  set from the test's attainable p-value; the resolution-screen exception
  for cost and twin runs; the section 5 wording on when the design was
  written; F144 added.
- 2026-10-13: section 2 gains the claim-label rule (Sprint 25 IMP-1).
