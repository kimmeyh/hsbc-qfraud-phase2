# XGBoost on ULB: best achievable result (F166)

**BLUF.** Tuned on validation and scored on the test fold over 10 seeds (42-51), XGBoost reaches a mean test AUPRC of 0.8229 (95% t interval 0.7976 to 0.8482). It is number 3 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [ULB_COMPARISON.md](ULB_COMPARISON.md).

- **Card**: F166 (Sprint 29 Task F, #69), the ULB part of F157.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F166", written before any score.
- **Evidence**: `experiments/phase2/results/f166_ulb_algorithms.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f166_ulb_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: ULB with duplicates dropped, `data.stratified_split` (60/20/20). Tuning reads the training and validation folds; every score here is on the test fold.
- **Setup**: `XGBClassifier`, `random_state=seed`, all 30 columns; the library default (depth 6, rate 0.3, 100 trees) is one of the grid.

## Configurations tried

8 configurations, named in the entry before any score. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| learning_rate 0.1, max_depth 3, n_estimators 100 | 0 of 10 |
| learning_rate 0.1, max_depth 3, n_estimators 300 | 3 of 10 |
| learning_rate 0.3, max_depth 3, n_estimators 100 | 0 of 10 |
| learning_rate 0.3, max_depth 3, n_estimators 300 | 0 of 10 |
| learning_rate 0.1, max_depth 6, n_estimators 100 | 1 of 10 |
| learning_rate 0.1, max_depth 6, n_estimators 300 | 6 of 10 |
| learning_rate 0.3, max_depth 6, n_estimators 100 | 0 of 10 |
| learning_rate 0.3, max_depth 6, n_estimators 300 | 0 of 10 |

## Test-fold results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.8229 | 0.0354 | 0.7976 to 0.8482 |
| AUPRC, floor-normalized | 0.8226 | 0.0354 | 0.7972 to 0.8479 |
| ROC-AUC | 0.9744 | 0.0081 | 0.9686 to 0.9802 |
| Recall at the 0.5% budget, test fold | 0.8589 | 0.0315 | 0.8364 to 0.8815 |
| Train-test AUPRC gap | 0.1770 | 0.0354 | 0.1517 to 0.2024 |

At the max-F1 threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.9421 | 0.0259 | 0.9236 to 0.9606 |
| Recall | 0.7611 | 0.0452 | 0.7287 to 0.7934 |
| Specificity | 0.9999 | 0.0000 | 0.9999 to 0.9999 |
| F1 | 0.8411 | 0.0290 | 0.8204 to 0.8618 |
| MCC | 0.8461 | 0.0272 | 0.8267 to 0.8655 |
| Balanced accuracy | 0.8805 | 0.0226 | 0.8643 to 0.8967 |

At the 0.5% alert-budget threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.2905 | 0.0117 | 0.2822 to 0.2989 |
| Recall | 0.8558 | 0.0314 | 0.8333 to 0.8783 |
| Specificity | 0.9965 | 0.0003 | 0.9963 to 0.9967 |
| F1 | 0.4335 | 0.0120 | 0.4249 to 0.4421 |
| MCC | 0.4972 | 0.0106 | 0.4896 to 0.5047 |
| Balanced accuracy | 0.9261 | 0.0156 | 0.9150 to 0.9373 |

## Confusion counts per seed, test fold

TP, FP, TN and FN at each validation-chosen threshold.

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN |
|---|---|---|---|
| 42 | learning_rate 0.1, max_depth 6, n_estimators 300 | 77 / 4 / 56647 / 18 | 86 / 213 / 56438 / 9 |
| 43 | learning_rate 0.1, max_depth 6, n_estimators 300 | 67 / 4 / 56647 / 28 | 78 / 177 / 56474 / 17 |
| 44 | learning_rate 0.1, max_depth 6, n_estimators 300 | 67 / 4 / 56647 / 28 | 82 / 185 / 56466 / 13 |
| 45 | learning_rate 0.1, max_depth 6, n_estimators 300 | 70 / 1 / 56650 / 25 | 83 / 211 / 56440 / 12 |
| 46 | learning_rate 0.1, max_depth 3, n_estimators 300 | 73 / 9 / 56642 / 22 | 81 / 210 / 56441 / 14 |
| 47 | learning_rate 0.1, max_depth 3, n_estimators 300 | 75 / 7 / 56644 / 20 | 81 / 195 / 56456 / 14 |
| 48 | learning_rate 0.1, max_depth 6, n_estimators 300 | 80 / 4 / 56647 / 15 | 85 / 227 / 56424 / 10 |
| 49 | learning_rate 0.1, max_depth 3, n_estimators 300 | 74 / 3 / 56648 / 21 | 81 / 187 / 56464 / 14 |
| 50 | learning_rate 0.1, max_depth 6, n_estimators 100 | 71 / 4 / 56647 / 24 | 76 / 186 / 56465 / 19 |
| 51 | learning_rate 0.1, max_depth 6, n_estimators 300 | 69 / 5 / 56646 / 26 | 80 / 200 / 56451 / 15 |

## Limits

- Each validation fold holds about 95 frauds, so validation AUPRC is noisy and the chosen configuration changes between seeds.
- One protocol and one grid per algorithm. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

