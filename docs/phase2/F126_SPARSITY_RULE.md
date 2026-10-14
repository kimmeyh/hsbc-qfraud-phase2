# F126: Does a Threshold Rule Predict the Device's Exact Zeros? No.

**Sprint 26 Task F**, 2026-10-14. Zero metered seconds. Evidence:
`experiments/phase2/results/f126_sparsity_rule.json` (tag SIM), from
`experiments/phase2/src/f126_sparsity_rule.py`. The rule, its fit and the
0.05 tolerance were committed before the first run (`81270b8`).

**Who reads this**: the team lead, and anyone modeling Dirac-3's output
(F17's emulator, F25).

## Bottom line

1. **The pre-set rule fails.** Rule R1, "the device zeroes every learner
   whose exact-optimum weight is below tau / n", was fitted on one
   dataset's 5 B4 fits and tested on the other's. Fitted on oilgas, it
   predicts telecom's zero fraction within 0.016 (mean absolute error,
   passes 0.05). Fitted on telecom, it misses oilgas by 0.847. The test
   required both directions, so **R1 fails**. **Measured** (SIM):
   `primary_passes_both_directions`, `directions.*.R1_relative_threshold`.
2. **On oilgas the rule fits only on a knife edge.** About 79% of the
   nonzero exact weights sit at one tied value, 1.023-1.025 / n on the
   five seeds, and the rest lie just below it. Averaged over the five
   seeds, R1's predicted zero fraction is 0.12 at tau 1.020, 0.14 at
   1.022 and 0.67 at 1.024; the device's is 0.14-0.16. So a tau fits
   oilgas only inside a window about 0.002 wide. **Measured** (SIM), from
   the cached exact weights.
3. **On telecom the rule cannot locate that window.** Its predicted zero
   fraction is flat at 0.35 for every tau from 0.9 to 1.34, so the
   telecom fit is nearly indifferent across that range. The grid's
   minimum fell at 1.342, which predicts 1.0 on oilgas; a tau of 1.0,
   equally good on telecom, predicts 0.07. Either way the transfer fails.
   **Measured** (SIM).
4. **The one passing direction is a coincidence.** Oilgas's narrow
   window (tau about 1.022) happens to lie inside telecom's flat range.
   Nothing in the rule explains why the two datasets should agree there.
   **Inferred.**
5. **What the device zeroes is not set by the exact weight's size.** On
   oilgas about 95% of learners have exact weights tied or within 4% of
   the tie (all five seeds, 0.946-0.950). The device zeroes 14-16%, so at
   least two-thirds of its zeros must fall among learners the exact
   solution weights almost equally. (Counting only: the rebuilt pool is not
   the device's, so no zero is matched to a learner.) This fits A31:
   the device cannot resolve differences this small, so on a near-uniform
   optimum it returns a sparser vector whose support the exact solution
   does not determine (`experiments/PREREGISTRATION.md` amendments A31
   and A32). **Inferred.** The leading alternative is that the exact
   weights come from rebuilt pools, not the device's own, which were never
   stored. It is not ruled out; F145 measured that drift on ULB's `free`
   pool at 327 of 4,426,188 test cells, small beside a tie held by 79% of
   the learners.

**Card outcome**: the acceptance's second branch, "a recorded finding
that the fits cannot support one". The 10 B4 fits cannot support a
threshold rule on the exact weights. The reason is structural: on oilgas
the optimum is nearly uniform, so the rule has nothing stable to fit.

## Figures

All from `f126_sparsity_rule.json`. Zero fraction is the share of weights
exactly 0.0 in the lowest-energy device sample, as F17 measured it.

| Dataset | n | Device zero fraction | Exact-optimum zero fraction |
|---|---|---|---|
| oilgas_gasturbine | 560 | 0.1446-0.1625 | 0.0036-0.0054 |
| telecom_churn | 816 | 0.3542-0.3787 | 0.1189-0.1311 |

| Rule | Fit on oilgas, test telecom (MAE) | Fit on telecom, test oilgas (MAE) |
|---|---|---|
| R1: exact weight below tau / n (primary) | 0.016 (tau 1.022) | 0.847 (tau 1.342) |
| R2: exact weight below t (reported) | 0.553 | 0.108 |
| R0: the other dataset's mean (reference) | 0.213 | 0.213 |

B5's 12 QSVM fits (27 variables, ULB), descriptive only and not part of
the test: zero fractions 0.81-0.93.

## What this means for the emulator and for F25

- **F17's emulator should not be tuned to match zero fractions** through a
  weight threshold. The device's support on a near-uniform optimum is not
  recoverable from the optimum. **Inferred.**
- **A device run is only informative where the optimum is not
  near-uniform.** F94 found the cardinality problem has many tied optima
  on the training fold, so F25's held-out Hamiltonian is the place to look.
  **Inferred**, from F94 and point 2.

## Limits

- Ten fits, two datasets, one pool configuration family.
- Exact weights from seeded rebuilds (F145), not the device's own pools.
- Only the lowest-energy sample is scored, as F17 did. Every sample is on
  disk, so a per-sample analysis costs no device time.
