# HGB on IEEE-CIS: best achievable result (F174)

**BLUF.** Tuned on month 3 and scored on month 4 over 10 seeds (42-51), HGB reaches a mean test AUPRC of 0.5211 (95% t interval 0.5171 to 0.5250). It is number 2 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [IEEE_COMPARISON.md](IEEE_COMPARISON.md). The ULB page for the same algorithm is [ULB_HGB.md](ULB_HGB.md).

- **Card**: F174 (Sprint 30 Task D, #78), the IEEE-CIS part of F157.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F174", written before any score.
- **Evidence**: `experiments/phase2/results/f174_ieee_algorithms.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f174_ieee_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: IEEE-CIS with exact duplicates dropped (3 rows), F105's month folds and F152's item-4 controls. Tuning fits months 0-2 and chooses on month 3 (98,027 rows); the chosen configuration is fitted again on months 0-3 and scored once on month 4 (85,302 rows). Every score here is on month 4.
- **Setup**: `HistGradientBoostingClassifier`, `random_state=seed`, every column the fold keeps.

## Configurations tried

8 configurations, F166's grid, imported unchanged. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| l2_regularization 0.0, learning_rate 0.05, max_leaf_nodes 15 | 0 of 10 |
| l2_regularization 0.0, learning_rate 0.05, max_leaf_nodes 31 | 0 of 10 |
| l2_regularization 0.0, learning_rate 0.1, max_leaf_nodes 15 | 0 of 10 |
| l2_regularization 0.0, learning_rate 0.1, max_leaf_nodes 31 | 2 of 10 |
| l2_regularization 1.0, learning_rate 0.05, max_leaf_nodes 15 | 0 of 10 |
| l2_regularization 1.0, learning_rate 0.05, max_leaf_nodes 31 | 0 of 10 |
| l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 15 | 0 of 10 |
| l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 31 | 8 of 10 |

## Test-month results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.5211 | 0.0055 | 0.5171 to 0.5250 |
| AUPRC, floor-normalized | 0.5038 | 0.0057 | 0.4998 to 0.5079 |
| ROC-AUC | 0.8903 | 0.0034 | 0.8879 to 0.8927 |
| Recall at the 0.5% budget, test fold | 0.1357 | 0.0018 | 0.1344 to 0.1370 |
| Train-test AUPRC gap | 0.1861 | 0.0089 | 0.1797 to 0.1924 |

At the max-F1 threshold chosen on the validation month:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.6463 | 0.0179 | 0.6335 to 0.6591 |
| Recall | 0.4338 | 0.0119 | 0.4253 to 0.4424 |
| Specificity | 0.9914 | 0.0008 | 0.9908 to 0.9920 |
| F1 | 0.5189 | 0.0077 | 0.5134 to 0.5245 |
| MCC | 0.5159 | 0.0078 | 0.5104 to 0.5215 |
| Balanced accuracy | 0.7126 | 0.0057 | 0.7086 to 0.7167 |

At the 0.5% alert-budget threshold chosen on the validation month:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.9577 | 0.0161 | 0.9461 to 0.9692 |
| Recall | 0.1205 | 0.0088 | 0.1142 to 0.1268 |
| Specificity | 0.9998 | 0.0001 | 0.9997 to 0.9999 |
| F1 | 0.2139 | 0.0139 | 0.2040 to 0.2239 |
| MCC | 0.3337 | 0.0113 | 0.3256 to 0.3418 |
| Balanced accuracy | 0.5601 | 0.0044 | 0.5570 to 0.5633 |

On the test month this threshold flags 305 to 405 of 85,302 test rows; the month's own 0.5% budget is 427 rows. The threshold is chosen on the validation month, so its alert volume on the test month is not the budget. The row "Recall at the 0.5% budget, test fold" above uses the test month's own budget.

## Confusion counts per seed, test month

TP, FP, TN and FN at each threshold chosen on the validation month, and at the test month's own 0.5% budget (the comparison page's recall).

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN | 0.5% budget on the test month: TP / FP / TN / FN |
|---|---|---|---|---|
| 42 | l2_regularization 0.0, learning_rate 0.1, max_leaf_nodes 31 | 1274 / 693 / 81647 / 1688 | 362 / 22 / 82318 / 2600 | 397 / 30 / 82310 / 2565 |
| 43 | l2_regularization 0.0, learning_rate 0.1, max_leaf_nodes 31 | 1333 / 759 / 81581 / 1629 | 298 / 7 / 82333 / 2664 | 407 / 20 / 82320 / 2555 |
| 44 | l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 31 | 1259 / 667 / 81673 / 1703 | 376 / 29 / 82311 / 2586 | 393 / 34 / 82306 / 2569 |
| 45 | l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 31 | 1252 / 620 / 81720 / 1710 | 350 / 11 / 82329 / 2612 | 404 / 23 / 82317 / 2558 |
| 46 | l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 31 | 1269 / 756 / 81584 / 1693 | 380 / 18 / 82322 / 2582 | 403 / 24 / 82316 / 2559 |
| 47 | l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 31 | 1320 / 653 / 81687 / 1642 | 366 / 24 / 82316 / 2596 | 399 / 28 / 82312 / 2563 |
| 48 | l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 31 | 1245 / 652 / 81688 / 1717 | 360 / 14 / 82326 / 2602 | 397 / 30 / 82310 / 2565 |
| 49 | l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 31 | 1322 / 825 / 81515 / 1640 | 384 / 12 / 82328 / 2578 | 411 / 16 / 82324 / 2551 |
| 50 | l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 31 | 1324 / 771 / 81569 / 1638 | 365 / 14 / 82326 / 2597 | 402 / 25 / 82315 / 2560 |
| 51 | l2_regularization 1.0, learning_rate 0.1, max_leaf_nodes 31 | 1252 / 656 / 81684 / 1710 | 328 / 10 / 82330 / 2634 | 406 / 22 / 82318 / 2556 |

## Limits

- The validation month holds about 3,849 frauds, so validation AUPRC is less noisy than on ULB; the chosen configuration changes between seeds.
- One protocol and one grid per algorithm, F166's. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- One test month. Month-to-month drift is outside this result; F152 scores months 4-6.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

