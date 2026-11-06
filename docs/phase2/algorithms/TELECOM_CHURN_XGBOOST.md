# XGBoost on SPECTRA telecom_churn: best achievable result (F157)

**BLUF.** Tuned on validation and scored on the test fold over 10 seeds (42-51), XGBoost reaches a mean test AUPRC of 0.8610 (95% t interval 0.8476 to 0.8743). It is number 4 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [TELECOM_CHURN_COMPARISON.md](TELECOM_CHURN_COMPARISON.md).

- **Card**: F157 (Sprint 31 Task F, #98), the SPECTRA part: F166's algorithms and grids on SPECTRA's four datasets.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F157 SPECTRA part", written before any score.
- **Amendment**: the SVM lane is the form the entry's rule keeps, scored on the test fold under the entry's amendment of 2026-11-05 (Sprint 31 D14 option 1). The first result, `experiments/phase2/results/f157_spectra_algorithms.json`, is kept as recorded; it scored the linear form only.
- **Evidence**: `experiments/phase2/results/f157_spectra_algorithms_rbf.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f157_spectra_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: SPECTRA `telecom_churn`, label `target`, spectra_segment.spectra_split 60/20/20, seeded. Tuning reads the training and validation folds; every score here is on the test fold (630 rows, 152 to 153 positives per seed; 17 feature columns).

## Configurations tried

8 configurations, F166's grid, imported unchanged. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| learning_rate 0.1, max_depth 3, n_estimators 100 | 0 of 10 |
| learning_rate 0.1, max_depth 3, n_estimators 300 | 0 of 10 |
| learning_rate 0.3, max_depth 3, n_estimators 100 | 0 of 10 |
| learning_rate 0.3, max_depth 3, n_estimators 300 | 0 of 10 |
| learning_rate 0.1, max_depth 6, n_estimators 100 | 1 of 10 |
| learning_rate 0.1, max_depth 6, n_estimators 300 | 6 of 10 |
| learning_rate 0.3, max_depth 6, n_estimators 100 | 1 of 10 |
| learning_rate 0.3, max_depth 6, n_estimators 300 | 2 of 10 |

## Test-fold results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.8610 | 0.0186 | 0.8476 to 0.8743 |
| AUPRC, floor-normalized | 0.8166 | 0.0246 | 0.7990 to 0.8342 |
| ROC-AUC | 0.9442 | 0.0100 | 0.9371 to 0.9513 |
| Recall at the 0.5% budget, test fold | 0.0263 | 0.0001 | 0.0262 to 0.0263 |
| Train-test AUPRC gap | 0.1387 | 0.0185 | 0.1254 to 0.1520 |

Secondary, as the entry reports it: test AUPRC inside the pocket (`in_pocket` = 1) 0.7689 (95% t interval 0.7367 to 0.8010, 10 seeds) and outside it 0.9013 (0.8919 to 0.9108, 10 seeds).

At the max-F1 threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.7812 | 0.0376 | 0.7543 to 0.8081 |
| Recall | 0.7761 | 0.0402 | 0.7473 to 0.8048 |
| Specificity | 0.9299 | 0.0170 | 0.9177 to 0.9420 |
| F1 | 0.7776 | 0.0245 | 0.7601 to 0.7951 |
| MCC | 0.7078 | 0.0321 | 0.6849 to 0.7308 |
| Balanced accuracy | 0.8530 | 0.0180 | 0.8401 to 0.8659 |

At the 0.5% alert-budget threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 1.0000 | 0.0000 | 1.0000 to 1.0000 |
| Recall | 0.0197 | 0.0120 | 0.0111 to 0.0283 |
| Specificity | 1.0000 | 0.0000 | 1.0000 to 1.0000 |
| F1 | 0.0384 | 0.0230 | 0.0219 to 0.0549 |
| MCC | 0.1169 | 0.0391 | 0.0889 to 0.1448 |
| Balanced accuracy | 0.5098 | 0.0060 | 0.5056 to 0.5141 |

## Confusion counts per seed, test fold

TP, FP, TN and FN at each validation-chosen threshold, and at the test fold's own 0.5% budget (the comparison page's recall).

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN | 0.5% budget on the test fold: TP / FP / TN / FN |
|---|---|---|---|---|
| 42 | learning_rate 0.1, max_depth 6, n_estimators 300 | 118 / 30 / 448 / 34 | 2 / 0 / 478 / 150 | 4 / 0 / 478 / 148 |
| 43 | learning_rate 0.1, max_depth 6, n_estimators 300 | 115 / 28 / 450 / 37 | 1 / 0 / 478 / 151 | 4 / 0 / 478 / 148 |
| 44 | learning_rate 0.3, max_depth 6, n_estimators 300 | 116 / 36 / 442 / 36 | 5 / 0 / 478 / 147 | 4 / 0 / 478 / 148 |
| 45 | learning_rate 0.1, max_depth 6, n_estimators 300 | 108 / 34 / 443 / 45 | 1 / 0 / 477 / 152 | 4 / 0 / 477 / 149 |
| 46 | learning_rate 0.1, max_depth 6, n_estimators 300 | 126 / 39 / 438 / 27 | 4 / 0 / 477 / 149 | 4 / 0 / 477 / 149 |
| 47 | learning_rate 0.3, max_depth 6, n_estimators 300 | 128 / 36 / 441 / 25 | 4 / 0 / 477 / 149 | 4 / 0 / 477 / 149 |
| 48 | learning_rate 0.3, max_depth 6, n_estimators 100 | 117 / 31 / 447 / 35 | 1 / 0 / 478 / 151 | 4 / 0 / 478 / 148 |
| 49 | learning_rate 0.1, max_depth 6, n_estimators 100 | 124 / 51 / 427 / 28 | 6 / 0 / 478 / 146 | 4 / 0 / 478 / 148 |
| 50 | learning_rate 0.1, max_depth 6, n_estimators 300 | 118 / 20 / 458 / 34 | 2 / 0 / 478 / 150 | 4 / 0 / 478 / 148 |
| 51 | learning_rate 0.1, max_depth 6, n_estimators 300 | 112 / 30 / 448 / 40 | 4 / 0 / 478 / 148 | 4 / 0 / 478 / 148 |

## Limits

- One protocol and one grid per algorithm, F166's. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

