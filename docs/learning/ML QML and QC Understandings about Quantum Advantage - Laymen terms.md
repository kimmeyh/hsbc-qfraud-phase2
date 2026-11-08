# What We Have Learned About Quantum Advantage for Fraud Detection, in Plain Terms

**Version 1.2**, 2026-11-06 (Sprint 31, card F178). Written for readers
who know some math, science, computing, machine learning and quantum
computing, and are expert in none of them. Two companion versions go
deeper: one for [machine learning experts](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20ML%20Expert.md)
and one for [quantum computing experts](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20QC%20Expert.md).

## Change list

- **1.2, 2026-11-06 (Sprint 31)**: the team lead's review. Each numbered section opens with an "In short" summary. Each dataset is named in full the first time, with a link to the new Appendix F (Datasets), and by its short name after that; the short name links to the same entry. "[Device](#def-device)" is defined (Appendix A). Section 3's results are rewritten in plain terms, each starting with what it means. The team lead's suggestions are added to "The data needed", with why each would help and what the public data already holds. New: the card-testing pattern, what our tests score inside the [alert budget](#ml-alert-budget), [interference](#qc-interference) beside [superposition](#qc-superposition) and [entanglement](#qc-entanglement), and where the training-cost growth was measured. "Experiments not yet planned" gains the backlog proposals of Sprint 31 D18.
- **1.1, 2026-11-05 (Sprint 31)**: Sprint 31's results added. Each is a tagged claim under its topic's "What our experiments showed" and a dated result under "Experiments planned": F114, F155, F157 (both parts), Experiment 5 and F95. No Sprint 32 run is preregistered yet, so none is listed.
- **1.0, 2026-11-05 (Sprint 31)**: first version. It covers Phase 1
  (filed 2026-09-12) and Phase 2 up to Sprint 30. Sprint 31's own runs
  have not finished; each has a marked place in "Experiments planned"
  where its result will go.

## Bottom line

