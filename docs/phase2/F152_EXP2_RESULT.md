# Experiment 2 (F152): temporal validity on IEEE-CIS, the result

Sprint 28 Task B (#49), 2026-10-22. Zero metered seconds. The entry is
`experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "Experiment 2",
committed before any Phase 2 score on IEEE-CIS's rolling-origin folds
(`cec20d6`). F109 had scored other lanes (GAM, GA2M, HGB, JOINT) on an
IEEE-CIS subsample on 2026-10-18 (corrected 2026-11-18, Sprint 33 D9). Every figure
below is in `experiments/phase2/results/f152_exp2.json` (five model seeds,
42-46, three rolling-origin folds); the two-seed pilot is
`f152_exp2_pilot.json`. Code: `experiments/phase2/src/f152_exp2_score.py`;
test: `experiments/src/test_f152_exp2_score.py`. Evidence tag `SIM`.

Every claim here carries the entry's limit: **trained on drifting
features.** The adversarial control stopped at its 20-round cap on every
fold, with early-versus-late AUC still 0.94 (month 4) and 0.89 (months 5
and 6).

## BLUF

- **P1 holds.** XGBoost beats logistic regression on floor-normalized
  AUPRC on both full months. Month 4: +0.106, 97.5% interval [+0.089,
  +0.123]. Month 5: +0.359 [+0.341, +0.378].
- **P2: XGBoost improves from month 4 to month 5**, by +0.038 [+0.010,
  +0.069]. The entry asked how much a strong lane loses; it gains. The
  change mixes drift with one more month of training rows (410,600 to
  495,902) and a re-selected feature set, so it is not a drift effect
  alone.
- **XGBoost is not the strongest lane here.** LightGBM leads on every
  month, and F151's stable HGB beats XGBoost on every month (secondary,
  uncorrected, each interval excluding zero). Only "trees beat logistic
  regression" is tested and holds; the order among tree lanes is not
  ULB's.

## The pilot check (run first)

LightGBM on month 4, seeds 42 and 43: the paired interval between the
seeds was [-0.0012, +0.0099] and included zero (`f152_exp2_pilot.json`),
so the bootstrap is not too narrow for seed
noise. The full run then started.

## Results (Measured, `SIM`)

Floor-normalized AUPRC, mean over five seeds (raw AUPRC and AUROC per
lane, month and seed are in the result file, each with its outcome
block):

- **Month 4**: LightGBM 0.526, HGB 0.499, XGBoost 0.443, logistic 0.337.
- **Month 5**: LightGBM 0.536, HGB 0.496, XGBoost 0.481, logistic 0.122.
- **Month 6** (secondary, 8,111 rows): LightGBM 0.616, HGB 0.552,
  XGBoost 0.527, logistic 0.418.
- **Seed spread**: tree lanes' SD across seeds is 0.004 to 0.013;
  logistic regression is deterministic (SD 0).
- **Against Phase 1** (`experiments/results/ieee_classical.json`, one
  seed, same folds): Phase 1's XGBoost and LightGBM raw AUPRC sit within
  0.021 of this run's five-seed means on every month (within 0.003 for
  LightGBM). The folds and configurations reproduce, to within one seed's
  scatter.

## Reading

- **Logistic regression collapses on month 5** (0.337 to 0.122), while
  every tree lane holds or improves. It is the lane P1 measures against,
  so P1's month-5 margin is mostly the logistic lane's fall. P1 holds on
  month 4 alone as well.
- **The P2 change is not a drift estimate (Inferred).** Each fold trains
  on every earlier month, and the controls re-select features per fold.
  Separating drift from training size would need a fixed training window,
  which the entry did not specify.
- **HGB above XGBoost** matters for the comparators elsewhere in Phase 2:
  on IEEE-CIS, Phase 1's XGBoost configuration is not the strongest
  classical bar. Whether a tuned XGBoost closes the gap is not tested
  here.

## What this does not settle

- No CVQBoost proxy lane (Decision 2).
- GAM, GA2M and the JOINT twin stay on the card, unsized on 180-plus
  features.
- One dataset, three folds from one six-month file.
