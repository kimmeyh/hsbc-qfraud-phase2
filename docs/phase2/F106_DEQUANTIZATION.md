# F106: an encoded circuit against its classical twins on ULB

Sprint 27 Task I, 2026-10-18. Zero metered seconds; a NumPy statevector,
no Braket call. The entry is the Phase 2 draft's section 6, "F106",
committed before the first run (`de63c40`); the step cut to 750 was
recorded in it before the eight-seed run (`a6b743f`). Every figure below
is in `experiments/phase2/results/f106_dequant.json` (seeds 42-49); the
one-seed pilot at 1,500 steps is `f106_dequant_pilot.json`. Run time
8,640 s.

## BLUF

**Inconclusive. The prediction (dequantized) is not confirmed, and the
falsifier (the circuit beats every twin) does not fire.** No twin's
99.17% interval clears the -0.005 margin, so no twin is shown to match
the circuit. Three twins are below it: logistic regression, the JOINT twin
and the RFF surrogate. Three are level with it, inside wide intervals:
GAM, GA2M and HGB. HGB is ahead on 6 of 8 seeds (+0.020 AUPRC, interval
-0.011 to +0.049). The test fold holds 99 positives, which is what makes
the intervals this wide. The encoding is phase-active (C = 0.53, far
above the 0.01 floor), so this does count as a test of the encoding.

## Results (Measured)

Test AUPRC, mean over eight seeds (range), then ROC-AUC:
- **circuit** 0.699 (0.635-0.741), ROC-AUC 0.965
- HGB 0.719 (0.663-0.751), 0.970
- GA2M 0.705 (0.618-0.754), 0.964
- GAM 0.704 (0.655-0.744), 0.967
- RFF 0.673 (0.612-0.735), 0.951
- logistic regression 0.662 (0.618-0.706), 0.949
- JOINT 0.625 (0.546-0.721), 0.960

Twin minus circuit, mean AUPRC delta, 99.17% paired bootstrap interval,
exact Wilcoxon p, seeds where the twin is ahead:
- HGB: +0.0203 [-0.0110, +0.0487], p = 0.195, 6 of 8
- GA2M: +0.0064 [-0.0217, +0.0391], p = 0.64, 5 of 8
- GAM: +0.0049 [-0.0170, +0.0299], p = 0.55, 4 of 8
- RFF: -0.0265 [-0.0510, -0.0016], p = 0.148, 2 of 8. **Below.**
- logistic regression: -0.0371 [-0.0643, -0.0102], p = 0.016, 1 of 8.
  **Below.**
- JOINT: -0.0741 [-0.1093, -0.0338], p = 0.016, 1 of 8. **Below.**

Diagnostics on the first layer (IBR section 6.4), mean over seeds:
- phase complexity C 0.533 (0.509-0.547);
- Berry connection |A| 0.096;
- summed single-qubit entropy 2.39 bits (1.47-2.93).

Trained lambdas, mean (range): 0.42 (0.27-0.48), 0.23 (-0.12-0.47),
0.68 (0.44-0.81). Features: the same eight V columns on every seed, in
slightly different orders (V10, V11, V12, V14, V16, V17, V3, V4).

## Reading

- **The circuit is a competent classifier on these phases, not a better
  one.** It sits level with the additive and tree twins and above the
  weakest ones. Nothing here shows a function the classical bar cannot
  reach.
- **The JOINT twin is the weakest lane, below its own GA2M base (0.625
  against 0.705).** Inferred: its six greedy 3-way terms overfit 6,295
  training rows with 295 positives. So "the complete bar" here is HGB and
  GA2M, not JOINT, and the circuit beating JOINT is not a finding about
  3-way structure.
- **Whether HGB matches the circuit is not settled.** HGB is ahead on 6
  of 8 seeds, but with 99 test positives the interval spans zero by a
  wide margin. More seeds would narrow it; a larger test set cannot be
  had on ULB's 492 positives.
- **HGB here is not the unstable F130 comparator.** Its eight values lie
  in 0.66-0.75 and track the other lanes. The setups differ (eight
  rank-phase features, 6,295 training rows at 4.7% positives).

## Limits

- 750 steps, cut from the preregistered 1,500 by timing alone (entry).
  The pilot's seed 42 circuit scored 0.6955 at 1,500 steps and the run's
  0.7053 at 750, so the cut did not obviously cost the circuit. One seed
  is not a test of that.
- Minibatch loss at step 700 is 0.013-0.070 across seeds, so training
  noise per seed is visible.
- 99 test positives per seed bound the precision of every AUPRC above.
- The circuit's AUPRC reproduces bit for bit only at F106's 8,192-row
  evaluation chunk. At 4,096 the scores move by at most 4e-14, near-tied
  rows reorder, and seed 42 moves by 1.5e-4 (found by F107's refusal).
  That is 30 times smaller than the margin.
- The circuit is exactly simulable at 8 qubits, so this tests the
  circuit's function class, not any computational effect (F6, section 3).
