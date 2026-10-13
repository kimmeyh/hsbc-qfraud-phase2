# Sprint 25 Retrospective

**Sprint**: 25, Learn the New Device, Then Build What Runs on Any Device
**Date**: 2026-10-13
**Scope**: F138 (A), F139 (B), F102 (C), F113 (D), F29 (E), F94 (F), and
Task G (F146, F147), added at Manual Validation. Issues #13-19. Draft PR
#12.
**Effort**: 172 measured minutes against 750 estimated
(`.claude/sprint_status.json`, `task_actuals`). The three reviews, their
fixes and Task G were not timed.
**Metered Dirac-3 seconds**: **0**.

## Scoring, both roles

The team lead scored every category **Very Good**. Claude scored six
lower. Where the two disagree both are recorded, and the improvements are
built from the lower score.

| Category | Team lead | Claude |
|---|---|---|
| Effective while as efficient as reasonably possible | Very Good | **Good** |
| Testing approach | Very Good | Very Good |
| Effort accuracy | Very Good | **Fair** |
| Planning quality | Very Good | **Good** |
| Model assignments | Very Good | Very Good |
| Communication | Very Good | **Good** |
| Requirements clarity | Very Good | Very Good |
| Documentation | Very Good | **Good** |
| Process issues | Very Good | **Good** |
| Risk management | Very Good | Very Good |
| Next sprint readiness | Very Good | Very Good |
| Architecture maintenance | Very Good | Very Good |
| Assigned coding agents quality | Very Good | Very Good |

Team lead: "Manual Validation complete"; minor function updates "none";
backlog additions "none"; questions before ending the sprint "none". At
Manual Validation he also asked for the Dirac-3 and Dirac-3S
understandings document (F146) and the evidence-library tool card (F147),
and closed F129.

## Sprint 25 Retrospective Feedback

The team lead gave combined Product Owner, Scrum Master and Lead Developer
feedback, recorded verbatim under each of the three roles.

### 1. Effective while as Efficient as Reasonably Possible
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. All six tasks met their
  acceptance criteria with zero metered seconds, and F138 held its gate: no
  Dirac-3 second was spent before the research reported. But the reviews
  changed four conclusions I had already committed: F113's falsifier could
  not have fired; F29's mechanism was the learners' agreement, not the
  ridge; F139's B1, B2 and B4 recommendations were revised; and F94's
  objective floor and SCIP's gap reading came from the reviewer. The F94
  run was stopped twice, once because the training-fold instances tied.
  Sprint 24 had the same pattern (8 overclaims in one write-up). The
  overclaims were mine (IMP-1).

### 2. Testing Approach
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. Every new guard was proven
  red with `assert_can_fail`. Two of my first tests stayed green under
  mutation (the greedy test and the oracle-half test); the proof caught
  both, and each was replaced by a test that fails (an m=1 case, a
  hand-built greedy reference, annealing reaching the optimum, a
  constructed legitimate-half case). SCIP was checked against brute-force
  enumeration before any SCIP result was trusted.

### 3. Effort Accuracy
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Fair. A 16/120, B 5/120, C 5/120,
  D 5/90, E 12/60, F 129/240: 172 minutes against 750, a ratio of 0.23,
  close to Sprint 24's 0.29. The writing tasks (B, C, D) ran at 0.04-0.06
  because their research had already been done by A's background sweep. The
  untimed review-and-fix work was larger than several timed tasks, so the
  ratio understates the sprint's real effort. Timing the reviews was
  declined in Sprint 24 and is not re-proposed.

### 4. Planning Quality
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. Plan verification paid for
  itself: it corrected F94's sizes from synthetic probes (60 and 150) to
  real pools (60 and 136), and a spike proved SCIP before approval. Two
  misses, both premise checks that `SPRINT_PLANNING.md` already requires
  ("a check that cannot fail is not evidence"): F113's 1-point falsifier
  also passes between two XGBoost configurations (3.6 points), so it could
  not separate a router from noise; and F94's instances were built on the
  training fold, where every method ties, so the controls could not be
  compared. Both were discoverable from data on disk before approval
  (IMP-2).

### 5. Model Assignments
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. Main loop for all tasks;
  the QCi site sweep and the E and F runs in the background; a code
  reviewer and two fresh-eyes reviewers with no sprint context found what
  the main loop missed.

### 6. Communication
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. Decisions went out as numbered
  lists, one per question, and the validation items were listed to the
  screen. One miss: I read "qip" as a website, checked the Phase 1 site,
  and asked a question about it; it meant the Quantum Insider Phase 1
  session. One question round was spent.

### 7. Requirements Clarity
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. The scope message named
  every card and its dependency (F139 after F138), canceled F140 with its
  reason, and stated that F102 is a living draft. D2, D3 and D4 were each
  answered with one digit.

