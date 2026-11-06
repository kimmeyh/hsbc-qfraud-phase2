# SVM on SPECTRA oilgas_gasturbine: best result within F166's grid (F157)

**BLUF.** Tuned on validation and scored on the test fold over 10 seeds (42-51), SVM reaches a mean test AUPRC of 0.8532 (95% t interval 0.8478 to 0.8587). It is number 5 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [OILGAS_GASTURBINE_COMPARISON.md](OILGAS_GASTURBINE_COMPARISON.md).

- **Card**: F157 (Sprint 31 Task F, #98), the SPECTRA part: F166's algorithms and grids on SPECTRA's four datasets.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F157 SPECTRA part", written before any score.
- **Amendment**: the SVM lane is the form the entry's rule keeps, scored on the test fold under the entry's amendment of 2026-11-05 (Sprint 31 D14 option 1). The first result, `experiments/phase2/results/f157_spectra_algorithms.json`, is kept as recorded; it scored the linear form only. The amendment was written after that result was seen; the other six lanes are unchanged from it.
- **Evidence**: `experiments/phase2/results/f157_spectra_algorithms_rbf.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f157_spectra_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: SPECTRA `oilgas_gasturbine`, label `target`, spectra_segment.spectra_split 60/20/20, seeded. Tuning reads the training and validation folds; every score here is on the test fold (7,347 rows, 2,050 positives per seed; 15 feature columns).

## Configurations tried

2 configurations, F166's grid, imported unchanged. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| C 1.0 | 0 of 10 |
| C 10.0 | 10 of 10 |

## The SVM's form

The RBF SVM is fitted on a stratified subsample of at most 20,000 training rows (the whole fold when smaller). The entry keeps the RBF form only if its best validation AUPRC beats the linear form's on a majority of seeds. It did so on 10 of 10 seeds, so the entry's rule keeps the **rbf** form. Every SVM figure here, its place in the order and its adjacent pairs are the RBF form's, scored on the test fold under the D14 amendment. The linear form is reported on the SVM page, not ranked.

The linear form (`LinearSVC`, all training rows, F166's grid), which the rule did not keep: mean test AUPRC 0.7802 over 10 seeds, from 0.7710 to 0.7873 (the SVM figures of `experiments/phase2/results/f157_spectra_algorithms.json`). It is not ranked.

The chosen C is the grid's largest value, 10, on 10 of 10 seeds, so a larger C may do better; the grid is the entry's, not widened here.

## Test-fold results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.8532 | 0.0076 | 0.8478 to 0.8587 |
| AUPRC, floor-normalized | 0.7964 | 0.0105 | 0.7889 to 0.8040 |
| ROC-AUC | 0.9135 | 0.0053 | 0.9097 to 0.9173 |
| Recall at the 0.5% budget, test fold | 0.0179 | 0.0003 | 0.0177 to 0.0180 |
| Train-test AUPRC gap | 0.0208 | 0.0085 | 0.0147 to 0.0269 |

Secondary, as the entry reports it: test AUPRC inside the pocket (`in_pocket` = 1) 0.7540 (95% t interval 0.7412 to 0.7667, 10 seeds) and outside it 0.9264 (0.9224 to 0.9303, 10 seeds).

At the max-F1 threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.8049 | 0.0296 | 0.7837 to 0.8261 |
| Recall | 0.7125 | 0.0235 | 0.6957 to 0.7293 |
| Specificity | 0.9324 | 0.0157 | 0.9211 to 0.9436 |
| F1 | 0.7551 | 0.0060 | 0.7508 to 0.7594 |
| MCC | 0.6710 | 0.0109 | 0.6632 to 0.6788 |
| Balanced accuracy | 0.8225 | 0.0053 | 0.8187 to 0.8262 |

At the 0.5% alert-budget threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.9889 | 0.0152 | 0.9779 to 0.9998 |
| Recall | 0.0186 | 0.0054 | 0.0147 to 0.0225 |
| Specificity | 0.9999 | 0.0001 | 0.9999 to 1.0000 |
| F1 | 0.0364 | 0.0104 | 0.0290 to 0.0439 |
| MCC | 0.1139 | 0.0169 | 0.1018 to 0.1260 |
| Balanced accuracy | 0.5093 | 0.0027 | 0.5073 to 0.5112 |

## Confusion counts per seed, test fold

TP, FP, TN and FN at each validation-chosen threshold, and at the test fold's own 0.5% budget (the comparison page's recall).

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN | 0.5% budget on the test fold: TP / FP / TN / FN |
|---|---|---|---|---|
| 42 | C 10.0 | 1475 / 347 / 4950 / 575 | 40 / 0 / 5297 / 2010 | 37 / 0 / 5297 / 2013 |
| 43 | C 10.0 | 1574 / 555 / 4742 / 476 | 33 / 0 / 5297 / 2017 | 36 / 1 / 5296 / 2014 |
| 44 | C 10.0 | 1411 / 330 / 4967 / 639 | 25 / 1 / 5296 / 2025 | 36 / 1 / 5296 / 2014 |
| 45 | C 10.0 | 1491 / 431 / 4866 / 559 | 33 / 1 / 5296 / 2017 | 36 / 1 / 5296 / 2014 |
| 46 | C 10.0 | 1425 / 275 / 5022 / 625 | 57 / 1 / 5296 / 1993 | 37 / 0 / 5297 / 2013 |
| 47 | C 10.0 | 1470 / 324 / 4973 / 580 | 54 / 0 / 5297 / 1996 | 37 / 0 / 5297 / 2013 |
| 48 | C 10.0 | 1441 / 345 / 4952 / 609 | 37 / 1 / 5296 / 2013 | 36 / 1 / 5296 / 2014 |
| 49 | C 10.0 | 1469 / 384 / 4913 / 581 | 27 / 0 / 5297 / 2023 | 37 / 0 / 5297 / 2013 |
| 50 | C 10.0 | 1433 / 313 / 4984 / 617 | 29 / 0 / 5297 / 2021 | 37 / 0 / 5297 / 2013 |
| 51 | C 10.0 | 1418 / 278 / 5019 / 632 | 46 / 0 / 5297 / 2004 | 37 / 0 / 5297 / 2013 |

## Limits

- One protocol and one grid per algorithm, F166's. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

