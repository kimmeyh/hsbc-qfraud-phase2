# SPECTRA telecom_churn: seven algorithms compared (F157)

**BLUF.** Over 10 seeds (42-51), the order by mean test AUPRC is CatBoost, LightGBM, HGB, XGBoost, SVM, the proxy and logistic regression. Of the six adjacent pairs, 2 differ reliably under the entry's test: SVM above the proxy; CVQBoost proxy above logistic regression. No other adjacent pair differs reliably, so the order among CatBoost, LightGBM, HGB, XGBoost and SVM is not established.

- **Card**: F157 (Sprint 31 Task F, #98), the SPECTRA part: F166's algorithms and grids on SPECTRA's four datasets.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F157 SPECTRA part", written before any score.
- **Amendment**: the SVM lane is the form the entry's rule keeps, scored on the test fold under the entry's amendment of 2026-11-05 (Sprint 31 D14 option 1). The first result, `experiments/phase2/results/f157_spectra_algorithms.json`, is kept as recorded; it scored the linear form only. The amendment was written after that result was seen; the other six lanes are unchanged from it.
- **Evidence**: `experiments/phase2/results/f157_spectra_algorithms_rbf.json` (evidence tag SIM, zero metered seconds). Every figure below comes from that file.
- **Seeds**: seed 42 took 0.91 minutes for all seven algorithms, so the entry's rule gave 10 seeds.
- **Data**: SPECTRA `telecom_churn`, label `target`, spectra_segment.spectra_split 60/20/20, seeded. Tuning reads the training and validation folds; every score here is on the test fold (630 rows, 152 to 153 positives per seed; 17 feature columns).

## Mean test AUPRC, in order

TP, FP, TN and FN are at the test fold's own 0.5% budget, each the minimum to the maximum over the 10 seeds; each algorithm page gives them per seed.

| Order | Algorithm | Mean | 95% t interval | Recall at the 0.5% budget, mean | TP | FP | TN | FN | Document |
|---|---|---|---|---|---|---|---|---|---|
| 1 | CatBoost | 0.8727 | 0.8596 to 0.8857 | 0.0263 | 4 to 4 | 0 to 0 | 477 to 478 | 148 to 149 | [TELECOM_CHURN_CATBOOST.md](TELECOM_CHURN_CATBOOST.md) |
| 2 | LightGBM | 0.8722 | 0.8596 to 0.8848 | 0.0263 | 4 to 4 | 0 to 0 | 477 to 478 | 148 to 149 | [TELECOM_CHURN_LIGHTGBM.md](TELECOM_CHURN_LIGHTGBM.md) |
| 3 | HGB | 0.8697 | 0.8564 to 0.8829 | 0.0263 | 4 to 4 | 0 to 0 | 477 to 478 | 148 to 149 | [TELECOM_CHURN_HGB.md](TELECOM_CHURN_HGB.md) |
| 4 | XGBoost | 0.8610 | 0.8476 to 0.8743 | 0.0263 | 4 to 4 | 0 to 0 | 477 to 478 | 148 to 149 | [TELECOM_CHURN_XGBOOST.md](TELECOM_CHURN_XGBOOST.md) |
| 5 | SVM | 0.8441 | 0.8253 to 0.8630 | 0.0263 | 4 to 4 | 0 to 0 | 477 to 478 | 148 to 149 | [TELECOM_CHURN_SVM.md](TELECOM_CHURN_SVM.md) |
| 6 | CVQBoost proxy | 0.7254 | 0.7042 to 0.7466 | 0.0236 | 3 to 4 | 0 to 1 | 476 to 478 | 148 to 150 | [TELECOM_CHURN_CVQBOOST_PROXY.md](TELECOM_CHURN_CVQBOOST_PROXY.md) |
| 7 | Logistic regression | 0.6509 | 0.6305 to 0.6713 | 0.0210 | 2 to 4 | 0 to 2 | 475 to 478 | 148 to 151 | [TELECOM_CHURN_LOGISTIC_REGRESSION.md](TELECOM_CHURN_LOGISTIC_REGRESSION.md) |

## Adjacent pairs

The entry's test (F166's): with 10 seeds (8 or more), the exact two-sided Wilcoxon signed-rank test on per-seed AUPRC differences is primary, at Bonferroni 0.05 / 6. "A above B" is written only when it rejects. Only adjacent pairs are tested, so a non-adjacent statement is not made here.

- CatBoost against LightGBM: mean difference 0.0004, Wilcoxon p 0.7695; reading: no reliable difference
- LightGBM against HGB: mean difference 0.0025, Wilcoxon p 0.3750; reading: no reliable difference
- HGB against XGBoost: mean difference 0.0087, Wilcoxon p 0.0195; reading: no reliable difference
- XGBoost against SVM: mean difference 0.0168, Wilcoxon p 0.0371; reading: no reliable difference
- SVM against CVQBoost proxy: mean difference 0.1187, Wilcoxon p 0.0020; reading: above
- CVQBoost proxy against Logistic regression: mean difference 0.0745, Wilcoxon p 0.0020; reading: above

## In and out of the pocket (secondary)

Test AUPRC inside the pocket (`in_pocket` = 1) and outside it, mean over seeds, as the entry reports it.

| Algorithm | In the pocket | Out of the pocket |
|---|---|---|
| CatBoost | 0.7664 (10 seeds) | 0.9151 (10 seeds) |
| LightGBM | 0.7788 (10 seeds) | 0.9127 (10 seeds) |
| HGB | 0.7769 (10 seeds) | 0.9108 (10 seeds) |
| XGBoost | 0.7689 (10 seeds) | 0.9013 (10 seeds) |
| SVM | 0.6796 (10 seeds) | 0.9161 (10 seeds) |
| CVQBoost proxy | 0.7943 (10 seeds) | 0.6928 (10 seeds) |
| Logistic regression | 0.5552 (10 seeds) | 0.7068 (10 seeds) |

## Notes

- At the test fold's own 0.5% alert budget, mean recall lies between 0.0210 and 0.0263. The budget is set for fraud rates; these datasets' positive rates are far higher, so the budget can catch only a small share of their positives.
- The entry keeps the RBF form only if its best validation AUPRC beats the linear form's on a majority of seeds. It did so on 10 of 10 seeds, so the entry's rule keeps the **rbf** form. Every SVM figure here, its place in the order and its adjacent pairs are the RBF form's, scored on the test fold under the D14 amendment. The linear form is reported on the SVM page, not ranked. ([TELECOM_CHURN_SVM.md](TELECOM_CHURN_SVM.md))