### 8. Documentation
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. Every write-up names its result
  file, and each result file records its generator's SHA-256. But three
  CHANGELOG entries and one commit message (066802a, "pinned at uniform by
  the ridge") state conclusions the later fix entry corrected. The F29 note
  records the correction; the earlier CHANGELOG lines still read as current
  to a reader who stops there.

### 9. Process Issues
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. `block_cross_repo_write.py`
  blocked a file inside this repository because its name contained
  "EvidenceBasedDB": its path check matches the name anywhere in the path.
  It is the guard's second false positive after Sprint 24's `sed -i` case
  (IMP-3). `update_sprint_status.py` cannot add an issue to
  `github_issues`, so #19 is missing from the status file (IMP-4). The
  heredoc-escape and shell-metacharacter hooks each blocked commands; their
  messages named the right route every time.

### 10. Risk Management
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. The F138 gate held: zero
  device seconds before the research. SCIP ran under a 600 s cap per
  instance and reported its gap rather than hanging. A new risk was found
  and carded: the pool build is not reproducible from its seed (F145), so
  any result that rebuilds a pool can drift by about 0.001 AUPRC.

### 11. Next Sprint Readiness
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. F141, F142, F144, F145 and
  F147 are carded with priorities, F146 is permanent HOLD, and F129 is
  closed. Open at refinement: F121's new hold condition, and whether the
  twelve QCi questions are sent. `SPRINT_25_SUMMARY.md` is written at
  Sprint 26 planning.

### 12. Architecture Maintenance
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. No preregistration drift;
  every Sprint 25 result is a dated Phase 2 `SIM` row; the frozen
  preregistration is untouched. The exact solver sits behind an
  `ExactSolver` interface so a commercial solver can replace SCIP, and
  `pyscipopt` is pinned and covered by the requirements guard.

### 13. Minor Function Updates for the Next Sprint Plan
- **Product Owner**: none
- **Scrum Master**: none
- **Lead Developer**: none
- **Claude Code Development Team**: none beyond the improvements below

### 14. Function Updates for the Future Backlog
- **Product Owner**: none
- **Scrum Master**: none
- **Lead Developer**: none
- **Claude Code Development Team**: F146 and F147, carded at the team
  lead's request during Manual Validation; F141-F145, carded by F139 and
  F29 during the sprint

### 15. Assigned Coding Agents Quality
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. The site sweep returned 71
  findings, each with a URL and a verbatim quote; one carried a local home
  path, which I removed before commit. The reviewers' 10, 24 and 15
  findings were each verified, and each was addressed.

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
| IMP-1 | Label each bottom-line claim, and name the alternative an inferred mechanism did not rule out | Cat 1, 8 | Prevention: extends the labels started in `DIRAC_UNDERSTANDINGS.md` (Measured, Inferred) into the Phase 2 draft's reporting standard | 15m | now |
| IMP-2 | Show at plan verification that each premise falsifier can fire | Cat 4 | Prevention: extends `SPRINT_PLANNING.md`'s premise-falsifier rule and the 3.2.2.1 verification with a reference comparison run on data already on disk | 10m | now |
| IMP-3 | The cross-repo guard matches a path component, not a substring | Cat 9 | Prevention: fix `check_path` in `block_cross_repo_write.py`; tests for both directions, proven red; removed from F147 | 20m | now |
| IMP-4 | `update_sprint_status.py --add-issue N` | Cat 9 | Prevention: extends the status tool so the list is never hand-edited; test proven red | 15m | now |

## Improvement Decisions

Team lead, 2026-10-13: "apply all now".

| # | Decision | Where |
|---|---|---|
| IMP-1 | **now** | `experiments/phase2/PREREGISTRATION_DRAFT.md` section 2: every bottom-line claim labeled Measured, Inferred or Unverified; an inferred mechanism names the alternative it did not rule out |
| IMP-2 | **now** | `docs/SPRINT_PLANNING.md` premise-falsifier rule and `SPRINT_EXECUTION_WORKFLOW.md` 3.2.2.1: each falsifier is run once on a reference comparison where it should not fire, and the result recorded in the plan |
| IMP-3 | **now** | `block_cross_repo_write.py` `check_path` matches a folder name, case-insensitive, not a substring; four new cases in `test_cross_repo_write_guard.py`, and both the substring and the case-fold mutations proven red with `assert_can_fail`; removed from F147 |
| IMP-4 | **now** | `update_sprint_status.py --add-issue N`; tests proven red under three mutations (duplicate, unsorted, nonpositive); #19 added to `github_issues` with it |

The first IMP-3 proof removed only one of the two case folds and stayed
green: the comparison was still lower case on both sides. The proof caught
the defect in the mutation, not in the guard; the mutation now removes
both.

**IMP-3 follow-up, from the automated security review of 2af9045.** The
exact folder match was weaker than the substring match it replaced in one
way: Windows opens `name.`, `name ` and `name:stream` as the folder `name`,
and resolves 8.3 short names and junctions, so those spellings would have
passed. Each folder is now canonicalized (trailing dots and spaces
stripped, a stream suffix dropped, case folded), and the path is also
checked after `os.path.realpath`. Three new BLOCK cases, proven red with
both defenses removed (on Windows `realpath` alone also strips the dots
and spaces, so removing one defense stays green; on Linux CI only the
canonicalization applies). 8.3 names and junctions rely on `realpath` and
have no test, because they need real folders of that kind on disk.
