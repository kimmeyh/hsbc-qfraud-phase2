# Sprint 28 Plan: Experiment Entries First, Then Their First Measurements

**Sprint**: 28 | **Branch**: `feature/20261019_Sprint_28`
**Planned**: 2026-10-21 | **Status**: DRAFT, revised 2026-10-22 from the
team lead's answers to Decisions 1-6; Decisions 7 and 8 open. Draft PR #46.
**Scope**: F151, F152, F153, F111, F110, F154, F150, F114, F115, F13 and
F146 (team lead selection, 2026-10-21)
**Metered Dirac seconds**: **0**. No task calls a device. No task calls a
paid AWS service. F153 ends with a quote for a later, separate approval.

## Objective

Write the Phase 2 entries for Experiments 2, 3, 4 and 6 before the
November filing, and take each one's first zero-metered measurement.

- **F151 first**: explain the unstable ULB HGB comparator, because F111
  and F154 read ULB results against it.
- **F152, F153, F111, F110**: each writes its section 6 entry in
  `experiments/phase2/PREREGISTRATION_DRAFT.md`, then runs.
- **F154**: confusion counts for every saved result, and where models
  differ by subset, to answer the ensemble question.
- **F114, F150**: both are blocked. Each gets the in-sprint step that can
  unblock it (Decisions 3 and 4).
- **F115, F13, F146**: documents and drafts.

## Decisions already made (team lead, 2026-10-21)

- **Scope**: as above. F102, F95, F143, F25 and F30 were not selected.
- **F143**: not selected, so it stays on HOLD. Its hold question is
  re-asked once below (Decision 7), separate from the plan.
- Priorities: the slate's numbers stand (F151 20, F152 22, F153 24, F111
  26, F110 28, F154 32, F150 41, F114 140, F115 170, F13 180, F146 HOLD).
  Task order below is by dependency, not by number.

## Decisions made 2026-10-22 (team lead)

- **Decision 1**: option 1. Opt-in `resolution_check_guide` beside F104's
  gate.
- **Decision 2**: option 2. Classical lanes only; F152's proxy lane stays
  on the card. B drops from 130 to 110.
- **Decisions 3, 4 and 5**: option 1 each (Tasks G, H and K as written).
- **Decision 6**: option 1. Task L (pypdf to 6.21.1) added.
- **F154 goes first, and becomes a standing rule.** "Please do first and
  ensure all future experiments (ML/QML...) compute and record these
  values (this sprint and future sprints)." Task F gains a shared recorder,
  a guard and the written rule (Task F detail); F rises from 130 to 190.
- **F111's protocol source**: the team lead named two local repositories:
  the unchanged clone of the Loke repository and his test copy of it. What
  they settle, and what they do not, is in Task D detail.
- **F13's dates**: the team lead supplied a screenshot of the program
  roadmap page (`quantumai.thequantuminsider.com/program/`), 2026-10-22.
  Phase II PoC runs 17 Nov 2026 to 28 Feb 2027; Review and Close runs
  1 Mar to 30 Apr 2027; winners are announced 30 April 2027. Task J cites
  the page and the capture date instead of marking the dates unconfirmed.
- **Decision 7**: the team lead asked for more information; it is restated
  below with it. **Decision 8** is open.

## Pre-kickoff (Phase 2)

