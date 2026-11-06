# What We Have Learned About Quantum Advantage for Fraud Detection: Machine Learning Expert Version

**Version 1.1**, 2026-11-05 (Sprint 31, card F178). For readers with
undergraduate-or-above or professional machine learning and data-science
experience. Acronyms and common terms link to the
[plain-terms version](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md),
which owns them; the appendix here holds only what that version lacks.
The [quantum computing expert version](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20QC%20Expert.md)
covers the devices in more depth.

## Change list

- **1.1, 2026-11-05 (Sprint 31)**: Sprint 31's results added. Each is a tagged claim under its topic's "What our experiments showed" and a dated result under "Experiments planned": F114, F155, F157 (both parts), Experiment 5 and F95. No Sprint 32 run is preregistered yet, so none is listed.
- **1.0, 2026-11-05 (Sprint 31)**: first version. Phase 1 and Phase 2
  through Sprint 30. Sprint 31's runs have placeholders in "Experiments
  planned".

## Bottom line

- **Tuned [gradient boosting](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ml-gradient-boosting) is the bar, and nothing quantum cleared it.**
  On [ULB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ulb) the four boosting libraries lead and their order is not
  established; on [IEEE-CIS](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ieee-cis), split by month, LightGBM is reliably first.
  The [CVQBoost](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qml-cvqboost) proxy sits below the boosting libraries and above the
  linear models on both.
- **The Phase 1 device null is a formulation result, not a solver
  result.** The continuous CVQBoost objective is convex; the device
  reproduced the exact solve, so the solver could not add anything. The
  one gain at scale came from the weak-learner pool, and an exact
  classical solve of the same pool reproduces it.
