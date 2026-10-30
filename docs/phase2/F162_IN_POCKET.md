# F162: Inside the SPECTRA Pocket, CVQBoost Proxy Against HGB and XGBoost

**Sprint 28 Task M (#59).** Zero metered seconds. Entry:
`experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F162", committed
before any score (`9b7f770`). Result:
`experiments/phase2/results/f162_in_pocket.json` (evidence tag `SIM`), from
`experiments/phase2/src/f162_in_pocket.py` at `d1c83ee` (recorded in
`provenance`, generator clean).

## Bottom line

- **The proxy is not reliably better than either classical model inside
  the pocket on any cell.** None of the six primary comparisons reads
  "proxy above", so the entry's falsifier fires on all three cells.
  **Measured**: `analysis.cells_with_proxy_above` is empty.
- **Where a difference is reliable, the proxy is below.** Inside the
  pocket, XGBoost beats the proxy on energy_steel (by 0.024 AUPRC,
  Wilcoxon p = 0.0020) and on oilgas_gasturbine (by 0.011, p = 0.0059),
  both under the family level 0.0083. **Measured**: `analysis.primary`.
- **telecom_churn is the one cell where the proxy is ahead on average,
  and it is not reliable.** Proxy minus HGB +0.013 (p = 0.16), proxy minus
  XGBoost +0.033 (p = 0.049); both intervals span zero. The pocket holds
  46 to 58 frauds per seed. **Measured**.
- **The FourierWall2 single-run wins do not repeat.** That run had the
  proxy above XGBoost in the pocket on all three cells (+0.091, +0.018,
  +0.021 AUPRC; `spectra_segment.py`, frozen cells comment). Over ten
  seeds, two of those three reverse reliably and the third is not
  reliable. **Inferred**: one stochastic run sits inside the seed-to-seed
  spread. The leading alternative not ruled out: FourierWall2's XGBoost
  settings and split differ from ours, and are not on record here.
- **For a device run**: nothing here justifies one. The entry's rule
  needs a "proxy above" on a cell. This bears on F161's "valuable"
  condition.

## Results (Measured, `SIM`)

Ten seeds (42-51): seed 42 took 3.1 minutes on the three cells, which
projected 31 minutes against the 120-minute cap (`seed_choice`). 90 rows,
each with an outcome block. Wall time about 28.5 minutes, **unverified**:
the result file does not record it (corrected 2026-10-26, F164: this
said "Recorded"). The rows' `seconds` sum to 20.5 minutes of lane time.

**Primary: in-pocket AUPRC, proxy minus each classical model** (mean over
ten seeds; Wilcoxon exact two-sided; t interval at 99.17%, the family
level for m = 6):

- telecom_churn
  - proxy minus HGB: +0.013, p = 0.160, [-0.019, +0.044]. No reliable
    difference.
  - proxy minus XGBoost: +0.033, p = 0.049, [-0.011, +0.078]. No reliable
    difference.
- energy_steel
  - proxy minus HGB: -0.020, p = 0.0098, [-0.036, -0.003]. **No reliable
    difference under the rule**: the interval excludes zero but the
    Wilcoxon p is above 0.0083. Reported as the rule reads it.
  - proxy minus XGBoost: -0.024, p = 0.0020, [-0.038, -0.011]. **Proxy
    below.**
- oilgas_gasturbine
  - proxy minus HGB: -0.001, p = 0.557, [-0.008, +0.006]. No reliable
    difference.
  - proxy minus XGBoost: -0.011, p = 0.0059, [-0.021, -0.001]. **Proxy
    below.**

**Mean AUPRC by lane, inside the pocket and overall** (`analysis.secondary`):

- telecom_churn: pocket proxy 0.795, HGB 0.783, XGBoost 0.762; overall
  proxy 0.726, HGB 0.873, XGBoost 0.862.
- energy_steel: pocket proxy 0.935, HGB 0.955, XGBoost 0.959; overall
  proxy 0.916, HGB 0.957, XGBoost 0.964.
- oilgas_gasturbine: pocket proxy 0.781, HGB 0.782, XGBoost 0.792;
  overall proxy 0.840, HGB 0.873, XGBoost 0.872.

**Secondary, uncorrected**:

- Per-seed paired bootstrap on in-pocket AUPRC (`pairs[].bootstrap`):
  telecom_churn proxy above XGBoost with the interval excluding zero on 4
  of 10 seeds, below on none; energy_steel proxy below HGB on 8 seeds and
  below XGBoost on 9; oilgas_gasturbine proxy below XGBoost on 4.
- In-pocket ROC-AUC and floor-normalized AUPRC point the same way on every
  cell (`*_pocket_auc_roc_mean`, `*_pocket_auprc_normalized_mean`).
- Train-test AUPRC gap, mean: the proxy's is the largest on every cell
  (0.274 on telecom_churn against 0.126 for HGB; 0.160 on
  oilgas_gasturbine against 0.048).

## Reading

- **Overall, the proxy is below both classical models on every cell**, as
  F100 found for HGB. Inside the pocket it closes most of that gap on
  telecom_churn and oilgas_gasturbine, but it does not pass them.
  **Measured** (the lane means above).
- **telecom_churn is where a pocket-specific edge could still exist.**
  The mean favors the proxy against both models and no seed's bootstrap
  favors XGBoost. Six primary tests over ten seeds cannot resolve +0.03
  on a pocket of about 50 frauds. **Inferred**: a telecom-only entry
  (m = 2, more seeds) is what would decide it; that is a new card, not a
  re-reading of this one.
- **The device result agrees with the proxy here.** Phase 1's B4 on
  Dirac-3 gave in-pocket AUPRC 0.787 on oilgas_gasturbine
  (`b4_hardware.json`, five seeds); the proxy here gives 0.781 over ten.
  Different seeds and an unseeded Phase 1 pool, so this is a consistency
  check, not a pairing.

## Limits

- **XGBoost at library defaults** (xgboost 3.4.1). A tuned XGBoost could
  move the classical side up; the entry chose defaults because the Phase
  1 tuned parameters were tuned on ULB.
- **One proxy configuration**: the frozen cell's (schedule 3, `dct`
  learners, lambda = 2 x n_train), seeded. Other pools (F124's leaf
  regularization, F130's KNN) were not run here.
- **The proxy, not the device.** The device's weights differ from the
  proxy's (weight cosine 0.83-0.90 at these sizes, Phase 1 B4).
- **Label `target` only.** `target_real` is the alternate task the
  authors name; not run.

## What this changes

- F161 (the B4 re-run on Dirac-3S) gains no support from the pocket: no
  cell clears the entry's bar for a device block.
- The reply draft to the SPECTRA authors can report the ten-seed
  head-to-head under their protocol.
