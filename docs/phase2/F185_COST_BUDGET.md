# F185: A Cost-Weighted Alert Budget

**Card**: F185 | **Sprint**: 32, Task D (#113) | **Metered seconds**: 0
**Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F185"
(written 2026-11-09, before any amount was joined)
**Result**: `experiments/phase2/results/f185_cost_budget.json`
**Generator**: `experiments/phase2/src/f185_cost_budget.py`

## Bottom line

At the same number of alerts as today's 0.5% budget, ranking by
expected loss (score times amount) instead of by score catches about
four times the fraud dollars on IEEE-CIS month 4, on all ten seeds: a
mean of $140,832 against $34,675, of $493,821 in fraud that month. It
catches fewer frauds to do it, on every seed of both datasets: on
IEEE-CIS 246 to 373 instead of 400 to 416. On ULB the mean gain is 755
units and its 95% interval includes zero: no reliable difference.
IEEE-CIS month 4 is one fixed test set, so its intervals show the spread
over training seeds only, not over months or transactions.

## What was compared

- **Scores**: the stored per-row test scores of the two champions, ten
  seeds each: ULB CatBoost (F166) and IEEE-CIS LightGBM (F174). Each
  file's SHA-256 was checked against its outcome block, and the rebuilt
  test labels against the stored ones, row for row, before any amount
  was joined. No file was refused.
- **Amounts**: ULB `Amount` (its unit is not stated in its source);
  IEEE-CIS `TransactionAmt`, read as US dollars (unverified: no source
  for the unit is recorded in this repository).
- **Rankings**: (1) by score, today's; (2) by score times amount, the
  expected loss of Hoppner et al.'s rule (EvidenceBasedDB
  `hoppner-instance-threshold`, high). Both flag the same number of
  rows: 284 on ULB, 427 on IEEE-CIS. Scores are used as given, not
  recalibrated.
- **Check first**: a built case where ranking (2) must catch more
  dollars (it caught 1,000 against 10), and a label vector with one
  label flipped, which the join refused. Both fired. The entry describes
  the second check as "a stored file with one label flipped"; the code
  flips a label in a built four-row vector and passes it to the join,
  without writing or reading a file. The join is the step that refuses,
  so the check reaches the same refusal, but by a shorter path than the
  entry states.

## What it found

- **IEEE-CIS**: dollars caught, mean over seeds (95% t interval):
  - by score: $34,675 ($32,485 to $36,865);
  - by expected loss: $140,832 ($136,567 to $145,098);
  - the paired gain: $106,157 ($101,562 to $110,753). Every seed gains.
- **ULB**: by score 9,546 units, by expected loss 10,301; the paired
  gain is 755 (-50 to 1,561). Six seeds lose 7 to 32 units; four gain
  679 to 2,816. Whether the large gains come from a few high-amount frauds
  was not tested (Inferred).
- **The cost of the trade**: at a fixed alert count both rankings pay
  the same review cost, so the review cost changes net savings, not the
  order. On IEEE-CIS seed 42, at $10 a review, net savings are $28,504 by
  score and $136,866 by expected loss.
- **Frauds caught fall on every seed**: IEEE-CIS 400 to 416 by score,
  246 to 373 by expected loss; ULB 77 to 86 by score, 43 to 73 by
  expected loss. On IEEE-CIS seed 42, false alerts rise from 12 to 119.
- **Hoppner's own rule** (s x A > c) raises far more alerts than the
  budget on IEEE-CIS (1,552 to 13,028 over seeds and costs, against
  427) and fewer on ULB (33 to 121, against 284). The scores are not
  calibrated probabilities, so these counts are not a staffing figure.

## What it means

- A bank weighs fraud by the money it loses. On IEEE-CIS, the measure
  this repository has used (frauds caught at 0.5%) and the bank's
  measure (dollars caught at the same review count) choose very
  different alerts from the same scores. A comparison of a quantum lane
  against a classical one should report both.
- On ULB the gain varies by seed: four seeds gain a lot and six lose a
  little, so the mean and its interval sit over two groups. Why (for
  example, a few high-amount frauds) was not tested.
- The expected-loss order depends on the scores' scale: a nonlinear
  calibration (Platt or isotonic) changes s x A and so the alerts
  chosen. The four-times figure holds for these uncalibrated scores
  only (Inferred).
- Net savings count the review cost of every alert, not the cost of a
  false alert to the customer, as the entry defined.
- Not tested here: calibrated scores, a review cost that grows with the
  amount, other test months, or a budget set in dollars rather than
  alerts.

## Outcome blocks

Each seed's row carries two blocks (`outcome_by_score`,
`outcome_by_expected_loss`): the confusion counts at the budget and the
scores' file with its SHA-256.
