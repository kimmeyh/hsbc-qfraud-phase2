# HGB on SPECTRA oilgas_gasturbine: best achievable result (F157)

**BLUF.** Tuned on validation and scored on the test fold over 10 seeds (42-51), HGB reaches a mean test AUPRC of 0.8730 (95% t interval 0.8677 to 0.8782). It is number 4 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [OILGAS_GASTURBINE_COMPARISON.md](OILGAS_GASTURBINE_COMPARISON.md).

- **Card**: F157 (Sprint 31 Task F, #98), the SPECTRA part: F166's algorithms and grids on SPECTRA's four datasets.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F157 SPECTRA part", written before any score.
- **Amendment**: the SVM lane is the form the entry's rule keeps, scored on the test fold under the entry's amendment of 2026-11-05 (Sprint 31 D14 option 1). The first result, `experiments/phase2/results/f157_spectra_algorithms.json`, is kept as recorded; it scored the linear form only.
- **Evidence**: `experiments/phase2/results/f157_spectra_algorithms_rbf.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f157_spectra_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: SPECTRA `oilgas_gasturbine`, label `target`, spectra_segment.spectra_split 60/20/20, seeded. Tuning reads the training and validation folds; every score here is on the test fold (7,347 rows, 2,050 positives per seed; 15 feature columns).

## Configurations tried

8 configurations, F166's grid, imported unchanged. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| l2_regularization 0.0, learning_rate 0.05, max_leaf_nodes 15 | 0 of 10 |
| l2_regularization 0.0, learning_rate 0.05, max_leaf_nodes 31 | 0 of 10 |
| l2_regularization 0.0, learning_rate 0.1, max_leaf_nodes 15 | 0 of 10 |
| l2_regularization 0.0, learning_rate 0.1, max_leaf_nodes 31 | 5 of 10 |
| l2_regularization 1.0, learning_rate 0.05, max_leaf_nodes 15 | 0 of 10 |
| l2_regularization 1.0, learning_rate 0.05, max_leaf_nodes 31 | 0 of 10 |
| l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 15 | 0 of 10 |
| l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 31 | 5 of 10 |

## Test-fold results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.8730 | 0.0074 | 0.8677 to 0.8782 |
| AUPRC, floor-normalized | 0.8238 | 0.0102 | 0.8165 to 0.8311 |
| ROC-AUC | 0.9316 | 0.0044 | 0.9285 to 0.9348 |
| Recall at the 0.5% budget, test fold | 0.0180 | 0.0002 | 0.0179 to 0.0182 |
| Train-test AUPRC gap | 0.0502 | 0.0072 | 0.0451 to 0.0553 |

Secondary, as the entry reports it: test AUPRC inside the pocket (`in_pocket` = 1) 0.7824 (95% t interval 0.7699 to 0.7948, 10 seeds) and outside it 0.9280 (0.9237 to 0.9323, 10 seeds).

At the max-F1 threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.7720 | 0.0235 | 0.7552 to 0.7889 |
| Recall | 0.7699 | 0.0299 | 0.7484 to 0.7913 |
| Specificity | 0.9114 | 0.0146 | 0.9009 to 0.9218 |
| F1 | 0.7702 | 0.0090 | 0.7638 to 0.7766 |
| MCC | 0.6821 | 0.0115 | 0.6739 to 0.6903 |
| Balanced accuracy | 0.8406 | 0.0093 | 0.8340 to 0.8472 |

At the 0.5% alert-budget threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.9980 | 0.0063 | 0.9935 to 1.0025 |
| Recall | 0.0179 | 0.0054 | 0.0141 to 0.0217 |
| Specificity | 1.0000 | 0.0001 | 0.9999 to 1.0000 |
| F1 | 0.0351 | 0.0104 | 0.0277 to 0.0425 |
| MCC | 0.1123 | 0.0181 | 0.0994 to 0.1253 |
| Balanced accuracy | 0.5089 | 0.0027 | 0.5070 to 0.5108 |

## Confusion counts per seed, test fold

TP, FP, TN and FN at each validation-chosen threshold, and at the test fold's own 0.5% budget (the comparison page's recall).

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN | 0.5% budget on the test fold: TP / FP / TN / FN |
|---|---|---|---|---|
| 42 | l2_regularization 0.0, learning_rate 0.1, max_leaf_nodes 31 | 1672 / 530 / 4767 / 378 | 49 / 0 / 5297 / 2001 | 38 / 0 / 5297 / 2012 |
| 43 | l2_regularization 0.0, learning_rate 0.1, max_leaf_nodes 31 | 1602 / 488 / 4809 / 448 | 43 / 0 / 5297 / 2007 | 37 / 0 / 5297 / 2013 |
| 44 | l2_regularization 0.0, learning_rate 0.1, max_leaf_nodes 31 | 1530 / 475 / 4822 / 520 | 32 / 0 / 5297 / 2018 | 37 / 0 / 5297 / 2013 |
| 45 | l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 31 | 1512 / 398 / 4899 / 538 | 38 / 0 / 5297 / 2012 | 37 / 0 / 5297 / 2013 |
| 46 | l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 31 | 1611 / 490 / 4807 / 439 | 32 / 0 / 5297 / 2018 | 37 / 0 / 5297 / 2013 |
| 47 | l2_regularization 0.0, learning_rate 0.1, max_leaf_nodes 31 | 1576 / 444 / 4853 / 474 | 37 / 0 / 5297 / 2013 | 37 / 0 / 5297 / 2013 |
| 48 | l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 31 | 1480 / 345 / 4952 / 570 | 24 / 0 / 5297 / 2026 | 37 / 0 / 5297 / 2013 |
| 49 | l2_regularization 0.0, learning_rate 0.1, max_leaf_nodes 31 | 1621 / 525 / 4772 / 429 | 16 / 0 / 5297 / 2034 | 37 / 0 / 5297 / 2013 |
| 50 | l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 31 | 1539 / 392 / 4905 / 511 | 49 / 1 / 5296 / 2001 | 36 / 1 / 5296 / 2014 |
| 51 | l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 31 | 1639 / 608 / 4689 / 411 | 47 / 0 / 5297 / 2003 | 37 / 0 / 5297 / 2013 |

## Limits

- One protocol and one grid per algorithm, F166's. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

