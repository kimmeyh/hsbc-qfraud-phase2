# ULB: seven algorithms compared (F166)

**BLUF.** Over 10 seeds (42-51), the four gradient-boosting libraries lead by mean test AUPRC, the CVQBoost proxy is next, then the linear SVM and logistic regression. Of the six adjacent pairs, 2 differ reliably under the entry's test: CVQBoost proxy above SVM; SVM above logistic regression. No other adjacent pair differs reliably, so the order among CatBoost, LightGBM, XGBoost, HGB and the proxy is not established.

- **Card**: F166 (Sprint 29 Task F, #69), the ULB part of F157.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F166", written before any score.
- **Evidence**: `experiments/phase2/results/f166_ulb_algorithms.json` (evidence tag SIM, zero metered seconds). Every figure below comes from that file.
- **Seeds**: seed 42 took 11.48 minutes for all seven algorithms, so the entry's rule gave 10 seeds.

## Mean test AUPRC, in order

TP, FP, TN and FN are at the test fold's own 0.5% budget, each the minimum to the maximum over the 10 seeds; each algorithm page gives them per seed.

| Order | Algorithm | Mean | 95% t interval | Recall at the 0.5% budget, mean | TP | FP | TN | FN | Document |
|---|---|---|---|---|---|---|---|---|---|
| 1 | CatBoost | 0.8329 | 0.8131 to 0.8527 | 0.8579 | 77 to 86 | 198 to 207 | 56,444 to 56,453 | 9 to 18 | [ULB_CATBOOST.md](ULB_CATBOOST.md) |
| 2 | LightGBM | 0.8270 | 0.8104 to 0.8436 | 0.8568 | 78 to 86 | 198 to 206 | 56,445 to 56,453 | 9 to 17 | [ULB_LIGHTGBM.md](ULB_LIGHTGBM.md) |
| 3 | XGBoost | 0.8229 | 0.7976 to 0.8482 | 0.8589 | 76 to 86 | 198 to 208 | 56,443 to 56,453 | 9 to 19 | [ULB_XGBOOST.md](ULB_XGBOOST.md) |
| 4 | HGB | 0.8124 | 0.7940 to 0.8307 | 0.8558 | 78 to 86 | 198 to 206 | 56,445 to 56,453 | 9 to 17 | [ULB_HGB.md](ULB_HGB.md) |
| 5 | CVQBoost proxy | 0.7925 | 0.7705 to 0.8146 | 0.8305 | 76 to 85 | 199 to 220 | 56,431 to 56,452 | 10 to 19 | [ULB_CVQBOOST_PROXY.md](ULB_CVQBOOST_PROXY.md) |
| 6 | SVM | 0.7419 | 0.7208 to 0.7630 | 0.8474 | 77 to 87 | 197 to 207 | 56,444 to 56,454 | 8 to 18 | [ULB_SVM.md](ULB_SVM.md) |
| 7 | Logistic regression | 0.7270 | 0.7050 to 0.7490 | 0.8421 | 77 to 86 | 198 to 207 | 56,444 to 56,453 | 9 to 18 | [ULB_LOGISTIC_REGRESSION.md](ULB_LOGISTIC_REGRESSION.md) |

## Adjacent pairs

The entry's test: with 10 seeds (8 or more), the exact two-sided Wilcoxon signed-rank test on per-seed AUPRC differences is primary, at Bonferroni 0.05 / 6. "A above B" is written only when it rejects. Only adjacent pairs are tested, so a non-adjacent statement (for example CatBoost against the proxy) is not made here.

- CatBoost against LightGBM: mean difference 0.0059, Wilcoxon p 0.0840; reading: no reliable difference
- LightGBM against XGBoost: mean difference 0.0041, Wilcoxon p 1.0000; reading: no reliable difference
- XGBoost against HGB: mean difference 0.0105, Wilcoxon p 0.0488; reading: no reliable difference
- HGB against CVQBoost proxy: mean difference 0.0198, Wilcoxon p 0.0098; reading: no reliable difference
- CVQBoost proxy against SVM: mean difference 0.0507, Wilcoxon p 0.0039; reading: above
- SVM against Logistic regression: mean difference 0.0149, Wilcoxon p 0.0039; reading: above

## Notes

- The proxy's train-test AUPRC gap has the largest mean (0.2075); the SVM's and logistic regression's are the smallest (0.0190 and 0.0291).
- HGB against the proxy has the smallest p among the pairs read "no reliable difference", but it is above the Bonferroni level of 0.05 / 6, so the entry does not write "above".
- At the 0.5% alert budget, mean recall on the test fold lies between 0.8305 and 0.8589 for all seven, a narrower spread than AUPRC's.
- At the test fold's own budget, scores tied at the budget's last place are all flagged, so a lane can flag more rows than the budget: the proxy on 7 of 10 seeds, up to 297 rows against a budget of 284. The counts include those rows.
- The SVM lane keeps its linear form; the RBF alternative beat it on validation on 2 of 10 seeds ([ULB_SVM.md](ULB_SVM.md)).
