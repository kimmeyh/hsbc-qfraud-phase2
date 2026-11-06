# Logistic regression on SPECTRA oilgas_gasturbine: best result within F166's grid (F157)

**BLUF.** Tuned on validation and scored on the test fold over 10 seeds (42-51), Logistic regression reaches a mean test AUPRC of 0.7811 (95% t interval 0.7771 to 0.7850). It is number 7 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [OILGAS_GASTURBINE_COMPARISON.md](OILGAS_GASTURBINE_COMPARISON.md).

- **Card**: F157 (Sprint 31 Task F, #98), the SPECTRA part: F166's algorithms and grids on SPECTRA's four datasets.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F157 SPECTRA part", written before any score.
- **Amendment**: the SVM lane is the form the entry's rule keeps, scored on the test fold under the entry's amendment of 2026-11-05 (Sprint 31 D14 option 1). The first result, `experiments/phase2/results/f157_spectra_algorithms.json`, is kept as recorded; it scored the linear form only. The amendment was written after that result was seen; the other six lanes are unchanged from it.
- **Evidence**: `experiments/phase2/results/f157_spectra_algorithms_rbf.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f157_spectra_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: SPECTRA `oilgas_gasturbine`, label `target`, spectra_segment.spectra_split 60/20/20, seeded. Tuning reads the training and validation folds; every score here is on the test fold (7,347 rows, 2,050 positives per seed; 15 feature columns).

## Configurations tried

8 configurations, F166's grid, imported unchanged. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| C 0.01, class_weight None | 0 of 10 |
| C 0.01, class_weight balanced | 0 of 10 |
| C 0.1, class_weight None | 0 of 10 |
| C 0.1, class_weight balanced | 0 of 10 |
| C 1.0, class_weight None | 0 of 10 |
| C 1.0, class_weight balanced | 0 of 10 |
| C 10.0, class_weight None | 10 of 10 |
| C 10.0, class_weight balanced | 0 of 10 |

No seed chose `class_weight` balanced.

## Test-fold results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.7811 | 0.0055 | 0.7771 to 0.7850 |
| AUPRC, floor-normalized | 0.6963 | 0.0076 | 0.6909 to 0.7018 |
| ROC-AUC | 0.8676 | 0.0032 | 0.8653 to 0.8699 |
| Recall at the 0.5% budget, test fold | 0.0179 | 0.0003 | 0.0177 to 0.0180 |
| Train-test AUPRC gap | 0.0008 | 0.0062 | -0.0036 to 0.0053 |

Secondary, as the entry reports it: test AUPRC inside the pocket (`in_pocket` = 1) 0.7147 (95% t interval 0.7026 to 0.7268, 10 seeds) and outside it 0.8610 (0.8548 to 0.8672, 10 seeds).

At the max-F1 threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.7325 | 0.0419 | 0.7025 to 0.7625 |
| Recall | 0.6562 | 0.0388 | 0.6285 to 0.6840 |
| Specificity | 0.9053 | 0.0244 | 0.8878 to 0.9227 |
| F1 | 0.6902 | 0.0067 | 0.6854 to 0.6950 |
| MCC | 0.5823 | 0.0109 | 0.5745 to 0.5901 |
| Balanced accuracy | 0.7808 | 0.0080 | 0.7751 to 0.7865 |

At the 0.5% alert-budget threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.9876 | 0.0163 | 0.9760 to 0.9993 |
| Recall | 0.0159 | 0.0024 | 0.0142 to 0.0176 |
| Specificity | 0.9999 | 0.0001 | 0.9999 to 1.0000 |
| F1 | 0.0313 | 0.0047 | 0.0279 to 0.0347 |
| MCC | 0.1059 | 0.0086 | 0.0998 to 0.1120 |
| Balanced accuracy | 0.5079 | 0.0012 | 0.5070 to 0.5088 |

## Confusion counts per seed, test fold

TP, FP, TN and FN at each validation-chosen threshold, and at the test fold's own 0.5% budget (the comparison page's recall).

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN | 0.5% budget on the test fold: TP / FP / TN / FN |
|---|---|---|---|---|
| 42 | C 10.0, class_weight None | 1255 / 326 / 4971 / 795 | 41 / 0 / 5297 / 2009 | 37 / 0 / 5297 / 2013 |
| 43 | C 10.0, class_weight None | 1398 / 633 / 4664 / 652 | 31 / 0 / 5297 / 2019 | 37 / 0 / 5297 / 2013 |
| 44 | C 10.0, class_weight None | 1358 / 528 / 4769 / 692 | 27 / 0 / 5297 / 2023 | 37 / 0 / 5297 / 2013 |
| 45 | C 10.0, class_weight None | 1231 / 306 / 4991 / 819 | 31 / 0 / 5297 / 2019 | 37 / 0 / 5297 / 2013 |
| 46 | C 10.0, class_weight None | 1401 / 559 / 4738 / 649 | 33 / 1 / 5296 / 2017 | 36 / 1 / 5296 / 2014 |
| 47 | C 10.0, class_weight None | 1458 / 686 / 4611 / 592 | 33 / 0 / 5297 / 2017 | 37 / 0 / 5297 / 2013 |
| 48 | C 10.0, class_weight None | 1349 / 514 / 4783 / 701 | 34 / 0 / 5297 / 2016 | 37 / 0 / 5297 / 2013 |
| 49 | C 10.0, class_weight None | 1353 / 511 / 4786 / 697 | 25 / 1 / 5296 / 2025 | 36 / 1 / 5296 / 2014 |
| 50 | C 10.0, class_weight None | 1235 / 368 / 4929 / 815 | 31 / 1 / 5296 / 2019 | 36 / 1 / 5296 / 2014 |
| 51 | C 10.0, class_weight None | 1415 / 587 / 4710 / 635 | 40 / 1 / 5296 / 2010 | 36 / 1 / 5296 / 2014 |

## Limits

- One protocol and one grid per algorithm, F166's. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

