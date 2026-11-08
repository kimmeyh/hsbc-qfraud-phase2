# SVM on SPECTRA energy_steel: best result within F166's grid (F157)

**BLUF.** Tuned on validation and scored on the test fold over 10 seeds (42-51), SVM reaches a mean test AUPRC of 0.6247 (95% t interval 0.3963 to 0.8530). It is number 7 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [ENERGY_STEEL_COMPARISON.md](ENERGY_STEEL_COMPARISON.md).

- **Card**: F157 (Sprint 31 Task F, #98), the SPECTRA part: F166's algorithms and grids on SPECTRA's four datasets.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F157 SPECTRA part", written before any score.
- **Amendment**: the SVM lane is the form the entry's rule keeps, scored on the test fold under the entry's amendment of 2026-11-05 (Sprint 31 D14 option 1). The first result, `experiments/phase2/results/f157_spectra_algorithms.json`, is kept as recorded; it scored the linear form only. The amendment was written after that result was seen; the other six lanes are unchanged from it.
- **Evidence**: `experiments/phase2/results/f157_spectra_algorithms_rbf.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f157_spectra_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: SPECTRA `energy_steel`, label `target`, spectra_segment.spectra_split 60/20/20, seeded. Tuning reads the training and validation folds; every score here is on the test fold (7,008 rows, 1,782 positives per seed; 17 feature columns).

## Configurations tried

2 configurations, F166's grid, imported unchanged. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| C 1.0 | 4 of 10 |
| C 10.0 | 6 of 10 |

## The SVM's form

The RBF SVM is fitted on a stratified subsample of at most 20,000 training rows (the whole fold when smaller). The entry keeps the RBF form only if its best validation AUPRC beats the linear form's on a majority of seeds. It did so on 6 of 10 seeds, so the entry's rule keeps the **rbf** form. Every SVM figure here, its place in the order and its adjacent pairs are the RBF form's, scored on the test fold under the D14 amendment. The linear form is reported on the SVM page, not ranked.

The linear form (`LinearSVC`, all training rows, F166's grid), which the rule did not keep: mean test AUPRC 0.6484 over 10 seeds, from 0.2543 to 0.7177 (the SVM figures of `experiments/phase2/results/f157_spectra_algorithms.json`). It is not ranked.

The chosen C is the grid's largest value, 10, on 6 of 10 seeds, so a larger C may do better; the grid is the entry's, not widened here.

On seeds 42, 44, 45, 46 the RBF form's best validation AUPRC equals the test fold's positive rate to four places, which is what a score with no ranking gets. They count as linear wins, so they do not add to the RBF majority.

On seeds 44, 45, 46 the scored RBF lane's test AUPRC is also the positive rate: no ranking there either, and those seeds are scored as they are, as the amendment sets.

On seed 42 the RBF scores carry no ranking on validation but do on test. **Not explained**: the same fit gives constant scores on one fold and ranked scores on the other. A cause in this dataset's features (the date columns parsed per fold, which raise a format warning) is a guess, not tested.

On seed 49 the reverse holds: the RBF scores carry a ranking on validation and none on test. **Not explained** either.

## Test-fold results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.6247 | 0.3192 | 0.3963 to 0.8530 |
| AUPRC, floor-normalized | 0.4967 | 0.4281 | 0.1905 to 0.8029 |
| ROC-AUC | 0.7745 | 0.2363 | 0.6055 to 0.9435 |
| Recall at the 0.5% budget, test fold | 0.4120 | 0.5061 | 0.0499 to 0.7740 |
| Train-test AUPRC gap | 0.2561 | 0.3062 | 0.0371 to 0.4751 |

Secondary, as the entry reports it: test AUPRC inside the pocket (`in_pocket` = 1) 0.8364 (95% t interval 0.7793 to 0.8936, 10 seeds) and outside it 0.5599 (0.3048 to 0.8150, 10 seeds).

At the max-F1 threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.5013 | 0.2888 | 0.2946 to 0.7079 |
| Recall | 0.8380 | 0.3013 | 0.6224 to 1.0536 |
| Specificity | 0.6149 | 0.4339 | 0.3045 to 0.9253 |
| F1 | 0.5918 | 0.2779 | 0.3930 to 0.7906 |
| MCC | 0.4268 | 0.3716 | 0.1610 to 0.6926 |
| Balanced accuracy | 0.7264 | 0.1961 | 0.5862 to 0.8667 |

At the 0.5% alert-budget threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.6182 | 0.4049 | 0.3285 to 0.9079 |
| Recall | 0.4105 | 0.5071 | 0.0478 to 0.7733 |
| Specificity | 0.6641 | 0.4714 | 0.3269 to 1.0014 |
| F1 | 0.2080 | 0.2354 | 0.0397 to 0.3764 |
| MCC | 0.1182 | 0.1667 | -0.0010 to 0.2375 |
| Balanced accuracy | 0.5373 | 0.0996 | 0.4661 to 0.6086 |

## Confusion counts per seed, test fold

TP, FP, TN and FN at each validation-chosen threshold, and at the test fold's own 0.5% budget (the comparison page's recall).

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN | 0.5% budget on the test fold: TP / FP / TN / FN |
|---|---|---|---|---|
| 42 | C 1.0 | 1780 / 1871 / 3355 / 2 | 1780 / 1871 / 3355 / 2 | 36 / 0 / 5226 / 1746 |
| 43 | C 10.0 | 1567 / 542 / 4684 / 215 | 43 / 2 / 5224 / 1739 | 34 / 2 / 5224 / 1748 |
| 44 | C 1.0 | 1782 / 5226 / 0 / 0 | 1782 / 5226 / 0 / 0 | 1782 / 5226 / 0 / 0 |
| 45 | C 1.0 | 1782 / 5226 / 0 / 0 | 1782 / 5226 / 0 / 0 | 1782 / 5226 / 0 / 0 |
| 46 | C 1.0 | 1782 / 5226 / 0 / 0 | 1782 / 5226 / 0 / 0 | 1782 / 5226 / 0 / 0 |
| 47 | C 10.0 | 1616 / 578 / 4648 / 166 | 36 / 0 / 5226 / 1746 | 36 / 0 / 5226 / 1746 |
| 48 | C 10.0 | 1483 / 441 / 4785 / 299 | 37 / 0 / 5226 / 1745 | 36 / 0 / 5226 / 1746 |
| 49 | C 10.0 | 0 / 0 / 5226 / 1782 | 0 / 0 / 5226 / 1782 | 1782 / 5226 / 0 / 0 |
| 50 | C 10.0 | 1555 / 478 / 4748 / 227 | 41 / 1 / 5225 / 1741 | 35 / 1 / 5225 / 1747 |
| 51 | C 10.0 | 1586 / 537 / 4689 / 196 | 33 / 0 / 5226 / 1749 | 36 / 0 / 5226 / 1746 |

## Limits

- One protocol and one grid per algorithm, F166's. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

