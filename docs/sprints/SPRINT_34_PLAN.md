# Sprint 34 Plan: After Filing, the Filed Text Kept and First Tested

**Sprint**: 34 | **Branch**: `feature/20261118_Sprint_34`
**Planned**: 2026-11-21 | **Status**: APPROVED 2026-11-22 (team lead:
"Do all of these"; Q2 b8e2c0e as applied, D2 1, D3 1, D4 1). Draft PR #134.
Issues: A #135, B #136, C #137, D #138, E #139, F #140, G #141, H #142, I #143
**Scope** (team lead, 2026-11-21): F200, F201, F202, F178, F102, F198,
F197 and F157.
**Metered seconds**: 0. No task calls a device or a paid service.

## Objective

**The first sprint after the Phase 2 preregistration was submitted
(2026-11-18).** The team lead, verbatim: "It is possible that we will
be asked to update the pre-registration after receiving additional
information from the Quantum Insider team. We will want to preserve
what has been submitted so far and provide new document with updates
if we are asked to submit again."

- The submitted text is kept byte for byte (D2, D3), and every change
  after filing is dated and kept apart from it.
- The filing's first test runs: Experiment 3's release rule (F200).
- The filed reporting rule is made enforceable before any new score
  (F201).
- The work that follows from Experiment 3 and Experiment 5 is written
  as amendments and entries before any run (F198, F197).
- F157's remainder is split into cards with quoted costs (D4).

The filing venue is not known (Q1, team lead).

## Decisions already made (team lead, 2026-11-21)

- **Q1**: the venue is "not known yet".
- **D1**: none of options 1-4; the scope above was set directly.

## Answers (team lead, 2026-11-22)

- **Q2**: "the one I said I sent on 11/18/2026 9:01am EST". Applied as
  commit b8e2c0e, the last before 9:01. The current FINAL file (c3d3c00)
  has section 7 wording added at 9:18, so the sent bytes are kept as a
  third, locked copy and the tag points at b8e2c0e. Neither existing
  copy is edited. Details: `SPRINT_34_DECISIONS.md`.
- **D2**: option 1. **D3**: option 1. **D4**: option 1.

## Decisions asked with this plan

From `docs/sprints/SPRINT_34_DECISIONS.md`. The tasks below assume the
recommended answer; each other answer's effect is stated.

- **Q2**: which commit's text was submitted (c3d3c00, b8e2c0e,
  d96ad30, or not known).
- **D2**: where post-filing text goes. Recommended: option 1, the new
  file `experiments/phase2/PREREGISTRATION_AMENDMENTS.md`.
- **D3**: lock the filed text now, without the venue. Recommended:
  option 1.
- **D4**: which part of F157. Recommended: option 1, split only.

## Pre-kickoff (Phase 2)

