# Sprint 28 Plan: Experiment Entries First, Then Their First Measurements

**Sprint**: 28 | **Branch**: `feature/20261019_Sprint_28`
**Planned**: 2026-10-21 | **Status**: DRAFT, awaiting the team lead's
approval.
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

## Pre-kickoff (Phase 2)

- Sprint 27 merged to `develop` (PR #32, `220a461`) and released to `main`
  (PR #45, `efe9641`). The branch is `develop` plus three refinement
  commits. Issues #33-44 are closed; no `sprint` issue is open.
- Working tree clean before this plan. Full suite run 2026-10-21: one
  failure, being identified by a second run; the result is recorded here
  before approval.
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
  audits; the harness and its no-score test are unchanged. Other findings:
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
  every date unconfirmed.
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
| B | F152 | Experiment 2 entry; new scoring module over F105's folds; classical lanes, 5 seeds, 3 folds; proxy lane per Decision 2 | 130 | ~45 (20 fixed + 10-25 classical, unverified) + proxy pilot | - |
| C | F153 | Experiment 3 entry; Hamiltonian on held-out predictions with a ridge sweep; greedy, SCIP and the floor; the resolution check per Decision 1; the probe quote | 150 | ~30 (SCIP per instance, F94 measured; one-instance pilot first) | - |
| D | F111 | Experiment 4 entry; their stated protocol (random 70/30, SMOTE on train, [0, 1] scaling, KNN k = 15, schedule 2, lambda 0) and ours, 10 seeds, same lane | 130 | ~30 (KNN on full ULB about 2.5 min per seed; SMOTE adds rows) | A |
| E | F110 | Experiment 6 entry; pool build plus solve time at 10, 25, 50 and 100% of ULB training rows | 100 | free cell ~12 (5 seeds); 833-variable cell ~23 per seed, so a 1-seed pilot first and 5 seeds only if projected at 120 or less | - |
| F | F154 | One confusion-count table for every result that has them; pairwise catch-and-miss at the alert budget; subset interaction (amount band, day) under the rewritten rule | 130 | ~5 | A |
| G | F114 | Per Decision 3 | 60 | ~3 (F108 measured 115 s for 5 seeds) | - |
| H | F150 | Per Decision 4 | 30 | - | - |
| I | F115 | `docs/phase2/F115_INTEGER_COST_SCALING.md`; the fit computed by a new script with a test | 45 | - | - |
| J | F13 | `docs/phase2/PHASE2_POC_PLAN.md` skeleton; dates marked unconfirmed | 75 | - | - |
| K | F146 | Drafts per Decision 5; `QCI_CORRESPONDENCE_HASHES.md`'s stale line cite corrected; `DIRAC_UNDERSTANDINGS.md` revision row | 45 | - | - |

**Derived total: 945 minutes of work**, the sum of the 11 task estimates
(50 + 130 + 150 + 130 + 100 + 130 + 60 + 30 + 45 + 75 + 45), with
Decisions 1-5 at their recommended options. Decision 6's recommended
option adds Task L (45), for **990**. Each other option's total is on the
option. One conditional addition is not in the total: if G's method
passes F108's rule, F114's real-data run adds 90.

Runtime is separate. B's, C's, D's and E's runs go to the background, each
with a heartbeat file before any run over 30 minutes. A full suite run
takes about 10 minutes.

How each estimate was set (`docs/VELOCITY_LOG.md` read first; Sprint 27
rows):

- **Research+code (A-G)**: Sprint 27's six measured research+code rows ran
  at 0.07-0.73 of estimate, median about 0.34. Each card is sized to its
  first decisive measurement: A 50 of the card's 90 (the probe already
  found the candidate); B 130 of 240 (entry, a scoring module, classical
  lanes); C 150 of 240 (130 plus 20 for the resolution check); D 130 of
  240; E 100 of 180; F 130 (the card's figure); G 60 (one method).
- **Docs (H-K)**: Sprint 27's docs rows ran at 0.06-0.07, but drew on
  sweeps already done. H 30, I 45 (30 plus the fit script and its test),
  J 75 (the timebox), K 45 (30 per update plus two drafts).

**Allowances**: none carried. Writing (the four entries, about 120, plus
H-K, 195) is about 315 of 945 minutes, a third; verification does not
dominate.

### Task order

1. **A** (F151) first: D and F read ULB against it.
2. **B** (F152), **C** (F153) and **E** (F110): entries first, then runs in
   the background.
3. **D** (F111) and **F** (F154) after A.
4. **G** (F114), **H** (F150), **I** (F115), **J** (F13) while runs go.
5. **K** (F146) last, so it can carry I's correction if Decision 5 says so;
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

- The entry records every choice the paper leaves open. Their protocol and
  ours on the same lane (the CVQBoost-KNN proxy), 10 seeds (42-51).
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
- **Acceptance**: the table committed with its source per row; the
  pairwise counts per seed; any subset claim only under the rewritten
  rule; a null reported as plainly as a find; the F154 card's segment
  wording corrected.

### Task G detail (F114, Decision 3 option 1)

- The F108 entry gains a dated amendment before the run: an
  isotonic-calibrated plug-in (HGB, calibrated on a held-out slice of
  train) with `max_bins` set, against the same rule on the main arm.
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

- Calendar (unconfirmed), one row per experiment (card, entry, device,
  quoted seconds, state), sprint cadence, the Dirac-3S default, the F6
  gate-based arm, confidentiality on receipt of the brief, and the items
  that wait for notification.
- **Acceptance**: every date labeled with its source or unconfirmed; no
  figure restated that another file owns.

### Task K detail (F146, Decision 5 option 1)

- Audience: QCi's eqc-models contact and the support contact. Two drafts:
  P1 restated for the eqc-models contact, and a reply to the review offer,
  with I's correction as an optional paragraph.
- **Acceptance**: both pass `scripts/outward_readability.py`; saved in the
  gitignored `docs/qci_package/`; listed at Manual Validation for the team
  lead to send or change.

## Decisions at approval

Each is independent of the others, and each option names its total. The
totals in Decisions 1-5 exclude Task L; add 45 if Decision 6 is option 1.

**Decision 1. F153's resolution check**

1. Add an opt-in `device_resolution.resolution_check_guide(J, C)` that
   reports the max/min ratio and the share of coefficient pairs that meet
   eq. 5; F153 reports it beside F104's gate; F104's gate and Phase 1 are
   unchanged; the F104 card gains the difference. Total 945.
   (Recommended)
2. F153 uses F104's gate only, and records the difference from the guide.
   Total 925.

**Decision 2. F152's CVQBoost proxy lane on IEEE-CIS**

1. A one-fold timed pilot at Phase 1's 100,000-row subsample, through a
   Phase 2 wrapper; three folds only if projected at 60 minutes or less,
   otherwise the pilot timing is the result. Total 945. (Recommended)
2. Classical lanes only this sprint; the proxy lane stays on the card.
   Total 925.

**Decision 3. F114**

1. Validate one new method on F108's harness this sprint: the
   isotonic-calibrated plug-in with `max_bins` set (Task G, 60). The real
   data run (90) only if it passes. Total 945. (Recommended)
2. No F114 work this sprint; it stays blocked. Total 885.

**Decision 4. F150**

1. Draft the construction request for you to send (Task H, 30); the
   rebuild waits for the reply. Total 945. (Recommended)
2. No F150 work this sprint. Total 915.

**Decision 5. F146's drafts**

1. Draft P1 for the eqc-models contact and a reply to QCi's review offer,
   with F115's correction as an optional paragraph (Task K, 45). Total 945.
   (Recommended)
2. Draft P1 only. Total 925.

**Decision 6. pypdf 6.20.0 advisories**

1. Add Task L: bump pypdf to 6.21.1 in the lock and both venvs, with the
   lock header line; the PDF tests run before and after (45). Total 990.
   (Recommended)
2. Card it for the backlog (F155, Priority 50). Total 945.

**Decision 7. F143's hold** (independent of the plan; F143 is not in
scope). It waited for QCi to confirm the cloud queue exceeds 949
variables. QCi named the configuration (base unit plus expansion, whose
guide ceiling is 9,980) but gave no variable figure.

1. The hold is met: F143 becomes a candidate at Priority 150; its metered
   run still needs per-block approval.
2. Keep the hold until QCi states a variable figure.

**Decision 8. The plan**

1. Approve the plan as written, with Decisions 1-6 applied.
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
