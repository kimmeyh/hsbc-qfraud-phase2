# CatBoost on ULB: best achievable result (F166)

**BLUF.** Tuned on validation and scored on the test fold over 10 seeds (42-51), CatBoost reaches a mean test AUPRC of 0.8329 (95% t interval 0.8131 to 0.8527). It is number 1 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [ULB_COMPARISON.md](ULB_COMPARISON.md).

- **Card**: F166 (Sprint 29 Task F, #69), the ULB part of F157.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F166", written before any score.
- **Evidence**: `experiments/phase2/results/f166_ulb_algorithms.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f166_ulb_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: ULB with duplicates dropped, `data.stratified_split` (60/20/20). Tuning reads the training and validation folds; every score here is on the test fold.
- **Setup**: `CatBoostClassifier`, 500 iterations, `random_seed=seed`, all 30 columns.

## Configurations tried

8 configurations, named in the entry before any score. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| depth 4, l2_leaf_reg 3, learning_rate 0.05 | 0 of 10 |
| depth 4, l2_leaf_reg 10, learning_rate 0.05 | 0 of 10 |
| depth 4, l2_leaf_reg 3, learning_rate 0.1 | 2 of 10 |
| depth 4, l2_leaf_reg 10, learning_rate 0.1 | 2 of 10 |
| depth 6, l2_leaf_reg 3, learning_rate 0.05 | 1 of 10 |
| depth 6, l2_leaf_reg 10, learning_rate 0.05 | 0 of 10 |
| depth 6, l2_leaf_reg 3, learning_rate 0.1 | 2 of 10 |
| depth 6, l2_leaf_reg 10, learning_rate 0.1 | 3 of 10 |

## Test-fold results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.8329 | 0.0277 | 0.8131 to 0.8527 |
| AUPRC, floor-normalized | 0.8326 | 0.0277 | 0.8128 to 0.8525 |
| ROC-AUC | 0.9781 | 0.0097 | 0.9712 to 0.9850 |
| Recall at the 0.5% budget, test fold | 0.8579 | 0.0315 | 0.8354 to 0.8804 |
| Train-test AUPRC gap | 0.1397 | 0.0233 | 0.1230 to 0.1564 |

At the max-F1 threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.9252 | 0.0436 | 0.8940 to 0.9564 |
| Recall | 0.7884 | 0.0401 | 0.7597 to 0.8171 |
| Specificity | 0.9999 | 0.0001 | 0.9998 to 0.9999 |
| F1 | 0.8500 | 0.0223 | 0.8341 to 0.8659 |
| MCC | 0.8532 | 0.0218 | 0.8375 to 0.8688 |
| Balanced accuracy | 0.8942 | 0.0201 | 0.8798 to 0.9085 |

At the 0.5% alert-budget threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.2967 | 0.0212 | 0.2815 to 0.3118 |
| Recall | 0.8558 | 0.0329 | 0.8322 to 0.8793 |
| Specificity | 0.9966 | 0.0004 | 0.9963 to 0.9968 |
| F1 | 0.4402 | 0.0255 | 0.4220 to 0.4584 |
| MCC | 0.5024 | 0.0234 | 0.4856 to 0.5191 |
| Balanced accuracy | 0.9262 | 0.0165 | 0.9144 to 0.9380 |

## Confusion counts per seed, test fold

TP, FP, TN and FN at each validation-chosen threshold.

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN |
|---|---|---|---|
| 42 | depth 6, l2_leaf_reg 10, learning_rate 0.1 | 79 / 6 / 56645 / 16 | 86 / 182 / 56469 / 9 |
| 43 | depth 4, l2_leaf_reg 10, learning_rate 0.1 | 72 / 3 / 56648 / 23 | 78 / 187 / 56464 / 17 |
| 44 | depth 4, l2_leaf_reg 3, learning_rate 0.1 | 78 / 14 / 56637 / 17 | 83 / 190 / 56461 / 12 |
| 45 | depth 6, l2_leaf_reg 3, learning_rate 0.1 | 75 / 1 / 56650 / 20 | 83 / 209 / 56442 / 12 |
| 46 | depth 6, l2_leaf_reg 10, learning_rate 0.1 | 75 / 7 / 56644 / 20 | 81 / 190 / 56461 / 14 |
| 47 | depth 4, l2_leaf_reg 3, learning_rate 0.1 | 75 / 6 / 56645 / 20 | 80 / 178 / 56473 / 15 |
| 48 | depth 6, l2_leaf_reg 3, learning_rate 0.1 | 81 / 8 / 56643 / 14 | 86 / 205 / 56446 / 9 |
| 49 | depth 6, l2_leaf_reg 10, learning_rate 0.1 | 69 / 1 / 56650 / 26 | 80 / 170 / 56481 / 15 |
| 50 | depth 4, l2_leaf_reg 10, learning_rate 0.1 | 75 / 10 / 56641 / 20 | 79 / 241 / 56410 / 16 |
| 51 | depth 6, l2_leaf_reg 3, learning_rate 0.05 | 70 / 7 / 56644 / 25 | 77 / 187 / 56464 / 18 |

## Limits

- Each validation fold holds about 95 frauds, so validation AUPRC is noisy and the chosen configuration changes between seeds.
- One protocol and one grid per algorithm. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

