# F169: the F108 plug-in with estimators set for extreme imbalance

Sprint 30 Task F (#80). Evidence: `experiments/phase2/results/f169_plugin_bins.json`
(SIM, 0 metered seconds), generator `experiments/phase2/src/f169_plugin_bins.py`.
Entry: the 2026-10-31 amendment to "F108" in
`experiments/phase2/PREREGISTRATION_DRAFT.md` section 6 (Decision D3,
option 1), committed before the module existed (f74125d).

## Result

**Both estimators pass F108's rule on the main arm.** The preset reading
is "both pass: early stopping, not bins, was the cause". This is the
first ceiling method to pass F108's harness, after the calibrated plug-in
(Sprint 28) and F156's Henze-Penrose bound (Sprint 29) failed.

- `lgbm_bins` (LightGBM, 4,095 bins, HGB's shape, no early stopping):
  recovered on 5 of 5 seeds on every arm (main, label-flip noise,
  reference). Its reference-arm passes are degenerate; see below.
- `hgb_no_es` (HGB, F108's settings, early stopping off): recovered on 4
  of 5 seeds on the main arm, 5 of 5 on the flip arm and 4 of 5 on the
  reference arm.

## What the rule does not show

- **The attribution is weaker than the preset sentence.** HGB without
  early stopping passes at the minimum, 4 of 5. On the reference arm,
  seed 44, it estimates 0.00431 against a Bayes error of 0, which is the
  F108 failure shape (`F108_CEILING_VALIDATION.md`, "HGB fails the
  reference").
- **LightGBM's reference-arm passes are degenerate.** The reference arm
  has a Bayes error of 0. On seeds 42-45, LightGBM's test AUPRC there is
  0.0006, the arm's fraud rate, so it ranks frauds no better than chance.
  Its plug-in is near 0 because its predicted probabilities are near 0
  on every row, not because it separates the classes (inferred from the
  AUPRC). Only seed 46 learns the arm (AUPRC 0.109). HGB without early
  stopping ranks better there (AUPRC 0.0010 to 0.0126). So the reference
  arm does not show that the finer bins fix HGB's failure. The amendment
  makes the reference arm reported, not decisive; the main-arm pass
  stands.
- **Per-seed margins on the main arm.** LightGBM's estimate is close to
  the Bayes error on each seed (for example seed 42: 0.00609 against
  0.0061). HGB without early stopping overstates it on each seed (seed
  42: 0.00662; seed 46: 0.00664 against 0.00603, not recovered).
- **The rule is F108's.** A pass means the plug-in recovers a known
  Bayes error on F108's simulator. It does not show that the plug-in is
  accurate on ULB or IEEE-CIS, where the Bayes error is unknown.

## What it changes

- F114 depended on a ceiling method that passes F108's harness. That
  dependency is now met. Recommendation for the backlog: use `lgbm_bins`
  as F114's plug-in, because it recovers on 5 of 5 seeds on the main and
  flip arms, against HGB's 4 of 5 on the main arm. Its reference-arm
  passes are not part of that reason (above).
- On the main arm both estimators still rank below the Bayes classifier
  (LightGBM's test AUPRC 0.282 to 0.300 against a Bayes AUPRC of 0.296 to
  0.318). Recovering the Bayes error is not the same as ranking as well
  as the Bayes classifier.
