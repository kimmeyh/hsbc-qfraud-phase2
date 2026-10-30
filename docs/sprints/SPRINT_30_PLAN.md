# Sprint 30 Plan: Measure the Work, Survive the Limits, Then Test the Ceiling and the Room

**Sprint**: 30 | **Branch**: `feature/20261030_Sprint_30`
**Planned**: 2026-10-30 | **Status**: DRAFT, awaiting Decisions D2-D4
(`SPRINT_30_DECISIONS.md`), then approval
**Scope**: F168, F173, F175, F172, F176, F169, F170, F171 and F174 (team
lead selection, 2026-10-30, D1 option 1)
**Metered Dirac seconds**: **0**. No task calls a device or a paid
service.

## Objective

Make a task's actual measure its work, and make agent work and long runs
survive a usage limit. Then take four measurements: a second ceiling
estimator, two row-level checks of the frauds every model misses, whether
a classical solver gets below greedy on IEEE-CIS, and the best result per
algorithm on IEEE-CIS.

- **F173, then F175, first**: every later task's actual is then measured
  as work, against its own task.
- **F168 next**: F174's long run is the first module to follow its
  restart rules.
- **F174's run in the background** from mid-sprint; F176, F169, F170,
  F171 and F172 while it runs.

## Decisions already made (team lead)

- **Scope**: as above, 945 minutes by card estimate (D1 option 1,
  2026-10-30). F155, F102, F161, F95, F114 and F13 were not selected.
- **F168**: assigned to Sprint 30 on 2026-10-26.

## Pre-kickoff (Phase 2)

