# Sprint 31 Retrospective

**Sprint**: 31, Make Testing Fast and Sure, Then Read the Ceiling, the
Segments and Dirac-3S
**Date**: 2026-11-07
**Scope**: F179 (A), F180 (B), F177 (C), the pypdf bump (D), F114 (E),
F157 SPECTRA (F), F157 QNN (G), F121 (H), F155 (I), F95 (J), F178 (K),
F13 (L); added: the Phase 5 fresh-eyes fixes (M), CI red on dfb1694 (N)
and the learning documents' A1 review (O). Issues #93-107. Draft PR #92.
**Effort**: `.claude/sprint_status.json`, `task_actuals` (active) and
`task_elapsed`, against the plan's 1,569 minutes. See category 3.
**Metered seconds**: the F155 and F95 Dirac-3S blocks only, each approved
per block (D9, D10, D12); the figures are in `SPRINT_31_VALIDATION.md` V9.

## Scoring, both roles

The team lead scored every category **Very Good**. Claude scored six
lower. Where the two disagree both are recorded, and the improvements are
built from the lower score.

| Category | Team lead | Claude |
|---|---|---|
| Effective while as efficient as reasonably possible | Very Good | **Good** |
| Testing approach | Very Good | **Good** |
| Effort accuracy | Very Good | **Poor** |
| Planning quality | Very Good | **Good** |
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

## Sprint 31 Retrospective Feedback

The team lead gave combined Product Owner, Scrum Master and Lead Developer
feedback on 2026-11-07, with "Manual Validation complete", recorded
verbatim under each of the three roles. Claude's lines were written while
the Phase 6 reviews ran.

### 1. Effective while as Efficient as Reasonably Possible
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. All twelve planned tasks met
  their acceptance, and both Dirac-3S blocks ran under per-block approval.
  Three tasks were added: M (the fresh-eyes findings), N (CI red on
  dfb1694 from a defect I introduced) and O (the A1 review of the
  learning documents). N is rework a local check could have caught. The
  sprint took 2,893 active minutes against a 1-2 hour sprint target;
  D17 now cuts the test share of that, but the scope of twelve tasks,
  six of them experiments, is the larger cause.

### 2. Testing Approach
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. Every new guard was proven red,
  and D16's nine untested refusals each gained a test and a proof. Three
  defects were in the verification, not in the thing verified. A
  vacuous proof ("a comment read as code") was caught before commit. One
  proof's mutation removed the `--tests` refusal, so the refusal test
  started real test runs that included itself; the runs nested without
  end from 16:29 to 17:52 on 2026-11-06. The first `--tests` selection
  took 110 of 163 files for one task's change; I found it only by running
  it, and the narrowed rule gives 30 files in 4 minutes 46 seconds. The
  inventory guard caught the two new test files missing from F180's
  inventory.

### 3. Effort Accuracy
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Poor. The twelve planned tasks took
  2,658 active minutes against 1,569 estimated (1.69). Over: E 316
  against 90 (3.5), I 99 against 30 (3.3), K 518 against 234 (2.2), F
  514 against 240 (2.1), J 189 against 90 (2.1), G 201 against 120, C
  336 against 240, B 229 against 180, L 101 against 75. Under: D 2
  against 45, H 95 against 180. The added tasks: M 41 against 150, N
  128 (no estimate), O 66 against 150. Elapsed time ran far longer than
  active (C: 2,573 elapsed, 336 active), mostly waits for answers and
  background runs. Sprint 30's research ratios (0.02-0.38) set this
  plan's estimates low; this sprint's research ran above them, so one
  sprint's ratio is not a basis for the next.

### 4. Planning Quality
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. Every task had acceptance
  criteria, and the two metered tasks stopped where the plan said. Two
  decisions needed a second round: D8 (the testing levers) was asked
  before its options were explained, and none of D15's options was taken,
  which led to D16. F180's card named the wrong deliverable folder
  (`docs/phase2/` for `docs/testing/`), fixed at Phase 5.

