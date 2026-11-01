# LightGBM on IEEE-CIS: best achievable result (F174)

**BLUF.** Tuned on month 3 and scored on month 4 over 10 seeds (42-51), LightGBM reaches a mean test AUPRC of 0.5785 (95% t interval 0.5706 to 0.5864). It is number 1 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [IEEE_COMPARISON.md](IEEE_COMPARISON.md). The ULB page for the same algorithm is [ULB_LIGHTGBM.md](ULB_LIGHTGBM.md).

- **Card**: F174 (Sprint 30 Task D, #78), the IEEE-CIS part of F157.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F174", written before any score.
- **Evidence**: `experiments/phase2/results/f174_ieee_algorithms.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f174_ieee_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: IEEE-CIS with exact duplicates dropped (3 rows), F105's month folds and F152's item-4 controls. Tuning fits months 0-2 and chooses on month 3 (98,027 rows); the chosen configuration is fitted again on months 0-3 and scored once on month 4 (85,302 rows). Every score here is on month 4.
- **Setup**: `LGBMClassifier`, 300 trees, `random_state=seed`, every column the fold keeps.

## Configurations tried

8 configurations, F166's grid, imported unchanged. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| learning_rate 0.05, num_leaves 15, reg_lambda 0.0 | 0 of 10 |
| learning_rate 0.05, num_leaves 15, reg_lambda 1.0 | 0 of 10 |
| learning_rate 0.1, num_leaves 15, reg_lambda 0.0 | 0 of 10 |
| learning_rate 0.1, num_leaves 15, reg_lambda 1.0 | 0 of 10 |
| learning_rate 0.05, num_leaves 63, reg_lambda 0.0 | 2 of 10 |
| learning_rate 0.05, num_leaves 63, reg_lambda 1.0 | 4 of 10 |
| learning_rate 0.1, num_leaves 63, reg_lambda 0.0 | 0 of 10 |
| learning_rate 0.1, num_leaves 63, reg_lambda 1.0 | 4 of 10 |

## Test-month results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.5785 | 0.0110 | 0.5706 to 0.5864 |
| AUPRC, floor-normalized | 0.5633 | 0.0114 | 0.5552 to 0.5715 |
| ROC-AUC | 0.9058 | 0.0029 | 0.9037 to 0.9078 |
| Recall at the 0.5% budget, test fold | 0.1389 | 0.0015 | 0.1378 to 0.1399 |
| Train-test AUPRC gap | 0.2947 | 0.0321 | 0.2717 to 0.3176 |

At the max-F1 threshold chosen on the validation month:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.7339 | 0.0208 | 0.7190 to 0.7488 |
| Recall | 0.4652 | 0.0178 | 0.4525 to 0.4779 |
| Specificity | 0.9939 | 0.0008 | 0.9934 to 0.9945 |
| F1 | 0.5691 | 0.0127 | 0.5600 to 0.5782 |
| MCC | 0.5727 | 0.0115 | 0.5645 to 0.5809 |
| Balanced accuracy | 0.7296 | 0.0087 | 0.7234 to 0.7358 |

At the 0.5% alert-budget threshold chosen on the validation month:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.9726 | 0.0095 | 0.9658 to 0.9794 |
| Recall | 0.1176 | 0.0084 | 0.1115 to 0.1236 |
| Specificity | 0.9999 | 0.0000 | 0.9998 to 0.9999 |
| F1 | 0.2097 | 0.0134 | 0.2001 to 0.2193 |
| MCC | 0.3324 | 0.0117 | 0.3240 to 0.3408 |
| Balanced accuracy | 0.5587 | 0.0042 | 0.5557 to 0.5617 |

On the test month this threshold flags 311 to 410 of 85,302 test rows; the month's own 0.5% budget is 427 rows. The threshold is chosen on the validation month, so its alert volume on the test month is not the budget. The row "Recall at the 0.5% budget, test fold" above uses the test month's own budget.

## Confusion counts per seed, test month

TP, FP, TN and FN at each threshold chosen on the validation month, and at the test month's own 0.5% budget (the comparison page's recall).

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN | 0.5% budget on the test month: TP / FP / TN / FN |
|---|---|---|---|---|
| 42 | learning_rate 0.05, num_leaves 63, reg_lambda 1.0 | 1353 / 540 / 81800 / 1609 | 373 / 10 / 82330 / 2589 | 415 / 12 / 82328 / 2547 |
| 43 | learning_rate 0.05, num_leaves 63, reg_lambda 1.0 | 1398 / 534 / 81806 / 1564 | 397 / 13 / 82327 / 2565 | 413 / 14 / 82326 / 2549 |
| 44 | learning_rate 0.1, num_leaves 63, reg_lambda 1.0 | 1424 / 499 / 81841 / 1538 | 346 / 9 / 82331 / 2616 | 412 / 15 / 82325 / 2550 |
| 45 | learning_rate 0.1, num_leaves 63, reg_lambda 1.0 | 1357 / 444 / 81896 / 1605 | 345 / 8 / 82332 / 2617 | 412 / 15 / 82325 / 2550 |
| 46 | learning_rate 0.05, num_leaves 63, reg_lambda 0.0 | 1258 / 416 / 81924 / 1704 | 356 / 11 / 82329 / 2606 | 412 / 15 / 82325 / 2550 |
| 47 | learning_rate 0.05, num_leaves 63, reg_lambda 1.0 | 1361 / 466 / 81874 / 1601 | 304 / 7 / 82333 / 2658 | 412 / 15 / 82325 / 2550 |
| 48 | learning_rate 0.1, num_leaves 63, reg_lambda 1.0 | 1418 / 610 / 81730 / 1544 | 345 / 19 / 82321 / 2617 | 400 / 27 / 82313 / 2562 |
| 49 | learning_rate 0.05, num_leaves 63, reg_lambda 1.0 | 1364 / 438 / 81902 / 1598 | 337 / 8 / 82332 / 2625 | 412 / 15 / 82325 / 2550 |
| 50 | learning_rate 0.1, num_leaves 63, reg_lambda 1.0 | 1443 / 491 / 81849 / 1519 | 327 / 7 / 82333 / 2635 | 409 / 18 / 82322 / 2553 |
| 51 | learning_rate 0.05, num_leaves 63, reg_lambda 0.0 | 1404 / 579 / 81761 / 1558 | 353 / 7 / 82333 / 2609 | 416 / 11 / 82329 / 2546 |

## Limits

- The validation month holds about 3,849 frauds, so validation AUPRC is less noisy than on ULB; the chosen configuration changes between seeds.
- One protocol and one grid per algorithm, F166's. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- One test month. Month-to-month drift is outside this result; F152 scores months 4-6.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

