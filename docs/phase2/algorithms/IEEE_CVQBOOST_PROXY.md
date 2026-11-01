# CVQBoost proxy on IEEE-CIS: best achievable result (F174)

**BLUF.** Tuned on month 3 and scored on month 4 over 10 seeds (42-51), CVQBoost proxy reaches a mean test AUPRC of 0.4862 (95% t interval 0.4751 to 0.4973). It is number 5 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [IEEE_COMPARISON.md](IEEE_COMPARISON.md). The ULB page for the same algorithm is [ULB_CVQBOOST_PROXY.md](ULB_CVQBOOST_PROXY.md).

- **Card**: F174 (Sprint 30 Task D, #78), the IEEE-CIS part of F157.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F174", written before any score.
- **Evidence**: `experiments/phase2/results/f174_ieee_algorithms.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f174_ieee_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: IEEE-CIS with exact duplicates dropped (3 rows), F105's month folds and F152's item-4 controls. Tuning fits months 0-2 and chooses on month 3 (98,027 rows); the chosen configuration is fitted again on months 0-3 and scored once on month 4 (85,302 rows). Every score here is on month 4.
- **Setup**: the three frozen `qubo_proxy` configurations, full-pair pool built serially, dct learners seeded by `qubo_proxy.seeded_weak_params(seed)`; each configuration uses its own top-k features, ranked by mutual information on a 50,000-row subsample of the training months.

## Configurations tried

3 configurations, F166's grid, imported unchanged. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| config free | 0 of 10 |
| config mid | 0 of 10 |
| config full | 10 of 10 |

Every pool was built serially. The chosen configuration's pool used 17 features and held 833 learners.

## Test-month results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.4862 | 0.0155 | 0.4751 to 0.4973 |
| AUPRC, floor-normalized | 0.4678 | 0.0161 | 0.4563 to 0.4793 |
| ROC-AUC | 0.7961 | 0.0127 | 0.7870 to 0.8052 |
| Recall at the 0.5% budget, test fold | 0.1377 | 0.0021 | 0.1362 to 0.1392 |
| Train-test AUPRC gap | 0.3771 | 0.0116 | 0.3688 to 0.3854 |

At the max-F1 threshold chosen on the validation month:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.5511 | 0.0398 | 0.5227 to 0.5796 |
| Recall | 0.4837 | 0.0138 | 0.4738 to 0.4936 |
| Specificity | 0.9857 | 0.0021 | 0.9842 to 0.9872 |
| F1 | 0.5146 | 0.0193 | 0.5008 to 0.5284 |
| MCC | 0.4997 | 0.0216 | 0.4843 to 0.5152 |
| Balanced accuracy | 0.7347 | 0.0070 | 0.7297 to 0.7397 |

At the 0.5% alert-budget threshold chosen on the validation month:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.9065 | 0.0098 | 0.8995 to 0.9136 |
| Recall | 0.2810 | 0.0208 | 0.2661 to 0.2958 |
| Specificity | 0.9990 | 0.0002 | 0.9988 to 0.9991 |
| F1 | 0.4285 | 0.0239 | 0.4114 to 0.4456 |
| MCC | 0.4963 | 0.0169 | 0.4842 to 0.5084 |
| Balanced accuracy | 0.6400 | 0.0103 | 0.6326 to 0.6473 |

On the test month this threshold flags 748 to 1,035 of 85,302 test rows; the month's own 0.5% budget is 427 rows. The threshold is chosen on the validation month, so its alert volume on the test month is not the budget. The row "Recall at the 0.5% budget, test fold" above uses the test month's own budget.

## Confusion counts per seed, test month

TP, FP, TN and FN at each threshold chosen on the validation month.

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN |
|---|---|---|---|
| 42 | config full | 1400 / 1288 / 81052 / 1562 | 919 / 116 / 82224 / 2043 |
| 43 | config full | 1416 / 1378 / 80962 / 1546 | 832 / 96 / 82244 / 2130 |
| 44 | config full | 1423 / 1231 / 81109 / 1539 | 906 / 102 / 82238 / 2056 |
| 45 | config full | 1507 / 1019 / 81321 / 1455 | 849 / 79 / 82261 / 2113 |
| 46 | config full | 1406 / 1183 / 81157 / 1556 | 817 / 80 / 82260 / 2145 |
| 47 | config full | 1367 / 801 / 81539 / 1595 | 689 / 59 / 82281 / 2273 |
| 48 | config full | 1457 / 1305 / 81035 / 1505 | 832 / 79 / 82261 / 2130 |
| 49 | config full | 1442 / 1272 / 81068 / 1520 | 826 / 81 / 82259 / 2136 |
| 50 | config full | 1428 / 1263 / 81077 / 1534 | 833 / 86 / 82254 / 2129 |
| 51 | config full | 1482 / 1039 / 81301 / 1480 | 819 / 86 / 82254 / 2143 |

## Limits

- The validation month holds about 3,849 frauds, so validation AUPRC is less noisy than on ULB. Here the same configuration (`full`) was chosen on every seed.
- The proxy's test scores are heavily tied: the tie fraction is 0.9365 to 0.9631, and the most common score covers a share of 0.8434 to 0.9111 of test rows. The score-health check warns on seeds 42 and 44. A threshold moves every row with a tied score at once, so a chosen threshold can flag many more rows than intended.
- One protocol and one grid per algorithm, F166's. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- One test month. Month-to-month drift is outside this result; F152 scores months 4-6.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