### 5. Model Assignments
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. The fresh-eyes agent ran
  seven units and its findings became Task M. The Phase 6 reviews ran as
  background agents while the retrospective was drafted.

### 6. Communication
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. Every decision was written to
  the decisions file before it was asked. Two faults: D17 stated "161
  proof files" when 161 was the count of proof tests (58 files), corrected
  in a dated note; and options nested under a bullet showed as letters,
  so answers came as "a" and needed a second message to confirm (now a
  memory rule: options at top level). The Stop hook rejected one typed
  footer.

### 7. Requirements Clarity
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. The team lead's V3
  comments (the CI full job under 20 minutes, the 1-2 hour sprint) and
  the A1 review were specific enough to build from without a question.

### 8. Documentation
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. The three learning
  documents reached version 1.2 with their link and acronym guard green;
  every decision carries its answer verbatim; `SPRINT_CHECKLIST.md`
  Phase 5 follows D17 as built.

### 9. Process Issues
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Good. The heredoc guard blocked two
  Python edits with `\n` in a quoted heredoc, and the metacharacter guard
  one command with `$(...)`; each was correct, and the Edit tool was the
  fix. `sprint_status.json` refused a write with WinError 5 twice although
  F179's lock was held: another process (cause unverified) had the file
  open, and a retry succeeded. A pytest stopped mid-run left no file
  changed.

### 10. Risk Management
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. Both metered blocks
  stopped for approval with the call count and seconds stated. F114's
  re-run overwrote the first run's score files; it was found, stopped
  under Criterion 7 and repaired by D13.

### 11. Next Sprint Readiness
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. Task L updated the Phase 2
  PoC plan and the backlog from this sprint's results, and D18 and
  EvidenceBasedDB's request added F184-F193.

### 12. Architecture Maintenance
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. New behavior went into
  small scripts with their own tests (`refusal_coverage.py`,
  `select_proofs.py`, `env_check.py`, `suite_times.py`); Phase 1 evidence
  was not written.

### 13. Minor Function Updates for the Next Sprint Plan
- **Product Owner**: none
- **Scrum Master**: none
- **Lead Developer**: none
- **Claude Code Development Team**: none beyond the improvements below.

### 14. Function Updates for the Future Backlog
- **Product Owner**: none
- **Scrum Master**: none
- **Lead Developer**: none
- **Claude Code Development Team**: none beyond F184-F193, already
  carded.

### 15. Assigned Coding Agents Quality
- **Product Owner**: Very Good
- **Scrum Master**: Very Good
- **Lead Developer**: Very Good
- **Claude Code Development Team**: Very Good. The fresh-eyes agent's
  findings were specific and each was fixed in Task M.

### 16. Questions to be discussed before ending the sprint
- **Product Owner**: none
- **Scrum Master**: none
- **Lead Developer**: none
- **Claude Code Development Team**: none.

## Review findings fixed (Task P, #108)

Four reviews of draft PR #92 on 2026-11-07: Copilot, and pr-review-toolkit's
code, silent-failure and test-coverage agents, each told to leave the
evidence files out. Fixed, each with a test and a red proof:

- `scripts/refusal_coverage.py`: the bare name `SystemExit` was read as a
  refusal, so `except SystemExit as exc:` could fail CI. Only a built
  `SystemExit(...)` counts now (Copilot).
- `run_dirac3s_units.py` `metered`: a returned paid call whose response
  was not stored raised before its row was written, so the result file
  lost the call and a later stop's cap read too few seconds. The row is
  written first; the refusal then marks it `stored_response_missing`, a
  nonzero state (code review).
- `run_dirac3s_units.py` `twins`: F95's reading was written `complete`
  from whatever rows existed, so a run after stop 1 alone would record a
  partial card and block the real reading. It now refuses unless F95 is
  complete and every unit has an ok row (code review and silent-failure
  review).
- `run_dirac3s_units.py`: the "built N variables, not the entry's M"
  refusal, the last offline check before a paid send, had no test
  (test-coverage review).