- **Comparator hygiene decided more readings than any model did.** An
  unregularized [HGB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-hgb) default made one [quantum-inspired](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qc-quantum-inspired) lane look better
  than it was; [deterministic lanes](#ml2-deterministic-lane) on fixed month folds make paired
  seed tests look stronger than they are; a 0.5% budget on a 3.47% fraud
  rate measures capacity, not models.
- **The frauds models miss look legitimate in the given [features](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ml-feature).**
  Every model family misses the same frauds, and their nearest
  neighbors are legitimate. More model variety will not catch them; new
  fields might.
- **Outside literature agrees**: no stored result shows a quantum model
  beating a tuned classical model on tabular, imbalanced data, and the
  positive quantum fraud results run on tiny or rebalanced subsets
  against untuned comparators.

## How to read this version

- The evidence tiers, tags and claim rule are those of the plain-terms
  version: our results first, under "What our experiments showed", each
  bullet ending with its tracked source path; outside results second,
  with their EvidenceBasedDB grade. `experiments/src/test_learning_docs.py`
  checks every link, acronym, path and decimal figure.
- Unless stated otherwise: [AUPRC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auprc) is step-wise average [precision](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ml-precision) on the
  [test fold](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ml-test-fold); "reliable" means the entry's preset test rejects at its
  Bonferroni level; seeds are 42 to 51 (10) or 42 to 46 (5).

## 1. Evaluation protocol

- **Splits**: [ULB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ulb) is deduplicated (1,081 exact duplicates removed) and
  split 60/20/20 stratified, one split per seed. [IEEE-CIS](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ieee-cis) uses
  rolling-origin month folds: train on all earlier months, choose
  settings on the last training month, test on the next. On [IEEE-CIS](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ieee-cis) the
  split is fixed, so the seed moves only the model
  (`docs/paper/proposal.md`; `experiments/phase2/PREREGISTRATION_DRAFT.md`).
- **Metrics**: test [AUPRC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auprc) (never trapezoidal), [recall](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ml-recall) at a 0.5% alert
  budget with ties at the cut all flagged, [floor normalization](#ml2-floor-normalization) where fraud
  rates differ, and [TP](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-tp), [FP](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-fp), [TN](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-tn) and [FN](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-fn) at that
  budget for every scored result (the outcome rule in `CLAUDE.md`).
- **Inference**: per-seed paired differences, an exact Wilcoxon
  signed-rank test with 8 or more seeds, a [Bonferroni correction](#ml2-bonferroni-correction) within
  each experiment's family, and equivalence against a preset margin where the
  question is "no worse". Every entry is written before its first score
  (`experiments/phase2/PREREGISTRATION_DRAFT.md`, sections 2, 2a and 2b).
- **Caveat stated in Phase 1**: seed intervals measure split dispersion,
  not sampling error, because the resplits share rows
  (`docs/paper/proposal.md`, section 2).

## 2. Credit card fraud as a learning problem

### What it is and what a bank needs

- The scope is [CNP](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-cnp) fraud as binary classification in batch evaluation
  (`docs/requirements-matrix.md`, D16).
- The decision runs under a fixed review budget and asymmetric cost; the
  filed proposal names the missing features (merchant, device, account
  age), [label](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ml-label) latency (chargebacks arrive weeks late, so recent rows are
  censored), unmeasured scoring latency, uncalibrated scores and absent
  fairness testing as the gaps between a benchmark and a trial
  (`docs/paper/proposal.md`, sections 1 and 3).
- Explainability was the team's stated deployment bar in Phase 1: a
  weighted vote over small inspectable learners is easier to explain
  than a large boosted model (`docs/RESULTS_MEMO.md`, decision item 4).
  That is a stated position, not a measured result.

### What our experiments showed

- [SIM] [ULB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ulb) missed-by-all frauds sit among legitimate rows: 36 frauds
  missed by all 12 on-split families in every seed against 370 caught in
  every seed; median legitimate share of the 10 nearest training rows 1.0
  against 0.1; 16.2% of caught frauds have mostly legitimate neighbors;
  Mann-Whitney U rejects (p below 1e-20). The simulator check fired first,
  so the comparison can detect a known information limit
  (`docs/phase2/F170_MISSED_NEIGHBORS.md`).
- [SIM] On [IEEE-CIS](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ieee-cis) the missed-by-all share at 0.5% is 81.5% against
  [ULB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ulb)'s 11.2%, but 4 [IEEE-CIS](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ieee-cis) families are compared with 12 [ULB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ulb)
  families, and at 0.5% the [capacity floor](#ml2-capacity-floor) alone is 42.3%. At three times
  each fold's fraud rate the shares are 18.2% and 11.2%. Not shown as a
  feature-richness effect (`docs/phase2/F171_MISSED_IEEE.md`).
- [SIM] Profile of [IEEE-CIS](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ieee-cis) missed rows at 0.5%: ProductCD W 53.0% of
  missed against 7.5% of caught; DeviceType missing 55.4% against 8.5%.
  The groups overlap across seeds, so this is descriptive only
  (`docs/phase2/F171_MISSED_IEEE.md`).
- [SIM] On F108's simulator, a per-type cascade (one detector per fraud
  type, max of the two probabilities) recalled less within 0.5% than one
  model: mean -0.079, 95% interval -0.126 to -0.013, over 8 seeds
  (`experiments/phase2/results/f158_fraud_types.json`).
- [SIM] The real-data step of that test did not run, because its
  condition was a cascade above one model
  (`docs/sprints/SPRINT_29_VALIDATION.md`).
- [SIM] On the simulator the Bayes classifier's [AUPRC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auprc) is 0.296 to 0.318:
  scenario 2 (a compromised terminal) is invisible in the observed
  features (`docs/phase2/F108_CEILING_VALIDATION.md`).
- [SIM] Temporal validity on [IEEE-CIS](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ieee-cis) (floor-normalized [AUPRC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auprc), 5 seeds):
  XGBoost beats [logistic regression](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ml-logistic-regression) on month 4 by +0.106 [+0.089,
  +0.123] and on month 5 by +0.359; logistic regression falls from 0.337
  to 0.122 while every tree lane holds; XGBoost's month 4 to 5 change,
  +0.038, mixes [drift](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ml-drift) with one more month of training rows. The
  adversarial control stopped at its cap with early against late [AUC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auc)
  still 0.94 and 0.89 (`docs/phase2/F152_EXP2_RESULT.md`).
- [SIM] Card-holder aggregation helps every [IEEE-CIS](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ieee-cis) lane: [HGB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-hgb) [AUROC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auroc) rose
  from 0.758 to 0.816 after it (`docs/phase2/F109_TIER1_LADDER.md`).

### What outside research says

- The best published [IEEE-CIS](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ieee-cis) test scores in one study ([AUPRC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auprc) 0.6699)
  come from a stratified random split, not a temporal one
  (EvidenceBasedDB `han-ieee-cis-best-test-scores-random-split`, low).
- [SMOTE](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-smote) before the split produced near-perfect XGBoost scores, which the
  authors attribute to leakage (EvidenceBasedDB
  `kabane-presplit-inflation`, low).
- With a fixed threshold of 0.5, balancing helped every classifier; with
  an optimized threshold it helped only weak ones, and [SMOTE](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-smote)-like methods
  were not better than random oversampling (EvidenceBasedDB
  `elor-fixed-threshold-balancing-helps-all`, low).
- With a fixed investigation cost, the cost-optimal rule flags a row when
  its score exceeds that cost over the amount (EvidenceBasedDB
  `hoppner-instance-threshold`, high).
- A fraud evaluation set undersampled to about 43% fraud does not carry
  over to real rates (EvidenceBasedDB
  `fraudtransformer-evaluation-set-undersampled`, high).
- The dataset authors' handbook asks for temporal splits with a label
  delay and step-wise average precision
  ([handbook, validation strategies](https://fraud-detection-handbook.github.io/fraud-detection-handbook/Chapter_5_ModelValidationAndSelection/ValidationStrategies.html)).

## 3. Classical machine learning results

### What our experiments showed

- [SIM] [ULB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ulb), 10 seeds, F166's grids: CatBoost 0.8329 (95% t interval
  0.8131 to 0.8527), LightGBM 0.8270, XGBoost 0.8229, [HGB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-hgb) 0.8124,
  CVQBoost proxy 0.7925, linear [SVM](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-svm) 0.7419, logistic regression 0.7270.
  Of six adjacent pairs, two reject at Bonferroni 0.05 / 6 (exact
  Wilcoxon p 0.0039 each): proxy above [SVM](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-svm), [SVM](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-svm) above logistic
  regression (`docs/phase2/algorithms/ULB_COMPARISON.md`).
- [SIM] [ULB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ulb) recall at 0.5% spans only 0.8305 to 0.8589 across the seven;
  the proxy's train-test [AUPRC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auprc) gap is the largest (0.2075), and its tied
  scores flag up to 297 rows against a budget of 284
  (`docs/phase2/algorithms/ULB_COMPARISON.md`).
- [SIM] [IEEE-CIS](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ieee-cis), 10 seeds, month-4 test: LightGBM 0.5785, [HGB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-hgb) 0.5211,
  CatBoost 0.5114, XGBoost 0.4960, proxy 0.4862, [SVM](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-svm) 0.3612, logistic
  regression 0.3564. LightGBM above [HGB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-hgb) is the one reliable pair with two
  stochastic lanes; XGBoost, [SVM](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-svm) and logistic regression are deterministic
  lanes, the same on every seed, so three other "reliable" pairs compare seeds
  with one fixed value (`docs/phase2/algorithms/IEEE_COMPARISON.md`).
- [SIM] [IEEE-CIS](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ieee-cis) recall at the test month's 0.5% budget is 0.1215 to
  0.1389: 427 alerts for 2,962 frauds (`docs/phase2/algorithms/IEEE_COMPARISON.md`).
- [SIM] The adversarial drift control stopped at 20 rounds with [AUC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auc)
  0.9906 on the tuning fold and 0.9450 on the scored fold, so the months
  stay distinguishable after it (`docs/phase2/algorithms/IEEE_COMPARISON.md`).
- [SIM] [HGB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-hgb)'s default `l2_regularization=0` is unstable at 0.17%
  prevalence: mean [AUPRC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auprc) 0.375, [SD](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-sd) 0.170; 1.0 alone gives 0.804, [SD](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-sd)
  0.022. The default's early stopping halted at 10 or 11 iterations;
  with the L2 term it ran 35-89. F130's "proxy beats [HGB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-hgb)" came from that
  comparator (`docs/phase2/F151_HGB_COMPARATOR.md`).
- [SIM] In 132 primary tests (66 model pairs, 2 subsets) on the stored
  [ULB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ulb) predictions, no interaction interval excludes zero; in every pair
  both models flag at least 776 of 950 test frauds
  (`docs/phase2/F154_WHERE_MODELS_WIN.md`).
- [SIM] An oracle choosing per row between the best proxy and the best
  XGBoost recalls 5.0 points more than XGBoost at 0.5%; the same oracle
  between two XGBoost configurations gives 3.6. Of the gap, frauds
  contribute 0.1 points and legitimate rows 4.4; label-free combinations
  (83.7% and 85.3%) are below XGBoost alone (85.6%)
  (`docs/phase2/F113_ORACLE_GAP.md`).
- [SIM] Protocol replication of the published CVQBoost-[KNN](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-knn) 0.8108: our
  lane's mean is 0.760 under the source protocol; the protocol does not
  measurably change it (A minus B -0.014, 95% interval [-0.046,
  +0.019]); stable [HGB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-hgb) beats it by 0.082 and 0.033
  (`docs/phase2/F111_LOKE_PROTOCOL.md`).
- [SIM] In Phase 1, fit-time class weighting on matched 6-feature pools
  gave +0.0319 on 10 of 10 seeds, and the optimizer's own contribution
  was +0.0047, below the [MDE](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-mde) of 0.0268 (`docs/paper/proposal.md`).
- [SIM] At a 0.1% review budget in Phase 1, CatBoost caught 59.3% of
  fraud against CVQBoost's 56.5% (`docs/paper/proposal.md`).
- [SIM] [IEEE-CIS](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ieee-cis) rolling-origin [AUROC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auroc) for LightGBM was 0.9139 in Phase 1;
  the challenge statement's 0.9459 is a leaderboard figure
  (`docs/paper/proposal.md`).
- [SIM] [SPECTRA](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-spectra), 10 seeds per dataset: boosted trees first by mean
  test [AUPRC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auprc) on all four datasets, the proxy fifth or sixth of
  seven. The [RBF](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-rbf) [SVM](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-svm) is reliably above the proxy on
  oilgas_gasturbine (0.8532 against 0.8394) and telecom_churn (0.8441
  against 0.7254); exact Wilcoxon on adjacent pairs, Bonferroni 0.05 / 6
  (`experiments/phase2/results/f157_spectra_algorithms_rbf.json`).

### What outside research says

- On nine tabular datasets, classical kernel [SVM](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-svm)s beat the best quantum
  kernel [SVM](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-svm) on 8 of 9; with 16 paired seeds classical kernels were
  significantly better on 6 of 7 (EvidenceBasedDB
  `qksvm-classical-kernels-better-on-uci-tabular`, low).
- Under training-fold rebalancing, CVQBoost's [AUC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auc) on [ULB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ulb) is below
  XGBoost's in every row but one (one oversampling method at ratio 1.0) in QCi's own fraud
  paper (EvidenceBasedDB `cvqboost-vs-xgboost-auc-under-balancing`, low).
- The same paper says the weighted features could explain decisions but
  did not examine it (EvidenceBasedDB `emami-explainability-not-examined`,
  high).

## 4. Ceilings: how much is left to find

### What our experiments showed

- [SIM] On F108's simulator (known [Bayes error](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ml-bayes-error) 0.0060-0.0063), the
  default [HGB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-hgb) plug-in overstated the Bayes error by 5-12% and recovered
  on 2 of 5 seeds; no method was validated
  (`docs/phase2/F108_CEILING_VALIDATION.md`).
- [SIM] [Isotonic calibration](#ml2-isotonic-calibration) did not move the main-arm estimate: the
  calibrated and uncalibrated plug-ins differ by less than 0.0002 on every
  seed (`docs/phase2/F114_CALIBRATED_PLUGIN.md`).
- [SIM] LightGBM with 4,095 bins and no early stopping recovers on 5 of 5
  seeds on the main arm (seed 42: 0.00609 against 0.0061); [HGB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-hgb) without
  early stopping on 4 of 5. Recovering the Bayes error is not ranking like
  the Bayes classifier: LightGBM's test [AUPRC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auprc) is 0.282 to 0.300 against a
  Bayes [AUPRC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auprc) of 0.296 to 0.318 (`docs/phase2/F169_PLUGIN_BINS.md`).
- [SIM] F169's plug-in, re-run at a lower learning rate, on [IEEE-CIS](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ieee-cis) month 4:
  0.0254 (0.0232 to 0.0276) against an achieved error of 0.0293, with a
  calibration warning; the shuffled-label check passed. [ULB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ulb): 0.00016,
  not a usable ceiling
  (`experiments/phase2/results/f114_real_ceiling_lr05.json`).

## 5. The quantum-inspired lane as a model

### What our experiments showed

- [HW] Phase 1 confirmatory endpoint: CVQBoost on [Dirac-3](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qc-dirac-3) 0.7671 minus
  matched-13 CatBoost 0.8070 is -0.0399 (interval -0.0571 to -0.0227), 9 of 10
  seeds negative (`docs/paper/proposal.md`).
- [HW] Device minus exact solve of the same objective: -0.0010 [AUPRC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auprc),
  weight cosine 0.975 to 0.999 (`docs/paper/proposal.md`).
- [HW] The 833-variable order-3 arm gained +0.0256 over the matched
  91-variable arm on 10 of 10 seeds (absolute 0.7928); feature count and
  order moved together, so it is confounded
  (`docs/paper/proposal.md`).
- [HW, SIM] An exact solve of a rebuilt pool of that arm differs from the
  device by +0.0002 (Wilcoxon p = 0.92; t-interval -0.0013 to +0.0018),
  so the device accounts for at most a small part of the gain; the step
  comes from schedule 3's three-feature learners
  (`docs/phase2/F144_PROXY_TWIN.md`).
- [SIM] F112 removes the confound on the [ULB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ulb) proxy, 10 seeds. P1 holds:
  order 2 to 3 at k=13 adds +0.0245 [AUPRC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auprc), 97.5% interval [+0.0184,
  +0.0304], exact Wilcoxon p = 0.00195. P2 holds: k 13 to 17 at order 2
  adds +0.0001, 97.5% interval [-0.0034, +0.0037], equivalent to zero
  within 0.005 (`experiments/phase2/PREREGISTRATION_DRAFT.md`,
  `docs/sprints/SPRINT_27_SUMMARY.md`).
- [SIM] On [SPECTRA](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-spectra) cells, [HGB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-hgb) and [GA2M](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ga2m) beat the proxy on 5 of 5 seeds
  each on all three cells (`docs/F100_CLASSICAL_BAR.md`).
- [SIM] Laplace-smoothed soft votes help on 15 of 15 cells (+0.074 on
  energy_steel) and bring the proxy to parity with [HGB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-hgb) there only
  (+0.011); multi-sample ensembling adds +0.0014
  (`docs/phase2/F20_SOFT_VOTES_RESULT.md`).
- [SIM] `min_samples_leaf=20` lifts the proxy on energy_steel from 0.902
  to 0.973, level with [HGB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-hgb)'s 0.965; the later sweep found no leaf value
  that beats [HGB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-hgb) with an interval excluding zero on any dataset
  (`docs/phase2/SPECTRA_IMPROVEMENT_RESEARCH.md`).
- [SIM] Inside [SPECTRA](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-spectra)'s pocket, over 10 seeds, XGBoost beats the proxy
  on energy_steel by 0.024 and on oilgas_gasturbine by 0.011; telecom's
  proxy lead over [HGB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-hgb) (+0.013, p = 0.16) is not reliable
  (`docs/phase2/F162_IN_POCKET.md`).
- [SIM] The pocket indicator is predictable from the phase features at
  [AUROC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auroc) 0.93-0.99, so a router keyed on it is not independent of the
  specialist (`docs/F101_IN_POCKET_PROVENANCE.md`).
- [SIM] The pool build grows faster than linearly in rows: log-log
  slope 1.40 [1.35, 1.45] at 91 variables and 1.44 [1.38, 1.49] at 833;
  the solve is flat in rows (`docs/phase2/F110_SCALING.md`).
- [SIM] Experiment 5: no ProductCD segment accepted for the proxy or for
  [HGB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-hgb); on C, R, H and S recall at the budget saturates, so the edge is
  0 or below by construction (`docs/phase2/EXP5_ROUTER.md`).

## 6. Quantum machine learning

### What we know for sure

- A quantum learner gains only where its function class fits the data
  better than a classical model of the same order and size, or where it
  is cheaper at equal quality. Our tests compare each quantum lane with
  its [classical twins](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qml-classical-twin) on identical features and splits.

### What our experiments showed

- [SIM] An 8-qubit sandwich-encoded circuit on [ULB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ulb) phase features, 8
  seeds: circuit 0.699, [HGB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-hgb) 0.719, [GA2M](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ga2m) 0.705, [GAM](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-gam) 0.704, [RFF](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-rff) 0.673,
  logistic regression 0.662, joint twin 0.625. [HGB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-hgb) minus circuit +0.0203
  [-0.0110, +0.0487], p = 0.195; [RFF](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-rff), logistic regression and the joint
  twin are below it. Inconclusive at 99 test positives
  (`docs/phase2/F106_DEQUANTIZATION.md`).
- [SIM] That circuit needs about 10,000 [shots](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qc-shot) per row to stay within
  0.005 [AUPRC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auprc) of exact; shot [noise](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qc-noise) reorders a few positives and moves
  [AUPRC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auprc) by several points (`docs/phase2/F107_SHOT_BUDGET.md`).
- [SIM] The [SPECTRA](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-spectra) Tier 1 screen reproduces on [UCI](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-uci) steel ([GAM](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-gam) 0.914
  against 0.94) and says "candidate" on 32 of 35 runs, fraud included,
  so it does not refuse fraud (`docs/phase2/F103_TIER1_CHECK.md`,
  `docs/phase2/F109_TIER1_LADDER.md`).
- [HW] A [QSVM](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-qsvm) on Dirac-3 scored a mean test [AUPRC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auprc) of 0.212 against
  CVQBoost's 0.767 on the same data (`docs/B4_B5_HARDWARE_RESULT.md`).
- [SIM] F106's circuit on [IEEE-CIS](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ieee-cis) month 4, eight seeds: dequantized.
  [GAM](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-gam) and [HGB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-hgb) are no worse within the 0.005 margin on the test-row
  interval. A t interval over the eight per-seed deltas crosses the
  margin, so the outcome is not shown across training draws
  (`docs/phase2/F157_QNN_IEEE.md`).

### What outside research says

- No exponential [quantum advantage](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qc-quantum-advantage) is known for purely classical data
  (EvidenceBasedDB `cerezo-no-known-exponential-advantage-classical-data`,
  high).
- Quantum [PAC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-pac) sample complexity equals classical up to constants
  (EvidenceBasedDB `ciliberto-quantum-pac-sample-complexity-equivalent`,
  high).
- Generalization error is bounded by about sqrt(T log T / N) for T
  trainable gates and N points (EvidenceBasedDB
  `caro-generalization-error-sqrt-t-over-n`, low).
- Any variational model with a general encoding can be written as a
  matrix product state, a tensor network model (EvidenceBasedDB `vqml-is-mps-theorem`,
  high).
- Fidelity kernels with low-entangling circuits can be simulated
  classically (EvidenceBasedDB
  `fidelity-kernels-classically-simulable-limit`, high).
- Kernel bandwidth was the most important hyperparameter in one study
  (EvidenceBasedDB `bandwidth-most-important-hyperparameter`, low).
- The fraud kernel study reporting a 15% average-precision separation at
  20 [qubits](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qc-qubit) used 500 subsampled transactions with 25 frauds
  (EvidenceBasedDB `quantum-kernel-ap-separation`, low;
  EvidenceBasedDB `dataset-and-simulation-setup`, high).

### Candidate algorithms

- [QUBO](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-qubo) feature or [learner selection](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qml-learner-selection) built from statistics accumulated
  over the rows; the final model stays classical, and the [QUBO](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-qubo)'s size
  does not grow with the data.
- Projected or landmark [quantum kernels](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qml-quantum-kernel), each beside a random Fourier
  feature and tensor-network surrogate.
- Small trained circuits on low-dimensional phase features, beside
  [GAM](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-gam), [GA2M](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ga2m), the joint twin and [HGB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-hgb).

### Experiments that would show what quantum machine learning can do

- The circuit-against-twins test at a test-positive count large enough
  to decide equivalence at a 0.005 margin (Sprint 31's [QNN](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-qnn) run).
- An equal-feature ablation, so a quantum-selected subset is compared
  with classical lanes on the same subset.
- A selection problem with a gap below greedy larger than the device's
  resolution, then a device run against the best classical solver.

## 7. Experiments planned (Sprint 31)

Each entry is in `experiments/phase2/PREREGISTRATION_DRAFT.md`, written
before its run. Each result, dated, is under its entry. The
six-experiment frame is in `docs/phase2/PHASE2_POC_PLAN_DRAFT.md`.

- **F114, the ceiling on real data** (F108 entry, amendment of
  2026-11-05): F169's LightGBM plug-in on [ULB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ulb) (F166's split) and [IEEE-CIS](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ieee-cis)
  (F174's folds), seeds 42-51, with a shuffled-label arm first that must
  sit at the no-information level; if it fails, the real-data values are
  plug-in values only, never ceilings.
  - Result, 2026-11-05: the shuffled-label check failed (estimate 0.0011
    against a test fraud rate of 0.0017, margin 0.0005), and at learning
    rate 0.1 the estimator did not fit [ULB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ulb) on any of nine seeds (test
    [AUPRC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auprc) 0.002 to 0.327). No ceiling is reported; the check may reflect
    the collapse rather than the method. The next step is Sprint 31 D11
    (`experiments/phase2/results/f114_real_ceiling.json`).
  - Result of the re-run at learning rate 0.05, 2026-11-05 (D11
    option 1): stage 1 recovered on 5 of 5 seeds on every arm; the
    shuffled-label check passed (0.00118 against 0.00167, margin
    0.0005). [IEEE-CIS](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ieee-cis) plug-in 0.0254 (0.0232 to 0.0276)
    against an achieved error of 0.0293; [ULB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ulb) 0.00016 (0.00010
    to 0.00022) against 0.00111. Both carry the calibration warning;
    the [ULB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ulb) figure is not a usable ceiling, and three [ULB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ulb)
    seeds still fit badly (train [AUPRC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auprc) 0.887, 0.624, 0.925)
    (`experiments/phase2/results/f114_real_ceiling_lr05.json`).
- **F157 [QNN](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-qnn) part** (F106 entry, amendment of 2026-11-05): the same
  circuit and six twins on [IEEE-CIS](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ieee-cis)'s month-4 fold, about 2,962 test
  positives, 295 training positives and 6,000 negatives, seeds 42-49. It
  can decide "dequantized"; "circuit ahead" may stay out of reach for the
  three widest twins.
  - Result, 2026-11-05: **dequantized.** [GAM](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-gam) (twin minus circuit
    +0.0047, 99.17% interval +0.0007 to +0.0092) and [HGB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-hgb) (+0.0193,
    +0.0139 to +0.0247) are no worse within the 0.005 margin; the circuit
    is ahead of logistic regression, the joint 3-way twin and [RFF](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-rff). The interval
    resamples test rows; across seeds [HGB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-hgb) is ahead on 5 of 8
    (Wilcoxon p 0.109) (`experiments/phase2/results/f157_qnn_ieee.json`).
- **F157 [SPECTRA](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-spectra) part**: F166's seven algorithms and grids on
  energy_steel, oilgas_gasturbine, telecom_churn and maintenance_ai4i,
  with in-pocket and out-of-pocket [AUPRC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auprc) as secondaries.
  - Result, 2026-11-05: boosted trees first by mean test [AUPRC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auprc) on every
    dataset; the proxy fifth or sixth of seven. Reliable adjacent pairs
    (exact Wilcoxon, Bonferroni 0.05 / 6): the proxy above logistic
    regression on energy_steel, oilgas_gasturbine and telecom_churn; the
    [SVM](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-svm) above the proxy on oilgas_gasturbine (0.8532 against 0.8394)
    and telecom_churn (0.8441 against 0.7254); LightGBM above the proxy
    on maintenance_ai4i (0.6148 against 0.5387). The [SVM](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-svm) lane is
    the [RBF](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-rbf) form the entry's rule kept on all four datasets, scored
    under the entry's amendment of 2026-11-05. On energy_steel seed 42 its
    scores carry no ranking on validation and do on test; not explained
    (`experiments/phase2/results/f157_spectra_algorithms_rbf.json`).
- **Experiment 5, segment routing**: on F174's stored month-4 scores, is
  any ProductCD segment accepted for the proxy (mean in-segment recall
  edge at least 0.01 and a 99% interval of segment minus matched-control
  edge above 0)? [HGB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-hgb) is checked first in the proxy's place; the
  prediction is that no segment is accepted.
  - Result, 2026-11-05: no segment accepted for the proxy or for [HGB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-hgb).
    W cannot be matched; on C, R, H and S the champion's in-segment alerts
    are all frauds, so recall at the budget saturates and edges are 0 or
    below by construction. The minimum-edge clause, not the interval,
    kept [HGB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-hgb) out on C and R (`docs/phase2/EXP5_ROUTER.md`).
- **F155, the [Dirac-3S](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qc-dirac-3s) size limit**: one 1,350-variable job; accepted
  only if the solution has 1,350 entries. No accuracy is read.
  - Result, 2026-11-05: accepted; 1,350 entries returned, 6.0
    metered seconds. The pool failed the resolution screen, so the
    probe tests acceptance only, by design
    (`experiments/phase2/results/f155_variable_ceiling.json`).
- **F95, relaxation schedule 4**: four fits; the solver gap against the
  exact optimum. No accuracy is read.
  - Result, 2026-11-05: no change on the two fits with a schedule-2
    twin on the same device, whose pools fail the resolution screen,
    so the test is weak; the two 45-variable fits have only Dirac-3
    history and are not compared. 67.0 of 120 metered seconds
    (`docs/phase2/F95_SCHEDULE4.md`).

## 8. Experiments not yet planned

From EvidenceBasedDB's memo `docs/spikes/F118_WHAT_THE_STORE_SAYS.md`
(in that repository), ranked there by cost and decisiveness; none is
scheduled here.

- Equal-feature ablation on [ULB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ulb) and [IEEE-CIS](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ieee-cis): give every classical lane
  the proxy's 17 features.
- A classical surrogate (random Fourier features, a matrix product state or a spectral
  tensor network) for any quantum kernel lane.
- Kernel concentration against qubit count (2 to 14) and bandwidth on
  fraud features, fidelity against projected kernels.
- A sample-count sweep with a tuned classical control.
- Production-scale timing at 1, 10 and 100 million rows, classical
  training and scoring beside a quantum lane's loading and shot cost.
- A streaming build of the selection [QUBO](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-qubo) in one pass over the rows,
  checked against the in-memory build.

## 9. Index of what was tested

The plain-terms version's section 9 lists every dataset, model and
platform with its source. In short: [ULB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ulb), [IEEE-CIS](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ieee-cis), [SPECTRA](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-spectra)'s four
datasets, [UCI](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-uci) steel and the F108 simulator; XGBoost, LightGBM, CatBoost,
[HGB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-hgb), logistic regression, linear and [RBF](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-rbf) [SVM](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-svm), [GAM](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-gam), [GA2M](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ga2m), the joint twin,
[RFF](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-rff), [KNN](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-knn) within CVQBoost, CVQBoost on device and proxy, [QSVM](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-qsvm) and an
8-qubit simulated circuit; Dirac-3, Dirac-3S, a NumPy statevector
simulator and a classical workstation.

## Appendix A. Terms the plain-terms version does not define

- <a id="ml2-floor-normalization"></a>**Floor normalization**: [AUPRC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auprc)
  rescaled so the fraud rate (a random ranker's score) maps to 0 and a
  perfect ranker to 1, so folds with different fraud rates compare.
- <a id="ml2-wilcoxon-test"></a>**Exact Wilcoxon signed-rank test**: a
  paired test on per-seed differences, exact at small seed counts; our
  primary test with 8 or more seeds.
- <a id="ml2-bonferroni-correction"></a>**Bonferroni correction**:
  dividing the significance level by the number of tests in a family
  (for example 0.05 / 6 for six adjacent pairs).
- <a id="ml2-paired-bootstrap"></a>**Paired bootstrap interval**: an
  interval for a difference between two models from resampling the same
  test rows for both.
- <a id="ml2-rolling-origin"></a>**Rolling-origin evaluation**: train on
  all months before a cutoff, test on the next month, then move the
  cutoff forward.
- <a id="ml2-adversarial-validation"></a>**Adversarial validation**: a
  classifier trained to tell training rows from test rows; an [AUC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auc) near 1
  means the two still differ (drift). Our control drops the most
  telling features round by round, up to a cap.
- <a id="ml2-plug-in-estimator"></a>**Plug-in estimator**: an estimate of
  the Bayes error from a model's probabilities, the mean of min(p, 1 - p).
- <a id="ml2-isotonic-calibration"></a>**Isotonic calibration**: a
  monotone remapping of scores to probabilities, fitted on held-out rows.
- <a id="ml2-equivalence-margin"></a>**Equivalence margin**: the largest
  difference treated as "no difference"; our default is 0.005 [AUPRC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auprc).
- <a id="ml2-outcome-block"></a>**Outcome block**: the confusion counts
  at the 0.5% budget and the per-row test scores with their hash that
  every scored Phase 2 result stores.
- <a id="ml2-oracle-gap"></a>**Oracle gap**: the recall a per-row chooser
  that sees the label would add over one model; an upper bound on any
  router.
- <a id="ml2-capacity-floor"></a>**Capacity floor**: the share of frauds
  that must be missed because the alert budget is smaller than the fraud
  count.
- <a id="ml2-shuffled-label-control"></a>**Shuffled-label control**: the
  same pipeline on permuted training labels; it must fall to chance.
- <a id="ml2-deterministic-lane"></a>**Deterministic lane**: a model whose
  result does not change with the seed on fixed folds, so its seeds are
  not independent evidence.
- <a id="ml2-matched-control"></a>**Matched random-segment control**: a
  random group of rows of the same size and fraud rate as a segment, used
  to tell a segment effect from a routing effect.
