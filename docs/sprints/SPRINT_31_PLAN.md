# Sprint 31 Plan: Make Testing Fast and Sure, Then Read the Ceiling, the Segment and Both Devices

**Sprint**: 31 | **Branch**: `feature/20261104_Sprint_31`
**Planned**: 2026-11-04 | **Status**: DRAFT. D2 answered ("1 and 4");
D3-D6 written on their recommended answers (`SPRINT_31_DECISIONS.md`);
approval is asked after they are answered.
**Scope**: F180, F177, F178, F179, F114, F155, F157, F150, F95, F121 and
F13 (team lead selection, 2026-11-04, D1 option 4); the pypdf bump if D6
adds it.
**Metered seconds**: two device blocks, each stopping for its own
approval (Criterion H): F155, about 4 s (a floor, not a bound), and F95,
about 60 s (range 40-110, cap 120) on Dirac-3 under D5's recommended
answer. No other task calls a device or a paid service.

## Objective

Find where testing time goes and cut it with no guard lost, so an
approved small change is verified and committed in its development time
plus about 15 minutes. Then take the readings the last two sprints built
toward: the ceiling on real data, the classical reference on SPECTRA,
whether F121's hold condition is met, Dirac-3S's variable ceiling, and
schedule 4 on the residual. End with the Phase 2 plan and the backlog
updated from those results.

- **F179 first**: the status file every timer and the commit hook read
  gets its lock before the sprint's own timers run on it.
- **F180, then F177**: F180's findings are written as one decision; F177
  builds only the levers chosen there.
- **Long runs in the background** from early in the sprint: F157's
  pilots and runs, F114's runs.
- **Device blocks** (F155, F95) when their builds are ready, each with
  its own approval.
- **F178 before Manual Validation; F13 last** (team lead: "Last item in
  sprint after other results are known").

## Decisions already made (team lead)

- **Scope**: as above (D1, 2026-11-04, option 4).
- **F13**: the last task. "Update plan for Phase 2, then update the
  backlog based on updated priorities."
- **Open, asked with this draft**: D2 (F157's part), D3 (F121's test),
  D4 (F150's send status), D5 (F95's device), D6 (the pypdf bump).

## Pre-kickoff (Phase 2)

- Sprint 30 merged to `develop` (PR #74) and released to `main` (PR
  #91). No sprint issue is open. The branch is the Sprint 30 branch plus
  the two refinement commits and this plan.
- Working tree clean before planning. The non-proof suite ran on
  c97dee0; CI's full job, red proofs included, ran on a428b92, the code
  this branch carries. Their results are in the run output and CI, not
  restated here.
- Dependency scan, 2026-11-04: `pip-audit` on the lock file reports 7
  advisories against pypdf 6.21.2, fixed in 6.21.3 and 6.21.4 (D6).
  `pip list --outdated` also shows eqc-models 0.22.3 (installed 0.22.1);
  no bump is proposed in a sprint with device blocks, so both blocks run
  on the client the proven runner was tested with.

## Plan-to-branch-state verification (3.2.2.1)

Each card was checked against the repository and the installed packages
on 2026-11-04. Probes were read-only or scratch, zero metered, not
evidence. **Five cards cannot be planned as carded**; each is a decision
(D2-D6). The rest are confirmed below.

- **F179: confirmed, and seen at planning.** `update_sprint_status.py`
  writes through `os.replace` and holds no lock (no `O_EXCL`). On
  2026-11-04, while the pre-kickoff suite ran, two status updates failed
  with `PermissionError` from `os.replace`, each printing a traceback and
  leaving its `sprint_status.json.<pid>.tmp` behind (removed by hand).
  Task A's acceptance adds: a failed replace leaves no temporary file.
- **F180: confirmed.** `ci.yml` has `workflow_dispatch`, so CI's full job
  can be started by hand. The inventory test is new.
- **F177: confirmed, one note.** pytest-xdist is not installed; lever 2
  adds a declared dependency, and a lock header line, if chosen.
- **F178: confirmed.** The evidence store
  (`D:\Data\Harold\EvidenceBasedDB\store\evidence.db`) and
  `scripts/edb_query.py` exist; the store is opened read-only.
- **F114: confirmed.** `f169_plugin_bins.py` and `f108_ceiling.py` exist;
  LightGBM 4.7.0 is installed; ULB and IEEE-CIS data are on disk.
- **F155: confirmed, one finding.** The proven Phase 2 runner,
  `experiments/phase2/src/run_dirac3s_verify.py`, takes the device type,
  relaxation schedule and sample count per unit and stores through
  `device_store`. eqc-models 0.22.1 has no client-side size limit (no 949
  or 9,980 in its source), so a 1,300-variable job reaches QCi's queue
  and is accepted or rejected there. Whether a rejected job is billed is
  **unverified**.
  `qpu_cost_model.quote(1300, 1)` gives 4 s from one Dirac-3S anchor
  (833); above it, 4 s is a floor.
- **F157: no part named (D2, answered "1 and 4").** The other datasets
  on disk are SPECTRA's four. The QNN lane exists only as F106's
  statevector circuit on ULB, inconclusive at 99 test positives.
- **F121: hold not met (D3).** No Phase 2 result records an in-segment
  edge over a matched control. F162's per-row scores (three lanes, three
  cells, seeds 42-51, 90 files) are on disk, and the pocket flag is
  rebuilt from the seeded split, so the condition can be tested without
  a new fit.
- **F150: send status not recorded (D4).** The Sprint 28 draft exists in
  the gitignored `docs/spectra_package/`.
- **F95: the device question (D5).** On Dirac-3S, F142's schedule-2
  fits already reached the reference optimum. `qpu_cost_model.quote(91,
  1, relaxation_schedule=4)` returns unknown on Dirac-3S.
- **Allocation**: the last recorded read is 8,522 s on 2026-10-10
  (`experiments/results/allocation_reads.json`). The runner reads the
  balance again before any send.
- **F13: confirmed.** `docs/phase2/PHASE2_POC_PLAN_DRAFT.md` exists, on
  labeled assumptions.

### Show each threshold can fire (Sprint 25 IMP-2, Sprint 28 IMP-5)

- **F179.** Fires: two processes update the status file at once with the
  lock removed, and one change is lost. Does not fire: the same with the
  lock. Proven red in the commit that adds the lock.
- **F180.** Fires: a new test file not in the inventory fails the
  inventory test. Proven red.
- **F177.** Each lever is measured before and after on the same machine.
  Fires: a guard removed or weakened by a lever goes unproven, so each
  changed guard is proven red.
- **F114.** F108's pass rule can pass and fail on its harness (F169:
  HGB without early stopping failed one reference seed). On real data
  there is no known Bayes error. First run that shows the estimate can
  fire: a label-shuffled ULB arm on seed 42, where the estimate must sit
  at the no-information level; if it does not, the method does not
  transfer and the real-data figures are not reported as ceilings.
