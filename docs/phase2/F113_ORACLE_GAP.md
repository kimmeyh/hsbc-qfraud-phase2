# F113: Oracle Gap Between CVQBoost and XGBoost

**Sprint 25 Task D** (#16) | **Date**: 2026-10-13 | **Evidence tag**: `SIM`,
zero metered seconds
**Result file**: `experiments/phase2/results/f113_oracle_gap.json` (every
figure below is in it)
**Generator**: `experiments/phase2/src/oracle_gap.py` (tests:
`experiments/src/test_oracle_gap.py`)

## Bottom line

**The falsifier did not fire, but it could not have: the gap says nothing
specific about CVQBoost, and the evidence leans against a router.**

- A perfect per-transaction choice between the best CVQBoost proxy and the
  best XGBoost recalls 5.0 points more fraud than XGBoost alone at the
  0.5% alert budget (mean over 10 seeds; range 2.1 to 8.4). The plan's
  falsifier was a mean gap under 1 point.
- **The same oracle between two XGBoost configurations clears it too**
  (mean 3.6 points). Any two models that are not identical produce a gap of
  a few points, and one fraud is already 1.05 points at 95 frauds a fold.
  The criterion was too weak to separate CVQBoost from a second XGBoost.
- **Almost none of the gap is fraud that CVQBoost catches.** Giving frauds
  the better of the two ranks adds 0.1 points over XGBoost; lowering
  legitimate rows to the better rank adds 4.4 points. The oracle mostly uses
  the label to push XGBoost's false positives down, which no router can do.
- **Label-free combinations do worse than XGBoost alone**: averaging the two
  ranks recalls 83.7%, taking the higher rank 85.3%, against XGBoost's
  85.6%.

So a router is not ruled out by this test, but nothing here supports one.
Before any router work, a stronger falsifier is needed: a gap above the
within-XGBoost reference, or a label-free router that beats XGBoost on
validation.

## What was measured

- **Data**: the stored ULB test-fold predictions, stratified protocol,
  seeds 42-51. 56,746 test transactions and 95 frauds per seed. Nothing
  was refitted.
- **Which models**: every stored CVQBoost proxy family (3) and XGBoost
  family (2) with predictions on all ten seeds, each checked against a
  `results.json` row. One of each was chosen by mean **validation** AUPRC,
  so the choice never saw the test fold: CVQBoost `47012b1404d5d4de` and
  XGBoost `d68789d82137da1d`. (The plan said "identified from its
  `results.json` row by config hash"; the predictions directory is the
  complete list of what can be scored, and each family is checked against
  `results.json`.)
- **Baseline**: one fixed model, the pair's better model by mean validation
  recall at the budget: XGBoost. It also wins on every test seed.
- **Budget**: the top 0.5% of scores flagged, 284 transactions per seed.
  Where scores tie at the cut, the tied group gets fractional credit, so no
  figure depends on row order.
- **Oracle**: each transaction takes whichever model ranks it better for its
  true label, by within-model percentile rank. It bounds any router that
  chooses or averages the two ranks per transaction; it does not bound a
  stacker that uses features or the raw scores.

## Results (mean over 10 seeds)

| Quantity | Recall at 0.5% |
|---|---|
| CVQBoost alone | 0.828 |
| XGBoost alone (baseline) | 0.856 |
| Oracle | 0.905 |
| Oracle, fraud half only (frauds take the better rank) | 0.857 |
| Oracle, legitimate half only (legitimate rows take the better rank) | 0.900 |
| Label-free: mean of the two ranks | 0.837 |
| Label-free: higher of the two ranks | 0.853 |
| **Oracle gap over XGBoost** | **+0.050** (min 0.021, max 0.084) |
| Within-family reference: oracle gap, XGBoost `03999a57` with XGBoost `d68789d8` | +0.036 (min 0.011, max 0.074) |

The other five CVQBoost-XGBoost pairs give mean gaps of 0.042 to 0.056.
Spearman rank correlation between CVQBoost and XGBoost: 0.18 over all test
rows, 0.71 over the frauds.

## How to read it

- **Why the legitimate half carries the gap.** CVQBoost's scores are nearly
  all tied: 91-92% of test transactions share one score (204-269 distinct
  values per seed), because its near-uniform weights over plus-or-minus-one
  votes produce vote counts. Many of XGBoost's false positives sit in that
  block, and the oracle uses CVQBoost's low tied rank to drop them. That
  needs the label.
- **The criterion.** The verdict uses the mean gap. Recall moves in steps of
  1.05 points, so any nonzero gap passes 1 point. The smallest single-seed
  gap is two frauds (2.1 points).
- **Ties at the cut.** The first version broke ties by row order; the code
  review found the oracle's tied group held a fraud on seeds 43 and 49.
  Fractional credit moved the mean gap from 0.0495 to 0.0496.
- **What it does not test.** The proposal's router criterion is judged out
  of time, on prespecified segments, against a matched random-segment
  control. This is in-time, stratified, and over the whole population.
- **Not to the draft standard.** No interval is reported on the gap. This
  analysis predates the Phase 2 reporting standard
  (`experiments/phase2/PREREGISTRATION_DRAFT.md`), which is not yet binding.

## For the backlog

- F113 is complete. Its question ("if the oracle barely beats the best
  single model, no router can help") is answered only weakly: the oracle
  beats it, but by no more than a second XGBoost would, and mostly through
  the label.
- F121 (the transfer half and the router) is on HOLD until F129 reports.
  F139 recommends that F129 not run, so F121's hold needs a new condition
  or a decision at the next refinement. This result is evidence for that
  decision.