- Sprint 27 merged to `develop` (PR #32, `220a461`) and released to `main`
  (PR #45, `efe9641`). The branch is `develop` plus three refinement
  commits. Issues #33-44 are closed; no `sprint` issue is open.
- Working tree clean before this plan. Full suite, 2026-10-21: the first
  run (with `-x`) stopped on one failure whose name its captured tail did
  not show; a second full run, without `-x`, had no failure. The first
  failure is not identified and did not reproduce. The first run overlapped
  four verification agents reading the same data and prediction files; the
  second ran alone (context, not a diagnosis).
- Dependency scan: `pip-audit` (through `uvx`) on the lock file, 2026-10-21,
  finds three advisories in **pypdf 6.20.0**: CVE-2026-113792 and
  CVE-2026-113793 (crafted PDF causes an infinite loop in outline
  operations; fixed in 6.20.1) and CVE-2026-113786 (a crafted `/DCTDecode`
  image reaches an image parser; fixed in 6.21.1). This repository reads
  only its own rendered PDFs with pypdf (`test_submission_artifacts.py`,
  `check-page-limits.py`, `page-fill-report.py`, `render_pdf.py`). Decision
  6 asks whether the bump joins this sprint.

## Plan-to-branch-state verification (3.2.2.1)

Each card was checked against the repository, the installed packages and
the sources it names on 2026-10-21. **Seven cards cannot run as carded.**
Each correction below replaces the card's text in this plan, and the card
is corrected in the same commit as the task that meets it.

- **F151: one card claim corrected; a candidate cause found.**
  - The three setups differ. F130: the deduplicated ULB, 60/20/20
    stratified, 170,235 training rows at 0.17% positives, MI top-13, AUPRC.
    F109: a 30,000-row subsample, 6 phase features, and **ROC-AUC, not
    AUPRC**, so its "HGB strongest" cannot be compared with F130. F106: all
    positives plus 6,000 negatives (6,295 rows), 8 phase features, AUPRC
    SD 0.027. All use `HistGradientBoostingClassifier` defaults.
  - Early stopping (`"auto"`) is on above 10,000 rows (scikit-learn 1.9.0),
    so on for F130 and F109, off for F106. It is not the whole cause: F130's
    "no early stopping" row is stable (SD 0.020) but at 0.219 AUPRC, and its
    300-iteration row without early stopping has SD 0.207.
  - "Unstable under every setting tried" is wrong for "no early stopping".
  - **Candidate cause (scratch probe, zero metered, not evidence)**: HGB's
    default `l2_regularization=0`. With 1.0 on F130's exact preparation:
    five seeds 0.776-0.838, mean 0.806, SD 0.022. `min_samples_leaf=200`
    stays unstable (SD 0.246). Inferred mechanism: at 0.17% prevalence a
    mostly-positive leaf has a tiny Hessian sum, so the leaf value
    `-G/(H+0)` is large. Task A records this as a controlled change.
- **F152: the execution step needs new code.** `ieee_harness.py` computes
  no score by design: it has a pilot and an audit subcommand, no lanes,
  and `test_ieee_harness.py:111-121` fails if the module names a metric.
  So the scoring goes in a new module that imports the harness's folds and
  audits; the harness and its no-score test, which scans only `ieee_harness.py` (`inspect.getsource`), are unchanged. Other findings:
  - Section 6 lists Experiment 2 as "To write". Section 2 makes
    floor-normalized AUPRC primary (the card said AUPRC) and requires at
    least 5 seeds for a headline (the card named none).
  - With 3 folds an exact Wilcoxon test cannot go below p = 0.25, so the
    primary interval is the paired bootstrap of section 2.
  - The CVQBoost proxy on IEEE-CIS exists only in Phase 1's
    `run_ieee_cvqboost.py`, which writes `experiments/results/` (rule 3).
    Its KNN build did not finish one fold in 84 minutes at full size;
    Phase 1 used a 100,000-row subsample whose runtime is not recorded.
    Decision 2 sets this lane.
  - F105's facts hold: about 20 minutes per three-fold pass
    (`docs/phase2/F105_IEEE_HARNESS.md:51-54`), the adversarial control at
    its cap with AUC 0.945, 0.888 and 0.887, and month 6's 8,111 rows.
- **F153: F104's gate differs from the guide.** The Dirac-3S User Guide
  Rev A section 5.3 (p.18, evidence library copy) gives two conditions over
  all terms: max/min of the coefficients at most 200, and (eq. 5) two
  distinct terms resolve only if their difference is at least max/200.
  `device_resolution.resolution_gate` (lines 72-120) uses the max/200 step
  but applies it to each block's whole spread (max minus min), which is
  much weaker than the pairwise test, and it omits the max/min ratio on
  purpose (its docstring, lines 98-103). QCi's A7 answer points at that
  ratio. Whether A7 means C alone or every term is ambiguous. Decision 1
  sets what F153 uses.
  - F94's findings hold (`docs/phase2/F94_EXP3_CONTROLS.md`): the floor is
    `-1 + 2/m`; every method reaches it on the training fold; the ridge
    term carries over 99.67% of the objective at `lambda = 2 * rows`.
    `pyscipopt` 6.2.1 (SCIP 10.0) imports.
  - The probe quote can only be a bracket. F139's probes cost 28 s and
    165 s on Dirac-3 (193 s). No Dirac-3S integer-solver time exists;
    F142's Dirac-3S/Dirac-3 ratio ran 0.4-1.3 on the continuous solver, so
    the quote is about 80-250 s, **inferred**.
- **F111: the paper is on disk; three gaps and one card claim.**
  - Loke et al., ICAART 2026 (DOI 10.5220/0014628400004052), read from the
    evidence library's PDF. It states: rows with missing values removed,
    no deduplication mentioned; features scaled to [0, 1]; a random 70/30
    split, 10 runs; SMOTE on the training fold only; the test fold
    resampled into validation and evaluation subsets; KNN weak learners
    (k = 15); schedule 2, lambda 0. The 0.80 is CVQBoost-KNN, **0.8108**
    mean over 10 seeds (Tables 3 and 4).
  - Not stated: the seeds, stratification, the SMOTE ratio and neighbors,
    the validation/evaluation ratio, which subset AUC-PR is scored on,
    what the scaler is fit on. Each choice is recorded in the entry before
    the first run.
  - "Their comparator" (CAD, 0.7423) is cited from another paper, not run
    on their split. It can be cited, not replicated.
- **F110: no row-count timing exists.** F29 built its pool once at full
  rows. Dominant term: the weak-learner pool build, 735.4 s at 833
  variables (`SPRINT_12_PLAN.md`; the source of the hardware plan's "12
  minutes of CPU per fit") and about 76 s for the free cell. Whether the
  735.4 s build was sequential or full-pair is unverified.
- **F154: one rule rewritten, one wording corrected.**
  - `store.save_predictions` exists (`store.py:182`); the confusion counts
    are `metrics.summarize()`'s `operating_points` key, not a function.
    `F113_ORACLE_GAP.md` exists. 131 files: 80 classical, 30 proxy, 21
    hardware, as carded.
  - "The segments the proposal names" has no referent: `proposal.md` names
    none; the frozen preregistration names Sparkov and IEEE-CIS cohorts, not
    ULB. On ULB the subsets are amount band and time (day 1, day 2).
  - The files carry no row index. The split is recovered exactly by
    deduplicating before `data.stratified_split(df, seed)`; checked on all
    10 seeds (56,746 test rows, 95 frauds each).
  - The acceptance rule as carded fires on noise (below).
- **F114: blocked, as carded.** F108 validated none of its four methods on
  the main arm (HGB plug-in 2 of 5 seeds, overstating by 5-12%; the
  learning-curve floor 1 of 5 on error and on 1 - AUPRC; Cover-Hart 3 of
  5). The pass rule is 4 of 5. F108's own write-up names a calibrated model
  under the plug-in as a next candidate. Decision 3.
- **F150: blocked, as carded.** The checklist's construction request
  (`CHECKLIST-Phase2.md:64-65`, team-lead owned) is unticked, and nothing
  in the repository shows it was sent. F103's entry fixed the four choices
  the paper leaves open (coupling distribution, Trotter scheme, field
  order, label threshold), plus the row count and field screen; "joint
  ratio 9.9" is undefined in the paper. Decision 4.
- **F115: confirmed; a second location found.** The wrong sentence is
  `HARDWARE_PLAN_PHASE_2.md:160`. The fit (`vars^0.75 x levels^0.52`) has
  no code in the repository; it reproduces from `integer_probe.json` by a
  log-log least squares (0.747, 0.518, R^2 0.953). The hardware plan is
  FINAL (team lead, 2026-09-27) and is not a Class 4 document. The same
  wording is at `INTEGER_PROBE_RESULT.md:70`, where levels grew with
  variables, so it is true in context and is not edited. **The wrong
  sentence is in the hardware-plan PDF sent to QCi** (read from the copy in
  `docs/qci_package/`; that PDF is not hash-pinned, so it is the filed copy,
  not proven to be the bytes sent).
- **F13: one date claim is unverified.** "Nov 17 - Feb 28" has no primary
  source in the repository; the guidelines PDF says notification and the
  PoC start are mid-November 2026, with no end date. The skeleton marks
  every date unconfirmed. **Settled 2026-10-22**: the team lead's
  screenshot of the program roadmap page gives 17 Nov 2026 to 28 Feb 2027
  (see "Decisions made 2026-10-22").
- **F146: confirmed.** P1 is open (referred to the eqc-models contact);
  QCi's offer to review our report is recorded with no reply. Drafts go in
  the gitignored `docs/qci_package/` (`.gitignore:68`).
  `QCI_CORRESPONDENCE_HASHES.md` cites `.gitignore:62`, which is stale.

### Show each threshold can fire (Sprint 25 IMP-2)

- **F154, the subset rule.** Run on XGBoost full against XGBoost matched13
  (10 seeds, data on disk), recall at the 0.5% alert budget. That pair
  differs overall: +0.0126, t interval [+0.0021, +0.0232]. The carded rule
  ("a subset claim with a paired interval that excludes zero") **fires on
  day 1** (+0.0185 [+0.0074, +0.0295]) because the overall difference
  carries into the subset. Over 1,000 random half-splits it fired 31.2% of
  the time. **Rewritten**: a subset claim needs the interaction, in-subset
  difference minus complement difference, with a t interval over seeds
  that excludes zero after the section 2a Bonferroni correction. On the
  same pair the interaction does not fire (amount -0.0020 [-0.0262,
  +0.0222]; time +0.0122 [-0.0210, +0.0454]) and fires on 3.8% of random
  splits, near the nominal 5%. One fraud is 1.7-2.9 recall points inside
  these subsets.
- **F151, "the spread closes".** A change closes the spread only if the 5
  seeds have SD at most 0.03 AND range at most 0.10 AND a mean within 0.03
  of Phase 1's XGBoost matched13 on the same split (0.816 on seeds 42-46).
  On F130's recorded rows: the default (SD 0.170) fails; "no early
  stopping" (SD 0.020, mean 0.219) passes the spread terms and **fails the
  level term**, which is why the level term is there. XGBoost matched13
  itself is SD 0.019, range 0.050.
- **F111, the 0.80 target.** A tolerance of 0.03 around 0.8108 is also met
  by lanes that are not their method: our CVQBoost proxy dct cell under our
  protocol (0.793, results.json) and XGBoost (0.802 and 0.830). So
  "reproduces 0.81" cannot show that the protocol matters. The entry
  reports it as "consistent with", and the result is the paired difference
  between their protocol and ours on the same lane, with its interval.
- **F152, the per-fold interval.** No IEEE-CIS score exists. **First run
  that shows it**: one lane on two seeds; the paired interval between the
  seeds must include zero, or the interval is too narrow for seed noise.
- **F114 (if Decision 3 option 1)**: F108's rule already fails three of
  four methods; the new method faces the same rule on the main arm.
- **F153**: F94 showed every solver reaches the floor on the training
  fold, so the first held-out instance is checked for a gap between greedy
  and the floor before any comparison is read.
- **F110, F115, F13, F146, F150**: descriptive, no threshold.

## Tasks

| Task | Card | What | Est | Runtime | Depends on |
|---|---|---|---|---|---|
| A | F151 | One-setting controlled changes on F130's exact ULB preparation (`l2_regularization`, then early stopping); the stable reference recorded; F130's ULB reading re-stated or left void | 50 | ~10 (5 seeds per setting, about 25 s per fit) | - |
| B | F152 | Experiment 2 entry; new scoring module over F105's folds; lanes HGB (F151 settings), logistic regression, XGBoost and LightGBM, 5 seeds, 3 folds (GAM, GA2M and the JOINT twin stay on the card: unsized on IEEE-CIS's 400-plus features); no proxy lane (Decision 2) | 110 | ~45 (20 fixed + 10-25 for the four lanes, from Phase 1's 10-18 s GBM fits per fold, unverified) | F |
| C | F153 | Experiment 3 entry; Hamiltonian on held-out predictions with a ridge sweep; greedy, SCIP and the floor; the resolution check per Decision 1; the probe quote | 150 | ~30 (SCIP per instance, F94 measured; one-instance pilot first) | - |
| D | F111 | Experiment 4 entry; their stated protocol (random 70/30, SMOTE on train, [0, 1] scaling, KNN k = 15, schedule 2, lambda 0) and ours, 10 seeds, on the CVQBoost-KNN proxy, with F151's stable HGB as the reference under both | 130 | ~30 (KNN on full ULB about 2.5 min per seed; SMOTE adds rows) | A |
| E | F110 | Experiment 6 entry; pool build plus solve time at 10, 25, 50 and 100% of ULB training rows | 100 | free cell ~12 (5 seeds); 833-variable cell ~23 per seed, so a 1-seed pilot first and 5 seeds only if projected at 120 or less | - |
| F | F154 | First. One confusion-count table for every result that has them; pairwise catch-and-miss at the alert budget; subset interaction (amount band, day) under the rewritten rule; a shared recorder, a guard and the written rule so every later experiment records the same values | 190 | ~5 | - |
| G | F114 | Per Decision 3 | 60 | ~3 (F108 measured 115 s for 5 seeds) | - |
| H | F150 | Per Decision 4 | 30 | - | - |
| I | F115 | `docs/phase2/F115_INTEGER_COST_SCALING.md`; the fit computed by a new script with a test | 45 | - | - |
| J | F13 | `docs/phase2/PHASE2_POC_PLAN.md` skeleton; dates cited to the program roadmap page | 75 | - | - |
| K | F146 | Drafts per Decision 5; `QCI_CORRESPONDENCE_HASHES.md`'s stale line cite corrected; `DIRAC_UNDERSTANDINGS.md` revision row | 45 | - | - |
| L | none (Decision 6) | pypdf 6.20.0 to 6.21.1 in the lock and both venvs, with the lock header line; the PDF tests run before and after (Decision 6) | 45 | - | - |

**Derived total: 1,030 minutes of work**, the sum of the 12 task
estimates (50 + 110 + 150 + 130 + 100 + 190 + 60 + 30 + 45 + 75 + 45 +
45), with Decisions 1-6 as answered on 2026-10-22. One conditional
addition is not in the total: if G's method passes F108's rule, F114's
real-data run adds 90.

Runtime is separate. B's, C's, D's and E's runs go to the background, each
with a heartbeat file before any run over 30 minutes. A full suite run
takes about 10 minutes.

How each estimate was set (`docs/VELOCITY_LOG.md` read first; Sprint 27
rows):

- **Research+code (A-G)**: Sprint 27's six measured research+code rows ran
  at 0.07-0.73 of estimate, median about 0.34. Each card is sized to its
  first decisive measurement: A 50 of the card's 90 (the probe already
  found the candidate); B 110 of 240 (entry, a scoring module, classical
  lanes; the proxy pilot's 20 removed by Decision 2); C 150 of 240 (130
  plus 20 for the resolution check); D 130 of 240; E 100 of 180; F 190
  (the card's 130 plus 60 for the recorder, its guard proven red and the
  written rule); G 60 (one method).
- **Docs (H-K)**: Sprint 27's docs rows ran at 0.06-0.07, but drew on
  sweeps already done. H 30, I 45 (30 plus the fit script and its test),
  J 75 (the timebox), K 45 (30 per update plus two drafts).
- **Dependency (L)**: 45, a lock change with the PDF tests before and
  after.

**Allowances**: none carried. Writing (the four entries, about 120, plus
H-K, 195) is about 315 of 1,030 minutes, under a third; verification does
not dominate.

### Task order

1. **F** (F154) first (team lead, 2026-10-22): its recorder and guard
   exist before any other task writes a result, so every result this
   sprint records the values.
2. **A** (F151) next: D uses its stable HGB as the reference.
3. **B** (F152), **C** (F153) and **E** (F110): entries first, then runs in
   the background.
4. **D** (F111) after A. **L** (pypdf) at any point.
5. **G** (F114), **H** (F150), **I** (F115), **J** (F13) while runs go.
6. **K** (F146) last, so it can carry I's correction if Decision 5 says so;
   presented at Manual Validation.

### Task A detail (F151)

- `f130_levers._prep` reused unchanged; HGB with `l2_regularization` 1.0,
  then each early-stopping setting moved one at a time, 5 seeds (42-46).
  New script under `experiments/phase2/src/`, rows to
  `experiments/phase2/results/` with evidence tag `SIM`.
- **Acceptance**: the cause named and shown by one setting moved under the
  "spread closes" rule above; the stable reference recorded with its
  seeds; F130's ULB reading re-stated against it or left void with the
  reason; F109's ROC-AUC difference noted; a test, proven red.

### Task B detail (F152)

- The entry: lanes; floor-normalized AUPRC primary, raw AUPRC and AUROC
  beside it; the paired bootstrap; the family (section 2a); 5 seeds; the
  drift treatment (a stated limit, or a higher cap, written before any
  score); month 6 included or excluded, written before any score.
- New `experiments/phase2/src/f152_exp2_score.py` imports the harness's
  folds and audits; `ieee_harness.py` and its no-score test unchanged.
- **Acceptance**: the entry committed before the first score; per-fold
  scores with intervals; the drift treatment applied as written; the
  two-seed interval check run first.

### Task C detail (F153)

- The entry, then the Hamiltonian on held-out predictions with a ridge
  sweep (F94: the data term must matter); greedy, SCIP and the floor per
  instance; the resolution check per Decision 1 on the chosen instances.
- The quote: F139's two probes on Dirac-3S, a bracket of about 80-250 s,
  labeled inferred, for a separate approval.
- **Acceptance**: the entry before the build; the gap between greedy and
  the floor reported; the resolution result; the quote.

### Task D detail (F111)

- **The Loke repository** (team lead, 2026-10-22). Read only, never
  written: the local clone, its committed `0092a38` (2026-05-22), and the
  upstream `main` (`39a3443`, 2026-05-29) and `integrate-additional-datasets`
  (`2ac7d77`, 2026-10-17) branches through the GitHub API. Findings:
  - **The clone is not as-is.** Its working tree has uncommitted changes
    (`main.py`, `README.md`, `requirements.txt`; the README carries an
    "HK How to Run" section), and it lags upstream by 2 commits on `main`.
    The committed and upstream versions were read instead.
  - **It is not the paper's code.** It starts 2026-05-19, after the
    ICAART 2026 paper, and compares XGBoost with hybrid XGBoost; its
    default weak learner is XGBoost, not KNN. The October branch adds a
    KNN catalog (k of 3, 5, 11, 21), none at the paper's k = 15. So it
    shows the first author's own practice, not proof of the paper's
    settings. The entry says so.
  - **Seeds**: drawn by `random.randint(0, 100000)` on each run and
    logged; no fixed list exists. The paper's 10 seeds are unrecoverable.
    We use 42-51 and say why.
  - **Split**: `train_test_split(test_size=0.3, stratify=y, random_state=seed)`,
    so stratified. The test fold is split again into validation and
    evaluation, 33/67, stratified (`0092a38`). AUC-PR is scored on the
    evaluation part. The scaler is `MinMaxScaler`, fit on train only.
    `main` removed the validation split on 2026-05-29.
  - **SMOTE**: SMOTETomek, not plain SMOTE, on the training fold only,
    `k_neighbors = min(10, positives - 1)`, `random_state = seed`. Off by
    default. Target positive ratio 0.02 in May, 0.05 in October.
  - **Missing values**: `dropna()`. No deduplication, as the paper says.
- **Our use**: their protocol runs with the code's split and SMOTETomek
  at ratio 0.02 (the version nearest the paper) as primary, 0.05 as a
  sensitivity row, KNN k = 15 from the paper. Each choice is in the entry
  before the first run.
- The entry records every choice the paper leaves open. Their protocol and
  ours on the same lane (the CVQBoost-KNN proxy), 10 seeds (42-51), with
  F151's stable HGB run under both protocols as the reference.
- **Acceptance**: their figure reported as consistent or not, with the
  tolerance stated as unable to separate lanes; the paired protocol
  difference with its interval; CAD cited, not run.

### Task E detail (F110)

- Pool build, Hamiltonian construction and solve timed separately at four
  row fractions, free cell 5 seeds; the 833-variable cell pilot, then 5
  seeds only if projected at 120 minutes or less.
- **Acceptance**: time against rows per component, with the slope; the
  "about 2 s" claim in the literature (`evidence-inventory.md:71`) set
  beside the measured build time.

### Task F detail (F154)

- The table from `results.json` and the Phase 2 hardware files; the
  pairwise counts from the 131 local files, the split recovered by
  deduplicating first; the interaction rule above.
- **The standing rule** (team lead, 2026-10-22: every future experiment,
  ML or QML, this sprint and later, computes and records these values):
  - New `experiments/phase2/src/outcome_record.py`: the confusion counts
    (TP, FP, TN, FN) at the alert budget and at the experiment's own
    threshold, and the per-row test scores saved to a gitignored local
    file with its SHA-256 in the result row, so any two models can be
    compared case by case later.
  - New guard `experiments/phase2/src/test_outcome_record_required.py`:
    every result file under `experiments/phase2/results/` that holds a
    test score must hold both. Files that exist on the day it lands are
    listed by name as exempt, and the list can only shrink. Proven red.
  - The rule written in `docs/SPRINT_PROCESS.md`, in the Phase 2 draft's
    reporting section, and as one standing-rule line in `CLAUDE.md`.
  - Metered hardware rows are covered by the same guard; this sprint has
    none.
- **Acceptance**: the table committed with its source per row; the
  pairwise counts per seed; any subset claim only under the rewritten
  rule; a null reported as plainly as a find; the F154 card's segment
  wording corrected; the recorder used by every later task this sprint;
  the guard proven red.

### Task G detail (F114, Decision 3 option 1)

- The F108 entry gains a dated amendment before the run: an
  isotonic-calibrated plug-in (HGB, calibrated on a held-out slice of
  train) using F151's candidate settings (`l2_regularization=1.0`, `early_stopping=False`, `max_bins` at its default 255), against the same rule on the main arm.
- **Acceptance**: pass or fail under F108's rule. If it passes, F114's
  real-data run (ULB, IEEE-CIS) follows (90); if not, F114 stays blocked
  with the reason.

### Task H detail (F150, Decision 4 option 1)

- A request to the SPECTRA authors listing each construction choice F103
  fixed itself, and the undefined joint ratio. Saved in a new gitignored
  `docs/spectra_package/`; the ignore rule is written and checked with
  `git check-ignore` before the file. The send is the team lead's.
- **Acceptance**: the draft passes `scripts/outward_readability.py`; it is
  listed at Manual Validation.

### Task I detail (F115)

- Audience: QCi and anyone reading the hardware plan, who must take cost
  as sublinear in variables at fixed levels. The new document states the
  correct reading, the fit from code, and why the FINAL document is not
  edited.
- **Acceptance**: the script reproduces the exponents from
  `integer_probe.json`; its test proven red; the hardware plan and its
  guard unchanged.

### Task J detail (F13)

- Calendar from the program roadmap page (team lead's screenshot,
  2026-10-22): PoC 17 Nov 2026 to 28 Feb 2027, Review and Close 1 Mar to
  30 Apr 2027. One row per experiment (card, entry, device,
  quoted seconds, state), sprint cadence, the Dirac-3S default, the F6
  gate-based arm, confidentiality on receipt of the brief, and the items
  that wait for notification.
- **Acceptance**: every date labeled with its source and capture date; no
  figure restated that another file owns.

### Task K detail (F146, Decision 5 option 1)

- Audience: QCi's eqc-models contact and the support contact. Two drafts:
  P1 restated for the eqc-models contact, and a reply to the review offer,
  with I's correction as an optional paragraph.
- **Acceptance**: both pass `scripts/outward_readability.py`; saved in the
  gitignored `docs/qci_package/`; listed at Manual Validation for the team
  lead to send or change.

### Task L detail (pypdf, Decision 6 option 1)

- pip-audit found pypdf 6.20.0 affected by CVE-2026-113792 and
  CVE-2026-113793 (fixed in 6.20.1) and CVE-2026-113786 (fixed in
  6.21.1). Bump to 6.21.1 in `experiments/requirements-lock.txt` and both
  venvs, with a dated line in the lock header (rule 5).
- **Acceptance**: the PDF tests (`test_submission_artifacts.py`,
  `test_published_artifacts.py`, `test_requirements_complete.py`) run
  before and after; pip-audit shows no pypdf finding; no tracked PDF
  rebuilt.

## Decisions

**Decisions 1-6** were answered on 2026-10-22; the answers are in
"Decisions made 2026-10-22" above and applied in the tasks.

**Decision 7. F143's hold** (independent of the plan; F143 is not in
scope, and no option changes the sprint total).

- **What F143 is**: telecom_churn (a SPECTRA dataset) with all 18
  features, 987 variables, schedule 3, 5 seeds, on Dirac-3S. B4 ran it on
  Dirac-3 at 816 variables with `age` dropped, because Dirac-3 stops at
  949. Its in-segment edges were negative. F143 asks whether the dropped
  feature changes that.
- **Why it is held**: the Dirac-3S base module also stops at 949. Only
  base plus one expansion module reaches 9,980 (guide Table 2). No source
  said which one serves the cloud queue, so a 987-variable job might not
  fit.
- **What QCi said on 2026-10-20 (A1)**: base unit plus expansion module
  serves the cloud `dirac-3s` queue. Under Table 2 that is 9,980, so 987
  fits. **Inferred**: QCi named the configuration, not a number.
- **Cost if it runs later**: at least 450 metered seconds (Dirac-3 cost
  84-90 s per fit at 816 variables). `qpu_cost_model.quote(987, 8)` flags
  987 as above its largest Dirac-3S anchor, so its high figure is a floor.
  Every block still needs your per-block approval (Criterion H).
- **What a wrong inference costs**: one rejected or failed first fit. The
  first approved block can be a single fit. Whether a rejected job is
  metered is **unverified**.

1. The hold is met. F143 becomes a backlog candidate at Priority 150; it
   is not added to Sprint 28. (Recommended: the vendor's answer and its
   own guide table agree, and a wrong inference costs one fit.)
2. Keep the hold until QCi states a variable figure; no question is sent.
3. Keep the hold, and Task K's reply to QCi asks one line: "Does the
   cloud `dirac-3s` queue accept a 987-variable continuous job?" Task K
   stays at 45.

**Decision 8. The plan**

1. Approve the plan as revised on 2026-10-22: 12 tasks (A-L), 1,030
   minutes, F154 first, zero metered seconds.
2. Do not approve yet. I revise it from your comments and present it
   again.

## Risks

- **Entries written in one sprint.** Four entries bind the November
  filing. Each is written before its run and is revisable until filing.
- **Runtimes partly unmeasured.** The IEEE-CIS proxy and the 833-variable
  timing run pilots first; no unsized run starts.
- **F151's cause is a probe.** A recorded run can still disagree; the
  rule above decides.
- **Shared code** (`device_resolution`, Decision 1) is opt-in, with Phase 1
  behavior the default (rule 4). `test_evidence_immutability.py` and
  `test_document_figures_resolve.py` are the check.
- **Local-only files.** F154 and F111 read the gitignored predictions and
  ULB data on this machine; their tests skip in CI where the files are
  absent.
- **External sends.** H and K are drafts; every send is the team lead's.
- **CI goes red between this plan and approval.**
  `test_phase3_artifacts.py` requires the PR, issues and approval once the
  status is `phase_3_planning`. That red is expected.
- **Session continuity.** Every decision and finding lands in a committed
  file.

## Model assignments

Main loop for all tasks. Long runs and the suite run in the background,
each writing to a named file that is read in full when it finishes.

## Definition of Done

- Every task's acceptance criteria, as corrected above, are met.
- Each new test is proven to fail before it is trusted.
- The full suite passes locally, and CI is green on the final HEAD.
- Manual Validation items, including the H and K drafts, are listed on
  screen and saved in `SPRINT_28_VALIDATION.md`.
- Retrospective, `SPRINT_28_SUMMARY.md` at Sprint 29 planning, and the
  velocity log rows from measured start times.
