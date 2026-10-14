# Sprint 26 Plan: Reach Dirac-3S, Measure It, and Make the Proxy Repeatable

**Sprint**: 26 | **Branch**: `feature/20261013_Sprint_26`
**Planned**: 2026-10-13 | **Status**: APPROVED 2026-10-14 (team lead): Decision 1 option 1,
Decision 2 option 1, Decision 3 option 1; 700 minutes. Draft PR #21.
Issues: A #22, B #23, C #24, D #25, E #26, F #27, G #28, H #29.
**Scope**: F141, F142, F144, F147, F145, F146, F105 and F126 (team lead
selection, 2026-10-13)
**Metered Dirac-3S seconds**: about 172, cap 360, all in F142. **Plan
approval does not approve them.** Each block stops for its own approval
with its call count and seconds (Criterion H).

## Objective

Take the first Dirac-3S measurements, and make the classical proxy they are
compared against repeatable.

- **F141, then F142**: reach Dirac-3S, then price it and check it against
  Dirac-3 on a problem it can resolve.
- **F145, then F144**: make a pool build repeatable from its seed, then
  build the proxy twin of B2's configuration on it.
- **F147, F126, F105**: three items that need no device. A query tool over
  the evidence library; a model of the device's sparsity; the Experiment 2
  harness.
- **F146**: keep `docs/phase2/DIRAC_UNDERSTANDINGS.md` current as F141 and
  F142 report.

## Decisions already made (team lead, 2026-10-13)

- **Scope**: as above. F104 and the F102 increment, both in the
  recommended set at refinement, were not selected. F142 depends on both
  (see Decision 1).
- Priority numbers unchanged: F141 7, F142 8, F144 9, F147 10, F145 11,
  F105 60, F126 101, F146 HOLD (permanent). Task order below is by
  dependency, not by number.

## Pre-kickoff (Phase 2)

