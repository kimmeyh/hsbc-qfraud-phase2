# SVM on SPECTRA telecom_churn: best result within F166's grid (F157)

**BLUF.** Tuned on validation and scored on the test fold over 10 seeds (42-51), SVM reaches a mean test AUPRC of 0.8441 (95% t interval 0.8253 to 0.8630). It is number 5 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [TELECOM_CHURN_COMPARISON.md](TELECOM_CHURN_COMPARISON.md).

- **Card**: F157 (Sprint 31 Task F, #98), the SPECTRA part: F166's algorithms and grids on SPECTRA's four datasets.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F157 SPECTRA part", written before any score.
- **Amendment**: the SVM lane is the form the entry's rule keeps, scored on the test fold under the entry's amendment of 2026-11-05 (Sprint 31 D14 option 1). The first result, `experiments/phase2/results/f157_spectra_algorithms.json`, is kept as recorded; it scored the linear form only. The amendment was written after that result was seen; the other six lanes are unchanged from it.
- **Evidence**: `experiments/phase2/results/f157_spectra_algorithms_rbf.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f157_spectra_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: SPECTRA `telecom_churn`, label `target`, spectra_segment.spectra_split 60/20/20, seeded. Tuning reads the training and validation folds; every score here is on the test fold (630 rows, 152 to 153 positives per seed; 17 feature columns).

## Configurations tried

2 configurations, F166's grid, imported unchanged. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| C 1.0 | 0 of 10 |
| C 10.0 | 10 of 10 |

## The SVM's form

The RBF SVM is fitted on a stratified subsample of at most 20,000 training rows (the whole fold when smaller). The entry keeps the RBF form only if its best validation AUPRC beats the linear form's on a majority of seeds. It did so on 10 of 10 seeds, so the entry's rule keeps the **rbf** form. Every SVM figure here, its place in the order and its adjacent pairs are the RBF form's, scored on the test fold under the D14 amendment. The linear form is reported on the SVM page, not ranked.

The linear form (`LinearSVC`, all training rows, F166's grid), which the rule did not keep: mean test AUPRC 0.6535 over 10 seeds, from 0.6218 to 0.7150 (the SVM figures of `experiments/phase2/results/f157_spectra_algorithms.json`). It is not ranked.

The chosen C is the grid's largest value, 10, on 10 of 10 seeds, so a larger C may do better; the grid is the entry's, not widened here.

## Test-fold results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.8441 | 0.0263 | 0.8253 to 0.8630 |
| AUPRC, floor-normalized | 0.7944 | 0.0348 | 0.7696 to 0.8193 |
| ROC-AUC | 0.9352 | 0.0084 | 0.9291 to 0.9412 |
| Recall at the 0.5% budget, test fold | 0.0263 | 0.0001 | 0.0262 to 0.0263 |
| Train-test AUPRC gap | 0.0618 | 0.0272 | 0.0424 to 0.0813 |

Secondary, as the entry reports it: test AUPRC inside the pocket (`in_pocket` = 1) 0.6796 (95% t interval 0.6370 to 0.7222, 10 seeds) and outside it 0.9161 (0.9061 to 0.9261, 10 seeds).

At the max-F1 threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.7539 | 0.0381 | 0.7266 to 0.7811 |
| Recall | 0.7846 | 0.0548 | 0.7454 to 0.8238 |
| Specificity | 0.9173 | 0.0196 | 0.9033 to 0.9313 |
| F1 | 0.7674 | 0.0301 | 0.7458 to 0.7889 |
| MCC | 0.6929 | 0.0388 | 0.6651 to 0.7206 |
| Balanced accuracy | 0.8510 | 0.0243 | 0.8335 to 0.8684 |

At the 0.5% alert-budget threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 1.0000 | 0.0000 | 1.0000 to 1.0000 |
| Recall | 0.0263 | 0.0158 | 0.0150 to 0.0376 |
| Specificity | 1.0000 | 0.0000 | 1.0000 to 1.0000 |
| F1 | 0.0508 | 0.0300 | 0.0293 to 0.0722 |
| MCC | 0.1350 | 0.0457 | 0.1023 to 0.1676 |
| Balanced accuracy | 0.5131 | 0.0079 | 0.5075 to 0.5188 |

## Confusion counts per seed, test fold

TP, FP, TN and FN at each validation-chosen threshold, and at the test fold's own 0.5% budget (the comparison page's recall).

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN | 0.5% budget on the test fold: TP / FP / TN / FN |
|---|---|---|---|---|
| 42 | C 10.0 | 122 / 30 / 448 / 30 | 6 / 0 / 478 / 146 | 4 / 0 / 478 / 148 |
| 43 | C 10.0 | 116 / 40 / 438 / 36 | 6 / 0 / 478 / 146 | 4 / 0 / 478 / 148 |
| 44 | C 10.0 | 104 / 34 / 444 / 48 | 6 / 0 / 478 / 146 | 4 / 0 / 478 / 148 |
| 45 | C 10.0 | 122 / 55 / 422 / 31 | 4 / 0 / 477 / 149 | 4 / 0 / 477 / 149 |
| 46 | C 10.0 | 112 / 29 / 448 / 41 | 3 / 0 / 477 / 150 | 4 / 0 / 477 / 149 |
| 47 | C 10.0 | 135 / 44 / 433 / 18 | 3 / 0 / 477 / 150 | 4 / 0 / 477 / 149 |
| 48 | C 10.0 | 127 / 54 / 424 / 25 | 1 / 0 / 478 / 151 | 4 / 0 / 478 / 148 |
| 49 | C 10.0 | 118 / 42 / 436 / 34 | 8 / 0 / 478 / 144 | 4 / 0 / 478 / 148 |
| 50 | C 10.0 | 123 / 32 / 446 / 29 | 2 / 0 / 478 / 150 | 4 / 0 / 478 / 148 |
| 51 | C 10.0 | 116 / 35 / 443 / 36 | 1 / 0 / 478 / 151 | 4 / 0 / 478 / 148 |

## Limits

- One protocol and one grid per algorithm, F166's. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

