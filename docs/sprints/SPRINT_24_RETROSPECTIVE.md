# Sprint 24 Retrospective

**Sprint**: 24, Close the Boundary, Fix the Tooling, Sweep the Lever
**Date**: 2026-10-10
**Scope**: F131 (A), F136 (B), F132 (C), F134 (D), F133 (E), F135 (F),
F128 (G), F137 (H). Issues #3-10. Draft PR #2.
**Effort**: 84 measured minutes against 290 estimated
(`.claude/sprint_status.json`, `task_actuals`). The two reviews and their
fixes were not timed.
**Metered Dirac-3 seconds**: **0**. The balance read 1,022 s through the
sprint and **8,522 s on 2026-10-10**
(`experiments/results/call_logs/allocation_read_20261010.log`).

## Scoring, both roles

The team lead scored every category **Very Good**. Claude scored five
lower. Where the two disagree both are recorded, and the improvements are
built from the lower score.

| Category | Team lead | Claude |
|---|---|---|
| Effective while as efficient as reasonably possible | Very Good | **Good** |
| Testing approach | Very Good | Very Good |
| Effort accuracy | Very Good | **Fair** |
| Planning quality | Very Good | Very Good |
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
Manual Validation he also asked for the Dirac-3 balance check and for F138
(Dirac-3S research, Sprint 25, before any further Dirac-3 seconds).

## Sprint 24 Retrospective Feedback

The team lead gave combined Product Owner, Scrum Master and Lead Developer
feedback, recorded verbatim under each of the three roles.

### 1. Effective while as Efficient as Reasonably Possible
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. All eight tasks met their
  acceptance criteria with zero metered seconds. Rework came after the
  tasks: the code review found 6 real defects (one changed how a result was
  labeled: F128's top value was called "best" though it was chosen on the
  splits it is reported on), and the fresh-eyes review found 8
  interpretation overclaims in the F128 write-up, including "parity" on
  energy_steel that was a 3-loss, 2-win split. Both reviews worked as
  designed; the overclaims were mine.

### 2. Testing Approach
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. Every new guard was proven
  red with `assert_can_fail` or an injected file, with the mutation's bytes
  checked. Two proofs arrived only from the review: the Phase 1 boundary
  test had no injected offender, and the WSL scripts' wrong-directory guard
  could no longer fire. Both fixed in-sprint. Two full suite runs left the
  tree clean (F131).

### 3. Effort Accuracy
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Fair. The first measured sprint: A 3/30,
  B 1/20, C 12/90, D 2/30, E 2/40, F 1/10, G 29/50 (plus the run), H 34/20.
  84 minutes against 290, a ratio of 0.29. Tooling cards with a known fix (A-F) ran
  at 0.05-0.13, against 0.44-2.25 in the judged rows of Sprints 20-23. Two
  distortions: the review and fix time is real work that no task clock
  recorded, and H ran over because it waited for G's run (see 4). Task B's
  start was typed by hand, before the tool existed.

### 4. Planning Quality
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. Plan verification corrected
  two cards before work began: F133 had a second file shape, and F128 was
  smaller than carded. The plan's premise falsifier for F128 was written in
  advance and fired, so the null result is a finding, not a surprise. One
  miss: H reinstalls the venv that G's background run was using, and the
  plan listed H as depending on A only.

### 5. Model Assignments
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. Main loop for all tasks; the
  sweep ran in the background; two background reviewers with no sprint
  context found what the main loop missed.

### 6. Communication
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. I labeled the default-branch
  decision D3 when the rename already held D3; it was relabeled D4 in the
  CHANGELOG and master plan. No answer was misapplied, but a reused label is
  the kind of thing that can be.

### 7. Requirements Clarity
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. The rename sweep came with an
  exact boundary (the old name with the `p2` suffix, never the Phase 1 name
  without it), and the sweep touched one memory file only.

### 8. Documentation
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. The sprint's own records were
  current at every commit. But on 2026-10-10 the Dirac-3 balance read 8,522
  s, and an older figure is stated as current in six live places: the F129
  and F25 cards in the master plan, two `CHECKLIST-Phase2.md` items,
  `SPECTRA_IMPROVEMENT_RESEARCH.md` and `QPU_RECONCILIATION.md`, whose
  "currency" paragraph still says 1,961 s. The repository has no single
  owner for the balance (IMP-1).

