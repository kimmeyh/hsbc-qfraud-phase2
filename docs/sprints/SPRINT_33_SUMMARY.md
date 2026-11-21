# Sprint 33 Summary: The Phase 2 Preregistration, Ready to File

**Sprint**: 33 | **Dates**: 2026-11-16 to 2026-11-18
**Branch**: `feature/20261116_Sprint_33`
**PR**: #122 to `develop`, merged 2026-11-18. Released to `main` by PR #133.
**Issues**: #123-#132 (Tasks A-J)
**Cards**: F13, F102 and the F178 update
**Metered seconds**: **0**. No task called a device or a paid service.

Sources: `SPRINT_33_PLAN.md`, `SPRINT_33_VALIDATION.md`,
`SPRINT_33_DECISIONS.md`, `SPRINT_33_RETROSPECTIVE.md`, git history
`66d965e..7bb54df`, PR #122. Written at Sprint 34 refinement, before
planning (3.2.1). The master plan is not a source.

## The objective, and where it stands

**The Phase 2 registration document ready to submit** (team lead's
goal). Done. The preregistration was marked FINAL and submitted for
filing on 2026-11-18. It is copied byte for byte to
`experiments/phase2/PREREGISTRATION_FINAL.md`. Two steps of its section
7 are open: the filing venue, and the lock step that follows it. The
team lead moved both, with Experiment 3's release rule, to Sprint 34.

## What was delivered

- **Task A (F13, #123)**: `docs/phase2/PHASE2_POC_PLAN_DRAFT.md`
  restated for a filing without the brief. Assumptions A1-A12, each
  with its basis and what replaces it.
- **Task B (F102, #124)**: the draft ready to file. A Filing section,
  an identifiers section, section 6's State and Result columns, and
  section 7 closed except the filing steps.
- **Task D (F102, #125)**: the drift guard,
  `experiments/src/test_phase2_prereg_draft.py`. A consistency guard,
  not a byte lock; each term proven red.
- **Task E (#127)**: the fresh-eyes review fixes.
- **Task C (F178, #126)**: the learning documents' per-sprint update.
- **Task F (#128)**: an outside adversarial review applied (D5, D6).
  D6 fixed Experiment 3's device release rule.
- **Task G (#129)**: the D9 claim audit applied. Seven read-only
  reviews checked every sentence with a figure, verdict or citation.
- **Task H (#130)**: D10-D12 applied. The preregistration marked FINAL.
  The learning documents give D6's rule.
- **Task I (#131)**: the PR 122 review fixes. The guard gained an
  eleventh term: the FINAL copy matches the draft.
- **Task J (#132)**: retrospective i2 and i3. The pre-push gate refuses
  a dirty tree at once; a CLAUDE.md rule on searches.

## What the reviews found

- **PR #122**: Copilot (four comments) and the pr-review-toolkit agents
  (two Important findings, three Suggestions). All fixed in Task I
  except two small guard gaps, which the team lead skipped (i4).
  Classes: a check that matches more than it should (recurring; i1,
  tracked only); a claim with no check behind it (single; fixed).
- **Improvement commits**: one short review, no finding at its bar. One
  low note: `--base @` is refused on a dirty tree although
  `--base HEAD` is not. Carried to Sprint 34 refinement.
- **CI**: green on 7bb54df, the full job included.

## Decisions

- **At planning**: D3 (option 2: file without the brief, on stated
  assumptions; the venue and date blank until notified). D1 and D2 were
  replaced by D3's questions.
- **At Manual Validation**: D4 (three learning documents stay); D5 and
  D6 (the adversarial review applied; Experiment 3's release rule);
  D7 (the repository stays public, the QCi correspondence stays
  private and gitignored); D8 (the QCi letters in the history
  stay); D9 (a second review by several agents); D10 (recall at the
  0.1% budget reported from filing on); D11 (a hash test of the filed
  text at filing); D12 (the release rule computed after filing).
- **At the retrospective**: "i1. e i2. a i3. a i4. f i5. f". i2 and i3
  applied (Task J); i1 tracked; i4 and i5 skipped.

## Effort

The ten timed tasks were estimated at 610 minutes; their recorded active
minutes total 154. That figure understates the work: Tasks A to E
started their timers after most edits, and background agent work is not
timed (i5, skipped). Rows are in `docs/VELOCITY_LOG.md`.

## Next sprint readiness

Sprint 34 runs on `feature/20261118_Sprint_34`, cut from this sprint's
branch. Carried by the team lead's decision: the filing venue and the
lock step (F102), Experiment 3's release rule (D12), and the 0.1% budget
in the outcome block (D10).
