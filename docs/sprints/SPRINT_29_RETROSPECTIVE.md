# Sprint 29 Retrospective

**Sprint**: 29, Make the Tools Repeatable, Then Find the Best Each Model Can Do
**Date**: 2026-10-28
**Scope**: F165 (A), F159 (B), F164 (C), F156 (D), F160 (E), F166 (F),
F158 (G), F167 (H), pypdf (I). Issues #64-72. Draft PR #63. Review fixes
timed as task J (no issue; `fix` commits name "PR 63 review").
**Effort**: `.claude/sprint_status.json`, `task_actuals`, against the plan's
1,050 minutes. See category 3.
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

## Sprint 29 Retrospective Feedback

The team lead gave combined Product Owner, Scrum Master and Lead Developer
feedback, recorded verbatim under each of the three roles.

### 1. Effective while as Efficient as Reasonably Possible
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. All nine tasks met their
  acceptance with zero metered seconds, and four experiments gave a
  decisive reading (F156 fails, F158's cascade is below, F160 passes,
  F166 ranks two pairs). The largest loss was F159's resume, which hung
  for 9 hours (12:10am to 8:58am) with no in-process time limit; fixed in
  94f079e. Rework: the four PR #63 reviews returned silent-failure 7,
  test-coverage 10 ranked plus lower items, documents 11 and code 5
  findings, and Copilot an overview with no inline comment; fixed in 8bea51f, bc36281 and
  50cbb1f. One defect, a rerun refused only after its work, was in five
  modules because each copied the same resume line.

### 2. Testing Approach
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. Every new guard was proven red
  with `assert_can_fail`, and the test reviewer found no vacuous proof.
  The Phase 5 gate from Sprint 28 IMP-5 (one test per term of a compound
  rule) caught two rules at Phase 5 (92d89b6, a14c644), and the review
  then found eight more: F166's bootstrap rejection and both Bonferroni
  corrections, F158's Wilcoxon term, F160's order gate and resolution
  pass-through, F158's off-split check and F159's budget derivation. The
  gate is a manual walk, and it was walked at Phase 5, not as each rule
  was written (IMP-1). One test asserted a defect: `all_equal` true for a
  fraction that compared nothing.

### 3. Effort Accuracy
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Poor, as a measurement. Actual over
  estimate, minutes: A 2042/60, B 622/60, C none/270, D 2647/90, E 53/75,
  F 158/240, G 6/150, H 2036/60, I 17/45; J (review fixes, not planned)
  69. A, H, D and B ran across the overnight break or the F159 hang; C's
  timer was never started; E and G started only when their runs began.
  Only F, I and J are as measured. Same class as Sprint 28 (K and H read 1
  minute; D4 had no timer) (IMP-4).

### 4. Planning Quality
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. Decisions 1-3 were settled
  before execution and each entry was committed before its first score
  (the docs reviewer checked all four commits). Decision 3's rule set
  F166's seed count from a measured time.

### 5. Model Assignments
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. The main loop kept every
  run, decision and fix; the four review agents worked on the draft PR
  with the evidence files excluded and read results only to check
  figures.

### 6. Communication
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. Two figures in the on-screen
  Manual Validation handover were wrong: "106 of 950 ULB test frauds"
  counts (seed, test fraud) pairs, not frauds, and F160's range
  "0.096 to 0.099" is 0.096-0.098. Both came from the validation
  document, which no check read; corrected in 50cbb1f. One footer was
  typed by hand and caught by the Stop hook (9:20am, not 9:31am).

### 7. Requirements Clarity
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. The plan's "both venvs"
  named a second venv that does not exist here; reported, not assumed.

