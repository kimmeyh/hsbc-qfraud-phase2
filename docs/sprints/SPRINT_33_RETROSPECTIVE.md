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

## Review findings fixed (Task I, #131)

- Copilot (4 comments): the Filing section's "blank" line (removed by
  the team lead's filing-date change); the team lead's verbatim
  "gaurding" marked "[sic]" in three files.
- pr-review-toolkit, Important 1: nothing checked that
  `PREREGISTRATION_FINAL.md` matches the draft. The drift guard's
  eleventh term now does, with a red proof.
- pr-review-toolkit, Important 2: the lock design left open when the
  hash is taken and where "## Amendments" goes. Section 7 now says: after
  the venue is recorded; after the revision log.
- pr-review-toolkit, Suggestions: a Result cell must be a file, not a
  directory or a glob (red proof added); the validation document's
  registered-figure count (five, not six); the PoC plan's A2 adds the
  0.1% budget.

## Review finding classes (input to the improvements)

- **A check that matches more than it should** (recurring: Sprint 32's
  scan guard missed shapes; Sprint 33: the figure pool matched -0.0024 by
  coincidence, and `git ls-files` accepted a directory). The second is
  fixed; the first is i1.
- **A claim with no check behind it** (single this sprint: "byte-identical"
  with no test). Root cause: the copy was made at the team lead's request
  late in the day, and the claim was written without asking which test
  holds it. Fixed by the eleventh term.

## Review findings not fixed (for the team lead's disposition)

- Each entry's "State at filing (2026-11-16)" date is not tied to the
  Filing section's date, and the assumption-citation reader does not
  read "assumptions A2 and A4" or "A2, A4" forms (the draft uses
  neither today). Both are in i4.

## Improvements proposed

### i1. A figure resolves only in the result file its own sentence cites

- **What it is:** `experiments/src/test_phase2_figures_resolve.py`
  resolves a figure against the result files cited in the same
  paragraph or entry, not against every file the document names. The
  drift guard's term 10 inherits it.
- **What it prevents and/or catches:** catches, at the testing stage, a
  figure whose stated source is wrong but whose value appears in some
  other named file. Prevention (writing the right source) cannot be
  checked without this.
- **Long-term value:** every new result file a document names widens
  the pool; the chance of a coincidental match grows with each sprint.
