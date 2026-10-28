# HGB on ULB: best achievable result (F166)

**BLUF.** Tuned on validation and scored on the test fold over 10 seeds (42-51), HGB reaches a mean test AUPRC of 0.8124 (95% t interval 0.7940 to 0.8307). It is number 4 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [ULB_COMPARISON.md](ULB_COMPARISON.md).

- **Card**: F166 (Sprint 29 Task F, #69), the ULB part of F157.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F166", written before any score.
- **Evidence**: `experiments/phase2/results/f166_ulb_algorithms.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f166_ulb_algorithms.py`. Every figure below comes from that file. The per-row test scores and the outcome block for each seed are in the file's rows.
- **Data**: ULB with duplicates dropped, `data.stratified_split` (60/20/20). Tuning reads the training and validation folds; every score here is on the test fold.
- **Setup**: `HistGradientBoostingClassifier`, `random_state=seed`, all 30 columns.

## Configurations tried

8 configurations, named in the entry before any score. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| l2_regularization 0.0, learning_rate 0.05, max_leaf_nodes 15 | 0 of 10 |
| l2_regularization 0.0, learning_rate 0.05, max_leaf_nodes 31 | 0 of 10 |
| l2_regularization 0.0, learning_rate 0.1, max_leaf_nodes 15 | 0 of 10 |
| l2_regularization 0.0, learning_rate 0.1, max_leaf_nodes 31 | 0 of 10 |
| l2_regularization 1.0, learning_rate 0.05, max_leaf_nodes 15 | 0 of 10 |
| l2_regularization 1.0, learning_rate 0.05, max_leaf_nodes 31 | 7 of 10 |
| l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 15 | 1 of 10 |
| l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 31 | 2 of 10 |

## Test-fold results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.8124 | 0.0257 | 0.7940 to 0.8307 |
| AUPRC, floor-normalized | 0.8120 | 0.0257 | 0.7937 to 0.8304 |
| ROC-AUC | 0.9772 | 0.0085 | 0.9711 to 0.9833 |
| Recall at the 0.5% budget, test fold | 0.8558 | 0.0285 | 0.8354 to 0.8762 |
| Train-test AUPRC gap | 0.1647 | 0.0280 | 0.1447 to 0.1847 |

At the max-F1 threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.9101 | 0.0531 | 0.8721 to 0.9481 |
| Recall | 0.7579 | 0.0371 | 0.7313 to 0.7845 |
| Specificity | 0.9999 | 0.0001 | 0.9998 to 0.9999 |
| F1 | 0.8253 | 0.0209 | 0.8104 to 0.8402 |
| MCC | 0.8294 | 0.0208 | 0.8145 to 0.8442 |
| Balanced accuracy | 0.8789 | 0.0185 | 0.8656 to 0.8921 |

At the 0.5% alert-budget threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.2850 | 0.0142 | 0.2748 to 0.2952 |
| Recall | 0.8568 | 0.0294 | 0.8358 to 0.8779 |
| Specificity | 0.9964 | 0.0003 | 0.9962 to 0.9966 |
| F1 | 0.4275 | 0.0164 | 0.4157 to 0.4392 |
| MCC | 0.4927 | 0.0153 | 0.4818 to 0.5037 |
| Balanced accuracy | 0.9266 | 0.0147 | 0.9161 to 0.9371 |

## Confusion counts per seed, test fold

TP, FP, TN and FN at each validation-chosen threshold.

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN |
|---|---|---|---|
| 42 | l2_regularization 1.0, learning_rate 0.05, max_leaf_nodes 31 | 75 / 5 / 56646 / 20 | 84 / 212 / 56439 / 11 |
| 43 | l2_regularization 1.0, learning_rate 0.05, max_leaf_nodes 31 | 68 / 5 / 56646 / 27 | 79 / 209 / 56442 / 16 |
| 44 | l2_regularization 1.0, learning_rate 0.05, max_leaf_nodes 31 | 68 / 4 / 56647 / 27 | 83 / 192 / 56459 / 12 |
| 45 | l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 31 | 76 / 10 / 56641 / 19 | 83 / 214 / 56437 / 12 |
| 46 | l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 31 | 76 / 19 / 56632 / 19 | 80 / 206 / 56445 / 15 |
| 47 | l2_regularization 1.0, learning_rate 0.05, max_leaf_nodes 31 | 73 / 4 / 56647 / 22 | 81 / 222 / 56429 / 14 |
| 48 | l2_regularization 1.0, learning_rate 0.05, max_leaf_nodes 31 | 73 / 4 / 56647 / 22 | 87 / 219 / 56432 / 8 |
| 49 | l2_regularization 1.0, learning_rate 0.05, max_leaf_nodes 31 | 66 / 2 / 56649 / 29 | 80 / 173 / 56478 / 15 |
| 50 | l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 15 | 72 / 10 / 56641 / 23 | 78 / 194 / 56457 / 17 |
| 51 | l2_regularization 1.0, learning_rate 0.05, max_leaf_nodes 31 | 73 / 12 / 56639 / 22 | 79 / 207 / 56444 / 16 |

## Limits

- Each validation fold holds about 95 frauds, so validation AUPRC is noisy and the chosen configuration changes between seeds.
- One protocol and one grid per algorithm. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

