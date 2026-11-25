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

Format: this repository's step 5 fields, merged with the team lead's
example from spamfilter-multi (2026-11-24): a **Source** line, and an
**Effort** line that gives each option's effort and its impact on test
time, measured or marked as a best guess (i10). Test impacts marked
"measured" come from one run on 2026-11-24:
`experiments/src/test_f188_rounding.py`, non-proof, 23 s without
coverage and 43 s with branch coverage.

### i1. A refusal is designed, briefed and confirmed testable before the gate (revised)

Revised 2026-11-24 at the team lead's request: "How can we develop and
test so that the refusal-coverage check is extremely unlikely to fail."
The first version (coverage in the pre-push gate) is now option c.

- **What it is:** three layers, earliest first.
  1. Sprint card: a card that adds a refusal names it in its acceptance
     criteria as "refusal: <what is refused> -> test <test name>".
  2. Design rule, given in the agent's brief and in the Phase 4
     checklist: a refusal lives in a small named function
     (`require_*`, `check_*` or `main(argv)`) that a test calls
     in-process with built data. `run()` and the `__main__` block only
     call it. The agent's return lists each new refusal with its test
     and its red-proof mutation.
  3. Orchestrator confirmation at task end: `select_proofs.py
     --refusals` runs the changed modules' own test files under branch
     coverage, then `refusal_coverage.py` on the task's diff. CI's step
     stays as the final control.
- **Source:** category 2 (Claude); the CI finding on 76c740b.
- **What it prevents:** an untested refusal, at the sprint-card stage
  (named in the acceptance), the brief stage (designed testable) and
  the development stage (confirmed at task end, before the gate).
- **Prevention or control:** prevention (layers 1-2); layer 3 is a
  control at the task's end, kept because the design rule can be
  missed.
- **Extends:** `refusal_coverage.py` (CI's step), `select_proofs.py`,
  the Phase 4 per-term test line, the agent-brief requirements.
- **Long-term value:** every experiment module adds refusals; this
  class reached review 37 times in Sprints 28-30.
- **Evidence:** 3 this sprint, all in code that needs real data to
  reach (a label check inside `run()`, two argument checks in the
  `__main__` block): the exact shape layer 2 removes. One red CI round,
  about 40 minutes.
- **Pros and cons:** pro: the refusal is testable by design, so the
  check rarely has anything to find. Con: small modules get a few more
  named functions.
- **Effort:** a: about 75 minutes in all (rules about 15 minutes, 3
  files, now; `--refusals` about 60 minutes, 2 files and tests, in
  Sprint 35); test impact: about 20-45 s per task that adds a refusal
  (measured: one module's tests take 1.9 times as long under branch
  coverage, 23 s to 43 s), suite about +3 s (best guess), gate
  unchanged. b: about 15 minutes, 3 files; test impact 0 s. c: about
  60 minutes, 2 files and a test; test impact: the gate takes about 1.9
  times as long, 9-19 minutes becoming about 17-36 (extrapolated from
  the one measured file).
  - a. Rules now; `--refusals` as F210, priority 11, in Sprint 35.
    Pro: three layers before CI. Con: Sprint 35 grows by an hour.
    **(Recommendation)**
  - b. Rules only (layers 1-2), now. Pro: 15 minutes, no test cost.
    Con: nothing confirms them before CI.
  - c. Branch coverage and the refusal check in the pre-push gate (the
    first proposal), F210, priority 11. Pro: catches every case before
    push. Con: every gate run about doubles.
  - e. Skip this sprint, track. Pro: no work. Con: CI keeps finding
    them.
- **Decision**: a.

### i2. Files written during a gate run go where the gate does not look (revised)

Revised 2026-11-24 at the team lead's request: prevention as early as
possible, and "arrange the working files so they can be used while the
test runs without conflict (naming convention...)". The first version
(a lock hook) is now option c.

- **What it is:** a naming convention and a place in the process.
  Anything written while a gate runs (a draft, notes, a decision being
  written) goes to a gitignored `wip/` folder at the repository root
  and is moved into place after the run. `git status` skips ignored
  files, so the gate neither refuses nor loses the run;
  `.claude/sprint_status.json` is already exempt (`UNTESTED_OK`). The
  Phase 4 and Phase 7 checklists say: commit, start the gate, then
  write only under `wip/` until it reports.
- **Source:** category 9 (Claude).
- **What it prevents:** a gate run that cannot count, at the sprint
  process stage (the step order) and development stage (the folder).
- **Prevention or control:** prevention.
- **Extends:** the gate's tree check (`select_proofs.py`
  `other_changes`, Sprint 33 i3) and `.gitignore`.
