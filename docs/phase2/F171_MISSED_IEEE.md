# F171: does the group every model misses shrink on IEEE-CIS?

Sprint 30 Task H (#82). Evidence (SIM, 0 metered seconds):
- `experiments/phase2/results/f171_missed_ieee.json`, generator
  `experiments/phase2/src/f171_missed_ieee.py`: the preregistered count
  at the 0.5% alert budget, and the raw-field profile.
- `experiments/phase2/results/f171_budgets.json`, generator
  `experiments/phase2/src/f171_budgets.py`: the POST HOC budgets added by
  Decision D7, option 1.

Entry: "F171" in `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6
(f74125d), and its 2026-10-31 amendment, written after the 0.5% result
was seen and before the new budgets were counted.

## Result

**Not shown. At every budget, a larger share of IEEE-CIS frauds is
missed by all families than of ULB frauds, but the counts compare 4
IEEE-CIS families with 12 ULB families.** The entry's reading ("a share
well below ULB's is consistent with richer information catching
frauds") is not met. More families flag more distinct frauds, so the
gap is not shown to come from the data. The like-for-like row is the
matched budget, 18.2% against 11.2%. The 3.5% row is about one times
IEEE-CIS's fraud rate and many times ULB's, so it is tight on one
dataset and loose on the other.

Share of (fold, seed, test fraud) pairs that no family flags. IEEE-CIS:
F152's 4 families, months 4-6, seeds 42-46, 31,220 pairs. ULB: F158 step
3's 12 on-split families, seeds 42-51, 950 pairs.

| Budget | IEEE-CIS missed | ULB missed | IEEE-CIS capacity floor |
|---|---|---|---|
| 0.5% (preregistered) | 81.5% | 11.2% | 42.3% |
| 3.5% (post hoc) | 38.1% | 5.4% | 0% |
| three times fold fraud rate (post hoc) | 18.2% (mean budget 11.1%) | 11.2% (budget 0.5%) | 0% |

- **The 0.5% count measures the budget.** On IEEE-CIS month 4, each
  family has 427 alerts for 2,962 frauds. Four families with no overlap
  could flag at most 1,708, so 1,254 frauds (42%) are missed before any
  model is scored. The capacity floor column shows this share for each
  budget.
- **The matched budget is the like-for-like comparison.** At three times
  each fold's fraud rate, the strictness ULB's 0.5% has, IEEE-CIS misses
  18.2% and ULB 11.2%. On ULB the matched budget equals 0.5%, so the ULB
  count does not change.
- The 0.5% count was recomputed by the budget module and equals the
  recorded F171 and F158 counts.
- Per month at 0.5%: 81.0% (month 4), 81.9% (month 5), 82.8% (month 6).

## Profile (0.5% budget, as preregistered)

Missed against caught frauds on raw fields; 5,264 distinct rows are
missed in some seed. The caught group is the rows caught in some seed,
and the months are fixed across seeds, so a row missed in one seed and
caught in another is in BOTH groups: the two are not disjoint, and the
result records neither group's size nor the overlap (PR 74 review).
F170's rule (missed in every seed against caught in every seed, mixed
rows left out) was not applied here:
- ProductCD W: 53.0% of missed rows, 7.5% of caught rows. ProductCD C:
  32.5% against 73.2%.
- DeviceType missing: 55.4% of missed, 8.5% of caught. Desktop: 21.0%
  against 56.9%.
- C1 median 2 missed, 14 caught; TransactionAmt median 77 against 49.

At 0.5% the caught group is the top of each family's ranking, so the
profile shows what the top 0.5% looks like, more than what models cannot
see. It was not recomputed at the post hoc budgets.

## What the result does not show

- **Descriptive, not causal, as the entry sets.** The datasets differ in
  more than feature richness: IEEE-CIS's fraud rate is about 20 times
  ULB's, its split is by month, and its labels mark linked transactions.
- **Family count differs.** ULB has 12 families and IEEE-CIS 4. More
  families flag more distinct rows, so ULB's share is lowered by its
  family count. A 4-family ULB count was not computed.
- The post hoc budgets are exploratory. They were chosen after the 0.5%
  result was seen.

## What it changes

- Richer raw fields did not, on this count, leave fewer frauds that every
  model misses. F174's tuned IEEE-CIS lanes are the next reference: a
  stronger model set could lower the IEEE-CIS share.
- Cross-dataset reads of alert-budget counts use a budget tied to each
  dataset's fraud rate. The 0.5% budget in every outcome block (F154)
  is unchanged.