- `.github/workflows/ci.yml`: the refusal gate ran only in the draft-only
  push job, so a push after ready for review, the HEAD that is merged,
  was not gated. The push job now runs on every pull request push; the
  header comment no longer says the full job runs every proof
  (silent-failure review).
- `exp5_router.py`: a label mismatch was written as a complete result and
  exited 0. It now writes nothing and exits nonzero (silent-failure
  review).

Not changed, with the reason, and the thread answered:

- Copilot: "Dirace-3S" in `docs/SPRINT_EXECUTION_WORKFLOW.md` is the team
  lead's words quoted verbatim (Sprint 31 D5), so it stays as written.
- Copilot (summary only): `os.link` in `outcome_record.py` may fail
  where hard links are not supported. NTFS and the CI runner's ext4
  support them, and a fallback to replace would weaken the never-replace
  guarantee the change exists for. Its missing temporary-file cleanup is
  in the deferred list below.

## Review finding classes (input to the improvements)

1. **A refusal or rule with no test, or a test with no proof** (recurring:
   Sprint 30 IMP-2 named it). Test-coverage findings 1, 5, 8 and 9: six
   `ClaimError` refusals in `f157_spectra_docs.py`, three runner refusals,
   two `f157_spectra_algorithms.py` refusals, the `ci95[1] < 0` term in
   F114's calibration warning. And the gate D16 built cannot see the
   repository's commonest refusal form, `print("REFUSING: ..."); return N`
   (silent-failure finding 4), or a one-line `if bad: raise`.
2. **A result marked complete without checking that it is** (recurring
   this sprint: four places). `twins` and the Experiment 5 alignment stop
   (fixed); F114 `--lr05` does not read stage 1's pass; `run_rbf` does not
   check each dataset's seeds against its plan.
3. **A file read by its conventional name, not by the path its record
   holds.** Experiment 5 builds `f174_{lane}_{seed}.npz`; since this PR a
   changed re-score goes to `_v2.npz`, so it would read superseded scores
   with a valid-looking hash. Latent: no `_v2` file exists.
4. **Defects in my own verification** (recurring: Sprint 16 IMP-4, Sprint
   30). A proof whose mutation started nested test runs without end, a
   vacuous proof, and a selection rule that took 110 of 163 files, each
   found only by running it.

## Review findings not fixed (for the team lead's disposition)

- **Prove the Sprint 31 refusals red** (class 1): proofs for the tested
  refusals in `f157_spectra_docs.py` (six), `run_dirac3s_units.py` (the
  unreadable ledger, the unreadable balance, `--stop` missing, the
  intents term of `done`), `f157_spectra_algorithms.py` (two) and the
  `ci95[1] < 0` term; and `test_the_runner_refuses_when_invoked_from_a_test`
  and `test_an_unknown_stop_is_refused` moved onto `_paths` with
  `offline`, `run_stop` and `dry_run` stubbed BEFORE they get proofs,
  because a mutation of either guard today would write into
  `experiments/phase2/results/` or open a device client. About 90 minutes.
- **The refusal gate sees `REFUSING` lines and one-line raises** (class
  1): extend `refusal_coverage.py`, and in the same commit test every
  such line the branch changed, or CI goes red on them. About 60 minutes.
- **The latent set** (classes 2 and 3): Experiment 5 reads each score
  file from F174's outcome block and checks its hash; F114 `--lr05`
  refuses unless stage 1 is complete and passed; `run_rbf` refuses a
  dataset whose seeds differ from its plan; `provenance.start(replace=)`
  refuses `resumable=True`; `outcome_record` removes its temporary file
  when `os.link` fails; `f157_spectra_docs` calls `linear_paragraph` only
  for a kept RBF form, and states a missing pocket figure instead of
  leaving it out; `exp5_router`'s untested `edges()` and `accept()`
  refusals. The reviewers checked three recorded runs and found them
  unaffected: no `_v2` score file exists, F169's stage 1 recorded a
  pass, and all four SPECTRA datasets keep the RBF form. About 120
  minutes.

