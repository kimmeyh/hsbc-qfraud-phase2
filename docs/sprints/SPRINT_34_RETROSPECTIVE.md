# Sprint 34 Retrospective

**Sprint**: 34, the Phase 2 filing lock and the first post-filing checks
**Date**: 2026-11-24
**Scope**: F201 (A), F202 (B), F102 (C and D), F200 (E), F198 (F), F197
(G), F157 (H), F178 (I); the Phase 5 fixes, timed as P5. Issues
#135-#143, all closed. Draft PR #134.
**Effort**: `.claude/sprint_status.json` `task_actuals`, against the
plan's estimates. See category 3.
**Metered seconds**: 0.

## Scoring, both roles

The team lead scored every category **Very Good**. Claude scored seven
lower. The improvements are built from the lower scores and the review
findings.

| Category | Team lead | Claude |
|---|---|---|
| Effective while as efficient as reasonably possible | Very Good | **Good** |
| Testing approach | Very Good | **Good** |
| Effort accuracy | Very Good | **Needs improvement** |
| Planning quality | Very Good | **Good** |
| Model assignments | Very Good | Very Good |
| Communication | Very Good | **Good** |
| Requirements clarity | Very Good | Very Good |
| Documentation | Very Good | **Good** |
| Process issues | Very Good | **Good** |
| Risk management | Very Good | Good |
| Next sprint readiness | Very Good | Very Good |
| Architecture maintenance | Very Good | Very Good |
| Assigned coding agents quality | Very Good | Very Good |

Team lead: minor function updates "none"; backlog additions "none";
questions before ending the sprint "none".

## Sprint 34 Retrospective Feedback

The team lead gave combined Product Owner, Scrum Master and Lead
Developer feedback on 2026-11-24, recorded verbatim under each of the
three roles. The paste was headed "Sprint 18 Review/Retrospective"; it
was given at Sprint 34's retrospective and is recorded as Sprint 34's.
Claude's lines are from
`docs/sprints/drafts/SPRINT_34_RETROSPECTIVE_claude_draft.md`.

### 1. Effective while as Efficient as Reasonably Possible
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. Every task shipped and the
  release rule was computed as filed. Rework was high: the pre-push
  gate ran six times on the Phase 5 and close-out commits (two
  figure-format failures, one complete-check failure, one start on a
  dirty tree, one pass lost to edits made while it ran, and the passes),
  each 9 to 19 minutes. Two failures had one cause: a figure rewritten
  in one document broke a guard on another, and I ran only the guard I
  was thinking of.

