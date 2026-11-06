# Logistic regression on SPECTRA maintenance_ai4i: best achievable result (F157)

**BLUF.** Tuned on validation and scored on the test fold over 10 seeds (42-51), Logistic regression reaches a mean test AUPRC of 0.5126 (95% t interval 0.4951 to 0.5300). It is number 7 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [MAINTENANCE_AI4I_COMPARISON.md](MAINTENANCE_AI4I_COMPARISON.md).

- **Card**: F157 (Sprint 31 Task F, #98), the SPECTRA part: F166's algorithms and grids on SPECTRA's four datasets.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F157 SPECTRA part", written before any score.
- **Amendment**: the SVM lane is the form the entry's rule keeps, scored on the test fold under the entry's amendment of 2026-11-05 (Sprint 31 D14 option 1). The first result, `experiments/phase2/results/f157_spectra_algorithms.json`, is kept as recorded; it scored the linear form only.
- **Evidence**: `experiments/phase2/results/f157_spectra_algorithms_rbf.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f157_spectra_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: SPECTRA `maintenance_ai4i`, label `target`, spectra_segment.spectra_split 60/20/20, seeded. Tuning reads the training and validation folds; every score here is on the test fold (2,000 rows, 235 positives per seed; 12 feature columns).

## Configurations tried

8 configurations, F166's grid, imported unchanged. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| C 0.01, class_weight None | 0 of 10 |
| C 0.01, class_weight balanced | 0 of 10 |
| C 0.1, class_weight None | 0 of 10 |
| C 0.1, class_weight balanced | 0 of 10 |
| C 1.0, class_weight None | 1 of 10 |
| C 1.0, class_weight balanced | 0 of 10 |
| C 10.0, class_weight None | 4 of 10 |
| C 10.0, class_weight balanced | 5 of 10 |

5 of 10 seeds chose `class_weight` balanced.

## Test-fold results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.5126 | 0.0244 | 0.4951 to 0.5300 |
| AUPRC, floor-normalized | 0.4477 | 0.0276 | 0.4279 to 0.4675 |
| ROC-AUC | 0.8933 | 0.0092 | 0.8867 to 0.8999 |
| Recall at the 0.5% budget, test fold | 0.0366 | 0.0041 | 0.0337 to 0.0395 |
| Train-test AUPRC gap | 0.0079 | 0.0287 | -0.0127 to 0.0284 |

Secondary, as the entry reports it: test AUPRC inside the pocket (`in_pocket` = 1) 0.5914 (95% t interval 0.5738 to 0.6089, 10 seeds) and outside it 0.3494 (0.3070 to 0.3917, 10 seeds).

At the max-F1 threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.4545 | 0.0297 | 0.4332 to 0.4757 |
| Recall | 0.6732 | 0.0570 | 0.6324 to 0.7140 |
| Specificity | 0.8910 | 0.0207 | 0.8762 to 0.9059 |
| F1 | 0.5406 | 0.0199 | 0.5263 to 0.5548 |
| MCC | 0.4793 | 0.0229 | 0.4629 to 0.4956 |
| Balanced accuracy | 0.7821 | 0.0206 | 0.7674 to 0.7968 |

At the 0.5% alert-budget threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.8548 | 0.0543 | 0.8160 to 0.8937 |
| Recall | 0.0460 | 0.0151 | 0.0351 to 0.0568 |
| Specificity | 0.9990 | 0.0005 | 0.9986 to 0.9994 |
| F1 | 0.0869 | 0.0275 | 0.0672 to 0.1065 |
| MCC | 0.1804 | 0.0352 | 0.1552 to 0.2056 |
| Balanced accuracy | 0.5225 | 0.0075 | 0.5171 to 0.5278 |

## Confusion counts per seed, test fold

TP, FP, TN and FN at each validation-chosen threshold, and at the test fold's own 0.5% budget (the comparison page's recall).

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN | 0.5% budget on the test fold: TP / FP / TN / FN |
|---|---|---|---|---|
| 42 | C 10.0, class_weight balanced | 161 / 207 / 1558 / 74 | 6 / 1 / 1764 / 229 | 8 / 2 / 1763 / 227 |
| 43 | C 10.0, class_weight balanced | 176 / 261 / 1504 / 59 | 17 / 1 / 1764 / 218 | 10 / 0 / 1765 / 225 |
| 44 | C 10.0, class_weight balanced | 140 / 157 / 1608 / 95 | 14 / 3 / 1762 / 221 | 9 / 1 / 1764 / 226 |
| 45 | C 10.0, class_weight None | 155 / 160 / 1605 / 80 | 10 / 1 / 1764 / 225 | 9 / 1 / 1764 / 226 |
| 46 | C 10.0, class_weight None | 161 / 203 / 1562 / 74 | 10 / 2 / 1763 / 225 | 8 / 2 / 1763 / 227 |
| 47 | C 10.0, class_weight None | 157 / 176 / 1589 / 78 | 5 / 1 / 1764 / 230 | 7 / 3 / 1762 / 228 |
| 48 | C 1.0, class_weight None | 136 / 166 / 1599 / 99 | 11 / 3 / 1762 / 224 | 8 / 2 / 1763 / 227 |
| 49 | C 10.0, class_weight balanced | 161 / 164 / 1601 / 74 | 10 / 2 / 1763 / 225 | 8 / 2 / 1763 / 227 |
| 50 | C 10.0, class_weight None | 179 / 246 / 1519 / 56 | 12 / 3 / 1762 / 223 | 9 / 1 / 1764 / 226 |
| 51 | C 10.0, class_weight balanced | 156 / 183 / 1582 / 79 | 13 / 1 / 1764 / 222 | 10 / 0 / 1765 / 225 |

## Limits

- One protocol and one grid per algorithm, F166's. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

