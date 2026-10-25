# Sprint 28 Retrospective

**Sprint**: 28, Experiment Entries First, Then Their First Measurements
**Date**: 2026-10-24
**Scope**: F154 (F), F115 (I), F151 (A), F13 (J), pypdf (L), F146 (K),
F150 (H), F114 (G), F152 (B), F153 (C), F110 (E), F111 (D), F162 (M, added
at Manual Validation). Issues #47-59. Draft PR #46. Also D4 (storage
prevention), added at Manual Validation: 39f9943 and fe07674.
**Effort**: `.claude/sprint_status.json`, `task_actuals`, against the plan's
1,030 minutes plus F162's 90. See category 3.
**Metered seconds**: 0. No Dirac, Braket or other paid service was called.

## Scoring, both roles

The team lead scored every category **Very Good**. Claude scored six
lower. Where the two disagree both are recorded, and the improvements are
built from the lower score.

| Category | Team lead | Claude |
|---|---|---|
| Effective while as efficient as reasonably possible | Very Good | **Good** |
| Testing approach | Very Good | **Good** |
| Effort accuracy | Very Good | **Poor** |
| Planning quality | Very Good | Very Good |
| Model assignments | Very Good | Very Good |
| Communication | Very Good | **Good** |
| Requirements clarity | Very Good | Very Good |
| Documentation | Very Good | **Good** |
| Process issues | Very Good | **Good** |
| Risk management | Very Good | Very Good |
| Next sprint readiness | Very Good | Very Good |
| Architecture maintenance | Very Good | **Good** |
| Assigned coding agents quality | Very Good | Very Good |

Team lead: "Manual Validation complete"; minor function updates "none";
backlog additions "none"; questions before ending the sprint "none".

## Sprint 28 Retrospective Feedback

The team lead gave combined Product Owner, Scrum Master and Lead Developer
feedback, recorded verbatim under each of the three roles.

### 1. Effective while as Efficient as Reasonably Possible
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. All 13 tasks met their
  acceptance with zero metered seconds, and F162 answered the in-pocket
  question the same day it was carded. Rework: the four PR #46 reviews
  returned 46 findings, plus one Copilot thread, fixed in 28bdbcd, a78901b
  and f98ea2f. CI ran red on eight consecutive commits (39f9943 to f98ea2f,
  3 hours 41 minutes) because a docstring in `device_store.py` named the
  device call that `test_phase2_device_default.py` matches as text; fixed
  in fe07674. One injection mutation in `f111_loke_protocol.py` made its
  test run the real experiment; the process was stopped, no result file
  changed, and the test was made unable to start real work.

### 2. Testing Approach
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. Every new guard was proven red
  with `assert_can_fail`, and `InjectionError` caught two mutations whose
  new text kept the old. Gaps: four reviewers independently found that
  the outcome exempt list could grow by 14 names while its test stayed
  green (a count ceiling, not a content pin). Three compound decision
  rules had no test in which only one term fails: F153's two-part guide
  check, F151's range term (it cannot decide anything at five seeds), and
  F152's bootstrap, tested only against itself. While preparing this
  retrospective, Claude found the same grow-able shape in its own
  `test_device_store_required.py` (39f9943): `PHASE2_NOT_SUBMITTING` has
  no pin at all, `PHASE1_FROZEN` can take a new name if its count is
  raised, `PHASE2_SUBMIT_BEFORE_RULE` checks only `<= 1`, so a swap
  passes, and `UNSEEDED_BEFORE_RULE` checks only the total, so counts can
  move between modules (IMP-1). The first version of D4 part 3 had the
  same count-only pin; it was replaced with a hash pin before commit.

### 3. Effort Accuracy
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Poor. 572 measured minutes against
  1,120 estimated (ratio 0.51), and the total is not a measure of work.
  Per task, actual over estimate: F 12/190, I 3/45, A 8/50, J 4/75, L 2/45,
  K 1/45, H 1/30, G 8/60, B 46/110, C 70/150, E 198/100, D 180/130, M
  39/90. K and H read 1 minute because their timers started at the
  commit, after the work. E and D are wall clock dominated by background
  runs. F111's runtime projection was about 10 times the 82.5 minutes of
  lane time the run recorded. D4, the largest piece of Phase 6 work, had
  no timer and no issue (IMP-4). Pattern as in Sprint 27: research and
  documentation cards finish at 0.02-0.47 of estimate; runs land at
  1.4-2 times when the cell is new.

### 4. Planning Quality
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. Decisions 1-6 were settled
  before execution and every experiment entry was committed before its
  first score. The plan's "Show each threshold can fire" rule (Sprint 25
  IMP-2) was applied to the data and not to the tests, which is where the
  three compound-rule findings came from (IMP-5).

### 5. Model Assignments
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. Opus review agents found
  real defects, each with a file, a line and a failing scenario; the fix
  agents worked in bounded file sets; the main loop kept the experiment
  runs and every metered decision.

### 6. Communication
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. D4 parts 1 and 2 and the F162
  work were reported done while CI was red and unchecked; the red was
  found only by the full-suite run before fe07674. The Javier reply and the
  leak analysis were stated with what was measured and what was inferred.

### 7. Requirements Clarity
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. The team lead corrected the
  D4 directive's wording before it was built ("so results can be
  reproduced and compared over time"). Javier's answer settled the label
  question that the construction request had planned to ask.