### 9. Process Issues
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. `block_cross_repo_write.py`
  blocks any `sed -i` command whose text contains the Phase 1 name, even
  when the edit is in this repository; the Edit tool works (IMP-4). The
  heredoc-escape and shell-metacharacter hooks each blocked commands; their
  messages named the right route both times. The Edit tool once dropped a
  space in a WSL script, caught on re-read.

### 10. Risk Management
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. The F132 risk (a wrong
  `FORBIDDEN` entry blocking this repository) was covered by a
  two-direction test. A new risk: a stale balance in a card could size a
  metered run. F138 now gates every Dirac-3 card, and IMP-1 removes the
  restated figures.

### 11. Next Sprint Readiness
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. F138 is carded for Sprint 25
  and gates F129, F95, F25 and F30. F129 must be re-scored at refinement
  (the F128 falsifier fired). `SPRINT_24_SUMMARY.md` is written at Sprint
  25 planning.

### 12. Architecture Maintenance
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. No preregistration drift;
  F128 is SIM-tagged and its result file records the generator's SHA-256.
  A device change to Dirac-3S may need an amendment before any comparison
  with B2, B4 or B5; F138 asks that question.

### 13. Minor Function Updates for the Next Sprint Plan
- **Product Owner**: none
- **Scrum Master**: none
- **Lead Developer**: none
- **Claude Code Development Team**: none beyond the improvements below

### 14. Function Updates for the Future Backlog
- **Product Owner**: none
- **Scrum Master**: none
- **Lead Developer**: none
- **Claude Code Development Team**: F138, carded at the team lead's request
  during Manual Validation, priority 5, target Sprint 25

### 15. Assigned Coding Agents Quality
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. The code reviewer's 6
  findings and the fresh-eyes reviewer's 8 were all verified as real; none
  was rejected. The fresh-eyes reviewer recomputed all 12 summary cells from
  the rows before commenting on interpretation.

### 16. Questions to be discussed before ending the sprint
- **Product Owner**: none
- **Scrum Master**: none
- **Lead Developer**: none
- **Claude Code Development Team**: two, asked at the improvement decision:
  the source of the added 7,500 s, and where the balance is recorded

## Improvements proposed (awaiting the team lead's decision)

| # | Title | Source | Type | Effort | Recommendation |
|---|---|---|---|---|---|
| IMP-1 | One owner for the Dirac-3 balance | Cat 8, 10 | Prevention: `check_allocation.py --record` appends dated reads to `experiments/results/allocation_reads.json`; live docs cite it; a guard fails on a balance figure stated in a live doc | 45m | Sprint 25 |
| IMP-2 | Time the reviews, and plan from measured ratios | Cat 3 | Process: reviews and their fixes get their own `--start-task`; Sprint 25 planning reads Sprint 24's measured rows | 10m | now |
| IMP-3 | A task that reinstalls the venv depends on every run using it | Cat 4 | Process: one line in `SPRINT_PLANNING.md` | 5m | now |
| IMP-4 | The `sed -i` false positive in the cross-repo hook | Cat 9 | Pointer: `TROUBLESHOOTING.md` entry (symptom, cause, use the Edit tool); hook unchanged | 5m | now |

## Improvement Decisions

Team lead, 2026-10-10: "IMP-2 not valuable and therefore not needed. imp-3
is this stating that any venv reinstalls need to run before any tasks that
depend on venv? noting this has only happened once and not expected to
happen again. imp-1 and imp4 implement now | D2 2".

| # | Decision | Where |
|---|---|---|
| IMP-1 | **now** | `check_allocation.py --record` writes `experiments/results/allocation_reads.json`; the six live statements cite it (D2 option 2); `test_allocation_single_source.py` fails on a restated balance and on a live consumer that stops citing the owner, both proven red with `assert_can_fail` |
| IMP-2 | **skip** | not valuable (team lead) |
| IMP-3 | **pending** | the team lead asked what it states; answered at the close-out decision |
| IMP-4 | **now** | `docs/TROUBLESHOOTING.md`, Hooks; widened to the `cp` case met on 2026-10-10 |

**The source of the added seconds (D3).** QCi's notice of 2026-10-09: "We've
loaded your account up with 8,522 seconds", and "Dirac-3S is available"
(`docs/QPU_RECONCILIATION.md`, grants). The copy goes to
`docs/qci_package/`, gitignored.

**Added at the retrospective**: F139 (team lead), every Dirac-3 run reviewed
for a Dirac-3S re-run and the plan updated for what the new hardware allows,
immediately after F138 in Sprint 25.
