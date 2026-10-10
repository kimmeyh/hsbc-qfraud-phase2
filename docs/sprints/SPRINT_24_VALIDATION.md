# Sprint 24 Manual Validation

**Sprint**: 24, Close the Boundary, Fix the Tooling, Sweep the Lever
**Branch**: `feature/20261008_Sprint_24` | **PR**: #2 (draft)
**Scope**: F131 (A), F136 (B), F132 (C), F134 (D), F133 (E), F135 (F),
F128 (G), F137 (H). Issues #3-10.
**Metered Dirac-3 seconds spent: 0.**

This file is the durable copy. The same items are listed to the screen at
handover: a pointer to a file is not a handover.

---

## V1. Task G (F128): the leaf sweep -- it decides what F129 would test

Read `docs/phase2/SPECTRA_IMPROVEMENT_RESEARCH.md`, section 6. Source:
`experiments/phase2/results/f128_leaf_sweep.json`, 60 cells, SIM, zero
metered seconds, no failed cell.

- **energy_steel: level on average, not seed by seed.** CVQBoost
  0.9699-0.9745 against HGB 0.9649; every CI includes zero. But CVQBoost
  loses on seeds 42, 43 and 46 at every value, and wins only on seeds 44
  and 45, where HGB is weak. The positive mean comes from HGB's weak seeds,
  not a consistent CVQBoost gain (found by the fresh-eyes review).
- **Between values**: 10 and 20 beat 50 on every seed; 5, 10 and 20 cannot
  be told apart. 20 (F124's value) is as good as any.
- **oilgas: every value loses** by 0.028-0.046; every CI excludes zero.
- **telecom: every value loses** by 0.11-0.16; every CI excludes zero.
- **The plan's premise falsifier fired.** No value beats HGB with a CI that
  excludes zero anywhere. It is recorded on F129 for re-scoring at the next
  refinement. F129's narrower question (does the device reproduce the proxy
  on a sparse problem?) stands; its case as a route to advantage does not.
- **Selection caveat.** The highest-scoring value (`highest_test_auprc_leaf`)
  is chosen on the test splits it is reported on. The code review caught
  that the first version called it "best"; it was corrected before commit,
  and the summary was rebuilt from the stored rows without a re-run.

Spot-check: `summary.spectra_energy_steel` in the result file.

## V2. Task C (F132): the Phase 1 boundary

- The cross-repo hook now blocks writes to the Phase 1 repository. Try it:
  ask any session in this repository to write a file there; it is refused.
  Reads still work.
- `git grep -i` for the Phase 1 name finds it only in the D2 and D6 files:
  the submitted proposal and appendix, the launcher log, the history
  records, `CHANGELOG.md`, the master plan, `docs/sprints/`, the hook and
  `CLAUDE.md`'s boundary rule. `test_phase1_boundary.py` enforces this.
- **A side effect to know about.** The hook's `sed -i` rule matches the
  name anywhere in a `sed -i` command, including inside the sed expression.
  So `sed -i` cannot edit text that mentions the Phase 1 repository; the
  Edit tool can. The sibling rules have always behaved this way. Recorded
  for the retrospective, not changed.
- Three untracked files still name the Phase 1 repository and were left
  alone: two QCi correspondence files in `docs/qci_package/` (records of
  what was sent) and `experiments/results/campaign_run.log` (a run log).

## V3. Tasks A, D, E: three guards, each proven able to fail

- **A (F131)**: a full suite run no longer changes
  `scripts/check_ci_status.py`. Check: run the suite, then `git status`.
- **D (F134)**: a commit in a clone with no `.secrets-patterns.txt` is
  blocked, with a message saying how to restore the file. Check: in a
  scratch clone, commit anything before copying the file.
- **E (F133)**: Phase 2 device rows and the 10 `device_samples/` files must
  carry a `job_id`. All real files pass today.

## V4. Tasks B and F: two process rules

- **B (F136)**: `update_sprint_status.py --start-task X` / `--finish-task X`.
  Tasks C to H of this sprint were timed with it. Task A's start was taken
  from the clock by hand; Task B's start was typed by hand before the tool
  existed, so its 1-minute actual is not fully measured.
