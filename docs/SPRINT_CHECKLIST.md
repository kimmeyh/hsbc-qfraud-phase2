# Sprint Checklist (single page)

Consult at EVERY phase boundary (open this file in the same turn; walk lines with DONE/N-A/NOT-DONE + evidence). Full detail: SPRINT_EXECUTION_WORKFLOW.md.

## Phase 1: Backlog Refinement (mandatory, every sprint)
- [ ] Read ALL_SPRINTS_MASTER_PLAN.md + repo CHECKLIST-Phase2.md
- [ ] Read BACKLOG_REFINEMENT.md "Backlog Presentation Format" THIS TURN, then present candidates (Summary Index first, F# IDs, numeric priorities, HOLD one-liners)
- [ ] Record team-lead selection; update master plan; commit

## Phase 2: Pre-Kickoff
- [ ] Previous PR merged; previous sprint issues CLOSED (manual close; feature->develop does not auto-close)
- [ ] Working tree clean; develop pulled current; sprint branches never deleted
- [ ] `pytest experiments/src -q` green; dependency scan noted

## Phase 3: Kickoff & Planning
- [ ] Previous sprint SUMMARY doc created and linked in master plan (three-doc rule: PLAN + RETROSPECTIVE + SUMMARY, no exceptions)
- [ ] Card estimates and inter-card dependencies recorded FIRST; sprint total computed from them
- [ ] SPRINT_N_PLAN.md drafted: objective, tasks, quantifiable acceptance criteria, minute estimates taken from that computed total (never typed in and checked later)
- [ ] Plan verified against branch state (already-shipped work marked, stale paths corrected); re-estimated if findings
- [ ] Branch exists (usually via prior 6.6 carry-forward); DRAFT PR created/updated (STAYS DRAFT until 7.7)
- [ ] CI checked ~5 min after the draft PR exists (`scripts/check_ci_status.py --after 300`). If RED, hand the failure to a background agent and CONTINUE the sprint -- it does not block execution
- [ ] One GitHub issue per task (`sprint` label) BEFORE first task file is touched; all OPEN; each recorded with its task (`update_sprint_status.py --add-issue N --task X`, F173)
- [ ] Explicit team-lead approval obtained; PR body updated to approved plan

## Phase 4: Execution (auto-advance window: no permission-asking)
- [ ] Tasks in plan order; tests after each change; commits reference issue #N
- [ ] ACTUAL minutes recorded in `sprint_status.json` `task_actuals` as each task completes (not reconstructed at the retrospective): `update_sprint_status.py --start-task X --estimate MIN` when it begins (the plan's minutes; `--finish-task` flags an actual under a fifth of it, Sprint 30 IMP-3), `--finish-task X` when it ends, which records active minutes (gaps over 30 minutes with no tool call subtracted, from `.claude/activity.log`) and elapsed minutes in `task_elapsed` (F175). `--pause-task X` / `--resume-task X` around an approval wait; `--parallel` only when tasks truly run at once. A task added mid-sprint (including at Manual Validation) starts its timer with the tool before its first file; the status file is never written by hand or by a one-off script (Sprint 26 IMP-2). Such a task also gets its issue first (`gh issue create`, then `update_sprint_status.py --add-issue N --task X`): `.githooks/commit-msg` refuses a `feat:` or `fix:` commit on a sprint branch that names neither an issue from `github_issues` nor `PR <n> review` (Sprint 28 IMP-4), and one whose task is not being timed: the named issue's task from `task_issues`, or for `PR <n> review` the task set with `--review-task X` (F173, Sprint 30)
- [ ] A commit that adds a compound decision rule carries one test per term in which only that term fails, each proven red, in THAT commit, not later (`SPRINT_PLANNING.md`, Sprint 28 IMP-5, moved to Phase 4 by Sprint 29 IMP-1). A refusal (each condition that raises or refuses) and each state a report or status tool prints is a term too: one test per refusal and per state, each proven red (Sprint 30 IMP-2; the PR 74 review found 9 such branches untested). The commit-msg hook also refuses a `feat:` or `fix:` commit when no task timer is running (Sprint 29 IMP-4)
- [ ] A test of a refusal replaces the action the refusal blocks (a run, a write, a device client) with a stub that fails at once, so its red proof, which removes the refusal, cannot start that action (Sprint 31 i1: a `--tests` proof started nested test runs for 83 minutes; two runner refusal tests run against real paths)
- [ ] `git status --short` before every staging; every entry accounted for; 0* files committed neutrally, never read
- [ ] Results only via frozen protocol; every metric -> results.json with evidence tag
- [ ] HARDWARE: any metered run stops for approval (Criterion H), always

## Phase 5: Review & Validation
- [ ] **Suite green, by risk (F177, Sprint 31 D8; D17 option 1).** Two runs, each output to a file and its summary read there, never piped to a tail, so a failing test's name is kept (Sprint 30 IMP-4, `TROUBLESHOOTING.md`):
  - **Every non-proof test and the selected proofs, on CI**: `gh workflow run ci.yml --ref <branch>` starts CI's full job; `scripts/check_ci_status.py --wait --require-job full` reads it. The full job runs every non-proof test, then `scripts/select_proofs.py --sample --run`: the red proofs of each test file whose test or named file changed against `origin/develop`, plus this sprint's rotating sample of one proof file in 20. A proof tests its test, so it shows nothing new unless its files changed.
  - **The changed files' tests, locally**: during a task, `scripts/select_proofs.py --tests --base HEAD` runs the non-proof tests of the uncommitted changes, of the files that name them, of the tests that name a changed folder two or more levels deep, and the repository guards (30 files in 4 minutes 46 seconds for one Sprint 31 change). At Phase 5 the branch's change set is the whole sprint (99 of 163 files on Sprint 31), so the Phase 5 local run is the parallel one: `pytest experiments/src -m "not proof and not serial" -n auto --dist loadfile -q -rf`, then `pytest experiments/src -m "serial and not proof" -q -rf` (`SERIAL_FILES` in the root `conftest.py`). A red proof is run locally only to prove a new or changed guard (`assert_can_fail`), never under xdist.
  - Before a long run, `scripts/env_check.py` prints this machine's start-up times beside the 2026-11-05 values (f); a SLOW line explains a slow run before it starts.
- [ ] No unamended drift from prereg-freeze in analysis code
- [ ] Plan acceptance criteria walked line by line WITH EVIDENCE
- [ ] Check: every compound decision rule, refusal and reported state added this sprint got its per-term tests, each proven red, in the commit that added it (Phase 4 item; a rule found here without them is a Phase 4 miss, recorded for the retrospective)
- [ ] OUTWARD documents pass `scripts/outward_readability.py` BEFORE handover (IMP-5: the QCi package needed a revision round purely to strip tokens a vendor reader cannot resolve, after the team lead had already reviewed it)
- [ ] **Learning documents updated (F178)**, in parallel with the full suite and the PR reviews, before the validation items are listed: each of the three documents in `docs/learning/` gets the next version number and a dated change-list entry that says, in a sentence or a paragraph at that document's reader level, what each piece of work did and what it found or changed, with the card number and sprint given beside that text for cross-reference, never in place of it (team lead, 2026-11-23, Sprint 34 Q4); each result this sprint produced goes in under its topic's "What our experiments showed" as a tagged claim ending with its tracked source path, our evidence before outside research, and replaces its placeholder in "Experiments planned"; the next sprint's preregistered runs are added there with placeholders; a new acronym goes only in the plain-terms version's acronym appendix, a new term in the first version that needs it; each outside claim names an EvidenceBasedDB id with its grade, checked by `scripts/edb_query.py show <id>`. `experiments/src/test_learning_docs.py` (links, acronyms, terms, claim paths and figures) is green before handover; it also runs in the full suite.
- [ ] **The validation items are LISTED TO THE SCREEN as the last step before handover** (team lead, 2026-10-03). Writing them to a file and pointing at the file is not the handover; it is the same referring-back failure in another form. The file is the durable copy, the screen list is the handover. **The list holds only the team lead's actions** (judge a document, confirm a change, answer a decision, run a check only that machine can run), each naming any file to open by its full absolute path; results, analysis and fixed defects go in a separate "for information" section (team lead, 2026-11-06, Sprint 31: 11 of 13 items were results, not actions)
- [ ] Handed to team lead for manual validation (questions correct from here)

## Phase 6: Push & Finalize PR
- [ ] Branch pushed; existing draft PR body updated (still DRAFT); interim status given, not "ready"
- [ ] **Reviews on the DRAFT PR** (team lead, 2026-10-23, Sprint 28 DV5): Copilot (GraphQL request, verified on the timeline) and pr-review-toolkit, the invocation naming the excluded evidence files. The PR stays draft. While they run, the team lead's retrospective feedback is collected (retrospective step 1)
- [ ] Every finding fixed, prevention first (the guard or gate before the patch), each thread answered and resolved
- [ ] ON MERGE NOTIFICATION: next sprint branch created FROM CURRENT FEATURE BRANCH immediately; post-merge work committed there; never stash; never branch from develop post-merge

## Phase 7: Retrospective (before ready)
- [ ] 7-step protocol run in order (SPRINT_RETROSPECTIVE.md); 16 categories x 4 roles, verbatim, no placeholders; the review findings are an input
- [ ] Every RECURRING finding class has an improvement (card acceptance criterion, Phase 5 gate, test or hook); single findings have a root cause recorded
- [ ] Improvements, questions and decisions proposed in the retrospective format (numbered i1-in with a title; what it is, what it prevents and/or catches and at which stage, long-term value, evidence, pros and cons, options lettered a-z with timing and effort, one marked Recommendation; answered "i1. a" or "all as recommended"; `SPRINT_RETROSPECTIVE.md` step 5 and its checklist) + dispositioned; now-items committed; backlog-items -> master plan with F#s
- [ ] **At the push of the improvement commits, start the short review and CI's full job together (F177 change e)**: `gh workflow run ci.yml --ref <branch>` and the review agent in the same step, so neither waits on the other; the review's time cap holds, and the full job's result is read at 7.0.
- [ ] ONE short review of the improvement commits only; its trivial findings fixed, the rest to the next sprint's Phase 1 refinement (no second round). "Short" is a time cap: the brief states about 10 minutes, the diff only, no test runs and no live GitHub calls (the full suite and CI's full job carry the tests; Sprint 30's ran 14 minutes on a brief with none of these limits)
- [ ] Completion updates: master plan Last Completed Sprint; CHECKLIST-Phase2.md reconciled; sprint_status updated
- [ ] CI checked on the final HEAD (`scripts/check_ci_status.py`, no waiting). If it is still running or RED, arm the watcher and hand the result to an agent; the close-out hook blocks the completion claim until it is green
- [ ] `gh pr ready` (ONLY here); final gate; team lead notified for approval
- [ ] After `gh pr ready`: `scripts/check_ci_status.py --wait --require-job full`. Ready for review starts CI's full job, the only CI run of the red proofs, selected and sampled (Sprint 30 Task L; Sprint 31 D17); without `--require-job` the earlier green push run reads as a pass before the full job is listed (PR 74 review). The completion claim waits for it to be green

## Phase 8: Delivery Cycle (after develop merge)
- [ ] Team lead merges develop->main (parallel; do not block on it)
- [ ] Refinement Pass 1 completeness sweep (issues, docs triad, master plan, pruning) -- corrections only
- [ ] Submission-artifact refresh if due (QCi letter numbers, requirements matrix, paper vs results.json)
- [ ] Refinement Pass 2 scope selection -> Phase 3
