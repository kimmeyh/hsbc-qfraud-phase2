# F114: the plug-in ceiling on ULB and IEEE-CIS

Sprint 31 Task E (#97), 2026-11-05. Zero metered seconds. The entry is
F108 in `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6: the
F114 amendment and the F114 re-run amendment of the same day (Sprint 31
D11 option 1), each committed before the fits it governs. Figures below
are in `experiments/phase2/results/f114_real_ceiling_lr05.json` (stage
2), `f169_plugin_bins_lr05.json` (stage 1) and `f114_real_ceiling.json`
(the first run, kept as recorded).

## BLUF

**Ceiling estimates are reported for both datasets, each with a
calibration warning, and the ULB figure should not be relied on.**

- The first run, at learning rate 0.1, failed its shuffled-label check
  and did not fit ULB on any of nine seeds. Under D11 the estimator was
  re-validated at learning rate 0.05 on F108's simulator and passed on
  5 of 5 seeds; F114 then re-ran.
- The re-run's shuffled-label check **passed by 0.00001**: estimate
  0.00118 against a test fraud rate of 0.00167, margin 0.0005.
- **ULB**: plug-in estimate 0.00016, 95% interval 0.00010 to 0.00022,
  against the model's own achieved error of 0.00111. The plug-in is
  about a seventh of an error the model actually achieves, so the model
  is overconfident on the test rows and the plug-in is too low as a
  Bayes-error estimate. Calibration warning.
- **IEEE-CIS month 4**: plug-in estimate 0.0254, interval 0.0232 to
  0.0276, against an achieved error of 0.0293. Calibration warning.

## Results (Measured)

Stage 1, `lgbm_lr05` on F108's simulator (`f169_plugin_bins_lr05.json`):
recovered on 5 of 5 seeds on the main arm, and on 5 of 5 on the flip
and reference arms. It passes F169's rule, so stage 2 ran.

Stage 2 (`f114_real_ceiling_lr05.json`), ten seeds each (42-51; seed 42
took 0.06 min on ULB and 0.08 min on IEEE-CIS, so no cut):

- Shuffled-label check, ULB seed 42: estimate 0.00118, test fraud rate
  0.00167, margin 0.0005: pass.
- ULB, 95 test positives per seed: estimate 0.00016 [0.00010, 0.00022];
  achieved error 0.00111 [0.00062, 0.00161]; consistency gap -0.00095
  [-0.00140, -0.00051]; test AUPRC 0.623 [0.503, 0.743].
- IEEE-CIS, 2,962 test positives: estimate 0.0254 [0.0232, 0.0276];
  achieved error 0.0293 [0.0274, 0.0312]; consistency gap -0.0038
  [-0.0058, -0.0019]; test AUPRC 0.478 [0.446, 0.509].

Training AUPRC, reported by the re-run amendment so a collapse shows
(`rows[].train_auprc`): ULB 1.0 on seven seeds, and 0.887 (seed 44),
0.624 (seed 50) and 0.925 (seed 51). Those three seeds also have the
lowest test AUPRC (0.321, 0.365 and 0.543) and achieved errors at or
above the test fraud rate. IEEE-CIS 0.662 to 0.665 on every seed.

## Reading

- **What the entry lets us say**: with the check passed, each interval
  is "the plug-in ceiling estimate, error metric, under the plug-in's
  calibration assumption". It is not a recall ceiling. Both consistency
  gaps exclude 0, so both figures carry the calibration warning the
  entry sets.
- **ULB**: the warning is large. A Bayes error may sit below an
  achieved error, but a plug-in this far below it on every seed is what
  an overconfident model gives. Three seeds still fit badly at 0.05.
  Inferred, not tested: the estimator is still unstable on about 290
  training positives. The ULB figure is reported as the entry requires and is
  not a usable ceiling.
- **IEEE-CIS**: the gap is smaller relative to the figure (about 13%).
  The plug-in says the model's own error of 0.0293 could fall to about
  0.025 on these features, if the probabilities were calibrated.
- **The check passed by a hair.** At 0.00049 against a 0.0005 margin, a
  slightly different permutation could fail it. The entry fixes one
  draw, so the pass stands, but it is weak support for "the method
  transfers".

## Defect found and repaired (Sprint 31 D13)

The re-run first kept the first run's record name, so it replaced the
first run's ULB score files for seeds 42-50 under
`experiments/phase2/predictions/` (gitignored, so no commit held them).
Repaired on 2026-11-05 under D13:
- `outcome_record.save_test_scores` never replaces a file now: a name
  held by different bytes gets the next free name (`_v2`, `_v3`, ...).
- The re-run records as `f114lr05_<dataset>`. It was repeated under that
  name; every figure matched the earlier re-run, and only the record
  names, score paths and timings changed (seed 42 on ULB 0.06 minutes,
  against 0.05). `f114_real_ceiling_lr05.json` was replaced with the
  reason recorded in its provenance block.
- The first run's nine files were restored from a scratch rebuild whose
  SHA-256 values match all nine recorded ones.

## What this changes

- F114 has its first real-data figures. The IEEE-CIS figure is the one
  to carry forward, with its warning; the ULB figure is not.
- A calibrated plug-in is the next step if a ULB ceiling is still
  wanted. Sprint 28's isotonic-calibrated plug-in
  (`experiments/phase2/src/f114_calibrated_plugin.py`) is the existing
  starting point. That is a backlog item, not this sprint's.
