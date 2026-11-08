# XGBoost on SPECTRA energy_steel: best result within F166's grid (F157)

**BLUF.** Tuned on validation and scored on the test fold over 10 seeds (42-51), XGBoost reaches a mean test AUPRC of 0.9669 (95% t interval 0.9396 to 0.9943). It is number 2 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [ENERGY_STEEL_COMPARISON.md](ENERGY_STEEL_COMPARISON.md).

- **Card**: F157 (Sprint 31 Task F, #98), the SPECTRA part: F166's algorithms and grids on SPECTRA's four datasets.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F157 SPECTRA part", written before any score.
- **Amendment**: the SVM lane is the form the entry's rule keeps, scored on the test fold under the entry's amendment of 2026-11-05 (Sprint 31 D14 option 1). The first result, `experiments/phase2/results/f157_spectra_algorithms.json`, is kept as recorded; it scored the linear form only. The amendment was written after that result was seen; the other six lanes are unchanged from it.
- **Evidence**: `experiments/phase2/results/f157_spectra_algorithms_rbf.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f157_spectra_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: SPECTRA `energy_steel`, label `target`, spectra_segment.spectra_split 60/20/20, seeded. Tuning reads the training and validation folds; every score here is on the test fold (7,008 rows, 1,782 positives per seed; 17 feature columns).

## Configurations tried

8 configurations, F166's grid, imported unchanged. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| learning_rate 0.1, max_depth 3, n_estimators 100 | 0 of 10 |
| learning_rate 0.1, max_depth 3, n_estimators 300 | 0 of 10 |
| learning_rate 0.3, max_depth 3, n_estimators 100 | 0 of 10 |
| learning_rate 0.3, max_depth 3, n_estimators 300 | 0 of 10 |
| learning_rate 0.1, max_depth 6, n_estimators 100 | 1 of 10 |
| learning_rate 0.1, max_depth 6, n_estimators 300 | 7 of 10 |
| learning_rate 0.3, max_depth 6, n_estimators 100 | 1 of 10 |
| learning_rate 0.3, max_depth 6, n_estimators 300 | 1 of 10 |

## Test-fold results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.9669 | 0.0382 | 0.9396 to 0.9943 |
| AUPRC, floor-normalized | 0.9557 | 0.0512 | 0.9190 to 0.9923 |
| ROC-AUC | 0.9875 | 0.0134 | 0.9779 to 0.9971 |
| Recall at the 0.5% budget, test fold | 0.0202 | 0.0000 | 0.0202 to 0.0202 |
| Train-test AUPRC gap | 0.0320 | 0.0384 | 0.0045 to 0.0595 |

Secondary, as the entry reports it: test AUPRC inside the pocket (`in_pocket` = 1) 0.9602 (95% t interval 0.9502 to 0.9701, 10 seeds) and outside it 0.9698 (0.9243 to 1.0153, 10 seeds).

At the max-F1 threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.8972 | 0.0621 | 0.8527 to 0.9416 |
| Recall | 0.8932 | 0.0685 | 0.8442 to 0.9421 |
| Specificity | 0.9642 | 0.0234 | 0.9474 to 0.9809 |
| F1 | 0.8937 | 0.0545 | 0.8548 to 0.9327 |
| MCC | 0.8589 | 0.0726 | 0.8070 to 0.9108 |
| Balanced accuracy | 0.9287 | 0.0391 | 0.9007 to 0.9566 |

At the 0.5% alert-budget threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 1.0000 | 0.0000 | 1.0000 to 1.0000 |
| Recall | 0.0293 | 0.0396 | 0.0009 to 0.0577 |
| Specificity | 1.0000 | 0.0000 | 1.0000 to 1.0000 |
| F1 | 0.0545 | 0.0687 | 0.0054 to 0.1037 |
| MCC | 0.1298 | 0.0778 | 0.0742 to 0.1854 |
| Balanced accuracy | 0.5146 | 0.0198 | 0.5005 to 0.5288 |

## Confusion counts per seed, test fold

TP, FP, TN and FN at each validation-chosen threshold, and at the test fold's own 0.5% budget (the comparison page's recall).

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN | 0.5% budget on the test fold: TP / FP / TN / FN |
|---|---|---|---|---|
| 42 | learning_rate 0.1, max_depth 6, n_estimators 300 | 1719 / 293 / 4933 / 63 | 250 / 0 / 5226 / 1532 | 36 / 0 / 5226 / 1746 |
| 43 | learning_rate 0.1, max_depth 6, n_estimators 300 | 1651 / 143 / 5083 / 131 | 43 / 0 / 5226 / 1739 | 36 / 0 / 5226 / 1746 |
| 44 | learning_rate 0.3, max_depth 6, n_estimators 100 | 1373 / 91 / 5135 / 409 | 37 / 0 / 5226 / 1745 | 36 / 0 / 5226 / 1746 |
| 45 | learning_rate 0.1, max_depth 6, n_estimators 300 | 1527 / 186 / 5040 / 255 | 24 / 0 / 5226 / 1758 | 36 / 0 / 5226 / 1746 |
| 46 | learning_rate 0.1, max_depth 6, n_estimators 300 | 1686 / 227 / 4999 / 96 | 22 / 0 / 5226 / 1760 | 36 / 0 / 5226 / 1746 |
| 47 | learning_rate 0.1, max_depth 6, n_estimators 300 | 1627 / 92 / 5134 / 155 | 38 / 0 / 5226 / 1744 | 36 / 0 / 5226 / 1746 |
| 48 | learning_rate 0.3, max_depth 6, n_estimators 300 | 1653 / 112 / 5114 / 129 | 43 / 0 / 5226 / 1739 | 36 / 0 / 5226 / 1746 |
| 49 | learning_rate 0.1, max_depth 6, n_estimators 300 | 1388 / 480 / 4746 / 394 | 1 / 0 / 5226 / 1781 | 36 / 0 / 5226 / 1746 |
| 50 | learning_rate 0.1, max_depth 6, n_estimators 100 | 1668 / 157 / 5069 / 114 | 37 / 0 / 5226 / 1745 | 36 / 0 / 5226 / 1746 |
| 51 | learning_rate 0.1, max_depth 6, n_estimators 300 | 1624 / 92 / 5134 / 158 | 27 / 0 / 5226 / 1755 | 36 / 0 / 5226 / 1746 |

## Limits

- One protocol and one grid per algorithm, F166's. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