- Sprint 25 merged to `develop` (PR #12, `e8d8bab`) and released to `main`
  (PR #20). `git log origin/develop..HEAD` is empty apart from this
  branch's Pass 1 commit. Issues #13-19 are closed. Working tree clean.
- Full suite passed on 2026-10-13, before this plan's edits.
- Dependency scan: `pip-audit` (run through `uvx`) on the lock file finds
  no known vulnerability, 2026-10-13. The only planned bump is F141.

## Plan-to-branch-state verification (3.2.2.1)

Each card was checked against the repository and the installed packages on
2026-10-13.

- **F141: confirmed, and one card claim corrected.** PyPI has
  `qci-client` 5.0.3 (uploaded 2026-10-05) and `eqc-models` 0.22.1
  (2026-10-07). From the 0.22.1 wheel: `QciClientSolver.__init__` takes
  `sampler_type`, whose only allowed value is `dirac-3s`. `Dirac3CloudSolver`
  and `Dirac3IntegerCloudSolver` inherit it. The card said 0.22.1 replaces
  `generation`; it does not. `generation` stays a class attribute, default
  `None`, and is appended to the device name when set. The card is
  corrected. 0.22.1 requires `lightgbm>=4.6`, which the lock already has
  (4.7.0). `get_dynamic_range` is still in 0.22.1. **The WSL venv must be
  bumped too**: every metered fit runs under WSL
  (`scripts/wsl_hw.sh` uses `/root/eqc-venv`), and that venv holds
  `eqc-models` 0.21.0 and `qci-client` 5.0.2. A bump to the Windows venv
  alone would pass F141's dry run and fail F142.
- **F145: the diagnosis was reproduced once.** The `free` pool for seed 42,
  built twice on Windows with the sequential build: the training rows
  (`H_tr`) are byte-identical; the validation and test rows differ. On test,
  61 of 78 learners differ, on 327 of 4,426,188 cells. That fits the card's
  first hypothesis. `qubo_proxy.py` builds `DecisionTreeClassifier` with no
  `random_state`, so ties between equally good splits are broken at
  random. The trees agree on the rows they were fitted to and disagree on
  other rows. **Inferred**: the leading alternative, thread order, does not
  apply to a sequential build. The pool-builder code is identical in 0.21.0
  and 0.22.1, so F141 does not interact with it. **Constraint**: seeding the
  trees changes every Phase 1 pool rebuilt afterward. So the fix is opt-in
  for Phase 2 builds, and Phase 1's path is unchanged. Changing Phase 1's
  default would be a Class 1 decision. Re-estimated from 60 to 30 minutes.
- **F144: runtime measured.** One 833-variable full-pair pool (`full`
  config, seed 42) built under WSL in **86 s wall-clock** (32 workers; the
  weak-learner build was 51 s of it). Ten seeds is about 15 minutes. The
  Sprint 12 figure of 735 s per pool is superseded. B2's own pools were
  never stored, so F144 is a twin of B2's configuration, not of its pools.
- **F142: inputs confirmed.** The B4 rows in
  `experiments/results/b4_hardware.json` record `dynamic_range_db` of
  8.1-8.4 against the 23 dB limit, and each has `job_id` and
  `all_samples`. The proven runner is `run_hardware_b4.py` with
  `eqc_submit.metered_fit`. The draft preregistration's section 6 has no
  entry for F142 or F144 yet; it says each is written before the run.
- **F147: the read-only open works.** A `mode=ro` URI opens
  `D:/Data/Harold/EvidenceBasedDB/store/evidence.db`. Its journal mode is
  `delete`, not WAL, so no writable side file is needed. A `CREATE TABLE`
  through the connection fails with "attempt to write a readonly
  database".
- **F126: inputs confirmed; one design choice for you to see.**
  `experiments/phase2/results/device_samples/` holds 22 sample files, as
  the card says: 10 B4 (CVQBoost) and 12 B5. B5 is QSVM, a different
  objective. **I plan to fit and test the rule on B4 only** (oilgas against
  telecom, 5 fits against 5), and to report B5's zero fraction beside it as
  a descriptive check, not as evidence for the rule. This narrows the card,
  which counts all 22. Object at approval if you want B5 inside the fit.
- **F105: inputs confirmed.** `experiments/data/ieee-cis/` holds
  `train_transaction.csv` and `train_identity.csv`. No harness exists yet.
- **F146**: the living document exists. F141's bump and F142's first fit
  are two of its listed triggers.

### Show each threshold can fire (Sprint 25 IMP-2)

Each threshold was run once on data already on disk, where it should not
fire, or the plan names the first run that will show it.

- **F145, acceptance "two builds byte-identical"**: it fires on today's
  code (the two builds above have different SHA-256 hashes). So the test
  can fail, and the fix is what will make it pass.
- **F142, B4 "Dirac-3S behaves differently from Dirac-3"**: Dirac-3's
  `weight_cosine_vs_classical` on oilgas is 0.892-0.901 across seeds
  42-46. A plain "outside Dirac-3's range" rule **fires on Dirac-3's own
  seeds**: leave seed 45 out, and its 0.892 falls 0.003 below the other
  four. The rule is widened: outside the Dirac-3 range, extended on each
  side by the range's own width. Leave-one-out, that fires on none of the
  five Dirac-3 seeds. For Dirac-3S it is outside [0.883, 0.909]. With 2
  fits, the result is descriptive, not a test.
- **F144, "the device beats its own proxy"**: the paired interval of
  (B2 device minus proxy twin) over 10 seeds must exclude zero. The noise
  it has to beat is the rebuild drift: about 0.0013 AUPRC on seed 42
  (F29). No 10-seed reference exists on disk. **First run that shows it**:
  F144's first step computes the same interval between the stored
  `h_*_free_dct_full` pools and fresh unseeded rebuilds of them, 10 seeds,
  where the true difference is zero. If that interval excludes zero, the
  device comparison is not read.
- **F126, tolerance on the held-out zero fraction**: the device's
  exact-zero fraction varies 0.02-0.03 within a dataset (oilgas 0.14-0.16,
  telecom 0.35-0.38). The gap between the datasets is about 0.21. The
  tolerance, set before the fit, is **0.05 absolute**. The reference rule
  "predict telecom from oilgas's fraction" misses by 0.21 and fails it.
  F17's emulator (0.14-0.17 on telecom) also fails it. So the test can
  fail.
- **F141**: no measured premise. Its guard, a hardware row without
  `device_type` failing the row-schema test, is proven red with
  `assert_can_fail` during the task.
- **F105**: a build card with no premise to falsify. No score is reported
  until F102 names its preregistration entry. Its leakage audit has a
  threshold, and no data exists for it yet. **First run that shows it**:
  adversarial validation on two random halves of one time window, where
  the classifier's AUC must stay at or below 0.55, before any cross-window
  run is read.
- **F147, F146**: no measured premise.

## Tasks

| Task | Card | What | Est | Runtime | Depends on |
|---|---|---|---|---|---|
| A | F141 | Bump `qci-client` 5.0.3 and `eqc-models` 0.22.1 in the lock, the Windows venv and the WSL venv; `sampler_type` at the solver construction points; `device_type` required on Phase 2 hardware rows | 45 | ~2 | - |
| B | F145 | Opt-in seeded weak learners for Phase 2 builds; a test that two builds are byte-identical | 30 | ~3 | - |
| C | F144 | The proxy twin of B2's configuration (k=17, schedule 3, full pair, 833 variables), 10 seeds, on B's seeded build; the drift reference first | 45 | ~25 | B |
| D | F142 | Runner and dry run for B1 2 fits, B2 1 fit, B4 2 fits on Dirac-3S; three approval stops; the write-up | 80 | ~172 metered s, plus queue | A; Decision 1 |
| E | F147 | Read-only query tool over the evidence library; one research note citing its records | 120 | - | - |
| F | F126 | Sparsity rule fitted on oilgas, tested on telecom (and the reverse), tolerance 0.05 | 60 | ~2 | - |
| G | F105 | IEEE-CIS rolling-origin folds, entity reconstruction for aggregations only, adversarial validation, leakage audit; no score reported | 240 | pilot first | - |
| H | F146 | Two updates of `DIRAC_UNDERSTANDINGS.md`: after A's bump, after D's first fit | 60 | - | A, D |

**Derived total: 680 minutes of work**, the sum of the card estimates
above, before Decision 1. With Decision 1's answer:

- Option 1: **700 minutes** (the two section 6 entries, 10 minutes each,
  in C and D).
- Option 2: **760 minutes** (F104 as a new task, 60, plus the two entries).
- Option 3: **670 minutes** (D builds and dry-runs only: 80 becomes 50;
  plus the two entries).

Runtime is separate. C's pool builds run under WSL in the background.
Each full suite run takes about 7 minutes.

How each estimate was set (`docs/VELOCITY_LOG.md` read first):

- **Tooling (A, B, E)**: the median ratio over Sprints 22-24 is 0.13, from
  9 rows (0.05-2.25). A ratio that low would give A 8 minutes. A is set at
  45 because it bumps two venvs and regenerates the lock, and because
  dependency bumps have run long: Sprint 24's pypdf bump ran at 1.7. B was
  re-estimated after its diagnosis was reproduced. E is a new tool with a
  read-only proof; set at 120 of the card's 180.
- **Research+code (C, D, F, G)**: the median ratio over Sprints 24-25 is
  0.37, from 4 rows (0.06-0.58). C 45 of 90, F 60 of 180 at about that
  ratio. D stays near its card (80 of 90), because it has three approval
  stops and a write-up. G has nothing comparable. It is sized to its
  first decisive step (the folds and the leakage audit) at 240 minutes,
  with the card's 360 as its timebox.
- **Docs (H)**: two updates at the card's 30 minutes each.

**Allowances**: none. No task is dominated by verification or by writing
claims.

### Task order

1. **A** (F141) first. It gates D and H.
2. **B** (F145), then **C** (F144) launched in the background on B's
   seeded build.
3. **D** (F142): the runner and dry run, then the **first approval stop**
   (B1, fit 1).
4. **H**'s first update (after A) while waiting for approval.
5. **E** (F147), **F** (F126) and **G** (F105) run while C's builds and
   D's queue wait proceed.
6. **H**'s second update after D's first fit.

### Task A detail (F141)

- `experiments/requirements.txt` and the lock: `qci-client==5.0.3`,
  `eqc-models==0.22.1`. Install into `.venv` and into `/root/eqc-venv`
  under WSL `OracleLinux_9_1`; record both versions in the task's commit.
- `sampler_type="dirac-3s"` passed where a Dirac-3S run asks for it: the
  `cb.Dirac3CloudSolver` substitution point in `eqc_submit.py`, and
  `Dirac3IntegerCloudSolver` directly.
- `device_type` required on every Phase 2 hardware row, beside F133's
  `job_id` rule. Job metrics are read by the submitted device name.
- **Acceptance**: an offline dry run reaches a request body naming
  `dirac-3s`, with no device call, in both venvs; the row-schema test fails
  on a Phase 2 hardware row without `device_type`, proven red; the
  proxy-identity check passes on 0.22.1; the full suite passes.

### Task B detail (F145)

- An opt-in `random_state` for the weak learners, passed through
  `qubo_proxy.py`'s `weak_params`, derived from the build seed. Phase 2
  builds use it. Phase 1 configurations and their stored pools are
  unchanged.
- **Acceptance**: a test builds the same small pool twice with the option
  and asserts byte-identical `H_tr`, `H_va` and `H_te`, proven red with
  `assert_can_fail` by removing the seed; the drift without the option is
  recorded as the known limit for Phase 1 pools in the Phase 2 draft's
  section 7.

### Task C detail (F144)

- **First, the reference**: the paired interval between the 10 stored
  `h_*_free_dct_full` pools and fresh unseeded rebuilds of them. If it
  excludes zero, the device comparison is not read, and the write-up says
  why.
- Then the twin: the `full` config (k=17, schedule 3, full pair, 833
  variables), seeds 42-51, built with B's seeded option under WSL, exact
  proxy solve, as dated Phase 2 rows with evidence tag `SIM`.
- **Acceptance**: the paired difference against B2's 10 device rows, with
  its interval; stated whether the device beats its own proxy; stated that
  this twins the configuration, not B2's unstored pools.

### Task D detail (F142)

- **Before any call**: the section 6 entry for these runs, as Decision 1
  says. The runner reuses `run_hardware_b4.py` and
  `eqc_submit.metered_fit`, with `sampler_type="dirac-3s"`, idempotent, and
  every row naming `device_type`, `job_id` and all samples. A dry run in
  both venvs.
- **Approval stop 1**: B1 `hw_b1_dct` seed 42, 1 call, about 5 s at
  Dirac-3 rates, cap 60. Its cost and queue wait re-quote everything after
  it.
- **Approval stop 2**: B1 seed 43 and B2 seed 42 (833 variables), 2
  calls, re-quoted from stop 1. B2's cap is 150.
- **Approval stop 3**: B4 oilgas_gasturbine seeds 42 and 43, 2 calls,
  re-quoted, cap 150. Each B4 job's dynamic range is read before its
  submit and must be under 23 dB (Decision 1 sets how).
- **Acceptance**: rows written as dated Phase 2 rows naming the device,
  never as Phase 1 gate cells; B1 and B2 reported as cost and queue
  evidence only, with their failed screen beside them; B4 reported as
  weight cosine, objective gap to the proxy optimum and in-pocket AUPRC
  against the Dirac-3 rows, with the widened range above.

### Task E detail (F147)

- `scripts/edb_query.py` (name to confirm at build): standard-library
  `sqlite3` over a `mode=ro` URI. Text search across record values and
  paper titles, filtered by context, class, evidence tag, certainty and
  date; one record with its relations, yields and cited documents;
  `--json`; record ids printed for `EDB: <id>` citations.
- **Acceptance**: a text query and an id lookup on the live database; a
  test that a write through the tool's connection fails, proven red with
  `assert_can_fail` on a read-write connection; one research note in this
  repository cites records the tool found; `docs/phase2/EDB_PROPOSALS.md`
  updated with anything found while building it. Nothing is written to
  the evidence library.

### Task F detail (F126)

- A sparsity rule (for example a threshold on the relaxed weight, or a
  cap on the support size) fitted on the 5 oilgas fits and tested on the 5
  telecom fits, then the reverse. **Tolerance 0.05 absolute** on the
  exact-zero fraction of the lowest-energy sample, fixed here before the
  fit.
- **Acceptance**: the rule's held-out error against the tolerance, both
  directions; or a recorded finding that 10 fits cannot support a rule. A
  rule fitted and tested on the same fits does not count. B5's 12 QSVM
  fits are reported beside it as a descriptive check only.

### Task G detail (F105)

- Rolling-origin folds over `TransactionDT`; entity key
  `card1_addr1_(day - D1)` used only to compute group aggregations, never
  as a feature; client-mean post-processing; time-consistency feature
  selection; adversarial validation; a temporal-leakage audit.
- **Pilot first**: one fold on a 10% sample, timed, before the full run.
  Any run over 30 minutes writes a heartbeat file first.
- **Acceptance**: the harness builds and is tested; the
  random-halves adversarial check at or below AUC 0.55; no model score is
  reported until F102 names its preregistration entry.

### Task H detail (F146)

- After A: the client versions and the `generation` correction, under the
  right labels, with sources.
- After D's first fit: Dirac-3S's measured cost and queue wait, labeled
  Measured, with the row and field cited.
- Each update adds a revision-log row.

## Decisions during execution

- **Decision 5 (2026-10-14, Task A): option 1.** The team lead asked that no
  Phase 1 figure or document change, and proposed an in-repository archive of
  Phase 1 files. The archived Phase 1 repository at tag `as-filed` already is
  that archive, and `docs/PHASE_SEPARATION.md` section 9 had already replaced
  the "never edit, wrap" rule. The five rules are now in CLAUDE.md ("The
  Phase 1 boundary inside THIS repository"). Task A bumps this repository's
  lock and adds a dated line to its header. Decision 4 (a separate Phase 2
  environment) was withdrawn.

- **Correction to Decision 1's screen (2026-10-14, Task D dry run, before
  any call).** Decision 1 named `get_dynamic_range` against 23 dB. That
  ratio passes B1 at 4.8 dB, although A31 shows B1 is unresolvable, so it
  is not the test the decision intended. F142's runner screens with A31's
  spread test instead and records the dB figure beside it. B4 passes
  either way (37 times the step; 8.3 dB). Recorded on F104 and in the
  Phase 2 draft's sections 4 and 6.

## Decisions at approval (answered 2026-10-14: 1, 1, 1)

Asked in order. Decision 2 does not depend on Decision 1. Decision 3's
total depends on Decision 1, and each option names the total for each
Decision 1 answer.

**Decision 1. How F142 meets its two unselected dependencies (the F102
entry and the F104 screen)**

1. Fold both into this sprint's tasks, and leave F102 and F104 open in the
   backlog. Tasks C and D each write their own section 6 entry first, 10
   minutes each. Each B4 job is screened with `eqc-models`'
   `get_dynamic_range` (already used by `run_hardware_b4.py`) against 23 dB
   before its submit. B1 and B2 run under the draft's stated exception.
   Total 700 minutes. (Recommended.)
2. Add F104 as a new Task I (60 minutes, before D): the screen with its
   own test, proven red. The entries are written as in option 1. Total
   760 minutes.
3. Spend no metered seconds this sprint. Task D builds the runner and dry-
   runs it in both venvs; the five fits wait for Sprint 27. The entries
   are written as in option 1. Total 670 minutes.

**Decision 2. F121's new hold condition** (open since refinement)

1. Keep F121 on HOLD until a Phase 2 run, proxy or device, shows an
   in-segment edge over the matched control with an interval excluding
   zero. (Recommended.)
2. Close F121. Record that Experiment 5's transfer half was not run,
   because its replication half (F90) did not reproduce.

**Decision 3. The plan**

1. Approve the plan as written, with Decision 1's answer applied (700,
   760 or 670 minutes).
2. Approve without Task G (F105). The total falls by 240 minutes (to 460,
   520 or 430), and F105 returns to the backlog at priority 60.

## Risks

- **Dirac-3S cost and queue are unmeasured.** The first fit sets both,
  and every later block is re-quoted from it. The queue-timing memory
  (usually empty after 5 pm local) dates from 2026-09-09 on Dirac-3, and
  is unverified for Dirac-3S.
- **The client versions are new**: 8 days (`qci-client`) and 6 days
  (`eqc-models`) old on 2026-10-13. The proxy-identity check and the
  dry run in both venvs are the guard against a changed behavior.
- **The WSL venv is outside CI.** CI tests the Windows-equivalent path on
  ubuntu-latest. Task A's acceptance names the WSL dry run for that
  reason.
- **F145's fix could reach Phase 1.** It is opt-in; the test asserts the
  Phase 1 default is unchanged.
- **F105 is the largest and least sized card.** Its pilot runs first;
  Decision 3 option 2 removes it.
- **Local memory.** The Windows commit limit was near full in Sprint 25 and
  caused local out-of-memory test errors. CI on the draft PR is the
  arbiter; C's builds run under WSL, which has its own memory.
- **CI goes red between this plan and approval.**
  `test_phase3_artifacts.py` requires the PR, issues and approval once the
  status is `phase_3_planning`. That red is expected. Any other failure
  goes to a background agent at the 3.3.2 checkpoint.
- **Session continuity.** Every decision and finding lands in a committed
  file.

## Model assignments

Main loop for all tasks. C's builds and G's pilot run in the background,
each writing to a named file that is read in full when it finishes.

## Definition of Done

- Every task's acceptance criteria, as stated on its card and above, are
  met.
- Each new test is proven to fail before it is trusted.
- The full suite passes locally, and CI is green on the final HEAD.
- Manual Validation items are listed on screen and saved in
  `SPRINT_26_VALIDATION.md`.
- Retrospective, `SPRINT_26_SUMMARY.md` at Sprint 27 planning, and the
  velocity log rows from measured start times.
