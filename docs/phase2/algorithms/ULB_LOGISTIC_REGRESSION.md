# Logistic regression on ULB: best achievable result (F166)

**BLUF.** Tuned on validation and scored on the test fold over 10 seeds (42-51), Logistic regression reaches a mean test AUPRC of 0.7270 (95% t interval 0.7050 to 0.7490). It is number 7 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [ULB_COMPARISON.md](ULB_COMPARISON.md).

- **Card**: F166 (Sprint 29 Task F, #69), the ULB part of F157.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F166", written before any score.
- **Evidence**: `experiments/phase2/results/f166_ulb_algorithms.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f166_ulb_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: ULB with duplicates dropped, `data.stratified_split` (60/20/20). Tuning reads the training and validation folds; every score here is on the test fold.
- **Setup**: `LogisticRegression`, `max_iter=2000`, all 30 columns standardized on the training fold.

## Configurations tried

8 configurations, named in the entry before any score. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| C 0.01, class_weight None | 2 of 10 |
| C 0.01, class_weight balanced | 0 of 10 |
| C 0.1, class_weight None | 5 of 10 |
| C 0.1, class_weight balanced | 0 of 10 |
| C 1.0, class_weight None | 1 of 10 |
| C 1.0, class_weight balanced | 0 of 10 |
| C 10.0, class_weight None | 2 of 10 |
| C 10.0, class_weight balanced | 0 of 10 |

No seed chose `class_weight` balanced.

## Test-fold results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.7270 | 0.0307 | 0.7050 to 0.7490 |
| AUPRC, floor-normalized | 0.7265 | 0.0308 | 0.7045 to 0.7485 |
| ROC-AUC | 0.9747 | 0.0094 | 0.9680 to 0.9815 |
| Recall at the 0.5% budget, test fold | 0.8421 | 0.0272 | 0.8227 to 0.8615 |
| Train-test AUPRC gap | 0.0291 | 0.0366 | 0.0029 to 0.0553 |

At the max-F1 threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.7624 | 0.0538 | 0.7239 to 0.8008 |
| Recall | 0.7684 | 0.0227 | 0.7522 to 0.7847 |
| Specificity | 0.9996 | 0.0001 | 0.9995 to 0.9997 |
| F1 | 0.7643 | 0.0272 | 0.7449 to 0.7837 |
| MCC | 0.7644 | 0.0273 | 0.7449 to 0.7840 |
| Balanced accuracy | 0.8840 | 0.0114 | 0.8759 to 0.8921 |

At the 0.5% alert-budget threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.2767 | 0.0186 | 0.2635 to 0.2900 |
| Recall | 0.8411 | 0.0287 | 0.8205 to 0.8616 |
| Specificity | 0.9963 | 0.0003 | 0.9961 to 0.9965 |
| F1 | 0.4162 | 0.0231 | 0.3997 to 0.4327 |
| MCC | 0.4810 | 0.0217 | 0.4654 to 0.4965 |
| Balanced accuracy | 0.9187 | 0.0144 | 0.9084 to 0.9290 |

## Confusion counts per seed, test fold

TP, FP, TN and FN at each validation-chosen threshold.

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN |
|---|---|---|---|
| 42 | C 1.0, class_weight None | 76 / 21 / 56630 / 19 | 82 / 206 / 56445 / 13 |
| 43 | C 10.0, class_weight None | 72 / 11 / 56640 / 23 | 79 / 186 / 56465 / 16 |
| 44 | C 0.1, class_weight None | 71 / 16 / 56635 / 24 | 80 / 204 / 56447 / 15 |
| 45 | C 0.1, class_weight None | 76 / 34 / 56617 / 19 | 80 / 220 / 56431 / 15 |
| 46 | C 10.0, class_weight None | 73 / 30 / 56621 / 22 | 80 / 187 / 56464 / 15 |
| 47 | C 0.01, class_weight None | 74 / 23 / 56628 / 21 | 79 / 241 / 56410 / 16 |
| 48 | C 0.1, class_weight None | 75 / 22 / 56629 / 20 | 86 / 205 / 56446 / 9 |
| 49 | C 0.1, class_weight None | 72 / 21 / 56630 / 23 | 80 / 215 / 56436 / 15 |
| 50 | C 0.01, class_weight None | 70 / 25 / 56626 / 25 | 77 / 229 / 56422 / 18 |
| 51 | C 0.1, class_weight None | 71 / 29 / 56622 / 24 | 76 / 204 / 56447 / 19 |

## Limits

- Each validation fold holds about 95 frauds, so validation AUPRC is noisy and the chosen configuration changes between seeds.
- One protocol and one grid per algorithm. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

