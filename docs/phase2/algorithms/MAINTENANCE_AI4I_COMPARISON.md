# SPECTRA maintenance_ai4i: seven algorithms compared (F157)

**BLUF.** Over 10 seeds (42-51), the order by mean test AUPRC is CatBoost, HGB, XGBoost, LightGBM, the proxy, SVM and logistic regression. Of the six adjacent pairs, 1 differs reliably under the entry's test: LightGBM above the proxy. No other adjacent pair differs reliably, so the order among CatBoost, HGB, XGBoost and LightGBM; the proxy, SVM and logistic regression is not established.

- **Card**: F157 (Sprint 31 Task F, #98), the SPECTRA part: F166's algorithms and grids on SPECTRA's four datasets.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F157 SPECTRA part", written before any score.
- **Amendment**: the SVM lane is the form the entry's rule keeps, scored on the test fold under the entry's amendment of 2026-11-05 (Sprint 31 D14 option 1). The first result, `experiments/phase2/results/f157_spectra_algorithms.json`, is kept as recorded; it scored the linear form only.
- **Evidence**: `experiments/phase2/results/f157_spectra_algorithms_rbf.json` (evidence tag SIM, zero metered seconds). Every figure below comes from that file.
- **Seeds**: seed 42 took 1.1 minutes for all seven algorithms, so the entry's rule gave 10 seeds.
- **Data**: SPECTRA `maintenance_ai4i`, label `target`, spectra_segment.spectra_split 60/20/20, seeded. Tuning reads the training and validation folds; every score here is on the test fold (2,000 rows, 235 positives per seed; 12 feature columns).

## Mean test AUPRC, in order

TP, FP, TN and FN are at the test fold's own 0.5% budget, each the minimum to the maximum over the 10 seeds; each algorithm page gives them per seed.

| Order | Algorithm | Mean | 95% t interval | Recall at the 0.5% budget, mean | TP | FP | TN | FN | Document |
|---|---|---|---|---|---|---|---|---|---|
| 1 | CatBoost | 0.6368 | 0.6222 to 0.6515 | 0.0417 | 9 to 10 | 0 to 1 | 1,764 to 1,765 | 225 to 226 | [MAINTENANCE_AI4I_CATBOOST.md](MAINTENANCE_AI4I_CATBOOST.md) |
| 2 | HGB | 0.6310 | 0.6210 to 0.6410 | 0.0426 | 10 to 10 | 0 to 0 | 1,765 to 1,765 | 225 to 225 | [MAINTENANCE_AI4I_HGB.md](MAINTENANCE_AI4I_HGB.md) |
| 3 | XGBoost | 0.6183 | 0.6034 to 0.6331 | 0.0409 | 9 to 10 | 0 to 1 | 1,764 to 1,765 | 225 to 226 | [MAINTENANCE_AI4I_XGBOOST.md](MAINTENANCE_AI4I_XGBOOST.md) |
| 4 | LightGBM | 0.6148 | 0.5992 to 0.6303 | 0.0396 | 8 to 10 | 0 to 2 | 1,763 to 1,765 | 225 to 227 | [MAINTENANCE_AI4I_LIGHTGBM.md](MAINTENANCE_AI4I_LIGHTGBM.md) |
| 5 | CVQBoost proxy | 0.5387 | 0.5225 to 0.5548 | 0.0328 | 6 to 9 | 1 to 4 | 1,761 to 1,764 | 226 to 229 | [MAINTENANCE_AI4I_CVQBOOST_PROXY.md](MAINTENANCE_AI4I_CVQBOOST_PROXY.md) |
| 6 | SVM | 0.5343 | 0.5176 to 0.5509 | 0.0362 | 7 to 10 | 0 to 3 | 1,762 to 1,765 | 225 to 228 | [MAINTENANCE_AI4I_SVM.md](MAINTENANCE_AI4I_SVM.md) |
| 7 | Logistic regression | 0.5126 | 0.4951 to 0.5300 | 0.0366 | 7 to 10 | 0 to 3 | 1,762 to 1,765 | 225 to 228 | [MAINTENANCE_AI4I_LOGISTIC_REGRESSION.md](MAINTENANCE_AI4I_LOGISTIC_REGRESSION.md) |

## Adjacent pairs

The entry's test (F166's): with 10 seeds (8 or more), the exact two-sided Wilcoxon signed-rank test on per-seed AUPRC differences is primary, at Bonferroni 0.05 / 6. "A above B" is written only when it rejects. Only adjacent pairs are tested, so a non-adjacent statement is not made here.

- CatBoost against HGB: mean difference 0.0058, Wilcoxon p 0.4922; reading: no reliable difference
- HGB against XGBoost: mean difference 0.0127, Wilcoxon p 0.0195; reading: no reliable difference
- XGBoost against LightGBM: mean difference 0.0035, Wilcoxon p 0.5566; reading: no reliable difference
- LightGBM against CVQBoost proxy: mean difference 0.0761, Wilcoxon p 0.0020; reading: above
- CVQBoost proxy against SVM: mean difference 0.0044, Wilcoxon p 0.7695; reading: no reliable difference
- SVM against Logistic regression: mean difference 0.0217, Wilcoxon p 0.1934; reading: no reliable difference

## In and out of the pocket (secondary)

Test AUPRC inside the pocket (`in_pocket` = 1) and outside it, mean over seeds, as the entry reports it.

| Algorithm | In the pocket | Out of the pocket |
|---|---|---|
| CatBoost | 0.6383 (10 seeds) | 0.7023 (10 seeds) |
| HGB | 0.6336 (10 seeds) | 0.6906 (10 seeds) |
| XGBoost | 0.6276 (10 seeds) | 0.6681 (10 seeds) |
| LightGBM | 0.6284 (10 seeds) | 0.6624 (10 seeds) |
| CVQBoost proxy | 0.5907 (10 seeds) | 0.4941 (10 seeds) |
| SVM | 0.6027 (10 seeds) | 0.6248 (10 seeds) |
| Logistic regression | 0.5914 (10 seeds) | 0.3494 (10 seeds) |

## Notes

- At the test fold's own 0.5% alert budget, mean recall lies between 0.0328 and 0.0426. The budget is set for fraud rates; these datasets' positive rates are far higher, so the budget can catch only a small share of their positives.
- The entry keeps the RBF form only if its best validation AUPRC beats the linear form's on a majority of seeds. It did so on 7 of 10 seeds, so the entry's rule keeps the **rbf** form. Every SVM figure here, its place in the order and its adjacent pairs are the RBF form's, scored on the test fold under the D14 amendment. The linear form is reported on the SVM page, not ranked. ([MAINTENANCE_AI4I_SVM.md](MAINTENANCE_AI4I_SVM.md))
