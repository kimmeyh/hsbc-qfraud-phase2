# F154: Where Each Model Wins, on the Stored ULB Predictions

**Sprint 28 Task F (#47).** Zero metered seconds. Entry:
`experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F154", written
before any pairwise or subset count. Result:
`experiments/phase2/results/f154_confusion.json` (evidence tag `SIM`), from
`experiments/phase2/src/f154_confusion.py`.

## Bottom line

- **Null. No stored model is reliably better than another on either
  subset.** None of the 132 primary tests (66 pairs, 2 subsets) has an
  interaction interval that excludes zero. **Measured**: the
  `interactions_excluding_zero` field is empty.
- **The null survives the tie check.** With tied scores given a
  tie-neutral share instead of all being flagged, still none fires.
  **Measured**: `tie_neutral_interactions_excluding_zero` is empty.
- **The models catch almost the same frauds.** In every pair, both models
  flag at least 776 of the 950 test frauds (95 per seed, 10 seeds). The
  frauds one model catches and the other misses number at most 34 over
  all ten seeds. **Measured**: `pairs[].a_only_total`, `b_only_total` and
  `both_total`. Example: Dirac-3 hardware against XGBoost (30 features):
  2 against 26, with 787 caught by both.
- **For the ensemble question**: these files give an ensemble no subset to
  route on. This widens F113's finding (no CVQBoost-specific
  complementarity with XGBoost) to every stored pair. **Inferred**, from
  the two subsets tested here. The leading alternative not ruled out: a
  subset defined by something other than amount or day (for example a
  feature region) could still separate models. Testing that needs a new
  entry, with its subsets chosen before the run.

## What was compared

- **13 stored families**, each with all ten seeds (42-51, stratified
  protocol), from `experiments/results/predictions/` (read, never
  written). XGBoost, LightGBM, CatBoost and logistic regression at 13 and
  30 features; three CVQBoost proxy configurations; Dirac-3 hardware
  (`cvqboost_hw`); and the F32 mixed-pool hardware family.
- **One family is out of the pairs.** The F32 mixed-pool hardware files
  (`cvqboost_hw_mixed_6e69c57361c937d6`) were made on the split without
  deduplication (56,962 test rows, 99 frauds). Every other family uses the
  deduplicated split (56,746 rows, 95 frauds). Its labels match the raw
  split on all ten seeds, so its rows are not the others' rows and cannot
  be paired with them. **Measured**: `excluded_reason`. The entry said a
  family off the split is reported and left out, so the family size is
  66 pairs, not the 78 the entry estimated. Its outcome blocks and its
  table rows are still recorded.
- **Operating point**: the 0.5% alert budget on the test rows (284 of
  56,746). Recall in a subset is the share of that subset's frauds
  flagged.
- **Subsets**: amount (above the test fold's median `Amount`, or not) and
  day (`Time` below 86,400 s, or not).

## Why the test is the interaction

- **The plain in-subset difference fires on 73 of the 132 cells** at an
  uncorrected 95% level (`pairs[].in_subset_diff_secondary`). It fires
  because 42 of the 66 pairs differ overall (`overall_recall_diff`), and
  an overall difference shows up inside any subset. That is the defect the
  plan's threshold check found in the carded rule.
- **The interaction removes the overall difference.** It asks whether A's
  advantage inside the subset is larger than A's advantage outside it.
  That is the question an ensemble needs answered.
- **Correction**: Bonferroni over the family, m = 132, so each t interval
  over the ten seeds is at 99.96%. The closest cell to firing was the
  CVQBoost proxy (13 features) against logistic regression (30 features)
  on day 1: interaction +0.034, interval [-0.006, +0.074].

## Limits

- **Tied scores.** The entry flags every row tied at the cut. The CVQBoost
  proxy and F32 hardware families tie heavily, so they flag more rows than
  the budget: up to 81 extra rows for one proxy configuration (mean 47.8
  over seeds). **Measured**: `extra_rows_flagged_by_ties`. Their catch
  counts are inflated by those extra rows. The tie-neutral check gives
  tied rows a share instead, and the verdict does not change.
- **Two subsets only.** On ULB, amount and day are the only subsets with a
  referent. "The segments the proposal names" (the card's earlier wording)
  has none: `proposal.md` names no ULB segment.
- **Ten seeds and 95 frauds per seed.** One fraud moves a subset's recall
  by about 2-3 points, so a small subset effect is below what this
  design can see.
- **Stored predictions only.** Lanes that saved no per-row file (QSVM, B1,
  SPECTRA B4, Dirac-3S) are in the confusion table only, not in the
  pairs.

## The confusion table

430 rows: every operating point with a confusion count in
`experiments/results/results.json` (420 rows, 210 results at two
validation-chosen thresholds each) and in
`experiments/phase2/results/f142_dirac3s_verify.json` (10 rows). Each row
names its source file, arm, configuration hash, seed, evidence tag and
operating point. It is the `table` field of the result file. This
document does not restate it.

## The standing rule this task added

The team lead asked (2026-10-22) that every later experiment, ML or QML,
record these values. From this sprint on:

- `experiments/phase2/src/outcome_record.py` builds an outcome block:
  confusion counts at the alert budget, at the validation-chosen operating
  points where a validation fold exists, and at the experiment's own
  threshold, plus the per-row test scores saved with their SHA-256.
- `experiments/src/test_outcome_record_required.py` fails any new Phase 2
  result file that holds a test score without a block. The 30 scored files
  that predated the rule were exempt by name, and that list can only
  shrink; after the Sprint 28 DV4 backfill, 16 remain.
- The rule is in the Phase 2 draft (section 2, "Outcomes recorded"),
  `docs/SPRINT_PROCESS.md` and `CLAUDE.md`.

This result file carries a block for every family and seed (130), each
pointing at its stored prediction file and that file's SHA-256.