- **F (F135)**: `CLAUDE.md` now says every decision option names its
  concrete values.

## V5. Task H (F137): pypdf

- `experiments/requirements-lock.txt` pins `pypdf==6.20.0` (was 6.17.0).
- The venv was reinstalled from the lock; a dry run showed pypdf was the
  only change. `pip-audit` now reports no known vulnerabilities. The full
  suite passed on the new version.
- Worth knowing: CI installs from `requirements.txt` (`pypdf>=4.0`), not the
  lock file, so CI was already using a current pypdf. The lock file governs
  local clones.

## V6. What the code review found and what was done

A background review of the sprint's code reported 6 findings (no critical,
no high). All 6 were verified against the code and fixed:

1. F128 named its top value "best" though it was chosen on the test split:
   renamed, with a caveat (V1).
2. F128 could rank values over different seed subsets: ranking now needs
   every value complete on every seed.
3. F133's job-id check skipped device files it could not read: they are
   now reported, and subdirectories are scanned.
4. The Phase 1 boundary test had no proof it could detect anything: an
   injected-offender test was added and proven able to fail.
5. The WSL scripts' "wrong directory" guard could no longer fire: they now
   check that they landed in the repository root.
6. The F128 result recorded no generator identity: it now carries the
   generator's SHA-256, which matches the committed file.

## V7. What the fresh-eyes evidence review found

A fresh-context reviewer read the F128 result file and the write-up. It
recomputed all 12 summary cells from the rows and matched them; no figure
was wrong. Its 8 findings were about interpretation, and the write-up was
revised for all of them. The two that matter: the energy_steel "parity" is
an average over a 3-loss, 2-win split (V1), and "the values cannot be told
apart" was too strong, since 50 is measurably worse.

## Acceptance criteria, walked

- **F131**: the suite never writes the tracked script, asserted by bytes in
  every stubbed run and by its own test; two full suite runs left
  `git status` clean; `assert_can_fail` proved the red-CI hook test and the
  byte test can fail. MET.
- **F136**: start stamped, actual computed (`task_started`,
  `task_actuals`); workflow Phase 4 and the checklist name the commands; the
  velocity log says which rows are measured. MET.
- **F132**: the new test fails on a tracked file outside the D2/D6 list,
  proven red twice (a real file and an injected one); the hook blocks a
  Write and a shell write to the Phase 1 path and allows them here, proven;
  the four scripts resolve this clone (`us_english_fix.py` run here: 184
  files scanned in this clone, 0 changes, the Phase 1 clone's status
  unchanged; the WSL scripts' root checked under WSL). MET.
- **F134**: a commit with no pattern file is blocked with a message naming
  the file and how to restore it; proven red against the old gate; no
  override flag. MET.
- **F133**: device rows and device-sample files must carry a nonempty
  `job_id`; proven red with `assert_can_fail` on injected files. MET.
- **F135**: the `CLAUDE.md` sub-rule exists, with the Sprint 23 example.
  MET.
- **F128**: dated result file with all 60 cells, the paired difference
  against HGB with its CI per dataset and value, the train-test gap and
  nonzero-weight count beside every AUPRC, and a stated top value per
  dataset (with its selection caveat); no Phase 1 file touched. MET.
- **F137**: lock pinned to 6.20.0, venv reinstalled, `pip-audit` clean,
  full suite passed. MET.

## Effort, measured

Actuals from `task_started` (Task A's start was taken from the clock; Task
B's was typed by hand before the tool existed):

- A (F131) 3 min, estimate 30
- B (F136) 1 min, estimate 20
- C (F132) 12 min, estimate 90
- D (F134) 2 min, estimate 30
- E (F133) 2 min, estimate 40
- F (F135) 1 min, estimate 10
- G (F128) 29 min, estimate 50 plus about 35 runtime; includes the 26-minute
  run and overlaps Task H
- H (F137) 34 min, estimate 20; it waited on the sweep, because it
  reinstalls into the venv the sweep was using
- Unplanned, not task-timed: the code review and its six fixes, and the
  fresh-eyes evidence review
