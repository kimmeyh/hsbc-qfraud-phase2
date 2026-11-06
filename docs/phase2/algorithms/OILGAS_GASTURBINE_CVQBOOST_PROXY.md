# CVQBoost proxy on SPECTRA oilgas_gasturbine: best result within F166's grid (F157)

**BLUF.** Tuned on validation and scored on the test fold over 10 seeds (42-51), CVQBoost proxy reaches a mean test AUPRC of 0.8394 (95% t interval 0.8339 to 0.8449). It is number 6 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [OILGAS_GASTURBINE_COMPARISON.md](OILGAS_GASTURBINE_COMPARISON.md).

- **Card**: F157 (Sprint 31 Task F, #98), the SPECTRA part: F166's algorithms and grids on SPECTRA's four datasets.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F157 SPECTRA part", written before any score.
- **Amendment**: the SVM lane is the form the entry's rule keeps, scored on the test fold under the entry's amendment of 2026-11-05 (Sprint 31 D14 option 1). The first result, `experiments/phase2/results/f157_spectra_algorithms.json`, is kept as recorded; it scored the linear form only. The amendment was written after that result was seen; the other six lanes are unchanged from it.
- **Evidence**: `experiments/phase2/results/f157_spectra_algorithms_rbf.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f157_spectra_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: SPECTRA `oilgas_gasturbine`, label `target`, spectra_segment.spectra_split 60/20/20, seeded. Tuning reads the training and validation folds; every score here is on the test fold (7,347 rows, 2,050 positives per seed; 15 feature columns).

## Configurations tried

3 configurations, F166's grid, imported unchanged. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| config free | 0 of 10 |
| config mid | 0 of 10 |
| config full | 10 of 10 |

The `full` configuration was chosen on every seed. Every pool was built serially; the chosen pool used 15 features and held 575 learners.

## Test-fold results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.8394 | 0.0077 | 0.8339 to 0.8449 |
| AUPRC, floor-normalized | 0.7772 | 0.0107 | 0.7696 to 0.7849 |
| ROC-AUC | 0.9059 | 0.0043 | 0.9029 to 0.9090 |
| Recall at the 0.5% budget, test fold | 0.0180 | 0.0003 | 0.0177 to 0.0182 |
| Train-test AUPRC gap | 0.1606 | 0.0077 | 0.1551 to 0.1661 |

Secondary, as the entry reports it: test AUPRC inside the pocket (`in_pocket` = 1) 0.7806 (95% t interval 0.7660 to 0.7952, 10 seeds) and outside it 0.9166 (0.9114 to 0.9218, 10 seeds).

At the max-F1 threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.7833 | 0.0245 | 0.7658 to 0.8009 |
| Recall | 0.6952 | 0.0188 | 0.6817 to 0.7086 |
| Specificity | 0.9251 | 0.0124 | 0.9162 to 0.9340 |
| F1 | 0.7361 | 0.0084 | 0.7301 to 0.7422 |
| MCC | 0.6447 | 0.0131 | 0.6353 to 0.6541 |
| Balanced accuracy | 0.8101 | 0.0061 | 0.8057 to 0.8145 |

At the 0.5% alert-budget threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.9948 | 0.0118 | 0.9864 to 1.0032 |
| Recall | 0.0182 | 0.0059 | 0.0140 to 0.0224 |
| Specificity | 0.9999 | 0.0001 | 0.9999 to 1.0000 |
| F1 | 0.0357 | 0.0113 | 0.0276 to 0.0438 |
| MCC | 0.1129 | 0.0174 | 0.1004 to 0.1253 |
| Balanced accuracy | 0.5091 | 0.0029 | 0.5070 to 0.5111 |

## Confusion counts per seed, test fold

TP, FP, TN and FN at each validation-chosen threshold, and at the test fold's own 0.5% budget (the comparison page's recall).

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN | 0.5% budget on the test fold: TP / FP / TN / FN |
|---|---|---|---|---|
| 42 | config full | 1455 / 392 / 4905 / 595 | 32 / 0 / 5297 / 2018 | 37 / 0 / 5297 / 2013 |
| 43 | config full | 1479 / 460 / 4837 / 571 | 58 / 1 / 5296 / 1992 | 37 / 0 / 5297 / 2013 |
| 44 | config full | 1443 / 525 / 4772 / 607 | 24 / 0 / 5297 / 2026 | 37 / 0 / 5297 / 2013 |
| 45 | config full | 1391 / 359 / 4938 / 659 | 55 / 2 / 5295 / 1995 | 35 / 2 / 5295 / 2015 |
| 46 | config full | 1485 / 453 / 4844 / 565 | 37 / 0 / 5297 / 2013 | 37 / 0 / 5297 / 2013 |
| 47 | config full | 1407 / 364 / 4933 / 643 | 36 / 0 / 5297 / 2014 | 37 / 0 / 5297 / 2013 |
| 48 | config full | 1427 / 392 / 4905 / 623 | 22 / 0 / 5297 / 2028 | 37 / 0 / 5297 / 2013 |
| 49 | config full | 1391 / 347 / 4950 / 659 | 29 / 0 / 5297 / 2021 | 37 / 0 / 5297 / 2013 |
| 50 | config full | 1392 / 380 / 4917 / 658 | 45 / 0 / 5297 / 2005 | 37 / 0 / 5297 / 2013 |
| 51 | config full | 1381 / 296 / 5001 / 669 | 35 / 0 / 5297 / 2015 | 37 / 0 / 5297 / 2013 |

## Limits

- One protocol and one grid per algorithm, F166's. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

