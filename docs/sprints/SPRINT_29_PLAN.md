# Sprint 29 Plan: Make the Tools Repeatable, Then Find the Best Each Model Can Do

**Sprint**: 29 | **Branch**: `feature/20261025_Sprint_29`
**Planned**: 2026-10-25 | **Status**: DRAFT, Decisions 1-3 answered
2026-10-26 (option 1 each); Decision 4, approval, open
**Scope**: F159, F164, F156, F160, F166, F158, F165 and F167 (team lead
selection, 2026-10-25), and the pypdf bump (Decision 2, 2026-10-26)
**Metered Dirac seconds**: **0**. No task calls a device or a paid
service.

## Objective

Make every new Phase 2 result safe to resume and parallel to build, check
the Phase 2 documents' figures against their evidence, and take the first
measurements of four questions: the best each algorithm reaches on ULB,
a ceiling estimator not tied to one model, room for Experiment 3 on a
second dataset, and whether removing fraud types helps.

- **F165 first**: every new module this sprint writes its result through
  `provenance.write_result`; F165 makes a resumed run keep its id.
- **F159 next**: F166 and F160 build pools; the parallel build makes the
  833-variable proxy lane affordable.
- **F166, F156, F160, F158**: each writes its entry before any score.
- **F164**: the figure check for `docs/phase2/` (Decision 1).
- **F167**: the full PoC plan drafted on stated assumptions.

## Decisions already made (team lead, 2026-10-25)

- **Scope**: as above. F155, F102, F157's other datasets, F161, F95 and
  F13 itself were not selected.
- **F167**: "Make a copy so that we can draft what this will look like
  and assign to this sprint", said of F13. Read as: a new card, F167,
  that drafts the full PoC plan now in a new file,
  `docs/phase2/PHASE2_POC_PLAN_DRAFT.md`, with every assumption about the
  brief labeled. F13 and the skeleton stay unchanged until notification.
  Approval confirms this reading.
- **F164's stopping rule** (Pass 2 recommendation, selected): measure the
  match rate first; if more than 200 distinct values do not match,
  re-size before building. It was measured at planning, and it fires
  (Decision 1).
- Priorities: the slate's numbers stand. Task order is by dependency.

## Pre-kickoff (Phase 2)

