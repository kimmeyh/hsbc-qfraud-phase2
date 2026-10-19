# F107: the shot budget of the F106 circuit

Sprint 27 Task J, 2026-10-18. Zero metered seconds; a NumPy statevector.
The entry is the Phase 2 draft's section 6, "F107", committed before the
first run (`bfd0d58`); the chunk-size note was added before any F107
result (`6d551af`). Every figure below is in
`experiments/phase2/results/f107_shots.json`: F106's eight trained
circuits (`f106_dequant.json`) on F106's test folds. Run time 508 s.

## BLUF

**The F106 circuit needs about 10,000 shots per row or more before its
test AUPRC stays within 0.005 of the exact statevector's.** The critical
budget is 10,000 on four seeds and above 10,000 on three. The prediction
(a budget between 100 and 10,000) holds on 5 of 8 seeds. **The measure
itself is unstable**: AUPRC does not rise steadily with the shot count,
so "the smallest budget within 0.005" can land on a lucky value. Seed 46
reads 100 shots, but it is 0.054 short at 1,000. With 99 test positives,
shot noise reorders a few positives and moves AUPRC by several points. At
10,000 shots it is still +0.034 above exact on seed 44.

## Results (Measured)

Exact AUPRC, then AUPRC at 10, 100, 1,000 and 10,000 shots per row, then
the critical budget:
- s42: 0.705; 0.362, 0.686, 0.680, 0.714; above 10,000
- s43: 0.717; 0.413, 0.626, 0.699, 0.719; 10,000
- s44: 0.721; 0.515, 0.736, 0.751, 0.755; above 10,000
- s45: 0.635; 0.335, 0.621, 0.621, 0.638; 10,000
- s46: 0.741; 0.539, 0.740, 0.687, 0.735; 100
- s47: 0.649; 0.563, 0.632, 0.635, 0.653; 10,000
- s48: 0.737; 0.477, 0.687, 0.721, 0.754; above 10,000
- s49: 0.687; 0.452, 0.702, 0.679, 0.689; 10,000

Every exact value matches F106's recorded circuit AUPRC (the module
refuses otherwise).

Measured beside it, per seed, over 500 test rows:
- **effective Schmidt rank** across the 0-3 | 4-7 cut: mean 1.67-3.22 of
  a possible 16;
- **|<Z_q>|**: mean 0.25-0.41, with the lowest 10% of values at
  0.04-0.09.

## Reading

- **A hardware run of this circuit would need about 10,000 shots per row,
  or more, to reproduce its simulated AUPRC.** At 56,962 test rows that is
  about 5.7 x 10^8 shots for one test fold. This supports F6's
  recommendation of simulation only (Inferred).
- **Small |<Z_q>| values are the likely reason** (Inferred). The readout is
  a weighted sum of expectations, and a tenth of them lie below 0.09, so
  shot noise of about 1/sqrt(m) is the same size as the signal until m
  is large.
- **The entanglement is low**: an effective rank of 2-3 out of 16. No
  relation to the shot budget is claimed (entry); eight circuits at one
  entanglement level cannot show one. That needs F116's ON-against-OFF
  ablation, which stays on HOLD because F106 did not show the circuit
  ahead.

## Limits

- The grid has four points, so the budget is known only to within a
  factor of 10.
- The "within 0.005" criterion is noisy on 99 positives. A per-seed
  repeat over several shot draws would give the budget as a distribution;
  this run has one draw per m.
- Shot noise only. No gate noise, readout error or device model.
