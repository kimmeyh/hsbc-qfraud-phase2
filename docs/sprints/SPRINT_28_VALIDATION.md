# Sprint 28 Manual Validation

**Sprint**: 28, Experiment Entries First, Then Their First Measurements
**Branch**: `feature/20261019_Sprint_28` | **PR**: #46 (draft)
**Scope**: F154 (F), F151 (A), F152 (B), F153 (C), F111 (D), F110 (E),
F114 (G), F150 request (H), F115 (I), F13 (J), F146 (K), pypdf (L).
Issues #47-58.
**Metered seconds**: 0. No Dirac, Braket or other paid service was called.

This file is the durable copy. The same items are listed to the screen at
handover: a pointer to a file is not a handover.

---

## V1. Task F (F154): where each model wins, and the standing rule

Read `docs/phase2/F154_WHERE_MODELS_WIN.md`.

- **New standing rule, in force from this sprint**: every Phase 2 result
  holding a test score carries an outcome block (confusion counts at the
  0.5% alert budget, and the per-row scores with their SHA-256).
  `experiments/phase2/src/outcome_record.py`; enforced by
  `test_outcome_record_required.py`, which exempts the 30 files written
  before the rule. Written into `docs/SPRINT_PROCESS.md` and `CLAUDE.md`.
- **Result: null.** 66 model pairs, 132 subset cells. The in-subset
  difference alone fired on 73 cells; the interaction (the rewritten
  rule) fired on none at the Bonferroni level.
- Both models flag at least 776 of the 950 rows either flags; the most
  rows one model catches alone is 34.
- The F32 `cvqboost_hw_mixed` family was excluded: it used the
  undeduplicated split.

## V2. Task A (F151): why the ULB HGB comparator was unstable

Read `docs/phase2/F151_HGB_COMPARATOR.md`.

- **Cause found: HGB's default `l2_regularization=0`.** Setting 1.0 alone
  closes the spread under the plan's rule (mean 0.804, SD 0.022, range
  0.055, against the 0.816 reference). The default: mean 0.375, SD 0.170.
- F130's voided ULB "beats HGB" is restated: both proxy variants sit
  below the stable HGB (KNN -0.027, dct -0.036, intervals excluding zero).
- The stable HGB is the reference in B, D and G.

## V3. Task B (F152): Experiment 2 on IEEE-CIS

Read `docs/phase2/F152_EXP2_RESULT.md`.

- **P1 holds**: XGBoost above logistic regression on months 4 and 5
  (97.5% intervals exclude zero).
- **P2**: XGBoost improves from month 4 to month 5 (+0.038, interval
  [+0.010, +0.069]). This mixes drift with one more month of training.
- LightGBM and the stable HGB both beat Phase 1's XGBoost configuration on
  every month (secondary, uncorrected).
- Every claim carries the stated limit: trained on drifting features.

## V4. Task C (F153): Experiment 3's design

Read `docs/phase2/F153_EXP3_DESIGN.md`.

- **The design fails its committed falsifier**, on all six instances: the
  gap to the floor is 0.0016-0.0026 (below 0.01), and both resolution
  checks fail. No device quote is carried forward; F25 stays parked.
- No ridge weight met the 10% data-share rule; the fallback (0.002) was
  used, as written. The rule itself was ill-posed: |objective| is close
  to 1 at every weight, so a data term near 0.002 could never reach 10%.
- Greedy equals the best selection found everywhere; SCIP hit its 300 s
  cap on all six without improving on it.
- **The two resolution checks disagree in kind.** QCi's A7 reading (max/min
  coefficient ratio) is about 2 and passes; the pairwise share (3-6%) and
  F104's gate fail. Which one the device honors is unverified.

## V5. Task D (F111): Experiment 4

Read `docs/phase2/F111_LOKE_PROTOCOL.md`.

- **No result yet. The pilot projects the run at about 825 minutes, far
  over the entry's 120-minute cap.** Under the entry's size rule, no seed
  ran at full size and the seed count is Decision DV2 below. The task
  tracker marks D finished because the pilot is the deliverable the
  size rule calls for; issue #51 stays open until the run is decided.
- About 72 minutes per seed pair (A 34.8, B 37.2), serial. The cost is
  KNN prediction: 465 learners, each predicting every row.