- **Long-term value:** each gate run is 9-19 minutes; work can go on
  during it instead of waiting.
- **Evidence:** this sprint, one lost pass (12 minutes, then a
  19-minute rerun: about 31 minutes) and one refused start; Sprint 33
  i3 was the same class.
- **Pros and cons:** pro: writing continues during the run. Con:
  tracked files (CHANGELOG, decisions) still wait for the run to end.
- **Effort:** a: about 15 minutes, 2 files (`.gitignore`,
  `docs/SPRINT_CHECKLIST.md`); test impact 0 s (no test runs are added;
  `wip/` is a new folder, so no test reads it). b: about 2 hours, 3 files; test impact about
  +5-10 s per gate run for the worktree setup (best guess). c: about 40
  minutes, 3 files; test impact about +2 s per suite (best guess).
  - a. The `wip/` convention, its ignore rule and the checklist lines,
    now. Pro: cheap, nothing new to maintain. Con: tracked files still
    wait. **(Recommendation)**
  - b. The gate runs in a separate git worktree of HEAD, with a link to
    the gitignored data, F211, priority 12, in Sprint 35. Pro: the
    whole tree is free during the run. Con: the data link must be kept
    right, or data tests skip there.
  - c. A lock file and a hook that blocks writes during the run (the
    first proposal), F211, priority 12. Pro: enforced. Con: it blocks
    work instead of allowing it.
  - e. Skip this sprint, track. Pro: no work. Con: lost runs recur.
- **Decision**: a.

### i3. A document edit runs every check that reads that document

- **What it is:** a `--docs` mode in `select_proofs.py` running every
  guard that reads the changed documents.
- **Source:** category 1 (Claude).
- **Prevention or control:** prevention. **Extends:**
  `select_proofs.py`.
- **Evidence:** 2 gate failures from one edit, about 30 minutes.
- **Effort:** a: about 45 minutes, 2 files; test impact about 2 minutes
  per document commit, saving a 9-17 minute gate rerun per failure
  (best guess). e: 0.
  - a. Backlog F212, priority 12. **(Recommendation)**
  - e. Skip this sprint, track it.
- **Decision**: e.

### i4. The figure check reads the amendments file

- **What it is:** `test_phase2_figures_resolve.py` also checks
  `experiments/phase2/PREREGISTRATION_AMENDMENTS.md`; each entry's
  figures resolve in the result file it names.
- **Source:** category 8 (Claude); review finding 3.
- **Prevention or control:** control. **Extends:**
  `test_phase2_figures_resolve.py`.
- **Evidence:** P2-A6's two figures, withdrawn by P2-A8 (about 20
  minutes).
- **Effort:** a: about 30 minutes, 2 files; test impact about +1 s per
  suite (best guess: one more document parsed).
  - a. Backlog F213, priority 11, Sprint 35. **(Recommendation)**
  - e. Skip, track.
- **Decision**: a.

### i5. The inventory check compares the test counts

- **What it is:** `test_test_inventory.py` compares each Tests count
  with pytest's collection.
- **Source:** category 8 (Claude).
- **Prevention or control:** control. **Extends:**
  `test_test_inventory.py`.
- **Evidence:** two stale counts, not detected.
- **Effort:** a: about 30 minutes, 1 file; test impact about +15-20 s
  per suite (best guess: one collection pass).
  - a. Backlog F214, priority 13. **(Recommendation)**
  - e. Skip, track.
- **Decision**: a.

### i6. Every commit for a task needs that task's timer running

- **What it is:** `.githooks/commit-msg` requires the named task's
  timer for every commit naming a task issue, `docs:` included.
- **Source:** category 3 (Claude).
- **Prevention or control:** prevention. **Extends:**
  `.githooks/commit-msg` (F173).
- **Evidence:** G timed 9 of 60 planned minutes, H 2 of 45.
- **Effort:** a and b: about 30 minutes, 2 files; test impact about +1
  s per suite (best guess: a few hook cases).
  - a. Now. **(Recommendation)**
  - b. Backlog F215, priority 12.
  - e. Skip, track.
