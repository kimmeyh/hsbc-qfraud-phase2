# Sprint 32 Retrospective

**Sprint**: 32, Close a Device Question, State Results in Dollars,
Tighten Two Guards
**Date**: 2026-11-13
**Scope**: F181 (A), F194 (B), F188 (C), F185 (D), F178 (E), the F150
request draft (F), the F111 feedback draft (G); added: the PR #116
review findings (H). Issues #110-#115, #117 and #118, all closed. Draft
PR #116.
**Effort**: `.claude/sprint_status.json` `task_actuals`, against the
plan's 210 estimated minutes. See category 3.
**Metered seconds**: 0.

## Scoring, both roles

The team lead scored every category **Very Good**. Claude scored five
lower. The improvements are built from the lower scores.

| Category | Team lead | Claude |
|---|---|---|
| Effective while as efficient as reasonably possible | Very Good | **Good** |
| Testing approach | Very Good | **Good** |
| Effort accuracy | Very Good | **Good** |
| Planning quality | Very Good | Very Good |
| Model assignments | Very Good | Very Good |
| Communication | Very Good | **Good** |
| Requirements clarity | Very Good | Very Good |
| Documentation | Very Good | Very Good |
| Process issues | Very Good | **Good** |
| Risk management | Very Good | Very Good |
| Next sprint readiness | Very Good | Very Good |
| Architecture maintenance | Very Good | Very Good |
| Assigned coding agents quality | Very Good | Very Good |

Team lead: minor function updates "none"; backlog additions "none";
questions before ending the sprint "none".

## Sprint 32 Retrospective Feedback

The team lead gave combined Product Owner, Scrum Master and Lead Developer
feedback on 2026-11-13, with "Manual Validation complete", recorded
verbatim under each of the three roles. Claude's lines were written while
the Phase 6 reviews ran
(`docs/sprints/drafts/SPRINT_32_RETROSPECTIVE_claude_draft.md`), and
category 15 was updated after the code review returned.

### 1. Effective while as Efficient as Reasonably Possible
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. All seven tasks met their
  acceptance criteria with zero metered seconds, and both results answer
  the question their card asked. Rework: two CI reds (5027f4f, c692eac)
  and one vacuous red proof (fixed in bcf67ad), each found by CI, not by
  me before the push. The fresh-eyes review caught three wrong claims in
  the F188 document before handover, and the PR review found a gap in
  Task A's rule (Task H).

### 2. Testing Approach
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. Every new rule has its own test
  and red proof, and `assert_can_fail` caught the vacuous proof as
  designed. But the local check the checklist names for a task
  (`scripts/select_proofs.py --tests --base HEAD`) was skipped in Tasks B
  and C, so two failures reached CI that it would have caught. Task A's
  rule was tested only against the shapes I wrote; the review found
  three more that passed it. The parallel Phase 5 suite ran out of memory
  on this machine (9 files); the serial rerun of the same files passed.

### 3. Effort Accuracy
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. 152 recorded active minutes
  against 210 estimated for A-G, plus H. B (37 of 45) and E (36 of 30)
  were close. C ran over (47 of 30) because of the amendment's second
  reading; D ran under (24 of 60) and overlapped C. Three actuals are
  wrong: A's 1 minute (the timer did not start, i1), and H's 2 minutes
  (its timer started only when the commit hook asked for it, after the
  fixes were made). F's 3 and G's 2 minutes leave out reading time spent
  before each timer started. The time not recorded is not measured.

### 4. Planning Quality
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. Each task had a "show it
  can fire" line before it ran, and both experiment checks fired first.
  D3's order (E after every other step, then F and G) worked as written.
  One gap, i3: Task A's "fires" line named one shape of the forbidden
  call, not each way to reach it.

### 5. Model Assignments
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. The main loop did all
  tasks. One fresh-eyes reviewer and one PR code reviewer each found
  material defects; Copilot found two small ones.

### 6. Communication
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. The handover listed only
  actions, with full paths, and D4 was written to the file before it was
  asked. Gaps: commit 3520a0f's message names only Task D but carries
  Task C's document too, and I hid the status tool's refusal behind
  `tail -1` (i1).

### 7. Requirements Clarity
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. D2's "after this sprint"
  had two readings; D3 asked which, and the answer added Task G.

### 8. Documentation
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. Both result documents
  state what was registered and what came after it, and the F188
  amendment is dated and logged in the preregistration draft. The PR
  review found one untested cause stated as a finding in the F185
  document; it is now marked Inferred.

