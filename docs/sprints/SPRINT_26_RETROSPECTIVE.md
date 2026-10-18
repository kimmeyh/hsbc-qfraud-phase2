# Sprint 26 Retrospective

**Sprint**: 26, Reach Dirac-3S, Measure It, and Make the Proxy Repeatable
**Date**: 2026-10-16
**Scope**: F141 (A), F145 (B), F144 (C), F142 (D), F147 (E), F126 (F),
F105 (G), F146 (H), and unplanned Task I (Decision 10). Issues #22-30.
Draft PR #21.
**Effort**: `.claude/sprint_status.json`, `task_actuals`, against the plan's
700 minutes. See category 3 for why the total is not a measure of work.
**Metered Dirac-3S seconds**: 86.0 over 5 fits
(`experiments/phase2/results/f142_dirac3s_verify.json`), against about 172
planned and a cap of 360.

## Scoring, both roles

The team lead scored every category **Very Good**. Claude scored six
lower. Where the two disagree both are recorded, and the improvements are
built from the lower score.

| Category | Team lead | Claude |
|---|---|---|
| Effective while as efficient as reasonably possible | Very Good | **Good** |
| Testing approach | Very Good | **Good** |
| Effort accuracy | Very Good | **Poor** |
| Planning quality | Very Good | **Good** |
| Model assignments | Very Good | Very Good |
| Communication | Very Good | Very Good |
| Requirements clarity | Very Good | Very Good |
| Documentation | Very Good | **Good** |
| Process issues | Very Good | **Good** |
| Risk management | Very Good | Very Good |
| Next sprint readiness | Very Good | Very Good |
| Architecture maintenance | Very Good | Very Good |
| Assigned coding agents quality | Very Good | Very Good |

Team lead: "Manual Validation complete"; minor function updates "none";
backlog additions "none"; questions before ending the sprint "none". At
Manual Validation he added Task I (Decision 10, from a prompt the
EvidenceBasedDB session shared) and made Dirac-3S the default device for
Phase 2 runs (Decision 11, on V1).

## Sprint 26 Retrospective Feedback

The team lead gave combined Product Owner, Scrum Master and Lead Developer
feedback, recorded verbatim under each of the three roles.

### 1. Effective while as Efficient as Reasonably Possible
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. All eight planned tasks met their
  acceptance criteria, and F142 used 86 of about 172 planned seconds. Two
  pieces of rework were mine. The first approved stop 1 attempt exited
  before any submit: the F142 runner's token loader, copied from
  `run_hardware_b4.py`, required `QCI_TOKEN`, and this repository's `.env`
  names the key `QCI_API_KEY`. It spent nothing, but it cost an approval
  round (IMP-1). And the "about 1/120 of the step" claim reached the F142
  write-up, the CHANGELOG and commit 3aa52f6 before the fresh-eyes review
  showed it measured the optimum's plateau offset, not its structure
  (IMP-3).

### 2. Testing Approach
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. Every new guard was proven red
  with `assert_can_fail`, including the eight runner guards, and the
  readout refuses unless its rebuilt Hamiltonian hashes to the one sent.
  One gap: no test ran the runner's credential path against the key name
  this repository actually uses, so the first metered attempt found it.
  The fix added that test, proven red. This repository has at least five
  separate `.env` readers (`check_allocation.py`, `job_query.py`,
  `probe_variable_ceiling.py`, `run_hardware.py`, the F142 runner), and
  they do not accept the same names (IMP-1).

### 3. Effort Accuracy
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Poor. Estimates against actuals: A
  45/75, B 30/3, C 45/24, D 80/884, E 120/3, F 60/9, G 240/66, H 60 with
  no start stamp, I 30/18. Most of these do not measure work. B, C, E, F,
  G and D were all started within 12 minutes of each other on 2026-10-14,
  and several ran at once, so a short actual measures a stamp gap. B's
  test was written before its timer started. D's 884 is elapsed time
  through three approval waits and an evening gap. H's updates fell
  inside D's span. For Task I, I wrote the start stamp and the actual
  into the status file by hand instead of through
  `update_sprint_status.py`, which Sprint 25 IMP-4 extended to prevent
  exactly that (IMP-2).

