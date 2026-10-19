# F109: Tier 1 on the six datasets on disk, and IEEE-CIS before and after aggregation

Sprint 27 Task G, 2026-10-18. Zero metered seconds. The entry is the
Phase 2 draft's section 6, "F109", committed before the first run
(`1d250d7`; prediction tightened in `eef3349` before any pilot output was
read). Every figure below is in `experiments/phase2/results/f109_ladder.json`
(five seeds, 42-46); the timing pilot is `f109_ladder_pilot.json`. Steel's
rows are cited from `f103_tier1.json`, not rerun (entry). Run time 3,700 s.

## BLUF

**The prediction is not falsified on any of the three fraud sets.** The
falsifier needed g4 (JOINT minus GA2M) >= 0.02 in at least 3 of 5 seeds on
one set. It fired on 0 seeds on ULB, 2 on IEEE-CIS before aggregation and
1 after. IEEE-CIS before aggregation is one seed short of the falsifier,
with a mean g4 of +0.020, so the margin is thin there. **Tier 1 says
`candidate` on almost every dataset and seed** (32 of 35), which is F103's
finding again: Tier 1 is permissive and does not refuse fraud. **The UID
aggregation raises every IEEE-CIS lane and lowers g4**: GAM 0.679 to
0.704, HGB 0.758 to 0.816, mean g4 +0.020 to +0.003.

## Results (Measured)

Lane test ROC-AUC, mean over five seeds (GAM, GA2M, HGB, JOINT), then g4
per seed, then the Tier 1 word:

- **ULB** (30,000-row subsample, 492 positives; features V14, V17, V10,
  V12, V11, V16 on every seed): 0.927, 0.942, 0.960, 0.950. g4 +0.009,
  +0.020, +0.001, +0.000, +0.009 (seed 43 is 0.0199, under 0.02).
  `candidate` x5.
- **IEEE-CIS before aggregation** (3,000 + 27,000; `card1` plus V columns
  from V189-V258): 0.679, 0.693, 0.758, 0.713. g4 +0.039, +0.003, +0.029,
  +0.019, +0.010. `candidate` x5.
- **IEEE-CIS after aggregation** (top features: `uid_TransactionAmt_mean`,
  `uid_C13_mean`, `uid_D15_mean`, `uid_D10_mean`, plus `card1` and V201 or
  V257): 0.704, 0.731, 0.816, 0.734. g4 +0.013, +0.001, +0.002, -0.023,
  +0.023. `candidate` x4, `refuse` x1 (seed 45, where g4 is negative).
- **Steel** (cited from F103): 0.914, 0.926, 1.000, 0.993. g4 +0.065 to
  +0.069. `candidate` x5.
- **ai4i**: 0.892, 0.914, 0.950, 0.913. g4 -0.009 to +0.005.
  `candidate` x3, `refuse` x2.
- **oilgas**: 0.917, 0.938, 0.957, 0.944. g4 +0.006 to +0.007.
  `candidate` x5.
- **telecom**: 0.851, 0.878, 0.944, 0.909. g4 +0.012 to +0.048 (4 of 5
  at or above 0.02). `candidate` x5.

Other gates: g1 (off-diagonal correlation) 0.76-0.81 everywhere; g3 (HGB
minus GAM) +0.02 to +0.13, largest on IEEE-CIS after aggregation (mean
+0.112, against +0.079 before); g5 is 5 qubits on the SPECTRA sets and 6
on ULB and IEEE-CIS (6 features).

## Reading

- **Inferred: no fraud set shows a 3-way interaction that JOINT finds and
  GA2M misses.** That fits the Fourier Wall spec's expectation for fraud,
  but Tier 1's word does not show it: the word is `candidate` because the
  gates are permissive, not because a quantum advantage is likely. Tier 2
  (F103's g6) is where the paper refuses.
- **The non-fraud sets carry the large g4 values**: Steel (+0.07) and
  telecom (+0.01 to +0.05). No prediction was made for them.
- **Aggregation helps every lane, the additive ones least.** HGB gains
  +0.058 and GAM +0.025, so g3 grows. Inferred: the UID aggregates carry
  structure that trees use and a per-feature Fourier basis does not.
- **HGB on the ULB subsample is the strongest lane** (0.960 ROC-AUC). The
  F130 ULB comparator failure (`docs/phase2/F130_LEVER_SCREENS.md`) did not
  appear here. The setups differ (ROC-AUC, not AUPRC; 1.6% positives, not
  0.17%; six rank-phase features, not 13 whitened ones), so this does not
  explain the F130 failure. Unverified.

## Limits

- ULB and IEEE-CIS use a 30,000-row subsample and six features, so the
  values are not comparable with the full-data harnesses (F105, Phase 1).
- AUC does not depend on the base rate, but the subsample's positive share
  (1.6% ULB, 10% IEEE-CIS) is not the population's.
- Five seeds, and the falsifier is a count, not a test.
