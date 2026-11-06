# Logistic regression on SPECTRA energy_steel: best achievable result (F157)

**BLUF.** Tuned on validation and scored on the test fold over 10 seeds (42-51), Logistic regression reaches a mean test AUPRC of 0.6441 (95% t interval 0.5456 to 0.7427). It is number 6 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [ENERGY_STEEL_COMPARISON.md](ENERGY_STEEL_COMPARISON.md).

- **Card**: F157 (Sprint 31 Task F, #98), the SPECTRA part: F166's algorithms and grids on SPECTRA's four datasets.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F157 SPECTRA part", written before any score.
- **Amendment**: the SVM lane is the form the entry's rule keeps, scored on the test fold under the entry's amendment of 2026-11-05 (Sprint 31 D14 option 1). The first result, `experiments/phase2/results/f157_spectra_algorithms.json`, is kept as recorded; it scored the linear form only.
- **Evidence**: `experiments/phase2/results/f157_spectra_algorithms_rbf.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f157_spectra_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: SPECTRA `energy_steel`, label `target`, spectra_segment.spectra_split 60/20/20, seeded. Tuning reads the training and validation folds; every score here is on the test fold (7,008 rows, 1,782 positives per seed; 17 feature columns).

## Configurations tried

8 configurations, F166's grid, imported unchanged. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| C 0.01, class_weight None | 8 of 10 |
| C 0.01, class_weight balanced | 0 of 10 |
| C 0.1, class_weight None | 1 of 10 |
| C 0.1, class_weight balanced | 0 of 10 |
| C 1.0, class_weight None | 0 of 10 |
| C 1.0, class_weight balanced | 0 of 10 |
| C 10.0, class_weight None | 1 of 10 |
| C 10.0, class_weight balanced | 0 of 10 |

No seed chose `class_weight` balanced.

## Test-fold results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.6441 | 0.1377 | 0.5456 to 0.7427 |
| AUPRC, floor-normalized | 0.5228 | 0.1847 | 0.3907 to 0.6549 |
| ROC-AUC | 0.8672 | 0.1291 | 0.7749 to 0.9595 |
| Recall at the 0.5% budget, test fold | 0.1140 | 0.3113 | -0.1087 to 0.3367 |
| Train-test AUPRC gap | 0.0469 | 0.1372 | -0.0513 to 0.1450 |

Secondary, as the entry reports it: test AUPRC inside the pocket (`in_pocket` = 1) 0.7506 (95% t interval 0.7342 to 0.7670, 10 seeds) and outside it 0.4549 (0.3768 to 0.5331, 10 seeds).

At the max-F1 threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.4687 | 0.2739 | 0.2728 to 0.6647 |
| Recall | 0.7221 | 0.3823 | 0.4486 to 0.9956 |
| Specificity | 0.7772 | 0.2827 | 0.5749 to 0.9794 |
| F1 | 0.5582 | 0.3121 | 0.3349 to 0.7815 |
| MCC | 0.4538 | 0.3132 | 0.2297 to 0.6779 |
| Balanced accuracy | 0.7496 | 0.1723 | 0.6264 to 0.8729 |

At the 0.5% alert-budget threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.5598 | 0.3529 | 0.3073 to 0.8123 |
| Recall | 0.1102 | 0.3127 | -0.1136 to 0.3339 |
| Specificity | 0.8989 | 0.3158 | 0.6730 to 1.1248 |
| F1 | 0.0605 | 0.1220 | -0.0268 to 0.1477 |
| MCC | 0.0566 | 0.0432 | 0.0257 to 0.0875 |
| Balanced accuracy | 0.5045 | 0.0036 | 0.5020 to 0.5071 |

## Confusion counts per seed, test fold

TP, FP, TN and FN at each validation-chosen threshold, and at the test fold's own 0.5% budget (the comparison page's recall).

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN | 0.5% budget on the test fold: TP / FP / TN / FN |
|---|---|---|---|---|
| 42 | C 0.01, class_weight None | 0 / 0 / 5226 / 1782 | 0 / 0 / 5226 / 1782 | 30 / 6 / 5220 / 1752 |
| 43 | C 0.01, class_weight None | 1575 / 896 / 4330 / 207 | 25 / 5 / 5221 / 1757 | 28 / 8 / 5218 / 1754 |
| 44 | C 0.01, class_weight None | 1555 / 924 / 4302 / 227 | 17 / 7 / 5219 / 1765 | 28 / 8 / 5218 / 1754 |
| 45 | C 0.1, class_weight None | 1599 / 901 / 4325 / 183 | 31 / 3 / 5223 / 1751 | 33 / 3 / 5223 / 1749 |
| 46 | C 0.01, class_weight None | 1782 / 5226 / 0 / 0 | 1782 / 5226 / 0 / 0 | 1782 / 5226 / 0 / 0 |
| 47 | C 10.0, class_weight None | 1605 / 954 / 4272 / 177 | 29 / 20 / 5206 / 1753 | 21 / 15 / 5211 / 1761 |
| 48 | C 0.01, class_weight None | 1554 / 889 / 4337 / 228 | 37 / 6 / 5220 / 1745 | 30 / 6 / 5220 / 1752 |
| 49 | C 0.01, class_weight None | 0 / 0 / 5226 / 1782 | 0 / 0 / 5226 / 1782 | 27 / 9 / 5217 / 1755 |
| 50 | C 0.01, class_weight None | 1591 / 924 / 4302 / 191 | 24 / 4 / 5222 / 1758 | 30 / 6 / 5220 / 1752 |
| 51 | C 0.01, class_weight None | 1607 / 932 / 4294 / 175 | 18 / 13 / 5213 / 1764 | 22 / 14 / 5212 / 1760 |

## Limits

- One protocol and one grid per algorithm, F166's. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

