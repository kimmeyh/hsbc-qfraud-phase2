# CVQBoost proxy on SPECTRA maintenance_ai4i: best achievable result (F157)

**BLUF.** Tuned on validation and scored on the test fold over 10 seeds (42-51), CVQBoost proxy reaches a mean test AUPRC of 0.5387 (95% t interval 0.5225 to 0.5548). It is number 5 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [MAINTENANCE_AI4I_COMPARISON.md](MAINTENANCE_AI4I_COMPARISON.md).

- **Card**: F157 (Sprint 31 Task F, #98), the SPECTRA part: F166's algorithms and grids on SPECTRA's four datasets.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F157 SPECTRA part", written before any score.
- **Amendment**: the SVM lane is the form the entry's rule keeps, scored on the test fold under the entry's amendment of 2026-11-05 (Sprint 31 D14 option 1). The first result, `experiments/phase2/results/f157_spectra_algorithms.json`, is kept as recorded; it scored the linear form only.
- **Evidence**: `experiments/phase2/results/f157_spectra_algorithms_rbf.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f157_spectra_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: SPECTRA `maintenance_ai4i`, label `target`, spectra_segment.spectra_split 60/20/20, seeded. Tuning reads the training and validation folds; every score here is on the test fold (2,000 rows, 235 positives per seed; 12 feature columns).

## Configurations tried

3 configurations, F166's grid, imported unchanged. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| config free | 0 of 10 |
| config mid | 0 of 10 |
| config full | 10 of 10 |

The `full` configuration was chosen on every seed. Every pool was built serially; the chosen pool used 12 features and held 298 learners.

## Test-fold results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.5387 | 0.0226 | 0.5225 to 0.5548 |
| AUPRC, floor-normalized | 0.4772 | 0.0256 | 0.4589 to 0.4955 |
| ROC-AUC | 0.8974 | 0.0081 | 0.8916 to 0.9032 |
| Recall at the 0.5% budget, test fold | 0.0328 | 0.0035 | 0.0303 to 0.0353 |
| Train-test AUPRC gap | 0.4613 | 0.0226 | 0.4452 to 0.4775 |

Secondary, as the entry reports it: test AUPRC inside the pocket (`in_pocket` = 1) 0.5907 (95% t interval 0.5724 to 0.6089, 10 seeds) and outside it 0.4941 (0.4558 to 0.5324, 10 seeds).

At the max-F1 threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.4738 | 0.0309 | 0.4517 to 0.4959 |
| Recall | 0.7089 | 0.0574 | 0.6679 to 0.7500 |
| Specificity | 0.8936 | 0.0214 | 0.8783 to 0.9089 |
| F1 | 0.5657 | 0.0143 | 0.5554 to 0.5759 |
| MCC | 0.5098 | 0.0161 | 0.4982 to 0.5213 |
| Balanced accuracy | 0.8013 | 0.0193 | 0.7875 to 0.8151 |

At the 0.5% alert-budget threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.7621 | 0.0976 | 0.6922 to 0.8319 |
| Recall | 0.0281 | 0.0092 | 0.0215 to 0.0347 |
| Specificity | 0.9987 | 0.0008 | 0.9981 to 0.9993 |
| F1 | 0.0539 | 0.0171 | 0.0417 to 0.0661 |
| MCC | 0.1292 | 0.0200 | 0.1149 to 0.1435 |
| Balanced accuracy | 0.5134 | 0.0043 | 0.5103 to 0.5165 |

## Confusion counts per seed, test fold

TP, FP, TN and FN at each validation-chosen threshold, and at the test fold's own 0.5% budget (the comparison page's recall).

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN | 0.5% budget on the test fold: TP / FP / TN / FN |
|---|---|---|---|---|
| 42 | config full | 176 / 190 / 1575 / 59 | 7 / 3 / 1762 / 228 | 7 / 3 / 1762 / 228 |
| 43 | config full | 186 / 257 / 1508 / 49 | 9 / 4 / 1761 / 226 | 7 / 3 / 1762 / 228 |
| 44 | config full | 151 / 151 / 1614 / 84 | 5 / 2 / 1763 / 230 | 8 / 2 / 1763 / 227 |
| 45 | config full | 168 / 195 / 1570 / 67 | 3 / 1 / 1764 / 232 | 8 / 2 / 1763 / 227 |
| 46 | config full | 156 / 163 / 1602 / 79 | 5 / 0 / 1765 / 230 | 9 / 1 / 1764 / 226 |
| 47 | config full | 156 / 143 / 1622 / 79 | 6 / 2 / 1763 / 229 | 8 / 2 / 1763 / 227 |
| 48 | config full | 167 / 201 / 1564 / 68 | 5 / 1 / 1764 / 230 | 8 / 2 / 1763 / 227 |
| 49 | config full | 167 / 170 / 1595 / 68 | 8 / 4 / 1761 / 227 | 6 / 4 / 1761 / 229 |
| 50 | config full | 188 / 243 / 1522 / 47 | 10 / 4 / 1761 / 225 | 8 / 2 / 1763 / 227 |
| 51 | config full | 151 / 165 / 1600 / 84 | 8 / 2 / 1763 / 227 | 8 / 2 / 1763 / 227 |

## Limits

- One protocol and one grid per algorithm, F166's. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

