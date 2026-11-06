# CatBoost on SPECTRA oilgas_gasturbine: best achievable result (F157)

**BLUF.** Tuned on validation and scored on the test fold over 10 seeds (42-51), CatBoost reaches a mean test AUPRC of 0.8753 (95% t interval 0.8709 to 0.8797). It is number 2 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [OILGAS_GASTURBINE_COMPARISON.md](OILGAS_GASTURBINE_COMPARISON.md).

- **Card**: F157 (Sprint 31 Task F, #98), the SPECTRA part: F166's algorithms and grids on SPECTRA's four datasets.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F157 SPECTRA part", written before any score.
- **Amendment**: the SVM lane is the form the entry's rule keeps, scored on the test fold under the entry's amendment of 2026-11-05 (Sprint 31 D14 option 1). The first result, `experiments/phase2/results/f157_spectra_algorithms.json`, is kept as recorded; it scored the linear form only.
- **Evidence**: `experiments/phase2/results/f157_spectra_algorithms_rbf.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f157_spectra_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: SPECTRA `oilgas_gasturbine`, label `target`, spectra_segment.spectra_split 60/20/20, seeded. Tuning reads the training and validation folds; every score here is on the test fold (7,347 rows, 2,050 positives per seed; 15 feature columns).

## Configurations tried

8 configurations, F166's grid, imported unchanged. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| depth 4, l2_leaf_reg 3, learning_rate 0.05 | 0 of 10 |
| depth 4, l2_leaf_reg 10, learning_rate 0.05 | 0 of 10 |
| depth 4, l2_leaf_reg 3, learning_rate 0.1 | 0 of 10 |
| depth 4, l2_leaf_reg 10, learning_rate 0.1 | 0 of 10 |
| depth 6, l2_leaf_reg 3, learning_rate 0.05 | 0 of 10 |
| depth 6, l2_leaf_reg 10, learning_rate 0.05 | 0 of 10 |
| depth 6, l2_leaf_reg 3, learning_rate 0.1 | 0 of 10 |
| depth 6, l2_leaf_reg 10, learning_rate 0.1 | 10 of 10 |

## Test-fold results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.8753 | 0.0061 | 0.8709 to 0.8797 |
| AUPRC, floor-normalized | 0.8271 | 0.0085 | 0.8210 to 0.8331 |
| ROC-AUC | 0.9324 | 0.0037 | 0.9297 to 0.9351 |
| Recall at the 0.5% budget, test fold | 0.0180 | 0.0000 | 0.0180 to 0.0180 |
| Train-test AUPRC gap | 0.0626 | 0.0073 | 0.0573 to 0.0678 |

Secondary, as the entry reports it: test AUPRC inside the pocket (`in_pocket` = 1) 0.7909 (95% t interval 0.7798 to 0.8021, 10 seeds) and outside it 0.9293 (0.9256 to 0.9329, 10 seeds).

At the max-F1 threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.7827 | 0.0210 | 0.7677 to 0.7977 |
| Recall | 0.7648 | 0.0225 | 0.7487 to 0.7809 |
| Specificity | 0.9173 | 0.0125 | 0.9084 to 0.9263 |
| F1 | 0.7731 | 0.0073 | 0.7679 to 0.7783 |
| MCC | 0.6872 | 0.0101 | 0.6800 to 0.6945 |
| Balanced accuracy | 0.8411 | 0.0068 | 0.8362 to 0.8459 |

At the 0.5% alert-budget threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 1.0000 | 0.0000 | 1.0000 to 1.0000 |
| Recall | 0.0181 | 0.0038 | 0.0154 to 0.0208 |
| Specificity | 1.0000 | 0.0000 | 1.0000 to 1.0000 |
| F1 | 0.0355 | 0.0073 | 0.0303 to 0.0408 |
| MCC | 0.1139 | 0.0125 | 0.1050 to 0.1229 |
| Balanced accuracy | 0.5090 | 0.0019 | 0.5077 to 0.5104 |

## Confusion counts per seed, test fold

TP, FP, TN and FN at each validation-chosen threshold, and at the test fold's own 0.5% budget (the comparison page's recall).

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN | 0.5% budget on the test fold: TP / FP / TN / FN |
|---|---|---|---|---|
| 42 | depth 6, l2_leaf_reg 10, learning_rate 0.1 | 1624 / 434 / 4863 / 426 | 42 / 0 / 5297 / 2008 | 37 / 0 / 5297 / 2013 |
| 43 | depth 6, l2_leaf_reg 10, learning_rate 0.1 | 1651 / 570 / 4727 / 399 | 39 / 0 / 5297 / 2011 | 37 / 0 / 5297 / 2013 |
| 44 | depth 6, l2_leaf_reg 10, learning_rate 0.1 | 1549 / 461 / 4836 / 501 | 30 / 0 / 5297 / 2020 | 37 / 0 / 5297 / 2013 |
| 45 | depth 6, l2_leaf_reg 10, learning_rate 0.1 | 1598 / 517 / 4780 / 452 | 39 / 0 / 5297 / 2011 | 37 / 0 / 5297 / 2013 |
| 46 | depth 6, l2_leaf_reg 10, learning_rate 0.1 | 1537 / 376 / 4921 / 513 | 37 / 0 / 5297 / 2013 | 37 / 0 / 5297 / 2013 |
| 47 | depth 6, l2_leaf_reg 10, learning_rate 0.1 | 1548 / 409 / 4888 / 502 | 48 / 0 / 5297 / 2002 | 37 / 0 / 5297 / 2013 |
| 48 | depth 6, l2_leaf_reg 10, learning_rate 0.1 | 1521 / 379 / 4918 / 529 | 28 / 0 / 5297 / 2022 | 37 / 0 / 5297 / 2013 |
| 49 | depth 6, l2_leaf_reg 10, learning_rate 0.1 | 1553 / 411 / 4886 / 497 | 23 / 0 / 5297 / 2027 | 37 / 0 / 5297 / 2013 |
| 50 | depth 6, l2_leaf_reg 10, learning_rate 0.1 | 1508 / 362 / 4935 / 542 | 42 / 0 / 5297 / 2008 | 37 / 0 / 5297 / 2013 |
| 51 | depth 6, l2_leaf_reg 10, learning_rate 0.1 | 1589 / 459 / 4838 / 461 | 43 / 0 / 5297 / 2007 | 37 / 0 / 5297 / 2013 |

## Limits

- One protocol and one grid per algorithm, F166's. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

