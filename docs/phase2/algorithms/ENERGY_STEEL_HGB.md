# HGB on SPECTRA energy_steel: best achievable result (F157)

**BLUF.** Tuned on validation and scored on the test fold over 10 seeds (42-51), HGB reaches a mean test AUPRC of 0.9582 (95% t interval 0.9168 to 0.9995). It is number 3 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [ENERGY_STEEL_COMPARISON.md](ENERGY_STEEL_COMPARISON.md).

- **Card**: F157 (Sprint 31 Task F, #98), the SPECTRA part: F166's algorithms and grids on SPECTRA's four datasets.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F157 SPECTRA part", written before any score.
- **Amendment**: the SVM lane is the form the entry's rule keeps, scored on the test fold under the entry's amendment of 2026-11-05 (Sprint 31 D14 option 1). The first result, `experiments/phase2/results/f157_spectra_algorithms.json`, is kept as recorded; it scored the linear form only.
- **Evidence**: `experiments/phase2/results/f157_spectra_algorithms_rbf.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f157_spectra_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: SPECTRA `energy_steel`, label `target`, spectra_segment.spectra_split 60/20/20, seeded. Tuning reads the training and validation folds; every score here is on the test fold (7,008 rows, 1,782 positives per seed; 17 feature columns).

## Configurations tried

8 configurations, F166's grid, imported unchanged. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| l2_regularization 0.0, learning_rate 0.05, max_leaf_nodes 15 | 0 of 10 |
| l2_regularization 0.0, learning_rate 0.05, max_leaf_nodes 31 | 0 of 10 |
| l2_regularization 0.0, learning_rate 0.1, max_leaf_nodes 15 | 0 of 10 |
| l2_regularization 0.0, learning_rate 0.1, max_leaf_nodes 31 | 3 of 10 |
| l2_regularization 1.0, learning_rate 0.05, max_leaf_nodes 15 | 0 of 10 |
| l2_regularization 1.0, learning_rate 0.05, max_leaf_nodes 31 | 1 of 10 |
| l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 15 | 1 of 10 |
| l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 31 | 5 of 10 |

## Test-fold results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.9582 | 0.0578 | 0.9168 to 0.9995 |
| AUPRC, floor-normalized | 0.9439 | 0.0775 | 0.8885 to 0.9993 |
| ROC-AUC | 0.9849 | 0.0193 | 0.9711 to 0.9987 |
| Recall at the 0.5% budget, test fold | 0.0204 | 0.0007 | 0.0199 to 0.0209 |
| Train-test AUPRC gap | 0.0364 | 0.0577 | -0.0049 to 0.0776 |

Secondary, as the entry reports it: test AUPRC inside the pocket (`in_pocket` = 1) 0.9555 (95% t interval 0.9411 to 0.9699, 10 seeds) and outside it 0.9578 (0.8939 to 1.0217, 10 seeds).

At the max-F1 threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.8843 | 0.0750 | 0.8306 to 0.9380 |
| Recall | 0.8871 | 0.0869 | 0.8249 to 0.9493 |
| Specificity | 0.9600 | 0.0255 | 0.9418 to 0.9783 |
| F1 | 0.8845 | 0.0745 | 0.8312 to 0.9378 |
| MCC | 0.8464 | 0.0975 | 0.7767 to 0.9161 |
| Balanced accuracy | 0.9236 | 0.0512 | 0.8869 to 0.9602 |

At the 0.5% alert-budget threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 1.0000 | 0.0000 | 1.0000 to 1.0000 |
| Recall | 0.0422 | 0.0706 | -0.0083 to 0.0927 |
| Specificity | 1.0000 | 0.0000 | 1.0000 to 1.0000 |
| F1 | 0.0742 | 0.1119 | -0.0059 to 0.1542 |
| MCC | 0.1492 | 0.1079 | 0.0720 to 0.2264 |
| Balanced accuracy | 0.5211 | 0.0353 | 0.4958 to 0.5464 |

## Confusion counts per seed, test fold

TP, FP, TN and FN at each validation-chosen threshold, and at the test fold's own 0.5% budget (the comparison page's recall).

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN | 0.5% budget on the test fold: TP / FP / TN / FN |
|---|---|---|---|---|
| 42 | l2_regularization 1.0, learning_rate 0.05, max_leaf_nodes 31 | 1701 / 272 / 4954 / 81 | 431 / 0 / 5226 / 1351 | 36 / 0 / 5226 / 1746 |
| 43 | l2_regularization 0.0, learning_rate 0.1, max_leaf_nodes 31 | 1612 / 96 / 5130 / 170 | 47 / 0 / 5226 / 1735 | 36 / 0 / 5226 / 1746 |
| 44 | l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 31 | 1628 / 402 / 4824 / 154 | 42 / 0 / 5226 / 1740 | 36 / 0 / 5226 / 1746 |
| 45 | l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 15 | 1533 / 285 / 4941 / 249 | 45 / 0 / 5226 / 1737 | 36 / 0 / 5226 / 1746 |
| 46 | l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 31 | 1678 / 224 / 5002 / 104 | 34 / 0 / 5226 / 1748 | 36 / 0 / 5226 / 1746 |
| 47 | l2_regularization 0.0, learning_rate 0.1, max_leaf_nodes 31 | 1666 / 137 / 5089 / 116 | 45 / 0 / 5226 / 1737 | 36 / 0 / 5226 / 1746 |
| 48 | l2_regularization 0.0, learning_rate 0.1, max_leaf_nodes 31 | 1608 / 77 / 5149 / 174 | 31 / 0 / 5226 / 1751 | 36 / 0 / 5226 / 1746 |
| 49 | l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 31 | 1161 / 424 / 4802 / 621 | 1 / 0 / 5226 / 1781 | 36 / 0 / 5226 / 1746 |
| 50 | l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 31 | 1628 / 103 / 5123 / 154 | 49 / 0 / 5226 / 1733 | 36 / 0 / 5226 / 1746 |
| 51 | l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 31 | 1593 / 69 / 5157 / 189 | 27 / 0 / 5226 / 1755 | 40 / 0 / 5226 / 1742 |

## Limits

- One protocol and one grid per algorithm, F166's. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

