# IEEE-CIS: seven algorithms compared (F174)

**BLUF.** Over 10 seeds (42-51), the order by mean test AUPRC is LightGBM, HGB, CatBoost, XGBoost, the proxy, SVM and logistic regression. Of the six adjacent pairs, 4 differ reliably under the entry's test: LightGBM above HGB; CatBoost above XGBoost; CVQBoost proxy above SVM; SVM above logistic regression. No other adjacent pair differs reliably, so the order among HGB and CatBoost; XGBoost and the proxy is not established.

- **Card**: F174 (Sprint 30 Task D, #78), the IEEE-CIS part of F157.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F174", written before any score.
- **Evidence**: `experiments/phase2/results/f174_ieee_algorithms.json` (evidence tag SIM, zero metered seconds). Every figure below comes from that file.
- **Seeds**: 10, as Sprint 30 Decision D5 set, with no time cap. Seed 42 took 65.42 minutes for all seven algorithms.
- **ULB**: the same algorithms and grids on ULB are on [ULB_COMPARISON.md](ULB_COMPARISON.md).

## Mean test AUPRC, in order

| Order | Algorithm | Mean | 95% t interval | Recall at the 0.5% budget, mean | Document |
|---|---|---|---|---|---|
| 1 | LightGBM | 0.5785 | 0.5706 to 0.5864 | 0.1389 | [IEEE_LIGHTGBM.md](IEEE_LIGHTGBM.md) |
| 2 | HGB | 0.5211 | 0.5171 to 0.5250 | 0.1357 | [IEEE_HGB.md](IEEE_HGB.md) |
| 3 | CatBoost | 0.5114 | 0.5069 to 0.5158 | 0.1388 | [IEEE_CATBOOST.md](IEEE_CATBOOST.md) |
| 4 | XGBoost | 0.4960 | 0.4960 to 0.4960 | 0.1364 | [IEEE_XGBOOST.md](IEEE_XGBOOST.md) |
| 5 | CVQBoost proxy | 0.4862 | 0.4751 to 0.4973 | 0.1377 | [IEEE_CVQBOOST_PROXY.md](IEEE_CVQBOOST_PROXY.md) |
| 6 | SVM | 0.3612 | 0.3612 to 0.3612 | 0.1256 | [IEEE_SVM.md](IEEE_SVM.md) |
| 7 | Logistic regression | 0.3564 | 0.3564 to 0.3564 | 0.1215 | [IEEE_LOGISTIC_REGRESSION.md](IEEE_LOGISTIC_REGRESSION.md) |

## Adjacent pairs

The entry's test: with 10 seeds (8 or more), the exact two-sided Wilcoxon signed-rank test on per-seed AUPRC differences is primary, at Bonferroni 0.05 / 6. "A above B" is written only when it rejects. Only adjacent pairs are tested, so a non-adjacent statement is not made here.

- LightGBM against HGB: mean difference 0.0574, Wilcoxon p 0.0020; reading: above
- HGB against CatBoost: mean difference 0.0097, Wilcoxon p 0.0137; reading: no reliable difference
- CatBoost against XGBoost: mean difference 0.0154, Wilcoxon p 0.0020; reading: above
- XGBoost against CVQBoost proxy: mean difference 0.0097, Wilcoxon p 0.1309; reading: no reliable difference
- CVQBoost proxy against SVM: mean difference 0.1250, Wilcoxon p 0.0020; reading: above
- SVM against Logistic regression: mean difference 0.0048, Wilcoxon p 0.0020; reading: above

## Notes

- At the 0.5% alert budget, mean recall on the test month lies between 0.1215 and 0.1389. The month's fraud rate is 3.47%, so a 0.5% budget cannot flag most frauds (F171).
- The SVM lane keeps its linear form; the RBF alternative beat it on validation on 0 of 10 seeds ([IEEE_SVM.md](IEEE_SVM.md)).
