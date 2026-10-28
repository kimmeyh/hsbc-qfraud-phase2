# LightGBM on ULB: best achievable result (F166)

**BLUF.** Tuned on validation and scored on the test fold over 10 seeds (42-51), LightGBM reaches a mean test AUPRC of 0.8270 (95% t interval 0.8104 to 0.8436). It is number 2 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [ULB_COMPARISON.md](ULB_COMPARISON.md).

- **Card**: F166 (Sprint 29 Task F, #69), the ULB part of F157.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F166", written before any score.
- **Evidence**: `experiments/phase2/results/f166_ulb_algorithms.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f166_ulb_algorithms.py`. Every figure below comes from that file. The per-row test scores and the outcome block for each seed are in the file's rows.
- **Data**: ULB with duplicates dropped, `data.stratified_split` (60/20/20). Tuning reads the training and validation folds; every score here is on the test fold.
- **Setup**: `LGBMClassifier`, 300 trees, `random_state=seed`, all 30 columns.

## Configurations tried

8 configurations, named in the entry before any score. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| learning_rate 0.05, num_leaves 15, reg_lambda 0.0 | 0 of 10 |
| learning_rate 0.05, num_leaves 15, reg_lambda 1.0 | 4 of 10 |
| learning_rate 0.1, num_leaves 15, reg_lambda 0.0 | 0 of 10 |
| learning_rate 0.1, num_leaves 15, reg_lambda 1.0 | 2 of 10 |
| learning_rate 0.05, num_leaves 63, reg_lambda 0.0 | 0 of 10 |
| learning_rate 0.05, num_leaves 63, reg_lambda 1.0 | 4 of 10 |
| learning_rate 0.1, num_leaves 63, reg_lambda 0.0 | 0 of 10 |
| learning_rate 0.1, num_leaves 63, reg_lambda 1.0 | 0 of 10 |

## Test-fold results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.8270 | 0.0232 | 0.8104 to 0.8436 |
| AUPRC, floor-normalized | 0.8267 | 0.0232 | 0.8101 to 0.8433 |
| ROC-AUC | 0.9748 | 0.0089 | 0.9684 to 0.9811 |
| Recall at the 0.5% budget, test fold | 0.8568 | 0.0259 | 0.8383 to 0.8754 |
| Train-test AUPRC gap | 0.1730 | 0.0232 | 0.1564 to 0.1896 |

At the max-F1 threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.9315 | 0.0274 | 0.9119 to 0.9511 |
| Recall | 0.7684 | 0.0457 | 0.7357 to 0.8011 |
| Specificity | 0.9999 | 0.0000 | 0.9999 to 0.9999 |
| F1 | 0.8410 | 0.0231 | 0.8244 to 0.8575 |
| MCC | 0.8452 | 0.0212 | 0.8300 to 0.8604 |
| Balanced accuracy | 0.8842 | 0.0229 | 0.8678 to 0.9005 |

At the 0.5% alert-budget threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.2854 | 0.0127 | 0.2763 to 0.2945 |
| Recall | 0.8589 | 0.0273 | 0.8394 to 0.8785 |
| Specificity | 0.9964 | 0.0003 | 0.9962 to 0.9966 |
| F1 | 0.4281 | 0.0133 | 0.4186 to 0.4376 |
| MCC | 0.4936 | 0.0106 | 0.4861 to 0.5012 |
| Balanced accuracy | 0.9277 | 0.0135 | 0.9180 to 0.9373 |

## Confusion counts per seed, test fold

TP, FP, TN and FN at each validation-chosen threshold.

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN |
|---|---|---|---|
| 42 | learning_rate 0.05, num_leaves 15, reg_lambda 1.0 | 75 / 6 / 56645 / 20 | 86 / 220 / 56431 / 9 |
| 43 | learning_rate 0.05, num_leaves 63, reg_lambda 1.0 | 66 / 4 / 56647 / 29 | 81 / 193 / 56458 / 14 |
| 44 | learning_rate 0.05, num_leaves 63, reg_lambda 1.0 | 69 / 3 / 56648 / 26 | 82 / 206 / 56445 / 13 |
| 45 | learning_rate 0.1, num_leaves 15, reg_lambda 1.0 | 76 / 3 / 56648 / 19 | 82 / 218 / 56433 / 13 |
| 46 | learning_rate 0.05, num_leaves 15, reg_lambda 1.0 | 73 / 7 / 56644 / 22 | 81 / 231 / 56420 / 14 |
| 47 | learning_rate 0.05, num_leaves 63, reg_lambda 1.0 | 74 / 3 / 56648 / 21 | 80 / 196 / 56455 / 15 |
| 48 | learning_rate 0.05, num_leaves 63, reg_lambda 1.0 | 82 / 12 / 56639 / 13 | 86 / 222 / 56429 / 9 |
| 49 | learning_rate 0.05, num_leaves 15, reg_lambda 1.0 | 72 / 6 / 56645 / 23 | 80 / 184 / 56467 / 15 |
| 50 | learning_rate 0.1, num_leaves 15, reg_lambda 1.0 | 73 / 5 / 56646 / 22 | 78 / 186 / 56465 / 17 |
| 51 | learning_rate 0.05, num_leaves 15, reg_lambda 1.0 | 70 / 6 / 56645 / 25 | 80 / 194 / 56457 / 15 |

## Limits

- Each validation fold holds about 95 frauds, so validation AUPRC is noisy and the chosen configuration changes between seeds.
- One protocol and one grid per algorithm. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

