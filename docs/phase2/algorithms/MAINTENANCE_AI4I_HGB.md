# HGB on SPECTRA maintenance_ai4i: best result within F166's grid (F157)

**BLUF.** Tuned on validation and scored on the test fold over 10 seeds (42-51), HGB reaches a mean test AUPRC of 0.6310 (95% t interval 0.6210 to 0.6410). It is number 2 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [MAINTENANCE_AI4I_COMPARISON.md](MAINTENANCE_AI4I_COMPARISON.md).

- **Card**: F157 (Sprint 31 Task F, #98), the SPECTRA part: F166's algorithms and grids on SPECTRA's four datasets.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F157 SPECTRA part", written before any score.
- **Amendment**: the SVM lane is the form the entry's rule keeps, scored on the test fold under the entry's amendment of 2026-11-05 (Sprint 31 D14 option 1). The first result, `experiments/phase2/results/f157_spectra_algorithms.json`, is kept as recorded; it scored the linear form only. The amendment was written after that result was seen; the other six lanes are unchanged from it.
- **Evidence**: `experiments/phase2/results/f157_spectra_algorithms_rbf.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f157_spectra_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: SPECTRA `maintenance_ai4i`, label `target`, spectra_segment.spectra_split 60/20/20, seeded. Tuning reads the training and validation folds; every score here is on the test fold (2,000 rows, 235 positives per seed; 12 feature columns).

## Configurations tried

8 configurations, F166's grid, imported unchanged. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| l2_regularization 0.0, learning_rate 0.05, max_leaf_nodes 15 | 1 of 10 |
| l2_regularization 0.0, learning_rate 0.05, max_leaf_nodes 31 | 3 of 10 |
| l2_regularization 0.0, learning_rate 0.1, max_leaf_nodes 15 | 1 of 10 |
| l2_regularization 0.0, learning_rate 0.1, max_leaf_nodes 31 | 1 of 10 |
| l2_regularization 1.0, learning_rate 0.05, max_leaf_nodes 15 | 0 of 10 |
| l2_regularization 1.0, learning_rate 0.05, max_leaf_nodes 31 | 3 of 10 |
| l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 15 | 1 of 10 |
| l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 31 | 0 of 10 |

## Test-fold results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.6310 | 0.0140 | 0.6210 to 0.6410 |
| AUPRC, floor-normalized | 0.5818 | 0.0158 | 0.5705 to 0.5932 |
| ROC-AUC | 0.9283 | 0.0028 | 0.9263 to 0.9303 |
| Recall at the 0.5% budget, test fold | 0.0426 | 0.0000 | 0.0426 to 0.0426 |
| Train-test AUPRC gap | 0.2596 | 0.0573 | 0.2186 to 0.3006 |

Secondary, as the entry reports it: test AUPRC inside the pocket (`in_pocket` = 1) 0.6336 (95% t interval 0.6215 to 0.6456, 10 seeds) and outside it 0.6906 (0.6582 to 0.7230, 10 seeds).

At the max-F1 threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.5257 | 0.0287 | 0.5052 to 0.5462 |
| Recall | 0.7251 | 0.0600 | 0.6822 to 0.7680 |
| Specificity | 0.9117 | 0.0169 | 0.8996 to 0.9238 |
| F1 | 0.6071 | 0.0075 | 0.6017 to 0.6125 |
| MCC | 0.5563 | 0.0113 | 0.5483 to 0.5644 |
| Balanced accuracy | 0.8184 | 0.0218 | 0.8028 to 0.8340 |

At the 0.5% alert-budget threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.9879 | 0.0256 | 0.9696 to 1.0062 |
| Recall | 0.0447 | 0.0179 | 0.0319 to 0.0575 |
| Specificity | 0.9999 | 0.0002 | 0.9997 to 1.0001 |
| F1 | 0.0849 | 0.0324 | 0.0618 to 0.1081 |
| MCC | 0.1938 | 0.0369 | 0.1674 to 0.2202 |
| Balanced accuracy | 0.5223 | 0.0089 | 0.5159 to 0.5286 |

## Confusion counts per seed, test fold

TP, FP, TN and FN at each validation-chosen threshold, and at the test fold's own 0.5% budget (the comparison page's recall).

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN | 0.5% budget on the test fold: TP / FP / TN / FN |
|---|---|---|---|---|
| 42 | l2_regularization 0.0, learning_rate 0.05, max_leaf_nodes 15 | 196 / 210 / 1555 / 39 | 6 / 0 / 1765 / 229 | 10 / 0 / 1765 / 225 |
| 43 | l2_regularization 0.0, learning_rate 0.05, max_leaf_nodes 31 | 170 / 164 / 1601 / 65 | 8 / 0 / 1765 / 227 | 10 / 0 / 1765 / 225 |
| 44 | l2_regularization 0.0, learning_rate 0.1, max_leaf_nodes 15 | 169 / 155 / 1610 / 66 | 10 / 0 / 1765 / 225 | 10 / 0 / 1765 / 225 |
| 45 | l2_regularization 1.0, learning_rate 0.05, max_leaf_nodes 31 | 159 / 128 / 1637 / 76 | 7 / 0 / 1765 / 228 | 10 / 0 / 1765 / 225 |
| 46 | l2_regularization 0.0, learning_rate 0.05, max_leaf_nodes 31 | 165 / 142 / 1623 / 70 | 7 / 0 / 1765 / 228 | 10 / 0 / 1765 / 225 |
| 47 | l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 15 | 155 / 114 / 1651 / 80 | 7 / 0 / 1765 / 228 | 10 / 0 / 1765 / 225 |
| 48 | l2_regularization 0.0, learning_rate 0.05, max_leaf_nodes 31 | 179 / 174 / 1591 / 56 | 15 / 1 / 1764 / 220 | 10 / 0 / 1765 / 225 |
| 49 | l2_regularization 0.0, learning_rate 0.1, max_leaf_nodes 31 | 176 / 171 / 1594 / 59 | 17 / 0 / 1765 / 218 | 10 / 0 / 1765 / 225 |
| 50 | l2_regularization 1.0, learning_rate 0.05, max_leaf_nodes 31 | 185 / 179 / 1586 / 50 | 12 / 0 / 1765 / 223 | 10 / 0 / 1765 / 225 |
| 51 | l2_regularization 1.0, learning_rate 0.05, max_leaf_nodes 31 | 150 / 121 / 1644 / 85 | 16 / 1 / 1764 / 219 | 10 / 0 / 1765 / 225 |

## Limits

- One protocol and one grid per algorithm, F166's. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

