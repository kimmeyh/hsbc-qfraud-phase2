# F151: Why the ULB HGB Comparator Was Unstable

**Sprint 28 Task A (#48).** Zero metered seconds. Result:
`experiments/phase2/results/f151_hgb_cause.json` (evidence tag `SIM`), from
`experiments/phase2/src/f151_hgb_cause.py`.

## Bottom line

- **The cause is HGB's default `l2_regularization=0`.** Setting it to 1.0,
  and changing nothing else, closes the spread under the rule the plan
  fixed before the run: mean 0.804, SD 0.022, range 0.055, within 0.03 of
  Phase 1's XGBoost matched13 (0.816). The default fails it: mean 0.375,
  SD 0.170, range 0.480. **Measured**: `summary.l2_1p0` and
  `summary.default`.
- **The stable ULB HGB reference is `HistGradientBoostingClassifier(
  l2_regularization=1.0)`, other settings at their defaults**, on F130's
  preparation (`qubo_proxy._prep(seed, 13)`), seeds 42-46. Later tasks
  that need an HGB on ULB use it (Sprint 28 Tasks B, D and G).
- **F130's voided ULB reading reverses.** Against the stable HGB, both of
  F130's CVQBoost proxy variants are below it: KNN by 0.027 (95% interval
  -0.046 to -0.008), the dct baseline by 0.036 (-0.047 to -0.026).
  F130's "beats HGB" came from a broken comparator. **Measured**:
  `f130_restated.variants`.

## The controlled changes

Five seeds, F130's exact preparation (deduplicated ULB, 60/20/20
stratified, 13 mutual-information features). One setting moved per
variant; the last combines the two single moves.

| Variant | Setting moved | Mean AUPRC | SD | Range | Closes |
|---|---|---|---|---|---|
| default | none | 0.375 | 0.170 | 0.480 | no |
| l2_0p1 | `l2_regularization=0.1` | 0.766 | 0.034 | 0.092 | no (SD) |
| **l2_1p0** | **`l2_regularization=1.0`** | **0.804** | **0.022** | **0.055** | **yes** |
| no_early_stopping | `early_stopping=False` | 0.219 | 0.020 | 0.052 | no (level) |
| l2_1p0_no_early_stopping | both | 0.806 | 0.022 | 0.062 | yes |

All values from `summary` in the result file. The rule: SD at most 0.03,
range at most 0.10, and mean within 0.03 of the XGBoost matched13
reference on the same seeds.

## Mechanism

- **Inferred**: with no L2 term, a leaf's value is about -G / H. At 0.17%
  prevalence a leaf holding mostly frauds has a tiny Hessian sum, so its
  value is very large. The default's early stopping then halts almost at
  once: it ran 10 or 11 iterations on every seed (`summary.default.n_iter`),
  against 35-89 with `l2_regularization=1.0`. Without early stopping and
  without L2, 100 iterations give a stable but poor model (0.219), which
  fits overshooting leaves.
- **The dose follows**: 0.1 nearly closes the spread (SD 0.034); 1.0
  closes it.
- **Leading alternative not ruled out**: a larger `min_samples_leaf`,
  which also limits small leaves. A scratch probe before the plan
  (`min_samples_leaf=200`) stayed unstable (SD 0.246), but that probe is
  not recorded evidence.

## What this corrects

- **The card's "unstable under every setting tried"** was wrong for "no
  early stopping", which was stable at the wrong level. The plan's level
  term exists for that case.
- **F109's "HGB strongest on ULB"** used ROC-AUC on a 30,000-row
  subsample, not AUPRC, so it cannot be set against F130 or this result.
  On this preparation the default is unstable on ROC-AUC too (0.30-0.86
  over the five seeds; `rows[].test_auc_roc`), so F109's subsample, with
  early stopping on at 30,000 rows, may have been affected. **Unverified**:
  F109 was not re-run.
- **F106's HGB twin** ran on 6,295 rows, where early stopping is off by
  default, and was not affected the same way (its SD was 0.027).

## Recording

Every row carries an outcome block (F154 standing rule): confusion counts
at the 0.5% alert budget and at the two validation-chosen operating
points, and the per-row test scores in `experiments/phase2/predictions/`
(gitignored; regenerable for free) with their SHA-256.