- Sprint 29 merged to `develop` (PR #63, `af03165`) and released to
  `main` (PR #73). The branch is the Sprint 29 branch plus the refinement
  commits, the selection and this plan. No issue is open.
- Working tree clean before this plan. The full suite ran on `672ea4e`;
  its result is recorded in this plan's commit message, not here.
- Dependency scan, 2026-10-30: `pip-audit` on the lock file finds no known
  vulnerability. `pip list --outdated` shows minor and major releases
  (pypdf 6.21.4, scikit-learn 1.9.1, numpy 2.5.4 and others), none with an
  advisory; none is proposed.

## Plan-to-branch-state verification (3.2.2.1)

Each card was checked against the repository and the installed packages
on 2026-10-30. Probes were read-only or scratch, zero metered, not
evidence. **Three cards cannot run as carded**; each is a decision
(D2-D4). Two more are corrected below and need no decision.

- **F173: confirmed.** `check_commit_issue.py` has `problem()` and
  `timed()`; `update_sprint_status.py` has `--add-issue` and no task map.
  The new map is set when an issue is added (`--add-issue N --task X`).
  A "PR n review" commit names no issue, so it needs the timer of the
  task recorded as the review-fix task (a new `review_task` field, set
  when that task starts, as Sprint 29's Task J was).
- **F175: mechanism chosen here.** `update_sprint_status.py` already
  subtracts paused time (`task_paused_s`). An activity log is added: a
  PostToolUse hook appends a timestamp to a gitignored file while any
  timer runs. `--finish-task` subtracts every gap above 30 minutes and
  records both the elapsed and the active minutes. A wait for a background
  run with no tool call is then not work, and is recorded as a gap.
- **F168, part 1: confirmed.** The repository keeps no launch prompts
  (no `.claude/agents/`, no prompt templates under `docs/`).
- **F168, part 2: the card conflicts with the repository's resume
  pattern (D2).** F110, F162, F166 and every Sprint 29 module keep their
  finished units in the result file itself, marked `complete: false`, and
  `provenance.start` resumes only such a file with the matching sidecar.
  The card says checkpoints go to a scratch folder and only the final
  result to `experiments/phase2/results/`. Both work; they cannot both be
  the standard.
- **F168, part 3: corrected.** `device_store.saving` writes the response
  in `makeResults`, after the job returns. A job that was sent and whose
  process stopped before the return has no record, so a lookup by
  problem hash alone cannot stop a second send. Part 3 adds an intent
  record, written before `solve` sends, and the lookup refuses a block
  with either record. The 27 files now in `device_samples/` are Phase 1
  backfills with no `problem_sha256`; the lookup reports them as not
  covered rather than matching nothing silently.
- **F168, part 6: verified.** The CronCreate tool states that recurring
  jobs expire after 7 days, live only in the session, and fire only while
  the session is idle. Claude Code here is 2.1.314.
- **F172: confirmed.** Each named branch exists: `f166.choose_seeds`
  (`t42_min > 0`), the "below" reading and `svm_form`; `f156.summarize`
  and `term1_alone_4_of_5`; F160's SCIP call through
  `exp3_controls.exact_solver_control`; F159's `MemoryError` and
  `BrokenProcessPool` handler; `test_the_budget_can_fail`.
- **F176: confirmed, one correction.** `f160_room_ieee.json` records each
  instance's rows but not its Hamiltonian, so F176 rebuilds the six
  instances from F160's seeded pools and checks greedy's value against
  the recorded one before any solver runs. `exact_solver_control` returns
  SCIP's dual bound; PySCIPOpt 6.2.1 is installed.
- **F169: the card's setting does not exist (D3).** In scikit-learn
  1.9.0, HGB's `max_bins` accepts 2-255, and 255 is the default (probed:
  256 raises `InvalidParameterError`). F108's inferred cause of HGB
  failing its reference arm is that 255 quantile bins put a top-0.05%
  threshold inside one bin. HGB cannot add bins; early stopping can be
  turned off. LightGBM's `max_bin` has no such limit.
- **F170: confirmed.** F154's stored ULB predictions are in
  `experiments/results/predictions/` (read only; Phase 1 evidence is
  never written), seeds 42-51, read through `f154_confusion.load`.
- **F171: confirmed at Pass 1.** F152 stores four IEEE-CIS families with
  outcome blocks; all 60 score files exist. The test labels per fold come
  from `ieee_harness`, checked against each outcome block's
  `n_positives` before use.
- **F174: F166's seed rule gives too few seeds on IEEE-CIS (D4).**
  IEEE-CIS trains on 410,600 rows and 181 features (F152's month-4
  fold), ULB on about 170,000 rows and 30. F166's classical lanes took
  about 77 s per seed and its proxy lanes 286 s. Scaled by rows and
  features (inferred, not timed), seed 42 takes about 30-35 minutes. F166's
  120-minute cap then gives 3 seeds, below the 8 at which the Wilcoxon
  test can reach 0.05 / 6.

### Show each threshold can fire (Sprint 25 IMP-2, Sprint 28 IMP-5)

- **F173.** Fires: a commit naming #66 while only D's and H's timers run.
  Does not fire: the same commit while C's timer runs. One test each.
- **F175.** Fires: an 8-hour gap in the activity log is subtracted. Does
  not fire: activity every 10 minutes, nothing subtracted.
- **F168, part 3.** Fires: a block whose problem hash has an intent or a
  response record. Does not fire: a new hash.
- **F176, below greedy.** First run that shows it can fire: a small
  instance (n = 20, m = 4) solved exactly by enumeration where greedy is
  not optimal. If no such instance is found among seeded draws, the
  reading is stated as unable to fire before the IEEE-CIS run.
- **F169.** F108's pass rule (4 of 5 on the main arm) can pass and fail
  on this harness: the plug-in passed the noise and reference arms 5 of 5
  and failed the main arm (2 of 5).
- **F170.** The primary comparison (legitimate share among neighbors,
  missed against caught) is checked first on F108's simulator, where the
  rows below the Bayes boundary are known, so the reading has a case
  where it must differ.
- **F171, F174.** Descriptive. F174's rankings use section 2's paired
  test, as F166's did.

## Tasks

Estimates assume D2-D4 as recommended; the other options' effect is
stated under each decision.

| Task | Card | What | Est | Runtime | Depends on |
|---|---|---|---|---|---|
| A | F173 | `task_issues` map set with `--add-issue N --task X`; the hook refuses a commit whose named issue's task is not timed; the review-commit rule; one test per term, each proven red | 45 | - | - |
| B | F175 | Activity log hook (gitignored); `--finish-task` subtracts gaps over 30 minutes and records elapsed and active; tests proven red | 60 | - | A |
| C | F168 | The seven parts; part 2 per D2; part 3 with the intent record; the two guard tests and the hash lookup proven red | 240 | - | A, B |
| D | F174 | Entry; IEEE-CIS data from `ieee_harness`; the seven lanes on F166's grids; seed count per D4; tracked page generator; pages | 240 | per D4: seed 42 first (~30-35, inferred), then about 4-6 hours in the background | C |
| E | F176 | Entry (dated Experiment 3 amendment); the six instances rebuilt and greedy checked; SCIP with a longer cap and a local search from greedy; the n = 20 enumeration check first | 90 | ~2 hours (SCIP 6 x up to 20 min) | C |
| F | F169 | Entry (dated F108 amendment) per D3; F108's harness, seeds 42-46, margin and pass rule unchanged | 120 | ~20 | C |
| G | F170 | Entry; k nearest training neighbors per ULB test fraud, seeds 42-51; the simulator check first; distinct missed frauds counted | 30 | ~10 | C |
| H | F171 | Entry; F158 step 3 on F152's four families, folds 4-6, seeds 42-46 | 60 | ~5 | C |
| I | F172 | The coverage tests, each proven red | 90 | - | - |

**Derived total: 975 minutes of work**, the sum of the task estimates
(45 + 60 + 240 + 240 + 90 + 120 + 30 + 60 + 90). The selection's 945
plus 30 for D3's recommended option (two arms instead of one).

How each estimate was set (`docs/VELOCITY_LOG.md`, Sprints 28-29; only
measured rows used): the usable ratios of actual to estimate are 0.38,
0.43, 0.44 and 0.66. Card estimates are kept, not reduced: the ratios
come from four rows, and three Sprint 29 tasks with no usable actual were
research+code like D-H.

- **Tooling (A, B, C, I)**: the cards' estimates. C is the largest and
  has seven parts; its part 3 grew by the intent record (absorbed in the
  card's 240).
- **Research+code (D-H)**: the cards' estimates, F plus 30 per D3.

**Allowances**: none carried. Writing (D's pages, four entries and
result documents) is about 180 of 975 minutes.

### Task order

1. **A**, then **B**: timers then measure the rest as work.
2. **C**: its restart rules apply to D's run.
3. **D**: seed 42 timed, then the run in the background with a heartbeat.
4. **E, F, G, H** while D runs; each run in the background.
5. **I** last, or while runs go.

## Risks

- **Runtimes inferred.** D's and E's are scaled, not timed; each starts
  with a pilot, and no unsized run starts.
- **F175 changes how every later actual is computed.** The velocity log
  records both elapsed and active minutes, so Sprint 30's rows are
  comparable with earlier ones.
- **F168 touches the process docs and adds a hook-like wake-up.** The
  wake-up never sends a device call; its prompt says so, and the job id
  and its expiry are reported when it is made.
- **Local-only files.** F170, F171 and F174 read gitignored data and
  prediction files; their tests skip in CI where the files are absent.
- **CI goes red between this plan and approval.**
  `test_phase3_artifacts.py` requires the PR, issues and approval once the
  status is `phase_3_planning`. That red is expected.

## Model assignments

Main loop for all tasks. Long runs and the suite run in the background,
each writing to a named file that is read in full when it finishes.

## Definition of Done

- Every task's acceptance criteria, as corrected above, are met.
- Each new test is proven to fail before it is trusted.
- The full suite passes locally, and CI is green on the final HEAD.
- Manual Validation items are listed on screen and saved in
  `SPRINT_30_VALIDATION.md`.
- Retrospective, `SPRINT_30_SUMMARY.md` at Sprint 31 planning, and the
  velocity log rows from measured times.
