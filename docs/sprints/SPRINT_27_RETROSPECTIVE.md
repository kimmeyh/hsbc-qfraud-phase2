# Sprint 27 Retrospective

**Sprint**: 27, Gates Before Reporting, and the Screens That Need No Device
**Date**: 2026-10-19
**Scope**: F149 (A), F104 (B), F102 (C), F112 (D), F130 (E), F103 (F),
F109 (G), F6 (H), F106 (I), F107 (J), F108 (K), F146 draft (L). Issues
#33-44. Draft PR #32.
**Effort**: `.claude/sprint_status.json`, `task_actuals`, against the plan's
1,470 minutes. See category 3 for why the total is not a measure of work.
**Metered seconds**: 0. No Dirac, Braket or other paid service was called.

## Scoring, both roles

The team lead scored every category **Very Good**. Claude scored four
lower. Where the two disagree both are recorded, and the improvements are
built from the lower score.

| Category | Team lead | Claude |
|---|---|---|
| Effective while as efficient as reasonably possible | Very Good | **Good** |
| Testing approach | Very Good | **Good** |
| Effort accuracy | Very Good | **Poor** |
| Planning quality | Very Good | Very Good |
| Model assignments | Very Good | Very Good |
| Communication | Very Good | Very Good |
| Requirements clarity | Very Good | Very Good |
| Documentation | Very Good | Very Good |
| Process issues | Very Good | **Good** |
| Risk management | Very Good | Very Good |
| Next sprint readiness | Very Good | Very Good |
| Architecture maintenance | Very Good | Very Good |
| Assigned coding agents quality | Very Good | Very Good |

Team lead: "Manual Validation complete"; minor function updates "none";
backlog additions "none"; questions before ending the sprint "none". The
team lead sent the QCi questions (Task L) on 2026-10-18.

## Sprint 27 Retrospective Feedback

The team lead gave combined Product Owner, Scrum Master and Lead Developer
feedback, recorded verbatim under each of the three roles.

### 1. Effective while as Efficient as Reasonably Possible
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. All 12 tasks met their
  acceptance with zero metered seconds. Rework: F107's first run refused
  because F107 carried its own copy of F106's evaluation chunk size
  (4,096 against 8,192) and had to run again (IMP-2); the code review's
  F108 and F104 fixes arrived after those runs, although no recorded
  result changed (IMP-4); and a CRLF rewrite of `f130_levers.py` cost one
  failed injection (IMP-5).

### 2. Testing Approach
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. Every new guard was proven red
  with `assert_can_fail`, and two refusals fired as designed (F107's
  exact-AUPRC check, F106's projected-runtime rule). Two scripts shipped
  without a test: F112's, found by the code review, and
  `f102_downsized_pair.py`, found only at this retrospective. Nothing
  requires a new Phase 2 script to have a test (IMP-3).

### 3. Effort Accuracy
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Poor. 10 of 12 tasks ran with another
  task's timer open. 6 of 12 actuals are stamp gaps (A 8, B 9, C 5, H 8,
  K 12, L 3 minutes against 45-180 estimated), and 3 more (E, G, I) are
  elapsed background-run time, not work. All 12 timers started within 71
  minutes. Sprint 26 IMP-2 now records the overlap, which is why the
  velocity rows can say so, but it did not prevent it. I chose to start
  timers in a batch; the tool allowed it (IMP-1).

### 4. Planning Quality
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. Plan verification
  corrected six cards before they ran. F106's pilot rule cut its steps
  from 1,500 to 750 before the full run. One miss: F107's "critical rank
  per shot budget" is undefined for classical inputs, found at task
  start, not at plan verification; the change was recorded before the
  run.

### 5. Model Assignments
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. Main loop for the
  experiments and write-ups, long runs in the background, a code reviewer
  and a fresh-eyes reviewer with no sprint context.

### 6. Communication
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. Decisions were numbered
  lists; the validation items and the 14 QCi questions were listed to the
  screen. Two small misses: a velocity note claimed something I could not
  verify (replaced before commit), and commit messages did not cite issue
  numbers (the CHANGELOG lines name the task).

### 7. Requirements Clarity
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. D4 was not answered and
  option 1 applied, recorded as such.

