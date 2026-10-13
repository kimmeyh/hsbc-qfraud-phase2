# F94: Experiment 3's Classical Controls

**Sprint 25 Task F** (#18) | **Date**: 2026-10-13 | **Evidence tag**: `SIM`,
zero metered seconds
**Result file**: `experiments/phase2/results/f94_controls.json`. Every
objective, time, status and AUPRC below is in it; the bound and the gaps to
it are computed from it, as shown.
**Generator**: `experiments/phase2/src/exp3_controls.py` (tests:
`experiments/src/test_exp3_controls.py`)
**Solver**: SCIP 10.0 through PySCIPOpt 6.2.1 (Sprint 25 D4), behind an
`ExactSolver` interface so a Phase 2 commercial solver can be swapped in

## Bottom line

- **The controls are built and correct.** Exact enumeration, greedy
  selection, simulated annealing and SCIP each return a selection within the
  learner limit. SCIP certified the optimum and matched enumeration on all 6
  small checks (20 learners, choose 4). Only the 3 validation-fold checks
  test it; the 3 training-fold checks have a trivial answer (below).
- **The objective has a floor every method can be measured against.** With
  plus-or-minus-one learners and labels, the objective equals
  `||H'w - y||^2 / n - 1 + 2 ||w||^2` (`n` rows). The first term is never
  negative and `||w||^2` is at least `1/m`, so **`-1 + 2/m` is a lower bound
  on every instance**: -0.8 at m = 10, -0.92 at m = 25. (Found by the
  fresh-eyes review; it is algebra on the generator's own objective.)
- **On the training fold, every method reaches the floor.** 51 to 53 of the
  first 60 `free` learners and 123 to 126 of the 136 `mid` learners classify
  every training row correctly, so any m of them at equal weight hits the
  floor exactly. There are many optimal selections and nothing to choose
  between them. **Experiment 3 built on the training fold, as every device
  run builds it, could not tell a device from a greedy loop.**
- **On the validation fold, the best selection found is within 0.0016 to
  0.0026 of the floor.** That is the most any method, a device included,
  could still gain. Greedy found the best objective on all 6 instances;
  annealing matched it on the 3 smaller ones and came within 3e-6 on the 3
  larger. **Greedy and annealing are equivalent here; greedy is the cheaper,
  deterministic bar.**
- **The ridge carries almost all of the objective.** The data term (how
  well the selection fits the labels) is at most 0.33% of the objective's
  size on any instance; the rest is the ridge term `2 ||w||^2`, from
  `lambda = 2 * rows`. That is the main design question for F25 (below).

## What was run

- **Instances**: ULB, seeds 42-44, sequential pool builds of the frozen
  `qubo_proxy` cells: the first 60 learners of `free` (78) with at most 10
  selected, and the whole 136-learner `mid` pool with at most 25. Sizes were
  corrected at plan verification from the card's 60 and 150, which came
  from synthetic probes.
- **Objective**: `qubo_proxy`'s Hamiltonian, `w'(HH^T + lambda*I)w -
  2(Hy)'w` with `lambda = 2 * rows`, weights summing to 1, divided by the
  row count. Every method's weights are re-solved exactly on the support it
  chose, so methods differ only in the support.
- **Two sources** (added during the run; see Deviations): the training fold,
  as `qubo_proxy` and the device runs build it, and the validation fold.
  Test AUPRC is scored on the test fold, which is never optimized on.
- **Exact check**: the first 20 `free` learners, choose 4, on each source
  and seed: 4,845 supports enumerated against SCIP.

## Results

Objective (lower is better). The floor is -0.8 for the 60-learner instances
and -0.92 for the 136-learner ones.

| Source | Seed | 60 learners, m=10: greedy / annealing / SCIP | 136 learners, m=25: greedy / annealing / SCIP |
|---|---|---|---|
| train | 42-44 | the floor, -0.8, for all three methods | the floor, -0.92, for greedy and annealing; SCIP within 1.1e-7 |
| validation | 42 | -0.7973701 / -0.7973701 / -0.7972679 | -0.9175500 / -0.9175491 / -0.9171576 |
| validation | 43 | -0.7982406 / -0.7982406 / -0.7981195 | -0.9183652 / -0.9183643 / -0.9181830 |
| validation | 44 | -0.7977373 / -0.7977373 / -0.7973906 | -0.9178998 / -0.9178970 / -0.9178076 |

- **Gap from the best found to the floor** (validation): 0.0026, 0.0018 and
  0.0023 at 60 learners; 0.0025, 0.0016 and 0.0021 at 136.
- **SCIP's shortfall behind greedy** (validation): 9e-5 to 4e-4. SCIP hit
  its 600 s cap on all 6 validation instances and on the 3 training-fold
  136-learner ones.
- **SCIP's reported gap is not the gap still open.** SCIP reports a
  relative gap of 0.25 at 60 learners and 0.11 at 136 (PySCIPOpt's
  `getGap`: the difference between its incumbent and its own bound, divided
  by the smaller of the two). Its bounds (-0.995 to -1.025) are weaker even
  than the plain continuous relaxation (about -0.96 and -0.98), let alone
  the floor. The real open gap is the 0.0016-0.0026 above.
- **Time**: greedy 0.04-5.4 s, annealing 0.3-5.9 s (3,000 iterations, one
  run per instance, not tuned), SCIP 10-24 s where it certified, otherwise
  its 600 s cap.
- **Unlimited selection** (all learners allowed) uses every learner on every
  instance, so the limit always binds.
- **A note on the result file.** Its `best_method` field names annealing
  alone on 4 of the 6 training-fold instances. That is floating-point
  rounding (differences of 2e-16 under an exact equality test); all three
  methods reached the floor.
- **Learner diagnostics.** The file's `agreement_with_label` and
  `pairwise_agreement_min` fields are correlations on a plus-or-minus-one
  scale. As fractions of rows: on the validation fold each learner is
  correct on 99.63% to 99.92% of rows; on the training fold every pair of
  learners agrees on at least 99.989%.

## Test AUPRC: context only

The objective is the experiment; test AUPRC is reported for context, over 3
seeds, with no interval.

- On the **training fold**, all methods reach the floor, and the selection
  they happen to pick among equals moves test AUPRC by 0.10 on two
  instances and 0.03 on the other four.
- On the **validation fold**, greedy's 25-of-136 selection scored 0.83,
  0.75 and 0.77 on test, against 0.80, 0.76 and 0.73 using all 136 learners
  solved on the same fold. Greedy's validation-built selections also beat
  its training-built ones on all 6 seed and size pairs. Neither is evidence
  at 3 seeds; both say F25 might build on held-out predictions.
- **Building on the validation fold uses it up.** Any later tuning would
  need another held-out fold.

## What it means for F25 and Experiment 3

- **Build the Hamiltonian on held-out predictions.** On the training fold
  the dct learners memorize the data, many selections reach the floor, and
  any solver returns an arbitrary one of them.
- **Choose the ridge weight deliberately.** With `lambda = 2 * rows`, the
  data term is at most a third of a percent of the objective, and the best
  found is already within 0.0026 of the floor. A device could gain at most
  that much over greedy. A smaller ridge weight makes the fit to the labels
  matter. This is the first design decision for F25, ahead of shallower or
  different learners.
- **The comparison bar is greedy, and the gap to the floor is the room
  left.** A device result counts only if it beats greedy's objective, or
  matches it faster, and is reported against the floor.
- **Resolution.** QCi's stated limit (about 200:1) applies to the
  coefficients the device receives. The differences that separate one
  learner from another here are about 1 part in 300 of the objective (an
  inference from the learner diagnostics, not a measurement). Run F104's
  screen on these validation-fold Hamiltonians before F25 is sized.

## Deviations from the plan

- **Two sources instead of one.** The plan built instances on the training
  fold only. The first run showed every selection tying there, so the
  controls could not be compared. The run was stopped, the validation-fold
  source added, and both re-run; nothing from the stopped run was kept.
- **Code review fixes before the committed run**: SCIP's agreement requires
  a certified optimum; SCIP's support is read from its binary variables;
  every selection is checked against the limit; SCIP is excluded from the
  ranking if it fails an exact check; a pool smaller than the instance size
  is refused.
- **The generator's comment on `SOURCES`** cites "69 of 78" and "124 of 136"
  perfect learners. Those came from a separate, uncommitted check of seed
  42's whole pool. The committed figures are the first-60 counts above
  (51-53) and 123-126 for `mid`.
