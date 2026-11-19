# What We Have Learned About Quantum Advantage for Fraud Detection: Quantum Computing Expert Version

**Version 1.5**, 2026-11-18 (Sprint 33, card F178). For readers with
undergraduate-or-above or professional quantum computing experience,
not necessarily in machine learning. Acronyms and common terms link to
the [plain-terms version](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md);
statistical terms link to the
[machine learning expert version](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20ML%20Expert.md).
The appendix here holds only what neither defines.

## Change list

- **1.5, 2026-11-18 (Sprint 33)**: no new result. F25's hold in the Bottom line and section 6 gives the testable rule (Sprint 33 D6) and when it is checked: after the [preregistration](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#def-preregistration) is filed (D12).
- **1.4, 2026-11-16 (Sprint 33)**: no new result. The Bottom line and section 6 give the team lead's decision on F188 (Sprint 32 D4); section 6 notes the [preregistration](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#def-preregistration)'s state at filing.
- **1.3, 2026-11-10 (Sprint 32)**: F188, the rounding test, added as a tagged claim in section 3 and a dated result in section 6, which also lists F185 (alerts ranked by cost; detail in the machine learning expert version). The bottom line and section 5's three conditions now cite it, and the rounding test leaves section 7. No Sprint 33 run is preregistered yet, so none is listed.
- **1.2, 2026-11-06 (Sprint 31)**: the team lead's review. Each numbered section opens with an "In short" summary. Datasets are named in full once and by short name after, both linked to the plain-terms version's Appendix F. New: [interference](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qc-interference) beside [superposition](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qc-superposition) and [entanglement](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qc-entanglement), in outside research and in our circuit; a proposed experiment with all three properties and many non-Clifford gates; the scope of the F110 build cost; and the backlog proposals of Sprint 31 D18.
- **1.1, 2026-11-05 (Sprint 31)**: Sprint 31's results added. Each is a tagged claim under its topic's "What our experiments showed" and a dated result under "Experiments planned": F114, F155, F157 (both parts), Experiment 5 and F95. No Sprint 32 run is preregistered yet, so none is listed.
- **1.0, 2026-11-05 (Sprint 31)**: first version. Phase 1 and Phase 2
  through Sprint 30. Sprint 31's [device](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#def-device) and simulator runs have
  placeholders in "Experiments planned".

## Bottom line

- **No quantum resource was tested on hardware.** The hardware was QCi's
  [Dirac-3](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qc-dirac-3) and [Dirac-3S](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qc-dirac-3s), photonic measurement-and-feedback optimizers.
  QCi's own authors state Dirac-3 uses no [entanglement](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qc-entanglement) and that its
  per-loop measurement rules out a [quantum advantage](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qc-quantum-advantage) for that version.
  We treat both as analog optimizers and claim no quantum resource.
- **The Phase 1 training problem left the solver nothing to win.** The
  [CVQBoost](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qml-cvqboost) weight problem is a convex quadratic on the simplex; the
  device matched the certified classical optimum. A device can only show
  something on a non-convex problem where a classical solver measurably
  falls short.