### 9. Process Issues
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. Four frictions: the timer
  refusal (i1); a CHANGELOG hook block left Task C's files staged, and
  they went into Task D's commit; `test_no_proofs_under_xdist.py` runs
  near its 300 s limit under load; the parallel suite's memory failures
  (i4).

### 10. Risk Management
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. The F188 reading that
  could have closed F25 was not used to close it: the registered rule
  said "open", and D4 left the call to the team lead (answered 3). F185's
  document states its unverified unit and its dependence on calibration.

### 11. Next Sprint Readiness
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. F198 is carded from D4; no
  Sprint 33 run is preregistered yet, and the learning documents say so.

### 12. Architecture Maintenance
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. Both new modules use
  `provenance.start` and `write_result`, carry outcome blocks, and
  declare `LONG_RUN` (after the CI red). The frozen preregistration was
  not touched.

### 13. Minor Function Updates for the Next Sprint Plan
- **Product Owner**: none
- **Scrum Master**: none
- **Lead Developer**: none
- **Claude Code Development Team**: none beyond the items below (i1-i5).

### 14. Function Updates for the Future Backlog
- **Product Owner**: none
- **Scrum Master**: none
- **Lead Developer**: none
- **Claude Code Development Team**: [Claude] F198, carded at D4 --
  estimated: 30m, priority: 10, depends on: nothing. Others only as the
  items below propose.

### 15. Assigned Coding Agents Quality
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. The fresh-eyes reviewer's
  three material findings were real and fixed. The PR code reviewer
  proved its main finding with a probe script (three bypassing shapes),
  checked every figure in both documents against the results, and
  separated two findings above its bar from three below it. No finding
  needed rework.

### 16. Questions to be discussed before ending the sprint
- **Product Owner**: none
- **Scrum Master**: none
- **Lead Developer**: none
- **Claude Code Development Team**: none

## Review findings fixed (Task H, #118)

- Copilot 1: `f185_cost_budget.checked_scores` left the npz file open.
  Fixed (605d01a).
- Copilot 2: "Dirace-3S" in the device guard's docstring. It quotes the
  team lead's D5 rule verbatim; marked [sic], not changed (605d01a).