- Sprint 28 merged to `develop` (PR #46, `346fbfd`) and released to `main`
  (PR #62). The branch is `develop` plus the two refinement commits and
  this plan. No `sprint` issue is open.
- Working tree clean before this plan. The full suite passed on
  `595f9dd` (2026-10-25).
- Dependency scan, 2026-10-25: `pip-audit` on the lock file finds three
  advisories in **pypdf 6.21.1** (CVE-2026-115572, CVE-2026-115585,
  CVE-2026-115580), all fixed in 6.21.2. This repository reads only its
  own rendered PDFs with pypdf. Decision 2. `pip list --outdated` shows
  other minor releases, none with an advisory; none is proposed.

## Plan-to-branch-state verification (3.2.2.1)

Each card was checked against the repository, the installed packages and
the files it names on 2026-10-25. Probes were scratch scripts, zero
metered, not evidence. **Five cards cannot run as carded.** Each
correction replaces the card's text in this plan, and the card is
corrected in the same commit as the task that meets it.

- **F165: confirmed.** No module calls `write_result` yet
  (`provenance.py` and its test only), so every Sprint 29 module is the
  first user. The sidecar is plain text, not `json.dumps`, so
  `test_result_writer_required.py`'s scan does not count it and its
  frozen table does not change. A fresh clone (CI, another machine) has
  no sidecar, so a rerun there still states `replace=`; that is correct.
  `.gitignore` already ignores `experiments/phase2/results/*.heartbeat`;
  the sidecar gets its own rule, checked with `git check-ignore` first.
- **F159: one card claim corrected; the primitive proven.**
  - `full_pair_pool.build_full` exists and builds serially. The card's
    "check the pool equals `build_full`'s" must compare **held-out rows**.
    Two seeded builds with different seeds agree exactly on the training
    rows and differ on validation rows (F145's finding, reproduced: free
    cell, 10% of ULB training rows, seeds 42 and 43 differ on 6.1e-5 of
    validation entries; seed 42 twice, identical).
  - Spike: a spawn-based `ProcessPoolExecutor` (4 workers) trains the 91
    learners and returns them intact; its validation H equals the serial
    build's exactly. At 10% rows it took 3.45 s against 1.8-2.2 s serial,
    so process start-up and data copying matter at small sizes.
  - This machine reports 32 logical processors (`os.cpu_count()`), so 32
    workers is the card's top count.
- **F164: the carded design cannot meet its own acceptance.**
  - The card's method is one global value pool (F44's). The tracked result
    files hold 145,445 numbers. Rounded to the quoted places, they cover
    **100% of the 2-place grid and 99.4% of the 3-place grid** in [0, 1).
    So a global pool accepts almost any figure quoted to 1-3 places: 528
    of the 835 distinct decimals outside code in `docs/phase2/`.
  - The card's own example shows it: **0.829** (the wrong endpoint)
    resolves in the global pool. In a **per-document pool**, built only
    from the result files that document names, 0.829 does not resolve and
    0.828 does (`F111_LOKE_PROTOCOL.md`).
  - Counts. Global pool, at quoted rounding: 72 distinct values
    unresolved; restricted to figures with 4 or more places, 30 of 307.
    Per-document pools: **211 distinct values unresolved** (264
    figure-document pairs). Four documents name no result file
    (`DIRAC_3S_RESEARCH.md`, `DIRAC_3S_SITE_SWEEP.md`, the PoC skeleton,
    the README); their figures are sourced from documents, not results.
  - **The approved stopping rule fires**: 211 is above 200. Decision 1
    re-sizes the card.
  - **The acceptance is restated.** Of the seven Sprint 28 findings the
    card names, one is a decimal (0.829). The others are an integer
    wall-clock figure (95 minutes), an integer label ("776 of 950"), and
    four prose claims (a clamp cause, a failing reason, a scope, P1
    listed open). A figure check cannot see prose, and integers are
    outside F44's decimal rule. So the acceptance is: 0.829 put back
    fails, proven red; the other six are named as out of this check's
    reach.
- **F156: the pass rule needs a width term.** F108's rule for an interval
  method is "the interval contains the Bayes error". On
  `f108_ceiling.json`'s main arm the trivial interval [0, test fraud
  rate] passes that rule on **5 of 5 seeds**, so a vacuous estimator
  would pass. The entry adds: the interval's width is at most twice the
  point margin, `2 x max(0.0005, 0.10 x Bayes error)`, about 0.0012 here.
  The trivial interval (width about 0.008) then fails on 5 of 5. Noted,
  not re-scored: F108's Cover-Hart intervals (width 0.0058-0.0063) also
  fail the width term. Training rows are about 880,000-900,000 per seed
  in 3 features; a divergence bound such as Henze-Penrose needs a minimum
  spanning tree, so the entry fixes a subsample (all training positives
  and a stated number of negatives) and a pilot on one seed sizes it.
- **F160: new preparation needed, and no positive case exists.**
  `qubo_proxy._prep` is ULB-only and `exp3_controls` builds ULB pools, so
  F160 needs an IEEE-CIS preparation: one F105 fold
  (`ieee_harness.folds_for`), the top features chosen on its training
  rows, pools at F94's two instance sizes (60 choose 10, 136 choose 25),
  H on held-out rows. F153's rule (gap at least 0.01) has **never passed
  on any recorded instance**: across F153's 25 recorded gaps the largest
  is 0.0026. So F160 adds a positive control (below).
- **F166: runtime and two lane forms set here.**
  - The house 60/20/20 split, tuning on each seed's own validation fold
    and scoring on its test fold, meets section 2 of the Phase 2 draft
    ("nested cross-validation where tuning and evaluation share data"):
    no score comes from the rows that chose its configuration.
  - **SVM**: an RBF kernel on about 170,000 training rows is quadratic
    and is not run at full size. The lane is a linear SVM on all rows; an
    RBF SVM on a stated stratified subsample is the alternative tried.
  - **Proxy**: the three `qubo_proxy` configurations (free, mid, full),
    dct learners, seeded. The full cell is 833 variables, about 13
    minutes per serial build (F110, measured); F159's parallel build is
    why F166 runs after F159.
  - **Dominant term**: the classical tuning loop. Sizing: 6 classical
    algorithms x 8 configurations x about 25 s per fit at ULB's training
    size (F151's HGB fits, Sprint 28 plan) is about 20 minutes per seed,
    plus about 5 minutes for the proxy with the parallel build, so about
    25 minutes per seed. **Inferred**: XGBoost, LightGBM and CatBoost fit
    times on ULB are not recorded in Phase 2 files. Seed 42 runs first,
    timed, and sets the seed count (Decision 3).
- **F158: the simulator hides one type from its own features.** F108's
  generator records each row's type (`hidden_s2`, a compromised terminal;
  `hidden_s3`, a compromised customer). Its model sees only amount, the
  customer mean and time, so terminal fraud cannot be seen through those
  features. A per-type detector needs features that reveal its type
  (terminal history from earlier days, with a label delay). With those
  features F108's Bayes posterior no longer bounds the models, so F158
  does not use F108's ceiling. Types can overlap (a row can be both).
