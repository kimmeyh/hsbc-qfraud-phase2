# CatBoost on SPECTRA telecom_churn: best achievable result (F157)

**BLUF.** Tuned on validation and scored on the test fold over 10 seeds (42-51), CatBoost reaches a mean test AUPRC of 0.8727 (95% t interval 0.8596 to 0.8857). It is number 1 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [TELECOM_CHURN_COMPARISON.md](TELECOM_CHURN_COMPARISON.md).

- **Card**: F157 (Sprint 31 Task F, #98), the SPECTRA part: F166's algorithms and grids on SPECTRA's four datasets.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F157 SPECTRA part", written before any score.
- **Amendment**: the SVM lane is the form the entry's rule keeps, scored on the test fold under the entry's amendment of 2026-11-05 (Sprint 31 D14 option 1). The first result, `experiments/phase2/results/f157_spectra_algorithms.json`, is kept as recorded; it scored the linear form only.
- **Evidence**: `experiments/phase2/results/f157_spectra_algorithms_rbf.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f157_spectra_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: SPECTRA `telecom_churn`, label `target`, spectra_segment.spectra_split 60/20/20, seeded. Tuning reads the training and validation folds; every score here is on the test fold (630 rows, 152 to 153 positives per seed; 17 feature columns).

## Configurations tried

8 configurations, F166's grid, imported unchanged. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| depth 4, l2_leaf_reg 3, learning_rate 0.05 | 0 of 10 |
| depth 4, l2_leaf_reg 10, learning_rate 0.05 | 0 of 10 |
| depth 4, l2_leaf_reg 3, learning_rate 0.1 | 0 of 10 |
| depth 4, l2_leaf_reg 10, learning_rate 0.1 | 0 of 10 |
| depth 6, l2_leaf_reg 3, learning_rate 0.05 | 4 of 10 |
| depth 6, l2_leaf_reg 10, learning_rate 0.05 | 1 of 10 |
| depth 6, l2_leaf_reg 3, learning_rate 0.1 | 5 of 10 |
| depth 6, l2_leaf_reg 10, learning_rate 0.1 | 0 of 10 |

## Test-fold results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.8727 | 0.0182 | 0.8596 to 0.8857 |
| AUPRC, floor-normalized | 0.8321 | 0.0240 | 0.8149 to 0.8493 |
| ROC-AUC | 0.9495 | 0.0083 | 0.9435 to 0.9555 |
| Recall at the 0.5% budget, test fold | 0.0263 | 0.0001 | 0.0262 to 0.0263 |
| Train-test AUPRC gap | 0.1259 | 0.0167 | 0.1140 to 0.1378 |

Secondary, as the entry reports it: test AUPRC inside the pocket (`in_pocket` = 1) 0.7664 (95% t interval 0.7324 to 0.8003, 10 seeds) and outside it 0.9151 (0.9081 to 0.9222, 10 seeds).

At the max-F1 threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.7727 | 0.0551 | 0.7333 to 0.8121 |
| Recall | 0.8089 | 0.0354 | 0.7836 to 0.8342 |
| Specificity | 0.9217 | 0.0292 | 0.9008 to 0.9426 |
| F1 | 0.7883 | 0.0200 | 0.7739 to 0.8026 |
| MCC | 0.7204 | 0.0280 | 0.7003 to 0.7404 |
| Balanced accuracy | 0.8653 | 0.0093 | 0.8586 to 0.8720 |

At the 0.5% alert-budget threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 1.0000 | 0.0000 | 1.0000 to 1.0000 |
| Recall | 0.0217 | 0.0120 | 0.0131 to 0.0303 |
| Specificity | 1.0000 | 0.0000 | 1.0000 to 1.0000 |
| F1 | 0.0422 | 0.0229 | 0.0258 to 0.0585 |
| MCC | 0.1240 | 0.0359 | 0.0983 to 0.1497 |
| Balanced accuracy | 0.5108 | 0.0060 | 0.5065 to 0.5151 |

## Confusion counts per seed, test fold

TP, FP, TN and FN at each validation-chosen threshold, and at the test fold's own 0.5% budget (the comparison page's recall).

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN | 0.5% budget on the test fold: TP / FP / TN / FN |
|---|---|---|---|---|
| 42 | depth 6, l2_leaf_reg 3, learning_rate 0.1 | 116 / 26 / 452 / 36 | 4 / 0 / 478 / 148 | 4 / 0 / 478 / 148 |
| 43 | depth 6, l2_leaf_reg 3, learning_rate 0.05 | 127 / 46 / 432 / 25 | 6 / 0 / 478 / 146 | 4 / 0 / 478 / 148 |
| 44 | depth 6, l2_leaf_reg 3, learning_rate 0.1 | 124 / 41 / 437 / 28 | 2 / 0 / 478 / 150 | 4 / 0 / 478 / 148 |
| 45 | depth 6, l2_leaf_reg 3, learning_rate 0.1 | 123 / 43 / 434 / 30 | 6 / 0 / 477 / 147 | 4 / 0 / 477 / 149 |
| 46 | depth 6, l2_leaf_reg 3, learning_rate 0.1 | 135 / 69 / 408 / 18 | 2 / 0 / 477 / 151 | 4 / 0 / 477 / 149 |
| 47 | depth 6, l2_leaf_reg 3, learning_rate 0.05 | 122 / 24 / 453 / 31 | 2 / 0 / 477 / 151 | 4 / 0 / 477 / 149 |
| 48 | depth 6, l2_leaf_reg 10, learning_rate 0.05 | 120 / 34 / 444 / 32 | 3 / 0 / 478 / 149 | 4 / 0 / 478 / 148 |
| 49 | depth 6, l2_leaf_reg 3, learning_rate 0.05 | 126 / 40 / 438 / 26 | 1 / 0 / 478 / 151 | 4 / 0 / 478 / 148 |
| 50 | depth 6, l2_leaf_reg 3, learning_rate 0.1 | 123 / 23 / 455 / 29 | 5 / 0 / 478 / 147 | 4 / 0 / 478 / 148 |
| 51 | depth 6, l2_leaf_reg 3, learning_rate 0.05 | 116 / 28 / 450 / 36 | 2 / 0 / 478 / 150 | 4 / 0 / 478 / 148 |

## Limits

- One protocol and one grid per algorithm, F166's. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

