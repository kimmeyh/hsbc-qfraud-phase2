# Sprint 25 Plan: Learn the New Device, Then Build What Runs on Any Device

**Sprint**: 25 | **Branch**: `feature/20261010_Sprint_25`
**Planned**: 2026-10-13 | **Status**: APPROVED 2026-10-13 (option 1, as
written). Issues #13-18 (Tasks A-F in order). Draft PR #12.
**Scope**: F138, F139, F102, F113, F29 and F94 (team lead selection,
2026-10-13)
**Metered Dirac-3 seconds**: **0**. No task touches the device. A read of
the balance with `check_allocation.py` is a GET and costs nothing.

## Objective

Find out what Dirac-3S changes before any further Dirac-3 seconds are
spent, and meanwhile build and measure the classical work that does not
depend on the answer.

- **F138, then F139**: what the upgraded device changes, and which past
  runs to repeat on it. Together they gate every card that spends Dirac-3
  seconds.
- **F102**: the first draft of the Phase 2 preregistration framework.
- **F113, F29, F94**: three classical items that need no device. F113 can
  retire the router line early. F29 answers and closes an open question.
  F94 builds the Experiment 3 controls that F25 cannot report without.

## Decisions already made (team lead, 2026-10-13)

- **D1**: scope as above. **F140 canceled**: CI on release PRs into
  `main` would duplicate the `develop` run for no value.
- **D2**: F129 re-scored from 34 to 100. F139 decides whether its device
  run happens.
- **D3**: priority numbers unchanged (F138 5, F139 6, F102 30, F94 50,
  F29 112, F113 130). Task order below is by dependency, not by number.
- **D4**: F94's exact solver is SCIP through PySCIPOpt, behind a solver
  interface.
- **F102 is a living draft**: it is updated across later sprints until
  Phase 2 is approved and a filing date is set.

## Pre-kickoff (Phase 2)

- Sprint 24 merged to `develop` (PR #2) and released to `main` (PR #11).
  Issues #3-10 closed. Working tree clean.
- Full suite passed on 2026-10-10 after the Pass 1 edits.
- Dependency scan: `pip-audit` on the lock file finds no known
  vulnerability. Newer versions exist for 16 packages. Two matter to this
  sprint: `eqc-models` 0.22.1 (pinned 0.21.0) and `qci-client` 5.0.3
  (pinned 5.0.2). F138 checks whether either is needed for Dirac-3S. No
  bump is planned.

## Plan-to-branch-state verification (3.2.2.1)

Each card was checked against the repository on 2026-10-13.

- **F138 confirmed.** The user's guide is on disk (13,714,215 bytes,
  dated 2026-10-10). All three web sources return HTTP 200. The QCi notice
  is in `docs/qci_package/` (gitignored).
- **F139 confirmed.** Its input records exist:
  `docs/QPU_RECONCILIATION.md`, `docs/B4_B5_HARDWARE_RESULT.md`,
  `docs/INTEGER_PROBE_RESULT.md`, `docs/RESULTS_MEMO.md`,
  `docs/HARDWARE_REQUEST_B1_G0b.md` and `docs/HARDWARE_REQUEST_B4.md`, plus
  `experiments/results/integer_probe.json` and the two
  `variable_ceiling_probe` files.
- **F102 confirmed.** Nothing exists yet. The card already carries the
  control design and its feasibility arithmetic.
- **F113 confirmed, and smaller than carded.** The inputs are stored: ULB
  test-fold predictions for three CVQBoost proxy configurations and two
  XGBoost configurations, 10 seeds each (42-51), in
  `experiments/results/predictions/`. For seed 42 the two families share
  the same `y_test` (95 positives). No model is refitted. Re-estimated from
  3h to 90m.
- **F29 confirmed.** No script exists. It reuses `qubo_proxy.py`
  (`build_pool`, `h_matrix`, `solve_simplex_qp`). The card's run was
  measured at 8-10 minutes for the full grid.
- **F94: one premise corrected.** The card cites "the two measured sizes,
  60 and 150 variables". Those integer probes used SYNTHETIC matrices
  (`run_integer_probe.build_job`, deliberately random). They size the
  device, not a fraud problem. F94 builds its instances from real ULB proxy
  pools instead, from the frozen cells in `qubo_proxy.CONFIGS`. Built
  sequentially, which runs on Windows (`qubo_proxy.py:227`), `free` (k=13,
  schedule 2) gives 78 learners and `mid` (k=17, schedule 2) gives 136.
  So the two sizes become **60 and 136**, not 60 and 150; 150 would need
  the full-pair build, which needs fork and therefore WSL.
