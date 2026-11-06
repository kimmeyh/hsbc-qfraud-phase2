# CVQBoost proxy on SPECTRA energy_steel: best achievable result (F157)

**BLUF.** Tuned on validation and scored on the test fold over 10 seeds (42-51), CVQBoost proxy reaches a mean test AUPRC of 0.9186 (95% t interval 0.9032 to 0.9340). It is number 5 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [ENERGY_STEEL_COMPARISON.md](ENERGY_STEEL_COMPARISON.md).

- **Card**: F157 (Sprint 31 Task F, #98), the SPECTRA part: F166's algorithms and grids on SPECTRA's four datasets.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F157 SPECTRA part", written before any score.
- **Amendment**: the SVM lane is the form the entry's rule keeps, scored on the test fold under the entry's amendment of 2026-11-05 (Sprint 31 D14 option 1). The first result, `experiments/phase2/results/f157_spectra_algorithms.json`, is kept as recorded; it scored the linear form only.
- **Evidence**: `experiments/phase2/results/f157_spectra_algorithms_rbf.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f157_spectra_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: SPECTRA `energy_steel`, label `target`, spectra_segment.spectra_split 60/20/20, seeded. Tuning reads the training and validation folds; every score here is on the test fold (7,008 rows, 1,782 positives per seed; 17 feature columns).

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
| AUPRC | 0.9186 | 0.0215 | 0.9032 to 0.9340 |
| AUPRC, floor-normalized | 0.8908 | 0.0289 | 0.8701 to 0.9114 |
| ROC-AUC | 0.9729 | 0.0070 | 0.9679 to 0.9779 |
| Recall at the 0.5% budget, test fold | 0.0200 | 0.0003 | 0.0198 to 0.0202 |
| Train-test AUPRC gap | 0.0814 | 0.0215 | 0.0660 to 0.0968 |

Secondary, as the entry reports it: test AUPRC inside the pocket (`in_pocket` = 1) 0.9362 (95% t interval 0.9252 to 0.9473, 10 seeds) and outside it 0.9031 (0.8809 to 0.9253, 10 seeds).

At the max-F1 threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.8212 | 0.0474 | 0.7873 to 0.8551 |
| Recall | 0.8553 | 0.0456 | 0.8227 to 0.8879 |
| Specificity | 0.9349 | 0.0237 | 0.9179 to 0.9518 |
| F1 | 0.8361 | 0.0249 | 0.8183 to 0.8539 |
| MCC | 0.7804 | 0.0324 | 0.7572 to 0.8036 |
| Balanced accuracy | 0.8951 | 0.0183 | 0.8820 to 0.9082 |

At the 0.5% alert-budget threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.8932 | 0.3140 | 0.6685 to 1.1178 |
| Recall | 0.0277 | 0.0355 | 0.0022 to 0.0531 |
| Specificity | 0.9999 | 0.0001 | 0.9999 to 1.0000 |
| F1 | 0.0519 | 0.0625 | 0.0072 to 0.0966 |
| MCC | 0.1243 | 0.0770 | 0.0693 to 0.1794 |
| Balanced accuracy | 0.5138 | 0.0178 | 0.5011 to 0.5265 |

## Confusion counts per seed, test fold

TP, FP, TN and FN at each validation-chosen threshold, and at the test fold's own 0.5% budget (the comparison page's recall).

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN | 0.5% budget on the test fold: TP / FP / TN / FN |
|---|---|---|---|---|
| 42 | config full | 1529 / 423 / 4803 / 253 | 225 / 0 / 5226 / 1557 | 36 / 0 / 5226 / 1746 |
| 43 | config full | 1642 / 602 / 4624 / 140 | 43 / 1 / 5225 / 1739 | 35 / 1 / 5225 / 1747 |
| 44 | config full | 1541 / 439 / 4787 / 241 | 36 / 1 / 5225 / 1746 | 35 / 1 / 5225 / 1747 |
| 45 | config full | 1522 / 364 / 4862 / 260 | 20 / 0 / 5226 / 1762 | 36 / 0 / 5226 / 1746 |
| 46 | config full | 1503 / 351 / 4875 / 279 | 23 / 0 / 5226 / 1759 | 36 / 0 / 5226 / 1746 |
| 47 | config full | 1558 / 286 / 4940 / 224 | 53 / 1 / 5225 / 1729 | 35 / 1 / 5225 / 1747 |
| 48 | config full | 1531 / 213 / 5013 / 251 | 29 / 0 / 5226 / 1753 | 36 / 0 / 5226 / 1746 |
| 49 | config full | 1328 / 218 / 5008 / 454 | 0 / 0 / 5226 / 1782 | 36 / 0 / 5226 / 1746 |
| 50 | config full | 1590 / 294 / 4932 / 192 | 34 / 0 / 5226 / 1748 | 36 / 0 / 5226 / 1746 |
| 51 | config full | 1497 / 214 / 5012 / 285 | 30 / 0 / 5226 / 1752 | 36 / 0 / 5226 / 1746 |

## Limits

- One protocol and one grid per algorithm, F166's. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

