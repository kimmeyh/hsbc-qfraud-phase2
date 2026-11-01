# XGBoost on IEEE-CIS: best achievable result (F174)

**BLUF.** Tuned on month 3 and scored on month 4 over 10 seeds (42-51), XGBoost reaches a mean test AUPRC of 0.4960 (95% t interval 0.4960 to 0.4960). It is number 4 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [IEEE_COMPARISON.md](IEEE_COMPARISON.md). The ULB page for the same algorithm is [ULB_XGBOOST.md](ULB_XGBOOST.md).

- **Card**: F174 (Sprint 30 Task D, #78), the IEEE-CIS part of F157.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F174", written before any score.
- **Evidence**: `experiments/phase2/results/f174_ieee_algorithms.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f174_ieee_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: IEEE-CIS with exact duplicates dropped (3 rows), F105's month folds and F152's item-4 controls. Tuning fits months 0-2 and chooses on month 3 (98,027 rows); the chosen configuration is fitted again on months 0-3 and scored once on month 4 (85,302 rows). Every score here is on month 4.
- **Setup**: `XGBClassifier`, `random_state=seed`, every column the fold keeps; the library default (depth 6, rate 0.3, 100 trees) is one of the grid.

## Configurations tried

8 configurations, F166's grid, imported unchanged. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| learning_rate 0.1, max_depth 3, n_estimators 100 | 0 of 10 |
| learning_rate 0.1, max_depth 3, n_estimators 300 | 0 of 10 |
| learning_rate 0.3, max_depth 3, n_estimators 100 | 0 of 10 |
| learning_rate 0.3, max_depth 3, n_estimators 300 | 0 of 10 |
| learning_rate 0.1, max_depth 6, n_estimators 100 | 0 of 10 |
| learning_rate 0.1, max_depth 6, n_estimators 300 | 10 of 10 |
| learning_rate 0.3, max_depth 6, n_estimators 100 | 0 of 10 |
| learning_rate 0.3, max_depth 6, n_estimators 300 | 0 of 10 |

## Test-month results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.4960 | 0.0000 | 0.4960 to 0.4960 |
| AUPRC, floor-normalized | 0.4779 | 0.0000 | 0.4779 to 0.4779 |
| ROC-AUC | 0.8618 | 0.0000 | 0.8618 to 0.8618 |
| Recall at the 0.5% budget, test fold | 0.1364 | 0.0000 | 0.1364 to 0.1364 |
| Train-test AUPRC gap | 0.3169 | 0.0000 | 0.3169 to 0.3169 |

XGBoost gives the same test AUPRC on every seed. It chose the same configuration on every seed, and the months are fixed, so the seed does not change the result. The SD is 0 and the interval has no width: the 10 seeds are one result.

At the max-F1 threshold chosen on the validation month:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.7543 | 0.0000 | 0.7543 to 0.7543 |
| Recall | 0.3835 | 0.0000 | 0.3835 to 0.3835 |
| Specificity | 0.9955 | 0.0000 | 0.9955 to 0.9955 |
| F1 | 0.5085 | 0.0000 | 0.5085 to 0.5085 |
| MCC | 0.5269 | 0.0000 | 0.5269 to 0.5269 |
| Balanced accuracy | 0.6895 | 0.0000 | 0.6895 to 0.6895 |

At the 0.5% alert-budget threshold chosen on the validation month:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.9766 | 0.0000 | 0.9766 to 0.9766 |
| Recall | 0.0844 | 0.0000 | 0.0844 to 0.0844 |
| Specificity | 0.9999 | 0.0000 | 0.9999 to 0.9999 |
| F1 | 0.1554 | 0.0000 | 0.1554 to 0.1554 |
| MCC | 0.2822 | 0.0000 | 0.2822 to 0.2822 |
| Balanced accuracy | 0.5422 | 0.0000 | 0.5422 to 0.5422 |

On the test month this threshold flags 256 of 85,302 test rows; the month's own 0.5% budget is 427 rows. The threshold is chosen on the validation month, so its alert volume on the test month is not the budget. The row "Recall at the 0.5% budget, test fold" above uses the test month's own budget.

## Confusion counts per seed, test month

TP, FP, TN and FN at each threshold chosen on the validation month, and at the test month's own 0.5% budget (the comparison page's recall).

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN | 0.5% budget on the test month: TP / FP / TN / FN |
|---|---|---|---|---|
| 42 | learning_rate 0.1, max_depth 6, n_estimators 300 | 1136 / 370 / 81970 / 1826 | 250 / 6 / 82334 / 2712 | 404 / 23 / 82317 / 2558 |
| 43 | learning_rate 0.1, max_depth 6, n_estimators 300 | 1136 / 370 / 81970 / 1826 | 250 / 6 / 82334 / 2712 | 404 / 23 / 82317 / 2558 |
| 44 | learning_rate 0.1, max_depth 6, n_estimators 300 | 1136 / 370 / 81970 / 1826 | 250 / 6 / 82334 / 2712 | 404 / 23 / 82317 / 2558 |
| 45 | learning_rate 0.1, max_depth 6, n_estimators 300 | 1136 / 370 / 81970 / 1826 | 250 / 6 / 82334 / 2712 | 404 / 23 / 82317 / 2558 |
| 46 | learning_rate 0.1, max_depth 6, n_estimators 300 | 1136 / 370 / 81970 / 1826 | 250 / 6 / 82334 / 2712 | 404 / 23 / 82317 / 2558 |
| 47 | learning_rate 0.1, max_depth 6, n_estimators 300 | 1136 / 370 / 81970 / 1826 | 250 / 6 / 82334 / 2712 | 404 / 23 / 82317 / 2558 |
| 48 | learning_rate 0.1, max_depth 6, n_estimators 300 | 1136 / 370 / 81970 / 1826 | 250 / 6 / 82334 / 2712 | 404 / 23 / 82317 / 2558 |
| 49 | learning_rate 0.1, max_depth 6, n_estimators 300 | 1136 / 370 / 81970 / 1826 | 250 / 6 / 82334 / 2712 | 404 / 23 / 82317 / 2558 |
| 50 | learning_rate 0.1, max_depth 6, n_estimators 300 | 1136 / 370 / 81970 / 1826 | 250 / 6 / 82334 / 2712 | 404 / 23 / 82317 / 2558 |
| 51 | learning_rate 0.1, max_depth 6, n_estimators 300 | 1136 / 370 / 81970 / 1826 | 250 / 6 / 82334 / 2712 | 404 / 23 / 82317 / 2558 |

## Limits

- The validation month holds about 3,849 frauds, so validation AUPRC is less noisy than on ULB. Here the same configuration (learning_rate 0.1, max_depth 6, n_estimators 300) was chosen on every seed.
- One protocol and one grid per algorithm, F166's. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- One test month. Month-to-month drift is outside this result; F152 scores months 4-6.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

