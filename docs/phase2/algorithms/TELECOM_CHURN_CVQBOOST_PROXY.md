# CVQBoost proxy on SPECTRA telecom_churn: best achievable result (F157)

**BLUF.** Tuned on validation and scored on the test fold over 10 seeds (42-51), CVQBoost proxy reaches a mean test AUPRC of 0.7254 (95% t interval 0.7042 to 0.7466). It is number 6 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [TELECOM_CHURN_COMPARISON.md](TELECOM_CHURN_COMPARISON.md).

- **Card**: F157 (Sprint 31 Task F, #98), the SPECTRA part: F166's algorithms and grids on SPECTRA's four datasets.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F157 SPECTRA part", written before any score.
- **Amendment**: the SVM lane is the form the entry's rule keeps, scored on the test fold under the entry's amendment of 2026-11-05 (Sprint 31 D14 option 1). The first result, `experiments/phase2/results/f157_spectra_algorithms.json`, is kept as recorded; it scored the linear form only.
- **Evidence**: `experiments/phase2/results/f157_spectra_algorithms_rbf.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f157_spectra_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: SPECTRA `telecom_churn`, label `target`, spectra_segment.spectra_split 60/20/20, seeded. Tuning reads the training and validation folds; every score here is on the test fold (630 rows, 152 to 153 positives per seed; 17 feature columns).

## Configurations tried

3 configurations, F166's grid, imported unchanged. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| config free | 0 of 10 |
| config mid | 0 of 10 |
| config full | 10 of 10 |

The `full` configuration was chosen on every seed. Every pool was built serially; the chosen pool used 17 features and held 833 learners.

## Test-fold results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.7254 | 0.0296 | 0.7042 to 0.7466 |
| AUPRC, floor-normalized | 0.6378 | 0.0391 | 0.6099 to 0.6658 |
| ROC-AUC | 0.8996 | 0.0136 | 0.8899 to 0.9093 |
| Recall at the 0.5% budget, test fold | 0.0236 | 0.0034 | 0.0212 to 0.0261 |
| Train-test AUPRC gap | 0.2746 | 0.0296 | 0.2534 to 0.2958 |

Secondary, as the entry reports it: test AUPRC inside the pocket (`in_pocket` = 1) 0.7943 (95% t interval 0.7609 to 0.8277, 10 seeds) and outside it 0.6928 (0.6617 to 0.7238, 10 seeds).

At the max-F1 threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.6504 | 0.0531 | 0.6124 to 0.6884 |
| Recall | 0.7610 | 0.0399 | 0.7325 to 0.7896 |
| Specificity | 0.8667 | 0.0365 | 0.8406 to 0.8927 |
| F1 | 0.6994 | 0.0302 | 0.6778 to 0.7210 |
| MCC | 0.5978 | 0.0415 | 0.5681 to 0.6275 |
| Balanced accuracy | 0.8138 | 0.0179 | 0.8011 to 0.8266 |

At the 0.5% alert-budget threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.8208 | 0.3192 | 0.5925 to 1.0492 |
| Recall | 0.0164 | 0.0133 | 0.0069 to 0.0259 |
| Specificity | 0.9994 | 0.0010 | 0.9986 to 1.0001 |
| F1 | 0.0319 | 0.0252 | 0.0139 to 0.0500 |
| MCC | 0.0929 | 0.0487 | 0.0581 to 0.1278 |
| Balanced accuracy | 0.5079 | 0.0064 | 0.5033 to 0.5125 |

## Confusion counts per seed, test fold

TP, FP, TN and FN at each validation-chosen threshold, and at the test fold's own 0.5% budget (the comparison page's recall).

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN | 0.5% budget on the test fold: TP / FP / TN / FN |
|---|---|---|---|---|
| 42 | config full | 117 / 74 / 404 / 35 | 4 / 0 / 478 / 148 | 4 / 0 / 478 / 148 |
| 43 | config full | 118 / 56 / 422 / 34 | 4 / 0 / 478 / 148 | 4 / 0 / 478 / 148 |
| 44 | config full | 115 / 60 / 418 / 37 | 2 / 0 / 478 / 150 | 4 / 0 / 478 / 148 |
| 45 | config full | 110 / 62 / 415 / 43 | 2 / 0 / 477 / 151 | 3 / 1 / 476 / 150 |
| 46 | config full | 120 / 71 / 406 / 33 | 2 / 1 / 476 / 151 | 3 / 1 / 476 / 150 |
| 47 | config full | 111 / 43 / 434 / 42 | 1 / 0 / 477 / 152 | 4 / 0 / 477 / 149 |
| 48 | config full | 125 / 103 / 375 / 27 | 0 / 0 / 478 / 152 | 4 / 0 / 478 / 148 |
| 49 | config full | 116 / 71 / 407 / 36 | 7 / 1 / 477 / 145 | 4 / 0 / 478 / 148 |
| 50 | config full | 122 / 46 / 432 / 30 | 2 / 1 / 477 / 150 | 3 / 1 / 477 / 149 |
| 51 | config full | 105 / 51 / 427 / 47 | 1 / 0 / 478 / 151 | 3 / 1 / 477 / 149 |

## Limits

- One protocol and one grid per algorithm, F166's. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

