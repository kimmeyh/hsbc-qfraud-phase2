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
  reference).
- `hgb_no_es` (HGB, F108's settings, early stopping off): recovered on 4
  of 5 seeds on the main arm, 5 of 5 on the flip arm and 4 of 5 on the
  reference arm.

## What the rule does not show

- **The attribution is weaker than the preset sentence.** HGB without
  early stopping passes at the minimum, 4 of 5. On the reference arm,
  seed 44, it estimates 0.00431 against a Bayes error of 0, which is the
  F108 failure shape (`F108_CEILING_VALIDATION.md`, "HGB fails the
  reference"). LightGBM with 4,095 bins recovers on every seed and arm.
  Reasonable inference, not tested: removing early stopping fixes most of
  HGB's failure, and the finer bins fix the rest.
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
  as F114's plug-in, because it is the only estimator that recovers on
  every seed and arm.