- **F157, SPECTRA part.** Descriptive, with F166's paired test, as F174.
- **F157, QNN part.** F106's rule (no twin's interval clears the -0.005
  margin) left the reading inconclusive at 99 positives. Fires: the entry
  states the positive count at which F106's observed spread gives an
  interval narrower than the margin, computed from `f106_dequant.json`
  before the run; if the chosen dataset cannot reach it, the entry says
  the run cannot decide and is redesigned before it starts.
- **F121.** Not run at planning: the test module does not exist yet. The
  task's first step, before the proxy's figures are read, runs the same
  test with HGB's stored scores in place of the proxy's. If HGB also
  shows an "edge", the test measures the pocket's difficulty, not a
  model's edge, and the test is redesigned before any reading.
- **F155.** Fires: a rejected job. An accepted job counts only if the
  returned solution has 1,300 entries; an accepted job that returns
  fewer reads as rejected.
- **F95.** The reference where the premise does not hold is on disk:
  Dirac-3S at schedule 2 shows no residual (F142). On Dirac-3, schedule 4
  closes the residual only if its gap to the exact optimum falls below
  the schedule-2 twin's, beyond the spread of the schedule-2 samples.
- **F178.** Fires: a broken link, an acronym used before it is spelled
  out, or an experimental claim that names no tracked source. Proven red.

## Tasks

Estimates are the cards', on the recommended answers to D2-D6.

| Task | Card | What | Est | Runtime | Depends on |
|---|---|---|---|---|---|
| A | F179 | Exclusive lock file around read, change and write; a stale-lock message naming the file; `PermissionError` on replace reported as a refusal, leaving no temporary file; `--review-task` after pause and finish; two-process test; each term proven red | 45 | - | - |
| B | F180 | Parts 1-7: the script-generated inventory and its test; effectiveness; efficiency, measured; the Sprint 30 timeline; the red-proof policy; which full run; risk tiers. Recommendations written as one decision, prevention first | 180 | one local full run with `--junitxml` (~49 min, measured 2026-11-01, background); one CI full job by `workflow_dispatch` (~12 min) | A |
| C | F177 | The levers chosen in B's decision, each measured before and after; `scripts/suite_times.py`; the checklist and workflow say which suite runs when | up to 240 | the before run is B's; one after run (~5-49 min) | B's decision |
| D | (D6) | pypdf 6.21.2 to 6.21.4 in the lock, a dated header line; the submission-artifact tests, no PDF re-rendered | 45 | - | - |
| E | F114 | Entry (dated F108 amendment) first; F169's LightGBM 4,095-bin plug-in on ULB and IEEE-CIS; the shuffled-label arm first; intervals over seeds | 90 | seed-42 pilot timed first, then the seeds the entry names, background | A |
| F | F157 | SPECTRA part (D2 option 1): F166's protocol on the four SPECTRA datasets; pages from the tracked generator | 240 | a timed seed-42 pilot per dataset, then the seeds it sets, background | A |
| M | F157 | QNN part (D2 option 4): entry first, choosing IEEE-CIS or a larger ULB test set and saying why; F106's circuit and twins; seeds from a timed seed-42 pilot | 120 | pilot first; F106's eight ULB seeds took 8,640 s; background | A |
| G | F121 | Per D3: entry; the HGB reference run first; the hold test on F162's stored scores; Experiment 5's entry as a draft | 60 | minutes | A |
| H | F150 | Per D4: the draft checked against the title and F109, handed to the team lead to send; the rebuild only if a reply arrives before Phase 5 | 15 | - | D4 |
| I | F155 | Entry; the 1,300-variable unit through the proven runner and `device_store`; offline dry run; then STOP for approval with the call count and seconds | 30 | about 4 metered s after approval | A |
| J | F95 | Per D5: entry naming Dirac-3; the four units on frozen pools through the proven runner; offline dry run; then STOP for approval; fit 1, then re-quote if over 27 s | 60 | about 60 metered s (40-110, cap 120) after approval | A |
| K | F178 | The three documents, version 1.0 with change lists; the link, acronym and claim test proven red; the Phase 5 update step | 234 | - | results of E-J where available |
| L | F13 | The Phase 2 plan updated from this sprint's results; then the backlog re-prioritized from it | 75 | - | all others |

