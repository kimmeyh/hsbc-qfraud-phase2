# LightGBM on SPECTRA energy_steel: best achievable result (F157)

**BLUF.** Tuned on validation and scored on the test fold over 10 seeds (42-51), LightGBM reaches a mean test AUPRC of 0.9570 (95% t interval 0.9187 to 0.9953). It is number 4 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [ENERGY_STEEL_COMPARISON.md](ENERGY_STEEL_COMPARISON.md).

- **Card**: F157 (Sprint 31 Task F, #98), the SPECTRA part: F166's algorithms and grids on SPECTRA's four datasets.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F157 SPECTRA part", written before any score.
- **Amendment**: the SVM lane is the form the entry's rule keeps, scored on the test fold under the entry's amendment of 2026-11-05 (Sprint 31 D14 option 1). The first result, `experiments/phase2/results/f157_spectra_algorithms.json`, is kept as recorded; it scored the linear form only.
- **Evidence**: `experiments/phase2/results/f157_spectra_algorithms_rbf.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f157_spectra_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: SPECTRA `energy_steel`, label `target`, spectra_segment.spectra_split 60/20/20, seeded. Tuning reads the training and validation folds; every score here is on the test fold (7,008 rows, 1,782 positives per seed; 17 feature columns).

## Configurations tried

8 configurations, F166's grid, imported unchanged. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| learning_rate 0.05, num_leaves 15, reg_lambda 0.0 | 0 of 10 |
| learning_rate 0.05, num_leaves 15, reg_lambda 1.0 | 0 of 10 |
| learning_rate 0.1, num_leaves 15, reg_lambda 0.0 | 1 of 10 |
| learning_rate 0.1, num_leaves 15, reg_lambda 1.0 | 1 of 10 |
| learning_rate 0.05, num_leaves 63, reg_lambda 0.0 | 2 of 10 |
| learning_rate 0.05, num_leaves 63, reg_lambda 1.0 | 5 of 10 |
| learning_rate 0.1, num_leaves 63, reg_lambda 0.0 | 0 of 10 |
| learning_rate 0.1, num_leaves 63, reg_lambda 1.0 | 1 of 10 |

## Test-fold results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.9570 | 0.0535 | 0.9187 to 0.9953 |
| AUPRC, floor-normalized | 0.9423 | 0.0717 | 0.8910 to 0.9936 |
| ROC-AUC | 0.9843 | 0.0185 | 0.9711 to 0.9976 |
| Recall at the 0.5% budget, test fold | 0.0202 | 0.0000 | 0.0202 to 0.0202 |
| Train-test AUPRC gap | 0.0425 | 0.0525 | 0.0050 to 0.0801 |

Secondary, as the entry reports it: test AUPRC inside the pocket (`in_pocket` = 1) 0.9549 (95% t interval 0.9352 to 0.9745, 10 seeds) and outside it 0.9551 (0.8990 to 1.0113, 10 seeds).

At the max-F1 threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.8667 | 0.1058 | 0.7911 to 0.9424 |
| Recall | 0.9366 | 0.0238 | 0.9196 to 0.9536 |
| Specificity | 0.9442 | 0.0548 | 0.9050 to 0.9834 |
| F1 | 0.8959 | 0.0538 | 0.8574 to 0.9344 |
| MCC | 0.8619 | 0.0696 | 0.8121 to 0.9117 |
| Balanced accuracy | 0.9404 | 0.0186 | 0.9271 to 0.9537 |

At the 0.5% alert-budget threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 1.0000 | 0.0000 | 1.0000 to 1.0000 |
| Recall | 0.0258 | 0.0224 | 0.0098 to 0.0419 |
| Specificity | 1.0000 | 0.0000 | 1.0000 to 1.0000 |
| F1 | 0.0495 | 0.0409 | 0.0203 to 0.0788 |
| MCC | 0.1313 | 0.0499 | 0.0956 to 0.1669 |
| Balanced accuracy | 0.5129 | 0.0112 | 0.5049 to 0.5209 |

## Confusion counts per seed, test fold

TP, FP, TN and FN at each validation-chosen threshold, and at the test fold's own 0.5% budget (the comparison page's recall).

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN | 0.5% budget on the test fold: TP / FP / TN / FN |
|---|---|---|---|---|
| 42 | learning_rate 0.1, num_leaves 63, reg_lambda 1.0 | 1678 / 182 / 5044 / 104 | 153 / 0 / 5226 / 1629 | 36 / 0 / 5226 / 1746 |
| 43 | learning_rate 0.05, num_leaves 63, reg_lambda 0.0 | 1642 / 102 / 5124 / 140 | 57 / 0 / 5226 / 1725 | 36 / 0 / 5226 / 1746 |
| 44 | learning_rate 0.1, num_leaves 15, reg_lambda 1.0 | 1744 / 836 / 4390 / 38 | 17 / 0 / 5226 / 1765 | 36 / 0 / 5226 / 1746 |
| 45 | learning_rate 0.1, num_leaves 15, reg_lambda 0.0 | 1747 / 766 / 4460 / 35 | 28 / 0 / 5226 / 1754 | 36 / 0 / 5226 / 1746 |
| 46 | learning_rate 0.05, num_leaves 63, reg_lambda 1.0 | 1650 / 169 / 5057 / 132 | 38 / 0 / 5226 / 1744 | 36 / 0 / 5226 / 1746 |
| 47 | learning_rate 0.05, num_leaves 63, reg_lambda 1.0 | 1645 / 113 / 5113 / 137 | 40 / 0 / 5226 / 1742 | 36 / 0 / 5226 / 1746 |
| 48 | learning_rate 0.05, num_leaves 63, reg_lambda 1.0 | 1650 / 103 / 5123 / 132 | 25 / 0 / 5226 / 1757 | 36 / 0 / 5226 / 1746 |
| 49 | learning_rate 0.05, num_leaves 63, reg_lambda 1.0 | 1626 / 429 / 4797 / 156 | 18 / 0 / 5226 / 1764 | 36 / 0 / 5226 / 1746 |
| 50 | learning_rate 0.05, num_leaves 63, reg_lambda 1.0 | 1648 / 99 / 5127 / 134 | 54 / 0 / 5226 / 1728 | 36 / 0 / 5226 / 1746 |
| 51 | learning_rate 0.05, num_leaves 63, reg_lambda 0.0 | 1660 / 118 / 5108 / 122 | 30 / 0 / 5226 / 1752 | 36 / 0 / 5226 / 1746 |

## Limits

- One protocol and one grid per algorithm, F166's. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

