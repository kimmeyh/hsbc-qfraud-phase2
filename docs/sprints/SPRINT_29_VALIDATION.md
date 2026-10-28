# Sprint 29 Manual Validation

**Sprint**: 29, Make the Tools Repeatable, Then Find the Best Each Model Can Do
**Branch**: `feature/20261025_Sprint_29` | **PR**: #63 (draft)
**Scope**: F165 (A), F159 (B), F164 (C), F156 (D), F160 (E), F166 (F),
F158 (G), F167 (H), pypdf (I). Issues #64-72, all closed.
**Metered seconds**: 0. No Dirac, Braket or other paid service was called.

This file is the durable copy. The same items are listed to the screen at
handover: a pointer to a file is not a handover.

---

## V1. Task A (F165): a resumed run keeps its own id

- `provenance.run_id_for(path)` writes the id to a gitignored
  `<result>.run_id` sidecar; `run_id_for(path, resume=True)` reads it
  back. `write_result` refuses an id copied out of a recorded result.
- Used for real this sprint: F159 resumed twice under one id.
- Check: the provenance bullet in `CLAUDE.md` names the resume path.

## V2. Task B (F159): the parallel pool build

Card Done line in `docs/ALL_SPRINTS_MASTER_PLAN.md`; result
`experiments/phase2/results/f159_parallel_pool.json`.

- Every parallel pool equals the serial pool on the validation rows, at
  all four row fractions and all five worker counts.
- Full ULB rows: serial 730.3 s; 32 workers 45.8 s; 16 workers 11.24
  times faster than serial. The longest single learner took 2.0 s, so
  process start-up and copying the rows limit the speed-up, not the
  learners.
- **Finding to confirm**: the first run stopped with a `MemoryError` at
  32 workers on the 0.5 fraction; its resume then hung for 9 hours
  (12:10am to 8:58am). One worker's log shows a `MemoryError` at start-up;
  that the pool then waited on the dead worker is inferred, not shown. The cause of the `MemoryError` is **unverified**: the
  machine's commit limit is 99.7 GB, so "out of memory" is not shown.
  Two fixes (`e02fa18`, `94f079e`): a failed build is recorded, not
  fatal, and each parallel build is stopped after 2 times its fraction's
  serial time. On the final resume the 32-worker build finished in 24.5 s.
- F166 used the 32-worker build for its proxy lane.

## V3. Task C (F164): figures in docs/phase2 resolve to evidence

`experiments/src/test_phase2_figures_resolve.py` and
`experiments/src/phase2_figure_registry.py`.

- Each figure resolves only against the result files its own document
  names. 0.829 put back fails; proven red.
- **Two documents corrected; please confirm each:**
  - `docs/phase2/F108_CEILING_VALIDATION.md`: three plug-in ratios read
    1.105, 1.114 and 1.118; recomputed from the rows they are 1.106,
    1.116 and 1.119. The noise row's range read 1.075-1.098; it is
    1.076-1.097. The pass counts do not change.
  - `docs/phase2/F162_IN_POCKET.md`: "Recorded wall time 28.5 minutes"
    now says the wall time is **unverified** (the result file does not
    record it); the rows' lane time sums to 20.5 minutes.
- The other six PR #46 findings are prose or integers, out of a figure
  check's reach (named in the test's docstring).

## V4. Task D (F156): the Henze-Penrose bound fails

Card Done line; results `f156_hp_bound_pilot.json` and `f156_hp_bound.json`.

- On the main arm the interval contained the true Bayes error on 2 of 5
  seeds and was narrow on 0 of 5; the rule needs 4 of 5. The entry had
  shown before the run that both terms cannot hold together here.
- Where it missed, the lower end sat just above the true value.
- **F114 stays blocked.** A decision on the next estimator is below (D1).

## V5. Task E (F160): Experiment 3's room check passes on IEEE-CIS

Card Done line; result `f160_room_ieee.json`. F25's card records the
reopened design.

- The positive control passed first. On IEEE-CIS (seeds 42-44, 60 and 136
  variables), greedy ends 0.096-0.099 above the floor on every instance,
  against the 0.01 rule; F104's resolution gate passes. The guide-based
  resolution check fails on every instance, as it does on the control;
  the falsifier needs both checks to fail, so it does not fire.
- **Caveat**: SCIP stopped at its 300 s cap on every instance without
  beating greedy. Its dual bound puts the true optimum between greedy and
  about 0.08-0.18 below it. No solver has yet been shown to beat greedy.
