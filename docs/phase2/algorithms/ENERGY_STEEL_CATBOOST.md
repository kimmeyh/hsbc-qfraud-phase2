# CatBoost on SPECTRA energy_steel: best result within F166's grid (F157)

**BLUF.** Tuned on validation and scored on the test fold over 10 seeds (42-51), CatBoost reaches a mean test AUPRC of 0.9770 (95% t interval 0.9676 to 0.9864). It is number 1 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [ENERGY_STEEL_COMPARISON.md](ENERGY_STEEL_COMPARISON.md).

- **Card**: F157 (Sprint 31 Task F, #98), the SPECTRA part: F166's algorithms and grids on SPECTRA's four datasets.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F157 SPECTRA part", written before any score.
- **Amendment**: the SVM lane is the form the entry's rule keeps, scored on the test fold under the entry's amendment of 2026-11-05 (Sprint 31 D14 option 1). The first result, `experiments/phase2/results/f157_spectra_algorithms.json`, is kept as recorded; it scored the linear form only. The amendment was written after that result was seen; the other six lanes are unchanged from it.
- **Evidence**: `experiments/phase2/results/f157_spectra_algorithms_rbf.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f157_spectra_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: SPECTRA `energy_steel`, label `target`, spectra_segment.spectra_split 60/20/20, seeded. Tuning reads the training and validation folds; every score here is on the test fold (7,008 rows, 1,782 positives per seed; 17 feature columns).

## Configurations tried

8 configurations, F166's grid, imported unchanged. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| depth 4, l2_leaf_reg 3, learning_rate 0.05 | 0 of 10 |
| depth 4, l2_leaf_reg 10, learning_rate 0.05 | 1 of 10 |
| depth 4, l2_leaf_reg 3, learning_rate 0.1 | 0 of 10 |
| depth 4, l2_leaf_reg 10, learning_rate 0.1 | 0 of 10 |
| depth 6, l2_leaf_reg 3, learning_rate 0.05 | 1 of 10 |
| depth 6, l2_leaf_reg 10, learning_rate 0.05 | 2 of 10 |
| depth 6, l2_leaf_reg 3, learning_rate 0.1 | 3 of 10 |
| depth 6, l2_leaf_reg 10, learning_rate 0.1 | 3 of 10 |

## Test-fold results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.9770 | 0.0131 | 0.9676 to 0.9864 |
| AUPRC, floor-normalized | 0.9692 | 0.0176 | 0.9566 to 0.9818 |
| ROC-AUC | 0.9914 | 0.0045 | 0.9882 to 0.9946 |
| Recall at the 0.5% budget, test fold | 0.0202 | 0.0000 | 0.0202 to 0.0202 |
| Train-test AUPRC gap | 0.0190 | 0.0127 | 0.0099 to 0.0281 |

Secondary, as the entry reports it: test AUPRC inside the pocket (`in_pocket` = 1) 0.9609 (95% t interval 0.9542 to 0.9676, 10 seeds) and outside it 0.9902 (0.9808 to 0.9996, 10 seeds).

At the max-F1 threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.9120 | 0.0312 | 0.8897 to 0.9343 |
| Recall | 0.9071 | 0.0329 | 0.8836 to 0.9306 |
| Specificity | 0.9698 | 0.0114 | 0.9617 to 0.9780 |
| F1 | 0.9091 | 0.0233 | 0.8924 to 0.9258 |
| MCC | 0.8786 | 0.0311 | 0.8564 to 0.9009 |
| Balanced accuracy | 0.9385 | 0.0172 | 0.9262 to 0.9508 |

At the 0.5% alert-budget threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 1.0000 | 0.0000 | 1.0000 to 1.0000 |
| Recall | 0.0173 | 0.0078 | 0.0118 to 0.0229 |
| Specificity | 1.0000 | 0.0000 | 1.0000 to 1.0000 |
| F1 | 0.0340 | 0.0151 | 0.0232 to 0.0448 |
| MCC | 0.1097 | 0.0328 | 0.0862 to 0.1331 |
| Balanced accuracy | 0.5087 | 0.0039 | 0.5059 to 0.5115 |

## Confusion counts per seed, test fold

TP, FP, TN and FN at each validation-chosen threshold, and at the test fold's own 0.5% budget (the comparison page's recall).

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN | 0.5% budget on the test fold: TP / FP / TN / FN |
|---|---|---|---|---|
| 42 | depth 6, l2_leaf_reg 3, learning_rate 0.05 | 1676 / 194 / 5032 / 106 | 31 / 0 / 5226 / 1751 | 36 / 0 / 5226 / 1746 |
| 43 | depth 6, l2_leaf_reg 3, learning_rate 0.1 | 1587 / 78 / 5148 / 195 | 48 / 0 / 5226 / 1734 | 36 / 0 / 5226 / 1746 |
| 44 | depth 4, l2_leaf_reg 10, learning_rate 0.05 | 1575 / 173 / 5053 / 207 | 24 / 0 / 5226 / 1758 | 36 / 0 / 5226 / 1746 |
| 45 | depth 6, l2_leaf_reg 10, learning_rate 0.05 | 1614 / 257 / 4969 / 168 | 37 / 0 / 5226 / 1745 | 36 / 0 / 5226 / 1746 |
| 46 | depth 6, l2_leaf_reg 10, learning_rate 0.05 | 1659 / 192 / 5034 / 123 | 34 / 0 / 5226 / 1748 | 36 / 0 / 5226 / 1746 |
| 47 | depth 6, l2_leaf_reg 3, learning_rate 0.1 | 1673 / 152 / 5074 / 109 | 51 / 0 / 5226 / 1731 | 36 / 0 / 5226 / 1746 |
| 48 | depth 6, l2_leaf_reg 3, learning_rate 0.1 | 1577 / 65 / 5161 / 205 | 21 / 0 / 5226 / 1761 | 36 / 0 / 5226 / 1746 |
| 49 | depth 6, l2_leaf_reg 10, learning_rate 0.1 | 1494 / 204 / 5022 / 288 | 2 / 0 / 5226 / 1780 | 36 / 0 / 5226 / 1746 |
| 50 | depth 6, l2_leaf_reg 10, learning_rate 0.1 | 1665 / 148 / 5078 / 117 | 29 / 0 / 5226 / 1753 | 36 / 0 / 5226 / 1746 |
| 51 | depth 6, l2_leaf_reg 10, learning_rate 0.1 | 1645 / 113 / 5113 / 137 | 32 / 0 / 5226 / 1750 | 36 / 0 / 5226 / 1746 |

## Limits

- One protocol and one grid per algorithm, F166's. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