**Derived total: 1,434 minutes of work**, the sum of the task estimates
(45 + 180 + 240 + 45 + 90 + 240 + 60 + 15 + 30 + 60 + 234 + 75 + 120).
Plus about 120 minutes for F150's rebuild only if the authors reply
before Phase 5. The selection's card estimates, with these changes: F157
as two parts, 240 and 120 (D2, answered "1 and 4"), F121 at 60 (D3), F150 at 15 (D4), F95 at 60 (D5), the
pypdf task at 45 (D6), and F178's sourcing allowance below.

How each estimate was set (`docs/VELOCITY_LOG.md`): Sprint 30's active
ratios run from 0.02 to 0.38 where an estimate exists, but four rows are
flagged "cause unverified" and two research rows ran in the background.
Sprints 28 and 29 give 0.06 to 0.66 on the rows measured as work. Card
estimates are kept, not reduced; B's parts 3 and 4 measure where the
time goes. No ratio is converted into a forecast.

**Allowances**: F178 carries a 30% sourcing allowance (54 of its 234
minutes): it is prose that makes claims about every result and outside
source (SPRINT_PLANNING.md, Sprint 15 improvement 3). If its claims
source cleanly, the allowance is returned. No verification allowance:
the sprint is not dominated by checks.

### Task order

1. **A** (F179): the lock, before the sprint's own timers lean on it.
2. **B** (F180) starts with the background full run. **E**, **F** and
   **M** pilots start in the background while B's analysis runs, one
   heavy run at a time beside the suite.
3. **D** (pypdf) and **G** (F121) while runs go.
4. B's recommendations asked as one decision; then **C** (F177).
5. **I** and **J** built and dry-run; each stops for its own approval.
   Run in the late afternoon or evening if the queue matters (the queue
   note in memory is dated and is checked again at the time).
6. **H** as soon as D4 is answered.
7. **K** (F178) once E-J have readings; its first versions exist by
   Phase 5.
8. **L** (F13) last.

## Risks

- **Two metered blocks (Criterion H).** Each stops for approval with its
  call count and seconds. `device_store` records an intent before each
  send and refuses a repeated problem hash. F155's rejected-job billing
  is unverified, and its 4 s is a floor.
- **Runtimes.** F157's two parts and F114's are unsized until their
  pilots; F106's eight ULB seeds took 8,640 s, and a larger positive
  count costs more. No
  unsized run starts; each run over 30 minutes writes a heartbeat.
- **Local red-proof runs edit source files.** No two suite runs at once,
  and no edit to a file a running proof mutates (Sprint 30's two restore
  failures).
- **F177 changes which tests run where.** A guard that leaves a run is
  named with where it now runs, and CI's full job stays the backstop.
- **F178's sourcing.** Its claims are checked against tracked results
  and the evidence store; a claim that cannot be sourced is removed, not
  softened.
- **Session continuity.** Long runs resume through `provenance.start`;
  agents launch from kept prompts; the hourly wake-up runs while the
  session is idle.
- **CI goes red between this plan and approval.**
  `test_phase3_artifacts.py` requires the PR, issues and approval once
  the status is `phase_3_planning`. That red is expected.

## Model assignments

Main loop (Opus, top tier) for all tasks, including B's analysis and L's
planning, which the top-tier rule names. Long runs and the suite run in
the background, each writing to a named file that is read in full when
it finishes.

## Definition of Done

- Every task's acceptance criteria, as corrected above, are met.
- Each new rule, refusal and reported state has its own test, proven red
  in the commit that adds it.
- CI's full job is green on the final HEAD.
- Manual Validation items are listed on screen and saved in
  `SPRINT_31_VALIDATION.md`.
- Retrospective, `SPRINT_31_SUMMARY.md` at Sprint 32 planning, and the
  velocity log rows from measured times.