### 8. Documentation
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. Every result names its
  file; readings added after a run (F108's main arm, F107's acceptance)
  carry dated notes saying so. The F109 card was retitled at the
  acceptance walk to match what ran.

### 9. Process Issues
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. Python `write_text` turned a
  source file into CRLF on Windows, which broke an injection target
  (IMP-5). `scripts/edb_query.py` crashed on a cp1252 console; the
  workaround was `PYTHONIOENCODING=utf-8` (IMP-6). The heredoc-escape
  hook blocked two edits and named the right route. `score_gates.py`
  writes the Phase 1 record on any invocation; I did not run it, and
  `test_evidence_immutability.py` would catch a write after the fact.

### 10. Risk Management
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. Zero metered seconds, as
  planned. F106's 3-hour limit and F107's exact-match refusal both fired
  before a wrong result was recorded.

### 11. Next Sprint Readiness
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. The QCi questions are
  sent; F150 waits on the authors. One open finding: the ULB HGB
  comparator is unstable (mean 0.22-0.52 AUPRC across settings), cause
  unverified, and it voids any "beats HGB on ULB" reading until it is
  explained (IMP-7).

### 12. Architecture Maintenance
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. `pair_count` is opt-in,
  with the default pool unchanged and proven equal; all new evidence is
  under `experiments/phase2/results/`; the locked files are unchanged.

### 13. Minor Function Updates for the Next Sprint Plan
- **Product Owner**: none
- **Scrum Master**: none
- **Lead Developer**: none
- **Claude Code Development Team**: none beyond the improvements below

### 14. Function Updates for the Future Backlog
- **Product Owner**: none
- **Scrum Master**: none
- **Lead Developer**: none
- **Claude Code Development Team**: [DEV] ULB HGB comparator instability
  -- estimated: 1.5h, priority: 20, depends on: none (IMP-7)

### 15. Assigned Coding Agents Quality
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. The code review found the
  F108 stopped-seed count and the F104 exit-code gap; the fresh-eyes
  review's 14 findings were each verified, then applied.

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
| IMP-1 | At most two task timers open | Cat 3 | Prevention: extends Sprint 26 IMP-2 in `update_sprint_status.py`. `--start-task` refuses while two tasks are timed, even with `--parallel` (one task worked, one run in the background); `SPRINT_CHECKLIST.md` Phase 4: a timer starts when the task's first file is touched | 20m | now |
| IMP-2 | One evaluation chunk size | Cat 1 | Prevention: `f106_dequant.py` names `PREDICT_CHUNK = 8192` and `predict()` defaults to it; `f107_shots.py` uses `fd.PREDICT_CHUNK` and drops its own constant. Test: F107 defines no chunk literal; proven red. Same value, so no recorded result changes | 15m | now |
| IMP-3 | Every Phase 2 script has a test | Cat 2 | Prevention: new guard test that each `experiments/phase2/src/*.py` is named by at least one test; tests added for `f102_downsized_pair.py` and `validate_emulator.py` so the guard starts with no exemptions; proven red | 45m | now |
| IMP-4 | Code review before an experiment's first full run | Cat 1 | Prevention: extends Sprint 26 IMP-3 in `SPRINT_EXECUTION_WORKFLOW.md`: the code-review pass on an experiment script runs at its "before the first run" commit, and the full run waits for the findings, unless the run is under 10 minutes | 10m | now |
| IMP-5 | Block `write_text` without `newline=` in inline Python | Cat 1, 9 | Prevention: extends `block_heredoc_escape_loss.py`, which already inspects heredoc Python. On Windows, `.write_text(` with no `newline=` rewrites LF files as CRLF; the hook names the Edit tool or `newline=""`. Two injections | 20m | now |
| IMP-6 | `edb_query.py` prints UTF-8 on any console | Cat 9 | Prevention at the source: the script reconfigures stdout and stderr to UTF-8 at start. Test with a non-ASCII row on a cp1252 stream; proven red | 10m | now |
| IMP-7 | ULB HGB comparator instability | Cat 11, 14 | Research card F151: find why default and tuned HGB range 0.06-0.70 AUPRC across ULB seeds when it was stable in F106 and strongest on F109's subsample; zero metered | 1.5h | backlog (F151, priority 20) |

## Improvement Decisions

Pending the team lead's disposition.
