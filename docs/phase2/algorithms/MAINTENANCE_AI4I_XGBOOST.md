# XGBoost on SPECTRA maintenance_ai4i: best result within F166's grid (F157)

**BLUF.** Tuned on validation and scored on the test fold over 10 seeds (42-51), XGBoost reaches a mean test AUPRC of 0.6183 (95% t interval 0.6034 to 0.6331). It is number 3 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [MAINTENANCE_AI4I_COMPARISON.md](MAINTENANCE_AI4I_COMPARISON.md).

- **Card**: F157 (Sprint 31 Task F, #98), the SPECTRA part: F166's algorithms and grids on SPECTRA's four datasets.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F157 SPECTRA part", written before any score.
- **Amendment**: the SVM lane is the form the entry's rule keeps, scored on the test fold under the entry's amendment of 2026-11-05 (Sprint 31 D14 option 1). The first result, `experiments/phase2/results/f157_spectra_algorithms.json`, is kept as recorded; it scored the linear form only. The amendment was written after that result was seen; the other six lanes are unchanged from it.
- **Evidence**: `experiments/phase2/results/f157_spectra_algorithms_rbf.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f157_spectra_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: SPECTRA `maintenance_ai4i`, label `target`, spectra_segment.spectra_split 60/20/20, seeded. Tuning reads the training and validation folds; every score here is on the test fold (2,000 rows, 235 positives per seed; 12 feature columns).

## Configurations tried

8 configurations, F166's grid, imported unchanged. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| learning_rate 0.1, max_depth 3, n_estimators 100 | 3 of 10 |
| learning_rate 0.1, max_depth 3, n_estimators 300 | 0 of 10 |
| learning_rate 0.3, max_depth 3, n_estimators 100 | 0 of 10 |
| learning_rate 0.3, max_depth 3, n_estimators 300 | 0 of 10 |
| learning_rate 0.1, max_depth 6, n_estimators 100 | 6 of 10 |
| learning_rate 0.1, max_depth 6, n_estimators 300 | 0 of 10 |
| learning_rate 0.3, max_depth 6, n_estimators 100 | 1 of 10 |
| learning_rate 0.3, max_depth 6, n_estimators 300 | 0 of 10 |

## Test-fold results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.6183 | 0.0208 | 0.6034 to 0.6331 |
| AUPRC, floor-normalized | 0.5674 | 0.0236 | 0.5505 to 0.5843 |
| ROC-AUC | 0.9266 | 0.0039 | 0.9238 to 0.9294 |
| Recall at the 0.5% budget, test fold | 0.0409 | 0.0022 | 0.0393 to 0.0424 |
| Train-test AUPRC gap | 0.2640 | 0.1007 | 0.1920 to 0.3360 |

Secondary, as the entry reports it: test AUPRC inside the pocket (`in_pocket` = 1) 0.6276 (95% t interval 0.6059 to 0.6493, 10 seeds) and outside it 0.6681 (0.6318 to 0.7044, 10 seeds).

At the max-F1 threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.5135 | 0.0332 | 0.4897 to 0.5372 |
| Recall | 0.7230 | 0.0462 | 0.6899 to 0.7560 |
| Specificity | 0.9078 | 0.0157 | 0.8965 to 0.9190 |
| F1 | 0.5989 | 0.0198 | 0.5847 to 0.6130 |
| MCC | 0.5466 | 0.0229 | 0.5302 to 0.5630 |
| Balanced accuracy | 0.8154 | 0.0179 | 0.8026 to 0.8282 |

At the 0.5% alert-budget threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.9527 | 0.0607 | 0.9093 to 0.9961 |
| Recall | 0.0464 | 0.0202 | 0.0319 to 0.0608 |
| Specificity | 0.9995 | 0.0007 | 0.9990 to 1.0000 |
| F1 | 0.0876 | 0.0363 | 0.0617 to 0.1136 |
| MCC | 0.1911 | 0.0389 | 0.1633 to 0.2189 |
| Balanced accuracy | 0.5230 | 0.0098 | 0.5159 to 0.5300 |

## Confusion counts per seed, test fold

TP, FP, TN and FN at each validation-chosen threshold, and at the test fold's own 0.5% budget (the comparison page's recall).

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN | 0.5% budget on the test fold: TP / FP / TN / FN |
|---|---|---|---|---|
| 42 | learning_rate 0.1, max_depth 3, n_estimators 100 | 168 / 132 / 1633 / 67 | 4 / 0 / 1765 / 231 | 10 / 0 / 1765 / 225 |
| 43 | learning_rate 0.1, max_depth 6, n_estimators 100 | 187 / 207 / 1558 / 48 | 9 / 0 / 1765 / 226 | 10 / 0 / 1765 / 225 |
| 44 | learning_rate 0.1, max_depth 3, n_estimators 100 | 183 / 184 / 1581 / 52 | 8 / 0 / 1765 / 227 | 10 / 0 / 1765 / 225 |
| 45 | learning_rate 0.3, max_depth 6, n_estimators 100 | 159 / 174 / 1591 / 76 | 6 / 0 / 1765 / 229 | 9 / 1 / 1764 / 226 |
| 46 | learning_rate 0.1, max_depth 6, n_estimators 100 | 157 / 130 / 1635 / 78 | 9 / 1 / 1764 / 226 | 9 / 1 / 1764 / 226 |
| 47 | learning_rate 0.1, max_depth 6, n_estimators 100 | 164 / 136 / 1629 / 71 | 10 / 0 / 1765 / 225 | 10 / 0 / 1765 / 225 |
| 48 | learning_rate 0.1, max_depth 6, n_estimators 100 | 170 / 174 / 1591 / 65 | 17 / 1 / 1764 / 218 | 10 / 0 / 1765 / 225 |
| 49 | learning_rate 0.1, max_depth 3, n_estimators 100 | 183 / 180 / 1585 / 52 | 18 / 4 / 1761 / 217 | 9 / 1 / 1764 / 226 |
| 50 | learning_rate 0.1, max_depth 6, n_estimators 100 | 160 / 132 / 1633 / 75 | 12 / 1 / 1764 / 223 | 9 / 1 / 1764 / 226 |
| 51 | learning_rate 0.1, max_depth 6, n_estimators 100 | 168 / 179 / 1586 / 67 | 16 / 1 / 1764 / 219 | 10 / 0 / 1765 / 225 |

## Limits

- One protocol and one grid per algorithm, F166's. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