## Improvements proposed

In the ADR review format of `SPRINT_RETROSPECTIVE.md` step 5 (team lead,
2026-11-07). These five were first written as IMP-1 to IMP-5. They are
now i1 to i5, in the same order. D20 has a "Changed since asked" note
that records this.

### i1. A refusal test stubs what the refusal protects

- **What it is:** a Phase 4 line in `SPRINT_CHECKLIST.md`: "a test of a
  refusal replaces the action the refusal blocks (a run, a write, a
  device client) with a stub that fails at once".
- **What it prevents:** a red proof removes the refusal and then does the
  real action. In Sprint 31, the `--tests` proof started nested test
  runs that did not stop, from 16:29 to 17:52. Two runner refusal tests
  still run against real paths (test-coverage finding 2). Their proofs
  would write into `experiments/phase2/results/` or open a device client.
- **Long-term value:** every future refusal proof is safe to run, both
  locally and in CI. It protects evidence files and metered seconds.
- **Prevention or control:** prevention.
- **Extends:** the Phase 4 per-term item.
- **Effort:** about 5 minutes. One file.
- **Alternatives:**
  - **a. A checklist line (the proposal).**
    - Pros: 5 minutes. It applies to every refusal test from the next task.
    - Cons: nothing enforces it. It depends on the checklist being read.
  - **b. A test that fails a refusal test with no stub.**
    - Pros: enforced.
    - Cons: about 60 minutes. A source scan cannot tell which action a
      refusal blocks, so it would be a heuristic with false results.
  - **c. A time limit on each proof run.**
    - Pros: stops a run that does not end.
    - Cons: a control, not prevention. It does not stop a write or a
      device call that happens before the limit.
- **Recommendation: a, now.** It costs minutes and stops the cause. b
  costs more than the one recorded case justifies.

### i2. A result is marked complete only by a check that it is

- **What it is:** a test that scans `experiments/phase2/src/` for a
  literal `"complete": True` (or `doc["complete"] = True`) with no refusal
  before it in the same function. The two functions fixed in Task P are
  its proven cases.
- **What it prevents:** a partial or wrong run recorded as complete.
  Sprint 31 found four places (class 2): `twins` and the Experiment 5
  alignment stop (fixed in 961e564), and F114 `--lr05` and `run_rbf`
  (open, D19 group c).
- **Long-term value:** "complete" is what the cards, the gate report and
  EvidenceBasedDB read. A false "complete" goes into reported results.
- **Prevention or control:** prevention at the source, checked by a test.
- **Extends:** `test_result_writer_required.py`.
- **Effort:** about 60 minutes. Two files.
- **Alternatives:**
  - **a. Backlog, built after D19 group (c) (the proposal).**
    - Pros: it arrives green, and each open place is fixed and proven
      first.
    - Cons: the gap stays open for one more sprint.
  - **b. Build it now, with a list of the two known open places as
    exceptions.**
    - Pros: it stops new cases at once.
    - Cons: 60 more minutes on a sprint already far over its target. An
      exception list must be emptied later, or it hides the gap.
  - **c. Put the check in `provenance.write_result`: it refuses
    `complete: True` unless the caller passes the result of its check.**
    - Pros: one place, and it prevents at write time for every module.
    - Cons: it changes every writer's call. About 120 minutes or more,
      across many modules.
- **Recommendation: a, backlog,** in the card with D19 group (c). Record
  c in the card as the design to compare when it is built.

### i3. The refusal gate sees the repository's refusal forms

- **What it is:** `scripts/refusal_coverage.py` also counts
  `print("REFUSING: ..."); return N` and a one-line `if bad: raise ...`
  as refusals. Each such line the branch changes gets a test in the same
  commit.
- **What it prevents:** an untested refusal in the commonest form in this
  repository passes CI (class 1; silent-failure finding 4). Today the gate
  sees only a line that starts with `raise`, or that has `sys.exit(` or
  `SystemExit(`.
