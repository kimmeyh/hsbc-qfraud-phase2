# Experiment 4 (F111): the CVQBoost-KNN lane, the pilot

Sprint 28 Task D (#51), 2026-10-22. Zero metered seconds. The entry is
`experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "Experiment 4",
committed before its harness (`e07aa84`). Every figure below is in
`experiments/phase2/results/f111_loke_protocol.json`. Code:
`experiments/phase2/src/f111_loke_protocol.py`; test:
`experiments/src/test_f111_loke_protocol.py`. Evidence tag `SIM`.

## BLUF

**The pilot projects the run at about 825 minutes, far over the
entry's 120-minute cap. Under the entry's size rule, the run did not
start, and the seed count goes to the team lead at Manual Validation.**
There is no Experiment 4 result yet. This document records the pilot,
which the entry requires to be reported whatever happens next.

## The pilot (Measured, `SIM`)

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

## Why the run is this slow

The weak learners are KNN with k = 15 on all 30 columns, and schedule 2
full-pair gives 465 of them. Each learner predicts every training row to
build H, and every scored row too. Prediction is the cost. The pool
build itself is small (about 5 s at 10%). Inferred: the cost grows with
training rows times query rows, which is why the full-size projection is
about 100 times the 10% pilot.

## What the team lead decides (Manual Validation)

The entry says: run if the projection is at most 120 minutes, otherwise
the seed count goes to Manual Validation. The options and their projected
serial times are in the sprint's validation document. Any seed count
other than the entry's is recorded as a dated amendment to the entry
before the run starts.

## What was not done

- No seed was run at full size. `run` refuses unless the pilot clears
  the cap, and it did not.
- No timing was taken with other work on the processor. The pilot ran
  alone, after Experiment 6's timing had finished.
