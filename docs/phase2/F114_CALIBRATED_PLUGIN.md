# F114 gate: an isotonic-calibrated plug-in on F108's simulator

Sprint 28 Task G (#53), 2026-10-22. Zero metered seconds. The entry is
the dated amendment to "F108" in `experiments/phase2/PREREGISTRATION_DRAFT.md`
section 6, committed before the module existed (`36e8d1d`). Every figure
below is in `experiments/phase2/results/f114_calibrated_plugin.json`
(five seeds, 42-46); the one-seed pilot is `f114_calibrated_plugin_pilot.json`.
Code: `experiments/phase2/src/f114_calibrated_plugin.py`; test:
`experiments/src/test_f114_calibrated_plugin.py`.

## BLUF

**The calibrated plug-in does not recover the ceiling, so F114 stays
blocked.** On the main no-noise arm, the deciding arm, it is within the
margin on 2 of 5 seeds; the rule needs 4. That is the same count as
F108's default plug-in. On the main arm, calibration did not move the
estimate: the calibrated and uncalibrated plug-ins from the same model
differ by less than 0.0002 on every seed. On the other two arms it does
move some estimates (see Results).

## What ran

F108's generator, posterior, splits, seeds, arms and margin, imported
unchanged. Only the plug-in's model changed: F151's stable HGB
(`l2_regularization=1.0`), fit on 75% of the training rows, with
isotonic calibration fit on the held-out 25%. The same model's
uncalibrated plug-in is reported beside it. The noisy labels match
F108's row for row (the module draws the same random numbers F108 draws,
and the test checks it).

## Results (Measured, `SIM`)

- **Main arm (deciding)**: calibrated recovers 2 of 5, uncalibrated 2 of
  5. Every estimate is **above** the Bayes error: calibrated by about
  3% to 13%, uncalibrated by about 4% to 14%; the margin is 10%.
- **Noise arm**: calibrated 3 of 5, uncalibrated 4 of 5. F108's default
  plug-in recovered 5 of 5 here.
- **Zero-ceiling reference arm**: calibrated 0 of 5, uncalibrated 1 of 5.
  The calibrated estimates sit just above the 0.0005 absolute margin.
  F108's default plug-in recovered 5 of 5 here.
- **Run time**: under 11 s per seed.

## Reading

- **The gap is not miscalibration (Inferred).** Isotonic calibration on a
  quarter of the training rows leaves the main-arm estimate where it was.
  So the overestimate comes from what the model's probabilities rank and
  resolve, not from how they are scaled.
- **The variant is worse on the two arms F108's plug-in passed.** Two
  changes happened at once: the regularization and the smaller fitting
  set (75% of train). This run cannot separate them; the uncalibrated
  column isolates calibration only.
- **What would change the verdict** is a different estimator, not a
  re-scaled one. F108's document names the other candidates: a
  Bayes-error estimator that does not go through one model, and an HGB
  set for extreme imbalance.

## What follows

- F114 stays blocked. Its card records this result.
- No real-data ceiling run (ULB, IEEE-CIS) happens this sprint; the 90
  minutes the plan reserved for it are not spent.