- F25's HOLD reason (F102 not filed) stands.

## V6. Task F (F166): best achievable result per algorithm on ULB

Read `docs/phase2/algorithms/ULB_COMPARISON.md`, then any of the seven
algorithm documents beside it.

- Seeds 42-51 (seed 42 took 11.48 minutes, so the entry's rule gave 10).
- Mean test AUPRC: CatBoost 0.8329, LightGBM 0.8270, XGBoost 0.8229,
  HGB 0.8124, CVQBoost proxy 0.7925, linear SVM 0.7419, logistic
  regression 0.7270.
- Reliable adjacent differences (Wilcoxon, Bonferroni 0.05 / 6): the
  proxy above the SVM, and the SVM above logistic regression. The order
  among the four boosting libraries and the proxy is not established.
- The RBF SVM alternative was dropped: better on validation on 2 of 10
  seeds.

## V7. Task G (F158): fraud types

Card Done line; result `f158_fraud_types.json`.

- Step 1 (simulator, seeds 42-49): recall at the 0.5% budget, cascade
  minus single model, mean -0.069, 95% interval -0.126 to -0.013: the
  cascade is **below** one model. The shuffled-type reference was also
  below, by less.
- Step 2 did not run (its condition is a cascade above).
- Step 3: 106 of 950 ULB test frauds were missed by all twelve stored
  model families; on V1-V8 they sit near zero, where the caught frauds
  do not.
- Added at Phase 5: one test per term of step 2's two-term condition,
  each proven red.

## V8. Task H (F167): the PoC plan draft

Read `docs/phase2/PHASE2_POC_PLAN_DRAFT.md`.

- Written for you. `scripts/outward_readability.py` finds 31 internal
  tokens (card IDs and similar). If it goes to QCi, it needs that pass
  first.

## V9. Task I: pypdf 6.21.2

- Lock and venv at 6.21.2 with a dated header line naming
  CVE-2026-115572, CVE-2026-115585 and CVE-2026-115580. pip-audit: three
  findings on 6.21.1, none on 6.21.2. The PDF tests ran before and after.
- Only the Windows venv exists on this machine; the plan said "both
  venvs". A second venv elsewhere still needs the upgrade.
- PyPI now lists pypdf 6.21.3; the approved 6.21.2 was kept.

## V10. Timers

- A 2,042 min, H 2,036 min, D 2,647 min and B 622 min are inflated:
  each ran across the overnight break or the 9-hour F159 hang.
- C has no actual: its timer was never started.
- E (53 min) and G (6 min) were started only when their runs began;
  their code was written earlier with no timer running.
- F 158 min and I 17 min are as measured.

## V11. Acceptance walk, evidence per task

- A: three terms each proven red (`test_result_writer_required.py`);
  `git check-ignore` matches the sidecar (`.gitignore` line 27); the
  `CLAUDE.md` provenance bullet names `run_id_for(path, resume=True)`.
- B: equality on validation rows at every fraction, proven red; speed-up
  and longest learner in the result's `analysis`.
- C: 0.829 put back fails, proven red; stale-registry check proven red;
  the six non-decimal findings named in the test's docstring.
- D: one test per term (`test_term_1_can_fail`, `test_term_2_can_fail`);
  fail recorded on the main arm, 4 of 5 rule.
- E: control first, then the gap per instance under F153's rule; F25's
  card records the reopened design.
- F: seven algorithm documents and the comparison page; every figure
  resolves (`test_phase2_figures_resolve.py`); rankings only under the
  entry's paired test. F166's parallel gate now has a red proof per term.
- G: step 3 characterization; step 1 with its interval and the shuffled
  reference; step 2 not run, with the reason.
- H: assumptions labeled `[Assumption An]` with a register at the end;
  dates sourced in the document. Not machine-checked; please read.
- I: PDF tests before and after; pip-audit clean; `git status --short`
  on `docs/paper` and `docs/submission` is empty, so no tracked PDF
  changed.

---

## Decision

**D1. F156 failed, so F114 has no validated estimator. What next?**

1. Leave F114 blocked and add no estimator card now.
2. Add a card for F108's second named candidate, an HGB set for extreme
   imbalance, validated on F108's harness, seeds and margin (about 90
   minutes, zero metered), for a later sprint's refinement.
3. Close F114 and F156 as not achievable with the methods tried, with
   that reason on both cards.
