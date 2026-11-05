# F157 QNN part: F106's circuit and twins on IEEE-CIS month 4

Sprint 31 Task G (#99), 2026-11-05. Zero metered seconds; a NumPy
statevector, no Braket call. The entry is F106 in
`experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, with its
2026-11-05 amendment (F157 QNN part), written before the module existed
or any lane was fit on the new data. Every figure below is in
`experiments/phase2/results/f157_qnn_ieee.json` (seeds 42-49); the
one-seed pilot is `f157_qnn_ieee_pilot.json`.

## BLUF

**Dequantized, by the entry's rule.** Two twins are shown to match the
circuit within the 0.005 margin: GAM (twin minus circuit +0.0047,
interval +0.0007 to +0.0092) and HGB (+0.0193, interval +0.0139 to
+0.0247). One twin whose lower bound is above -0.005 decides the outcome.
The circuit is ahead of logistic regression, the JOINT twin and the RFF
surrogate. F106 on ULB was inconclusive at 99 test positives per seed;
this test fold holds 2,962, which is what narrowed the intervals.

**Please read the caveat under Reading**: the interval resamples test
rows, not seeds. Across seeds HGB is ahead on 5 of 8 and its Wilcoxon p
is 0.109, so the seed-to-seed spread is wider than the interval.

## Results (Measured)

Twin minus circuit, mean AUPRC delta over eight seeds, 99.17% paired
bootstrap interval (2,000 resamples), exact Wilcoxon p, seeds where the
twin is ahead:
- HGB: +0.0193 [+0.0139, +0.0247], p = 0.109, 5 of 8. **No worse.**
- GAM: +0.0047 [+0.0007, +0.0092], p = 0.547, 4 of 8. **No worse.**
- GA2M: -0.0019 [-0.0060, +0.0024], p = 0.844, 4 of 8. Not decided:
  its lower bound, -0.0060, is below the -0.005 line by 0.001.
- JOINT: -0.0224 [-0.0270, -0.0176], p = 0.039, 2 of 8. **Below.**
- RFF: -0.0400 [-0.0449, -0.0349], p = 0.016, 1 of 8. **Below.**
- logistic regression: -0.0614 [-0.0665, -0.0560], p = 0.008, 0 of 8.
  **Below.**

Each seed's training rows: 295 positives and 6,000 negatives. Each
seed's test fold: all 85,302 month-4 rows, 2,962 positives. Per-seed
lane AUPRC and AUROC, the confusion counts at the 0.5% alert budget and
the stored test scores with their SHA-256 are in the result's `rows`.

Diagnostics on the first layer, per seed (`rows[].diagnostics`):
- phase complexity C: 0.4842 to 0.5506 on seven seeds; **0.095 on seed
  48**, still above the 0.01 floor;
- Berry connection |A|: 0.0267 (seed 48) to 0.0989;
- summed single-qubit entropy: 1.2639 to 3.538 bits.

Timing per seed (`rows[].seconds`): circuit training 682.5 to 719.9 s at
750 steps, prediction about 41 s, JOINT about 130 s, the other twins
under 6 s. The pilot projected 7,254 s for eight seeds, inside the
4-hour limit, so no seed was cut.

## Reading

- **The circuit is a competent classifier on IEEE-CIS, not a better
  one.** Its function is reached by an additive model (GAM) and by
  gradient-boosted trees (HGB) on the same eight features. This is the
  outcome F106 predicted and could not confirm on ULB.
- **The interval and the seeds disagree in strength.** The bootstrap
  resamples the test rows of each seed; with 2,962 positives it is
  narrow. The per-seed deltas vary more: HGB's run from -0.0143 to
  +0.0544. The entry's rule uses the interval, so the outcome stands as
  stated. A reading of "HGB is better than the circuit" would need the
  seed spread too, and the Wilcoxon p (0.109) does not support it.
- **GA2M is level but not decided.** Its interval is inside +/-0.006
  of zero; it misses the margin by about 0.001.
- **Seed 48 is the odd seed.** Its C is a fifth of the others and its
  Berry connection about a third, so the encoding was less
  phase-active there; the circuit's AUPRC on that seed (0.1993) is still
  inside the others' range. Inferred, not tested: the seed's features
  gave less phase spread.
- **The encoding was built as the entry states** (`encoding_built_wrong`
  is false).

## What this changes

- F106's question is answered on the second dataset: dequantized.
- The PoC plan draft records it under "Work beside the experiments".
- No device follow-up is proposed: a gate-based run of a circuit that a
  classical twin matches has nothing to show.
