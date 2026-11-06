# SPECTRA oilgas_gasturbine: seven algorithms compared (F157)

**BLUF.** Over 10 seeds (42-51), the order by mean test AUPRC is LightGBM, CatBoost, XGBoost, HGB, SVM, the proxy and logistic regression. Of the six adjacent pairs, 4 differ reliably under the entry's test: LightGBM above CatBoost; HGB above SVM; SVM above the proxy; CVQBoost proxy above logistic regression. No other adjacent pair differs reliably, so the order among CatBoost, XGBoost and HGB is not established.

- **Card**: F157 (Sprint 31 Task F, #98), the SPECTRA part: F166's algorithms and grids on SPECTRA's four datasets.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F157 SPECTRA part", written before any score.
- **Amendment**: the SVM lane is the form the entry's rule keeps, scored on the test fold under the entry's amendment of 2026-11-05 (Sprint 31 D14 option 1). The first result, `experiments/phase2/results/f157_spectra_algorithms.json`, is kept as recorded; it scored the linear form only.
- **Evidence**: `experiments/phase2/results/f157_spectra_algorithms_rbf.json` (evidence tag SIM, zero metered seconds). Every figure below comes from that file.
- **Seeds**: seed 42 took 4.71 minutes for all seven algorithms, so the entry's rule gave 10 seeds.
- **Data**: SPECTRA `oilgas_gasturbine`, label `target`, spectra_segment.spectra_split 60/20/20, seeded. Tuning reads the training and validation folds; every score here is on the test fold (7,347 rows, 2,050 positives per seed; 15 feature columns).

## Mean test AUPRC, in order

TP, FP, TN and FN are at the test fold's own 0.5% budget, each the minimum to the maximum over the 10 seeds; each algorithm page gives them per seed.

| Order | Algorithm | Mean | 95% t interval | Recall at the 0.5% budget, mean | TP | FP | TN | FN | Document |
|---|---|---|---|---|---|---|---|---|---|
| 1 | LightGBM | 0.8785 | 0.8736 to 0.8834 | 0.0180 | 36 to 37 | 0 to 1 | 5,296 to 5,297 | 2,013 to 2,014 | [OILGAS_GASTURBINE_LIGHTGBM.md](OILGAS_GASTURBINE_LIGHTGBM.md) |
| 2 | CatBoost | 0.8753 | 0.8709 to 0.8797 | 0.0180 | 37 to 37 | 0 to 0 | 5,297 to 5,297 | 2,013 to 2,013 | [OILGAS_GASTURBINE_CATBOOST.md](OILGAS_GASTURBINE_CATBOOST.md) |
| 3 | XGBoost | 0.8750 | 0.8705 to 0.8794 | 0.0180 | 37 to 37 | 0 to 0 | 5,297 to 5,297 | 2,013 to 2,013 | [OILGAS_GASTURBINE_XGBOOST.md](OILGAS_GASTURBINE_XGBOOST.md) |
| 4 | HGB | 0.8730 | 0.8677 to 0.8782 | 0.0180 | 36 to 38 | 0 to 1 | 5,296 to 5,297 | 2,012 to 2,014 | [OILGAS_GASTURBINE_HGB.md](OILGAS_GASTURBINE_HGB.md) |
| 5 | SVM | 0.8532 | 0.8478 to 0.8587 | 0.0179 | 36 to 37 | 0 to 1 | 5,296 to 5,297 | 2,013 to 2,014 | [OILGAS_GASTURBINE_SVM.md](OILGAS_GASTURBINE_SVM.md) |
| 6 | CVQBoost proxy | 0.8394 | 0.8339 to 0.8449 | 0.0180 | 35 to 37 | 0 to 2 | 5,295 to 5,297 | 2,013 to 2,015 | [OILGAS_GASTURBINE_CVQBOOST_PROXY.md](OILGAS_GASTURBINE_CVQBOOST_PROXY.md) |
| 7 | Logistic regression | 0.7811 | 0.7771 to 0.7850 | 0.0179 | 36 to 37 | 0 to 1 | 5,296 to 5,297 | 2,013 to 2,014 | [OILGAS_GASTURBINE_LOGISTIC_REGRESSION.md](OILGAS_GASTURBINE_LOGISTIC_REGRESSION.md) |

## Adjacent pairs

The entry's test (F166's): with 10 seeds (8 or more), the exact two-sided Wilcoxon signed-rank test on per-seed AUPRC differences is primary, at Bonferroni 0.05 / 6. "A above B" is written only when it rejects. Only adjacent pairs are tested, so a non-adjacent statement is not made here.

- LightGBM against CatBoost: mean difference 0.0032, Wilcoxon p 0.0039; reading: above
- CatBoost against XGBoost: mean difference 0.0003, Wilcoxon p 0.7695; reading: no reliable difference
- XGBoost against HGB: mean difference 0.0020, Wilcoxon p 0.0137; reading: no reliable difference
- HGB against SVM: mean difference 0.0197, Wilcoxon p 0.0020; reading: above
- SVM against CVQBoost proxy: mean difference 0.0138, Wilcoxon p 0.0020; reading: above
- CVQBoost proxy against Logistic regression: mean difference 0.0583, Wilcoxon p 0.0020; reading: above

## In and out of the pocket (secondary)

Test AUPRC inside the pocket (`in_pocket` = 1) and outside it, mean over seeds, as the entry reports it.

| Algorithm | In the pocket | Out of the pocket |
|---|---|---|
| LightGBM | 0.8038 (10 seeds) | 0.9323 (10 seeds) |
| CatBoost | 0.7909 (10 seeds) | 0.9293 (10 seeds) |
| XGBoost | 0.7923 (10 seeds) | 0.9301 (10 seeds) |
| HGB | 0.7824 (10 seeds) | 0.9280 (10 seeds) |
| SVM | 0.7540 (10 seeds) | 0.9264 (10 seeds) |
| CVQBoost proxy | 0.7806 (10 seeds) | 0.9166 (10 seeds) |
| Logistic regression | 0.7147 (10 seeds) | 0.8610 (10 seeds) |

## Notes

- At the test fold's own 0.5% alert budget, mean recall lies between 0.0179 and 0.0180. The budget is set for fraud rates; these datasets' positive rates are far higher, so the budget can catch only a small share of their positives.
- At the test fold's own budget, scores tied at the budget's last place are all flagged, so a lane can flag more rows than the budget: HGB on 1 of 10 seeds, up to 38 rows against a budget of 37. The counts include those rows.
- The entry keeps the RBF form only if its best validation AUPRC beats the linear form's on a majority of seeds. It did so on 10 of 10 seeds, so the entry's rule keeps the **rbf** form. Every SVM figure here, its place in the order and its adjacent pairs are the RBF form's, scored on the test fold under the D14 amendment. The linear form is reported on the SVM page, not ranked. ([OILGAS_GASTURBINE_SVM.md](OILGAS_GASTURBINE_SVM.md))
