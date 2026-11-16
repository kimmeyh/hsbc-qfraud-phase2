# Sprint 33 Plan: The Phase 2 Preregistration, Ready to File

**Sprint**: 33 | **Branch**: `feature/20261116_Sprint_33`
**Planned**: 2026-11-16 | **Status**: APPROVED 2026-11-16 (as amended: Task D added at planning). Draft PR #122.
Issues: A #123, B #124, D #125, C #126
**Scope**: F13, F102 (resized, with F199's coverage check) and the F178
update; F199 deferred (team lead, 2026-11-16, D3 option 2).
**Metered seconds**: 0. No task calls a device or a paid service.

## Objective

**Sprint goal (team lead, 2026-11-16): "have the Phase 2 registration
document ready to submit."** The document is
`experiments/phase2/PREREGISTRATION_DRAFT.md` (card F102).

- "Ready to submit" here means: every committed experiment has a current
  entry with a stated state, every assumption the filing rests on is
  written down, section 7 holds nothing open but the filing date and
  venue, and a test fails if any of that drifts. Filing itself (the date,
  the venue, freezing the file) is the team lead's step, later.
- **The brief is not available** (team lead, Q1: "we are going to have to
  file without the brief. Make assumptions as best possible"). Every
  missing fact becomes a labeled assumption.
- **The filing venue and date stay blank and changeable** (Q2: "don't
  know yet. leave blank and changable until notified otherwise").
- **Section 6 separates entries already run from entries to run** (Q3:
  "yes").
- **Assumptions first** (F13), because they set what the preregistration
  can say; then the preregistration (F102); then the learning documents
  (F178).

## Decisions already made (team lead, 2026-11-16)

- **D1 and D2** superseded by the team lead's proposed scope (noted in
  `SPRINT_33_DECISIONS.md`).
- **D3: option 2.** F102 resized with F199's coverage check, F13, the
  F178 update. F199 deferred. With Q1-Q3 answered as above, F13 runs on
  stated best-possible assumptions in place of the brief.
- **Added at planning (team lead, 2026-11-16)**, verbatim: "Add gaurding
  the draft of the preregistration so that it does not drift in the
  future. However, this is a draft that will go through a couple of
  reviews before submitting later today." This is Task D. The guard checks
  that the draft stays consistent with itself and with the repository;
  it does not lock its bytes, so the reviews can change it. The lock is
  a filing step (section 7). "Submitting later today" sets the order:
  the submission path (A, B, D, the reviews) runs first, and C (F178)
  last, so it cannot delay the submission.

## Pre-kickoff (Phase 2)

- Sprint 32 merged to `develop` (PR #116) and released to `main` (PR
  #121). No sprint issue is open. The branch is cut from the Sprint 32
  branch and carries the refinement commit c33fc03.
- CI's full job, red proofs included, is green on e4e61c3, the code this
  branch carries; the commits since change documents only. The changed
  files' tests passed on c33fc03 (the run recorded for the pre-push
  hook). The local non-proof suite runs in the background; its result is
  in its output file, not restated here.
- Dependency scan, 2026-11-16: `pip-audit` on the lock file
  (`--disable-pip --no-deps`, through `uvx`) finds no known
  vulnerability. No bump is proposed.

## Plan-to-branch-state verification (3.2.2.1)

Each card was checked against the repository on 2026-11-16. Probes were
read-only, zero metered, not evidence.

- **F13: confirmed.** `docs/phase2/PHASE2_POC_PLAN_DRAFT.md` holds the
  assumption register [A1]-[A8] and the stage plan; the skeleton
  `PHASE2_POC_PLAN.md` holds the calendar. The draft predates Sprint 32's
  results (F188, F185, D4). PoC week 1 starts
  2026-11-17 (roadmap page), so the draft's "before notification" items
  are now due.
- **F102: confirmed, three findings.**
  - Section 6's status table is headed "Status on 2026-10-23" and has no
    column saying whether an entry has been run. Its rows give the
    written date only.
  - Section 7's entry item is stale: it says Experiments 2-6 wait on
    their cards, while section 6 has an entry for each of the six.
  - `scripts/outward_readability.py` flags 506 tokens a reader outside
    this repository cannot resolve, nearly all card IDs (F112) and
    sprint numbers (Sprint 31). A rewrite of 2,360 lines does not fit
    the sprint. The task adds a section that tells the reader where
    these identifiers resolve, under a labeled assumption that the
    reader can open this repository; the tool is then run with the two
    token classes allowed, and every other hit fixed or listed.
  - No test reads the draft's structure today, so the drift above was
    not caught.
- **F199: deferred.** Its coverage check (each of the six filed
  commitments has a current entry) is part of F102's test.
- **F178: confirmed.** The three documents are at version 1.3 in
  `docs/learning/`; `test_learning_docs.py` checks them.

### Show each threshold can fire (Sprint 25 IMP-2, Sprint 28 IMP-5, Sprint 32 i3)

- **F102's readiness and drift guard (Task D)**, one test per term, each proven red:
  - an experiment of the six with no row, or no entry, fails;
  - a row whose state is not one of the stated values fails;
  - a table row with no entry heading, or an entry heading with no row,
    fails;
  - a header without the filing-date and filing-venue fields fails
    (blank is allowed and must say "not set");
  - a section 7 item still open, other than the filing date and venue,
    fails.
  - Not a source-scan guard, so i3's list of forms does not apply.
- **F13.** No rule; acceptance is checked by reading.
- **F178.** `test_learning_docs.py`'s existing checks.

## Tasks

| Task | Card | What | Est | Runtime | Depends on |
|---|---|---|---|---|---|
| A | F13 | `PHASE2_POC_PLAN_DRAFT.md` updated for a filing without the brief: each assumption [A1]-[A8] restated as the best available, with its source and what would change it; new assumptions for what the filing needs and the brief would have set (the filing venue and date, blank and changeable; whether the team proceeds to the PoC); Sprint 32's results placed where they bear (Experiment 3 after F188 and D4); a dated revision note | 75 | - | - |
| B | F102 | `PREREGISTRATION_DRAFT.md` ready to file: a filing header (date and venue "not set", changeable; the assumptions cited from A); section 6's table gains a state column separating "run before filing, result in <document>" from "to run in the PoC" (Q3), and each of the six entries is checked against its latest result; section 7 closed except the filing date and venue; a section on where the identifiers resolve; `outward_readability.py` run, every hit outside the two allowed classes fixed or listed; a revision-log row (the readiness test is in D) | 120 | - | A |
| C | F178 | The per-sprint update: each document's next version and change list; the preregistration's readiness and the PoC assumptions where the documents describe the plan | 45 | - | B, D and the reviews |
| D | F102 | The drift guard (team lead, added at planning): a test file that keeps the draft consistent while reviews change it, not a byte lock. B's readiness terms move here, plus: each "run" row's result document exists and is tracked; each assumption the header cites exists in the PoC plan's register; a commit that changes the draft adds a revision-log row dated that day or later; the draft's decimal figures resolve to tracked result files, by the same rule as `test_phase2_figures_resolve.py` (if more than 20 do not resolve, they are listed and the figure term becomes a card, not this sprint's work). One test per term, each proven red. The draft-time readiness terms stay valid after filing; the byte lock is added at filing | 60 | - | B |

**Derived total: 300 minutes of work**, the sum of the task estimates
(75 + 120 + 45 + 60). D's 60 is `[no-history]`; B keeps its 120 with its
test moved to D. F13's 75 is its card estimate. F102's 120 is the
resized estimate in D3 (the card's 180 is from 2026-10-13, when the draft
was new). F178's 45 is the middle of its card's 30-60 per sprint.
Sprint 32's actuals are understated in five of ten rows, so no ratio is
applied. Phase 3, the reviews and the retrospective are not in these
figures. The sprint is past the 1-2 hour target; the team lead chose it
(D3).

How each estimate was set (`docs/VELOCITY_LOG.md`): all three cards are
`[no-history]` or per-sprint; no allowance added.

### Task order

1. **A** (F13): the assumptions, before anything cites them.
2. **B** (F102): the preregistration, citing A.
3. **D** (F102): the drift guard, on B's result.
4. Phase 5: the suite by risk, the plan's criteria walked, fresh-eyes
   fixes. The team lead's reviews of the draft follow; the guard runs on
   every change they bring.
5. **C** (F178), last, so it cannot delay the submission.

## Risks

- **Assumptions in place of the brief.** The brief may set data,
  metrics, confidentiality or dates that differ. Each assumption names
  what would change it, and the document stays changeable until filed.
- **The venue is unknown.** If the reader cannot open this repository,
  the identifiers section does not resolve the card IDs; a rewrite for
  that reader would be a new card once the venue is known.
- **Entries already run.** Their value as preregistration rests on git
  showing each entry was written before its run. The state column names
  the result document; it restates no figure, so no number in the
  draft can drift from its owner.
- **The frozen-file guard is not added this sprint.** Phase 1's
  preregistration is locked by a hook and a hash test. That lock belongs
  to the filing commit, when the date and venue are known; section 7
  lists it as a filing step.
- **CI is red until approval.** `test_phase3_artifacts.py` requires the
  issues and the approval once the status is `phase_3_planning`. That
  red is expected.

## Model assignments

Main loop (Opus, top tier) for all tasks. The suite runs in the
background, each run writing to a named file that is read in full when
it finishes.

## Definition of Done

- Every task's acceptance criteria are met.
- Each term of the readiness test has its own test, proven red in the
  commit that adds it.
- CI's full job is green on the final HEAD.
- Manual Validation items are listed on screen and saved in
  `SPRINT_33_VALIDATION.md`.
- Retrospective, `SPRINT_33_SUMMARY.md` at Sprint 34 planning, and the
  master plan updated.