- **Long-term value:** D16's gate then covers the class it was built for.
  Without it, a green gate means less than it seems to.
- **Prevention or control:** a control (a CI gate). Prevention is the
  per-term test rule. The gate catches what that rule misses.
- **Extends:** D16's `refusal_coverage.py`.
- **Effort:** about 60 minutes. The same work as D19 group (b).
- **Alternatives:**
  - **a. Backlog, with D19 group (a), as one card (the proposal).**
    - Pros: the gate and the missing proofs arrive together. Sprint 31
      stays as it is.
    - Cons: one more sprint with the gate partly blind.
  - **b. Do it now.**
    - Pros: the gate is complete this sprint.
    - Cons: 60 minutes. Every `REFUSING` line this branch changed needs a
      test in the same commit, which can grow the work.
  - **c. Change the `REFUSING` / `return N` form to `raise SystemExit`
    across the repository, so the current gate sees it.**
    - Pros: one refusal form, and a simpler gate.
    - Cons: it changes the exit path of many modules, and the tests that
      read their return codes. Much larger than a or b.
- **Recommendation: a, backlog.**

### i4. A sprint plan fits the time target, or says that it does not

- **What it is:** a line in the Phase 3 estimate step of
  `SPRINT_PLANNING.md`. Phase 3 states the plan's estimated total beside
  the 1-2 hour target. When the total is over, the scope is asked as a
  decision with a cut option.
- **What it prevents:** a sprint approved at many times the target when
  the team lead never saw the total. Sprint 31 planned 1,569 minutes and
  used 2,893 active minutes, against 60-120 (categories 1 and 3).
- **Long-term value:** sprints stay small enough to review and validate.
  An overrun becomes a choice made with the number in view.
- **Prevention or control:** prevention.
- **Extends:** the Phase 3 estimate step in `SPRINT_PLANNING.md`.
- **Effort:** about 10 minutes. One file.
- **Alternatives:**
  - **a. State the total, and ask a decision with a cut option when it is
    over (the proposal).**
    - Pros: 10 minutes. The team lead decides with the number.
    - Cons: the estimates themselves ran 1.69 times low, so the total
      understates. It needs i5.
  - **b. A hard cap: a plan never goes over 2 hours, and tasks over the
    cap go to the backlog.**
    - Pros: the strongest prevention.
    - Cons: research tasks with device blocks may not split. It removes
      the team lead's choice.
  - **c. A hook that blocks plan approval when the estimate total in
    `sprint_status.json` is over 120 minutes.**
    - Pros: enforced.
    - Cons: about 60 minutes. A hook on a judgment call.
- **Recommendation: a, now,** with i5.

### i5. Research estimates use more than one sprint's ratio

- **What it is:** a rule in the estimation step of `SPRINT_PLANNING.md`.
  A research estimate uses the median ratio (actual to estimate) of the
  last three sprints' measured research rows in `VELOCITY_LOG.md`, and
  the plan states the ratio.
- **What it prevents:** one sprint's ratio sets the next sprint's
  estimates. Sprint 30's ratios of 0.02-0.38 set this sprint's research
  estimates. E, F, J and K then ran 2.1 to 3.5 times over (category 3).
- **Long-term value:** estimates follow measured history, and i4's total
  becomes a number the team lead can trust.
- **Prevention or control:** prevention.
- **Extends:** the estimation rule in `SPRINT_PLANNING.md`.
- **Effort:** about 10 minutes. One file.
- **Alternatives:**
  - **a. The median of the last three sprints (the proposal).**
    - Pros: one unusual sprint does not move it.
    - Cons: it is slow to follow a real change, by up to two sprints.
  - **b. The mean of all research rows.**
    - Pros: the most data.
    - Cons: old sprints had a different mix of work, and outliers move a
      mean.
  - **c. A fixed multiplier from this sprint (1.69).**
    - Pros: the simplest.
    - Cons: it is the one-sprint problem that i5 exists to fix.
- **Recommendation: a, now.**

