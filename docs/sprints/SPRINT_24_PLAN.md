# Sprint 24 Plan: Close the Boundary, Fix the Tooling, Sweep the Lever

**Sprint**: 24 | **Branch**: `feature/20261008_Sprint_24`
**Planned**: 2026-10-09 | **Status**: DRAFT, awaiting approval
**Repository**: `kimmeyh/hsbc-qfraud-phase2`. This is the first sprint in
this repository (Sprint 23's D5: it starts at the Phase 1 repository's last
sprint plus one).
**Scope**: F131, F136, F132, F134, F133, F135, F128 and F137 (team lead
selection, 2026-10-09: D1 option 1, plus F137 by D5)
**Metered Dirac-3 seconds**: **0**. No task touches the device.

## Objective

Make this repository stand on its own, then take the first Phase 2
measurement in it.

- **No live reference to the Phase 1 repository** (F132). A script here
  still writes into the Phase 1 clone, and no hook can see it.
- **Fix the tooling defects this repository inherited**: the suite rewrites
  a tracked script (F131), the pre-commit scan is silently off without its
  pattern file (F134), device rows can lose their job id (F133), and the
  pypdf in the lock file has seven known vulnerabilities (F137).
- **Apply Sprint 23's three improvements** (F134, F135, F136).
- **Sweep `min_samples_leaf`** on the proxy (F128), so a later device run
  (F129) uses a value chosen from a sweep, not one point.