- **The non-convex replacement is not yet decisive.** Cardinality
  constrained [learner selection](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qml-learner-selection) on the
  [fraud detection dataset of the Institute of Electrical and Electronics Engineers Computational Intelligence Society](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ds-ieee-cis)
  ([IEEE-CIS](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ds-ieee-cis)) has [room](#qc3-room) between greedy and
  the floor, but the best classical improvement on greedy found so far is
  under 2e-05. The Sprint 32 rounding test (F188) found that at 200:1
  the rounded problem's answer is worse than greedy on all six
  instances, so a device run on this design could not show a gain.
  The team lead decided (Sprint 32 D4, 2026-11-13; made testable by Sprint 33 D6, 2026-11-17): F25 stays on hold until, on F176's six instances at 200:1, the rounded problem's pick beats greedy's selection solved the same way (on the rounded problem, scored on the real one) by more than 1e-6 on at least one instance. On three of the six the pick is greedy's own selection, so only three can pass. The check needs no device time and runs after the preregistration is filed (Sprint 33 D12) (`docs/sprints/SPRINT_33_DECISIONS.md`).
- **Dirac-3S is a better solver than Dirac-3 on our one resolvable
  instance**, returning the reference optimum in every sample; accuracy
  did not change, because the optimum was already reachable classically.
- **The gate-based arm stays in simulation.** At every width we can
  afford the circuit is exactly simulable, and its simulated reading
  against [classical twins](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qml-classical-twin) is inconclusive at the test-positive counts
  the [credit card dataset of the Universite Libre de Bruxelles](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ds-ulb)
  ([ULB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ds-ulb)) allows. A circuit with superposition,
  entanglement and interference together was dequantized on [IEEE-CIS](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ds-ieee-cis).
- Device interpretations here are this project's own independent
  findings; QCi has not validated them
  (`docs/phase2/DIRAC_UNDERSTANDINGS.md`).

## How to read this version

- Same tiers, tags and claim rule as the plain-terms version: our
  results first, each bullet ending with its tracked source path; outside
  results second, with their EvidenceBasedDB grade.
  `experiments/src/test_learning_docs.py` checks the links, acronyms,
  paths and decimal figures.
- "Variables" means the continuous weights (one per [weak learner](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ml-weak-learner)) of a
  CVQBoost pool unless stated; "order 2" or "order 3" means [features](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ml-feature) per
  weak learner, not the polynomial degree, which is 2 throughout
  (`experiments/phase2/PREREGISTRATION_DRAFT.md`, section 3).

## 1. The optimization problem the devices solved

**In short:** Phase 1 trained CVQBoost's weights, a strictly convex
quadratic on the simplex, so any good solver reaches the same optimum.
Phase 2 moves to a cardinality-constrained selection problem, which is
not convex.

- **CVQBoost**: a pool of weak learners, each voting -1 or +1 on each
  training row; the weights minimize a quadratic objective, data term
  plus a ridge term, on the simplex (weights non-negative, summing to 1).
  The objective is quadratic for every configuration; Dirac devices
  solve it natively as a quasi-continuous problem
  (`docs/paper/proposal.md`, section 2).
- **Why the Phase 1 problem was easy**: with a ridge term the objective
  is strictly convex, so its optimum is unique and polynomial-time
  reachable; our classical solve is certified by its optimality
  residual. On the frozen pool the trees are unbounded, most learners
  reproduce the training [labels](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ml-label) exactly, and the Gram matrix is rank-one
  to numerical [precision](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ml-precision) (`docs/paper/proposal.md`, section 2).
- **The Phase 2 formulation**: choose exactly m learners (a cardinality
  constraint, binary variables), a [QUBO](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-qubo) with no [exact classical proxy](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qml-exact-classical-proxy) at
  scale. Its first proxy design failed its [falsifier](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#def-falsifier); its [IEEE-CIS](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ds-ieee-cis)
  design has room (section 3).

## 2. The hardware: Dirac-3 and Dirac-3S

**In short:** Dirac-3 matched the exact optimum on small problems and
lost fidelity as size grew, as its 200:1 resolution predicts.
Dirac-3S returned the optimum on our one resolvable instance, with no
change in accuracy. Dirac-3S takes 1,350 variables; schedule 4 showed
nothing.

### What our experiments showed

- [HW] On the Phase 1 [convex problem](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qc-convex-problem), Dirac-3 minus the exact solve was
  -0.0010 [AUPRC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auprc) (interval -0.0032 to +0.0012); hardware objectives were
  always above the exact minimum, by 0.013% to 0.413%; within-fit energy
  spread median 0.020%, maximum 0.343% (`docs/phase2/DIRAC_UNDERSTANDINGS.md`).
- [HW] Weight fidelity falls with pool size: cosine 0.975-0.999 up to 91
  variables, 0.89-0.90 at 560, 0.83-0.85 at 816 and 0.82-0.83 at 833,
  as the 200:1 weight-resolution limit predicts
  (`docs/phase2/DIRAC_UNDERSTANDINGS.md`).
- [HW] At 833 variables Dirac-3 returned sparser weights than the
  optimum, with exact zeros in all eleven fits (`docs/phase2/DIRAC_UNDERSTANDINGS.md`).
- [SIM] On the ten frozen Phase 1 pools, off-diagonal coefficients
  differ by at most 20.0 against a resolvable difference of 2,553.5, so
  agreement with the proxy there carries no fidelity information; B4's
  [Hamiltonians](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qc-hamiltonian), at 8.1 to 8.4 dB against the 23 dB limit, are the only
  ones where it does (`docs/phase2/DIRAC_UNDERSTANDINGS.md`).
- [HW] 11 of 12 [QSVM](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-qsvm) Hamiltonians in B5 exceeded the stated resolution
  (20.8-42.3 dB); B5's mean test [AUPRC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auprc) was 0.212
  (`docs/B4_B5_HARDWARE_RESULT.md`).
- [HW] Dirac-3 cost per fit was 84-90 s at 816 variables and 34-46 s at
  560; B2's measured 82.4 s per fit at 833 was confirmed
  (`docs/B4_B5_HARDWARE_RESULT.md`).
- [HW] Dirac-3 cost per sample was 11.27 s at 833 variables on B2
  (`docs/phase2/DIRAC_UNDERSTANDINGS.md`).
- [HW] On B4 (560 variables), Dirac-3S returned the reference optimum in
  all 8 samples of both jobs: [weight cosine](#qc3-weight-cosine) 0.999993 and 0.9999999,
  against Dirac-3's 0.895 and 0.901. A plain uniform vector scores
  0.993, and Dirac-3S's departures from uniform correlate 0.99976 and
  0.99999 with the optimum's (`docs/phase2/F142_DIRAC3S_VERIFY.md`).
- [HW] Dirac-3S weights lie within 0.000094 and 0.0000062 of the
  reference; the 8 samples of a job agree to 0.0000003 per weight and
  every returned value is a multiple of 0.0000001. That points to a
  post-processing step rather than an analog [output resolution](#qc3-output-resolution) of that
  fineness; which step is unverified (`docs/phase2/F142_DIRAC3S_VERIFY.md`).
- [HW] The device objective was below the reference solve's on both B4
  seeds in at least one sample (-0.0029 to -0.0025 on seed 42): the
  reference, an accelerated projected gradient, is less converged there
  (`docs/phase2/F142_DIRAC3S_VERIFY.md`).
- [HW] Same-pool test [AUPRC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auprc) did not change: 0.85224 for the reference
  against 0.85225 for the device on seed 42 (`docs/phase2/F142_DIRAC3S_VERIFY.md`).
- [HW, SIM] B2's +0.0256 at 833 variables is a pool effect: the exact solve
  of a rebuilt pool differs from the device by +0.0002 ([exact Wilcoxon signed-rank test](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20ML%20Expert.md#ml2-wilcoxon-test),
  p = 0.92), and the classical `deep` proxy cell alone reaches 0.7926
  against the twin's 0.7925 (`docs/phase2/F144_PROXY_TWIN.md`).
- [SIM] The pool effect is the subset order, not the feature count
  (F112, 10 seeds): order 2 to 3 adds +0.0245 [AUPRC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auprc); k 13 to 17 adds
  +0.0001, equivalent to zero within 0.005
  (`experiments/phase2/PREREGISTRATION_DRAFT.md`,
  `docs/sprints/SPRINT_27_SUMMARY.md`).
- [SIM] A software emulator of Dirac-3 matches the device's test [AUPRC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auprc)
  to within about 0.006 and its cost to within about 7%, but not its
  sparsity (14-38% exact zeros on the device, 0.2-17% emulated) or its
  solution shape on oilgas (cosine 0.83 against 0.89-0.90)
  (`docs/phase2/F17_EMULATOR.md`).
- [HW] Dirac-3S accepted a 1,350-variable continuous job at schedule 2,
  all entries returned, 6.0 metered seconds; the pool failed the resolution
  screen and the weights came back near flat, so size is shown, not solution quality
  (`experiments/phase2/results/f155_variable_ceiling.json`).
- [HW] [Relaxation schedule](#qc3-relaxation-schedule) 4 on Dirac-3S, four fits at 45 and 91
  variables: no change on the two 91-variable fits with a schedule-2
  twin on the same device, but both fail the resolution screen, so
  the test is weak; the 45-variable fits have only Dirac-3 history.
  67.0 metered seconds (`docs/phase2/F95_SCHEDULE4.md`).

### What outside research says

- QCi's authors state Dirac-3 detects its photons in every feedback loop
  and computes the next waveform electronically, which they say rules
  out a quantum advantage for that version (EvidenceBasedDB
  `dirac3-per-loop-measurement-rules-out-quantum-advantage`, high).
- They also state it uses no entanglement (EvidenceBasedDB
  `dirac3-does-not-use-entanglement`, high).
- The user guide gives an effective [analog resolution](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qc-analog-resolution) of about 200:1
  (23 dB): coefficients must differ by at least the largest over 200
  (EvidenceBasedDB `dirac3-analog-resolution-about-200-to-1`, high).
- The guide's variable ceiling falls with interaction order: 949 at
  second order, 135 at third, 39 at fourth, 19 at fifth
  (EvidenceBasedDB `dirac3-variable-ceiling-falls-with-interaction-order`,
  moderate).
- The guide's worked example returned the optimum in 23 of 100 trials
  (EvidenceBasedDB `dirac3-returns-suboptimal-answers-at-a-measurable-rate`,
  high).
- QCi's Dirac-3S review headline of optimal answers on every planted
  instance is contradicted by its own table (gaps of 7.56% and 9.59% at
  2,000 and 4,000 variables) (EvidenceBasedDB
  `dirac3s-all-optimal-headline-contradicted-by-own-table`, high).
- Classical solvers on a consumer computer matched QCi's published Dirac-3
  benchmarks; the authors read the device as sampling from an effective
  Gibbs distribution (EvidenceBasedDB
  `classical-solvers-match-dirac3-published-benchmarks`, low).

## 3. The non-convex selection problem (Experiment 3)

**In short:** the first design had no room above greedy. The [IEEE-CIS](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ds-ieee-cis)
design has room, but the best classical gain below greedy is under
2e-05, and rounding to 200:1 loses it on every instance.

### What our experiments showed

- [SIM] On the training fold, as every device run built it, the
  cardinality problem has many tied optima: every method reaches the
  floor (`docs/phase2/DIRAC_UNDERSTANDINGS.md`).
- [SIM] The first proxy design (held-out predictions, [ULB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ds-ulb)) fails its
  falsifier on all six instances: the best selection is 0.0016 to 0.0026
  above the floor, below the 0.01 required; greedy equals the best any
  method found; [SCIP](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-scip) at its 300 s cap did not improve on greedy
  (`docs/phase2/F153_EXP3_DESIGN.md`).
- [SIM] The two resolution checks disagree in kind there: the max/min
  coefficient ratio is about 2.01 (passes 200:1), but only 2.9% to 6.2%
  of coefficient pairs differ by at least max / 200 (fails)
  (`docs/phase2/F153_EXP3_DESIGN.md`).
- [SIM] On [IEEE-CIS](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ds-ieee-cis) (60 and 136 variables), greedy ends 0.096-0.098
  above the floor, so the room rule passes; [SCIP](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-scip)'s [dual bound](#qc3-dual-bound) puts the
  true optimum between greedy and about 0.08-0.18 below it
  (`docs/sprints/SPRINT_29_VALIDATION.md`).
- [SIM] Below greedy on 3 of 6 [IEEE-CIS](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ds-ieee-cis) instances, each by under 2e-05:
  [simulated annealing](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qc-simulated-annealing) from greedy reached -0.702763 against -0.702745 on
  one instance, with room about 0.097; [SCIP](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-scip) at 1,200 s never beat greedy;
  on the mid instances its dual bound (for example -0.9026 against a
  floor of -0.92) tightens the room to about 0.081-0.084
  (`docs/phase2/F176_BELOW_GREEDY.md`).
- [SIM] On 26 small instances solved exactly, greedy is above the
  optimum on 7, and the one-swap local search reaches the optimum on 4 of
  those 7, so "nothing below greedy" does not prove greedy optimal
  (`docs/phase2/F176_BELOW_GREEDY.md`).
- [SIM] A sparsity rule fixed before the fit failed one direction
  (held-out error 0.847 against a 0.05 tolerance)
  (`docs/sprints/SPRINT_26_SUMMARY.md`).
- [SIM] Rounding test (F188): every coefficient of F176's six [IEEE-CIS](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ds-ieee-cis)
  instances rounded to the nearest multiple of max |coefficient| / R,
  at R = 100, 200 and 400; the step is 0.015 at R = 200 on every
  instance. The registered reading (gain on the rounded problem) is
  "kept" at R = 200 on 42/free and 43/free, but by 0.0009 and 0.0012,
  49 and 73 times F176's gains: made by the rounding. The amendment's
  reading (the rounded problem's selection and weights, scored on the
  real objective) is worse than greedy on all six at R = 100 and 200;
  on the three gain instances the loss exceeds the gain (42/free
  0.000024 against 0.000018, 42/mid 0.000056 against 0.000003, 43/free
  0.0012 against 0.000017). The loss comes mostly from the rounded
  weights; on 43/free the pick also changes with R. At R = 400 only
  43/free delivers a gain. 200:1 is QCi's figure, carried to Dirac-3S
  and not measured there (`docs/phase2/F188_ROUNDING.md`).

### What outside research says

- In a [QUBO](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-qubo) solver comparison, branch-and-cut matched every reference
  energy on 176 instances, and the tested quantum approximate
  optimization runs showed no quality advantage (EvidenceBasedDB
  `hellstern-conclusions-main`, low).
- Grover search gives a quadratic, query-optimal speedup for
  unstructured search, not an exponential one (EvidenceBasedDB
  `qml-grover-quadratic-speedup-optimal`, high).

## 4. The gate-based arm, in simulation

**In short:** our 8-qubit circuit used superposition, entanglement and
interference, and was exactly simulable and dequantized. Outside
results agree that those three are not enough: a circuit becomes hard
to simulate through many non-Clifford gates.

### What our experiments showed

- [SIM] The design study recommends simulation only: at every affordable
  width the circuit is exactly simulable on a laptop, so hardware adds
  [noise](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qc-noise) and cost; no Braket service was called
  (`docs/phase2/F6_GATE_BASED_ARM.md`).
- [SIM] An 8-qubit, three-layer sandwich-encoded circuit on [ULB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ds-ulb) phase
  features (8 seeds, 99 test positives): circuit [AUPRC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auprc) 0.699 against [HGB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-hgb)
  0.719, [GA2M](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-ga2m) 0.705, [GAM](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-gam) 0.704, [RFF](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-rff) 0.673; inconclusive under the
  preset [equivalence margin](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20ML%20Expert.md#ml2-equivalence-margin) of 0.005 [AUPRC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auprc) (`docs/phase2/F106_DEQUANTIZATION.md`).
- [SIM] The encoding is phase-active: [phase complexity](#qc3-phase-complexity) 0.533 (0.509 to
  0.547), far above the 0.01 floor; Berry connection 0.096; summed
  single-qubit entropy 2.39 bits (`docs/phase2/F106_DEQUANTIZATION.md`).
- [SIM] Effective [Schmidt rank](#qc3-schmidt-rank) across the middle cut is a mean of
  1.67-3.22 of a possible 16, and the single-qubit expectation magnitudes
  average 0.25-0.41 (`docs/phase2/F107_SHOT_BUDGET.md`).
- [SIM] [Shot](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qc-shot) budget: about 10,000 shots per row to stay within 0.005
  [AUPRC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auprc) of exact, about 5.7 x 10^8 shots for one [ULB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ds-ulb) [test fold](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ml-test-fold); [AUPRC](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-auprc) is
  not monotone in shots, so the critical budget is unstable
  (`docs/phase2/F107_SHOT_BUDGET.md`).
- [SIM] On [SPECTRA](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ds-spectra)'s datasets, the Tier 1 screen says "candidate" on 32
  of 35 runs; it does not refuse fraud (`docs/phase2/F109_TIER1_LADDER.md`).
- [SIM] The circuit has all three properties: data-dependent Y
  rotations put each [qubit](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qc-qubit) in [superposition](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qc-superposition), a ring of
  exp(-i lambda Z Z) couplings entangles neighbors, and the readout
  depends on [interference](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qc-interference) between amplitudes; its rotation angles are
  data-dependent, so it is not a Clifford circuit. At 8 qubits it is
  exactly simulable by statevector, and on [IEEE-CIS](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ds-ieee-cis) it is dequantized
  (`experiments/phase2/src/f106_dequant.py`,
  `docs/phase2/F157_QNN_IEEE.md`).

### What outside research says

- Stabilizer circuits create large entanglement and [superposition](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qc-superposition) and
  still simulate efficiently (EvidenceBasedDB
  `chowdhury-gottesman-knill-restated-stabilizer-simulable`, high), and
  the stabilizer subtheory is not universal (EvidenceBasedDB
  `howard-stabilizer-subtheory-efficiently-simulable`, high).
- Interference does not change that. The Gottesman-Knill record does
  not mention interference, but any circuit of [Clifford gates](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qc-clifford-gate) only is
  classically simulable (EvidenceBasedDB `dz-lg-clifford-simulable`,
  low), and Clifford circuits already interfere: a Hadamard on each
  side of a phase gate cancels amplitudes (our inference, from the
  definition in EvidenceBasedDB `ferrie-classical-is-restricted-quantum`,
  low). Classical simulation cost grows exponentially with the number
  of non-Clifford operations, the "magic" (EvidenceBasedDB
  `cited-nonclifford-cost-magic`, low).
- Interference gives a large speedup only for special problems
  (EvidenceBasedDB `aaronson-foreword-special-problems`, low).
- Random parameterized circuits forming 2-designs have exponentially
  small gradient variance in the [qubit](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qc-qubit) count (EvidenceBasedDB
  `mcclean-rpqc-gradient-variance-exp-small`, high); local costs at
  logarithmic depth keep polynomial gradients (EvidenceBasedDB
  `cerezo-local-cost-polynomial-gradient-log-depth`, high).
- Trainable, non-dequantizable variational models are proved to exist,
  under a complexity assumption (EvidenceBasedDB
  `gilfuster-trainable-nondequantizable-exist`, high).
- Fidelity-kernel off-diagonal entries vanish exponentially in qubit
  count, so shots grow exponentially (EvidenceBasedDB
  `qfk-vanishing-similarity-definition`, high).
- Amplitude state preparation depth scales about linearly with the
  nonzero amplitudes (EvidenceBasedDB
  `appendix-b2-amplitude-state-prep-depth-limit`, high), and [QRAM](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-qram) needs
  resources of order rows times features (EvidenceBasedDB
  `ciliberto-qram-caveats`, high).
- Probabilistic error cancellation's sampling overhead is estimated as
  impractical for a 127-qubit circuit of depth 60 (EvidenceBasedDB
  `gacon-pec-sampling-overhead`, low); noise can induce [barren plateaus](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qml-barren-plateau)
  (EvidenceBasedDB `cerezo-noise-undermines-qml-claims`, high).
- The Inverse Born Rule Equivalence shows that real amplitude encodings
  with a data-independent unitary and basis measurement give classical
  quadratic forms, as summarized in our F6 study
  ([Zajac et al., arXiv 2602.21350](https://arxiv.org/abs/2602.21350)).

## 5. Quantum advantage on real hardware

**In short:** no device run showed an advantage. On our problems the
slow step is the classical pool build, not the solve.

### What our experiments showed

- [HW] The Phase 1 device campaign: 61 fits, zero failures, zero
  retries, and no accuracy gain over the exact solve
  (`docs/paper/proposal.md`).
- [HW] On the [IEEE-CIS](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ds-ieee-cis) feature ladder, hardware and classical proxy
  agreed within a maximum cell gap of 0.0013 over 12 cells
  (`docs/paper/proposal.md`).
- [SIM] The classical cost is in the pool build, not the solve: a serial
  833-variable build at full rows takes 773 s, and the 833-variable
  solve is flat in rows at about 0.35 s. The build's log-log slope in
  rows is 1.40 at 91 variables and 1.44 at 833; Hamiltonian
  construction is about linear (0.93 and 0.95). Scope: [ULB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ds-ulb), the serial
  full-pair build, 17,023 to 170,235 rows; a parallel build, other
  models and other datasets were not measured
  (`docs/phase2/F110_SCALING.md`).

### What outside research says

- For purely classical data no exponential advantage is known
  (EvidenceBasedDB `cerezo-no-known-exponential-advantage-classical-data`,
  high); the exponential speedup of quantum recommendation is removed
  under classical sampling access (EvidenceBasedDB
  `tang-no-exponential-speedup`, high).
- An experimental [QNN](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-qnn) advantage was estimated to need more than 60
  qubits (EvidenceBasedDB `jaderberg-scale-limit`, high).

### What this means for a device test

- A device result can carry information only when three conditions hold
  together: the Hamiltonian passes the resolution screens, a classical
  solver measurably misses the optimum, and the miss is larger than the
  device's resolution. F176's gains fail the third condition: F188
  rounded the instances to 200:1 and every rounded answer, scored on
  the real objective, lost to greedy (section 3). F188 adds a fourth
  check before any device proposal: score the rounded problem's pick
  on the real problem.
- The quantum role that fits production scale is a [QUBO](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-qubo) built from
  statistics accumulated over the rows (feature or learner selection),
  whose size does not grow with the data (EvidenceBasedDB memo
  `docs/spikes/F118_WHAT_THE_STORE_SAYS.md`, inference).

## 6. Experiments planned (Sprints 31 and 32)

**In short:** Sprint 31 ran these. The two device runs tested size and
a schedule, not accuracy; the circuit run on [IEEE-CIS](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ds-ieee-cis) was dequantized.
Sprint 32's rounding test found the device's 200:1 resolution too
coarse for the [IEEE-CIS](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ds-ieee-cis) selection design.

Sprint 31 ran these. Each entry is in `experiments/phase2/PREREGISTRATION_DRAFT.md`, written
before any call or score. Metered calls stop for approval with their call
count and seconds stated. The six-experiment frame is in
`docs/phase2/PHASE2_POC_PLAN_DRAFT.md`.

- **F155, the Dirac-3S variable ceiling**: one continuous job of 1,350
  variables (a CVQBoost pool on [ULB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ds-ulb), top 20 features, order 3: 20 + 190 +
  1,140), [relaxation schedule](#qc3-relaxation-schedule) 2, one sample. Accepted only if the
  returned solution has 1,350 entries. Its quote is a floor, since 1,350
  is above every Dirac-3S cost anchor.
  - Result, 2026-11-05: **accepted.** The solution has 1,350
    entries; 6.0 metered seconds, so 1,350 continuous variables run
    on Dirac-3S at schedule 2. The weights came back near flat
    (about 1/1,350 each); no accuracy is read
    (`experiments/phase2/results/f155_variable_ceiling.json`).
- **F95, relaxation schedule 4 on Dirac-3S**: four fits (two B1 91-variable
  rebuilds with Dirac-3S schedule-2 twins, two 45-variable fits with only
  Dirac-3 history), the relative gap to the reference optimum per
  sample. Cap 120 s over two stops. "No change" is the expected result.
  - Result, 2026-11-05: **no change on the two twin-compared fits**,
    whose pools fail the resolution screen, so the test is weak. The
    45-variable fits have only Dirac-3 history and are not compared.
    18.0, 18.0, 15.0 and 16.0 s per fit, 67.0 of the 120 s cap. There
    is no evidence for schedule 4; device plans stay at schedule 2
    (`docs/phase2/F95_SCHEDULE4.md`).
- **F157 [QNN](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-qnn) part**: the F106 circuit and six twins on [IEEE-CIS](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ds-ieee-cis)'s
  month-4 fold, about 2,962 test positives, so "dequantized" becomes
  decidable at the 0.005 margin.
  - Result, 2026-11-05: **dequantized.** [GAM](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-gam) and [HGB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-hgb) match
    the circuit within the margin; the encoding was phase-active on
    every seed (phase complexity 0.4842 to 0.5506 on seven seeds,
    and 0.095 on seed 48, about a fifth of the others; all above the
    0.01 floor)
    (`experiments/phase2/results/f157_qnn_ieee.json`).
- **F114, F157 [SPECTRA](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ds-spectra) part and Experiment 5**: classical ceilings,
  algorithm rankings and segment routing; see the machine learning
  expert version's section 7.
  - Result, 2026-11-05: all three reported in the machine learning
    expert version's section 7; none used a device.

Sprint 32 ran two more, zero metered seconds, each entry written in the
same file before its run. No Sprint 33 run is preregistered yet.

- **F188, the rounding test**: F176's six [IEEE-CIS](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ds-ieee-cis) instances rounded at
  R = 100, 200 and 400; a check first that the test can say "lost". The
  amendment of 2026-11-09, written after the first reading and before
  the second, scores the rounded problem's answer on the real objective.
  - Result, 2026-11-09: the check fired (7 exact-size cases, all lost at
    R = 2). Registered reading: "kept" on 42/free and 43/free, by gains
    the rounding made. Amendment's reading: worse than greedy on all
    six at R = 200. The amendment set no decision rule, so whether
    F25's [IEEE-CIS](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ds-ieee-cis) case closes was the team lead's decision
    (`docs/phase2/F188_ROUNDING.md`). The team lead decided (Sprint 32 D4, 2026-11-13; made testable by Sprint 33 D6, 2026-11-17): F25 stays on hold until, on F176's six instances at 200:1, the rounded problem's pick beats greedy's selection solved the same way (on the rounded problem, scored on the real one) by more than 1e-6 on at least one instance. On three of the six the pick is greedy's own selection, so only three can pass. The check needs no device time and runs after the preregistration is filed (Sprint 33 D12) (`docs/sprints/SPRINT_33_DECISIONS.md`).
- **F185, a cost-weighted [alert budget](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ml-alert-budget)**: classical; see the machine
  learning expert version's section 7.
  - Result, 2026-11-09: reported there; no device was used.

**Sprint 33 (2026-11-16): the preregistration ready to file.** No
experiment ran. `experiments/phase2/PREREGISTRATION_DRAFT.md` now gives
each section 6 entry a state at filing (Run, Partly run, To run) and its
result document; Experiments 3 and 6 are partly run. It is filed without
the program's brief, on assumptions A1 to A12 in
`docs/phase2/PHASE2_POC_PLAN_DRAFT.md`; the filing date and venue are
not set. `experiments/src/test_phase2_prereg_draft.py` keeps it
consistent through review; the byte lock comes at filing.

## 7. Experiments not yet planned

**In short:** ideas, not scheduled work: the store's ranked list, then
the team lead's review (2026-11-06), proposed for the backlog as
Sprint 31 D18. The main new one is a circuit beyond cheap simulation.

From EvidenceBasedDB's memo `docs/spikes/F118_WHAT_THE_STORE_SAYS.md`
(in that repository); none is scheduled.

- **Rounding test**: ran in Sprint 32 (F188, section 6). Its open
  follow-ups: other lambda values, other instance sizes, and R above
  400.
- **Resolution test on Dirac-3S**: rescale a Hamiltonian so distinct
  coefficients differ by at least max / 200 and test whether solution
  quality changes.
- **Per-sample success rate on Dirac-3S** against best-of-N.
- **Kernel concentration** against qubit count (2 to 14) and bandwidth,
  fidelity against projected kernels, on fraud features.
- **Fault-tolerant resource estimates** (logical qubits, T-count,
  wall clock) for each candidate quantum step at production sizes.

From the team lead's review:

- **A circuit with all three properties and many non-Clifford gates**
  (proposed card; related to the held F116 and F117). Design, for
  refinement:
  - Circuits: the F106 [sandwich encoding](#qc3-sandwich-encoding) plus layers of T and
    arbitrary-angle rotations, at widths 8, 12, 16 and 20 qubits and a
    non-Clifford count stepped so that the largest is beyond exact
    statevector cost on a workstation; a tensor-network or
    stabilizer-rank simulator records the classical cost of each.
  - Data: [ULB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ds-ulb), [IEEE-CIS](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ds-ieee-cis)'s month-4 fold, and [SPECTRA](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ds-spectra)'s four datasets
    on the quantum-enhanced `target` label, in and out of the pocket,
    with `target_real` as a second reading.
  - Comparators: the six F106 twins, [HGB](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-hgb), and a classical surrogate of
    the circuit's own kernel, on the same features and splits.
  - Gate: hardware only if a circuit beats every twin in simulation,
    and only under its own approval with shots and cost stated, since
    gate-based hardware is paid by use and adds noise.
  - Prediction (from the outside results above): the twins match the
    circuit wherever it is simulable, and no width we can afford
    leaves simulation.
- **A study of the data fraud investigators use** and **card-testing
  sequences**: classical; see the machine learning expert version's
  section 8. The cost-weighted [alert budget](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#ml-alert-budget) ran in Sprint 32 (F185).

## 8. Index of what was tested

**In short:** two quantum devices and one [statevector simulator](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#qc-statevector-simulator); no
gate-based hardware. The datasets are described in the plain-terms
version's Appendix F.

Every dataset, model and platform is listed with its source in the
plain-terms version's section 9. Hardware: Dirac-3 (Phase 1 blocks B1 to
B5, G0b) and Dirac-3S (F142, five fits); simulation: a NumPy statevector
of the 8-qubit circuit; no gate-based hardware.

## Appendix A. Terms neither other version defines

- <a id="qc3-relaxation-schedule"></a>**Relaxation schedule**: a Dirac
  device setting for how slowly the system settles; every Phase 1 fit
  used schedule 2.
- <a id="qc3-weight-cosine"></a>**Weight cosine**: the cosine between the
  device's weight vector and the reference optimum's; 1 means the same
  direction.
- <a id="qc3-simplex-constraint"></a>**Simplex constraint**: weights
  non-negative and summing to 1.
- <a id="qc3-input-resolution"></a>**Input resolution**: whether a device
  can tell a Hamiltonian's coefficients apart; checked by a spread test
  before a run.
- <a id="qc3-output-resolution"></a>**Output resolution**: how finely the
  returned values can differ.
- <a id="qc3-dual-bound"></a>**Dual bound**: a proven limit on how good
  the optimum can be, from a branch-and-bound solver such as [SCIP](ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage%20-%20Laymen%20terms.md#acr-scip).
- <a id="qc3-schmidt-rank"></a>**Schmidt rank**: the number of terms in a
  state's decomposition across a cut; a low effective rank means little
  entanglement across it.
- <a id="qc3-phase-complexity"></a>**Phase complexity**: a measure of how
  much an encoding uses complex phases rather than real amplitudes; near
  0 means the encoding reduces to a classical quadratic form.
- <a id="qc3-sandwich-encoding"></a>**Sandwich encoding**: data-encoding
  layers placed between trainable layers.
- <a id="qc3-room"></a>**Room**: the gap between greedy's objective and a
  bound on the optimum; without room no solver can beat greedy by much.
