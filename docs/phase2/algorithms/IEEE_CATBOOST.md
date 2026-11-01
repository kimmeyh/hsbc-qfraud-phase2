# CatBoost on IEEE-CIS: best achievable result (F174)

**BLUF.** Tuned on month 3 and scored on month 4 over 10 seeds (42-51), CatBoost reaches a mean test AUPRC of 0.5114 (95% t interval 0.5069 to 0.5158). It is number 3 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [IEEE_COMPARISON.md](IEEE_COMPARISON.md). The ULB page for the same algorithm is [ULB_CATBOOST.md](ULB_CATBOOST.md).

- **Card**: F174 (Sprint 30 Task D, #78), the IEEE-CIS part of F157.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F174", written before any score.
- **Evidence**: `experiments/phase2/results/f174_ieee_algorithms.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f174_ieee_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: IEEE-CIS with exact duplicates dropped (3 rows), F105's month folds and F152's item-4 controls. Tuning fits months 0-2 and chooses on month 3 (98,027 rows); the chosen configuration is fitted again on months 0-3 and scored once on month 4 (85,302 rows). Every score here is on month 4.
- **Setup**: `CatBoostClassifier`, 500 iterations, `random_seed=seed`, every column the fold keeps.

## Configurations tried

8 configurations, F166's grid, imported unchanged. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| depth 4, l2_leaf_reg 3, learning_rate 0.05 | 0 of 10 |
| depth 4, l2_leaf_reg 10, learning_rate 0.05 | 0 of 10 |
| depth 4, l2_leaf_reg 3, learning_rate 0.1 | 0 of 10 |
| depth 4, l2_leaf_reg 10, learning_rate 0.1 | 0 of 10 |
| depth 6, l2_leaf_reg 3, learning_rate 0.05 | 0 of 10 |
| depth 6, l2_leaf_reg 10, learning_rate 0.05 | 0 of 10 |
| depth 6, l2_leaf_reg 3, learning_rate 0.1 | 6 of 10 |
| depth 6, l2_leaf_reg 10, learning_rate 0.1 | 4 of 10 |

## Test-month results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.5114 | 0.0063 | 0.5069 to 0.5158 |
| AUPRC, floor-normalized | 0.4938 | 0.0065 | 0.4891 to 0.4984 |
| ROC-AUC | 0.8723 | 0.0024 | 0.8706 to 0.8740 |
| Recall at the 0.5% budget, test fold | 0.1388 | 0.0009 | 0.1381 to 0.1394 |
| Train-test AUPRC gap | 0.1846 | 0.0066 | 0.1799 to 0.1894 |

At the max-F1 threshold chosen on the validation month:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.7111 | 0.0206 | 0.6963 to 0.7258 |
| Recall | 0.3971 | 0.0156 | 0.3859 to 0.4083 |
| Specificity | 0.9942 | 0.0008 | 0.9936 to 0.9947 |
| F1 | 0.5092 | 0.0091 | 0.5026 to 0.5157 |
| MCC | 0.5192 | 0.0063 | 0.5147 to 0.5238 |
| Balanced accuracy | 0.6956 | 0.0075 | 0.6903 to 0.7010 |

At the 0.5% alert-budget threshold chosen on the validation month:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.9664 | 0.0068 | 0.9615 to 0.9712 |
| Recall | 0.1275 | 0.0138 | 0.1176 to 0.1373 |
| Specificity | 0.9998 | 0.0000 | 0.9998 to 0.9999 |
| F1 | 0.2250 | 0.0215 | 0.2096 to 0.2404 |
| MCC | 0.3447 | 0.0184 | 0.3315 to 0.3579 |
| Balanced accuracy | 0.5637 | 0.0069 | 0.5587 to 0.5686 |

On the test month this threshold flags 318 to 451 of 85,302 test rows; the month's own 0.5% budget is 427 rows. The threshold is chosen on the validation month, so its alert volume on the test month is not the budget. The row "Recall at the 0.5% budget, test fold" above uses the test month's own budget.

## Confusion counts per seed, test month

TP, FP, TN and FN at each threshold chosen on the validation month.

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN |
|---|---|---|---|
| 42 | depth 6, l2_leaf_reg 10, learning_rate 0.1 | 1100 / 409 / 81931 / 1862 | 311 / 7 / 82333 / 2651 |
| 43 | depth 6, l2_leaf_reg 3, learning_rate 0.1 | 1162 / 415 / 81925 / 1800 | 395 / 20 / 82320 / 2567 |
| 44 | depth 6, l2_leaf_reg 3, learning_rate 0.1 | 1183 / 463 / 81877 / 1779 | 343 / 12 / 82328 / 2619 |
| 45 | depth 6, l2_leaf_reg 3, learning_rate 0.1 | 1131 / 420 / 81920 / 1831 | 427 / 14 / 82326 / 2535 |
| 46 | depth 6, l2_leaf_reg 3, learning_rate 0.1 | 1261 / 611 / 81729 / 1701 | 321 / 11 / 82329 / 2641 |
| 47 | depth 6, l2_leaf_reg 10, learning_rate 0.1 | 1162 / 504 / 81836 / 1800 | 382 / 12 / 82328 / 2580 |
| 48 | depth 6, l2_leaf_reg 3, learning_rate 0.1 | 1212 / 559 / 81781 / 1750 | 385 / 12 / 82328 / 2577 |
| 49 | depth 6, l2_leaf_reg 10, learning_rate 0.1 | 1211 / 492 / 81848 / 1751 | 391 / 14 / 82326 / 2571 |
| 50 | depth 6, l2_leaf_reg 10, learning_rate 0.1 | 1145 / 440 / 81900 / 1817 | 388 / 13 / 82327 / 2574 |
| 51 | depth 6, l2_leaf_reg 3, learning_rate 0.1 | 1195 / 493 / 81847 / 1767 | 433 / 18 / 82322 / 2529 |

## Limits

- The validation month holds about 3,849 frauds, so validation AUPRC is less noisy than on ULB; the chosen configuration changes between seeds.
- One protocol and one grid per algorithm, F166's. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- One test month. Month-to-month drift is outside this result; F152 scores months 4-6.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

