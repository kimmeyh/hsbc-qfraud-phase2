# SPECTRA energy_steel: seven algorithms compared (F157)

**BLUF.** Over 10 seeds (42-51), the order by mean test AUPRC is CatBoost, XGBoost, HGB, LightGBM, the proxy, logistic regression and SVM. Of the six adjacent pairs, 1 differs reliably under the entry's test: CVQBoost proxy above logistic regression. No other adjacent pair differs reliably, so the order among CatBoost, XGBoost, HGB, LightGBM and the proxy; logistic regression and SVM is not established.

- **Card**: F157 (Sprint 31 Task F, #98), the SPECTRA part: F166's algorithms and grids on SPECTRA's four datasets.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F157 SPECTRA part", written before any score.
- **Amendment**: the SVM lane is the form the entry's rule keeps, scored on the test fold under the entry's amendment of 2026-11-05 (Sprint 31 D14 option 1). The first result, `experiments/phase2/results/f157_spectra_algorithms.json`, is kept as recorded; it scored the linear form only.
- **Evidence**: `experiments/phase2/results/f157_spectra_algorithms_rbf.json` (evidence tag SIM, zero metered seconds). Every figure below comes from that file.
- **Seeds**: seed 42 took 3.45 minutes for all seven algorithms, so the entry's rule gave 10 seeds.
- **Data**: SPECTRA `energy_steel`, label `target`, spectra_segment.spectra_split 60/20/20, seeded. Tuning reads the training and validation folds; every score here is on the test fold (7,008 rows, 1,782 positives per seed; 17 feature columns).

## Mean test AUPRC, in order

TP, FP, TN and FN are at the test fold's own 0.5% budget, each the minimum to the maximum over the 10 seeds; each algorithm page gives them per seed.

| Order | Algorithm | Mean | 95% t interval | Recall at the 0.5% budget, mean | TP | FP | TN | FN | Document |
|---|---|---|---|---|---|---|---|---|---|
| 1 | CatBoost | 0.9770 | 0.9676 to 0.9864 | 0.0202 | 36 to 36 | 0 to 0 | 5,226 to 5,226 | 1,746 to 1,746 | [ENERGY_STEEL_CATBOOST.md](ENERGY_STEEL_CATBOOST.md) |
| 2 | XGBoost | 0.9669 | 0.9396 to 0.9943 | 0.0202 | 36 to 36 | 0 to 0 | 5,226 to 5,226 | 1,746 to 1,746 | [ENERGY_STEEL_XGBOOST.md](ENERGY_STEEL_XGBOOST.md) |
| 3 | HGB | 0.9582 | 0.9168 to 0.9995 | 0.0204 | 36 to 40 | 0 to 0 | 5,226 to 5,226 | 1,742 to 1,746 | [ENERGY_STEEL_HGB.md](ENERGY_STEEL_HGB.md) |
| 4 | LightGBM | 0.9570 | 0.9187 to 0.9953 | 0.0202 | 36 to 36 | 0 to 0 | 5,226 to 5,226 | 1,746 to 1,746 | [ENERGY_STEEL_LIGHTGBM.md](ENERGY_STEEL_LIGHTGBM.md) |
| 5 | CVQBoost proxy | 0.9186 | 0.9032 to 0.9340 | 0.0200 | 35 to 36 | 0 to 1 | 5,225 to 5,226 | 1,746 to 1,747 | [ENERGY_STEEL_CVQBOOST_PROXY.md](ENERGY_STEEL_CVQBOOST_PROXY.md) |
| 6 | Logistic regression | 0.6441 | 0.5456 to 0.7427 | 0.1140 | 21 to 1,782 | 3 to 5,226 | 0 to 5,223 | 0 to 1,761 | [ENERGY_STEEL_LOGISTIC_REGRESSION.md](ENERGY_STEEL_LOGISTIC_REGRESSION.md) |
| 7 | SVM | 0.6247 | 0.3963 to 0.8530 | 0.4120 | 34 to 1,782 | 0 to 5,226 | 0 to 5,226 | 0 to 1,748 | [ENERGY_STEEL_SVM.md](ENERGY_STEEL_SVM.md) |

## Adjacent pairs

The entry's test (F166's): with 10 seeds (8 or more), the exact two-sided Wilcoxon signed-rank test on per-seed AUPRC differences is primary, at Bonferroni 0.05 / 6. "A above B" is written only when it rejects. Only adjacent pairs are tested, so a non-adjacent statement is not made here.

- CatBoost against XGBoost: mean difference 0.0101, Wilcoxon p 1.0000; reading: no reliable difference
- XGBoost against HGB: mean difference 0.0088, Wilcoxon p 0.0645; reading: no reliable difference
- HGB against LightGBM: mean difference 0.0012, Wilcoxon p 0.3750; reading: no reliable difference
- LightGBM against CVQBoost proxy: mean difference 0.0384, Wilcoxon p 0.0488; reading: no reliable difference
- CVQBoost proxy against Logistic regression: mean difference 0.2744, Wilcoxon p 0.0020; reading: above
- Logistic regression against SVM: mean difference 0.0195, Wilcoxon p 0.9102; reading: no reliable difference

## In and out of the pocket (secondary)

Test AUPRC inside the pocket (`in_pocket` = 1) and outside it, mean over seeds, as the entry reports it.

| Algorithm | In the pocket | Out of the pocket |
|---|---|---|
| CatBoost | 0.9609 (10 seeds) | 0.9902 (10 seeds) |
| XGBoost | 0.9602 (10 seeds) | 0.9698 (10 seeds) |
| HGB | 0.9555 (10 seeds) | 0.9578 (10 seeds) |
| LightGBM | 0.9549 (10 seeds) | 0.9551 (10 seeds) |
| CVQBoost proxy | 0.9362 (10 seeds) | 0.9031 (10 seeds) |
| Logistic regression | 0.7506 (10 seeds) | 0.4549 (10 seeds) |
| SVM | 0.8364 (10 seeds) | 0.5599 (10 seeds) |

## Notes

- At the test fold's own 0.5% alert budget, mean recall lies between 0.0200 and 0.4120. The budget is set for fraud rates; these datasets' positive rates are far higher, so the budget can catch only a small share of their positives.
- At the test fold's own budget, scores tied at the budget's last place are all flagged, so a lane can flag more rows than the budget: HGB on 1 of 10 seeds, up to 40 rows against a budget of 36; logistic regression on 1 of 10 seeds, up to 7,008 rows against a budget of 36; SVM on 4 of 10 seeds, up to 7,008 rows against a budget of 36. The counts include those rows.
- The entry keeps the RBF form only if its best validation AUPRC beats the linear form's on a majority of seeds. It did so on 6 of 10 seeds, so the entry's rule keeps the **rbf** form. Every SVM figure here, its place in the order and its adjacent pairs are the RBF form's, scored on the test fold under the D14 amendment. The linear form is reported on the SVM page, not ranked. ([ENERGY_STEEL_SVM.md](ENERGY_STEEL_SVM.md))
