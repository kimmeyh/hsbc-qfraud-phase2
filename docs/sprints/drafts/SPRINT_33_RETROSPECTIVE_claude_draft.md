# Sprint 33 Retrospective

**Sprint**: 33, the Phase 2 Preregistration Ready to File
**Date**: 2026-11-18
**Scope**: F13 (A), F102 (B and D), F178 (C), the fresh-eyes review
fixes (E); added at Manual Validation: the outside adversarial review
(F), the exhaustive claim audit (G), the team lead's answers to D10-D12
and the FINAL status (H). Issues #123-#130, all closed. Draft PR #122.
**Effort**: `.claude/sprint_status.json` `task_actuals`, against the
plan's estimates. See category 3.
**Metered seconds**: 0.
**Goal** (team lead): "have the Phase 2 registration document ready to
submit." Met: `experiments/phase2/PREREGISTRATION_FINAL.md`, a
byte-identical copy of `PREREGISTRATION_DRAFT.md`. The official filing,
its lock and Experiment 3's release-rule check move to Sprint 34 (team
lead, 2026-11-18).

## Scoring, both roles

The team lead scored every category **Very Good**. Claude scored four
lower. The improvements are built from the lower scores.

| Category | Team lead | Claude |
|---|---|---|
| Effective while as efficient as reasonably possible | Very Good | **Good** |
| Testing approach | Very Good | **Good** |
| Effort accuracy | Very Good | **Good** |
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

Team lead: minor function updates "none"; backlog additions "none";
questions before ending the sprint "none".

## Sprint 33 Retrospective Feedback

The team lead gave combined Product Owner, Scrum Master and Lead Developer
feedback on 2026-11-18, with "Manual Validation complete", recorded
verbatim under each of the three roles. (The paste was headed "Sprint
34"; the team lead confirmed it is Sprint 33.) Claude's lines were
written while the Phase 6 reviews ran
(`docs/sprints/drafts/SPRINT_33_RETROSPECTIVE_claude_draft.md`).

### 1. Effective while as Efficient as Reasonably Possible
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. The goal was met with zero
  metered seconds. But the draft I handed over as "ready to file" on
  2026-11-16 had 8 Blocker findings in the first outside review and 3
  more in the claim audit. Most were statements true of a working draft
  and false of a filing (R1-R3), or figures and verdicts I had carried
  forward without rechecking the source (Experiment 2's "no IEEE-CIS
  score", F108's "failed"). The drift guard checked consistency, which is
  what it was built for; nothing checked truth until the reviews did.

### 2. Testing Approach
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. Every guard term has its own
  red proof, and the guards caught real defects: an unresolved figure
  after the audit's notes, and an unlinked first use in two learning
  documents in Task H. One weakness showed: the figure guard resolves a
  figure against any value in the result files the document names, so
  -0.0024 (from F64's document) "resolved" by coincidence once the
  audit's notes named `f144_proxy_twin.json` and `f154_confusion.json`.
  A figure can pass while its stated source is wrong.

### 3. Effort Accuracy
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. Recorded active minutes
  against estimates: A 6/75, B 12/120, D 14/60, C 4/45, E 1/30, F 60/110,
  G 23/90, H 12/30. Every row understates the work. A-E's timers started
  after the edits (as in Sprint 32). G's 23 minutes cover my own edits;
  the seven audit agents ran for several hours unattended (wall time not
  measured), which the timer does not record at all.

### 4. Planning Quality
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. D3 reduced a 360-minute
  proposal to one goal, and F199's coverage check folded into F102. The
  three tasks added at Manual Validation (F, G, H) were the team lead's
  requests and each had its own issue and timer.

### 5. Model Assignments
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. A different model (Fable)
  for the first review and seven Opus agents, one per block, for the
  audit found different defect classes: the first found claims false of
  a filing, the second found figures and verdicts false against their
  sources. The read-only agents cannot write files, so I saved their
  reports; that cost a few minutes each.

### 6. Communication
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. Every decision (D1-D12)
  was written to the decisions file before it was asked and answered by
  digit. One slip: a closing footer was typed, not generated; the Stop
  hook caught it and the line was regenerated.

### 7. Requirements Clarity
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. "Ready to submit" without
  the brief or a venue was resolved by written assumptions (A1-A12) and
  "not set" fields. The request to rename the file was met with a
  byte-identical copy, because about 45 evidence files and 40 modules
  cite the draft's path; the team lead then asked that both be locked.

### 8. Documentation
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. The draft's own edit rule
  held through two review rounds: entry text written before a run was
  never rewritten; each affected entry got one dated note.

### 9. Process Issues
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. A broad `grep -rn` over the
  working tree, run to find tests that check the draft's status line,
  matched one line in the gitignored `docs/qci_package/`, a folder this
  session must not open. Nothing from it was used, and the match was
  reported to the team lead. `git grep` searches tracked files only and
  would not have reached it.

### 10. Risk Management
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. The repository became
  public mid-sprint (D7, D8); the private correspondence was confirmed
  never committed, and the draft's QCi attributions were reworded to our
  own reading. The rename was not done, so no evidence path broke.

### 11. Next Sprint Readiness
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. Sprint 34's first work is
  named in the draft's section 7: fill the Filing section, add the tag
  and the hash test of both files (D11), add the 0.1% budget to the
  outcome record (D10), then compute Experiment 3's release rule (D12).

### 12. Architecture Maintenance
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. The drift guard reused
  the per-document figure pools of `test_phase2_figures_resolve.py`
  rather than a second resolver.

### 13. Minor Function Updates for the Next Sprint Plan
- **Product Owner**: none
- **Scrum Master**: none
- **Lead Developer**: none
- **Claude Code Development Team**: The filing steps in category 11.

### 14. Function Updates for the Future Backlog
- **Product Owner**: none
- **Scrum Master**: none
- **Lead Developer**: none
- **Claude Code Development Team**: See the improvements below.

### 15. Assigned Coding Agents Quality
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. Every Blocker and Major
  the audit agents reported held when I spot-checked it against the
  source before any edit. Some of my own note details, written from
  memory, did not, and were corrected against the source before commit.

### 16. Questions to be discussed before ending the sprint
- **Product Owner**: none
- **Scrum Master**: none
- **Lead Developer**: none
- **Claude Code Development Team**: none.