### 8. Documentation
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. F164 caught two older
  documents. The review found seven claims its sources do not support:
  F159's speed-up attribution, the proxy page's "configuration changes
  between seeds" (it never did), F170's "V1-V17", the PoC draft's stale
  F160 state, V7's "twelve stored families" and "950 frauds", and F160's
  0.099. Four signed figures had resolved to unrelated values by chance,
  and F166's eight documents shared one pool covering 74.7% of the
  3-place grid. The F166 documents come from a generator in the session
  scratchpad, not the repository, so their boilerplate cannot be
  regenerated or reviewed (IMP-2).

### 9. Process Issues
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. The F159 hang ran 9 hours
  unseen while the session was idle; F168 (Sprint 30, part 6) covers a
  recurring check that would see it. The watchdog added in 94f079e was
  applied at F159's call site only; F166 called the unguarded build
  directly (IMP-3). Hooks worked as designed: a typed footer and `${...}`
  in a Python command were each blocked.

### 10. Risk Management
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. Zero metered seconds. The
  `MemoryError` at 32 workers is recorded with its cause unverified.
  Copilot flagged the preregistration amendments and the F159 incident
  for human sign-off, with no open issue.

### 11. Next Sprint Readiness
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. F168 is assigned to Sprint
  30; F169, F170 and F171 are carded from Manual Validation.

### 12. Architecture Maintenance
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. `provenance.start` now decides
  a run's start, resume or refusal in one place, and a guard keeps
  modules from deciding it themselves (8bea51f). Before that, five
  modules each carried a copy of a resume line that refused a rerun only
  after its work. Shared `experiments/src` code kept Phase 1 behavior as
  the default.

### 13. Minor Function Updates for the Next Sprint Plan
- **Product Owner**: none
- **Scrum Master**: none
- **Lead Developer**: none
- **Claude Code Development Team**: none beyond the improvements below.

### 14. Function Updates for the Future Backlog
- **Product Owner**: none
- **Scrum Master**: none
- **Lead Developer**: none
- **Claude Code Development Team**: F169, F170 and F171, carded at
  Manual Validation; F172 (IMP-5), carded at the retrospective.

### 15. Assigned Coding Agents Quality
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. No coding agents were
  assigned this sprint. The four review agents' findings each named a
  file, a line and a failing scenario; the ones checked against the code
  held, and the test reviewer probed its gaps with crafted inputs.

### 16. Questions to be discussed before ending the sprint
- **Product Owner**: none
- **Scrum Master**: none
- **Lead Developer**: none
- **Claude Code Development Team**: none

## Review finding classes (input to the improvements)

- **Compound rule with no test per term** (8 at review, 2 at Phase 5):
  recurring (Sprint 28, 3). IMP-1.
- **Document claim its source does not support** (7, plus 4 signed
  figures matched by chance): recurring (Sprint 28, 7). F164 extended in
  50cbb1f; IMP-2 for the generated documents.
- **Refusal after the work** (one defect in 5 modules, 3 reviewers):
  single class; root cause a copied resume line. Prevented in 8bea51f
  (`provenance.start` and a guard that no module decides it).
- **A guard applied at one call site** (F166 called the unguarded
  build): single; root cause the watchdog wraps the caller, not the
  function. IMP-3.
- **Vacuous aggregate** (`all({})` read as equal): single; root cause an
  empty comparison set; fixed in bc36281.
- **Timers not reflecting work** (C, E, G, and four inflated): recurring
  (Sprint 28 IMP-4). IMP-4.

## Review findings not fixed

The lower-rated test-coverage items, each a test that would make a branch
fail visibly; none changes a recorded result:

- F166: the proxy's validation and training labels are not checked
  against the classical lanes' (only the test labels are); the "below"
  reading, the `svm_form` majority rule and `t42_min <= 0` are untested.
- F156: `summarize`'s pass term and `term1_alone_4_of_5`, the
  single-class refusal. The key name `term1_alone_4_of_5` stays: it is in
  the recorded result.
- F160: SCIP's best-found minimum. F159: the MemoryError and broken-pool
  path end to end; `test_the_budget_can_fail` goes red through a KeyError
  rather than its timing assertion.
