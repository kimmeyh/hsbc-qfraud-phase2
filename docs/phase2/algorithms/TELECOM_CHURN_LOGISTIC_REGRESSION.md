# Logistic regression on SPECTRA telecom_churn: best result within F166's grid (F157)

**BLUF.** Tuned on validation and scored on the test fold over 10 seeds (42-51), Logistic regression reaches a mean test AUPRC of 0.6509 (95% t interval 0.6305 to 0.6713). It is number 7 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [TELECOM_CHURN_COMPARISON.md](TELECOM_CHURN_COMPARISON.md).

- **Card**: F157 (Sprint 31 Task F, #98), the SPECTRA part: F166's algorithms and grids on SPECTRA's four datasets.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F157 SPECTRA part", written before any score.
- **Amendment**: the SVM lane is the form the entry's rule keeps, scored on the test fold under the entry's amendment of 2026-11-05 (Sprint 31 D14 option 1). The first result, `experiments/phase2/results/f157_spectra_algorithms.json`, is kept as recorded; it scored the linear form only. The amendment was written after that result was seen; the other six lanes are unchanged from it.
- **Evidence**: `experiments/phase2/results/f157_spectra_algorithms_rbf.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f157_spectra_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: SPECTRA `telecom_churn`, label `target`, spectra_segment.spectra_split 60/20/20, seeded. Tuning reads the training and validation folds; every score here is on the test fold (630 rows, 152 to 153 positives per seed; 17 feature columns).

## Configurations tried

8 configurations, F166's grid, imported unchanged. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| C 0.01, class_weight None | 2 of 10 |
| C 0.01, class_weight balanced | 0 of 10 |
| C 0.1, class_weight None | 0 of 10 |
| C 0.1, class_weight balanced | 0 of 10 |
| C 1.0, class_weight None | 1 of 10 |
| C 1.0, class_weight balanced | 0 of 10 |
| C 10.0, class_weight None | 7 of 10 |
| C 10.0, class_weight balanced | 0 of 10 |

No seed chose `class_weight` balanced.

## Test-fold results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.6509 | 0.0286 | 0.6305 to 0.6713 |
| AUPRC, floor-normalized | 0.5396 | 0.0378 | 0.5125 to 0.5666 |
| ROC-AUC | 0.8504 | 0.0112 | 0.8424 to 0.8584 |
| Recall at the 0.5% budget, test fold | 0.0210 | 0.0061 | 0.0167 to 0.0253 |
| Train-test AUPRC gap | 0.0172 | 0.0282 | -0.0030 to 0.0374 |

Secondary, as the entry reports it: test AUPRC inside the pocket (`in_pocket` = 1) 0.5552 (95% t interval 0.5103 to 0.6001, 10 seeds) and outside it 0.7068 (0.6862 to 0.7274, 10 seeds).

At the max-F1 threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.5153 | 0.0245 | 0.4978 to 0.5328 |
| Recall | 0.7854 | 0.1002 | 0.7137 to 0.8571 |
| Specificity | 0.7622 | 0.0443 | 0.7305 to 0.7939 |
| F1 | 0.6188 | 0.0281 | 0.5987 to 0.6388 |
| MCC | 0.4879 | 0.0405 | 0.4589 to 0.5169 |
| Balanced accuracy | 0.7738 | 0.0306 | 0.7519 to 0.7957 |

At the 0.5% alert-budget threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.7898 | 0.2225 | 0.6306 to 0.9489 |
| Recall | 0.0210 | 0.0110 | 0.0131 to 0.0289 |
| Specificity | 0.9979 | 0.0020 | 0.9965 to 0.9993 |
| F1 | 0.0406 | 0.0208 | 0.0257 to 0.0555 |
| MCC | 0.0987 | 0.0385 | 0.0711 to 0.1262 |
| Balanced accuracy | 0.5095 | 0.0053 | 0.5057 to 0.5132 |

## Confusion counts per seed, test fold

TP, FP, TN and FN at each validation-chosen threshold, and at the test fold's own 0.5% budget (the comparison page's recall).

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN | 0.5% budget on the test fold: TP / FP / TN / FN |
|---|---|---|---|---|
| 42 | C 10.0, class_weight None | 127 / 119 / 359 / 25 | 2 / 0 / 478 / 150 | 4 / 0 / 478 / 148 |
| 43 | C 10.0, class_weight None | 125 / 123 / 355 / 27 | 6 / 2 / 476 / 146 | 3 / 1 / 477 / 149 |
| 44 | C 10.0, class_weight None | 136 / 143 / 335 / 16 | 2 / 0 / 478 / 150 | 4 / 0 / 478 / 148 |
| 45 | C 10.0, class_weight None | 111 / 94 / 383 / 42 | 3 / 2 / 475 / 150 | 2 / 2 / 475 / 151 |
| 46 | C 0.01, class_weight None | 93 / 91 / 386 / 60 | 5 / 1 / 476 / 148 | 4 / 0 / 477 / 149 |
| 47 | C 1.0, class_weight None | 131 / 123 / 354 / 22 | 5 / 2 / 475 / 148 | 2 / 2 / 475 / 151 |
| 48 | C 10.0, class_weight None | 117 / 120 / 358 / 35 | 2 / 1 / 477 / 150 | 3 / 1 / 477 / 149 |
| 49 | C 0.01, class_weight None | 127 / 122 / 356 / 25 | 4 / 0 / 478 / 148 | 4 / 0 / 478 / 148 |
| 50 | C 10.0, class_weight None | 133 / 129 / 349 / 19 | 2 / 0 / 478 / 150 | 4 / 0 / 478 / 148 |
| 51 | C 10.0, class_weight None | 96 / 72 / 406 / 56 | 1 / 2 / 476 / 151 | 2 / 2 / 476 / 150 |

## Limits

- One protocol and one grid per algorithm, F166's. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

