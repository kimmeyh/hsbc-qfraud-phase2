# F113: Oracle Gap Between CVQBoost and XGBoost

**Sprint 25 Task D** (#16) | **Date**: 2026-10-13 | **Evidence tag**: `SIM`,
zero metered seconds
**Result file**: `experiments/phase2/results/f113_oracle_gap.json`
**Generator**: `experiments/phase2/src/oracle_gap.py` (tests:
`experiments/src/test_oracle_gap.py`)

## Bottom line

**A router is not ruled out.** A perfect per-transaction choice between the
best CVQBoost proxy and the best XGBoost catches 4.9 points more fraud than
XGBoost alone at the 0.5% alert budget (mean over 10 seeds; range 2.1 to
8.4). The plan's falsifier was a gap under 1 point, and it did not fire.

This is an **upper bound**, not evidence that a router would work. The
oracle knows each transaction's label; a real router does not. F121 stays
on HOLD for its own stated reason (F129), and this result does not move it.

## What was measured

- **Data**: the stored ULB test-fold predictions, stratified protocol,
  seeds 42-51. 56,746 test transactions and 95 frauds per seed. Nothing
  was refitted.
- **Which models**: one CVQBoost proxy family and one XGBoost family, each
  chosen by mean **validation** AUPRC across the seeds, so the choice never
  saw the test fold. CVQBoost: `47012b1404d5d4de` (the `deep` cell, 377
  learners). XGBoost: `d68789d82137da1d`.
- **Budget**: the top 0.5% of scores flagged, 284 transactions per seed.
- **Oracle**: each transaction takes whichever model ranks it better for its
  true label, by within-model percentile rank. A fraud takes the higher
  rank; a legitimate transaction takes the lower.

## Results (primary pair, mean over 10 seeds)

| Quantity | Value |
|---|---|
| CVQBoost recall at 0.5% | 0.828 |
| XGBoost recall at 0.5% | 0.856 |
| Oracle recall at 0.5% | 0.905 |
| Oracle gap over the better model | **+0.049** (min 0.021, max 0.084) |
| Spearman, all test rows | 0.18 |
| Spearman, frauds only | 0.71 |

The other five pairs give gaps of 0.042 to 0.056, so the result does not
depend on which families were chosen.

## How to read it

- **Every seed clears 1 point**, the smallest by 2.1 points. One fraud is
  1.05 points of recall at 95 frauds per fold, so the smallest gap is two
  frauds and the mean about five.
- **The two models agree on the frauds and disagree on everything else.**
  Rank correlation is 0.71 among frauds and 0.18 overall. The low overall
  figure is mostly CVQBoost's ties: its scores take only 204-269 distinct
  values per seed, because near-uniform weights over plus-or-minus-one
  votes produce vote counts. XGBoost's take 25,000-56,000.
- **Ties do not move the recall figures.** At the 0.5% cut, the tied
  scores hold no frauds on any seed, for either model.
- **What it does not test.** The proposal's router criterion is judged out
  of time, on prespecified segments, against a matched random-segment
  control. This is in-time, stratified, and over the whole population. It
  bounds that test from above; it does not run it.

## For the backlog

- F113 is complete. Its question ("if the oracle barely beats the best
  single model, no router can help") is answered: the oracle does more than
  barely beat it, so the router line stays open.
- F121's hold is unchanged (it waits for F129).