- **Our experiments found no [quantum advantage](#qc-quantum-advantage) for credit card fraud
  detection.** Tuned classical models were the best detectors on every
  fraud dataset we tried. The quantum and [quantum-inspired](#qc-quantum-inspired) methods came
  close on some tests and never won on a test that was set before the
  run.
- **The quantum hardware worked as a solver.** The [Dirac-3](#qc-dirac-3) and [Dirac-3S](#qc-dirac-3s)
  machines solved the math problems we gave them. On our first problem
  any good solver gets the same answer, so a perfect solver could not
  help. The problem has to change before a [device](#def-device) can show anything.
- **Outside research agrees.** Our store of published papers, in the
  themes we read, holds no result in which a quantum model beats a tuned classical model on
  table-shaped, unbalanced data like card payments.
- **What could still help is mostly classical.** Better data (more fields
  about the merchant, the customer's device and the account) and better use of the
  [alert budget](#ml-alert-budget) matter more than any quantum step we tested.
- **The quantum role that still fits is narrow.** A device can pick a
  small set of [features](#ml-feature) or models from a summary of the data. Our tests
  of that role are not finished.

## How to read this document

- **Each numbered section starts with "In short"**: its conclusion in a
  few sentences. The detail follows.
- **Two tiers of evidence.** Each topic has "What our experiments
  showed" first, then "What outside research says". Our results are
  measured by this project. Outside results come from published papers.
- **Every one of our claims names its source.** Each claim ends with the
  repository path of the result file or document it comes from. A test
  (`experiments/src/test_learning_docs.py`) checks that each path exists
  and that each decimal number in the claim appears in that source.
- **Every claim carries an [evidence tag](#def-evidence-tag)**: [HW] measured on quantum
  hardware, [SIM] measured on a classical computer (including
  simulations), [PROJ] projected. See [evidence tag](#def-evidence-tag).
- **Outside claims carry a grade**, copied from the EvidenceBasedDB
  store: "high" means the paper proves or defines it; "low" means one
  study measured or claimed it.
- **Linked words** go to the appendices at the end. Each acronym
  is spelled out the first time and links to its entry every time. Each
  dataset is named in full the first time; its short name links to the
  same entry in Appendix F.
- **Adding to this document.** Anyone may add text, for example a
  suggestion under "The data needed". Two rules are checked when the
  test runs: a line under "What our experiments showed" must be a tagged
  claim with its source file, and a word of two or more capital letters
  (an acronym) needs an entry in Appendix B and a link to it. If an
  addition breaks a rule, the next update fixes it.

## How this document was made

- Our results were read from this repository's result documents on
  2026-11-05 and 2026-11-06: `docs/phase2/`, `docs/phase2/algorithms/`,
  the sprint summaries in `docs/sprints/`, the Phase 2 draft plan
  `experiments/phase2/PREREGISTRATION_DRAFT.md`, and the filed Phase 1
  proposal `docs/paper/proposal.md`.
- Outside claims were read from the EvidenceBasedDB store, read only, on
  2026-11-05 and 2026-11-06 (snapshot). Refresh one with
  `python scripts/edb_query.py show <id>`.
- The form follows EvidenceBasedDB's memo
  `docs/spikes/F118_WHAT_THE_STORE_SAYS.md` (in that repository).

## 1. The challenge, in one paragraph

**In short:** can quantum computing find more card fraud than ordinary
computing, within the number of alerts a bank can check? We tested this
on public data and on real quantum hardware.

[HSBC](#acr-hsbc) asked whether quantum computing ([QC](#acr-qc)) can help find credit card
fraud. This project answered with machine learning ([ML](#acr-ml)) models, a
quantum-inspired model trained on real quantum hardware, and simulated
[quantum circuits](#qc-quantum-circuit). Phase 1 was filed on 2026-09-12. Phase 2 continues
the work. The aim is any real gain, quantum or classical: more fraud
caught and fewer frauds missed, within the number of alerts a bank can
review. Our data: two public card-fraud datasets, the
[credit card dataset of the Universite Libre de Bruxelles](#ds-ulb) ([ULB](#ds-ulb))
and the [fraud detection dataset of the Institute of Electrical and Electronics Engineers Computational Intelligence Society](#ds-ieee-cis) ([IEEE-CIS](#ds-ieee-cis));
four [quantum-ready benchmark datasets](#ds-spectra) called [SPECTRA](#ds-spectra), built so that a
quantum model could win; and our own [fraud simulator](#ds-simulator). Appendix F describes
each one.

## 2. Credit card fraud

**In short:** fraud is rare, it changes over time, and a bank can check
only a small share of payments. On [IEEE-CIS](#ds-ieee-cis) the review limit alone means
most fraud is missed before any model is chosen. The frauds every model
misses look like normal payments in the data we have, so the next gain
needs more data, not a different model.

### What it is

Card fraud is a payment the card holder did not make or did not allow.
This project works on card-not-present ([CNP](#acr-cnp)) fraud: online or phone
payments, where no physical card is shown (`docs/requirements-matrix.md`,
item D16). Other kinds, such as account takeover or a person defrauding
the bank with their own card, are out of scope.

### Why it is hard

- **It is rare.** Frauds are 0.17% of payments in [ULB](#ds-ulb) and 3.5% in
  [IEEE-CIS](#ds-ieee-cis) (`docs/paper/proposal.md`, section 1). A model that calls every
  payment "not fraud" is almost always right and still useless. This is
  [class imbalance](#ml-class-imbalance).
- **Mistakes cost different amounts.** A missed fraud becomes a
  chargeback: the bank pays it back. A false alarm can lose a good
  customer (`docs/paper/proposal.md`, section 1).
- **People can check only so many alerts.** A bank sets an alert budget:
  for example, the top 0.5% most suspicious payments go to an analyst.
  What matters is how much fraud lands inside that budget.
- **[Labels](#ml-label) arrive late.** A payment is confirmed as fraud weeks after it
  happens, when the chargeback arrives (`docs/paper/proposal.md`,
  section 3).
- **Fraud changes over time.** Fraudsters adapt, so a model trained on
  last month can do worse this month. This is [drift](#ml-drift).

### Known patterns

- **A compromised terminal**: every payment at one shop terminal is
  fraud for some days. The fraud-detection handbook from the team that
  released [ULB](#ds-ulb) describes this pattern, and our simulator copies it
  (`experiments/phase2/PREREGISTRATION_DRAFT.md`, the F108 entry).
- **A compromised customer**: a stolen card is used for some of the
  owner's payments, at larger amounts (the same entry).
- **Card testing** (the team lead's example, 2026-11-06): a very small
  payment, such as $0.50, checks that a stolen card works, and a large
  one, $100 or more, follows within a day. Seeing it needs payments
  linked to one card over time. [ULB](#ds-ulb) has no card field, so it cannot show
  this; [IEEE-CIS](#ds-ieee-cis) has masked card fields that can link payments. This
  pattern is not yet in our evidence store or tested; a test is proposed
  (section 8).
- **Product and customer device signals**: in [IEEE-CIS](#ds-ieee-cis), the frauds every
  model missed were more often of one product type and more often had no
  customer device type recorded (section 2's claims below).

### The data needed

- **What public data has**: amounts, times, and features made
  anonymous. In the filed proposal's words, "the benchmarks' features are
  anonymized principal components", the output of principal component
  analysis ([PCA](#acr-pca)) (`docs/paper/proposal.md`, section 3). That is true
  of [ULB](#ds-ulb); [IEEE-CIS](#ds-ieee-cis) has more named fields (Appendix F).
- **What a bank would need to add**: merchant, customer device and
  account-age features, and labels that wait for the chargeback window to
  close (`docs/paper/proposal.md`, section 3). No public benchmark carries
  them.
- **The team lead's suggestions (2026-11-06)**, each with why it could
  help and what the public data already holds:
  - **Card identifier and the card's purchase history**: to see one
    card's pattern over time, including card testing. [IEEE-CIS](#ds-ieee-cis) has masked
    card fields (card1 to card6) and no card number. A card-holder key
    built from them already raised one model's ranking score from 0.758
    to 0.816 (`docs/phase2/F109_TIER1_LADDER.md`).
  - **Customer identifier, the customer's other cards, and their
    purchase histories**: to cross-check a customer's wider buying
    pattern, not one card's. Neither public dataset has them.
  - **Customer advertising identifiers and their purchase histories**:
    to cross-check the same person's buying across sites and apps.
    Neither dataset has them.
  - **Social media accounts tied to the customer** (posts, likes and
    text on X, TikTok, Facebook, Instagram and others): for generative
    artificial intelligence tools to read. Neither dataset has them.
    Whether a bank may use them is a legal and consent question we have
    not checked.
  - **Customer address** (street, postal code, county, state, country):
    some fraud shows in address details. [IEEE-CIS](#ds-ieee-cis) has two masked address
    fields and two distance fields; [ULB](#ds-ulb) has none.
  - **Product details** (model, quantity, price, description), to add to
    the customer's purchase pattern and for generative artificial
    intelligence tools: product code W was 53.0% of the frauds every
    model missed (`docs/phase2/F171_MISSED_IEEE.md`). [IEEE-CIS](#ds-ieee-cis) has one product
    code only.
  - **Merchant details**: company, location, a registry number (such as
    a Dun & Bradstreet number or a Legal Entity Identifier), the parent
    company or division, and the web page or app. Why: to see fraud
    patterns at one merchant across many customers. [IEEE-CIS](#ds-ieee-cis) has the buyer's
    and the recipient's email domains and no merchant field.
  - **More customer device details** (web page or app, and similar):
    a missing customer device type was 55.4% of the frauds every model
    missed (`docs/phase2/F171_MISSED_IEEE.md`), and on our simulator a
    compromised terminal leaves no trace in the visible fields. Device
    details may also show which devices make fraud more or less likely.
    [IEEE-CIS](#ds-ieee-cis) has a device type, a device description and masked identity
    fields for some payments.
  - A study of the data fraud investigators use, or could use, is
    proposed (section 8).

### How companies use machine learning against it, and what matters to them

- **A model scores every payment.** The highest scores go to analysts or
  are blocked. Tuned [gradient boosting](#ml-gradient-boosting) models
  are a strong choice, and they were the best in our tests.
- **What matters**, as this project's filed proposal states it
  (`docs/paper/proposal.md`, sections 1 and 3): fraud caught within a
  fixed review budget; few false alarms; scoring fast enough for a live
  payment (low tens of milliseconds, not measured by us); results that
  can be explained to a customer or a regulator; and fair treatment of
  customer groups.
- **What our tests score inside the budget.** Each model ranks all
  payments, and we count the frauds among the top 0.5%. With a fixed
  number of alerts, each extra fraud caught is one fewer false alarm, so
  "most frauds caught" and "fewest false alarms" are the same goal there.
  Our tests do not yet weigh a payment by its amount or by the cost of
  checking it. Both datasets record the amount, so a test that ranks by
  money saved is possible; one is proposed (section 8).

### What our experiments showed

- [SIM] **Some frauds look exactly like normal payments, so no model can
  catch them from these fields.** On [ULB](#ds-ulb), 36 frauds were missed by every
  model family in every test in which they appeared. Their 10 nearest
  payments were all or almost all legitimate (median share of legitimate
  neighbors 1.0, against 0.1 for frauds that were caught)
  (`docs/phase2/F170_MISSED_NEIGHBORS.md`).
- [SIM] **On [IEEE-CIS](#ds-ieee-cis), the review limit, not the models, decides most of
  what is missed.** With a 0.5% alert budget, 81.5% of frauds were missed
  by every model, against 11.2% on [ULB](#ds-ulb). [IEEE-CIS](#ds-ieee-cis) has far more fraud than a
  0.5% budget can hold. With a budget matched to each dataset's fraud
  rate the shares were 18.2% and 11.2%
  (`docs/phase2/F171_MISSED_IEEE.md`).
- [SIM] **The frauds every model missed share two traits, which point to
  the data that is missing.** Among the frauds every model missed in at
  least one seed on [IEEE-CIS](#ds-ieee-cis), product code W was 53.0% of missed frauds
  against 7.5% of caught ones, and a missing customer device type was
  55.4% against 8.5%. This describes them; it does not explain them
  (`docs/phase2/F171_MISSED_IEEE.md`).
- [SIM] **On [IEEE-CIS](#ds-ieee-cis), most fraud is missed before any model is scored.**
  In its test month, frauds are 3.47% of payments. A 0.5% budget allows
  427 alerts for 2,962 frauds
  (`docs/phase2/algorithms/IEEE_COMPARISON.md`).
- [SIM] **Fraud changes over time, and simple models suffer most.**
  Trained on earlier months of [IEEE-CIS](#ds-ieee-cis), [logistic regression](#ml-logistic-regression) scored 0.337 on
  month 4 and 0.122 on month 5 (a floor-normalized [precision](#ml-precision) score), while
  the tree models held or improved; LightGBM led every month with 0.526,
  0.536 and 0.616 (`docs/phase2/F152_EXP2_RESULT.md`).
- [SIM] **One detector per fraud type did worse than one detector for
  all fraud.** On our [fraud simulator](#ds-simulator), the set of detectors caught less
  fraud within a 0.5% budget than one model trained on all fraud (mean
  [recall](#ml-recall) difference -0.069) (`docs/sprints/SPRINT_29_VALIDATION.md`).
- [SIM] **Some fraud cannot be seen in the data at all.** On the
  simulator, even the best possible model reaches a precision-recall
  score of only 0.296 to 0.318, because a compromised terminal leaves no
  trace in the visible features
  (`docs/phase2/F108_CEILING_VALIDATION.md`).

### What outside research says

- Quantum fraud studies often run on tiny samples: one used 500
  payments with 25 frauds, drawn from 284,807 (EvidenceBasedDB
  `dataset-and-simulation-setup`, high).
- Some studies test on data with frauds made common on purpose (about
  43% fraud), so their scores do not carry over to real fraud rates
  (EvidenceBasedDB `fraudtransformer-evaluation-set-undersampled`, high).
- Balancing the data before splitting it into training and test parts
  leaks information and inflates scores to near perfect
  (EvidenceBasedDB `kabane-presplit-inflation`, low).
- Many published scores on [IEEE-CIS](#ds-ieee-cis) use random splits, not splits by
  time, so they are not a fair target for a model that must work on next
  month's payments (EvidenceBasedDB
  `han-ieee-cis-best-test-scores-random-split`, low).
- If checking an alert has a fixed cost, the best rule flags a payment
  when its fraud score is above that cost divided by the payment amount
  (EvidenceBasedDB `hoppner-instance-threshold`, high).
- The fraud-detection handbook from [ULB](#ds-ulb)'s authors advises splits by
  time, with a delay for late labels
  ([handbook, validation strategies](https://fraud-detection-handbook.github.io/fraud-detection-handbook/Chapter_5_ModelValidationAndSelection/ValidationStrategies.html)).

## 3. Machine learning

**In short:** ordinary tuned models, mostly boosted trees, were the best
on every dataset. The quantum-inspired model placed in the middle: below
the boosted trees, above the simplest models. Most of the top models are
too close to put in a firm order. Our checks show the methods are honest,
and a published quantum-inspired result did not hold up.

### What we know for sure

Machine learning finds patterns in past examples and scores new ones.
For fraud, each example is a payment with features (amount, time and so
on) and a label (fraud or not). A model is trained on one part of the
data and scored on a separate test part it has never seen. The scores
that matter are the area under the precision-recall curve ([AUPRC](#acr-auprc)) and
recall at the alert budget. [AUPRC](#acr-auprc) runs from 0 to 1: 1 means every
fraud is ranked above every normal payment, and a random guess scores
about the fraud rate.

### What our experiments showed

- [SIM] **On [ULB](#ds-ulb), the boosted-tree models scored best, the
  quantum-inspired model came next, and the simple linear models came
  last. The top four cannot be put in a firm order.** Over 10
  [repeats](#def-repeat), mean test [AUPRC](#acr-auprc) was CatBoost 0.8329, LightGBM 0.8270,
  XGBoost 0.8229, histogram-based gradient boosting ([HGB](#acr-hgb)) 0.8124, the
  quantum-inspired [CVQBoost](#qml-cvqboost) model run on a classical solver 0.7925, a
  linear support vector machine ([SVM](#acr-svm)) 0.7419 and logistic regression
  0.7270. Only two neighboring pairs differ reliably: the
  quantum-inspired model above the [SVM](#acr-svm), and the [SVM](#acr-svm) above logistic
  regression (`docs/phase2/algorithms/ULB_COMPARISON.md`).
- [SIM] **At the bank's review limit, all seven models catch about the
  same share of fraud on [ULB](#ds-ulb): 83 to 86 frauds of every 100.** Recall at a
  0.5% alert budget was between 0.8305 and 0.8589, a narrower spread than
  [AUPRC](#acr-auprc)'s (`docs/phase2/algorithms/ULB_COMPARISON.md`).
- [SIM] **On [IEEE-CIS](#ds-ieee-cis), a harder dataset tested month by month, LightGBM
  is clearly best, and the quantum-inspired model is fifth of seven.**
  Mean test [AUPRC](#acr-auprc) was LightGBM 0.5785, [HGB](#acr-hgb) 0.5211, CatBoost 0.5114,
  XGBoost 0.4960, the quantum-inspired model 0.4862, [SVM](#acr-svm) 0.3612 and
  logistic regression 0.3564. LightGBM is reliably above [HGB](#acr-hgb)
  (`docs/phase2/algorithms/IEEE_COMPARISON.md`).
- [SIM] **Our method passes a basic honesty check: with the answers
  scrambled, the model finds nothing.** In Phase 1, tuned CatBoost on
  [ULB](#ds-ulb) scored [AUPRC](#acr-auprc) 0.8368. With the labels shuffled, the same pipeline
  fell to 0.0023, near the fraud rate of 0.0017
  (`docs/paper/proposal.md`).
- [SIM] **We report our misses.** A goal set before Phase 1 (tuned
  XGBoost at [AUPRC](#acr-auprc) 0.85 or more on [ULB](#ds-ulb)) failed at 0.8296, and it is
  reported as a failure (`README.md`).
- [SIM] **One wrong default setting can make a good model look bad, and
  so make another model look better than it is.** [HGB](#acr-hgb) with its default
  settings scored a mean [AUPRC](#acr-auprc) of 0.375, and its results swung widely
  between repeats (standard deviation 0.170). One change, a small
  penalty on large leaf values, gave 0.804 with a spread of 0.022
  (`docs/phase2/F151_HGB_COMPARATOR.md`).
- [SIM] **The models make almost the same mistakes, so switching between
  them gains little.** In every pair of stored [ULB](#ds-ulb) models, the frauds one
  model catches and the other misses number at most 34 over ten repeats
  (`docs/phase2/F154_WHERE_MODELS_WIN.md`).
- [SIM] **Choosing the right model for each payment could help a little,
  but the help comes from having any two different models, not from the
  quantum-inspired one.** A perfect chooser between the quantum-inspired
  model and XGBoost would catch 5.0 more points of fraud than XGBoost
  alone, and a perfect chooser between two XGBoost settings gains 3.6
  points too. No real chooser can be perfect
  (`docs/phase2/F113_ORACLE_GAP.md`).
- [SIM] **A published quantum-inspired fraud result did not hold up when
  we repeated it.** The paper reported 0.8108; our run of that k-nearest
  neighbors ([KNN](#acr-knn)) variant averaged 0.760, and a stable [HGB](#acr-hgb) beat it by 0.082
  and 0.033 under the two protocols tested
  (`docs/phase2/F111_LOKE_PROTOCOL.md`).
- [SIM] **We can now estimate the best score any model could reach, but
  so far only on simulated data.** That limit is the
  [Bayes error](#ml-bayes-error). On our simulator, where the true value is known, a
  LightGBM model with fine bins recovered it on 5 of 5 repeats (for
  example 0.00609 against 0.0061) (`docs/phase2/F169_PLUGIN_BINS.md`).
- [SIM] **Two earlier ways to estimate that limit failed the same
  check**: they recovered the known value on only 2 of 5 repeats
  (`docs/phase2/F108_CEILING_VALIDATION.md`,
  `docs/phase2/F114_CALIBRATED_PLUGIN.md`).
- [SIM] **On [SPECTRA](#ds-spectra)'s four datasets, which were built to favor quantum
  models, ordinary boosted trees still won.** Over 10 repeats on each of
  energy_steel, oilgas_gasturbine, telecom_churn and maintenance_ai4i,
  scored on the label with the planted quantum-friendly pattern,
  boosted-tree models had the highest mean test [AUPRC](#acr-auprc), and the
  quantum-inspired model placed fifth or sixth of seven. A radial basis
  function ([RBF](#acr-rbf)) [SVM](#acr-svm) scored reliably above it on oilgas_gasturbine
  (0.8532 against 0.8394) and telecom_churn (0.8441 against 0.7254)
  (`experiments/phase2/results/f157_spectra_algorithms_rbf.json`).
- [SIM] **On [IEEE-CIS](#ds-ieee-cis), the best possible model may not be much better
  than ours, but this estimate rests on an assumption that does not fully
  hold.** For the fourth month the estimated limit is 0.0254 (0.0232 to
  0.0276), against the model's own error of 0.0293: about 25 errors per
  1,000 payments against 29. The check says the model's probabilities are
  not well calibrated, which weakens the estimate. The [ULB](#ds-ulb) estimate,
  0.00016, is not usable
  (`experiments/phase2/results/f114_real_ceiling_lr05.json`).

### What outside research says

- Tuned classical kernels beat the best [quantum kernel](#qml-quantum-kernel) on 8 of 9 public
  table datasets in one study; with 16 paired repeats the classical
  kernels were significantly better on 6 of 7 (EvidenceBasedDB
  `qksvm-classical-kernels-better-on-uci-tabular`, low).
- Balancing data before the split inflates fraud scores (EvidenceBasedDB
  `kabane-presplit-inflation`, low).
- [ULB](#ds-ulb)'s authors say precision-recall curves must not be drawn by
  straight-line interpolation, which overstates the area
  ([handbook, threshold-free metrics](https://fraud-detection-handbook.github.io/fraud-detection-handbook/Chapter_4_PerformanceMetrics/ThresholdFree.html)).

## 4. Quantum computing and the hardware we used

**In short:** the devices we used, QCi's Dirac-3 and Dirac-3S, are
optical machines that solve one kind of math problem. They solved our
problems correctly, and Dirac-3S more exactly than Dirac-3, but the
problems were ones a classical computer solves just as well. So the
hardware could not add accuracy, and no quantum effect was tested on it.

### What we know for sure

A quantum computer stores information in [qubits](#qc-qubit). A gate
based quantum computer runs [quantum circuits](#qc-quantum-circuit)
made of [quantum gates](#qc-quantum-gate) and reads the result by
repeated measurement, one [shot](#qc-shot) at a time. We did not use a
gate based machine; we simulated one on a laptop. The hardware we used
is different: QCi's Dirac-3 and Dirac-3S are optical machines that solve
optimization problems. QCi calls this [entropy quantum computing](#qc-entropy-quantum-computing).

Device findings below are this project's own. QCi has not validated
them (`docs/phase2/DIRAC_UNDERSTANDINGS.md`).

### What our experiments showed

- [HW] **The main Phase 1 test was a loss for the quantum-inspired
  model.** Trained on Dirac-3, CVQBoost scored [AUPRC](#acr-auprc) 0.7671 on [ULB](#ds-ulb) against
  0.8070 for CatBoost on the same 13 features. It trailed by 0.0399 and
  lost on 9 of 10 repeats. This is a [null result](#def-null-result) (`docs/paper/proposal.md`).
- [HW] **The device gave the same answer as an exact classical solve, so
  it could not add anything.** The difference was 0.0010 [AUPRC](#acr-auprc), and the
  answers pointed the same way (weight cosine 0.975 to 0.999). The
  problem was easy (a [convex problem](#qc-convex-problem)), so any good solver finds the same
  answer (`docs/paper/proposal.md`).
- [HW] **The one gain at scale was real but still behind the classical
  model.** An 833-variable version with three-feature parts gained
  0.0256 [AUPRC](#acr-auprc) on 10 of 10 repeats (absolute 0.7928). It still trailed
  full-feature CatBoost by 0.0440 (`docs/paper/proposal.md`).
- [HW, SIM] **That gain came from the model's design, not from the
  device.** An exact classical solve of the same set of parts differed
  from the device by +0.0002 on average (p = 0.92)
  (`docs/phase2/F144_PROXY_TWIN.md`).
- [SIM] **The gain came from bigger parts, not from more features.**
  With the device's classical stand-in on [ULB](#ds-ulb), going from two-feature
  to three-feature parts added 0.0245 [AUPRC](#acr-auprc). Going from 13 to 17
  features changed it by 0.0001, which counts as no change within 0.005
  (`experiments/phase2/PREREGISTRATION_DRAFT.md`,
  `docs/sprints/SPRINT_27_SUMMARY.md`).
- [HW] **Dirac-3 got less exact as problems grew.** The weight cosine was
  0.975-0.999 at small sizes, 0.89-0.90 at 560 variables, 0.83-0.85 at
  816 and 0.82-0.83 at 833. This fits QCi's stated limit on how finely
  the device can tell numbers apart
  (`docs/phase2/DIRAC_UNDERSTANDINGS.md`).
- [HW] **On [SPECTRA](#ds-spectra) data, an earlier positive device result did not
  repeat.** On telecom_churn and oilgas_gasturbine (energy_steel could
  not be scored), inside the chosen group the model did worse than a
  matched random group on all 8 cells that could be scored
  (`docs/B4_B5_HARDWARE_RESULT.md`).
- [HW] **A quantum support vector machine ([QSVM](#acr-qsvm)) on Dirac-3 was cheap and
  weak**: mean test [AUPRC](#acr-auprc) 0.212, against 0.767 for CVQBoost on the same
  data (`docs/B4_B5_HARDWARE_RESULT.md`).
- [HW] **Dirac-3S is the more exact solver, but exactness did not change
  accuracy.** It returned the exact answer where Dirac-3 did not: weight
  cosine 0.999993 and 0.9999999 against Dirac-3's 0.895 and 0.901. Test
  [AUPRC](#acr-auprc) did not change (0.85224 against 0.85225 for the exact solve)
  (`docs/phase2/F142_DIRAC3S_VERIFY.md`).
- [SIM] **Our first design of a harder problem for the device left no
  room for it to do better.** The best choice found was only 0.0016 to
  0.0026 from the lowest possible score, below the 0.01 needed, and a
  simple [greedy search](#qc-greedy-search) already found it
  (`docs/phase2/F153_EXP3_DESIGN.md`).
- [SIM] **A second design, on [IEEE-CIS](#ds-ieee-cis), has room.** Greedy search ends
  0.096 to 0.098 above the lowest possible score
  (`docs/sprints/SPRINT_29_VALIDATION.md`).
- [SIM] **But the best classical solver beat greedy by amounts too tiny
  to matter.** It got below greedy on 3 of 6 of those problems:
  [simulated annealing](#qc-simulated-annealing) reached -0.702763 against greedy's -0.702745,
  while the room was about 0.097. Gains that small may be too fine for
  the device to see (`docs/phase2/F176_BELOW_GREEDY.md`).
- [SIM] **A software copy of Dirac-3 matched its accuracy, not its
  answers.** The device returns 14-38% exact zeros, the copy 0.2-17%
  (`docs/phase2/F17_EMULATOR.md`).
- [SIM] **Averaging several device answers barely helped**: +0.0014
  [AUPRC](#acr-auprc), far below the spread between repeats
  (`docs/phase2/F20_SOFT_VOTES_RESULT.md`).
- [HW] **Dirac-3S takes problems of 1,350 variables.** It accepted the
  job and returned all 1,350 values, using 6.0 metered seconds. This
  tests size only, not accuracy
  (`experiments/phase2/results/f155_variable_ceiling.json`).
- [HW] **A slower device setting cost more and gained nothing we could
  see.** It found the same best answer as the usual one on four fits, at
  about three times the device time per sample
  (`experiments/phase2/results/f95_schedule4.json`).

### What outside research says

- QCi's own authors state that Dirac-3 does not use [entanglement](#qc-entanglement)
  (EvidenceBasedDB `dirac3-does-not-use-entanglement`, high).
- Dirac-3's user guide states an effective resolution of about 200:1:
  two numbers must differ by at least the largest divided by 200 to be
  told apart (EvidenceBasedDB `dirac3-analog-resolution-about-200-to-1`,
  high).
- An independent group matched QCi's published Dirac-3 benchmarks with
  classical solvers on an ordinary computer (EvidenceBasedDB
  `classical-solvers-match-dirac3-published-benchmarks`, low).
- The favorable Dirac-3 fraud paper lists all of its authors at QCi
  (EvidenceBasedDB `favorable-dirac3-papers-are-qci-authored`, high).
- Entanglement and [superposition](#qc-superposition) are not enough for an advantage: a class
  of circuits that uses both can be simulated quickly on a classical
  computer (EvidenceBasedDB
  `chowdhury-gottesman-knill-restated-stabilizer-simulable`, high).
- [Interference](#qc-interference) does not change that. Any circuit made only of
  "Clifford" gates can be simulated quickly on a classical computer
  (EvidenceBasedDB `dz-lg-clifford-simulable`, low), and those gates
  already make waves cancel, which is interference (EvidenceBasedDB
  `ferrie-classical-is-restricted-quantum`, low; the pairing of the two
  is our reading). What a classical computer cannot simulate cheaply is
  a circuit with many other ("non-Clifford") gates: the cost grows
  exponentially with their number (EvidenceBasedDB
  `cited-nonclifford-cost-magic`, low).
- Interference gives a large speedup only on special problems built for
  it, which is why quantum computers are expected to help classical ones,
  not replace them (EvidenceBasedDB `aaronson-foreword-special-problems`,
  low).
- Grover's search gives a proven quadratic speedup, not an exponential
  one (EvidenceBasedDB `qml-grover-quadratic-speedup-optimal`, high).
- In a comparison of solvers for this kind of problem, a classical
  method matched every best known answer on 176 problems
  (EvidenceBasedDB `hellstern-conclusions-main`, low).

## 5. Quantum machine learning

**In short:** we tested quantum learning models in simulation. Each time,
an ordinary model built to copy the quantum one did at least as well. A
simulated circuit that used superposition, entanglement and interference
together was matched by ordinary models on [IEEE-CIS](#ds-ieee-cis). Outside research
gives no known large advantage for data like ours.

### What we know for sure

Quantum machine learning ([QML](#acr-qml)) uses a quantum step inside a learning
model. The step can be a circuit that turns features into a score, a
[quantum kernel](#qml-quantum-kernel) that measures how alike two
payments are, or a device that solves the training problem, as with
CVQBoost. A quantum step helps only if no classical method can do the
same job as well and as fast. When a classical method can, the step is
"dequantized" ([dequantization](#qml-dequantization)).

### What our experiments showed

- [SIM] **On [ULB](#ds-ulb), a simulated quantum circuit could not be told apart
  from ordinary copies of it, because the test data held too few
  frauds.** We simulated an 8-qubit circuit and compared it with
  [classical twins](#qml-classical-twin) built to copy its function. The circuit scored
  0.699; [HGB](#acr-hgb) 0.719, a generalized additive model with pairwise
  interactions ([GA2M](#acr-ga2m)) 0.705, and a generalized additive model ([GAM](#acr-gam))
  0.704. With only 99 test frauds, no twin is shown to match the circuit,
  and the circuit does not beat every twin
  (`docs/phase2/F106_DEQUANTIZATION.md`).
- [SIM] **Running that circuit on real hardware would be very
  expensive.** It would need about 10,000 shots per payment to stay
  within 0.005 [AUPRC](#acr-auprc) of the exact simulation: about 5.7 x 10^8 shots
  for one test set (`docs/phase2/F107_SHOT_BUDGET.md`).
- [SIM] **At the sizes we can afford, hardware adds only cost and
  errors.** At every width we can afford, the circuit is exactly
  simulable on a laptop, so hardware would add [noise](#qc-noise) and cost and
  nothing else (`docs/phase2/F6_GATE_BASED_ARM.md`).
- [SIM] **The circuit used all three quantum properties at once and was
  still matched by ordinary models.** It puts each qubit in
  superposition with data-dependent rotations, links neighboring qubits
  with entangling gates, and its readout depends on interference. On
  [IEEE-CIS](#ds-ieee-cis)'s test month, two ordinary models, [GAM](#acr-gam) and [HGB](#acr-hgb), scored at least
  as well on eight repeats. Eight qubits is small enough to simulate
  exactly (`experiments/phase2/src/f106_dequant.py`,
  `docs/phase2/F157_QNN_IEEE.md`).
- [SIM] **The [SPECTRA](#ds-spectra) screening method works on the data it was built
  for**: it reproduced its published check on the
  [steel dataset of the University of California, Irvine](#ds-uci-steel) ([UCI](#acr-uci)): 0.914
  against the paper's 0.94 (`docs/phase2/F103_TIER1_CHECK.md`).
- [SIM] **But that screen says "maybe" to almost everything, fraud
  included, so it does not filter anything out.** It says "candidate" on
  32 of 35 dataset and repeat runs (`docs/phase2/F109_TIER1_LADDER.md`).
- [SIM] **On [SPECTRA](#ds-spectra)'s data, ordinary models beat the quantum-inspired
  model.** [HGB](#acr-hgb) and [GA2M](#acr-ga2m) beat it on all three cells tested
  (`docs/F100_CLASSICAL_BAR.md`).
- [SIM] **Our best fix brought the quantum-inspired model level with an
  ordinary model, never ahead.** A limit on how small a tree's leaves can
  be lifted it from 0.902 to 0.973 on [SPECTRA](#ds-spectra) energy_steel, level with
  [HGB](#acr-hgb)'s 0.965 there; no setting beat [HGB](#acr-hgb) on any dataset
  (`docs/phase2/SPECTRA_IMPROVEMENT_RESEARCH.md`).
- [SIM] **Even inside the group [SPECTRA](#ds-spectra) built for quantum models, the
  quantum-inspired model did not win.** It was not reliably above [HGB](#acr-hgb) or
  XGBoost on any dataset; where a difference was reliable, XGBoost was
  ahead, by 0.024 and 0.011 (`docs/phase2/F162_IN_POCKET.md`).
- [SIM] **That group is easy to spot from the ordinary fields, so sending
  it to a special model is not an independent choice.** The group can be
  predicted from the same features (area under the receiver operating
  characteristic curve ([AUROC](#acr-auroc)) 0.93 to 0.99)
  (`docs/F101_IN_POCKET_PROVENANCE.md`).
- [SIM] **Sending one product type to the quantum-inspired model did not
  help**: it did not add the required one point of recall in any product
  type (`docs/phase2/EXP5_ROUTER.md`).

### What outside research says

- For purely classical data, no exponential quantum advantage is known
  (EvidenceBasedDB `cerezo-no-known-exponential-advantage-classical-data`,
  high).
- A famous quantum speedup for recommendations disappears when a
  classical method gets the same kind of sampling access to the data
  (EvidenceBasedDB `tang-no-exponential-speedup`, high).
- Random trainable circuits get "flat": their training signal shrinks
  exponentially with the number of qubits, a
  [barren plateau](#qml-barren-plateau) (EvidenceBasedDB
  `mcclean-rpqc-gradient-variance-exp-small`, high).
- A common quantum kernel makes every pair of payments look equally
  unlike as qubits grow, so it needs exponentially many shots
  (EvidenceBasedDB `qfk-vanishing-similarity-definition`, high).
- One simulated fraud study reports a 15% better average precision for
  quantum kernels at 20 qubits, on a small sample (EvidenceBasedDB
  `quantum-kernel-ap-separation`, low).
- Noise can cause flat training on its own, and most studies ignore
  noise (EvidenceBasedDB `cerezo-noise-undermines-qml-claims`, high).
- One paper estimates that a quantum neural network ([QNN](#acr-qnn)) would need to
  be wider than 60 qubits to show an advantage in practice
  (EvidenceBasedDB `jaderberg-scale-limit`, high).
- A quantum memory that loads big data sets, a quantum random access
  memory ([QRAM](#acr-qram)), needs resources that grow with the data, so it may give
  no real advantage (EvidenceBasedDB `ciliberto-qram-caveats`, high).

### Candidate algorithms

- **Quantum selection of features or models.** A device picks a small set
  from a summary matrix. The summary does not grow with the number of
  payments, so this fits a bank's data size. It is our Experiment 3.
- **Quantum kernels with a small number of landmark payments**, compared
  against a classical copy of the same kernel.
- **Trained circuits on few features**, compared against classical twins
  on enough test frauds to decide.
- Not candidates for fraud data at bank scale: methods that load every
  payment into quantum memory (see [QRAM](#acr-qram) above).

### Experiments that would show what quantum machine learning can do

- A circuit test with thousands of test frauds per repeat, so a small
  difference can be decided. Sprint 31's [QNN](#acr-qnn) run did this on [IEEE-CIS](#ds-ieee-cis)
  (section 7).
- A selection problem where greedy search is clearly beaten by a
  classical solver by a margin the device can resolve, then the same
  problem on Dirac-3S.
- A classical copy of every quantum kernel tried. If the copy matches,
  the kernel has nothing to offer.
- A circuit with many non-Clifford gates, the kind a classical computer
  cannot simulate cheaply, tested against classical twins on every
  dataset before any hardware run (proposed, section 8).

## 6. Quantum advantage on real quantum computers

**In short:** no device run showed an advantage. The devices matched
exact classical answers, and on our problems the slow part of training
is a classical step, not the device.

### What our experiments showed

- [HW] **The full Phase 1 device campaign worked and showed no
  advantage.** Dirac-3 ran 61 fits with zero failures; the device agreed
  with an exact classical solve (`docs/paper/proposal.md`).
- [HW] **A more exact device did not change accuracy**, because the
  problem's exact answer was already known and reached classically
  (`docs/phase2/F142_DIRAC3S_VERIFY.md`).
- [SIM] **For the quantum-inspired model, the slow step is classical and
  it grows faster than the data, but only that step was measured.** On
  [ULB](#ds-ulb), building CVQBoost's pool of small models one processor at a time
  grew with a slope of about 1.4 against the number of rows (doubling the
  rows more than doubles the time), measured at 91 and 833
  variables between 17,023 and 170,235 rows. In the same runs the problem
  build grew in step with the rows (slopes 0.93 and 0.95) and the device
  step did not grow at all. Not measured: a build spread over many
  processors, other models, other datasets, or more rows
  (`docs/phase2/F110_SCALING.md`).

### What outside research says

- Proven quantum speedups are on built-for-purpose or code-breaking
  problems, and no exponential advantage is known for classical data
  (EvidenceBasedDB `cerezo-no-known-exponential-advantage-classical-data`,
  high).
- The speedup from Grover's search is quadratic (EvidenceBasedDB
  `qml-grover-quadratic-speedup-optimal`, high).

### What this means

- For card fraud on today's devices, a quantum advantage would need a
  problem where (1) a classical solver does measurably worse, (2) the
  device can resolve the difference, and (3) the difference changes how
  much fraud is caught. None of our problems met all three yet.
- The search space for an advantage is narrow but not empty: selection
  problems built from data summaries remain open.

## 7. Experiments planned

**In short:** Sprint 31 ran six planned experiments. None found a
quantum advantage. One gave a first estimate of the best any model can
do on [IEEE-CIS](#ds-ieee-cis), with a warning. Two device runs checked size and a
setting, not accuracy.

Sprint 31 ran these. Each design was written before its run, in
`experiments/phase2/PREREGISTRATION_DRAFT.md`. Each result, dated, is
under its design.
The six-experiment frame they fit into is in
`docs/phase2/PHASE2_POC_PLAN_DRAFT.md`.

- **A ceiling for the real datasets (F114).** Apply the one ceiling
  method that passed on the simulator to [ULB](#ds-ulb) and [IEEE-CIS](#ds-ieee-cis), after a
  shuffled-label check. Entry: the F108 entry's amendment of 2026-11-05.
  - Result, 2026-11-05: **no ceiling reported.** The shuffled-label check
    failed, and the estimator did not learn on [ULB](#ds-ulb) at its fixed settings:
    on nine seeds it scored worse than flagging nothing. The method has
    not yet been tested fairly on real data; what to do next is a
    decision for the team lead (Sprint 31 D11)
    (`experiments/phase2/results/f114_real_ceiling.json`).
  - Result of the re-run, 2026-11-05: the team lead chose to re-test
    the estimator at a slower learning rate. It passed on the
    simulator, and the shuffled-label check then passed, by a very
    small amount. For [IEEE-CIS](#ds-ieee-cis) the best error the data allows is
    estimated at about 2.5%, against the model's own 2.9%. That figure rests on an
    assumption, that the model's probabilities are well calibrated,
    which the check says does not hold here.
    The [ULB](#ds-ulb) estimate is far below an error the model actually
    reaches, so it is not a usable ceiling
    (`experiments/phase2/results/f114_real_ceiling_lr05.json`).
- **The circuit and its twins on more test frauds (F157, [QNN](#acr-qnn) part).**
  Rerun the 8-qubit circuit on [IEEE-CIS](#ds-ieee-cis)'s test month, which has about
  2,962 frauds, so "the twin copies the circuit" can be decided. Entry:
  the F106 entry's amendment of 2026-11-05.
  - Result, 2026-11-05: **the twin copies the circuit.** Two ordinary
    models, [GAM](#acr-gam) and [HGB](#acr-hgb), scored at least as well as the circuit on
    average over eight seeds (on a single seed either can be ahead), so the circuit shows nothing a classical model cannot
    do here (`experiments/phase2/results/f157_qnn_ieee.json`).
- **Seven algorithms on [SPECTRA](#ds-spectra)'s four datasets (F157, [SPECTRA](#ds-spectra) part).**
  Entry: "F157 [SPECTRA](#ds-spectra) part".
  - Result, 2026-11-05: **the boosted-tree models led on all four
    datasets, and the quantum-inspired model was never first.** By mean
    score it placed fifth or sixth of seven on every dataset. On
    oilgas_gasturbine and telecom_churn the [SVM](#acr-svm) scored reliably above
    it (0.8532 against 0.8394, and 0.8441 against 0.7254), and on
    maintenance_ai4i LightGBM did (0.6148 against 0.5387). Most neighbors
    in the order cannot be told apart. Every score uses the label with the
    planted quantum-friendly pattern (Appendix F). The [SVM](#acr-svm) here is the
    radial basis function form the design's rule chose, scored under a
    dated change to the design
    (`experiments/phase2/results/f157_spectra_algorithms_rbf.json`).
- **Routing one product type to the quantum-inspired model (Experiment
  5).** Does sending one product code of [IEEE-CIS](#ds-ieee-cis) to the quantum-inspired
  model add one point of recall at the 0.5% budget? The prediction is
  no. Entry: "Experiment 5".
  - Result, 2026-11-05: **no product type was accepted**, for the
    quantum-inspired model or for the classical check model. A lesson
    about the test itself: in every product type that could be scored, the best
    model's few allowed alerts are already all fraud, so no other model can beat it
    there (`docs/phase2/EXP5_ROUTER.md`).
- **Does Dirac-3S accept a 1,350-variable job (F155)?** One device call,
  approved on its own. Entry: "F155".
  - Result, 2026-11-05: **accepted.** The device took the
    1,350-variable job and returned 1,350 values, using 6.0 metered
    seconds. This is a size test only, by design: the problem
    was too flat for any answer to show quality, and no accuracy was
    read
    (`experiments/phase2/results/f155_variable_ceiling.json`).
- **Relaxation schedule 4 on Dirac-3S (F95).** Four fits; does a slower
  device setting close the small gap Dirac-3 left? Entry: "F95".
  - Result, 2026-11-05: **no change on the two fits that could be
    compared**, but those two problems are too easy to tell the
    settings apart, so this is weak evidence. The other two fits had
    no match on the same device. Each sample cost about three times
    the device time, and the card used 67.0 of its 120 approved
    seconds. Later plans keep the usual setting
    (`docs/phase2/F95_SCHEDULE4.md`).

## 8. Experiments not yet planned

**In short:** these are ideas, not scheduled work. The first group comes
from our evidence store. The second comes from the team lead's review of
this document (2026-11-06) and is proposed for the backlog in Sprint 31
decision D18. Each costs classical computer minutes unless noted.

From EvidenceBasedDB's memo
(`docs/spikes/F118_WHAT_THE_STORE_SAYS.md` in that repository, its
ranked list):

- **A rounding test**: round each selection problem's numbers to the
  device's 200:1 resolution and see whether the tiny classical gains
  survive. If they do not, no device run on that problem can show
  anything.
- **The same solver test on the first design's problems**, with a sweep
  of the penalty that sets how many items are picked.
- **An equal-feature comparison**: give the classical models the same 17
  features the quantum-inspired model used, to see whether feature
  choice explains its edge over linear models.
- **A classical copy of any quantum kernel**, and a sweep of kernel
  quality against qubit count from 2 to 14 qubits on fraud features.
- **Bank-scale timing**: classical training and scoring time at 1, 10
  and 100 million rows, beside the loading and shot cost a quantum step
  would pay.

From the team lead's review:

- **A study of the data fraud investigators use or could use**: what
  banks, card networks and investigators record, which fields the public
  datasets lack, and which of the suggestions in section 2 are lawful and
  available.
- **Alerts ranked by money saved**: choose the 0.5% of payments that
  save the most money after the cost of checking each alert, and compare
  with choosing by fraud count, on [ULB](#ds-ulb) and [IEEE-CIS](#ds-ieee-cis).
- **Card testing**: on [IEEE-CIS](#ds-ieee-cis), find small payments followed within a day
  by a large one on the same card key, count how often they are fraud,
  and test whether "small then large" fields catch more fraud.
- **A circuit with all three quantum properties and many non-Clifford
  gates**, in simulation first on [ULB](#ds-ulb), [IEEE-CIS](#ds-ieee-cis) and [SPECTRA](#ds-spectra)'s four datasets
  on the quantum-friendly label, against classical twins. A run on
  gate-based hardware would follow only if a circuit beats every twin,
  under its own approval, because such hardware is paid by use and adds
  [noise](#qc-noise).

## 9. Index: every dataset, model and platform we tested

**In short:** the lists below name every dataset, model and machine
behind the results above, each with its source. Appendix F describes the
datasets.

- **Datasets**: [ULB](#ds-ulb) card payments (`docs/phase2/algorithms/ULB_COMPARISON.md`);
  [IEEE-CIS](#ds-ieee-cis) card payments, split by month
  (`docs/phase2/algorithms/IEEE_COMPARISON.md`); [SPECTRA](#ds-spectra)'s four datasets:
  energy_steel, oilgas_gasturbine, telecom_churn and maintenance_ai4i
  (`docs/phase2/F109_TIER1_LADDER.md`); [UCI](#acr-uci) steel
  (`docs/phase2/F103_TIER1_CHECK.md`), the real-data check of [SPECTRA](#ds-spectra)'s
  screen; our fraud simulator with a known
  ceiling (`docs/phase2/F108_CEILING_VALIDATION.md`).
- **Classical models**: XGBoost, LightGBM, CatBoost, [HGB](#acr-hgb), logistic
  regression, linear [SVM](#acr-svm) and a radial basis function ([RBF](#acr-rbf)) alternative
  (`docs/phase2/algorithms/ULB_COMPARISON.md`); [GAM](#acr-gam), [GA2M](#acr-ga2m), the joint twin
  (`docs/F100_CLASSICAL_BAR.md`); random Fourier features ([RFF](#acr-rff))
  (`docs/phase2/F106_DEQUANTIZATION.md`); greedy search, simulated
  annealing, Solving Constraint Integer Programs ([SCIP](#acr-scip)) and exact
  enumeration
  (`docs/phase2/F176_BELOW_GREEDY.md`).
- **Quantum and quantum-inspired models**: CVQBoost on Dirac-3, Dirac-3S
  and its exact classical solve (`docs/phase2/F142_DIRAC3S_VERIFY.md`);
  the CVQBoost [KNN](#acr-knn) variant (`docs/phase2/F111_LOKE_PROTOCOL.md`); [QSVM](#acr-qsvm) on
  Dirac-3 (`docs/B4_B5_HARDWARE_RESULT.md`); an 8-qubit circuit, simulated
  (`docs/phase2/F106_DEQUANTIZATION.md`); a software copy of Dirac-3
  (`docs/phase2/F17_EMULATOR.md`).
- **Platforms**: QCi Dirac-3 and Dirac-3S; a NumPy [statevector simulator](#qc-statevector-simulator)
  on a laptop; a workstation for every classical run. No gate based
  hardware was used (`docs/phase2/F6_GATE_BASED_ARM.md`).

## Appendix A. Definitions

- <a id="def-device"></a>**Device**: in these documents, a quantum
  computer that runs our problems: QCi's Dirac-3 or Dirac-3S, which
  charge by the second of use ("metered seconds"). A customer's phone,
  computer or card terminal is written "customer device" instead;
  [IEEE-CIS](#ds-ieee-cis) records it in its DeviceType and DeviceInfo fields.
- <a id="def-evidence-tag"></a>**Evidence tag**: a mark on every result.
  [HW] means measured on quantum hardware; [SIM] means measured on a
  classical computer, simulations included; [PROJ] means projected, not
  measured.
- <a id="def-null-result"></a>**Null result**: a test that did not find
  the effect it looked for. It is still a result, and we report it.
- <a id="def-preregistration"></a>**Preregistration**: a written plan of
  what a test measures and what result would count against it, fixed
  before the test runs.
- <a id="def-falsifier"></a>**Falsifier**: the result, written down in
  advance, that would show a prediction wrong.
- <a id="def-repeat"></a>**Repeat**: one run of a test with its own random
  seed. We use 5 or 10 repeats so one lucky run cannot decide a result.
- <a id="def-reliable-difference"></a>**Reliable difference**: a
  difference between two models that passes the statistical test set in
  advance. Smaller differences may be chance.
- <a id="def-backlog-card"></a>**Backlog card**: a numbered work item,
  such as F142. Every result names its card.

## Appendix B. Acronyms

- <a id="acr-auprc"></a>**AUPRC**: area under the precision-recall curve.
  A score from 0 to 1 for how well a model ranks frauds above other
  payments; a random model scores the fraud rate.
- <a id="acr-auc"></a>**AUC**: area under the curve. Here, the receiver
  operating characteristic curve unless stated.
- <a id="acr-auroc"></a>**AUROC**: area under the receiver operating
  characteristic curve. A ranking score that looks good even when frauds
  are rare, so we prefer [AUPRC](#acr-auprc).
- <a id="acr-cnp"></a>**CNP**: card-not-present. A payment made without
  the physical card, online or by phone.
- <a id="acr-fn"></a>**FN**: false negative. A fraud the model missed.
- <a id="acr-fp"></a>**FP**: false positive. A legitimate payment the
  model flagged.
- <a id="acr-fpga"></a>**FPGA**: field-programmable gate array. A
  reprogrammable chip; Dirac-3 computes its couplings in one.
- <a id="acr-ga2m"></a>**GA2M**: generalized additive model with pairwise
  interactions. A [GAM](#acr-gam) that adds terms for pairs of features.
- <a id="acr-gam"></a>**GAM**: generalized additive model. A model that
  adds one simple curve per feature.
- <a id="acr-hgb"></a>**HGB**: histogram-based gradient boosting. The
  scikit-learn version of gradient boosting.
- <a id="acr-hsbc"></a>**HSBC**: Name, not an acronym, as used here. The
  bank that set the fraud challenge.
- <a id="acr-ieee-cis"></a>**IEEE-CIS**: Institute of Electrical and
  Electronics Engineers Computational Intelligence Society. Here, its
  public fraud dataset; see [the dataset entry](#ds-ieee-cis).
- <a id="acr-knn"></a>**KNN**: k-nearest neighbors. A model that scores
  a payment by the k most similar past payments.
- <a id="acr-mde"></a>**MDE**: minimum detectable effect. The smallest
  difference a test design can find with its stated power.
- <a id="acr-ml"></a>**ML**: machine learning.
- <a id="acr-pac"></a>**PAC**: probably approximately correct. A standard
  theory of how much data learning needs.
- <a id="acr-pca"></a>**PCA**: principal component analysis. A way to
  turn many features into fewer combined ones.
- <a id="acr-qc"></a>**QC**: quantum computing.
- <a id="acr-qml"></a>**QML**: quantum machine learning.
- <a id="acr-qnn"></a>**QNN**: quantum neural network. A trained quantum
  circuit used as a model.
- <a id="acr-qram"></a>**QRAM**: quantum random access memory. A
  proposed memory that loads classical data into qubits; none has been
  built at useful size.
- <a id="acr-qsvm"></a>**QSVM**: quantum support vector machine.
- <a id="acr-qubo"></a>**QUBO**: quadratic unconstrained binary
  optimization. A problem of choosing yes or no for each item to make a
  score as low as possible; the kind of problem Dirac devices solve.
- <a id="acr-rbf"></a>**RBF**: radial basis function. A common
  similarity measure used by support vector machines.
- <a id="acr-rff"></a>**RFF**: random Fourier features. A fast classical
  copy of a kernel.
- <a id="acr-scip"></a>**SCIP**: Solving Constraint Integer Programs. A
  free solver that can prove an answer is the best one.
- <a id="acr-sd"></a>**SD**: standard deviation. A measure of spread.
- <a id="acr-smote"></a>**SMOTE**: synthetic minority over-sampling
  technique. A way to add made-up fraud examples before training.
- <a id="acr-spectra"></a>**SPECTRA**: Name, not an acronym, as used
  here. A set of four public datasets, and a screening method, built so a
  quantum model could show a win; see [the dataset entry](#ds-spectra).
- <a id="acr-svm"></a>**SVM**: support vector machine. A model that draws
  the widest possible boundary between two classes.
- <a id="acr-tn"></a>**TN**: true negative. A legitimate payment the
  model passed.
- <a id="acr-tp"></a>**TP**: true positive. A fraud the model caught.
- <a id="acr-uci"></a>**UCI**: University of California, Irvine. Its
  machine learning repository holds public datasets.
- <a id="acr-ulb"></a>**ULB**: Universite Libre de Bruxelles. Here, its
  public credit card dataset; see [the dataset entry](#ds-ulb).

## Appendix C. Quantum computing

- <a id="qc-qubit"></a>**Qubit**: the basic unit of a quantum computer.
  Unlike a bit, it can hold a mix of 0 and 1 until it is measured.
- <a id="qc-superposition"></a>**Superposition**: the mix of 0 and 1 a
  qubit holds before measurement.
- <a id="qc-entanglement"></a>**Entanglement**: a link between qubits so
  that their measured values are related more strongly than classical
  objects allow.
- <a id="qc-interference"></a>**Interference**: waves adding or
  canceling. Quantum programs use it to make right answers more likely.
- <a id="qc-quantum-gate"></a>**Quantum gate**: one operation on one or
  two qubits.
- <a id="qc-quantum-circuit"></a>**Quantum circuit**: a sequence of
  gates followed by measurement.
- <a id="qc-shot"></a>**Shot**: one run and measurement of a circuit.
  Results are averages over many shots, so few shots give noisy answers.
- <a id="qc-noise"></a>**Noise**: errors from the hardware. It grows with
  circuit size.
- <a id="qc-statevector-simulator"></a>**Statevector simulator**: a
  classical program that computes a small circuit's result exactly.
- <a id="qc-hamiltonian"></a>**Hamiltonian**: the energy formula a
  device minimizes. Our training problems are written as one.
- <a id="qc-convex-problem"></a>**Convex problem**: an optimization
  problem with one best answer and no traps, which classical solvers
  solve exactly and fast.
- <a id="qc-greedy-search"></a>**Greedy search**: pick the best next item
  one at a time. Fast, and often good.
- <a id="qc-simulated-annealing"></a>**Simulated annealing**: a classical
  search that accepts some worse steps early to escape traps.
- <a id="qc-entropy-quantum-computing"></a>**Entropy quantum computing**:
  QCi's name for how its Dirac devices work: an optical loop with
  measurement and feedback that settles into low-energy answers.
- <a id="qc-dirac-3"></a>**Dirac-3**: QCi's optical optimization device,
  used in Phase 1.
- <a id="qc-dirac-3s"></a>**Dirac-3S**: QCi's newer device; the default
  for Phase 2 runs since 2026-10-16.
- <a id="qc-analog-resolution"></a>**Analog resolution**: how finely a
  device can tell two numbers apart. Dirac-3's guide states about 200:1.
- <a id="qc-quantum-advantage"></a>**Quantum advantage**: a quantum
  method doing a useful job better, faster or cheaper than the best
  classical method, shown by a fair test.
- <a id="qc-quantum-inspired"></a>**Quantum-inspired**: a method shaped
  for quantum hardware that can also run on classical solvers.
- <a id="qc-clifford-gate"></a>**Clifford gate**: a member of a common
  set of quantum gates. Circuits made only of these gates can still use
  superposition, entanglement and interference, and a classical computer
  can still simulate them quickly. Other gates, called non-Clifford, are
  what make a circuit hard to simulate.

## Appendix D. Machine learning

- <a id="ml-feature"></a>**Feature**: one input to a model, such as the
  payment amount.
- <a id="ml-label"></a>**Label**: the known answer for a past example:
  fraud or not.
- <a id="ml-test-fold"></a>**Test fold**: the part of the data kept out
  of training and used only to score the final model.
- <a id="ml-class-imbalance"></a>**Class imbalance**: one class (fraud)
  is far rarer than the other.
- <a id="ml-alert-budget"></a>**Alert budget**: the share of payments a
  bank can send for review, such as the top 0.5% by score.
- <a id="ml-recall"></a>**Recall**: the share of all frauds the model
  flags.
- <a id="ml-precision"></a>**Precision**: the share of flagged payments
  that are fraud.
- <a id="ml-decision-tree"></a>**Decision tree**: a model that asks a
  series of yes or no questions about features.
- <a id="ml-gradient-boosting"></a>**Gradient boosting**: many small
  decision trees, each fixing the errors of the ones before. XGBoost,
  LightGBM, CatBoost and [HGB](#acr-hgb) are versions of it.
- <a id="ml-logistic-regression"></a>**Logistic regression**: a model
  that adds weighted features and turns the sum into a probability.
- <a id="ml-ensemble"></a>**Ensemble**: a model made by combining many
  models' votes.
- <a id="ml-weak-learner"></a>**Weak learner**: one small model in an
  ensemble, only a little better than chance on its own.
- <a id="ml-hyperparameter-tuning"></a>**Hyperparameter tuning**:
  choosing a model's settings by trying them on data the test never sees.
- <a id="ml-data-leakage"></a>**Data leakage**: information from the test
  data reaching training, which makes scores look better than they are.
- <a id="ml-drift"></a>**Drift**: a change in the data over time, so a
  model trained on the past fits the present less well.
- <a id="ml-bayes-error"></a>**Bayes error**: the lowest error any model
  can reach with the features given. It is the ceiling on accuracy.
- <a id="ml-overfitting"></a>**Overfitting**: learning the training data
  so closely that the model does worse on new data.

## Appendix E. Quantum machine learning

- <a id="qml-cvqboost"></a>**CVQBoost**: a quantum-inspired ensemble. A
  device chooses the weight of each weak learner by solving one
  optimization problem.
- <a id="qml-exact-classical-proxy"></a>**Exact classical proxy**: the
  same training problem solved exactly on a classical computer, run
  beside the device as a control.
- <a id="qml-quantum-kernel"></a>**Quantum kernel**: a similarity
  measure between two examples computed with a quantum circuit.
- <a id="qml-classical-twin"></a>**Classical twin**: a classical model
  built to match what a quantum model can express, used to test whether
  the quantum model adds anything.
- <a id="qml-dequantization"></a>**Dequantization**: showing that a
  classical method does the same job as a quantum one about as well.
- <a id="qml-barren-plateau"></a>**Barren plateau**: a training landscape
  so flat that a circuit cannot learn.
- <a id="qml-data-encoding"></a>**Data encoding**: how features are
  turned into qubit settings at the start of a circuit.
- <a id="qml-learner-selection"></a>**Learner selection**: choosing a
  small set of weak learners or features, a yes or no problem that fits
  a quantum optimizer.

## Appendix F. Datasets

Each dataset is named in full the first time it appears in a document,
and by its short name after that. Both link here.

- <a id="ds-ulb"></a>**Credit card dataset of the Universite Libre de Bruxelles**:
  short name [ULB](#ds-ulb). 284,807 card payments made by European card holders
  over two days, 0.17% of them fraud, released by the university's
  machine learning group. Apart from time and amount, its fields are
  anonymous combinations of the original fields (principal components),
  so it carries no card, customer, merchant or customer device field. We
  split it 60/20/20 at random, once per seed, after removing 1,081 exact
  duplicates (`docs/paper/proposal.md`). Results:
  `docs/phase2/algorithms/ULB_COMPARISON.md`.
- <a id="ds-ieee-cis"></a>**Fraud detection dataset of the Institute of Electrical and Electronics Engineers Computational Intelligence Society**:
  short name [IEEE-CIS](#ds-ieee-cis). 590,540 card-not-present payments from the payment
  company Vesta, released for a public competition, 3.5% fraud. It has
  named fields: amount, a product code, masked card fields (card1 to
  card6), masked billing address and distance fields, the buyer's and
  recipient's email domains, counts and time gaps built by Vesta, and,
  for some payments, a customer device type and description and masked
  identity fields. We split it by month: train on earlier months, test
  on the next (`docs/paper/proposal.md`; the fields as read by
  `experiments/src/data.py`). Results:
  `docs/phase2/algorithms/IEEE_COMPARISON.md`.
- <a id="ds-spectra"></a>**Quantum-ready benchmark datasets**: short
  name [SPECTRA](#ds-spectra). Four public datasets released in 2026 by the authors of
  the [SPECTRA](#ds-spectra) screening method, each built from a real University of
  California, Irvine dataset: energy_steel (a steel plant's energy use),
  oilgas_gasturbine (a gas turbine's emissions), maintenance_ai4i
  (machine failures) and telecom_churn (customers leaving a telephone
  company). The real fields are rewritten as phases (angles), the form a
  quantum circuit takes in. Each has two labels: `target_real`, the real
  outcome, and `target`, the real outcome plus a planted pattern inside
  one group of rows, the "pocket" (flagged by `in_pocket`), built so a
  quantum model could win there. The `target` label is the
  quantum-enhanced one, and every [SPECTRA](#ds-spectra) result in these documents uses
  it; `target_real` has not been run. A result on `target` is benchmark
  performance, not a claim about real behavior (`docs/references.md`,
  items 2 and 3). None of the four is fraud data. Results:
  `docs/phase2/algorithms/` (one page per dataset and model).
- <a id="ds-uci-steel"></a>**Steel dataset of the University of California, Irvine**:
  a public steel dataset used once, to check that our copy of the
  [SPECTRA](#ds-spectra) screen gives the published answer (`docs/phase2/F103_TIER1_CHECK.md`).
- <a id="ds-simulator"></a>**Fraud simulator**: our own simulated card
  payments, built from the fraud patterns in [ULB](#ds-ulb)'s authors' handbook
  (compromised terminals and customers). Because we wrote the rules, we
  know the best score any model can reach on it, which makes it a test
  bed for methods (`experiments/phase2/PREREGISTRATION_DRAFT.md`, the
  F108 entry; `docs/phase2/F108_CEILING_VALIDATION.md`).