- Protocol A (the source's) leaves 326 evaluation rows that are exact
  duplicates of training rows. Protocol B leaves none.
- The library's full-pair builder needs `fork`, which Windows lacks. The
  new `full_pair_pool.py` builds the same learners serially; it was
  checked equal under `fork` in WSL (the only use of that venv), and
  Linux CI repeats the check.

## V6. Task E (F110): Experiment 6

Read `docs/phase2/F110_SCALING.md`.

- **P1 is false at both sizes.** The pool build is the largest part
  everywhere, but its slope in rows is about 1.4 (intervals [1.35, 1.45]
  at 91 variables, [1.38, 1.49] at 833), above the predicted [0.7, 1.3].
- **P2 holds at 833 variables** (solve flat, about 0.35 s). At 91
  variables it fails under the rule: 9 of 20 solves were below the
  timer's resolution, so the interval is too wide to read.
- A serial 833-variable build at full rows takes about 13 minutes,
  close to the hardware plan's 735.4 s. That suggests the plan's build
  was serial too (inferred, unverified).
- Scaled to 150,000 rows, the training is about 650 s at 833 variables,
  against the paper's 2 s. Not like for like, and the scaling is an
  inference from the slope.
- A timing defect was found after two rows and before any slope; the
  entry carries a dated correction and the two rows were discarded.

## V7. Task G (F114): a calibrated plug-in on F108's harness

Read `docs/phase2/F114_CALIBRATED_PLUGIN.md`.

- **Does not recover: 2 of 5 seeds on the main arm** (4 needed), the same
  as F108's default plug-in. **F114 stays blocked**; the 90-minute
  real-data run was not spent.
- Calibration does not move the estimate (under 0.0002 on every seed).
  Every seed overestimates the Bayes error, by about 3% to 13%.
- The amendment named F151's setting (`l2_regularization=1.0`) and not the
  plan's candidate `early_stopping=False`, because F151 found l2 alone
  sufficient.

## V8. Task H (F150): the construction request to the SPECTRA authors

- Draft: `docs/spectra_package/F150_CONSTRUCTION_REQUEST_DRAFT.md`
  (gitignored; the rule was written and checked before the file).
- Eleven items, each a choice F103 fixed itself, checked against
  `f103_tier1.py`, plus the release's phase jitter and the undefined
  joint ratio.
- **Your action**: check the paper's exact title (this repository records
  only its arXiv number), then send, change or discard.

## V9. Task I (F115): integer cost scaling, stated correctly

Read `docs/phase2/F115_INTEGER_COST_SCALING.md`.

- Fit from code: `vars^0.75 x levels^0.52`, R^2 0.953. Cost is sublinear
  in variables at a fixed level budget.
- The hardware plan (FINAL) is not edited. Its wrong sentence went to QCi
  in the plan's PDF; the optional correction paragraph is in Task K's
  reply draft.

## V10. Task J (F13): the PoC plan skeleton

Read `docs/phase2/PHASE2_POC_PLAN.md`.

- Calendar from your screenshot of the program roadmap: PoC 17 Nov 2026 to
  28 Feb 2027; review and close 1 Mar to 30 Apr 2027.

## V11. Task K (F146): QCi records and the reply draft

- **Your QQ: were the three 2026-10-21 QCi emails incorporated? No, not
  until today.** The 2026-10-21 update recorded only the 2026-10-20
  reply. Two later replies were missed and are now in
  `docs/phase2/DIRAC_UNDERSTANDINGS.md` section 4:
  - P1 (our reading of the Hamiltonian) is confirmed by QCi's eqc-models
    contact. P1 is closed.
  - The integer solver now has 954 levels on both devices. Dirac-3S moves
    to 9,980 levels "in the coming weeks".
- The planned P1 draft was dropped (P1 is answered). One reply draft:
  `docs/qci_package/F146_QCI_REPLY_DRAFT_20261022.md` (gitignored). It
  accepts the review offer, asks whether the continuous solver also
  accepts 954 variables and when 9,980 is live, and carries the optional
  F115 paragraph.
- The stale `.gitignore` line cite now names the rule.

## V12. Task L: pypdf 6.20.0 to 6.21.1

- Three advisories cleared; lock header dated; no tracked PDF rebuilt.
- Only one venv exists on this machine (`.venv`). The WSL venv
  (`/root/eqc-venv`) does not match the lock (numpy 2.5.2 against
  1.26.4) and has no imbalanced-learn, pyscipopt or pytest. It was used
  this sprint only for one equality check (V5), not for any result.

---

## Decisions for you

**DV1. F155 probe size** (the probe itself needs its own per-block
approval later; `qpu_cost_model.quote` gives 3-4 s for either, a floor):

1. 955 variables, just above the new 954 integer limit
2. 987 variables, F143's own size

**DV2. Experiment 4 (F111) seed count.** Serial projections from the
pilot. Any count other than the entry's goes in as a dated amendment to
the entry before the run starts. The run goes in the background after
Manual Validation, alone on the processor.

1. As written: seeds 42-51 on both protocols plus the 0.05 sensitivity
   on seeds 42-44, about 825 min
2. Seeds 42-51 on both protocols, sensitivity dropped, about 720 min
3. Seeds 42-44 on both protocols, sensitivity dropped, about 216 min
4. No run in Sprint 28; F111's run goes to Sprint 29 planning

**DV3. The QCi reply draft**
(`docs/qci_package/F146_QCI_REPLY_DRAFT_20261022.md`). Sending is yours.

1. Keep the optional F115 paragraph
2. Cut the optional F115 paragraph

## Notes for the retrospective

- K and H timers record about 1 minute: each was started at its commit,
  not when its work began.
- E (198 min) and D (180 min) actuals include time while other tasks
  ran beside them; they are wall clock from start, not effort.
- E's method: 9 of 20 solves at 91 variables were below the timer's
  resolution. A timing entry needs repeated solves or a finer timer
  when the solve is milliseconds.
- E's first timing version subtracted H as well as J and clamped the
  solve to zero; found after two rows, corrected by a dated entry
  note before any slope.

## Your actions (no decision needed from me)

- Check the SPECTRA paper's exact title, then send, change or discard the
  F150 draft (V8).
- Send the QCi reply when ready (DV3).
