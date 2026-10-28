# SVM on ULB: best achievable result (F166)

**BLUF.** Tuned on validation and scored on the test fold over 10 seeds (42-51), SVM reaches a mean test AUPRC of 0.7419 (95% t interval 0.7208 to 0.7630). It is number 6 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [ULB_COMPARISON.md](ULB_COMPARISON.md).

- **Card**: F166 (Sprint 29 Task F, #69), the ULB part of F157.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F166", written before any score.
- **Evidence**: `experiments/phase2/results/f166_ulb_algorithms.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f166_ulb_algorithms.py`. Every figure below comes from that file. The per-row test scores and the outcome block for each seed are in the file's rows.
- **Data**: ULB with duplicates dropped, `data.stratified_split` (60/20/20). Tuning reads the training and validation folds; every score here is on the test fold.
- **Setup**: `LinearSVC` on all training rows, scores from `decision_function`, all 30 columns standardized on the training fold.

## Configurations tried

8 configurations, named in the entry before any score. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| C 0.001, class_weight None | 1 of 10 |
| C 0.001, class_weight balanced | 0 of 10 |
| C 0.01, class_weight None | 2 of 10 |
| C 0.01, class_weight balanced | 0 of 10 |
| C 0.1, class_weight None | 0 of 10 |
| C 0.1, class_weight balanced | 0 of 10 |
| C 1.0, class_weight None | 7 of 10 |
| C 1.0, class_weight balanced | 0 of 10 |

No seed chose `class_weight` balanced.

## Alternative tried: an RBF kernel

An RBF SVM (`SVC`, `gamma="scale"`, C 1 and 10) on a stratified 20,000-row subsample of the training fold, because an RBF kernel on the full fold is quadratic in rows. The entry keeps it only if its best validation AUPRC beats the linear form's on a majority of seeds. It did so on 2 of 10 seeds, so the lane keeps the **linear** form. Every figure in this document is the linear form.

## Test-fold results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.7419 | 0.0295 | 0.7208 to 0.7630 |
| AUPRC, floor-normalized | 0.7414 | 0.0295 | 0.7203 to 0.7626 |
| ROC-AUC | 0.9688 | 0.0136 | 0.9591 to 0.9786 |
| Recall at the 0.5% budget, test fold | 0.8474 | 0.0315 | 0.8248 to 0.8699 |
| Train-test AUPRC gap | 0.0190 | 0.0305 | -0.0028 to 0.0409 |

At the max-F1 threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.8492 | 0.0392 | 0.8212 to 0.8773 |
| Recall | 0.7632 | 0.0311 | 0.7409 to 0.7854 |
| Specificity | 0.9998 | 0.0001 | 0.9997 to 0.9998 |
| F1 | 0.8029 | 0.0183 | 0.7898 to 0.8160 |
| MCC | 0.8042 | 0.0185 | 0.7910 to 0.8175 |
| Balanced accuracy | 0.8815 | 0.0155 | 0.8704 to 0.8926 |

At the 0.5% alert-budget threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.2718 | 0.0198 | 0.2577 to 0.2860 |
| Recall | 0.8495 | 0.0333 | 0.8256 to 0.8733 |
| Specificity | 0.9962 | 0.0004 | 0.9959 to 0.9964 |
| F1 | 0.4116 | 0.0242 | 0.3943 to 0.4289 |
| MCC | 0.4790 | 0.0225 | 0.4629 to 0.4951 |
| Balanced accuracy | 0.9228 | 0.0166 | 0.9109 to 0.9347 |

## Confusion counts per seed, test fold

TP, FP, TN and FN at each validation-chosen threshold.

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN |
|---|---|---|---|
| 42 | C 1.0, class_weight None | 73 / 10 / 56641 / 22 | 83 / 199 / 56452 / 12 |
| 43 | C 1.0, class_weight None | 69 / 7 / 56644 / 26 | 80 / 193 / 56458 / 15 |
| 44 | C 1.0, class_weight None | 70 / 10 / 56641 / 25 | 81 / 224 / 56427 / 14 |
| 45 | C 1.0, class_weight None | 74 / 9 / 56642 / 21 | 81 / 215 / 56436 / 14 |
| 46 | C 1.0, class_weight None | 76 / 14 / 56637 / 19 | 80 / 185 / 56466 / 15 |
| 47 | C 1.0, class_weight None | 74 / 18 / 56633 / 21 | 81 / 238 / 56413 / 14 |
| 48 | C 0.01, class_weight None | 77 / 20 / 56631 / 18 | 88 / 235 / 56416 / 7 |
| 49 | C 0.01, class_weight None | 73 / 14 / 56637 / 22 | 79 / 219 / 56432 / 16 |
| 50 | C 0.001, class_weight None | 68 / 12 / 56639 / 27 | 77 / 246 / 56405 / 18 |
| 51 | C 1.0, class_weight None | 71 / 17 / 56634 / 24 | 77 / 219 / 56432 / 18 |

## Limits

- Each validation fold holds about 95 frauds, so validation AUPRC is noisy and the chosen configuration changes between seeds.
- One protocol and one grid per algorithm. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

