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
flags fewer frauds to do it (308 against 415 on seed 42). On ULB the
mean gain is 755 units and its 95% interval includes zero: no reliable
difference.

## What was compared

- **Scores**: the stored per-row test scores of the two champions, ten
  seeds each: ULB CatBoost (F166) and IEEE-CIS LightGBM (F174). Each
  file's SHA-256 was checked against its outcome block, and the rebuilt
  test labels against the stored ones, row for row, before any amount
  was joined. No file was refused.
- **Amounts**: ULB `Amount` (its unit is not stated in its source);
  IEEE-CIS `TransactionAmt`, read as US dollars.
- **Rankings**: (1) by score, today's; (2) by score times amount, the
  expected loss of Hoppner et al.'s rule (EvidenceBasedDB
  `hoppner-instance-threshold`, high). Both flag the same number of
  rows: 284 on ULB, 427 on IEEE-CIS. Scores are used as given, not
  recalibrated.
- **Check first**: a built case where ranking (2) must catch more
  dollars (it caught 1,000 against 10), and a label vector with one
  label flipped, which the join refused. Both fired.

## What it found

- **IEEE-CIS**: dollars caught, mean over seeds (95% t interval):
  - by score: $34,675 ($32,485 to $36,865);
  - by expected loss: $140,832 ($136,567 to $145,098);
  - the paired gain: $106,157 ($101,562 to $110,753). Every seed gains.
- **ULB**: by score 9,546 units, by expected loss 10,301; the paired
  gain is 755 (-50 to 1,561). Six seeds lose 7 to 32 units; four gain
  679 to 2,816. The large gains come from a few high-amount frauds.
- **The cost of the trade**: at a fixed alert count both rankings pay
  the same review cost, so the review cost changes net savings, not the
  order. On IEEE-CIS seed 42, at $10 a review, net savings are $28,504 by
  score and $136,866 by expected loss.
- **Hoppner's own rule raises far more alerts**: on IEEE-CIS seed 42,
  s x A > c gives 8,528, 4,618 and 1,943 alerts at review costs of $5,
  $10 and $25, against the budget's 427. The scores are not calibrated
  probabilities, so these counts are an upper reading, not a staffing
  figure.

## What it means

- A bank weighs fraud by the money it loses. On IEEE-CIS, the measure
  this repository has used (frauds caught at 0.5%) and the bank's
  measure (dollars caught at the same review count) rank the same model
  very differently. A comparison of a quantum lane against a classical
  one should report both.
- The ULB result shows the gain depends on the data: where amounts are
  small and the frauds few, ranking by amount moves little and can lose.
- Not tested here: calibrated scores, a review cost that grows with the
  amount, or a budget set in dollars rather than alerts.

## Outcome blocks

Each seed's row carries two blocks (`outcome_by_score`,
`outcome_by_expected_loss`): the confusion counts at the budget and the
scores' file with its SHA-256.