### 2. Testing Approach
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. The guards caught real
  defects before handover: the figure guards, `test_complete_checked.py`
  and CI's refusal-coverage step. But three refusals shipped in Phase 4
  with no in-process test, and only CI found them, because the local
  gate does not run the coverage step. The review found a test gap (the
  pick's side of the release comparison had no test of its own), and
  the tag hook's parity cases missed four delete and move shapes.

### 3. Effort Accuracy
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Needs improvement. Plan 465
  minutes, actual 363 (A 45/48, B 15/30, C 15/28, D 60/17, E 45/84,
  F 30/78, G 60/9, H 45/2, I 105/29, P5 45/38). G and H were timed for
  far less than the work took, because work ran with no timer or under
  another task's timer. E and F were real misses: E's run was planned
  at "about 1 minute, cap 10" and took about 11, mostly rebuilding the
  IEEE-CIS instances; F's cap of 20 was not coded and its run took 15.
  The sprint passed the 1-2 hour target by a wide margin.

### 4. Planning Quality
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. The tasks were clear and
  their acceptance criteria could be checked. The runtime figures for E
  and F were guesses: no timed first instance was in their basis.

### 5. Model Assignments
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. The independent review
  agent, given the code and not my conclusions, found four real issues
  and no false ones.

### 6. Communication
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. At handover the on-screen
  list (A1 to A6, with D7) did not match the validation file (A1 to A5,
  no D7). The answers were given against the screen and recorded that
  way, but the two records differed until then.

### 7. Requirements Clarity
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. Q4 (the change-list
  rule) was echoed back and confirmed before the rewrite.

### 8. Documentation
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. P2-A6 quoted two figures from
  an unrecorded scratch check, so P2-A8 had to withdraw them. The test
  inventory, marked "do not edit by hand", was edited by hand, and two
  of its counts are stale.

### 9. Process Issues
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. One commit needed three tries
  against the commit-msg hook (timer, issue reference, review task),
  and a mislabeled commit was amended. A passing gate run on 8b4533e
  (12 minutes) was not recorded because I wrote files while it ran; the
  push was refused and the gate ran again (19 minutes).

### 10. Risk Management
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. The filing tags have no
  server-side protection and the hook can be bypassed; the team lead
  chose the hook only (D7 option 3). The filed commit is on four
  branches and the filed files are hash-locked, so the text is not at
  risk.

### 11. Next Sprint Readiness
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. Sprint 35 has two
  approved items, Experiment 5b (D6) and F25 (D8), with F25's cost
  probes and first run approved in advance.

### 12. Architecture Maintenance
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. No locked file changed;
  every post-filing change is a dated amendment; every new result file
  carries provenance and outcome blocks.

### 13. Minor Function Updates for the Next Sprint Plan
- **Product Owner**: none
- **Scrum Master**: none
- **Lead Developer**: none
- **Claude Code Development Team**: [DEV] Regenerate
  `docs/testing/F180_TEST_INVENTORY.md` from a full local report --
  target: Sprint 35 plan, est: 10m. [DEV] Re-read the allocation
  balance before F25's first block -- target: Sprint 35 plan, est: 5m.

### 14. Function Updates for the Future Backlog
- **Product Owner**: none
- **Scrum Master**: none
- **Lead Developer**: none
- **Claude Code Development Team**: [DEV] Tokenize the tag hook's input
  before matching -- estimated: 1h, priority: 12, depends on: none (i9).

### 15. Assigned Coding Agents Quality
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. The review agent's four
  findings were all correct and needed no rework.

### 16. Questions to be discussed before ending the sprint
- **Product Owner**: none
- **Scrum Master**: none
- **Lead Developer**: none
- **Claude Code Development Team**: None.

## Review findings and their classes (input to the improvements)

- **Fixed**: the pick-side test, the four tag-hook shapes, P2-A6's
  unrecorded figures (P2-A8), F198's merged readings, the three
  untested refusals (CI), the complete-check (gate).
- **Not fixed**: the security review's further hook bypasses (D7
  option 3; i9).
- **Classes**: untested refusals or rules (recurring: 37 in Sprints
  28-30, 3 this sprint; i1); a figure without a recorded source
  (recurring: Sprint 33 i1, this sprint P2-A6; i4); guard coverage gaps
  in a hook (single this sprint: root cause, regular expressions on a
  command line; i9).

## Improvements proposed

### i1. The local gate runs the refusal-coverage check

- **What it is:** `scripts/select_proofs.py --tests` runs its selected
  tests under coverage, then `diff-cover` and
  `scripts/refusal_coverage.py`, the same step CI's push job runs, and
  fails on an untested changed refusal.
- **What it prevents and/or catches:** prevents a push with an untested
  refusal, at the development stage (the gate before push), instead of
  CI after the push.
- **Long-term value:** every sprint adds refusals; the coverage step is
  the only check that sees them, and today it runs only after a push.
- **Evidence:** 3 untested refusals this sprint, found by CI on 76c740b
  (one red CI round, about 40 minutes of fix and rerun); 37 reached
  review in Sprints 28-30 (`refusal_coverage.py` docstring).
- **Pros and cons:** pro: one fewer red CI round per occurrence. Con:
  coverage slows the gate, by an amount not measured.
- **Prevention or control:** prevention. **Extends:** the pre-push gate
  (`select_proofs.py --tests`) with CI's existing step. **Effort:**
  about 60 minutes; 2 files and a test.
