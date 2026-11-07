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

- **IMP-1. A refusal test stubs what the refusal protects.**
  Source: class 4; the `--tests` proof ran nested test runs from 16:29 to
  17:52, and test-coverage finding 2 (two runner refusal tests run
  against real paths). Type: test rule. Prevention: a Phase 4 checklist
  line, "a test of a refusal replaces the action the refusal blocks
  (a run, a write, a client) with a stub that fails at once", so its red
  proof cannot start the action. Extends: the Phase 4 per-term item.
  Effort: about 5 minutes. Recommendation: now.
- **IMP-2. A result is marked complete only by a check that it is.**
  Source: class 2, four places this sprint. Type: guard. Prevention: a
  test that scans `experiments/phase2/src/` for a literal
  `"complete": True` (or `doc["complete"] = True`) not preceded in its
  function by a refusal, with the two fixed functions as its proven
  cases. Extends: `test_result_writer_required.py`. Effort: about 60
  minutes. Recommendation: backlog (it needs the deferred set fixed first,
  or it is red on arrival).
- **IMP-3. The refusal gate sees the repository's refusal forms.**
  Source: class 1; silent-failure finding 4. Type: gate. Prevention: as
  the deferred item above. Extends: D16's `refusal_coverage.py`. Effort:
  about 60 minutes. Recommendation: backlog, with the deferred proofs.
- **IMP-4. A sprint plan fits the sprint time target, or says it does
  not.** Source: category 3 (Poor) and category 1: 2,893 active minutes
  against the 1-2 hour target, from twelve tasks. Type: planning rule.
  Prevention: Phase 3 states the plan's derived total beside the 1-2
  hour target and, when it exceeds it, asks the scope as a decision with
  a cut option. Extends: the Phase 3 estimate step in
  `SPRINT_PLANNING.md`. Effort: about 10 minutes. Recommendation: now.
- **IMP-5. Research estimates use more than one sprint's ratio.**
  Source: category 3; Sprint 30's 0.02-0.38 set this sprint's research
  estimates, and E, F, J and K ran 2.1 to 3.5 times over. Type: planning
  rule. Prevention: a research estimate uses the median ratio of the
  last three sprints' measured research rows in `VELOCITY_LOG.md`, and
  states it. Extends: the estimation rule in `SPRINT_PLANNING.md`.
  Effort: about 10 minutes. Recommendation: now.

## Improvement Decisions

Awaiting the team lead (step 6).