- Code review 1 (confidence 85): F181's rule missed a held literal, a
  keyword argument and a `from` import of `DIRAC_3`. Fixed; each shape
  and the one exclusion (a record's `"device": "dirac-3"` history label)
  has a test and a red proof (8e0796a).
- Code review 2 (82): the F185 document stated an untested cause as a
  finding. Marked Inferred (8e0796a).
- Code review, below its bar: the F185 label-flip check takes a shorter
  path than the entry states (now disclosed in the document); the F188
  document's "weights a device can represent" (corrected). Both 8e0796a.

## Review finding classes (input to the improvements)

- **A source-scan guard tested only against the shape its author wrote**:
  recurring. Sprint 32 code review 1; Sprint 31 i3 (the refusal gate
  missed the repository's refusal forms); Sprint 28 IMP-2 (prose read as
  a call). Improvement: i3.
- **A check that ran after the push instead of before it**: recurring.
  Sprint 32: 5027f4f and c692eac red on CI, the vacuous proof found by
  CI; Sprint 31: Task N, CI red on dfb1694. Improvement: i2.
- **Resource handling** (the open npz): single finding. Root cause: the
  module copied `np.load` usage that is safe in a short script and not
  under a test's temporary folder on Windows. No item.
- **A cause stated as a finding**: single finding this sprint (the
  fresh-eyes review's F188 corrections were of wrong facts, not of
  untested causes). Root cause: the "What it found" section was written
  from the per-seed numbers, before "What it means" set the limit. No
  item.

## Review findings not fixed (for the team lead's disposition)

- **F185's two rankings are not forced to flag the same count**
  (code review, confidence about 60). `flagged_at_budget` flags every row
  tied at the cut, so a tie could make the counts differ. The run shows
  equal counts (284 and 427), so the result holds. Item i5.

## Improvements proposed

In the format of `SPRINT_RETROSPECTIVE.md` step 5.

### i1. The status tool's timer starts when a repeated estimate matches

- **What it is:** in `scripts/update_sprint_status.py`, `set_estimate`
  treats an estimate equal to the recorded one as no change, so
  `--start-task X --estimate N` still starts the timer; a different
  estimate is still refused. A test and a red proof in
  `test_update_sprint_status.py`.
- **What it prevents and/or catches:** prevents, at the development
  stage (the tool the sprint runs on), a start command that silently
  does not start. Today the refusal prints, but one line, which is easy
  to lose in piped output.
- **Long-term value:** every later sprint's actual minutes feed
  `VELOCITY_LOG.md` and the next plan's estimates; a lost start corrupts
  both.
- **Evidence:** once, Sprint 32 Task A: recorded 1 minute; the true time
  is not measured. My `tail -1` hid the refusal. Earlier sprints: not
  measured.
- **Pros and cons:** pro: removes a refusal that protects nothing (the
  same estimate twice is not a conflict). Con: one more branch in the
  tool.
- **Prevention or control:** prevention. **Extends:** the existing
  second-estimate refusal in `set_estimate`. **Effort:** about 15
  minutes, 2 files.
- **Options for implementing:**
  - **a. (Recommendation)** Equal estimate is a no-op, now, about 15
    minutes. Pro: the command does what it says. Con: none found.
  - **c.** Print the refusal to stderr in capitals, now, 5 minutes. Pro:
    smaller change. Con: still refuses a harmless repeat.
  - **e.** Skip, track for recurrence. Pro: no time. Con: Task A's error
    can repeat.
  - **f.** Skip.

### i2. Tests of the pushed change run before the push, not after

- **What it is:** a git pre-push hook, `.githooks/pre-push`, that refuses
  a push unless `scripts/select_proofs.py --tests` has passed on the
  exact tree being pushed. `select_proofs.py --tests` records the tree
  hash it passed on in a gitignored file; the hook compares it with
  `git rev-parse HEAD^{tree}`. A test of the hook, with a red proof.
- **What it prevents and/or catches:** prevents, at the development
  stage, a push whose changed files' tests were not run. It does not run
  the tests itself, so a push is not slowed when they were run.
- **Long-term value:** CI reds stop being the first test of a change;
  each costs a fix commit, a CI rerun and a CHANGELOG entry.
- **Evidence:** Sprint 32: two CI reds (5027f4f, c692eac), each a test
  the local `--tests` run would have failed; Sprint 31: Task N (CI red on
  dfb1694). Time per red: not measured.
- **Pros and cons:** pro: enforces a rule the checklist already states
  (line 37). Con: a doc-only push also needs a run (the run is short
  when only documents changed).
- **Prevention or control:** prevention. **Extends:** the existing
  `.githooks/` hooks and `select_proofs.py --tests`. **Effort:** about 60
  minutes, 3-4 files.
- **Options for implementing:**
  - **a.** The hook as described, now, about 60 minutes. Pro: in force
    from Sprint 33's first push. Con: past the sprint's time target.
  - **b. (Recommendation)** The same, as backlog card F199, priority 15,
    about 60 minutes. Pro: planned and estimated in Sprint 33's own
    selection. Con: Sprint 33's first pushes are unguarded unless it is
    selected.
  - **c.** A pre-push hook that runs `select_proofs.py --tests` itself,
    now, about 20 minutes. Pro: simplest. Con: every push waits 2-5
    minutes, even when the tests were just run.
  - **e.** Skip, track for recurrence. Pro: no time. Con: it has already
    recurred.
  - **f.** Skip.

### i3. A scan guard's "fires" line names each way to reach the thing

- **What it is:** in `docs/SPRINT_CHECKLIST.md` (Phase 3, "Show each
  threshold can fire"), one sentence: "for a source-scan guard, the
  fires line lists each way the forbidden thing can be reached (a held
  variable, a keyword argument, an import, an alias) and the plan's test
  covers each".
- **What it prevents and/or catches:** prevents, at the sprint card
  stage, a scan guard tested only against the shape its author first
  thought of.
- **Long-term value:** this repository relies on source-scan guards for
  its hardware, refusal and provenance rules; each new one inherits the
  check.
- **Evidence:** three occurrences: Sprint 32 (F181 rule, three bypassing
  shapes), Sprint 31 i3 (refusal forms), Sprint 28 IMP-2 (prose read as
  a call). Time: Task H's fix, not measured.
- **Pros and cons:** pro: one sentence at the stage where the card is
  written. Con: relies on the checklist being read.
- **Prevention or control:** prevention. **Extends:** the existing "show
  each threshold can fire" item (Sprint 25 IMP-2, Sprint 28 IMP-5).
  **Effort:** about 5 minutes, 1 file.
- **Options for implementing:**
  - **a. (Recommendation)** The checklist sentence, now, 5 minutes. Pro:
    applies from Sprint 33's planning. Con: not enforced.
  - **c.** A shared helper in `source_scan.py` that every scan guard uses
    to match a name held, imported or passed by keyword, as backlog card
    F200, priority 40, about 90 minutes. Pro: enforced by reuse. Con:
    each guard's forbidden shapes differ; a helper fits some only.
  - **e.** Skip, track. Pro: no time. Con: it has recurred three times.
  - **f.** Skip.

### i4. The parallel suite's memory failures get a troubleshooting entry

- **What it is:** an entry in `docs/TROUBLESHOOTING.md` ("Shell, paths
  and tooling on this workstation"): symptom, MemoryError or crashed
  xdist workers in the Phase 5 parallel run; cause, `-n auto` on this
  machine's memory; action, rerun the failed files serially, and read a
  failure as code only if it fails there.
- **What it prevents and/or catches:** prevents, at the testing stage, a
  memory failure read as a code failure, or a session spending time on
  it.
- **Long-term value:** the next session that sees it finds the answer in
  one place (category 9's rule).
- **Evidence:** once, Sprint 32 Phase 5: 9 files failed in parallel; the
  serial rerun passed (188 tests). Earlier: not measured.
- **Pros and cons:** pro: 5 minutes. Con: it does not stop the failure.
- **Prevention or control:** control: prevention would cap the workers,
  and the right cap is not measured. **Extends:** `TROUBLESHOOTING.md`.
  **Effort:** 5 minutes, 1 file.
- **Options for implementing:**
  - **a. (Recommendation)** The entry, now, 5 minutes. Pro: cheap and
    findable. Con: a control, not prevention.
  - **c.** Change the Phase 5 command to `-n 4`, now, 10 minutes. Pro:
    may prevent it. Con: the cap is a guess and slows a machine that has
    the memory.
  - **e.** Skip, track. Pro: no time. Con: rediscovered next time.
  - **f.** Skip.

### i5. F185's rankings forced to flag the same count

- **What it is:** `f185_cost_budget.compare` refuses when the two
  rankings flag different numbers of rows, with a test and a red proof.
- **What it prevents and/or catches:** catches, at the development
  stage, a rerun where a tie at the cut makes the comparison unequal.
- **Long-term value:** small: the recorded result already shows equal
  counts, and a rerun is refused by provenance unless replaced.
- **Evidence:** zero occurrences; the review's note (confidence about
  60).
- **Pros and cons:** pro: the "same alert count" claim becomes a check.
  Con: the generator changes after its result was recorded.
- **Prevention or control:** control. **Extends:** the module's existing
  refusals. **Effort:** about 15 minutes, 2 files.
- **Options for implementing:**
  - **a.** The refusal, now, 15 minutes. Pro: the claim is enforced.
    Con: changes a generator whose result is recorded.
  - **e. (Recommendation)** Skip, track: if F185 is rerun or extended
    (calibrated scores), add the refusal then. Pro: no change to a
    recorded generator. Con: the claim stays checked by the result only.
  - **f.** Skip.

## Improvement Decisions

Team lead, 2026-11-16, verbatim: "i1. a i2. a i3. a i4. a i5. e".

| # (i1-in) | Title | Alternative taken (a-z) | Effort | Decision (now/backlog/skip) |
|---|---|---|---|---|
| i1 | The timer starts when a repeated estimate matches | a | about 15 min | now (bb37d0d) |
| i2 | Tests run before the push | a | about 60 min | now (77101ad) |
| i3 | A scan guard's "fires" line names each way to reach the forbidden thing | a | 5 min | now (8640767); placed in `SPRINT_PLANNING.md` beside "show each term can fire", not in `SPRINT_CHECKLIST.md` as the item said, because the checklist has no such line and the "show it can fire" rules live in `SPRINT_PLANNING.md` |
| i4 | A troubleshooting entry for the parallel suite's memory failures | a | 5 min | now (8640767) |
| i5 | F185's two rankings forced to flag the same count | e | none | skip, tracked: add the refusal if F185 is rerun or extended |

Observed while applying i1 (2026-11-16), not yet an item: the status
tool's first `--add-issue 119 --task I --estimate 85` printed "could not
be replaced ... Nothing was written", yet the rerun found the estimate and
the issue already recorded. The message was wrong in that run; the cause
was not found. Tracked here in case it recurs.
