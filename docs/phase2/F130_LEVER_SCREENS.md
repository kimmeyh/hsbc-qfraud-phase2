# F130: proxy screens for F124 ranks 3, 5 and 6

Sprint 27 Task E, 2026-10-18. Zero metered seconds. Every figure below is
in `experiments/phase2/results/f130_levers.json` (five seeds, 42-46),
except the ULB comparator check, which is in
`experiments/phase2/results/f130_ulb_hgb_check.json`. The generator is
`experiments/phase2/src/f130_levers.py`. The decision rule was set before
the runs (Phase 2 draft section 2b; the plan): a lever **moves AUPRC** if
its mean paired delta against the seeded dct pool is at least 0.005 and
the 95% bootstrap interval over the seed deltas excludes zero. It **beats
HGB** if its interval against HGB lies above zero.

## BLUF

**No lever beats HGB on any SPECTRA dataset.** Two levers move AUPRC up
against the dct pool: KNN weak learners (rank 3) on oilgas and telecom,
and the phase block (rank 5) on telecom and steel. Pool-size caps (rank 6)
move nothing and are rejected. On ULB, KNN moves AUPRC up by +0.0095, but
the "beats HGB" result there is **not a finding**: the HGB comparator on
ULB is unstable under every setting tried (mean test AUPRC 0.22-0.52,
single seeds 0.06-0.70), so it is not a valid reference. The cause is
unverified.

## Results (Measured)

**Rank 3, KNN weak learners** (delta against the dct pool, then against
HGB):
- oilgas: AUPRC 0.8513, +0.0124 [+0.0101, +0.0147]; against HGB -0.0226
  [-0.0260, -0.0197]. **Moves up.**
- telecom: 0.7573, +0.0246 [+0.0086, +0.0409]; against HGB -0.1096
  [-0.1249, -0.0943]. **Moves up.**
- ULB (`free`, k = 13, schedule 2, 78 learners, full split): 0.7772,
  +0.0095 [+0.0015, +0.0165]. **Moves up.** The comparison against HGB
  is void; see below. **Restated 2026-10-22 (F151, Sprint 28 Task A)**:
  against the stable HGB (`l2_regularization=1.0`), this cell is BELOW
  HGB by 0.027 [-0.046, -0.008]; `docs/phase2/F151_HGB_COMPARATOR.md`. This setup is not the EvidenceBasedDB record's
  (SMOTE, 70/30, 10 seeds), so 0.7772 is not a test of its 0.8108 claim.

**Rank 5, the phase block** (cyclic columns phase-encoded and whitened on
training rows, pool rebuilt):
- telecom: 0.7695, +0.0369 [+0.0238, +0.0520]; against HGB -0.0974
  [-0.1097, -0.0753].
  **Moves up.**
- steel: 0.9072, +0.0052 [+0.0008, +0.0099]; against HGB -0.0577
  [-0.0783, -0.0332]. **Moves up, at the threshold.**
- oilgas: -0.0007 [-0.0017, +0.0004]. **Rejected.**
- Caveat on every phase cell: `in_pocket` is predictable from the phase
  features at AUC 0.93-0.99 (`docs/F101_IN_POCKET_PROVENANCE.md`), so a
  rank 5 gain may be a gain on the segment flag.

**Rank 6, `weak_cls_pair_count`** (30, 60 and 90 on every dataset, plus
119 on steel and telecom; team lead D3):
- No cell reaches the 0.005 threshold. The largest is steel at 30 pairs,
  +0.0048 [+0.0036, +0.0058]: a real but sub-threshold gain. Every cap is
  **rejected**.
- **The cells at the cap are identity controls, not levers.** The cap is
  eqc-models' `topNPairs` limit d(d-3)/2: 119 for 17 features (steel,
  telecom) and 90 for 15 (oilgas). So `pairs_119` on steel and telecom
  and `pairs_90` on oilgas build the default pool. Each reproduces the
  baseline exactly (delta 0.0000, interval [0, 0]), which shows the new
  opt-in `pair_count` leaves the default build unchanged.
- The card named 100, 200 and 400 pairs. Those cannot be built: the cap
  is 90-119 on these datasets, and eqc-models asserts above it. The plan
  replaced them with 30, 60, 90 and 119 before the run.

## The ULB HGB comparator is invalid (Measured; cause unverified)

`ulb_full` reports KNN ahead of HGB by +0.4023, because HGB averaged
0.3748. A tree ensemble on the same 13 features should not trail a
78-learner pool by that much, so the comparator was checked after the run.
`f130_ulb_hgb_check.json` refits HGB on the same features and splits:
- default (early stopping on, 10-11 iterations): mean 0.3748, seeds
  0.13-0.61;
- early stopping off (100 iterations): 0.2186, seeds 0.20-0.25;
- learning rate 0.05, `max_iter` 300 (early stopping stops it at 11):
  0.5150, seeds 0.10-0.70;
- learning rate 0.05, 300 iterations, early stopping off: 0.3815, seeds
  0.06-0.57.

More iterations do not fix it, so early stopping is not the whole cause.
Inferred: HGB's binned, unweighted fit is unstable at ULB's positive rate
(0.167% of test rows) on these whitened features. That is not verified. F108 found
the same failure class: default HGB scored AUPRC 0.01-0.03 against a known
1.0 on a rare-event reference arm. **Risk, unverified:** HGB is a lane in
F106 and F109; their readings on rare-positive data should not lean on HGB
alone.

## Reading

- Ranks 3 and 5 are worth carrying into a device screen only as
  improvements to the CVQBoost pool. Neither closes the gap to HGB on
  SPECTRA (0.023-0.110 short).
- Rank 6 is rejected for AUPRC. Its other claim, a cheaper device fit
  from a smaller pool, was not measured here.

## Limits

- Five seeds; intervals are percentile bootstrap over seed deltas, so
  they are narrow and not a test across datasets.
- The ULB comparator check was designed after the run. It changes no
  recorded row and no decision on a SPECTRA cell.
- `generator_sha256` in `f130_levers.json` records the generator as run.
  Later edits (the ULB check mode and a fix that keeps a dataset's
  baseline on a partial rerun) did not touch the recorded run. Its rows
  hold a baseline for every dataset and seed (15 rows).