- **F167: confirmed.** The skeleton exists (101 lines) and its dates are
  sourced. Two of its lines are stale (the Experiments table's states as
  of 2026-10-22, and "the open QCi question"); F167's draft carries the
  current state and the skeleton is not edited.

### Show each threshold can fire (Sprint 25 IMP-2, Sprint 28 IMP-5)

- **F159, pool equality on validation rows.** Reference where it should
  fail: seeds 42 and 43 differ on 6.1e-5 of entries, so the check is not
  vacuous. Measured (scratch).
- **F164, per-document resolution.** Reference: 0.829 fails and 0.828
  passes in F111's pool; in the global pool both pass. Measured
  (scratch).
- **F156, the two terms.** Containment: the trivial interval passes it on
  5 of 5 seeds, so containment alone cannot fail. Width: the trivial
  interval fails it on 5 of 5. One test per term, in which only that term
  fails, each proven red.
- **F160, the room rule.** It has failed on every recorded instance and
  never passed. **First run that shows it can pass**: a positive control
  at the same instance sizes, an H from random-sign learners (no subset
  fits the labels), where greedy should stay well above the floor. If the
  control also shows no room, the rule cannot pass and is redesigned
  before any IEEE-CIS reading.
- **F158, the primary comparison.** No data yet. **First run that shows
  it**: the cascade on shuffled type labels, which should not beat one
  model on everything. If it does, the gain is not from the types.
- **F165, the three terms.** A resume with its sidecar continues without
  `replace=`; a copied id with no sidecar is refused; a different run's
  id is still refused. One test per term, each proven red.
- **F166**: descriptive; no pass or fail. Any ranking on the comparison
  page uses section 2's paired test. The reference that such a test can
  fire is Sprint 28's (XGBoost full against matched13 on ULB, 10 seeds).
- **F167**: descriptive, no threshold.

## Tasks

The table shows Decisions 1-3 as answered (option 1 each, team lead,
2026-10-26); the alternatives not taken stay stated under each decision.

