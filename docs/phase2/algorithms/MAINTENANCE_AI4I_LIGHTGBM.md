# LightGBM on SPECTRA maintenance_ai4i: best achievable result (F157)

**BLUF.** Tuned on validation and scored on the test fold over 10 seeds (42-51), LightGBM reaches a mean test AUPRC of 0.6148 (95% t interval 0.5992 to 0.6303). It is number 4 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [MAINTENANCE_AI4I_COMPARISON.md](MAINTENANCE_AI4I_COMPARISON.md).

- **Card**: F157 (Sprint 31 Task F, #98), the SPECTRA part: F166's algorithms and grids on SPECTRA's four datasets.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F157 SPECTRA part", written before any score.
- **Amendment**: the SVM lane is the form the entry's rule keeps, scored on the test fold under the entry's amendment of 2026-11-05 (Sprint 31 D14 option 1). The first result, `experiments/phase2/results/f157_spectra_algorithms.json`, is kept as recorded; it scored the linear form only.
- **Evidence**: `experiments/phase2/results/f157_spectra_algorithms_rbf.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f157_spectra_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: SPECTRA `maintenance_ai4i`, label `target`, spectra_segment.spectra_split 60/20/20, seeded. Tuning reads the training and validation folds; every score here is on the test fold (2,000 rows, 235 positives per seed; 12 feature columns).

## Configurations tried

8 configurations, F166's grid, imported unchanged. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| learning_rate 0.05, num_leaves 15, reg_lambda 0.0 | 4 of 10 |
| learning_rate 0.05, num_leaves 15, reg_lambda 1.0 | 1 of 10 |
| learning_rate 0.1, num_leaves 15, reg_lambda 0.0 | 0 of 10 |
| learning_rate 0.1, num_leaves 15, reg_lambda 1.0 | 0 of 10 |
| learning_rate 0.05, num_leaves 63, reg_lambda 0.0 | 2 of 10 |
| learning_rate 0.05, num_leaves 63, reg_lambda 1.0 | 2 of 10 |
| learning_rate 0.1, num_leaves 63, reg_lambda 0.0 | 1 of 10 |
| learning_rate 0.1, num_leaves 63, reg_lambda 1.0 | 0 of 10 |

## Test-fold results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.6148 | 0.0217 | 0.5992 to 0.6303 |
| AUPRC, floor-normalized | 0.5635 | 0.0246 | 0.5459 to 0.5811 |
| ROC-AUC | 0.9244 | 0.0034 | 0.9219 to 0.9268 |
| Recall at the 0.5% budget, test fold | 0.0396 | 0.0029 | 0.0375 to 0.0416 |
| Train-test AUPRC gap | 0.3553 | 0.0501 | 0.3194 to 0.3911 |

Secondary, as the entry reports it: test AUPRC inside the pocket (`in_pocket` = 1) 0.6284 (95% t interval 0.6137 to 0.6431, 10 seeds) and outside it 0.6624 (0.6128 to 0.7119, 10 seeds).

At the max-F1 threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.5330 | 0.0304 | 0.5113 to 0.5547 |
| Recall | 0.6655 | 0.0688 | 0.6163 to 0.7147 |
| Specificity | 0.9212 | 0.0165 | 0.9094 to 0.9330 |
| F1 | 0.5889 | 0.0172 | 0.5766 to 0.6012 |
| MCC | 0.5336 | 0.0201 | 0.5192 to 0.5480 |
| Balanced accuracy | 0.7934 | 0.0268 | 0.7742 to 0.8125 |

At the 0.5% alert-budget threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.9080 | 0.0826 | 0.8489 to 0.9670 |
| Recall | 0.0417 | 0.0137 | 0.0319 to 0.0515 |
| Specificity | 0.9994 | 0.0005 | 0.9991 to 0.9998 |
| F1 | 0.0794 | 0.0251 | 0.0615 to 0.0974 |
| MCC | 0.1788 | 0.0337 | 0.1546 to 0.2029 |
| Balanced accuracy | 0.5206 | 0.0068 | 0.5157 to 0.5255 |

## Confusion counts per seed, test fold

TP, FP, TN and FN at each validation-chosen threshold, and at the test fold's own 0.5% budget (the comparison page's recall).

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN | 0.5% budget on the test fold: TP / FP / TN / FN |
|---|---|---|---|---|
| 42 | learning_rate 0.05, num_leaves 63, reg_lambda 1.0 | 168 / 154 / 1611 / 67 | 10 / 1 / 1764 / 225 | 9 / 1 / 1764 / 226 |
| 43 | learning_rate 0.05, num_leaves 63, reg_lambda 0.0 | 135 / 116 / 1649 / 100 | 6 / 2 / 1763 / 229 | 8 / 2 / 1763 / 227 |
| 44 | learning_rate 0.05, num_leaves 15, reg_lambda 0.0 | 181 / 187 / 1578 / 54 | 6 / 0 / 1765 / 229 | 10 / 0 / 1765 / 225 |
| 45 | learning_rate 0.05, num_leaves 63, reg_lambda 0.0 | 164 / 148 / 1617 / 71 | 7 / 1 / 1764 / 228 | 9 / 1 / 1764 / 226 |
| 46 | learning_rate 0.05, num_leaves 15, reg_lambda 1.0 | 162 / 132 / 1633 / 73 | 9 / 0 / 1765 / 226 | 10 / 0 / 1765 / 225 |
| 47 | learning_rate 0.05, num_leaves 15, reg_lambda 0.0 | 132 / 89 / 1676 / 103 | 9 / 1 / 1764 / 226 | 9 / 1 / 1764 / 226 |
| 48 | learning_rate 0.05, num_leaves 15, reg_lambda 0.0 | 172 / 178 / 1587 / 63 | 14 / 1 / 1764 / 221 | 10 / 0 / 1765 / 225 |
| 49 | learning_rate 0.1, num_leaves 63, reg_lambda 0.0 | 142 / 120 / 1645 / 93 | 13 / 3 / 1762 / 222 | 9 / 1 / 1764 / 226 |
| 50 | learning_rate 0.05, num_leaves 15, reg_lambda 0.0 | 156 / 131 / 1634 / 79 | 15 / 0 / 1765 / 220 | 10 / 0 / 1765 / 225 |
| 51 | learning_rate 0.05, num_leaves 63, reg_lambda 1.0 | 152 / 136 / 1629 / 83 | 9 / 1 / 1764 / 226 | 9 / 1 / 1764 / 226 |

## Limits

- One protocol and one grid per algorithm, F166's. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

