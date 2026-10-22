# Experiment 3 (F153): the proxy design, the result

Sprint 28 Task C (#50), 2026-10-22. Zero metered seconds. The entry is
`experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "Experiment 3",
committed before any Hamiltonian here was built (`db4c800`). Every figure
below is in `experiments/phase2/results/f153_exp3_design.json`. Code:
`experiments/phase2/src/f153_exp3_design.py`; test:
`experiments/src/test_f153_exp3_design.py`. Evidence tag `SIM`.

## BLUF

**The design fails under the entry's falsifier, so no device quote is
carried forward as ready and F25 does not proceed on this Hamiltonian.**
Both of the falsifier's conditions fire, each on all six instances:

- the gap between the best selection found and the floor is 0.0016 to
  0.0026, below the 0.01 the entry requires; and
- the chosen Hamiltonian fails F104's gate and fails the guide's
  pairwise check.

Changing the ridge weight does not open room. The gap is the data term,
about 0.002 at every weight tried, and greedy already reaches the best
selection any method found.

## Results (Measured, `SIM`)

- **Ridge sweep**: at every weight (2, 0.2, 0.02, 0.002) the greedy
  solution's data term is 0.16% to 0.33% of the objective's absolute
  value. None reaches 10%, so the rule's fallback applies: **0.002, rule
  not met**, labeled as the entry requires. (The run used a version of
  `choose_ridge` without the empty-weight guard added the same day; on the
  saved rows the current code gives the same choice.)
- **First-instance check** (seed 42, `free`): gap 0.0026, below 0.01. No
  room before any comparison.
- **Controls at 0.002**: greedy equals the best objective found on all six
  instances. Simulated annealing ties or is slightly worse. SCIP stopped at
  its 300 s cap on all six without improving on greedy.
- **F104's gate**: fails on all six (unchanged code).
- **The guide's check** (`resolution_check_guide`, new, opt-in):
  - the max/min ratio of the nonzero coefficients is about 2.01, far
    inside 200, so **that half passes**;
  - only 2.9% (`mid`) to 6.2% (`free`) of coefficient pairs differ by at
    least max / 200, so **the pairwise half fails**.
- **Test AUPRC, context only** (three seeds, no interval): 0.74 to 0.82
  across instances; each row carries an outcome block.
- **Device quote**: 77 to 251 s on Dirac-3S (inferred bracket from F139's
  two Dirac-3 integer probes). Not carried forward as ready (falsifier).

## Reading

- **The ridge rule was ill-posed (Inferred).** The objective is
  `data term - 1 + ridge` in `exp3_controls`' scaled units, so its
  absolute value is close to 1 at every weight. A data term of about 0.002
  can never be 10% of it. The rule meant "the data term is a material
  share of what the optimizer trades off"; a share of data against ridge
  would have said that. This does not rescue the design: the gap to the
  floor is the data term itself, and it does not move with the weight.
- **The two resolution checks disagree in kind (QCi A7).** QCi's answer
  of 2026-10-20 placed the 200:1 limit on "the ratio of max and min linear
  contributions" (guide section 5.3). On these Hamiltonians that ratio is
  about 2 and passes. What fails is how finely the coefficients differ
  from each other, which F104's gate and the pairwise share measure. Which
  of the two the device actually honors is still **unverified**; QCi's
  answer reads as the ratio, our measured A31 finding as the pairwise
  differences. Both are reported, as Decision 1 asked.
- **Consistent with F94**: a device cannot show an advantage on this
  formulation. The limit is the formulation, not the solver.

## What follows

- F25 (the device arm) stays parked until a formulation leaves measurable
  room between greedy and the floor. No metered seconds are requested.
- `device_resolution.resolution_check_guide` is opt-in; every Phase 1
  caller and `resolution_gate` are unchanged.
