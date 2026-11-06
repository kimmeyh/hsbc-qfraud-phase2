# XGBoost on SPECTRA oilgas_gasturbine: best result within F166's grid (F157)

**BLUF.** Tuned on validation and scored on the test fold over 10 seeds (42-51), XGBoost reaches a mean test AUPRC of 0.8750 (95% t interval 0.8705 to 0.8794). It is number 3 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [OILGAS_GASTURBINE_COMPARISON.md](OILGAS_GASTURBINE_COMPARISON.md).

- **Card**: F157 (Sprint 31 Task F, #98), the SPECTRA part: F166's algorithms and grids on SPECTRA's four datasets.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F157 SPECTRA part", written before any score.
- **Amendment**: the SVM lane is the form the entry's rule keeps, scored on the test fold under the entry's amendment of 2026-11-05 (Sprint 31 D14 option 1). The first result, `experiments/phase2/results/f157_spectra_algorithms.json`, is kept as recorded; it scored the linear form only. The amendment was written after that result was seen; the other six lanes are unchanged from it.
- **Evidence**: `experiments/phase2/results/f157_spectra_algorithms_rbf.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f157_spectra_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: SPECTRA `oilgas_gasturbine`, label `target`, spectra_segment.spectra_split 60/20/20, seeded. Tuning reads the training and validation folds; every score here is on the test fold (7,347 rows, 2,050 positives per seed; 15 feature columns).

## Configurations tried

8 configurations, F166's grid, imported unchanged. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| learning_rate 0.1, max_depth 3, n_estimators 100 | 0 of 10 |
| learning_rate 0.1, max_depth 3, n_estimators 300 | 0 of 10 |
| learning_rate 0.3, max_depth 3, n_estimators 100 | 0 of 10 |
| learning_rate 0.3, max_depth 3, n_estimators 300 | 0 of 10 |
| learning_rate 0.1, max_depth 6, n_estimators 100 | 0 of 10 |
| learning_rate 0.1, max_depth 6, n_estimators 300 | 10 of 10 |
| learning_rate 0.3, max_depth 6, n_estimators 100 | 0 of 10 |
| learning_rate 0.3, max_depth 6, n_estimators 300 | 0 of 10 |

## Test-fold results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.8750 | 0.0062 | 0.8705 to 0.8794 |
| AUPRC, floor-normalized | 0.8266 | 0.0086 | 0.8204 to 0.8328 |
| ROC-AUC | 0.9315 | 0.0034 | 0.9291 to 0.9340 |
| Recall at the 0.5% budget, test fold | 0.0180 | 0.0000 | 0.0180 to 0.0180 |
| Train-test AUPRC gap | 0.0950 | 0.0068 | 0.0902 to 0.0998 |

Secondary, as the entry reports it: test AUPRC inside the pocket (`in_pocket` = 1) 0.7923 (95% t interval 0.7819 to 0.8026, 10 seeds) and outside it 0.9301 (0.9266 to 0.9337, 10 seeds).

At the max-F1 threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.7743 | 0.0281 | 0.7542 to 0.7944 |
| Recall | 0.7707 | 0.0157 | 0.7595 to 0.7819 |
| Specificity | 0.9124 | 0.0148 | 0.9018 to 0.9230 |
| F1 | 0.7720 | 0.0087 | 0.7658 to 0.7782 |
| MCC | 0.6844 | 0.0149 | 0.6737 to 0.6950 |
| Balanced accuracy | 0.8416 | 0.0044 | 0.8384 to 0.8447 |

At the 0.5% alert-budget threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 1.0000 | 0.0000 | 1.0000 to 1.0000 |
| Recall | 0.0184 | 0.0031 | 0.0162 to 0.0206 |
| Specificity | 1.0000 | 0.0000 | 1.0000 to 1.0000 |
| F1 | 0.0361 | 0.0060 | 0.0318 to 0.0404 |
| MCC | 0.1151 | 0.0098 | 0.1081 to 0.1221 |
| Balanced accuracy | 0.5092 | 0.0016 | 0.5081 to 0.5103 |

## Confusion counts per seed, test fold

TP, FP, TN and FN at each validation-chosen threshold, and at the test fold's own 0.5% budget (the comparison page's recall).

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN | 0.5% budget on the test fold: TP / FP / TN / FN |
|---|---|---|---|---|
| 42 | learning_rate 0.1, max_depth 6, n_estimators 300 | 1533 / 295 / 5002 / 517 | 44 / 0 / 5297 / 2006 | 37 / 0 / 5297 / 2013 |
| 43 | learning_rate 0.1, max_depth 6, n_estimators 300 | 1604 / 476 / 4821 / 446 | 43 / 0 / 5297 / 2007 | 37 / 0 / 5297 / 2013 |
| 44 | learning_rate 0.1, max_depth 6, n_estimators 300 | 1593 / 555 / 4742 / 457 | 32 / 0 / 5297 / 2018 | 37 / 0 / 5297 / 2013 |
| 45 | learning_rate 0.1, max_depth 6, n_estimators 300 | 1560 / 482 / 4815 / 490 | 37 / 0 / 5297 / 2013 | 37 / 0 / 5297 / 2013 |
| 46 | learning_rate 0.1, max_depth 6, n_estimators 300 | 1625 / 534 / 4763 / 425 | 31 / 0 / 5297 / 2019 | 37 / 0 / 5297 / 2013 |
| 47 | learning_rate 0.1, max_depth 6, n_estimators 300 | 1620 / 520 / 4777 / 430 | 49 / 0 / 5297 / 2001 | 37 / 0 / 5297 / 2013 |
| 48 | learning_rate 0.1, max_depth 6, n_estimators 300 | 1547 / 421 / 4876 / 503 | 29 / 0 / 5297 / 2021 | 37 / 0 / 5297 / 2013 |
| 49 | learning_rate 0.1, max_depth 6, n_estimators 300 | 1554 / 407 / 4890 / 496 | 36 / 0 / 5297 / 2014 | 37 / 0 / 5297 / 2013 |
| 50 | learning_rate 0.1, max_depth 6, n_estimators 300 | 1598 / 522 / 4775 / 452 | 35 / 0 / 5297 / 2015 | 37 / 0 / 5297 / 2013 |
| 51 | learning_rate 0.1, max_depth 6, n_estimators 300 | 1566 / 427 / 4870 / 484 | 41 / 0 / 5297 / 2009 | 37 / 0 / 5297 / 2013 |

## Limits

- One protocol and one grid per algorithm, F166's. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

