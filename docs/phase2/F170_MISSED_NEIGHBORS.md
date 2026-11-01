# F170: are the ULB frauds that every model misses among legitimate rows?

Sprint 30 Task G (#81). Evidence: `experiments/phase2/results/f170_missed_neighbors.json`
(SIM, 0 metered seconds), generator `experiments/phase2/src/f170_missed_neighbors.py`.
Entry: "F170" in `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6,
committed before the module existed (f74125d).

## Result

**Yes. The reading set in the entry is "consistent with ULB's information
limit".** For each ULB test fraud the measure is the share of legitimate
rows among its 10 nearest training rows (Euclidean, on the 30 features
standardized on the training rows). The 12 on-split families of F158 step 3,
seeds 42-51, are compared.

- **Simulator check (F108's world, seed 42) fired first.** Frauds that the
  Bayes classifier calls legitimate (3,720 of 5,103) sit among more
  legitimate rows than the rest (median share 1.0 against 0.0; two-sided
  Mann-Whitney U rejects). The comparison can detect a known information
  limit, so the ULB reading is made.
- **Primary test, distinct frauds.** 36 frauds are missed by every family
  in every seed in which they are test rows, and 370 are caught by some
  family in every such seed. Median legitimate share: 1.0 missed, 0.1 caught. Every missed
  fraud has mostly legitimate neighbors; 16.2% of caught frauds do. U
  rejects at alpha 0.05 (p below 1e-20), direction "higher".
- **Secondary, (seed, fraud) pairs.** 106 missed and 844 caught pairs; the
  same direction (p below 1e-57).
- 12 distinct frauds are missed in some seeds and caught in others
  ("mixed"); they are outside the primary test, as the entry sets.

## What the result does not show

- **Consistent with, not proof of, an information limit.** The neighbors
  are measured in the same 30 features the models use. A fraud whose 10
  nearest rows are all legitimate is hard for any model in that space. A
  different transform, or a feature ULB does not carry, could still
  separate it. The test shows where the missed frauds sit, not that no
  model could catch them.
- **The cvqboost hardware-mixed family is off split** for all 10 seeds and
  is not used (as in F158).

## What it changes

- F158 step 3 compared group means. Here the comparison is per row and
  tested. The result is consistent with reading ULB's missed-by-all
  group as a data limit, not proof of it. The neighbor share is in
  effect a 10-nearest-neighbor score in the same 30 features the models
  use, so the result also fits "every model in this feature space misses
  the same frauds" (inferred). F171 asks the same
  question on IEEE-CIS, which has richer raw fields.
