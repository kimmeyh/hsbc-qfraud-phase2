# SVM on IEEE-CIS: best achievable result (F174)

**BLUF.** Tuned on month 3 and scored on month 4 over 10 seeds (42-51), SVM reaches a mean test AUPRC of 0.3612 (95% t interval 0.3612 to 0.3612). It is number 6 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [IEEE_COMPARISON.md](IEEE_COMPARISON.md). The ULB page for the same algorithm is [ULB_SVM.md](ULB_SVM.md).

- **Card**: F174 (Sprint 30 Task D, #78), the IEEE-CIS part of F157.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F174", written before any score.
- **Evidence**: `experiments/phase2/results/f174_ieee_algorithms.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f174_ieee_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: IEEE-CIS with exact duplicates dropped (3 rows), F105's month folds and F152's item-4 controls. Tuning fits months 0-2 and chooses on month 3 (98,027 rows); the chosen configuration is fitted again on months 0-3 and scored once on month 4 (85,302 rows). Every score here is on month 4.
- **Setup**: `LinearSVC` on all training rows, scores from `decision_function`, missing values imputed with the training months' medians, then standardized on them.

## Configurations tried

8 configurations, F166's grid, imported unchanged. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| C 0.001, class_weight None | 0 of 10 |
| C 0.001, class_weight balanced | 0 of 10 |
| C 0.01, class_weight None | 0 of 10 |
| C 0.01, class_weight balanced | 0 of 10 |
| C 0.1, class_weight None | 10 of 10 |
| C 0.1, class_weight balanced | 0 of 10 |
| C 1.0, class_weight None | 0 of 10 |
| C 1.0, class_weight balanced | 0 of 10 |

No seed chose `class_weight` balanced.

## Alternative tried: an RBF kernel

An RBF SVM (`SVC`, `gamma="scale"`, C 1 and 10) on a stratified 20,000-row subsample of the tuning months, because an RBF kernel on every row is quadratic in rows. The entry keeps it only if its best validation AUPRC beats the linear form's on a majority of seeds. It did so on 0 of 10 seeds, so the lane keeps the **linear** form. Every figure in this document is the linear form.

## Test-month results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.3612 | 0.0000 | 0.3612 to 0.3612 |
| AUPRC, floor-normalized | 0.3382 | 0.0000 | 0.3382 to 0.3382 |
| ROC-AUC | 0.7884 | 0.0000 | 0.7884 to 0.7884 |
| Recall at the 0.5% budget, test fold | 0.1256 | 0.0000 | 0.1256 to 0.1256 |
| Train-test AUPRC gap | 0.0363 | 0.0000 | 0.0363 to 0.0363 |

SVM gives the same test AUPRC on every seed. It chose the same configuration on every seed, and the months are fixed, so the seed does not change the result. The SD is 0 and the interval has no width: the 10 seeds are one result.

At the max-F1 threshold chosen on the validation month:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.4951 | 0.0000 | 0.4951 to 0.4951 |
| Recall | 0.3261 | 0.0000 | 0.3261 to 0.3261 |
| Specificity | 0.9880 | 0.0000 | 0.9880 to 0.9880 |
| F1 | 0.3932 | 0.0000 | 0.3932 to 0.3932 |
| MCC | 0.3847 | 0.0000 | 0.3847 to 0.3847 |
| Balanced accuracy | 0.6571 | 0.0000 | 0.6571 to 0.6571 |

At the 0.5% alert-budget threshold chosen on the validation month:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.8651 | 0.0000 | 0.8651 to 0.8651 |
| Recall | 0.1472 | 0.0000 | 0.1472 to 0.1472 |
| Specificity | 0.9992 | 0.0000 | 0.9992 to 0.9992 |
| F1 | 0.2516 | 0.0000 | 0.2516 to 0.2516 |
| MCC | 0.3497 | 0.0000 | 0.3497 to 0.3497 |
| Balanced accuracy | 0.5732 | 0.0000 | 0.5732 to 0.5732 |

On the test month this threshold flags 504 of 85,302 test rows; the month's own 0.5% budget is 427 rows. The threshold is chosen on the validation month, so its alert volume on the test month is not the budget. The row "Recall at the 0.5% budget, test fold" above uses the test month's own budget.

## Confusion counts per seed, test month

TP, FP, TN and FN at each threshold chosen on the validation month.

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN |
|---|---|---|---|
| 42 | C 0.1, class_weight None | 966 / 985 / 81355 / 1996 | 436 / 68 / 82272 / 2526 |
| 43 | C 0.1, class_weight None | 966 / 985 / 81355 / 1996 | 436 / 68 / 82272 / 2526 |
| 44 | C 0.1, class_weight None | 966 / 985 / 81355 / 1996 | 436 / 68 / 82272 / 2526 |
| 45 | C 0.1, class_weight None | 966 / 985 / 81355 / 1996 | 436 / 68 / 82272 / 2526 |
| 46 | C 0.1, class_weight None | 966 / 985 / 81355 / 1996 | 436 / 68 / 82272 / 2526 |
| 47 | C 0.1, class_weight None | 966 / 985 / 81355 / 1996 | 436 / 68 / 82272 / 2526 |
| 48 | C 0.1, class_weight None | 966 / 985 / 81355 / 1996 | 436 / 68 / 82272 / 2526 |
| 49 | C 0.1, class_weight None | 966 / 985 / 81355 / 1996 | 436 / 68 / 82272 / 2526 |
| 50 | C 0.1, class_weight None | 966 / 985 / 81355 / 1996 | 436 / 68 / 82272 / 2526 |
| 51 | C 0.1, class_weight None | 966 / 985 / 81355 / 1996 | 436 / 68 / 82272 / 2526 |

## Limits

- The validation month holds about 3,849 frauds, so validation AUPRC is less noisy than on ULB. Here the same configuration (C 0.1, class_weight None) was chosen on every seed.
- One protocol and one grid per algorithm, F166's. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- One test month. Month-to-month drift is outside this result; F152 scores months 4-6.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