- **F94's solver: proven by a spike.** PySCIPOpt 6.2.1 (uploaded
  2026-05-16, bundling SCIP 10.0) installs from a wheel on Windows. A
  12-learner, choose-4 problem with the quadratic objective entered as a
  constraint solved to optimal in 0.89 s. It matched brute-force
  enumeration to 6 decimals (2.715651). The spike ran in a scratch venv;
  the project venv is unchanged.

## Tasks

| Task | Card | What | Est | Runtime | Depends on |
|---|---|---|---|---|---|
| A | F138 | `docs/phase2/DIRAC_3S_RESEARCH.md`: the card's seven questions answered with sources; every Dirac-3 card's cost and sizing re-checked | 120 | - | - |
| B | F139 | Every Dirac-3 run reviewed: verify, full re-run or no re-run, each with its seconds; the plan update for new problem sizes and degrees | 120 | - | A |
| C | F102 | First draft of the Phase 2 preregistration framework | 120 | - | A (its amendment answer) |
| D | F113 | Oracle-gap test on the stored ULB predictions | 90 | ~2 | - |
| E | F29 | Sample-size insensitivity of the CVQBoost optimum on ULB | 60 | ~10 | - |
| F | F94 | Experiment 3 controls: exact enumeration, greedy, simulated annealing and SCIP, on ULB proxy pools | 240 | ~60 | - |

**Derived total: 750 minutes of work**, the sum of the card estimates
above. Runtime is separate. Task E's run and Task F's solves run in the
background while other tasks proceed. Each full suite run takes about 7
minutes.

How each estimate was set (`docs/VELOCITY_LOG.md` read first):

- **A, B and C** are `[no-history]` research and writing. Research cards
  in Sprints 21-22 ran at 0.09-0.57 of their estimates; F124, the closest
  match, ran at 0.4. Each is sized to its first decisive measurement, and
  its original card estimate (3h) is its timebox.
- **D**: analysis of stored scores. The closest row is Sprint 21's F101
  analysis at 0.57; 0.5 of the card's 3h gives 90m.
- **E**: the card's own measured figure.
- **F**: new code plus measurement. The comparable code-and-compute rows
  ran at 0.37 and 0.95 in Sprint 21, so the card's 4h stands.

**Allowances.** Tasks A, B and C are dominated by writing that makes
factual claims. Per `SPRINT_PLANNING.md`, they carry a **30% sourcing
allowance**, 108 minutes, named here and not part of the derived total. If
every claim sources cleanly, it is returned.

### Task order

A first, because it gates B and informs C. B straight after A (team lead,
2026-10-10). E's run is launched as soon as its script exists, and F's
solves the same way, so their runtime overlaps the writing tasks.

### Task A detail (F138)

- Read the user's guide in full with `pypdf`. The site sweep against the
  last scrape (EvidenceBasedDB `508a14d`, 2026-09-24) goes to a background
  agent, with its findings written to a named scratchpad file and read in
  full.
- The note answers each question with its source, or says the source does
  not answer it. It covers which device serves this account and how it is
  chosen; the variable ceiling; cost per fit against the F17 model; the
  relaxation schedules, samples and integer limit; `qci-client` and
  `eqc-models` support (pinned against newest); the preregistration
  question; and queue timing.
- EvidenceBasedDB is read only. Anything its reference library should hold
  is handed to an EvidenceBasedDB session.

### Task B detail (F139)

- One row per run on record: G0b, B1, F32, the A21 probe, B3 (both runs),
  B2, the integer probes, B5 and B4. Fits, seconds and configuration come
  from the result files and `QPU_RECONCILIATION.md`, not from summaries.
- Each row gets one recommendation and its seconds against
  `experiments/results/allocation_reads.json`. Any re-run is a new card
  with its own approval (Criterion H). Nothing runs in this sprint.
- The plan update lists what Dirac-3S allows that Dirac-3 did not (4th or
  5th degree problems; telecom_churn at 987 variables), each as a card
  with its seconds, and re-checks the Phase 2 hardware plan's sizing.

### Task C detail (F102)

`experiments/phase2/PREREGISTRATION_DRAFT.md`, a new document.
`experiments/PREREGISTRATION.md` stays FROZEN and is not touched. The draft
holds the per-experiment template, the reporting standard named on the
card, the downsized matched-pair control with repeated draws and its
arithmetic, and F138's answer on device changes. Its header says it is a
draft, revised across sprints until Phase 2 is approved and a filing date
is set.

### Task D detail (F113)

- On each of the 10 seeds, on the test fold: the champion CVQBoost proxy
  and the champion XGBoost, each identified from its `results.json` row by
  config hash. Matched operating point at the 0.5% alert budget, rank
  correlation of the two score vectors, and the oracle: the better of the
  two per transaction, using the true label.