| Task | Card | What | Est | Runtime | Depends on |
|---|---|---|---|---|---|
| A | F165 | Run-id sidecar beside each result, read on resume; `write_result` refuses a copied id with no sidecar; ignore rule; three tests, each proven red | 60 | - | - |
| B | F159 | Spawn-based parallel pool build; equality on validation rows against `build_full`; timed at 1, 4, 8, 16 and 32 workers at F110's four row fractions, 833-variable cell; longest single learner reported | 60 | ~40 (serial builds about 24 at the four fractions; parallel runs add about 10-15) | A |
| C | F164 | Per Decision 1: per-document pools; the 211 values resolved, corrected or registered with a reason; 0.829 proven red | 270 | ~1 | - |
| D | F156 | Entry with the width term; Henze-Penrose bound on a stated subsample, pilot on one seed; F108's harness, seeds and margin unchanged | 90 | ~10 (pilot first) | A |
| E | F160 | Entry; IEEE-CIS pools at F94's two sizes on one F105 fold; greedy, SCIP (300 s cap) and the floor; the positive control first | 75 | ~40 (SCIP up to 6 x 5 min; pool builds a few minutes) | A, B |
| F | F166 | Entry; seven algorithms tuned per seed on validation (8 configurations each; linear SVM, RBF subsample as the alternative); one document per algorithm and the ULB comparison page | 240 | per Decision 3: seed 42 first (~25), then the seed count | A, B |
| G | F158 | Entry; step 3 (frauds every stored model misses, from F154's files), then step 1 (per-type cascade on the simulator with type-revealing features, against one model; the shuffled-label reference); step 2 only if step 1 shows a gain | 150 | ~20 (simulator generation and HGB fits) | A |
| H | F167 | `docs/phase2/PHASE2_POC_PLAN_DRAFT.md` | 60 | - | - |
| I | none (Decision 2) | pypdf 6.21.1 to 6.21.2 in the lock and both venvs, with the lock header line; the PDF tests before and after | 45 | - | - |

**Derived total as answered: 1,050 minutes of work**, the
sum of the nine task estimates (60 + 60 + 270 + 90 + 75 + 240 + 150 + 60 +
45). Decision 3 changes runtime only. One conditional addition is not in the total: if G's step 1
shows a gain, step 2 adds about 60.

Runtime is separate. B's, D's, E's, F's and G's runs go to the
background, each with a heartbeat file before any run over 30 minutes. A
full suite run takes about 12 minutes.

How each estimate was set (`docs/VELOCITY_LOG.md` read first; Sprints
26-28):

- **Research+code (B, D, E, F, G)**: the measured research+code rows of
  Sprints 26-28 ran at 0.13-0.73 of estimate, median about 0.35. Each
  card is sized to its first decisive measurement: B 60 (the card's; the
  primitive is proven); D 90 (the card's; one estimator, the width term
  added); E 75 (the card's 45 plus 30 for the IEEE-CIS preparation and
  the positive control); F 240 (the card's); G 150 (the card's, with step
  2 conditional).
- **Tooling (A, I)**: Sprints 26-28 tooling rows ran at 0.04-1.67. A 60
  (the card's); I 45 (Sprint 28's same bump took 2 minutes against 45;
  kept, because the PDF tests run before and after).
- **Verification (C)**: 270, about 1 minute per unresolved value to trace
  it to its file, correct the document or register it, plus 60 for the
  per-document resolver and its tests. No history for this step type.
- **Docs (H)**: 60 (the card's).

**Allowances**: none carried. Writing (F's eight documents, H, and four
entries and result documents) is about 260 of 1,050 minutes, under a
third. Verification (C) is about 270 of 1,050, about a quarter; it does
not dominate.

### Task order

1. **A** (F165) first: every later task writes through `write_result`.
2. **B** (F159) next: E and F build pools with it.
3. **F** (F166) after B, seed 42 timed first, then the run in the
   background. **E** (F160) after B, its positive control first.
4. **D** (F156) and **G** (F158) after A, runs in the background.
5. **C** (F164), **H** (F167) and **I** (pypdf) while runs go.

### Task A detail (F165)

- `provenance.run_id_for(path)` (or the same behavior under another name
  set in the task): creates the id and its sidecar,
  `<result>.run_id`, at the run's start; on resume returns the recorded
  id. `write_result` refuses an id that matches the recorded result's but
  has no matching sidecar.
- **Acceptance**: the three terms above, each proven red with
  `assert_can_fail`; the sidecar ignored (`git check-ignore`, checked
  before the first one is written); `CLAUDE.md`'s provenance rule names
  the resume path.

### Task B detail (F159)

- New module under `experiments/phase2/src/`: the parallel build returns
  the same classifier object `build_full` returns, so `qubo_proxy.h_matrix`
  reads it unchanged. `full_pair_pool.py` gains nothing that changes its
  serial behavior.
- **Acceptance**: equality with the serial build on validation rows at
  every fraction (the test proven red); speed-up against workers; the
  longest single learner, the floor any number of processors reaches.

### Task C detail (F164, Decision 1 option 1)

- A per-document resolver for `docs/phase2/*.md`: each document's figures
  resolve against the tracked result files it names, at the quoted
  rounding; F44's extraction rules (code spans excluded) and its timing
  exclusion reused. A registry with a reason per entry; a document that
  names no result file registers its figures with their source.
- Each of the 211 values is resolved, corrected in its document (a wrong
  figure), or registered. Corrections are listed at Manual Validation.
- **Acceptance**: 0.829 put back fails, proven red; the registry-unused
  check, as in F44; the six non-decimal findings named as out of reach;
  F44's stated limit kept (a figure that exists in a cited file but is
  quoted in the wrong place is not caught).

### Task D detail (F156)

- Entry first (a dated amendment to F108's, as F114's was): the
  estimator (a Henze-Penrose bound from the Friedman-Rafsky statistic on a
  minimum spanning tree, Berisha et al.), the subsample, and the pass rule
  with both terms. F108's generator, seeds, arms and margin imported
  unchanged.
- **Acceptance**: pass or fail on the main arm under both terms, 4 of 5
  seeds; one test per term, each proven red. If it passes, F114 is
  unblocked (its real-data run is not in this sprint).

### Task E detail (F160)

- Entry first. The positive control at both sizes, then the IEEE-CIS
  instances (seeds 42-44, as F153), greedy, SCIP and the floor.
- **Acceptance**: the control's gap reported first; the gap per instance
  under F153's rule; a pass reopens F25's design (a card, not this
  sprint).

### Task F detail (F166)

- Entry first: the seven algorithms, each with its 8 configurations
  named before any score; per-seed tuning on validation; the test-fold
  metrics F157 names (TP, FP, TN and FN at the 0.5% alert budget and at
  the validation-chosen threshold, precision, recall, specificity, F1,
  MCC, balanced accuracy, AUC-PR, ROC-AUC) with intervals over seeds;
  every row with its outcome block.
- **Acceptance**: seven documents under `docs/phase2/algorithms/` and one
  ULB comparison page, each figure resolving to the result file (C's
  resolver checks them); rankings only under section 2's paired test.

### Task G detail (F158)

- Entry first: the types (S2, S3, overlap handled as stated), the
  type-revealing features, the cascade, the single model, the alert
  budget, the shuffled-label reference, and the primary comparison
  (recall at the 0.5% budget, cascade minus single model, paired over
  seeds).
- **Acceptance**: step 3's characterization; step 1's primary comparison
  with its interval and the reference beside it; step 2 run or not, with
  the reason.

### Task H detail (F167)

- Audience: the team lead, who must see what the PoC plan will look like
  after notification. The PoC window split into sprints; each experiment
  placed with its entry, its device block and the decision that releases
  it; the items that wait for the brief, each with its assumption
  labeled.
- **Acceptance**: every date sourced; every assumption labeled; no figure
  restated that another file owns.

### Task I detail (pypdf, Decision 2 option 1)

- Bump to 6.21.2 in `experiments/requirements-lock.txt` and both venvs,
  with a dated line in the lock header (rule 5).
- **Acceptance**: the PDF tests (`test_submission_artifacts.py`,
  `test_published_artifacts.py`, `test_requirements_complete.py`) run
  before and after; pip-audit shows no pypdf finding; no tracked PDF
  rebuilt.

## Decisions

**Answered 2026-10-26 by the team lead: Decision 1 option 1, Decision 2
option 1, Decision 3 option 1** ("D1 1 d2 1 d3 1"). The options are kept
below as asked.

**Decision 1. F164's scope** (the approved stopping rule fired at
planning: 211 distinct values unresolved under per-document pools, above
200).

