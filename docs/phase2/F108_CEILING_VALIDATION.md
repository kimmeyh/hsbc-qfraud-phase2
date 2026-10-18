# F108: ceiling validation on a simulator with hidden state

Sprint 27 Task K, 2026-10-18. Zero metered seconds. The entry is the
Phase 2 draft's section 6, "F108", committed before the first run
(`0721393`). Every figure below is in
`experiments/phase2/results/f108_ceiling.json` (seeds 42-46); the
one-seed pilot is `f108_ceiling_pilot.json`.

## BLUF

**No ceiling method recovered the known ceiling on the main, no-noise
arm, so none is validated for real data, and F114 has no method to
run.** The generator is exact: on every seed the Bayes classifier's
realized error matches the posterior's Bayes error to within 0.00002.
On the main arm, the HGB plug-in overstates the Bayes error by 5-12%
(recovered on 2 of 5 seeds; three misses are by 0.5-1.8 points past the
10% margin, so the verdict turns on that margin) and the learning-curve
floor by a similar amount (1 of 5); the AUPRC floor understates the
attainable AUPRC by about 0.04 and is unstable; the Cover-Hart interval
contains the truth on 3 of 5. The entry needs 4 of 5.

**What "validated" means here was read after the run.** The entry
states no rule combining the arms. Under the entry as written, the
plug-in meets 4 of 5 on the noise arm (5 of 5) and on the reference arm
(5 of 5). This document requires the main arm, for the reasons in
"Reading"; the entry carries a dated note saying so.

## The world (Measured)

- 1.75-1.80 million transactions per seed (mean 1.77); main-label fraud
  rate 0.83% in the test window. The handbook's text states about 1.75
  million.
- Known ceiling, main labels, no noise: Bayes error 0.0060-0.0063,
  Bayes AUPRC 0.296-0.318. Scenario 2 (a compromised terminal, with a
  normal amount) is invisible in the features, which is chiefly what
  makes the ceiling nonzero; scenario 3's multiplied amounts overlap
  normal ones and add a little.
- Generator check: realized Bayes-classifier error against the exact
  Bayes error, within 3 SDs on all five seeds (largest gap 0.00002).

## Results (Measured; recovered seeds of 5)

- **Main, no noise**:
  - plug-in 0.0064-0.0070 against 0.0060-0.0063, ratios 1.053, 1.097,
    1.105, 1.114 and 1.118: **2 of 5** within the 10% margin.
  - learning-curve floor on error 0.0064-0.0071: **1 of 5**.
  - learning-curve floor on AUPRC, ceiling 0.255-0.312 on four seeds
    and 0.87 on seed 43 (true 0.300), against 0.296-0.318: **1 of 5**. The full-data HGB
    reaches 0.250-0.268, so the floor mostly tracks the model, not the
    ceiling.
  - Cover-Hart interval: **3 of 5**; its lower bound sits just above the
    truth on the other two.
- **Main, with label noise (0.05 and 0.0005)**: plug-in **5 of 5**
  (ratios 1.075-1.098); floor on error 3 of 5; floor on AUPRC 0 of 5
  (0.98 on seed 43, true 0.272); Cover-Hart 2 of 5.
- **Zero-ceiling reference (scenario 1, fraud iff amount > 220)**:
  plug-in 5 of 5, but only through the absolute margin (0.0003-0.0004
  against 0); floor on error 1 of 5; floor on AUPRC 0 of 5; Cover-Hart 0
  of 5, because any positive 1-NN error puts the lower bound above 0.
- **HGB fails the reference.** On a label that is a single threshold in
  a visible feature, default HGB reaches AUPRC 0.008-0.026 where the
  Bayes AUPRC is 1.0. The positives are the top 0.05% of amounts.
  Cause, Inferred and not verified: the 255 quantile bins put the
  threshold inside one bin, possibly compounded by early stopping on so
  few positives.

## Reading

- **What a ceiling method must beat here (Inferred).** Each method's
  estimate is anchored on a fitted model, and the model is about 10%
  short of the posterior on the error scale and about 0.04 short on
  AUPRC. A method that reports the model's own performance as the
  ceiling cannot see that gap. This is the case F114 exists for:
  headroom that a better model could reach.
- **The AUPRC floor is not usable as specified.** A three-parameter fit
  to six points at extreme imbalance is ill-conditioned; on seed 43 it
  returned a ceiling (1 - c) near 0.9 on both arms.
- **The noise arm's pass is narrow (Inferred).** The plug-in overstates
  the Bayes error by 8-10% with noise and 5-12% without. Noise raises the
  true error, so the same model gap is a smaller fraction of it and falls
  under the 10% margin. The named alternative: the plug-in genuinely
  tracks noisy ceilings better. Five seeds cannot separate the two.
- **The HGB finding may matter beyond F108 (Inferred).** A default HGB
  can miss a rare, sharp threshold entirely. HGB is the classical bar in
  F103, F106 and F109. Whether their positives contain such a threshold
  is **Unverified**; it needs a check before this transfers or is ruled
  out.

## What follows

- F114 does not run on real data with any of these four methods (F108
  card rule). A ceiling method has to be validated here first.
- Candidates for that work, not done here: a calibrated or better model
  under the plug-in (the gap is the model's), a Bayes-error estimator
  that does not go through one model, and an HGB with `max_bins` and
  early stopping set for extreme imbalance.

## Clean-room note

The generator is written from the handbook's prose (Le Borgne et al.,
"Reproducible Machine Learning for Credit Card Fraud Detection: Practical
Handbook", chapter 3, "Simulated dataset", CC BY-SA 4.0). The handbook's
code is GPL-3.0 and was not read or copied. Two stated departures:
amounts are not rounded, and scenario 3 selects each transaction with
probability 1/3, so the posterior is exact.
