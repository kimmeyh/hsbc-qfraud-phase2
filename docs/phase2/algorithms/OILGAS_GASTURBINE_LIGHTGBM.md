# LightGBM on SPECTRA oilgas_gasturbine: best result within F166's grid (F157)

**BLUF.** Tuned on validation and scored on the test fold over 10 seeds (42-51), LightGBM reaches a mean test AUPRC of 0.8785 (95% t interval 0.8736 to 0.8834). It is number 1 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [OILGAS_GASTURBINE_COMPARISON.md](OILGAS_GASTURBINE_COMPARISON.md).

- **Card**: F157 (Sprint 31 Task F, #98), the SPECTRA part: F166's algorithms and grids on SPECTRA's four datasets.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F157 SPECTRA part", written before any score.
- **Amendment**: the SVM lane is the form the entry's rule keeps, scored on the test fold under the entry's amendment of 2026-11-05 (Sprint 31 D14 option 1). The first result, `experiments/phase2/results/f157_spectra_algorithms.json`, is kept as recorded; it scored the linear form only. The amendment was written after that result was seen; the other six lanes are unchanged from it.
- **Evidence**: `experiments/phase2/results/f157_spectra_algorithms_rbf.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f157_spectra_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: SPECTRA `oilgas_gasturbine`, label `target`, spectra_segment.spectra_split 60/20/20, seeded. Tuning reads the training and validation folds; every score here is on the test fold (7,347 rows, 2,050 positives per seed; 15 feature columns).

## Configurations tried

8 configurations, F166's grid, imported unchanged. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| learning_rate 0.05, num_leaves 15, reg_lambda 0.0 | 0 of 10 |
| learning_rate 0.05, num_leaves 15, reg_lambda 1.0 | 0 of 10 |
| learning_rate 0.1, num_leaves 15, reg_lambda 0.0 | 0 of 10 |
| learning_rate 0.1, num_leaves 15, reg_lambda 1.0 | 0 of 10 |
| learning_rate 0.05, num_leaves 63, reg_lambda 0.0 | 2 of 10 |
| learning_rate 0.05, num_leaves 63, reg_lambda 1.0 | 5 of 10 |
| learning_rate 0.1, num_leaves 63, reg_lambda 0.0 | 1 of 10 |
| learning_rate 0.1, num_leaves 63, reg_lambda 1.0 | 2 of 10 |

## Test-fold results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.8785 | 0.0069 | 0.8736 to 0.8834 |
| AUPRC, floor-normalized | 0.8315 | 0.0095 | 0.8247 to 0.8383 |
| ROC-AUC | 0.9340 | 0.0036 | 0.9314 to 0.9366 |
| Recall at the 0.5% budget, test fold | 0.0180 | 0.0002 | 0.0178 to 0.0181 |
| Train-test AUPRC gap | 0.1053 | 0.0058 | 0.1011 to 0.1095 |

Secondary, as the entry reports it: test AUPRC inside the pocket (`in_pocket` = 1) 0.8038 (95% t interval 0.7916 to 0.8159, 10 seeds) and outside it 0.9323 (0.9284 to 0.9362, 10 seeds).

At the max-F1 threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.7891 | 0.0276 | 0.7693 to 0.8088 |
| Recall | 0.7673 | 0.0286 | 0.7468 to 0.7877 |
| Specificity | 0.9199 | 0.0154 | 0.9088 to 0.9309 |
| F1 | 0.7772 | 0.0105 | 0.7697 to 0.7847 |
| MCC | 0.6934 | 0.0144 | 0.6831 to 0.7038 |
| Balanced accuracy | 0.8436 | 0.0092 | 0.8370 to 0.8502 |

At the 0.5% alert-budget threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.9956 | 0.0093 | 0.9890 to 1.0022 |
| Recall | 0.0189 | 0.0044 | 0.0157 to 0.0221 |
| Specificity | 1.0000 | 0.0001 | 0.9999 to 1.0000 |
| F1 | 0.0371 | 0.0086 | 0.0310 to 0.0433 |
| MCC | 0.1158 | 0.0142 | 0.1057 to 0.1260 |
| Balanced accuracy | 0.5094 | 0.0022 | 0.5079 to 0.5110 |

## Confusion counts per seed, test fold

TP, FP, TN and FN at each validation-chosen threshold, and at the test fold's own 0.5% budget (the comparison page's recall).

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN | 0.5% budget on the test fold: TP / FP / TN / FN |
|---|---|---|---|---|
| 42 | learning_rate 0.1, num_leaves 63, reg_lambda 0.0 | 1599 / 352 / 4945 / 451 | 45 / 0 / 5297 / 2005 | 37 / 0 / 5297 / 2013 |
| 43 | learning_rate 0.1, num_leaves 63, reg_lambda 1.0 | 1656 / 502 / 4795 / 394 | 40 / 0 / 5297 / 2010 | 37 / 0 / 5297 / 2013 |
| 44 | learning_rate 0.05, num_leaves 63, reg_lambda 1.0 | 1573 / 492 / 4805 / 477 | 34 / 0 / 5297 / 2016 | 37 / 0 / 5297 / 2013 |
| 45 | learning_rate 0.05, num_leaves 63, reg_lambda 1.0 | 1497 / 352 / 4945 / 553 | 40 / 0 / 5297 / 2010 | 37 / 0 / 5297 / 2013 |
| 46 | learning_rate 0.05, num_leaves 63, reg_lambda 0.0 | 1590 / 428 / 4869 / 460 | 29 / 0 / 5297 / 2021 | 37 / 0 / 5297 / 2013 |
| 47 | learning_rate 0.1, num_leaves 63, reg_lambda 1.0 | 1619 / 471 / 4826 / 431 | 53 / 0 / 5297 / 1997 | 37 / 0 / 5297 / 2013 |
| 48 | learning_rate 0.05, num_leaves 63, reg_lambda 1.0 | 1478 / 308 / 4989 / 572 | 37 / 0 / 5297 / 2013 | 37 / 0 / 5297 / 2013 |
| 49 | learning_rate 0.05, num_leaves 63, reg_lambda 0.0 | 1516 / 341 / 4956 / 534 | 21 / 0 / 5297 / 2029 | 37 / 0 / 5297 / 2013 |
| 50 | learning_rate 0.05, num_leaves 63, reg_lambda 1.0 | 1627 / 550 / 4747 / 423 | 45 / 1 / 5296 / 2005 | 36 / 1 / 5296 / 2014 |
| 51 | learning_rate 0.05, num_leaves 63, reg_lambda 1.0 | 1574 / 448 / 4849 / 476 | 44 / 1 / 5296 / 2006 | 36 / 1 / 5296 / 2014 |

## Limits

- One protocol and one grid per algorithm, F166's. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

