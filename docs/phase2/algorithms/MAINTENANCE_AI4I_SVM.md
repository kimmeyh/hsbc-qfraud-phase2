# SVM on SPECTRA maintenance_ai4i: best result within F166's grid (F157)

**BLUF.** Tuned on validation and scored on the test fold over 10 seeds (42-51), SVM reaches a mean test AUPRC of 0.5343 (95% t interval 0.5176 to 0.5509). It is number 6 of 7 by mean test AUPRC; the ranking and which differences are reliable are on [MAINTENANCE_AI4I_COMPARISON.md](MAINTENANCE_AI4I_COMPARISON.md).

- **Card**: F157 (Sprint 31 Task F, #98), the SPECTRA part: F166's algorithms and grids on SPECTRA's four datasets.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F157 SPECTRA part", written before any score.
- **Amendment**: the SVM lane is the form the entry's rule keeps, scored on the test fold under the entry's amendment of 2026-11-05 (Sprint 31 D14 option 1). The first result, `experiments/phase2/results/f157_spectra_algorithms.json`, is kept as recorded; it scored the linear form only. The amendment was written after that result was seen; the other six lanes are unchanged from it.
- **Evidence**: `experiments/phase2/results/f157_spectra_algorithms_rbf.json` (evidence tag SIM, zero metered seconds), generator `experiments/phase2/src/f157_spectra_algorithms.py`. Every figure below comes from that file. Each seed's outcome block is in the file's rows; the per-row test scores it names are in `experiments/phase2/predictions/` (gitignored, kept on this machine), each recorded with its SHA-256.
- **Data**: SPECTRA `maintenance_ai4i`, label `target`, spectra_segment.spectra_split 60/20/20, seeded. Tuning reads the training and validation folds; every score here is on the test fold (2,000 rows, 235 positives per seed; 12 feature columns).

## Configurations tried

2 configurations, F166's grid, imported unchanged. Per seed, the one with the highest validation AUPRC was kept (ties: the first listed).

| Configuration | Seeds that chose it |
|---|---|
| C 1.0 | 8 of 10 |
| C 10.0 | 2 of 10 |

## The SVM's form

The RBF SVM is fitted on a stratified subsample of at most 20,000 training rows (the whole fold when smaller). The entry keeps the RBF form only if its best validation AUPRC beats the linear form's on a majority of seeds. It did so on 7 of 10 seeds, so the entry's rule keeps the **rbf** form. Every SVM figure here, its place in the order and its adjacent pairs are the RBF form's, scored on the test fold under the D14 amendment. The linear form is reported on the SVM page, not ranked.

The linear form (`LinearSVC`, all training rows, F166's grid), which the rule did not keep: mean test AUPRC 0.5184 over 10 seeds, from 0.4910 to 0.5644 (the SVM figures of `experiments/phase2/results/f157_spectra_algorithms.json`). It is not ranked.

The chosen C is the grid's largest value, 10, on 2 of 10 seeds, so a larger C may do better; the grid is the entry's, not widened here.

## Test-fold results over seeds

Mean, SD and 95% t interval over 10 seeds, each seed at its own chosen configuration.

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| AUPRC | 0.5343 | 0.0232 | 0.5176 to 0.5509 |
| AUPRC, floor-normalized | 0.4723 | 0.0263 | 0.4534 to 0.4911 |
| ROC-AUC | 0.8751 | 0.0153 | 0.8642 to 0.8861 |
| Recall at the 0.5% budget, test fold | 0.0362 | 0.0041 | 0.0332 to 0.0391 |
| Train-test AUPRC gap | 0.0892 | 0.0570 | 0.0485 to 0.1300 |

Secondary, as the entry reports it: test AUPRC inside the pocket (`in_pocket` = 1) 0.6027 (95% t interval 0.5880 to 0.6174, 10 seeds) and outside it 0.6248 (0.5798 to 0.6697, 10 seeds).

At the max-F1 threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.5013 | 0.0215 | 0.4859 to 0.5166 |
| Recall | 0.6174 | 0.0570 | 0.5767 to 0.6582 |
| Specificity | 0.9178 | 0.0115 | 0.9096 to 0.9260 |
| F1 | 0.5518 | 0.0229 | 0.5354 to 0.5682 |
| MCC | 0.4896 | 0.0268 | 0.4705 to 0.5088 |
| Balanced accuracy | 0.7676 | 0.0240 | 0.7504 to 0.7848 |

At the 0.5% alert-budget threshold chosen on validation:

| Metric | Mean | SD | 95% t interval |
|---|---|---|---|
| Precision | 0.8549 | 0.0892 | 0.7911 to 0.9187 |
| Recall | 0.0417 | 0.0130 | 0.0324 to 0.0510 |
| Specificity | 0.9991 | 0.0005 | 0.9988 to 0.9994 |
| F1 | 0.0793 | 0.0236 | 0.0624 to 0.0961 |
| MCC | 0.1726 | 0.0336 | 0.1486 to 0.1966 |
| Balanced accuracy | 0.5204 | 0.0065 | 0.5157 to 0.5251 |

## Confusion counts per seed, test fold

TP, FP, TN and FN at each validation-chosen threshold, and at the test fold's own 0.5% budget (the comparison page's recall).

| Seed | Chosen configuration | max-F1: TP / FP / TN / FN | 0.5% budget: TP / FP / TN / FN | 0.5% budget on the test fold: TP / FP / TN / FN |
|---|---|---|---|---|
| 42 | C 1.0 | 156 / 152 / 1613 / 79 | 9 / 2 / 1763 / 226 | 8 / 2 / 1763 / 227 |
| 43 | C 1.0 | 166 / 179 / 1586 / 69 | 16 / 2 / 1763 / 219 | 9 / 1 / 1764 / 226 |
| 44 | C 1.0 | 132 / 126 / 1639 / 103 | 8 / 1 / 1764 / 227 | 9 / 1 / 1764 / 226 |
| 45 | C 10.0 | 136 / 152 / 1613 / 99 | 9 / 2 / 1763 / 226 | 8 / 2 / 1763 / 227 |
| 46 | C 1.0 | 139 / 153 / 1612 / 96 | 8 / 0 / 1765 / 227 | 9 / 1 / 1764 / 226 |
| 47 | C 1.0 | 160 / 169 / 1596 / 75 | 6 / 2 / 1763 / 229 | 7 / 3 / 1762 / 228 |
| 48 | C 1.0 | 135 / 116 / 1649 / 100 | 7 / 3 / 1762 / 228 | 7 / 3 / 1762 / 228 |
| 49 | C 10.0 | 128 / 125 / 1640 / 107 | 10 / 2 / 1763 / 225 | 9 / 1 / 1764 / 226 |
| 50 | C 1.0 | 157 / 148 / 1617 / 78 | 12 / 1 / 1764 / 223 | 10 / 0 / 1765 / 225 |
| 51 | C 1.0 | 142 / 131 / 1634 / 93 | 13 / 1 / 1764 / 222 | 9 / 1 / 1764 / 226 |

## Limits

- One protocol and one grid per algorithm, F166's. A larger grid may do better; this is the best of the configurations named in the entry, not the best possible.
- Device lanes (CVQBoost on hardware, QSVM) and QNN are outside this part of F157.