1. Per-document pools, as Task C above: the 211 values resolved,
   corrected or registered; 0.829 proven red. C is 270; the sprint is
   1,050. (Recommended: the only option that catches a wrong figure
   quoted to 1-3 places, which is where the Sprint 28 finding was.)
2. One global pool as carded, checking only figures with 4 or more places
   (30 of 307 unresolved); the 528 figures with 1-3 places listed as
   unchecked, with the reason; 0.829 not caught, stated. C is 90; the
   sprint is 870.
3. F164 leaves this sprint and returns to the backlog, re-sized at 270,
   Priority 25. C is removed; the sprint is 780.

**Decision 2. pypdf 6.21.2** (three advisories in 6.21.1).

1. Add Task I (45 minutes) to this sprint.
2. Do not add it; card it in the backlog at Priority 60.

**Decision 3. F166's seed count** (runtime only; the work estimate does
not change).

1. Seed 42 first, timed; the seed count set from its time with a
   120-minute runtime cap, as F162 did. At about 25 minutes per seed
   (inferred) that is 4-5 seeds; rankings then use the paired bootstrap,
   with the Wilcoxon test secondary. (Recommended: the cap keeps the run
   readable inside the sprint.)
2. Ten seeds (42-51) in the background whatever the time, so the Wilcoxon
   test can reach its alpha; about 250 minutes of runtime (inferred).

**Decision 4. The plan**: approve Tasks A-I at 1,050 minutes, zero
metered seconds. Open.

## Risks

- **F164 corrects documents.** Each correction is listed at Manual
  Validation; a document of record (`docs/paper/`, `docs/submission/`,
  the frozen preregistration) is never touched.
- **Runtimes partly inferred.** F166's per-fit times and F156's spanning
  tree are unmeasured; each runs a pilot first; no unsized run starts.
- **F158's features are new.** Type-revealing features use earlier days'
  labels; a label delay is stated in the entry to keep the future out.
- **Local-only files.** F166 and F158 read the gitignored ULB data and
  F154's prediction files on this machine; their tests skip in CI where
  the files are absent.
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
- Manual Validation items, including F164's corrections, are listed on
  screen and saved in `SPRINT_29_VALIDATION.md`.
- Retrospective, `SPRINT_29_SUMMARY.md` at Sprint 30 planning, and the
  velocity log rows from measured start times.