## Open items (the 2026-11-07 format, `SPRINT_RETROSPECTIVE.md` step 5)

The team lead asked for every open retrospective item in this format.
i2 is D21. i6 and i7 are D19's groups (a) and (c); group (b) is done
(i3, ca774e7). Answer: "i2. a i6. a i7. a", or "all as recommended".

### i2. A result is marked complete only by a check that it is

- **What it is:** a test that scans `experiments/phase2/src/` for a
  literal `complete: True` with no refusal earlier in the same function.
  The 13 places that do this today go on a list that can only shrink
  (`frozen_list.check`): f114 `main`, f157 `run` and `run_rbf`, f158
  `main`, f160 `main`, f166 `run`, f169 `main_lr05` and `main`, f170
  `main`, f171 budgets `main`, f171 missed `main`, f174 `run`,
  `run_dirac3s_units.dry_run`.
- **What it prevents and/or catches:** prevents, at development: a new
  module cannot record a partial or wrong run as complete without a check
  first. It catches nothing in the 13 listed places until they are
  reviewed.
- **Long-term value:** "complete" is what the cards, the gate report and
  EvidenceBasedDB read. A false "complete" goes into reported results.
- **Evidence:** 4 places in Sprint 31 (review class 2): `twins` could
  record a partial F95 card as complete, and Experiment 5 recorded a label
  mismatch as complete (both fixed in 961e564); F114 `--lr05` and
  `run_rbf` are still open. No recorded run was affected (the reviewers
  checked three). Time wasted: not measured; the two fixes were part of
  Task P.
- **Pros and cons:** Pro: automatic, and every new module is covered from
  its first commit. Con: a refusal earlier in the function is a proxy; a
  refusal about something else also passes.
- **Prevention or control:** prevention. **Extends:** the
  `test_result_writer_required.py` family and `frozen_list.check`.
  **Effort:** 45 minutes to 3 hours, by option.
- **Options for implementing:**
  - a. (Recommendation) Build it now, with the 13 places on the
    shrink-only list. About 45 minutes; a new test file and the
    regenerated test inventory. Pro: new cases stop now. Con: the 13 stay
    unchecked until reviewed.
  - b. Build it now and review all 13 now: each gets a check before it, or
    a stated reason it is complete by construction. About 3 hours. Pro:
    complete. Con: about 2 more hours on a sprint far over its target.
  - c. Backlog: card F196, priority 28, with this item's options b and c
    recorded. About 10 minutes now. Pro: no sprint time. Con: new modules
    stay unguarded until it is built.
  - d. Put the check in `provenance.write_result`: it refuses
    `complete: True` unless the caller passes its check's result, as card
    F196, priority 28. About 10 minutes now, 120 or more later. Pro: one
    place, prevention at write time. Con: every writer's call changes.
  - e. Skip for this sprint; track it in the retrospective, in case it
    recurs. Pro: no cost. Con: no protection.
  - f. Skip. Pro: no cost. Con: no protection, and no record.

### i6. Prove the Sprint 31 refusals red

- **What it is:** red proofs for the 13 Sprint 31 refusals and terms that
  have a test and no proof: six in `f157_spectra_docs.py`, four in
  `run_dirac3s_units.py` (the unreadable ledger, the unreadable balance,
  `--stop` missing, the intents term of `done`), two in
  `f157_spectra_algorithms.py`, and the `ci95[1] < 0` term in F114. First,
  two runner refusal tests move onto temporary paths with stubs (i1's
  rule), because a proof of either today would write into
  `experiments/phase2/results/` or open a device client.
- **What it prevents and/or catches:** catches, at testing: a refusal
  test that passes whether or not the refusal works. The prevention
  already exists (the per-term rule in Phase 4); this completes it for
  Sprint 31.
- **Long-term value:** each refusal's test is shown able to fail, so a
  later change that breaks the refusal turns CI red.