- **Premise falsifier, stated before the run**: if the oracle's recall at
  the 0.5% budget is less than 1 point above the better single model, no
  router can meet the proposal's router criterion (at least 1 point of
  recall at that budget). The write-up then recommends retiring F121.
- Output: `experiments/phase2/results/f113_oracle_gap.json`, evidence tag
  `SIM`, and a short write-up in `docs/phase2/`. 95 positives per test
  fold makes each recall step about 1 point, so the result is reported
  across all 10 seeds with its spread.

### Task E detail (F29)

- ULB train fold subsampled to 4 sizes, 3 seeds each, from the card's
  measured grid. Same pool, same lambda rule. Report the weight cosine
  between each size and the full fold, and the test AUPRC.
- **Premise falsifier, stated before the run**: the optimum is called
  insensitive if every subsample's weights have cosine at least 0.99 with
  the full-fold weights on the same seed. Any value below that, and the
  card's premise is wrong; the result is recorded either way and the card
  closes.
- Output: `experiments/phase2/results/f29_sample_size.json`, evidence tag
  `SIM`.

### Task F detail (F94)

- **Instances**: ULB proxy pools from `qubo_proxy.build_pool` and
  `h_matrix`, built sequentially, seeds 42-44: the first 60 learners of
  the `free` pool, and the whole 136-learner `mid` pool. Objective as
  `qubo_proxy` (`J = HH^T + lambda*I`, `C = -2Hy`), weights summing to 1,
  at most m learners selected. m is 10 at 60 learners and 25 at 136,
  recorded before any solve.
- **Controls**: exact enumeration at a small size (20 learners, choose 4)
  as a certified optimum; greedy forward selection; simulated annealing
  with recorded seeds; SCIP through a thin solver interface, capped at 600
  s per instance, reporting its optimality gap when the cap is reached.
- **Dependency**: `pyscipopt==6.2.1` added to `experiments/requirements.txt`
  and the lock file; `test_requirements_complete.py` passes; CI installs it
  on ubuntu-latest from its manylinux wheel.
- **Premise falsifier for the solver leg**: SCIP and exact enumeration
  must agree at the size where both run. If they do not, the SCIP leg is
  not used, and the cause is recorded.
- Output: `experiments/phase2/results/f94_controls.json`, evidence tag
  `SIM`, as dated post-submission rows. No Phase 1 claim touched.

## Decision at approval

1. Approve the plan as written.
2. Approve without Task F (F94). The total falls to 510 minutes, and F94
   goes back to the backlog at priority 50.

## Deviations from the process

- **Task G added during Manual Validation** (team lead, 2026-10-13, "do
  now"; issue #19). A first draft of `docs/phase2/DIRAC_UNDERSTANDINGS.md`
  (Dirac-3 and Dirac-3S understandings, suggested Dirac-3S improvements,
  QCi questions), kept current by the new permanent HOLD card F146; the
  next-sprint card F147 (a read-only query tool over the evidence library);
  and `docs/phase2/EDB_PROPOSALS.md`. Documents only, zero metered seconds.
  Not task-timed: no start was stamped before the work began.

## Risks

- **The QCi sources may not answer every F138 question.** The note says
  which ones are unanswered. Anything still open goes to the team lead as a
  question for QCi. No device call is made to find out.
- **F94 may be slow at 136 learners.** Each SCIP solve is capped at 600 s
  and reports its gap; a capped result is still a result.
- **F29 and F94 need pool builds.** Both use the sequential build, which
  runs on Windows. No task needs the full-pair build or WSL.
- **A new dependency enters CI.** PySCIPOpt ships a manylinux wheel; the
  first CI run after Task F proves it installs.
- **CI goes red between this plan and approval.** `test_phase3_artifacts.py`
  requires the PR, issues and approval once the status is
  `phase_3_planning`. That red is expected. Any other failure goes to a
  background agent at the 3.3.2 checkpoint.
- **Session continuity.** Every decision and finding lands in a committed
  file, so a context compaction loses nothing the sprint needs.

## Model assignments

Main loop for all tasks. Task A's site sweep goes to a background agent
with its output file named in advance. Task E's run and Task F's solves run
in the background.

## Definition of Done

- Every task's acceptance criteria, as stated on its card and above, are
  met.
- Each new test is proven to fail before it is trusted.
- The full suite passes locally, and CI is green on the final HEAD.
- Manual Validation items are listed on screen and saved in
  `SPRINT_25_VALIDATION.md`.
- Retrospective, `SPRINT_25_SUMMARY.md` at Sprint 26 planning, and the
  velocity log rows from measured start times.