This sprint's merge to `develop` also releases the Phase 1 repository's
restore commit (Sprint 23's D6).

## Decisions already made (team lead, 2026-10-09)

- **D1**: scope option 1, F132, F134, F133, F131, F135, F136 and F128.
- **D2**: every F132 exception stays: the submitted proposal and appendix,
  the B5/B4 launcher log and the four history records.
- **D3**: this repository and its disk folder renamed to
  `hsbc-qfraud-phase2`.
- **D4**: the GitHub default branch is `develop`, matching the process docs.
- **D5**: F137 (pypdf bump) added from the Phase 2.6 dependency scan.

## Plan-to-branch-state verification (3.2.2.1)

Each card was checked against the repository on 2026-10-09.

- **F131 confirmed.** `test_ci_status.py:169` writes a stub over
  `scripts/check_ci_status.py` and `:177` writes it back as text. Every full
  suite run this session left the script modified, with only its line
  endings changed.
- **F136 confirmed.** `task_actuals` exists in `.claude/sprint_status.json`
  with no start field.
- **F132 confirmed, with a wider exception list.** `git grep` finds the
  Phase 1 repository's name in 22 tracked files, matching the card. The
  guard's `FORBIDDEN` is `("spamfilter-multi", "EvidenceBasedDB")`; its one
  mention of the Phase 1 name is a docstring line, not an entry. D2 settled
  three exception groups. The guard test will also meet files that must
  name the Phase 1 repository, or that record its history. Those are listed
  under D6 below for approval.
- **F134 confirmed.** `.githooks/pre-commit:26` is
  `if [ -f .secrets-patterns.txt ]; then`.
- **F133: the premise is wrong in one place.**
  `experiments/phase2/results/device_samples/*.json` (10 files) are
  recovered B4 device data, not proxy rows. They have no `rows` and no
  `evidence_tag`, and each carries a top-level `job_id`. The test covers
  both shapes. Re-estimated from 30m to 40m on the card.
- **F135 confirmed.** The dependent-decision rule is in `CLAUDE.md`.
- **F128: smaller than carded.** `lever_screen.py confirm` already runs 5
  seeds against HGB on the same splits. The sweep is a new part of that
  script. Re-estimated from 1.5h to 50m of work plus about 35m of runtime
  on the card.
- **F137 confirmed.** `requirements-lock.txt:40` is `pypdf==6.17.0`;
  `requirements.txt` says `pypdf>=4.0`, which allows the bump.

## Tasks

Ordered by hazard, not by priority number. F131 goes first because every
suite run until then rewrites a tracked script, and a CI check run during
the suite reads the stub. F136 goes second so the remaining tasks are timed
from a recorded start. Starting with Task A, each task's start time is
recorded in `.claude/sprint_status.json`, before F136 makes it a rule.

| Task | Card | What | Est | Runtime | Depends on |
|---|---|---|---|---|---|
| A | F131 | `test_ci_status.py` works on a hermetic copy; the tracked script's bytes asserted unchanged | 30 | - | - |
| B | F136 | Task start time recorded; actual computed from it; workflow Phase 4 and velocity log updated | 20 | - | - |
| C | F132 | No live reference to the Phase 1 repository; the guard names it; a tracked-file guard test | 90 | - | D6 |
| D | F134 | The pre-commit hook blocks when `.secrets-patterns.txt` is missing | 30 | - | - |
| E | F133 | `test_row_schema.py` requires `job_id` on Phase 2 device rows and device-sample files | 40 | - | - |
| F | F135 | `CLAUDE.md` sub-rule: every decision option names its concrete values | 10 | - | - |
| G | F128 | `lever_screen.py sweep`: `min_samples_leaf` 5, 10, 20, 50 on three datasets, 5 seeds, against HGB; result file and write-up | 50 | ~35 | - |
| H | F137 | `pypdf==6.20.0` in the lock file; venv reinstalled; `pip-audit` clean for pypdf; full suite | 20 | ~7 | A |

**Derived total: 290 minutes of work**, the sum of the card estimates
above. Runtime is separate: Task G's run takes about 35 minutes in the
background while other tasks proceed, and each full suite run takes about
7 minutes. `docs/VELOCITY_LOG.md` was read first. Tooling cards in Sprints
20-23 ran at 0.44-2.25 of their estimates, with most near 1.0, so no
reduction is applied to Tasks A-F and H. Task G is `[no-history]` and is
sized to its first decisive measurement, as `SPRINT_PLANNING.md` requires.

### Task A detail (F131)

`_hook_with_ci` copies `scripts/check_ci_status.py` and the hook into a
temporary directory and stubs the copy. The tracked script is never
opened for writing. The test reads the tracked script's bytes before and
after and asserts they are equal. `assert_can_fail` proves the hook test
still fails when the hook ignores CI status.

### Task C detail (F132)

- The four scripts (`us_english_fix.py`, `wsl_build_pools.sh`, `wsl_hw.sh`,
  `wsl_tune_proxy.sh`) derive their root from their own location.
  **`us_english_fix.py` is not run before this lands.**
- `block_cross_repo_write.py` adds the Phase 1 repository to `FORBIDDEN`.
  A test proves both directions: a Write and a shell write to the Phase 1
  path are blocked, and the same to this repository are allowed. The
  existing ALLOW case at `test_cross_repo_write_guard.py:95`, which uses the
  Phase 1 path, changes to this repository's path.
- Live process docs and code comments change to this repository or to "the
  Phase 1 repository": `SPRINT_PROCESS.md:19`,
  `SPRINT_EXECUTION_WORKFLOW.md:3`, four `README.md` clone lines,
  `PHASE_SEPARATION.md:173`, `confidentiality_scan.py:28,36`,
  `test_confidentiality_scan.py:64`, `test_hook_parity.py:230`.
- A new guard test fails if any tracked file outside the approved list
  names the Phase 1 repository: path, `/mnt/d` form, backslash form or URL.
  It is proven red with `assert_can_fail`.

### Task E detail (F133)

Two checks in `test_row_schema.py`. First, every row in an
`experiments/phase2/results/*.json` file whose evidence tag is hardware, or
whose file reports nonzero metered seconds, carries a nonempty `job_id`.
Second, every `device_samples/*.json` file carries a nonempty top-level
`job_id`. Both pass today. Each is proven red by an injected file.

### Task G detail (F128)

A `sweep` part in `lever_screen.py`, reusing the `confirm` path. It writes
`experiments/phase2/results/f128_leaf_sweep.json` with all 60 cells, and
for each dataset and value the paired difference against HGB with its CI,
the train-test gap and the nonzero-weight count. A short write-up goes in
`docs/phase2/SPECTRA_IMPROVEMENT_RESEARCH.md` and names the best value per
dataset. No Phase 1 file changes. Evidence tag `SIM`, zero metered seconds.

## Decision needed at approval

**D6: what the F132 guard test allows to name the Phase 1 repository.**
D2's three groups are in every option: `docs/paper/proposal.md` and
`appendix.md`; `experiments/results/call_logs/b5_then_b4_launcher.log`;
`SPRINT_1_SUMMARY.md`, `SPRINT_14_RETROSPECTIVE.md`,
`SPRINT_16_RETROSPECTIVE.md` and `docs/reviews/f36-float-tables-outcome.md`.
The files that must name it to block it are also in every option:
`.claude/hooks/block_cross_repo_write.py`,
`test_cross_repo_write_guard.py`, the new guard test, and `CLAUDE.md`'s
boundary rule.

1. Also allow the record files wholesale: `CHANGELOG.md`,
   `docs/ALL_SPRINTS_MASTER_PLAN.md` and everything under `docs/sprints/`.
   They record F127, the rename and Sprint 23, which cannot be described
   without the name. (recommended)
2. Allow no more files. Rewrite every line in `CHANGELOG.md`, the master
   plan and `docs/sprints/` (outside D2's history group) to say "the Phase 1
   repository" instead of its name.

## Deviations from the process

None. `SPRINT_23_SUMMARY.md` was written here at 3.2.1, as the Sprint 23
plan approved.

## Premise falsifiers

- If Task G shows no `min_samples_leaf` value beats HGB on any dataset
  within its CI, F129 is not justified by this lever. The write-up says so
  and F129 is re-scored at the next refinement.
- If Task E's first check finds a real hardware row without `job_id`, that
  is a data finding, not a test failure to work around. It stops Task E and
  goes to the team lead.

## Risks

- **F132 touches the cross-repo guard.** A wrong `FORBIDDEN` entry could
  block writes to this repository. The two-direction test covers it, and
  the rename means neither name contains the other.
- **F134 could block a legitimate commit** in a clone without the pattern
  file. That is the intended behavior. The message says how to restore the
  file, and there is no override flag.
- **F137 changes a dependency.** pypdf reads PDFs in tests only. The full
  suite runs after the bump.
- **CI goes red between this plan and approval.** `test_phase3_artifacts.py`
  requires a PR, issues and approval once the status is
  `phase_3_planning`. That red is expected. Any other failure goes to a
  background agent at the 3.3.2 checkpoint.

## Model assignments

Main loop for all tasks. Task G's run goes to the background with its
output file named in advance.

## Definition of Done

- Every task's acceptance criteria, as stated on its card, are met.
- Each new guard is proven to fail before it is trusted.
- The full suite passes locally, and CI is green on the final HEAD.
- Manual Validation items are listed on screen and saved in
  `SPRINT_24_VALIDATION.md`.
- Retrospective, `SPRINT_24_SUMMARY.md` at Sprint 25 planning, and the
  velocity log rows from measured start times.