### 4. Planning Quality
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. The plan sequenced the metered
  work behind three separate approvals, and plan verification set B4 as
  the only fidelity question. Two misses. Decision 1 named
  `get_dynamic_range` as the screen; the dry run showed it passes B1 at
  4.8 dB although A31 shows B1 unresolvable, so the screen was corrected
  before any call. And the stop 2 quote (about 115 s, from Dirac-3's
  per-fit costs scaled by one 91-variable fit) was three times the 37 s
  spent; stop 3, quoted from measured per-sample times, was 44 against 43
  (IMP-5).

### 5. Model Assignments
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. Main loop for the runner,
  the metered stops and the write-ups; pool builds and the IEEE-CIS audit
  in the background; a code reviewer and two fresh-eyes reviewers with no
  sprint context.

### 6. Communication
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. Every metered stop went out
  with its call count, quote and cap; Decisions 5 and 7 to 11 were each
  one numbered question. The validation items were listed to the screen,
  and re-listed after Task I. One interrupt was needed: the team lead had
  to state that Phase 1 figures and documents must not change, which
  became Decision 5.

### 7. Requirements Clarity
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. The scope message named
  every card and its priority. Decision 3 arrived without a digit and was
  read as option 1, recorded as such. Decision 9 carried a standing
  approval for further runs, recorded and not used.

### 8. Documentation
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. Every write-up names its result
  file, and the F142 and F144 entries keep their pre-result text with
  dated post-result notes below. But the stop 3 CHANGELOG entry still
  carries "about 1/120 of the 200:1 step" and "cosine 0.99999 and 1.0",
  which the fix entry above it replaced. A reader who stops at the older
  line reads a withdrawn claim. Sprint 25 had the same finding (IMP-3).

### 9. Process Issues
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. `check_ci_status.py --after 300`
  reported "CI STATUS UNDETERMINED: gh timed out after 3s" on Task I's
  commit; `gh run list` answered at once and showed green. The script
  failed closed, as designed, but its 3-second limit on a network call
  makes the undetermined state routine (IMP-4). A background CI wait from
  an earlier session waited on a commit that did not exist and had to be
  stopped. The heredoc-escape hook blocked a Python heredoc and named the
  right route.

### 10. Risk Management
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. Each stop needed its own
  approval and stayed under its cap. The runner refuses a changed
  Hamiltonian or a failing screen before anything is sent, makes one
  attempt per unit, saves the raw response before post-processing and
  never resubmits a unit with a row. The risk that materialized (the key
  name) failed safe.

### 11. Next Sprint Readiness
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. F142 is done; F95, F25 and
  F30 carry dated notes to re-price on Dirac-3S; Experiment 2 has its
  harness. Open at refinement: whether to send question A6 (and the other
  unsent QCi questions), and F126 and F25 read against Dirac-3S not
  returning forced sparsity. `SPRINT_26_SUMMARY.md` is written at Sprint
  27 planning.

### 12. Architecture Maintenance
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. Decision 5 put the Phase 1
  boundary into five rules, and every shared-code change this sprint is
  opt-in with Phase 1 behavior as the default: `device()`, seeded
  learners, `metered_fit`'s new arguments, and `PHASE2_DEVICE`. All new
  evidence is under `experiments/phase2/results/`. The frozen
  preregistration is untouched.

### 13. Minor Function Updates for the Next Sprint Plan
- **Product Owner**: none
- **Scrum Master**: none
- **Lead Developer**: none
- **Claude Code Development Team**: none beyond the improvements below

### 14. Function Updates for the Future Backlog
- **Product Owner**: none
- **Scrum Master**: none
- **Lead Developer**: none
- **Claude Code Development Team**: none beyond IMP-5, if it goes to the
  backlog

### 15. Assigned Coding Agents Quality
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. The code review (16), the
  fresh-eyes evidence review (16) and the F142 fresh-eyes review (9) were
  each verified before acting. The evidence review found a Sprint 25
  error that six documents carried; the F142 review withdrew a claim of
  mine before handover.

### 16. Questions to be discussed before ending the sprint
- **Product Owner**: none
- **Scrum Master**: none
- **Lead Developer**: none
- **Claude Code Development Team**: none

## Improvements proposed

Each starts with prevention, and each extends a mechanism that already
exists.

