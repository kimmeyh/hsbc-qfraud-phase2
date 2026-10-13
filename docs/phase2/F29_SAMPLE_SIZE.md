# F29: The CVQBoost Optimum Does Not Move With Sample Size

**Sprint 25 Task E** (#17) | **Date**: 2026-10-13 | **Evidence tag**: `SIM`,
zero metered seconds
**Result file**: `experiments/phase2/results/f29_sample_size.json`
**Generator**: `experiments/phase2/src/sample_size.py` (tests:
`experiments/src/test_sample_size.py`)

## Bottom line

**Insensitive, and the reason is structural.** On ULB, with the frozen
`free` pool (78 learners), the weights solved on 1/8, 1/4 and 1/2 of the
training fold have cosine at least 0.99999999999994 with the full-fold
weights, on all 3 seeds. The plan's threshold was 0.99, so the premise
holds and the card closes.

But the optimum does not move because it **cannot**: on every solve the
weights are uniform to about one part in a million (largest over smallest
weight, 1.0000009 to 1.0000023). This is the Sprint 4 degeneracy finding,
measured again. The test confirms it; it does not add a new property of
the optimizer.

## Why the optimum is pinned

The objective is `w'(HH^T + lambda*I)w - 2(Hy)'w` with `lambda = 2 *
n_train` (the frozen `LAMBDA_MULT`). Dividing by `n_train` changes no
argmin and gives `HH^T/n + 2I` and `-2Hy/n`. Every entry of `HH^T/n` is
an average of plus-or-minus-one products, so it lies in [-1, 1], while the
ridge adds 2 to every diagonal entry. On the simplex the ridge term is
smallest at uniform weights, and it dominates. Because `lambda` scales with
`n`, a smaller sample changes only the noise in those averages, never the
balance between the two terms. Sample size has nothing to act on.

## Results

| Fraction of the train fold | Rows | Cosine with full-fold weights (min) | Test AUPRC, mean of 3 seeds (sd) |
|---|---|---|---|
| 1/8 | 21,280 | 0.99999999999995 | 0.7642 (0.035) |
| 1/4 | 42,559 | 0.99999999999995 | 0.7663 (0.033) |
| 1/2 | 85,118 | 0.99999999999999 | 0.7673 (0.033) |
| 1 | 170,235 | 1 | 0.7672 (0.034) |

Means are from the committed result file. All 78 weights are nonzero at
every size.

## How to read the AUPRC column

- The differences across fractions (at most 0.003) are smaller than the
  spread across seeds (about 0.03).
- With weights equal to six decimals, the ensemble score is close to a
  plain vote count, which has many ties. Weight differences of one part in
  a million reorder tied transactions, and that is enough to move AUPRC in
  the third decimal. The column measures tie-breaking, not a change in the
  model.
- **The pool build is not bit-reproducible.** The same seed's full-fold
  AUPRC was 0.8056 on a first run and 0.8049 on the committed run, with
  the same code apart from two added output fields. The committed run is
  the record.

## What it means for the backlog

- F29 closes. Its question is answered, and the answer is the degeneracy
  already on record, measured at four sample sizes.
- The finding that matters for Phase 2 is the one F94 and F25 already
  carry: the continuous formulation leaves the optimizer nothing to do.
  The cardinality-constrained formulation is where the optimizer has work.
