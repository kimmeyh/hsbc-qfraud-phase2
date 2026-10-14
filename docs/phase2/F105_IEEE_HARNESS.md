# F105: The Experiment 2 Harness on IEEE-CIS (Built, Audited, No Score)

**Sprint 26 Task G**, 2026-10-14. Zero metered seconds. Code:
`experiments/phase2/src/ieee_harness.py`, tested by
`experiments/src/test_ieee_harness.py`. Evidence:
`experiments/phase2/results/f105_pilot.json` (one fold, 10% sample) and
`experiments/phase2/results/f105_full_audit.json` (three folds, full
data), both tag SIM.

**No model score is reported, here or in either file.** F105's card says
none is until F102 names Experiment 2's preregistration entry. The harness
fits one model per fold only to time it, and a test scans the whole
module for any scoring call.

**Who reads this**: the team lead, and whoever writes Experiment 2's
section 6 entry.

## Bottom line

1. **The harness is built and every audit passes on the full data.**
   Three rolling-origin folds (evaluation months 4, 5 and 6, each trained
   on every earlier month) over 590,537 rows after exact duplicates are
   removed. On every fold: the entity key `card1_addr1_(day - D1)` reaches
   no feature column; the 22 aggregate columns do not move when the
   evaluation rows' own values are scrambled; the frequency-encoded
   columns equal a recomputation from training rows alone; and a
   classifier cannot tell two random halves of the training window apart
   (AUC at most 0.55). **Measured**: `f105_full_audit.json`, `folds[*].audits`.


   | Evaluation month | Train rows | Eval rows | Key columns | Aggregates moved | `*_freq` mismatched | Random-halves AUC |
   |---|---|---|---|---|---|---|
   | 4 | 410,600 | 85,302 | 0 | 0 of 22 | 0 | 0.500 |
   | 5 | 495,902 | 86,524 | 0 | 0 of 22 | 0 | 0.499 |
   | 6 | 582,426 | 8,111 | 0 | 0 of 22 | 0 | 0.499 |

   Month 6 is a partial bucket at the end of the file (8,111 rows), so its
   fold is about a tenth the size of the others; Experiment 2's entry
   should say whether it counts as a fold.
2. **The data drifts more than Phase 1's adversarial control can remove.**
   The control drops the feature that best separates early from late
   training rows, up to 20 times. On every fold it stops at that cap with
   early-versus-late AUC still 0.945, 0.888 and 0.887 (months 4, 5, 6),
   far above its 0.60 target; 181-183 of 227-231 features remain. Phase
   1's own IEEE-CIS run recorded the same three values
   (`experiments/results/ieee_classical.json`, `item4_controls`), which
   cross-checks the harness against Phase 1. **Measured.** Experiment 2's
   entry must decide how to treat it before any score is read: a higher
   cap, dropping features by group, or reporting the drift as a stated
   limit. **Inferred.**
3. **A full run is cheap.** Load 18 s; per fold 22-24 s of features,
   45-51 s of aggregate audit, 4.4-5.9 minutes of controls and 8-11 s of
   model fit. About 19 minutes for three folds. **Measured**: `timings_s`.

## What the harness does

- **Folds**: `ieee_splits.rolling_origin_folds`, Phase 1's splitter,
  unchanged, with its hard leakage assertion run on every build.
- **Entity key for aggregation only**: Phase 1's `IEEEFeaturePipeline`
  computes the key, fits the UID aggregates on training rows and drops the
  key. `audit_entity_key_not_a_feature` checks no column is a one-to-one
  encoding of it.
- **Aggregate audit**: scramble the evaluation rows' transaction values and
  rebuild; a `uid_*` column that moves was fitted on evaluation rows.
  `*_freq` columns are recomputed from training rows and compared exactly,
  because their sources are the key's own inputs, which the scramble
  leaves fixed (code review finding 7). There are no graph features.
- **Time-consistency selection and adversarial validation**: Phase 1's
  `ieee_controls`, inside the training fold only.
- **Random-halves check**: the plan's gate before any cross-window
  adversarial result is read; at most 0.55.
- **Client-mean post-processing**: each prediction replaced by its
  entity's mean prediction over the evaluation fold, from predictions only.

Each audit is shown to fire on an injected leak in the tests: aggregates
refitted on evaluation rows, frequency tables refitted on evaluation rows,
the key added as a feature, and a feature that identifies the random half.

## Limits

- A harness, not an experiment: Experiment 2's question, arms, metric and
  multiplicity belong to its section 6 entry, which does not exist yet.
- The fit used to time each fold is Phase 1's LightGBM configuration,
  carried from ULB as a hypothesis (`run_ieee.py`), not tuned for IEEE-CIS.