- **Options for implementing:**
  - a. Backlog F210, priority 11, in Sprint 35: add the step, measure
    the gate's added time first on one run. Pro: closes the CI-only gap.
    Con: Sprint 35 grows by an hour. **(Recommendation)**
  - b. Now, in Sprint 34. Pro: closed at once. Con: this sprint is
    already far past its target.
  - c. A Phase 4 checklist line only ("run refusal_coverage before
    push"). Pro: 5 minutes. Con: a rule to remember, as before.
  - e. Skip, track it.

### i2. Nothing writes to the tree while the gate runs

- **What it is:** `select_proofs.py --tests` writes a lock file while it
  runs; a PreToolUse hook blocks Edit, Write and `git commit` while the
  lock exists, naming the running gate.
- **What it prevents and/or catches:** prevents a lost gate run, at the
  development stage.
- **Long-term value:** the gate takes 9-19 minutes; any write during it
  wastes the run.
- **Evidence:** one lost pass this sprint (12 minutes, then a 19-minute
  rerun); one start on a dirty tree (refused at once, since f45fb7e).
- **Pros and cons:** pro: the rule is enforced, not remembered. Con: a
  stale lock after a crash must be removed (the hook names it).
- **Prevention or control:** prevention. **Extends:** f45fb7e's
  dirty-tree refusal. **Effort:** about 40 minutes; 3 files.
- **Options for implementing:**
  - a. Backlog F211, priority 12, in Sprint 35. Pro: small and
    contained. Con: one more hook. **(Recommendation)**
  - b. Now, in Sprint 34. Pro: at once. Con: sprint size.
  - c. A troubleshooting entry only. Pro: 5 minutes. Con: not enforced.
  - e. Skip, track it.

### i3. A document edit runs every guard that reads that document

- **What it is:** a `--docs` mode in `select_proofs.py` that, for the
  changed `.md` files, runs every guard that reads them (figures,
  learning documents, US English, amendments, drift), about 2 minutes;
  the Phase 4 checklist runs it before each document commit.
- **What it prevents and/or catches:** prevents a 9-17 minute gate
  failure on a document, at the development stage.
- **Long-term value:** documents change in every sprint; each guard
  reads a different set.
- **Evidence:** 2 gate failures this sprint from one edit (about 30
  minutes of reruns).
- **Pros and cons:** pro: fast feedback. Con: the map of guards to
  documents must stay current; the selector already holds one.
- **Prevention or control:** prevention. **Extends:**
  `select_proofs.py`'s existing selection. **Effort:** about 45
  minutes; 2 files.
- **Options for implementing:**
  - a. Backlog F212, priority 12, in Sprint 35. Pro: reuses the
    selector. Con: Sprint 35 grows. **(Recommendation)**
  - c. A checklist line naming the four guards. Pro: 5 minutes. Con:
    the list goes stale.
  - e. Skip, track it.

### i4. The figure guard reads the amendments file

- **What it is:** `test_phase2_figures_resolve.py` also checks
  `experiments/phase2/PREREGISTRATION_AMENDMENTS.md`: each entry's
  figures must resolve in the result file the entry names.
- **What it prevents and/or catches:** catches, at the testing stage, a
  figure from an unrecorded check. Prevention (quote only recorded
  results) is already the rule; this checks it.
- **Long-term value:** the ledger cannot be edited, so an error stays
  and needs a correction entry.
- **Evidence:** P2-A6's two figures, withdrawn by P2-A8 (about 20
  minutes); Sprint 33 i1 was the same class in another document.
- **Pros and cons:** pro: the ledger meets the same rule as the
  documents. Con: earlier entries may need registry lines.
- **Prevention or control:** control, because only a check can enforce
  the existing rule. **Extends:** `test_phase2_figures_resolve.py`.
  **Effort:** about 30 minutes; 2 files.
- **Options for implementing:**
  - a. Backlog F213, priority 11, in Sprint 35. Pro: small. Con: waits a
    sprint. **(Recommendation)**
  - b. Now. Pro: at once. Con: sprint size.
  - e. Skip, track it.

### i5. The inventory guard checks the counts

- **What it is:** `test_test_inventory.py` compares each file's Tests
  count with pytest's collection, so a stale or hand-edited count fails.
- **What it prevents and/or catches:** catches, at the testing stage, a
  stale inventory.
- **Long-term value:** the inventory is read to size test work.
- **Evidence:** two stale counts this sprint, not detected.
- **Pros and cons:** pro: the "do not edit by hand" line is enforced.
  Con: collection adds about 20 seconds.
- **Prevention or control:** control. **Extends:**
  `test_test_inventory.py`. **Effort:** about 30 minutes; 1 file.
- **Options for implementing:**
  - a. Backlog F214, priority 13. Pro: small. Con: waits.
    **(Recommendation)**
  - e. Skip, track it; regenerate the inventory in Sprint 35 (category
    13).

### i6. A task's commits need its timer running

