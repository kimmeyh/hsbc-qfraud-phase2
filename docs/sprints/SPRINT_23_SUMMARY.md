# Sprint 23 Summary: Restore the Repository as Filed

**Sprint**: 23 | **Date**: 2026-10-08
**Ran in**: the Phase 1 repository, `kimmeyh/hsbc-quantum-fraud-2026`. It was
the last sprint there.
**Branch**: `feature/20261007_Sprint_23`
**PR**: #167 in the Phase 1 repository, to `develop`, still DRAFT
**Issues**: #168-171 in the Phase 1 repository
**Cards**: F127 step (6), the steps that run in the Phase 1 repository
**Metered Dirac-3 seconds**: **0**. Balance 1,022 s throughout.

Sources: `SPRINT_23_RETROSPECTIVE.md`, `SPRINT_23_PLAN.md`,
`SPRINT_23_VALIDATION.md`, git history `6574d48..c3d9ec3`, PR #167. Written
in this repository at Sprint 24 Phase 3.2.1, as the Sprint 23 plan's
Deviations section states. The master plan is not a source.

## The objective, and where it stands

**Make the public Phase 1 repository show what was filed on 2026-09-12,
then hand it to the team lead to archive.** The proposal and appendix cite
its URL, so a reader who follows the link should find the filed tree.

**Half done, by design.** Tasks A and B are complete. Tasks C and D are
PENDING. Team lead decision D6: the restore commit waits until this
repository's Sprint 24 merges to `develop`. That merge is the first proof
that this repository's hooks, memory, pre-commit scan, CI and sprint process
work together in a real session.

## What was delivered

- **Task A (#168)**: the restore recipe, dry-run in a detached scratch
  worktree. It committed nothing. `git diff --cached --stat f35699c` named
  exactly the 7 approved paths. The three PDFs' SHA-256 equal the values in
  `docs/submission/PACKAGE.md`. All 260 ignored files stay ignored. The
  pre-commit scan blocked a planted match.
- **Task B**: the sprint record. Plan, validation file and retrospective,
  on this repository's `feature/20261007_Sprint_23` at `c3d9ec3`.
- **Manual Validation**: V1 (the restore changes exactly the approved
  paths) and V2 (what the restore takes away) approved by the team lead.
- **Decisions D1-D6**: D1 keeps the current `.gitignore` in the restored
  tree. D5 set the numbering rule: this repository's first sprint is the
  Phase 1 repository's last plus one, so it starts at 24. D6 holds Task C
  for this repository's Sprint 24 merge.

## What is pending

- **Task C**: the restore commit, built in a worktree, pushed by ID, then
  CI and `gh pr ready` on PR #167. Runs in the Phase 1 repository after this
  repository's Sprint 24 merges to `develop`.
- **Task D**: the `as-filed` tag on the Phase 1 repository's `main`, after
  the team lead's merges.
- **F127 step (7)**: the team lead archives the Phase 1 repository.

## What the pre-flight found

Four hazards, each found before any restore step ran, and each one would
have failed silently:

- **The as-filed `.gitignore` exposes private files.** At `f35699c` it does
  not ignore `docs/qci_package/` (18 files of private QCi correspondence).
  D1 keeps the current `.gitignore`.
- **The as-filed status file and hooks trip the old close-out hook.**
- **The pre-commit scan skips in a fresh worktree**, because its pattern
  file is gitignored. Carded here as F134.
- **The sprint branch was checked out**, so no worktree could take it. The
  restore commit is pushed by ID.

## Defects in this sprint's own work

- **D2 option 2 could not be executed as answered.** It said "this
  repository's sprint is renumbered" and gave no number, which cost a
  decision round (D5). Carded here as F135.
- **Task A's actual is an estimate of an actual.** No start time was
  recorded. Carded here as F136.
- **One status footer was typed instead of generated.** The Stop hook
  caught it.

## Improvements

The team lead sent all three to this repository's backlog (2026-10-08):
IMP-1 is F134 (the pre-commit hook blocks when its pattern file is missing),
IMP-2 is F135 (a decision option is complete enough to execute as answered),
IMP-3 is F136 (record each task's start time). All three are in Sprint 24's
selected scope.

## Effort

- Task A (F127 restore dry run): 20 minutes against 45 estimated. Judged at
  completion, not measured.
- Tasks C and D: not yet run.
- Planning and the pre-flight were not task-tracked and took most of the
  sprint.

## Next sprint readiness

This repository's Sprint 24 runs on `feature/20261008_Sprint_24`, cut from
the Sprint 23 branch at `c3d9ec3`. When it merges to `develop`, the Phase 1
repository's session checks this repository read-only and then runs Task C.
That session needs this repository's name, `kimmeyh/hsbc-qfraud-phase2`.