- **Evidence:** 37 untested refusals, terms and states reached review in
  Sprints 28-30. The PR 92 review found these 13 (test-coverage findings
  1, 5, 8, 9). CLAUDE.md records three vacuous guards in two earlier
  sprints. Time wasted: not measured.
- **Pros and cons:** Pro: closes a known gap with proofs, the repository's
  standard. Con: about 90 minutes, and proofs run slowly on this machine.
- **Prevention or control:** control (catches). **Extends:** the Phase 4
  per-term rule and `injection.Mutation`. **Effort:** about 90 minutes.
- **Options for implementing:**
  - a. (Recommendation) Backlog: card F194, priority 12, the top of
    Sprint 32. About 10 minutes now. Pro: done early next sprint, with no
    more time on this one. Con: the 13 stay unproven for one sprint.
  - b. Do it now, in Sprint 31. About 90 minutes. Pro: the gap closes
    before merge. Con: more time on a sprint far over its target.
  - c. Backlog at a lower priority: card F194, priority 28. Pro: it does
    not displace experiments. Con: it may wait several sprints.
  - d. Skip for this sprint; track it, in case it recurs. Pro: no cost.
    Con: the 13 stay unproven.
  - e. Skip. Pro: no cost. Con: no record.

### i7. Fix the latent set

- **What it is:** eight defects that no recorded run has hit. Experiment
  5 reads each score file from F174's outcome block and checks its hash;
  F114 `--lr05` refuses unless stage 1 is complete and passed; `run_rbf`
  refuses a dataset whose seeds differ from its plan;
  `provenance.start(replace=)` refuses `resumable=True`; `outcome_record`
  removes its temporary file when `os.link` fails; `f157_spectra_docs`
  writes `linear_paragraph` only for a kept RBF form and states a missing
  pocket figure; tests for Experiment 5's `edges()` and `accept()`
  refusals.
- **What it prevents and/or catches:** prevents, at development: a later
  run reading superseded scores, or recording a run as complete without
  its stage-1 or seed check.
- **Long-term value:** the next re-score or rerun cannot quietly produce
  a wrong record.
- **Evidence:** 0 occurrences in recorded runs. The reviewers checked
  three: no `_v2` score file exists, F169's stage 1 recorded a pass, and
  all four SPECTRA datasets keep the RBF form. Review classes 2 and 3.
  Time wasted: none yet.
- **Pros and cons:** Pro: removes defects before a run hits them. Con:
  about 120 minutes for defects with no occurrence yet.
- **Prevention or control:** prevention. **Extends:** each module's
  existing refusals. **Effort:** about 120 minutes.
- **Options for implementing:**
  - a. (Recommendation) Backlog: card F195, priority 28. About 10 minutes
    now. Pro: no sprint time; done before the next run of these modules.
    Con: latent for some sprints.
  - b. Backlog at the top: card F195, priority 12, beside i6. Pro: fixed
    early in Sprint 32. Con: it displaces experiment work.
  - c. Do it now, in Sprint 31. About 120 minutes. Pro: fixed before
    merge. Con: more time on a sprint far over its target.
  - d. Skip for this sprint; track it, in case one is hit. Pro: no cost.
    Con: a rerun can still record a wrong result.
  - e. Skip. Pro: no cost. Con: no record.

## Improvement Decisions

Team lead, 2026-11-07 (D20), verbatim: "i1. a i2. b i3. b i4. not
needed - skip i5. not needed. skip".

| # (i1-in) | Title | Alternative taken (a-z) | Effort | Decision (now/backlog/skip) |
|---|---|---|---|---|
| i1 | A refusal test stubs what the refusal protects | a | about 5 min | now (ca774e7) |
| i2 | A result is marked complete only by a check that it is | b | see D21 | now; 13 exceptions, not 2, so asked again as D21 |
| i3 | The refusal gate sees the repository's refusal forms | b | about 60 min | now (ca774e7); D19 group (b) |
| i4 | A sprint plan fits the time target, or says that it does not | none | none | skip |
| i5 | Research estimates use more than one sprint's ratio | none | none | skip |
