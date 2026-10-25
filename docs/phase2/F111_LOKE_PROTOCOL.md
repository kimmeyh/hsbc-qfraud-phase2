# Experiment 4 (F111): the CVQBoost-KNN lane, the result

Sprint 28 Task D (#51), 2026-10-22 (pilot) and 2026-10-23 (run). Zero
metered seconds. The entry is
`experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "Experiment 4",
committed before its harness (`e07aa84`). Every figure below is in
`experiments/phase2/results/f111_loke_protocol.json`, except the run's
wall clock, which the file does not record (marked where used). Code:
`experiments/phase2/src/f111_loke_protocol.py`; test:
`experiments/src/test_f111_loke_protocol.py`. Evidence tag `SIM`.

## BLUF

- **Primary result: the protocol does not measurably change the KNN
  lane.** KNN AUC-PR under the source protocol (A) minus under ours (B):
  -0.014, 95% interval [-0.046, +0.019], 10 paired seeds. The interval
  includes zero.
- **The lane is not consistent with the published 0.8108.** Its mean
  under A is 0.760, 0.051 below; the entry's tolerance is 0.03.
- **The stable HGB beats the KNN lane under both protocols**: by 0.082
  [0.061, 0.104] under A and by 0.033 [0.014, 0.053] under B.
- **The protocol does move HGB**: A minus B is +0.035 [+0.008, +0.062].
  A differs from B in more than duplicates (more training rows,
  resampling, a different split), so this run cannot say which part
  moves it.
- **Duplicates**: under A, 267 to 329 evaluation rows per seed (mean
  303.5) have an exact copy in the training rows. Under B, none.

## Results (Measured, `SIM`)

Seeds 42-51, both protocols, both lanes; every row carries an outcome
block. The rows record 82.5 minutes of lane time (the sum of every
row's `seconds`; preparation is not recorded), against the pilot's
projection of 824.6 (see "The projection was wrong").

- **KNN lane AUC-PR**: A mean 0.760 (range 0.683-0.828), B mean 0.774
  (0.707-0.831).
- **HGB AUC-PR** (F151's stable setting): A mean 0.842 (0.788-0.881),
  B mean 0.807 (0.762-0.849).
- **Sensitivity, SMOTETomek 0.05 under A** (seeds 42-44, reported, not
  decisive): KNN 0.774, HGB 0.860.
- **Team lead's approval**: the run was over the entry's cap and ran
  under the dated amendment and the recorded `over_cap_approval`
  (Sprint 28 Manual Validation DV2).

## Reading

- **Duplicates did not lift this lane (Inferred).** About 300
  evaluation rows per seed have a twin in training, yet the KNN lane is
  no higher under A. The weight solve keeps only 12 to 19 of the 465
  learners per row (`rows[].n_nonzero_weights`), so the vote is narrow,
  and why one exact match does not dominate it is **unverified**. Each
  kept learner votes over 15 neighbors on one or two columns, where an
  exact twin is one neighbor of 15; that is a candidate reason, not a
  measured one.
- **0.8108 is not reached with the settings recoverable from the paper
  and the code.** The paper's seeds cannot be recovered, and settings it
  leaves open (feature count, resampling ratio) may differ. This run
  cannot say which, so it does not claim the published value is wrong.
- **For a QML claim on ULB, the comparison that matters is against a
  stable classical model on the same rows**, and here the KNN lane is
  below it under both protocols.

## The projection was wrong

The pilot projected 824.6 minutes with F130's formula, which scales the
lane time by training rows times query rows. The rows record 82.5
minutes of lane time (each KNN lane 184-252 s), and the observed wall
clock, preparation included, was about 95 minutes (not recorded in the
result file; future runs record it). The formula overstated the cost
about 9 to 10 times. Inferred cause: scikit-learn's KNN on one or two columns
uses a tree search, whose cost grows close to rows times log rows, not
rows squared. The full run also shared the processor with the DV4
backfill, so its seconds are not timing evidence. A projection formula
that assumes brute-force search needs a check against a second pilot
size before it decides a run.

## The pilot (Measured, `SIM`, 2026-10-22)

Seed 42. The lane was timed on 10% of each protocol's rows. The data
preparation was timed at full size.

- **Protocol A** (Loke et al.'s: no deduplication, 70/30 stratified,
  SMOTETomek at 0.02):
  - lane at 10%: 20.7 s (pool build 5.1, H on train 10.0, H on the scored
    rows 4.7)
  - full-size preparation: 18.8 s
  - resampled training set: 344 positives and 199,020 negatives before,
    3,974 and 199,014 after
  - **326 evaluation rows are exact duplicates of training rows**. That
    is the entry's duplicate count, reported as required. Protocol A does
    not deduplicate.
- **Protocol B** (ours: deduplicated, 60/20/20, no resampling):
  - lane at 10%: 22.3 s (4.3, 9.7, 5.9)
  - full-size preparation: 2.1 s
  - no evaluation row duplicates a training row
- **Projection.** This is F130's lane formula: the pilot time scaled by
  the ratio of training rows times the ratio of query rows. It is about
  100 times for each protocol, because the KNN learners compare every
  query row with every training row. The full-size preparation is added,
  and the total is multiplied by the run's seed counts (13 for A, 10 for
  B).
  - per seed: A 34.8 min, B 37.2 min, so about 72 min per seed pair
  - entry as written (10 seeds per protocol, plus 3 sensitivity seeds on
    A): **824.6 min**, against the cap of 120
- The projection is an inference from the pilot and the formula, not a
  measurement.

The pilot's reading of the cost ("each learner compares every query row
with every training row") was the inference the run disproved; see "The
projection was wrong".

## What was not done

- The paper's own seeds: unrecoverable (the code draws them at random).
- Which part of protocol A moves HGB (duplicates, training size,
  resampling or split): one protocol against another cannot separate
  them.
- No device: the lane was solved classically on the Hamiltonian
  eqc-models sends.
