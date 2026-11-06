# CatBoost on SPECTRA maintenance_ai4i: best result within F166's grid (F157)

**BLUF.** Tuned on validation and scored on the test fold over 10 seeds (42-51), CatBoost reaches a mean test AUPRC of 0.6368 (95% t interval 0.6222 to 0.6515). It is number 1 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [MAINTENANCE_AI4I_COMPARISON.md](MAINTENANCE_AI4I_COMPARISON.md).

- **Card**: F157 (Sprint 31 Task F, #98), the SPECTRA part: F166's algorithms and grids on SPECTRA's four datasets.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F157 SPECTRA part", written before any score.
- **Amendment**: the SVM lane is the form the entry's rule keeps, scored on the test fold under the entry's amendment of 2026-11-05 (Sprint 31 D14 option 1). The first result, `experiments/phase2/results/f157_spectra_algorithms.json`, is kept as recorded; it scored the linear form only. The amendment was written after that result was seen; the other six lanes are unchanged from it.
- **Evidence**: `experiments/phase2/results/f157_spectra_algorithms_rbf.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f157_spectra_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: SPECTRA `maintenance_ai4i`, label `target`, spectra_segment.spectra_split 60/20/20, seeded. Tuning reads the training and validation folds; every score here is on the test fold (2,000 rows, 235 positives per seed; 12 feature columns).

## Configurations tried

8 configurations, F166's grid, imported unchanged. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| depth 4, l2_leaf_reg 3, learning_rate 0.05 | 1 of 10 |
| depth 4, l2_leaf_reg 10, learning_rate 0.05 | 2 of 10 |
| depth 4, l2_leaf_reg 3, learning_rate 0.1 | 0 of 10 |
| depth 4, l2_leaf_reg 10, learning_rate 0.1 | 1 of 10 |
| depth 6, l2_leaf_reg 3, learning_rate 0.05 | 2 of 10 |
| depth 6, l2_leaf_reg 10, learning_rate 0.05 | 3 of 10 |
| depth 6, l2_leaf_reg 3, learning_rate 0.1 | 0 of 10 |
| depth 6, l2_leaf_reg 10, learning_rate 0.1 | 1 of 10 |

## Test-fold results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.6368 | 0.0205 | 0.6222 to 0.6515 |
| AUPRC, floor-normalized | 0.5885 | 0.0232 | 0.5718 to 0.6051 |
| ROC-AUC | 0.9303 | 0.0044 | 0.9271 to 0.9334 |
| Recall at the 0.5% budget, test fold | 0.0417 | 0.0018 | 0.0404 to 0.0430 |
| Train-test AUPRC gap | 0.2528 | 0.0401 | 0.2241 to 0.2814 |

Secondary, as the entry reports it: test AUPRC inside the pocket (`in_pocket` = 1) 0.6383 (95% t interval 0.6196 to 0.6570, 10 seeds) and outside it 0.7023 (0.6806 to 0.7241, 10 seeds).

At the max-F1 threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.5381 | 0.0324 | 0.5149 to 0.5613 |
| Recall | 0.7140 | 0.0656 | 0.6671 to 0.7610 |
| Specificity | 0.9171 | 0.0178 | 0.9044 to 0.9298 |
| F1 | 0.6109 | 0.0176 | 0.5983 to 0.6235 |
| MCC | 0.5600 | 0.0205 | 0.5453 to 0.5747 |
| Balanced accuracy | 0.8156 | 0.0251 | 0.7976 to 0.8336 |

At the 0.5% alert-budget threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.9630 | 0.0484 | 0.9283 to 0.9976 |
| Recall | 0.0494 | 0.0255 | 0.0311 to 0.0676 |
| Specificity | 0.9997 | 0.0005 | 0.9993 to 1.0000 |
| F1 | 0.0928 | 0.0450 | 0.0606 to 0.1250 |
| MCC | 0.1976 | 0.0498 | 0.1620 to 0.2332 |
| Balanced accuracy | 0.5245 | 0.0126 | 0.5155 to 0.5335 |

## Confusion counts per seed, test fold

TP, FP, TN and FN at each validation-chosen threshold, and at the test fold's own 0.5% budget (the comparison page's recall).

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN | 0.5% budget on the test fold: TP / FP / TN / FN |
|---|---|---|---|---|
| 42 | depth 4, l2_leaf_reg 10, learning_rate 0.1 | 169 / 140 / 1625 / 66 | 7 / 0 / 1765 / 228 | 10 / 0 / 1765 / 225 |
| 43 | depth 4, l2_leaf_reg 10, learning_rate 0.05 | 184 / 201 / 1564 / 51 | 10 / 1 / 1764 / 225 | 9 / 1 / 1764 / 226 |
| 44 | depth 4, l2_leaf_reg 3, learning_rate 0.05 | 182 / 176 / 1589 / 53 | 3 / 0 / 1765 / 232 | 10 / 0 / 1765 / 225 |
| 45 | depth 6, l2_leaf_reg 3, learning_rate 0.05 | 146 / 107 / 1658 / 89 | 11 / 0 / 1765 / 224 | 10 / 0 / 1765 / 225 |
| 46 | depth 6, l2_leaf_reg 10, learning_rate 0.05 | 159 / 137 / 1628 / 76 | 10 / 0 / 1765 / 225 | 10 / 0 / 1765 / 225 |
| 47 | depth 6, l2_leaf_reg 10, learning_rate 0.05 | 164 / 120 / 1645 / 71 | 10 / 0 / 1765 / 225 | 10 / 0 / 1765 / 225 |
| 48 | depth 4, l2_leaf_reg 10, learning_rate 0.05 | 163 / 134 / 1631 / 72 | 14 / 0 / 1765 / 221 | 10 / 0 / 1765 / 225 |
| 49 | depth 6, l2_leaf_reg 10, learning_rate 0.05 | 187 / 185 / 1580 / 48 | 17 / 2 / 1763 / 218 | 10 / 0 / 1765 / 225 |
| 50 | depth 6, l2_leaf_reg 10, learning_rate 0.1 | 180 / 148 / 1617 / 55 | 9 / 1 / 1764 / 226 | 9 / 1 / 1764 / 226 |
| 51 | depth 6, l2_leaf_reg 3, learning_rate 0.05 | 144 / 115 / 1650 / 91 | 25 / 2 / 1763 / 210 | 10 / 0 / 1765 / 225 |

## Limits

- One protocol and one grid per algorithm, F166's. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

