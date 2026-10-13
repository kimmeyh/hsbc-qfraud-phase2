# F94: Experiment 3's Classical Controls

**Sprint 25 Task F** (#18) | **Date**: 2026-10-13 | **Evidence tag**: `SIM`,
zero metered seconds
**Result file**: `experiments/phase2/results/f94_controls.json` (every
figure below is in it)
**Generator**: `experiments/phase2/src/exp3_controls.py` (tests:
`experiments/src/test_exp3_controls.py`)
**Solver**: SCIP 10.0 through PySCIPOpt 6.2.1 (Sprint 25 D4), behind an
`ExactSolver` interface so a Phase 2 commercial solver can be swapped in

## Bottom line

- **The controls are built and correct.** Exact enumeration, greedy
  selection, simulated annealing and SCIP each return a selection within the
  learner limit. SCIP **certified** the optimum and matched enumeration to
  1e-6 on all 6 small checks (20 learners, choose 4), so the falsifier for
  the solver leg did not fire.
- **On the training fold, as every device run builds it, the problem has no
  answer to find.** On the training fold, 51 to 53 of the first 60 `free`
  learners and 123 to 126 of the 136 `mid` learners classify every row
  correctly, and every pair agrees on at least 99.98% of rows. Every
  selection of m learners then gives the same objective (-0.8 at m = 10,
  -0.92 at m = 25), and all four controls tie. **Experiment 3 built this
  way could not tell a device from a greedy loop.** This is the most
  important result for F25.
- **On the held-out validation fold the learners differ, and the controls
  can be compared.** No learner is perfect there (agreement with the label
  0.993-0.998). Greedy selection found the best objective on all 6
  instances; simulated annealing matched it on the 3 smaller ones and came
  within 3e-6 on the 3 larger. SCIP did not certify optimality within its
  600 s cap on any of them (relative gap 0.25 at 60 learners, 0.11 at 136),
  and its incumbent was 1e-4 to 4e-4 worse than greedy's.
- **So at these sizes the strongest control is greedy, in under 6
  seconds.** An exact certificate exists only at small sizes; a device
  result in Experiment 3 would be compared against greedy and annealing,
  with SCIP's bound reported as the gap still open.

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
- **Two sources** (added during the run; see Deviations): the training fold
  (170,235 rows), as `qubo_proxy` and the device runs build it, and the
  validation fold (56,745 rows). Test AUPRC is scored on the test fold,
  which is never optimized on.
- **Exact check**: the first 20 `free` learners, choose 4, on each source
  and seed: 4,845 supports enumerated against SCIP.

## Results

Objective (lower is better). Train-fold values are identical across methods
to 1e-7 on every instance and are shown once.

| Source | Seed | 60 learners, m=10: greedy / annealing / SCIP | 136 learners, m=25: greedy / annealing / SCIP |
|---|---|---|---|
| train | 42-44 | -0.8 for all three methods, every seed | -0.92 for all three methods, every seed |
| validation | 42 | -0.7973701 / -0.7973701 / -0.7972679 | -0.9175500 / -0.9175491 / -0.9171576 |
| validation | 43 | -0.7982406 / -0.7982406 / -0.7981195 | -0.9183652 / -0.9183643 / -0.9181830 |
| validation | 44 | -0.7977373 / -0.7977373 / -0.7973906 | -0.9178998 / -0.9178970 / -0.9178076 |

- **SCIP status**: optimal on the 3 train-fold 60-learner instances; time
  limit on the other 9. Relative gap 0.034-0.041 on train at 136, 0.25 on
  validation at 60, 0.11-0.12 on validation at 136.
- **Time**: greedy 0.04-5.4 s, annealing 0.3-5.9 s (3,000 iterations),
  SCIP 10-24 s where it certified, otherwise its 600 s cap.
- **Unlimited selection** (all learners allowed) uses every learner on every
  instance, so the limit always binds.

## Test AUPRC: context only

The objective is the experiment; test AUPRC is reported for context, over 3
seeds, with no interval.

- On the **training fold**, tied selections score anywhere from 0.61 to
  0.78 on test. Which learners a method happens to pick among equals moves
  test AUPRC by more than 0.1, which is what a flat objective means.
- On the **validation fold**, selecting 25 of 136 learners scored 0.83,
  0.75 and 0.77 on test (greedy), against 0.80, 0.76 and 0.73 using all 136
  learners solved on the same fold. Two seeds of three favor the limited
  selection. That is not evidence of anything at 3 seeds; it is a reason
  F25 might build on held-out predictions.

## What it means for F25 and Experiment 3

- **Build the Hamiltonian on held-out predictions, not the training fold.**
  On the training fold, dct learners memorize the data and the cardinality
  problem is flat; any solver, quantum or classical, returns an arbitrary
  tie. Validation-fold predictions (a standard stacking practice) give a
  problem with structure. Alternatives: shallower learners, or a different
  learner type. F25's design must choose before any device run.
- **The comparison bar is greedy.** At 60 and 136 learners greedy reached
  the best objective found, in seconds, and SCIP could not certify better
  in 10 minutes. A device result would need to beat greedy's objective, or
  match it faster, to count.
- **The objective differences are small** (1e-4 between the best and SCIP's
  incumbent). The device's stated resolution of about 200:1 may not resolve
  them. F104's screen should be run on these validation-fold Hamiltonians
  before F25 is sized.

## Deviations from the plan

- **Two sources instead of one.** The plan built instances on the training
  fold only. The first run showed that every selection ties there, so the
  controls could not be compared. The run was stopped, the validation-fold
  source added, and both re-run; nothing from the stopped run was kept.
- **Code review fixes before the committed run**: SCIP's agreement now
  requires a certified optimum; SCIP's support is read from its binary
  variables; every method's selection is checked against the limit; SCIP
  is excluded from the ranking if it fails an exact check; a pool smaller
  than the instance size is refused.