- Sprint 33 merged to `develop` (PR #122, b1a86f8) and released to
  `main` (PR #133, fb5f2ca). No sprint issue is open.
- The branch was cut from the Sprint 33 branch and carries the
  refinement commit 648e11e (documents only). CI's full job is green on
  7bb54df. 648e11e has no CI run yet; the draft PR starts one.
- Dependency scan, 2026-11-21: `pip-audit` on the lock file
  (`--disable-pip --no-deps`, through `uvx`) finds no known
  vulnerability. No bump is proposed.

## Plan-to-branch-state verification (3.2.2.1)

Each card was checked against the repository on 2026-11-21. Probes
were read-only, zero metered, not evidence.

- **F200: confirmed.** `experiments/phase2/src/f188_rounding.py`
  (`delivered`, `run_delivered`) compares the rounded pick against
  greedy solved on the unrounded problem, the old rule.
  `f188_rounding_delivered.json` has six rows. At R = 200 the pick is
  greedy on 43/mid, 44/free and 44/mid.
- **F201: confirmed.** `outcome_record.py` has one
  `ALERT_BUDGET = 0.005`. `test_outcome_record_required.py` already
  exempts scored files from before its rule by a list that may only
  shrink. The 0.1% term uses the same form: the scored files at filing
  are listed, and any other scored file needs the 0.1% figures.
- **F202: confirmed.** `scripts/select_proofs.py` line 236 compares
  `args.base != "HEAD"` as a string.
- **F102: confirmed, one finding.** No `test_phase2_prereg_filed.py`
  exists. The hook guards `experiments/PREREGISTRATION.md` only. The
  only prereg tag is `prereg-freeze` (Phase 1). **Finding**: the FINAL
  file changed in three commits on 2026-11-18 (d96ad30, b8e2c0e,
  c3d3c00). The last added section 7 wording after the PR #122 review.
  Which one was sent is Q2.
- **F198: confirmed.** The ridge multiplier and R are inputs in
  `f188_rounding.py` (`RANGES`). The filed Experiment 3 entry says any
  other ridge weight or resolution "is a new dated amendment written
  before its run".
- **F197: confirmed.** `exp5_router.json` holds each seed's outcome
  block and the path and SHA-256 of its per-row test scores
  (`f174_lightgbm_<seed>.npz`). The saturation check can run from disk.
- **F157: confirmed.** The ULB and IEEE-CIS comparison pages exist;
  no QSVM or device-lane page. `dirac3_emulator.py` runs
  `QSVMClassifier` against a fitted cost model at zero metered seconds
  (D4 option 2 only).
- **F178: confirmed.** The documents are at versions 1.6, 1.5 and 1.5.

### Show each threshold can fire (Sprint 25 IMP-2, Sprint 28 IMP-5, Sprint 32 i3)

- **F200's rule** (gain > 1e-6 on at least one instance):
  - Reference where it must not fire: the three instances where the
    pick is greedy's selection. Under the new comparison their gain is
    0 by construction. Under the old comparison on disk it is not 0
    (between 1.6e-5 and 6.4e-5 in size). So a check that "gain is
    exactly 0 where pick is greedy" separates the two comparisons. It
    runs first, before the verdict.
  - Terms, each with its own test proven red: the threshold (a gain of
    exactly 1e-6 does not pass); "at least one instance" (one passing
    instance of six passes, none fails).
- **F201's term**: a scored file not on the filing list and without
  the 0.1% figures fails. A file on the list passes. A file with them
  passes. Each is proven red. Reference: every scored file on disk
  today is on the list, so the term is green at the start.
- **F202**: `--base @` on a dirty tree is not refused;
  `--base origin/develop` on a dirty tree still is. The existing red
  proof still fires.
- **F102's hash test**: an edited copy fails, one test per copy, each
  proven red. Not a source-scan guard. The hook gets one test per
  guarded path.
- **F198**: F188's coarse-R check (gain lost at a coarse R) fires
  first, as on its card.
- **F197's saturation check**: the champion's recall under the new
  measure is below 1.0 on each segment. Reference: the old measure,
  recall at 0.5% inside C, R and S, must show saturation on the same
  scores. If it does not, the check cannot tell the two measures apart,
  and the entry says so.
- **F157 and F178**: no rule. F178 has `test_learning_docs.py`'s
  existing checks.

## Tasks

| Task | Card | What | Est | Runtime | Depends on |
|---|---|---|---|---|---|
| A | F201 | `outcome_record.record` writes the confusion counts and recall at the 0.1% budget beside the 0.5% ones; `test_outcome_record_required.py` gains the term above, with the filing list; no result file rewritten | 45 | - | - |
| B | F202 | `select_proofs.py` compares `git rev-parse` of `--base` with HEAD's; a test for `@`; the existing proof kept | 15 | - | - |
| C | F102 (D2) | `experiments/phase2/PREREGISTRATION_AMENDMENTS.md`: its purpose, the rule (dated entries, each naming the filed section), and a first entry stating the departure from section 7's wording and why (D2); the drift guard checks that each entry has a date and a section | 15 | - | - |
| D | F102 (D3) | The lock: the sent text restored from b8e2c0e as `PREREGISTRATION_SUBMITTED_2026-11-18.md` (Q2); `test_phase2_prereg_filed.py` (SHA-256 of the three copies, a proof per copy); the hook extended to the three paths, with a test per path; the tag `phase2-prereg-filed` at b8e2c0e; the venue line stays "not set" in the locked text | 60 | - | C |
| E | F200 | A new option in `f188_rounding.py`: greedy's selection solved on the rounded problem and scored on the real one; the zero-gain check first; `f188_release_rule.json` with provenance; the verdict as a dated entry in the amendments file; F25's HOLD note in the master plan updated | 45 | about 1 minute (F188's six instances; the first is timed, cap 10) | A, D |
| F | F198 | The amendment first (multipliers 0.1, 1 and 10; R = 100, 200, 400, 800, 1,600), committed before the run; then the run; a short document | 30 | about 5 times F188's run (90 solves against 18); the first instance timed, cap 20 | E |
| G | F197 | A new Experiment 5 entry in the amendments file, every section 1 field filled, naming the measure; the saturation check on the recorded F121 scores; no run | 60 | under 1 minute (reads stored scores) | C |
| H | F157 (D4) | The split into cards, each with its estimate, metered-second quote (`qpu_cost_model.quote`) and entry needs; the F157 card updated | 45 | - | - |
| I | F178 | The per-sprint update: each document's next version and change list; F200's verdict, F201's rule and the filing's lock where the documents describe them | 45 | - | E, D |

**Derived total: 360 minutes of work**, the sum of the task estimates
(45 + 15 + 15 + 60 + 45 + 30 + 60 + 45 + 45). Each is its card's
estimate. C is new (D2). I is the middle of F178's 30-60 per sprint.
`[no-history]` cards: E, F and G. Sprint 33's rows understate their
actuals (`SPRINT_33_SUMMARY.md`, "Effort"), so no ratio is applied.
Phase 3, the reviews and the retrospective are not in these figures.

**The sprint is about 6 hours against the 1-2 hour target.** The team
lead set the scope. B, C, G and H do not depend on each other, so the
elapsed time is less than the sum.

**Effect of other answers.**
- D2 option 2 or 3: C writes the heading instead, about the same time.
- D3 option 2: D is removed (300 minutes). E's entry still goes where
  D2 puts it.
- D4 option 2: H becomes about 150 minutes, and runs after A (465).
  Option 3: H is removed (315).

### Task order

1. **A** (F201): before any scored result.
2. **B** (F202): small, and it removes a false refusal during the
   sprint.
3. **C**, then **D** (F102): the place for post-filing text, then the
   lock, before anything is written about the filing.
4. **E** (F200): the filing's first test.
5. **F** (F198): its amendment before its run, after E.
6. **G** (F197): the entry.
7. **H** (F157): the split.
8. Phase 5: the suite by risk, the plan's criteria walked, fresh-eyes
   review of E's and F's results before their write-ups.
9. **I** (F178), last, in parallel with the reviews.

## Risks

- **The submitted text is not known for certain (Q2).** If the answer
  is "not known", the lock is at c3d3c00 and the tag message says so.
  A later correction is a new tag, not an edit.
- **The Quantum Insider team may ask for changes.** The amendments
  file is then the source of the new document; nothing in the
  submitted text is edited (D2).
- **F200 may fail.** A fail is a valid result: F25 stays on HOLD and
  the PoC report says no design was found with room for a device to
  win (Experiment 3's entry). F198 then tests other settings under its
  own amendment, which cannot change F200's verdict.
- **Results seen before the amendment.** F198's and F197's text is
  committed before their runs; git records the order.
- **Sprint length.** About 6 hours of work. If time runs short, the
  team lead decides what moves (Class 3); nothing is dropped by
  inference.
- **CI is red until approval.** `test_phase3_artifacts.py` requires the
  issues and the approval once the status is `phase_3_planning`. That
  red is expected.

## Model assignments

Main loop (Opus, top tier) for all tasks. The suite runs in the
background, each run writing to a named file that is read in full when
it finishes.

## Definition of Done

- Every task's acceptance criteria are met.
- Each term above has its own test, proven red in the commit that adds
  it.
- CI's full job is green on the final HEAD.
- Manual Validation items are listed on screen and saved in
  `SPRINT_34_VALIDATION.md`.
- Retrospective, `SPRINT_34_SUMMARY.md` at Sprint 35 planning, and the
  master plan updated.
