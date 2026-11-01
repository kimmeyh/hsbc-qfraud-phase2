# IEEE-CIS: seven algorithms compared (F174)

**BLUF.** Over 10 seeds (42-51), the order by mean test AUPRC is LightGBM, HGB, CatBoost, XGBoost, the proxy, SVM and logistic regression. Of the six adjacent pairs, 4 differ reliably under the entry's test: LightGBM above HGB; CatBoost above XGBoost; CVQBoost proxy above SVM; SVM above logistic regression. Of these, CatBoost above XGBoost; CVQBoost proxy above SVM; SVM above logistic regression rest on a lane whose test AUPRC is the same on every seed, so the seeds are not independent evidence there (see the adjacent pairs). No other adjacent pair differs reliably, so the order among HGB and CatBoost; XGBoost and the proxy is not established.

- **Card**: F174 (Sprint 30 Task D, #78), the IEEE-CIS part of F157.
- **Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F174", written before any score.
- **Evidence**: `experiments/phase2/results/f174_ieee_algorithms.json` (evidence tag SIM, zero metered seconds). Every figure below comes from that file.
- **Seeds**: 10, as Sprint 30 Decision D5 set, with no time cap. Seed 42 took 65.42 minutes for all seven algorithms.
- **ULB**: the same algorithms and grids on ULB are on [ULB_COMPARISON.md](ULB_COMPARISON.md).

## Mean test AUPRC, in order

TP, FP, TN and FN are at the test month's own 0.5% budget, each the minimum to the maximum over the 10 seeds; each algorithm page gives them per seed.

| Order | Algorithm | Mean | 95% t interval | Recall at the 0.5% budget, mean | TP | FP | TN | FN | Document |
|---|---|---|---|---|---|---|---|---|---|
| 1 | LightGBM | 0.5785 | 0.5706 to 0.5864 | 0.1389 | 400 to 416 | 11 to 27 | 82,313 to 82,329 | 2,546 to 2,562 | [IEEE_LIGHTGBM.md](IEEE_LIGHTGBM.md) |
| 2 | HGB | 0.5211 | 0.5171 to 0.5250 | 0.1357 | 393 to 411 | 16 to 34 | 82,306 to 82,324 | 2,551 to 2,569 | [IEEE_HGB.md](IEEE_HGB.md) |
| 3 | CatBoost | 0.5114 | 0.5069 to 0.5158 | 0.1388 | 405 to 415 | 12 to 22 | 82,318 to 82,328 | 2,547 to 2,557 | [IEEE_CATBOOST.md](IEEE_CATBOOST.md) |
| 4 | XGBoost | 0.4960 | 0.4960 to 0.4960 | 0.1364 | 404 to 404 | 23 to 23 | 82,317 to 82,317 | 2,558 to 2,558 | [IEEE_XGBOOST.md](IEEE_XGBOOST.md) |
| 5 | CVQBoost proxy | 0.4862 | 0.4751 to 0.4973 | 0.1377 | 400 to 417 | 23 to 30 | 82,310 to 82,317 | 2,545 to 2,562 | [IEEE_CVQBOOST_PROXY.md](IEEE_CVQBOOST_PROXY.md) |
| 6 | SVM | 0.3612 | 0.3612 to 0.3612 | 0.1256 | 372 to 372 | 55 to 55 | 82,285 to 82,285 | 2,590 to 2,590 | [IEEE_SVM.md](IEEE_SVM.md) |
| 7 | Logistic regression | 0.3564 | 0.3564 to 0.3564 | 0.1215 | 360 to 360 | 67 to 67 | 82,273 to 82,273 | 2,602 to 2,602 | [IEEE_LOGISTIC_REGRESSION.md](IEEE_LOGISTIC_REGRESSION.md) |

## Adjacent pairs

The entry's test: with 10 seeds (8 or more), the exact two-sided Wilcoxon signed-rank test on per-seed AUPRC differences is primary, at Bonferroni 0.05 / 6. "A above B" is written only when it rejects. Only adjacent pairs are tested, so a non-adjacent statement is not made here.

- LightGBM against HGB: mean difference 0.0574, Wilcoxon p 0.0020; reading: above
- HGB against CatBoost: mean difference 0.0097, Wilcoxon p 0.0137; reading: no reliable difference
- CatBoost against XGBoost: mean difference 0.0154, Wilcoxon p 0.0020; reading: above
- XGBoost against CVQBoost proxy: mean difference 0.0097, Wilcoxon p 0.1309; reading: no reliable difference
- CVQBoost proxy against SVM: mean difference 0.1250, Wilcoxon p 0.0020; reading: above
- SVM against Logistic regression: mean difference 0.0048, Wilcoxon p 0.0020; reading: above

Pairs with a lane whose test AUPRC is the same on every seed (the month folds are fixed, so a deterministic lane at one configuration gives one result):

- CatBoost against XGBoost: XGBoost is the same on every seed, so the test compares CatBoost's seeds with one fixed value.
- XGBoost against the proxy: XGBoost is the same on every seed, so the test compares the proxy's seeds with one fixed value.
- CVQBoost proxy against SVM: SVM is the same on every seed, so the test compares the proxy's seeds with one fixed value.
- SVM against logistic regression: both lanes are the same on every seed, so the 10 differences are one difference repeated. The p value comes from the repeats; the evidence is one test month.

## Notes

- At the test month's own 0.5% alert budget (427 rows), mean recall lies between 0.1215 and 0.1389. The month's fraud rate is 3.47%, so the budget can catch at most 427 of its 2,962 frauds (F171).
- The 0.5% thresholds chosen on the validation month flag 256 to 1,035 test rows across algorithms and seeds, so the per-page tables at that threshold compare different alert volumes. The recall column above uses the test month's own budget.
- At the test month's own budget, scores tied at the budget's last place are all flagged, so a lane can flag more rows than the budget: HGB on 1 of 10 seeds, up to 428 rows against a budget of 427; the proxy on 8 of 10 seeds, up to 442 rows against a budget of 427. The counts include those rows.
- F152's adversarial drift control: on the tuning fold it stopped at its cap of 20 rounds, with a final adversarial AUC of 0.9906; on the scored fold it stopped at its cap of 20 rounds, with a final adversarial AUC of 0.9450. An AUC near 1 means a classifier still tells the training months from the scored month. The tuning fold keeps 171 features and the scored fold 181.
- The SVM lane keeps its linear form; the RBF alternative beat it on validation on 0 of 10 seeds ([IEEE_SVM.md](IEEE_SVM.md)).
