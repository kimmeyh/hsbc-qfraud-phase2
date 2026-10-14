# F29: The CVQBoost Optimum Does Not Move With Sample Size

**Sprint 25 Task E** (#17) | **Date**: 2026-10-13 | **Evidence tag**: `SIM`,
zero metered seconds
**Result file**: `experiments/phase2/results/f29_sample_size.json`
**Generator**: `experiments/phase2/src/sample_size.py` (tests:
`experiments/src/test_sample_size.py`)

## Bottom line

**The premise holds, and the reason is the Sprint 4 degeneracy: the
optimum sits at uniform weights at every sample size, so there is nothing
to move.**

- On ULB, with the frozen `free` cell built sequentially (78 learners), the
  weights solved on 1/8, 1/4 and 1/2 of the training fold have cosine at
  least 1 - 6e-14 with the full-fold weights, on all 3 seeds. The plan's
  threshold was 0.99, so the falsifier did not fire and the card closes.
- Every solve is uniform to about one part in a million (largest over
  smallest weight, 1.0000009 to 1.0000023). The verdict follows from that
  uniformity; it is not separate evidence about the optimizer.
- **The tiny non-uniform residue does move.** Comparing only the parts of
  the weights that differ from uniform, the subsample against the full fold
  gives a cosine of 0.51 to 0.96. At one part in a million that residue has
  no effect on the model; it shows the objective is flat, not that the
  optimizer is stable.

**Scope.** Only the solve sees the subsample. Feature selection and the
weak-learner pool are built once per seed on the full 170,235-row fold. This
tests how the optimization depends on sample size, not the whole pipeline.

## Why the optimum is uniform

The learners agree on almost every row. F94's diagnostics in this sprint
measured it on the same cell (`experiments/phase2/results/f94_controls.json`):
on the training fold, 51 to 53 of the first 60 learners classify every row
correctly, and every pair of learners agrees on at least 99.989% of rows. So `HH^T/n` is close to a matrix of ones and `Hy/n` close
to a vector of ones, and both are nearly flat on the simplex: every weighting
gives almost the same data term.

> **Corrected 2026-10-14 (Sprint 26 fresh-eyes review).** The paragraph
> below, as first written, said Sprint 4 found the weights uniform "even at
> lambda = 0", so the ridge was not the cause. Amendment A27
> (`experiments/PREREGISTRATION.md`, 2026-09-10) had already withdrawn that
> claim: at lambda = 0 uniform is NOT the optimum, the minimizer set is a
> face of the simplex (twenty random starts land a mean L1 of 0.90 apart),
> and the penalty SELECTS a diffuse solution near uniform. The Sprint 4
> figure came from solving FROM uniform. So the ridge is what makes the
> answer near-uniform, and `066802a`'s "pinned at uniform by the ridge",
> which this write-up called wrong, was closer to the record. F29's
> measured result (cosine at least 0.99999999999994 across sample sizes)
> is unaffected; only its mechanism paragraph changes.

The data term is nearly flat on the simplex, so at lambda = 0 many
weightings tie (A27). The ridge (`lambda = 2 * n_train`) picks the most
even one among them, which pins the answer near uniform to about one part
in a million. F29 held lambda's rule fixed, so it does not measure how
uniformity changes with lambda; A27's `run_lambda0_spread.py` does at
lambda = 0.

## Results

| Fraction of the train fold | Rows | Cosine with full-fold weights (min) | Test AUPRC, mean of 3 seeds (sd) |
|---|---|---|---|
| 1/8 | 21,280 | 1 - 5e-14 | 0.7627 (0.036) |
| 1/4 | 42,559 | 1 - 5e-14 | 0.7651 (0.034) |
| 1/2 | 85,118 | 1 - 1e-14 | 0.7649 (0.035) |
| 1 | 170,235 | 1 | 0.7649 (0.036) |

All 78 weights are nonzero at every size.

## How to read the AUPRC column

- Mean differences across fractions are at most 0.0024; within one seed, at
  most 0.0064 (seed 44). Both are small against the spread across seeds
  (0.73 to 0.80).
- With weights equal to six decimals, the ensemble score is close to a
  plain vote count, which has many ties. Differences of one part in a
  million reorder tied transactions, and that moves AUPRC in the third
  decimal. The column measures tie-breaking, not a change in the model.
- **The pool build is not reproducible from the seed.** Seed 42's
  full-fold AUPRC came out 0.8056, 0.8049 and 0.8043 on three runs of this
  study with the same seed. The first two runs are not committed (their
  output was overwritten by the next run); the committed file is the third.
  The cause is not known. Any result that rebuilds a pool can drift by
  about this much between runs. Carded as F145.
- **Not to the draft standard.** 3 seeds and raw AUPRC, as the plan set.
  The Phase 2 reporting standard (`experiments/phase2/PREREGISTRATION_DRAFT.md`)
  asks for at least 5 seeds and normalized AUPRC; it is not yet binding,
  and this result predates it.

## What it means for the backlog

- F29 closes. Its question is answered, and the answer is the Sprint 4
  degeneracy, measured at four sample sizes.
- The same degeneracy is what F94 found on its training-fold instances: the
  continuous formulation, and the cardinality formulation built on the
  training fold, leave the optimizer nothing to choose between.
- F145 (new): find why the pool build is not reproducible from its seed.