- **What it is:** `.githooks/commit-msg` requires the named task's
  timer for every commit that names a task issue, `docs:` included, not
  only `feat:` and `fix:`.
- **What it prevents and/or catches:** prevents untimed work, at the
  development stage.
- **Long-term value:** effort accuracy is scored every sprint and the
  estimates for later sprints come from these actuals.
- **Evidence:** G timed at 9 minutes and H at 2 against 60 and 45 of
  plan; how much work went untimed is not measured.
- **Pros and cons:** pro: actuals become usable. Con: more hook
  refusals during documentation work.
- **Prevention or control:** prevention. **Extends:**
  `.githooks/commit-msg` (F173). **Effort:** about 30 minutes; 2 files.
- **Options for implementing:**
  - a. Now, in Sprint 34's improvement commits. Pro: Sprint 35's
    actuals are clean. Con: 30 minutes added. **(Recommendation)**
  - b. Backlog F215, priority 12. Pro: no added time now. Con: Sprint
    35 runs without it.
  - e. Skip, track it.

### i7. A run's estimate is measured, and its cap is coded

- **What it is:** the Phase 3 plan states a run's time from a timed
  first instance or says "unmeasured", and a cap the plan states is
  coded as a refusal with a test. A line in `docs/SPRINT_CHECKLIST.md`
  Phase 3.
- **What it prevents and/or catches:** prevents a run far over its
  estimate, at the sprint-card stage.
- **Long-term value:** F25 runs metered blocks in Sprint 35; an
  uncoded cap there costs device seconds.
- **Evidence:** E (planned 1 minute, ran 11) and F (cap 20 not coded,
  ran 15) this sprint.
- **Pros and cons:** pro: estimates rest on a measurement. Con: one
  timed instance per run at planning.
- **Prevention or control:** prevention. **Extends:** Criterion H's
  provenance rule (measured, extrapolated, unknown) to unmetered runs.
  **Effort:** about 10 minutes; 1 file.
- **Options for implementing:**
  - a. Now, in the improvement commits. Pro: it binds Sprint 35's plan.
    Con: none of note. **(Recommendation)**
  - e. Skip, track it.

### i8. The handover screen list is printed from the file

- **What it is:** `docs/SPRINT_CHECKLIST.md` Phase 5.3: the screen list
  is the validation file's Actions section, printed after the file is
  final, with the same numbers.
- **What it prevents and/or catches:** prevents a screen list and a
  file that differ, at the sprint-process stage.
- **Long-term value:** answers are given against numbers; two numberings
  make an answer ambiguous.
- **Evidence:** this sprint (screen A1-A6, file A1-A5); the answers
  were mapped by hand.
- **Pros and cons:** pro: one source. Con: none of note.
- **Prevention or control:** prevention. **Extends:** the Phase 5.3
  "listed to the screen" line. **Effort:** about 10 minutes; 1 file.
- **Options for implementing:**
  - a. Now, in the improvement commits. **(Recommendation)** Pro: cheap.
    Con: none of note.
  - e. Skip, track it.

### i9. The tag hook tokenizes the command

- **What it is:** `block_frozen_history_rewrite.py` splits the command
  with `shlex`, skips git's global options, and checks each argument
  for a delete or force flag (grouped flags included), a `:` or `+`
  refspec, `update-ref --stdin` and `push --mirror`, when a freeze tag
  is named.
- **What it prevents and/or catches:** prevents a session moving or
  deleting a freeze tag by a command shape the patterns miss, at the
  development stage.
- **Long-term value:** D7 chose the hook only, so the hook is the whole
  control.
- **Evidence:** 4 shapes missed (code review), 5 more ways past it
  (security review), this sprint; no tag was moved.
- **Pros and cons:** pro: closes the known shapes. Con: a local hook
  never covers every client.
- **Prevention or control:** prevention. **Extends:** the existing
  hook. **Effort:** about 60 minutes; 2 files.
- **Options for implementing:**
  - a. Backlog F216, priority 12. Pro: sized and scheduled. Con: the
    gap stays until then. **(Recommendation)**
  - b. Now. Pro: at once. Con: sprint size.
  - e. Skip, track it.

## Improvement Decisions

| # (i1-in) | Title | Alternative taken (a-z) | Effort | Decision (now/backlog/skip) |
|---|---|---|---|---|
