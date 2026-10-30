# CVQBoost proxy on ULB: best achievable result (F166)

**BLUF.** Tuned on validation and scored on the test fold over 10 seeds (42-51), CVQBoost proxy reaches a mean test AUPRC of 0.7925 (95% t interval 0.7705 to 0.8146). It is number 5 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [ULB_COMPARISON.md](ULB_COMPARISON.md).

- **Card**: F166 (Sprint 29 Task F, #69), the ULB part of F157.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F166", written before any score.
- **Evidence**: `experiments/phase2/results/f166_ulb_algorithms.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f166_ulb_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: ULB with duplicates dropped, `data.stratified_split` (60/20/20). Tuning reads the training and validation folds; every score here is on the test fold.
- **Setup**: the three frozen `qubo_proxy` configurations, full-pair pool, dct learners seeded by `qubo_proxy.seeded_weak_params(seed)`, lambda 2 x n_train; each configuration uses its own top-k features.

## Configurations tried

3 configurations, named in the entry before any score. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| config free | 0 of 10 |
| config mid | 0 of 10 |
| config full | 10 of 10 |

The full configuration (k 17, order 3) was chosen on every seed. Its pool was built with F159's parallel build (32 workers), which F159 showed gives the same pool as the serial build; free and mid were built serially, so the fit seconds of the three configurations are not comparable.

## Test-fold results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.7925 | 0.0308 | 0.7705 to 0.8146 |
| AUPRC, floor-normalized | 0.7922 | 0.0309 | 0.7701 to 0.8143 |
| ROC-AUC | 0.9441 | 0.0108 | 0.9364 to 0.9518 |
| Recall at the 0.5% budget, test fold | 0.8305 | 0.0319 | 0.8077 to 0.8534 |
| Train-test AUPRC gap | 0.2075 | 0.0308 | 0.1854 to 0.2295 |

At the max-F1 threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.8885 | 0.0368 | 0.8621 to 0.9149 |
| Recall | 0.7726 | 0.0422 | 0.7425 to 0.8028 |
| Specificity | 0.9998 | 0.0001 | 0.9998 to 0.9999 |
| F1 | 0.8254 | 0.0231 | 0.8088 to 0.8419 |
| MCC | 0.8277 | 0.0227 | 0.8115 to 0.8439 |
| Balanced accuracy | 0.8862 | 0.0211 | 0.8712 to 0.9013 |

At the 0.5% alert-budget threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.2892 | 0.0250 | 0.2713 to 0.3071 |
| Recall | 0.8305 | 0.0319 | 0.8077 to 0.8534 |
| Specificity | 0.9965 | 0.0004 | 0.9962 to 0.9969 |
| F1 | 0.4282 | 0.0258 | 0.4098 to 0.4467 |
| MCC | 0.4883 | 0.0203 | 0.4738 to 0.5028 |
| Balanced accuracy | 0.9135 | 0.0159 | 0.9022 to 0.9249 |

## Confusion counts per seed, test fold

TP, FP, TN and FN at each validation-chosen threshold.

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN |
|---|---|---|---|
| 42 | config full | 76 / 7 / 56644 / 19 | 81 / 224 / 56427 / 14 |
| 43 | config full | 69 / 6 / 56645 / 26 | 76 / 148 / 56503 / 19 |
| 44 | config full | 71 / 8 / 56643 / 24 | 80 / 202 / 56449 / 15 |
| 45 | config full | 75 / 7 / 56644 / 20 | 78 / 160 / 56491 / 17 |
| 46 | config full | 79 / 12 / 56639 / 16 | 82 / 207 / 56444 / 13 |
| 47 | config full | 74 / 12 / 56639 / 21 | 78 / 218 / 56433 / 17 |
| 48 | config full | 80 / 15 / 56636 / 15 | 85 / 212 / 56439 / 10 |
| 49 | config full | 70 / 4 / 56647 / 25 | 77 / 199 / 56452 / 18 |
| 50 | config full | 70 / 9 / 56642 / 25 | 76 / 202 / 56449 / 19 |
| 51 | config full | 70 / 14 / 56637 / 25 | 76 / 186 / 56465 / 19 |

## Limits

- Each validation fold holds about 95 frauds, so validation AUPRC is noisy. Here the same configuration (`full`) was chosen on every seed.
- One protocol and one grid per algorithm. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