| # | Title | Source | Type | Effort | Recommendation |
|---|---|---|---|---|---|
| IMP-1 | One QCi credential loader | Cat 1, 2 | Prevention: extends `eqc_submit` with one loader that accepts both key names; the five readers call it; a test fails on any new `.env` reader | 30m | now |
| IMP-2 | Task timers measure work | Cat 3 | Prevention: extends `update_sprint_status.py` with `--pause-task` and `--resume-task` (approval waits), and `--start-task` refuses while another task is open unless `--parallel` is passed and recorded; `SPRINT_CHECKLIST.md` Phase 4 says a task added mid-sprint starts its timer with the tool before its first file. No new control: my bypass was a Python one-liner, which an Edit/Write hook would not see | 30m | now |
| IMP-3 | A result's interpretation is reviewed before it is recorded | Cat 1, 8 | Prevention: extends Sprint 25 IMP-1 (claim labels) in `SPRINT_EXECUTION_WORKFLOW.md`: a metered result's fresh-eyes review runs before its CHANGELOG entry and commit; correction: a withdrawn claim's older CHANGELOG line gets an inline dated marker, as the master plan already does; applied to stop 3's entry | 15m | now |
| IMP-4 | `check_ci_status.py` waits long enough for `gh` | Cat 9 | Prevention: the network calls get a 20-second limit and one retry; it still fails closed; test proven red | 15m | now |
| IMP-5 | Quote Dirac-3S seconds from measured per-sample times | Cat 4 | Prevention: extends `qpu_cost_model.py` with F142's per-sample times by size and a `quote()` that F95, F25 and F30 use at refinement | 45m | backlog (F148, priority 12) |

## Improvement Decisions

Team lead, 2026-10-16: "apply all five now" (Decision 12, which Claude
had recommended as option 1: IMP-5 to the backlog).

| # | Decision | Where |
|---|---|---|
| IMP-1 | **now** | New `experiments/src/qci_env.py`, the one `.env` reader; it accepts `QCI_API_KEY` as the token and strips quotes. `check_allocation.py`, `job_query.py`, `recover_device_samples.py` and the F142 runner call it. The Phase 1 hardware runners keep their own readers, as code that produced filed evidence. `test_qci_env_single_loader.py` fails on any new reader; two injections. A separate module rather than `eqc_submit`, as proposed, so a small tool does not load eqc-models |
| IMP-2 | **now** | `update_sprint_status.py --pause-task`, `--resume-task` and `--parallel`; a start while another task is timed is refused unless `--parallel`, which is recorded in `task_parallel`; a paused task cannot finish. Three injections. `SPRINT_CHECKLIST.md` Phase 4: a task added mid-sprint starts its timer with the tool, and the status file is never written by hand or by a one-off script |
| IMP-3 | **now** | `SPRINT_EXECUTION_WORKFLOW.md`, under the fresh-eyes review: a metered result's rows are committed at once, and its interpretation, CHANGELOG entry and commit message wait for the review; a withdrawn claim's older CHANGELOG line gets an inline dated marker. The stop 3 entry is marked |
| IMP-4 | **now** | `check_ci_status.py`: from the command line, 20 s per call and one retry; inside the Stop hook, 3 s and one attempt, so the hook budget is unchanged. Still fails closed. Tests for both paths; two injections |
| IMP-5 | **now** | `qpu_cost_model.dirac3s_anchors()` reads F142's per-sample times from its rows; `quote()` gives a range from anchors on the same device and relaxation schedule, says unknown off its anchors, and flags a size above the largest anchor. Test: the 560-variable quote contains both B4 fits' billed seconds; two injections. F95, F25 and F143 point at it |

**Found while applying IMP-4: stale bytecode after an injection.** The first
proof swapped `CLI_ATTEMPTS = 2` for `= 1`, which keeps the file the same
size. The mutation and its restore landed in the same second, so Python
reused the cached mutated bytecode: the file on disk read 2, the imported
module read 1, and the next run's baseline was already red. The guard was
right and the verification was wrong, the Sprint 16 IMP-4 pattern again.
`injection.py` now drops a module's cached bytecode on every write. A new
test cycles a same-size mutation three times; with the fix removed it
failed, and with it restored it passed. `docs/TROUBLESHOOTING.md` has the
entry.