### 8. Documentation
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. Seven review findings were
  document figures or labels that the result files do not support: F111's
  95-minute wall clock (not recorded), F110's clamp cause, the "776 of
  950" denominator label, F151's second failing reason, F114's scope,
  F146 P1 still listed open, and a range endpoint. All corrected in
  28bdbcd. `test_document_figures_resolve.py` checks only `docs/paper/`,
  so nothing checks the Phase 2 documents (IMP-7).

### 9. Process Issues
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. CI ran red unnoticed between
  the 3.3.2 checkpoint and the 7.0 checkpoint, which are the only two the
  process names (IMP-2, IMP-3). D4 was built without an issue or a timer,
  although `SPRINT_CHECKLIST.md` Phase 4 requires both for a task added at
  Manual Validation (IMP-4). Hooks worked as designed: a heredoc escape,
  a `$(...)` in a Python command, one code commit without a CHANGELOG
  entry and one typed footer were each blocked. One agent stopped at the
  session limit mid-work and finished after a resume.
  `docs/TROUBLESHOOTING.md` gains the docstring entry (IMP-2).

### 10. Risk Management
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. Zero metered seconds. The
  SPECTRA confusion matrices were traced to a copied label column, and
  this repository was shown clean: the leak-free contract in
  `spectra_segment`, every recorded feature list, and the dataset hashes.
  D4's storage rule is in place before any Phase 2 device run.

### 11. Next Sprint Readiness
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. F161 is carded with its
  run condition; F162 removed the pocket's case for a device block; the
  construction request is drafted as a reply for the team lead to send.

### 12. Architecture Maintenance
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. `device_store.py` and
  `provenance.py` give every future device job and result one stored,
  rebuildable form, and Phase 1 code stayed default-preserving. The guards
  that hold them use frozen lists that can still grow (IMP-1).

### 13. Minor Function Updates for the Next Sprint Plan
- **Product Owner**: none
- **Scrum Master**: none
- **Lead Developer**: none
- **Claude Code Development Team**: none beyond the improvements below.

### 14. Function Updates for the Future Backlog
- **Product Owner**: none
- **Scrum Master**: none
- **Lead Developer**: none
- **Claude Code Development Team**: IMP-6 and IMP-7 below, carded only
  if the team lead disposes them to the backlog.

### 15. Assigned Coding Agents Quality
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. The fix agents' work held
  up under the suite and their own red proofs. One agent stopped at the
  session limit and finished after a resume, with nothing lost.

### 16. Questions to be discussed before ending the sprint
- **Product Owner**: none
- **Scrum Master**: none
- **Lead Developer**: none
- **Claude Code Development Team**: none

## Review finding classes (input to the improvements)

- **Shrink-only list that can grow** (4 reviewers, Copilot, and this
  retrospective's own find in `test_device_store_required.py`): recurring.
  IMP-1.
- **Document figure not supported by its result file** (7): recurring,
  F44's class. IMP-7.
- **Default mode overwrites or duplicates recorded output** (f110, f111,
  f152) and **write before verify** (backfill, 2): recurring. IMP-6.
- **Compound rule with no test per term** (3): recurring. IMP-5.
- **Text guard tripped by prose** (CI red, 8 commits): single; root cause
  a substring match over the whole file. IMP-2.
- **Silent type coercion in JSON writers** (1): single; root cause
  `default=str`; fixed by `strict_json.py` in a78901b.

## Improvements proposed

Each starts with prevention, and each extends a mechanism that already
exists unless it says "new".

| # | Title | Source | Type | Extends | Effort | Recommendation |
|---|---|---|---|---|---|---|
| IMP-1 | One content pin for every shrink-only list | Cat 2, 12; the review class above | Prevention | f98ea2f's subset pin and fe07674's hash pin, made one helper | 45m | now |
| IMP-2 | Text guards read code, not prose | Cat 1, 9; CI red 39f9943-f98ea2f | Prevention | `test_phase2_device_default.py` and the SUBMIT scan in `test_device_store_required.py` | 20m | now |
| IMP-3 | CI checked after every push from Manual Validation on | Cat 6, 9 | Control | `check_ci_status.py` and CLAUDE.md's two checkpoints | 45m | now |
| IMP-4 | Feature and fix commits name their issue | Cat 3, 9; D4 untimed | Prevention | `.githooks` (a new `commit-msg` beside `pre-commit`) | 30m | now |
| IMP-5 | One test per term of a compound rule | Cat 2, 4 | Prevention | Sprint 25 IMP-2 "Show each threshold can fire" | 10m | now |
| IMP-6 | Results written only through one refusing writer | Review class (5 findings) | Prevention | `provenance.py` | 90m | backlog |
| IMP-7 | Phase 2 document figures resolve | Cat 8; 7 findings | Detection | `test_document_figures_resolve.py` (F44) | 3h | backlog |

## Improvement Decisions

Team lead, 2026-10-24: "do now imp-1, 2, 4, 5, 6 and backlog imp-7 | we
have covered CI checks sufficiently, so no to IMP-3".

The now-items are timed as task R under issue #61. D4 was given issue #60
after the work, closed at once, and its time is recorded as not measured.

| # | Decision | Where |
|---|---|---|
| IMP-1 | **now** | See the commit for IMP-1 under #61 |
| IMP-2 | **now** | See the commit for IMP-2 under #61 |
| IMP-3 | **skip** | The team lead's reason: CI checks are covered sufficiently |
| IMP-4 | **now** | See the commit for IMP-4 under #61 |
| IMP-5 | **now** | See the commit for IMP-5 under #61 |
| IMP-6 | **now** | Not the recommended backlog; built this sprint under #61 |
| IMP-7 | **backlog** | F164 in `ALL_SPRINTS_MASTER_PLAN.md`, priority 25 |