- **Evidence:** one coincidental match seen (-0.0024, Sprint 33 Task G);
  how many draft figures would resolve by chance is not measured (the
  review's measurement was stopped after 3 minutes).
- **Pros and cons:** pro: the guard checks the source, not only the
  value. Con: paragraph scoping may flag figures that cite their source
  one paragraph away; each needs a citation or a registry entry.
- **Prevention or control:** control. **Extends:**
  `test_phase2_figures_resolve.py` (F164's per-document pools).
  **Effort:** about 60 minutes; 2 files plus the documents it flags.
- **Options for implementing:**
  - a. Backlog F200, priority P2: first measure the share of 2-4 place
    decimals the draft's pool resolves (15 minutes), then scope by
    paragraph if it is above 5%. Pro: sized by measurement. Con: the
    gap stays until scheduled. **(Recommendation)**
  - b. Now: scope by paragraph in this sprint (about 60 minutes). Pro:
    closed before the filing lock. Con: the close-out grows by an hour.
  - e. Track only; act if a second coincidental match is found. Pro: no
    cost. Con: a wrong source can pass meanwhile.
  - f. Skip.

### i2. Repository text searches never read ignored folders

- **What it is:** a CLAUDE.md "Things Claude Should NOT Do" entry: in
  this repository, search text with the Grep tool or `git grep` (both
  skip gitignored paths), never `grep -r` over the working tree.
- **What it prevents and/or catches:** prevents, at the development
  stage, reading a private gitignored folder (`docs/qci_package/`) by a
  broad search.
- **Long-term value:** the repository is public and holds private
  ignored folders; every broad search is a chance to read or quote them.
- **Evidence:** one occurrence (Sprint 33, a `grep -rn` matched one line
  in `docs/qci_package/`; nothing was used). Time lost: none.
- **Pros and cons:** pro: one sentence, no code. Con: a rule in a
  document is not enforced; a hook would be.
- **Prevention or control:** prevention. **Extends:** the CLAUDE.md
  entry "Don't move an ignored file without writing its rule at the
  DESTINATION first" (the same folder's protection). **Effort:** 5
  minutes; 1 file.
- **Options for implementing:**
  - a. Now: the CLAUDE.md entry. Pro: immediate, costs nothing. Con:
    not enforced. **(Recommendation)**
  - b. Backlog F201, priority P3: a PreToolUse hook that blocks
    `grep -r` or `rg --no-ignore` over the repository root. Pro:
    enforced. Con: a new hook and its tests, about 45 minutes.
  - e. Track only. Pro: no cost. Con: relies on memory.
  - f. Skip.

### i3. The pre-push gate refuses to start on a dirty tree

- **What it is:** `scripts/select_proofs.py --tests` exits at once,
  naming the dirty paths, when `git status --porcelain` is not empty,
  instead of running for minutes and then not being accepted by the
  pre-push hook.
- **What it prevents and/or catches:** prevents, at the development
  stage, a full gate run that cannot count.
- **Long-term value:** every push runs the gate; a wasted run costs its
  full length.
- **Evidence:** one occurrence (Sprint 33, b8e2c0e: the gate passed on a
  tree with an uncommitted status file and two untracked retrospective
  files, and the push was refused; about 8 minutes lost).
- **Pros and cons:** pro: fails in a second, not minutes. Con: one more
  refusal path to test.
- **Prevention or control:** prevention. **Extends:** the pre-push hook's
  "no passing --tests run tested this tree" check, moved earlier.
  **Effort:** about 20 minutes; 2 files (the script and its test, with
  a red proof).
- **Options for implementing:**
  - a. Now, on this branch. Pro: the next push benefits. Con: adds code
    to the close-out, covered only by the short review.
  - b. Backlog F202, priority P2. Pro: done
    with its own plan and review. Con: may recur meanwhile.
    **(Recommendation)**
  - e. Track only.
  - f. Skip.

### i4. The two drift-guard gaps the review left open

- **What it is:** before the Sprint 34 lock step, the drift guard (a)
  checks that each "State at filing" date is on or before the Filing
  date and that all six match, and (b) reads "assumptions A2 and A4" and
  "A2, A4" citations.
- **What it prevents and/or catches:** catches, at the testing stage, a
  stale state date or an unread citation in the locked text.
- **Long-term value:** small after the lock, because the filed text
  cannot change; most of its value is before the lock.
- **Evidence:** neither defect is present today (review, 2026-11-18).
- **Pros and cons:** pro: closes two holes before the text is frozen.
  Con: about 30 minutes for defects not present.
- **Prevention or control:** control. **Extends:**
  `experiments/src/test_phase2_prereg_draft.py` terms 5 and 7.
  **Effort:** about 30 minutes; 1 file.
- **Options for implementing:**
  - a. In Sprint 34, before the lock step. Pro: the guard is complete
    when the text freezes. Con: 30 minutes for defects not present.
  - e. Track only: the lock makes later drift impossible. Pro: no cost.
    Con: the holes stay until the lock. **(Recommendation)**
  - f. Skip.

### i5. Task timers record agent wall time

- **What it is:** `scripts/update_sprint_status.py` gains
  `--agent-minutes TASK N`, added to the task's actuals as a separate
  field, so work done by background agents is counted.
- **What it prevents and/or catches:** prevents, at the sprint-process
  stage, effort records that omit agent work.
- **Long-term value:** effort calibration needs every minute of work.
- **Evidence:** Sprint 33 Task G recorded 23 minutes against several
  hours of seven agents (agent wall time not measured); Sprints 32 and
  33 understated every row.
- **Pros and cons:** pro: honest effort data. Con: one more field to
  fill.
- **Prevention or control:** prevention. **Extends:** the status tool's
  timers. **Effort:** about 30 minutes; 2 files.
- **Options for implementing:**
  - a. Backlog F203, priority P3. Pro: done with its own plan. Con:
    effort data stays short meanwhile. **(Recommendation)**
  - e. Track only. Pro: no cost. Con: calibration stays blind to agents.
  - f. Skip.

## Improvement Decisions

| # (i1-in) | Title | Alternative taken (a-z) | Effort | Decision (now/backlog/skip) |
|---|---|---|---|---|
| i1 | A figure resolves only in the result file its own sentence cites | e | none | track only: act if a second coincidental match is found |
| i2 | Repository text searches never read ignored folders | a | 5 minutes | now: CLAUDE.md entry |
| i3 | The pre-push gate refuses to start on a dirty tree | a | about 20 minutes | now: Task J, #132 |
| i4 | The two drift-guard gaps the review left open | f | none | skip |
| i5 | Task timers record agent wall time | f | none | skip |

Answered by the team lead, 2026-11-18: "i1. e i2. a i3. a i4. f i5. f".

Task J keeps `--base HEAD` and runs narrowed after `--` working on a
dirty tree, because `docs/SPRINT_CHECKLIST.md` uses `--tests --base HEAD`
to test a task's uncommitted changes. Only a run that could be recorded
for the pre-push hook refuses.
