# HGB on SPECTRA telecom_churn: best achievable result (F157)

**BLUF.** Tuned on validation and scored on the test fold over 10 seeds (42-51), HGB reaches a mean test AUPRC of 0.8697 (95% t interval 0.8564 to 0.8829). It is number 3 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [TELECOM_CHURN_COMPARISON.md](TELECOM_CHURN_COMPARISON.md).

- **Card**: F157 (Sprint 31 Task F, #98), the SPECTRA part: F166's algorithms and grids on SPECTRA's four datasets.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F157 SPECTRA part", written before any score.
- **Amendment**: the SVM lane is the form the entry's rule keeps, scored on the test fold under the entry's amendment of 2026-11-05 (Sprint 31 D14 option 1). The first result, `experiments/phase2/results/f157_spectra_algorithms.json`, is kept as recorded; it scored the linear form only.
- **Evidence**: `experiments/phase2/results/f157_spectra_algorithms_rbf.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f157_spectra_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: SPECTRA `telecom_churn`, label `target`, spectra_segment.spectra_split 60/20/20, seeded. Tuning reads the training and validation folds; every score here is on the test fold (630 rows, 152 to 153 positives per seed; 17 feature columns).

## Configurations tried

8 configurations, F166's grid, imported unchanged. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| l2_regularization 0.0, learning_rate 0.05, max_leaf_nodes 15 | 0 of 10 |
| l2_regularization 0.0, learning_rate 0.05, max_leaf_nodes 31 | 1 of 10 |
| l2_regularization 0.0, learning_rate 0.1, max_leaf_nodes 15 | 0 of 10 |
| l2_regularization 0.0, learning_rate 0.1, max_leaf_nodes 31 | 3 of 10 |
| l2_regularization 1.0, learning_rate 0.05, max_leaf_nodes 15 | 0 of 10 |
| l2_regularization 1.0, learning_rate 0.05, max_leaf_nodes 31 | 1 of 10 |
| l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 15 | 0 of 10 |
| l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 31 | 5 of 10 |

## Test-fold results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.8697 | 0.0185 | 0.8564 to 0.8829 |
| AUPRC, floor-normalized | 0.8281 | 0.0245 | 0.8106 to 0.8456 |
| ROC-AUC | 0.9469 | 0.0098 | 0.9399 to 0.9539 |
| Recall at the 0.5% budget, test fold | 0.0263 | 0.0001 | 0.0262 to 0.0263 |
| Train-test AUPRC gap | 0.1281 | 0.0182 | 0.1151 to 0.1412 |

Secondary, as the entry reports it: test AUPRC inside the pocket (`in_pocket` = 1) 0.7769 (95% t interval 0.7477 to 0.8062, 10 seeds) and outside it 0.9108 (0.9014 to 0.9203, 10 seeds).

At the max-F1 threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.7610 | 0.0467 | 0.7276 to 0.7944 |
| Recall | 0.8010 | 0.0438 | 0.7696 to 0.8324 |
| Specificity | 0.9181 | 0.0237 | 0.9012 to 0.9351 |
| F1 | 0.7788 | 0.0256 | 0.7605 to 0.7970 |
| MCC | 0.7075 | 0.0336 | 0.6835 to 0.7315 |
| Balanced accuracy | 0.8596 | 0.0181 | 0.8466 to 0.8725 |

At the 0.5% alert-budget threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 1.0000 | 0.0000 | 1.0000 to 1.0000 |
| Recall | 0.0263 | 0.0161 | 0.0147 to 0.0378 |
| Specificity | 1.0000 | 0.0000 | 1.0000 to 1.0000 |
| F1 | 0.0508 | 0.0302 | 0.0292 to 0.0724 |
| MCC | 0.1358 | 0.0428 | 0.1052 to 0.1665 |
| Balanced accuracy | 0.5131 | 0.0081 | 0.5074 to 0.5189 |

## Confusion counts per seed, test fold

TP, FP, TN and FN at each validation-chosen threshold, and at the test fold's own 0.5% budget (the comparison page's recall).

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN | 0.5% budget on the test fold: TP / FP / TN / FN |
|---|---|---|---|---|
| 42 | l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 31 | 121 / 32 / 446 / 31 | 2 / 0 / 478 / 150 | 4 / 0 / 478 / 148 |
| 43 | l2_regularization 0.0, learning_rate 0.1, max_leaf_nodes 31 | 106 / 26 / 452 / 46 | 4 / 0 / 478 / 148 | 4 / 0 / 478 / 148 |
| 44 | l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 31 | 126 / 48 / 430 / 26 | 4 / 0 / 478 / 148 | 4 / 0 / 478 / 148 |
| 45 | l2_regularization 0.0, learning_rate 0.1, max_leaf_nodes 31 | 122 / 52 / 425 / 31 | 5 / 0 / 477 / 148 | 4 / 0 / 477 / 149 |
| 46 | l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 31 | 131 / 58 / 419 / 22 | 1 / 0 / 477 / 152 | 4 / 0 / 477 / 149 |
| 47 | l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 31 | 127 / 34 / 443 / 26 | 3 / 0 / 477 / 150 | 4 / 0 / 477 / 149 |
| 48 | l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 31 | 117 / 29 / 449 / 35 | 2 / 0 / 478 / 150 | 4 / 0 / 478 / 148 |
| 49 | l2_regularization 1.0, learning_rate 0.05, max_leaf_nodes 31 | 123 / 46 / 432 / 29 | 9 / 0 / 478 / 143 | 4 / 0 / 478 / 148 |
| 50 | l2_regularization 0.0, learning_rate 0.1, max_leaf_nodes 31 | 126 / 27 / 451 / 26 | 3 / 0 / 478 / 149 | 4 / 0 / 478 / 148 |
| 51 | l2_regularization 0.0, learning_rate 0.05, max_leaf_nodes 31 | 121 / 39 / 439 / 31 | 7 / 0 / 478 / 145 | 4 / 0 / 478 / 148 |

## Limits

- One protocol and one grid per algorithm, F166's. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