- **Decision**: b.

### i7. A run's time estimate is measured, and its time cap is coded

- **What it is:** a Phase 3 checklist line: run times from a timed
  first instance, and stated caps coded as tested refusals.
- **Source:** category 3 and 4 (Claude).
- **Prevention or control:** prevention. **Extends:** Criterion H's
  provenance rule.
- **Evidence:** E planned 1 minute, ran 11; F's cap not coded, ran 15.
- **Effort:** a: about 10 minutes, 1 file; test impact 0 s.
  - a. Now. **(Recommendation)**
  - e. Skip, track.
- **Decision**: e.

### i8. The Manual Validation list on screen is printed from the file

- **What it is:** a Phase 5.3 checklist line: the screen list is the
  validation file's Actions section, printed after the file is final.
- **Source:** category 6 (Claude).
- **Prevention or control:** prevention. **Extends:** the Phase 5.3
  "listed to the screen" line.
- **Evidence:** screen A1-A6 against file A1-A5 this sprint.
- **Effort:** a: about 10 minutes, 1 file; test impact 0 s.
  - a. Now. **(Recommendation)**
  - e. Skip, track.
- **Decision**: a.

### i9. The tag hook reads the command word by word

- **What it is:** `block_frozen_history_rewrite.py` splits the command
  with `shlex`, skips git's global options, and checks each argument.
- **Source:** category 10 (Claude); the code and security reviews.
- **Prevention or control:** prevention. **Extends:** the existing
  hook.
- **Evidence:** 4 shapes missed (code review), 5 more ways past it
  (security review).
- **Effort:** a: about 60 minutes, 2 files; test impact about +2 s per
  suite (best guess: about 15 parity cases).
  - a. Backlog F216, priority 12. **(Recommendation)**
  - b. Now.
  - e. Skip, track.
- **Decision**: a.

### i10. The merged item format becomes the standing format

- **What it is:** `docs/SPRINT_RETROSPECTIVE.md` step 5 adds the
  **Source** line and an **Effort** line giving each option's effort and
  its test-time impact, measured or marked as a best guess. "Not
  measured" is not accepted for effort or test impact.
- **Source:** the team lead, 2026-11-24 (the spamfilter-multi example).
- **Prevention or control:** prevention (sprint process stage).
- **Extends:** step 5's field list and its checklist.
- **Evidence:** this retrospective's first display had no per-option
  effort and no test impact, and wrote "not measured".
- **Effort:** a: about 10 minutes, 1 file; test impact 0 s.
  - a. Now. **(Recommendation)**
  - e. Skip, track.
- **Decision**: a.

## Improvement Decisions

Answered 2026-11-24, verbatim in substance: "i1" and "i2" asked to be
reworked (questions above); "i3. e", "i4. a", "i5. a", "i6. b",
"i7. e", "i8. a", "i9. a".

Revised items answered 2026-11-24, verbatim: "i1. a i2. a i10. a".

| # (i1-in) | Title | Alternative taken (a-z) | Effort | Decision (now/backlog/skip) |
|---|---|---|---|---|
| i1 | Refusals testable before the gate | a | 15 min now; 60 min F210 | rules now (`SPRINT_PLANNING.md`, `SPRINT_CHECKLIST.md` Phase 4, `docs/agent_prompts/research.md`); backlog F210, P11, Sprint 35 |
| i2 | Gate-time writes to `wip/` | a | 15 min | now (`.gitignore`, `SPRINT_CHECKLIST.md` Phases 4 and 7) |
| i3 | Document edits run their guards | e | 0 | skip, tracked |
| i4 | Figure check reads amendments | a | 30 min | backlog F213, P11, Sprint 35 |
| i5 | Inventory counts checked | a | 30 min | backlog F214, P13 |
| i6 | Commit needs the task timer | b | 30 min | backlog F215, P12 |
| i7 | Run estimates measured, caps coded | e | 0 | skip, tracked |
| i8 | Screen list printed from the file | a | 10 min | now |
| i9 | Tag hook tokenizes | a | 60 min | backlog F216, P12 |
| i10 | Merged item format | a | 10 min | now (`SPRINT_RETROSPECTIVE.md` step 5 and its checklist; `SPRINT_CHECKLIST.md` Phase 7) |
