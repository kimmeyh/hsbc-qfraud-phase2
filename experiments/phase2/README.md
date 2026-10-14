# experiments/phase2

Phase 2 code and evidence, kept apart from Phase 1's files
(`docs/PHASE_SEPARATION.md`, F123).

- `src/`: Phase 2 modules. They import shared code from `experiments/src/`.
  That code may change, with Phase 1 behavior kept as the default (CLAUDE.md,
  "The Phase 1 boundary inside THIS repository", 2026-10-14). The Phase 1
  record is the archived Phase 1 repository at tag `as-filed`. This replaces
  the earlier "never edit it; wrap" rule, which section 9 of
  `docs/PHASE_SEPARATION.md` dropped on 2026-10-07.
- `results/`: Phase 2 evidence, one JSON file per experiment, each carrying
  its generator, card, evidence tag and metered seconds (team lead decision
  D7, Sprint 22). Rows in the section-11 schema, in a Phase 2
  `results.json`, start with the first run under the Phase 2
  preregistration (F102) or the first device run, whichever comes first.
  `results/device_samples/` holds device responses recovered in full by job
  id.

Tests stay in `experiments/src/test_*.py`, where CI already runs them.

**History.** The team lead decided at Sprint 22 Manual Validation that Phase 2
moves to its own private repository (`docs/PHASE_SEPARATION.md` section 9,
card F127). That move is done: this repository is the Phase 2 repository, and
the Phase 1 repository is restored as filed and archived. New Phase 2 evidence
still goes to `results/` here, so it stays apart from Phase 1's
`experiments/results/`.