- Each module's "never redo a seed" resume loop has no module-level test;
  `provenance.start` covers the decision, not the loop.

## Improvements proposed

Each starts with prevention, and each extends a mechanism that already
exists unless it says "new".

| # | Title | Source | Type | Extends | Effort | Recommendation |
|---|---|---|---|---|---|---|
| IMP-1 | A rule's per-term tests land in the commit that adds the rule | Cat 2; 10 terms found after their commit | Prevention | Sprint 28 IMP-5 (`SPRINT_PLANNING.md`, Phase 5 gate), moved to Phase 4 in `SPRINT_CHECKLIST.md` | 15m | now |
| IMP-2 | Generated result documents come from a tracked generator | Cat 8; F166's eight pages from a scratchpad script | Prevention | `test_phase2_figures_resolve.py` (F164): the generator moves to `scripts/`, and its boilerplate is computed from the result | 60m | now |
| IMP-3 | The parallel build cannot run without a budget | Cat 9; F166 called `build_parallel` directly | Prevention | `build_with_budget` (94f079e): `budget_s` becomes a required argument of the public build | 20m | now |
| IMP-4 | A feature or fix commit for a task needs its timer running | Cat 3; C, E, G | Prevention | `.githooks/commit-msg` and `check_commit_issue.py` (Sprint 28 IMP-4) | 30m | now |
| IMP-5 | The test-coverage items above | Review findings not fixed | Detection | the modules' own test files | 90m | backlog |

## Improvement Decisions

Team lead, 2026-10-30: option 1, as recommended (Decision D2, in full in
`SPRINT_29_DECISIONS.md`). Applied on this branch, timed as task K:

- **IMP-1, applied.** `SPRINT_CHECKLIST.md` Phase 4 requires a compound
  rule's per-term tests, each proven red, in the commit that adds the
  rule; Phase 5 now checks that this was done. `SPRINT_PLANNING.md`
  records the reason.
- **IMP-2, applied.** `scripts/f166_docs.py` renders the eight F166 pages
  from the result. Each statement in its fixed text is computed from the
  result, or refused (`ClaimError`) when the result does not support it.
  `test_f166_docs.py` fails when a committed page differs from the
  render. One sentence changed on rendering: the comparison page now
  lists the two smallest train-test gaps in ascending order.
- **IMP-3, applied.** `f159.build_parallel` requires `budget_s`, a
  positive number of seconds, and runs under the watchdog. The build
  without a limit is private (`_build_unbudgeted`), and a test fails any
  other module that calls it. F166 calls `build_parallel`.
- **IMP-4, applied.** `check_commit_issue.py` refuses a feat or fix commit
  on a sprint branch when no task timer is running (started, not
  finished, not paused).
- **IMP-5, to the backlog** as F172, priority 40.

Each new rule is proven red with `assert_can_fail`.

## Review of the improvement commits

One short review of eaed56f, baa1555, 6cd51ad, 3846b20 and c6201f4 (no
second round). Five findings:

- **IMP-4 accepts any running timer, not the commit's own task's.** It
  would have admitted Task C's commit 5348add, because D's and H's timers
  were running. The wording now says so (the hook's docstring and
  message); the stronger check needs an issue-to-task map and is carded as
  F173, priority 40.
- **The F166 generator still fixed some text without checking it**: the
  linear SVM, Wilcoxon as primary, the Bonferroni divisor, the evidence
  tag and the metered seconds. Fixed: `check_fixed_text` refuses a result
  that differs on any of them.
- **No test reached the BLUF order refusal**: the order case was refused
  first by the pair-order check. Fixed: both refusals are tested by their
  message, and the BLUF check has its own red proof.
- **A red proof failed through a TypeError**, not through the missing
  refusal. Fixed: the mutation now makes the claim be written with no
  refusal.
- **`time_unit`'s `budget_s=None` default** reads as allowed for a
  parallel build. Fixed: its docstring says a parallel build with no
  budget raises.
