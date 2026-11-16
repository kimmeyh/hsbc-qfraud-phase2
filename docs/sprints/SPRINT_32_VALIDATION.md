# Sprint 32 Manual Validation

**Sprint**: 32
**Branch**: `feature/20261108_Sprint_32` | **PR**: #116 (draft)
**Scope**: F181 (A), F194 (B), F188 (C), F185 (D), F178 (E), the F150
request draft (F) and the F111 feedback draft (G). Issues #110-#115 and
#117, all closed.
**Metered seconds**: 0. No device, Braket or other paid service was
called.

This file is the durable copy. The same items are listed to the screen at
handover: a pointer to a file is not a handover.

## Actions for the team lead

- **A1. Answer D4**: close F25's IEEE-CIS design after F188, or keep it
  on HOLD. Recommendation: 2 (keep on HOLD; F188's check becomes a
  condition of any device proposal).
  `D:\Data\Harold\github\hsbc-qfraud-phase2\docs\sprints\SPRINT_32_DECISIONS.md`
- **A2. Review the F150 request draft** (gitignored, not sent). Decide
  whether the optional Tier 1 paragraph in its first line goes into the
  email. It says our Tier 1 does not refuse fraud data, which questions
  the paper's headline, so it is left to you.
  `D:\Data\Harold\github\hsbc-qfraud-phase2\docs\spectra_package\F150_CONSTRUCTION_REQUEST_DRAFT.md`
- **A3. Review the F111 feedback draft** (gitignored, not sent).
  Suggestion 4 gains the tuned-CatBoost figure. Your suggestions are
  numbered 1, 2, 3, 4, 6; renumber 6 to 5 if 5 is not coming back.
  `D:\Data\Harold\github\hsbc-qfraud-phase2\docs\loke_package\F111_FEEDBACK_DRAFT.md`
- **A4. Judge the learning documents' Sprint 32 changes**: do the new
  F185 and F188 claims read as intended? In the plain-terms version (each document's new change-list entry is dated 2026-11-10):
  section 2 (last claim), section 6 (last claim and "What this means"),
  section 7 (the Sprint 32 part) and section 8 (its "In short").
  `D:\Data\Harold\github\hsbc-qfraud-phase2\docs\learning\ML QML and QC Understandings about Quantum Advantage - Laymen terms.md`
  The two expert versions carry the same results in more detail (ML
  section 2 and 7; QC bottom line, sections 3, 5 and 6):
  `D:\Data\Harold\github\hsbc-qfraud-phase2\docs\learning\ML QML and QC Understandings about Quantum Advantage - ML Expert.md`
  `D:\Data\Harold\github\hsbc-qfraud-phase2\docs\learning\ML QML and QC Understandings about Quantum Advantage - QC Expert.md`

## For information (no action needed)

---

## V1. Task A (F181): the device guard refuses Dirac-3

- `test_phase2_device_default.py` refuses a Phase 2 module that names
  `eqc_submit.DIRAC_3` or passes `'dirac-3'` to `eqc_submit.device(`,
  with or without a `# device named:` reason. Proven red (3f418b0).

## V2. Task B (F194): the refusal gate measures branches

- `.coveragerc` sets `branch = True`; CI's diff-cover step passes
  `--branch-coverage`. A one-line `if bad: raise` whose raise never runs
  now fails the gate. The three `REFUSING` print prefixes (`rf"`, `fr"`,
  `F"`) are read; `: raise` inside a string is not. Each proven red
  (5027f4f, c692eac).
- CI's push job, one run each: 8m30s before, 8m05s after, inside its 12
  minutes.

## V3. Task C (F188): the rounding test

- `docs/phase2/F188_ROUNDING.md`; results
  `experiments/phase2/results/f188_rounding.json` and
  `experiments/phase2/results/f188_rounding_delivered.json`.
- The check fired: 7 exact-size cases, every gain kept unrounded and lost
  at R = 2.
- Registered reading: "kept" at R = 200 on 42/free and 43/free, by gains
  the rounding made. Amendment's reading: worse than greedy on all six
  at R = 200. The decision this leaves is D4.

## V4. Task D (F185): a cost-weighted alert budget

- `docs/phase2/F185_COST_BUDGET.md`; result
  `experiments/phase2/results/f185_cost_budget.json`.
- IEEE-CIS month 4: ranking by score times amount catches about four
  times the fraud dollars of ranking by score, at the same 427 alerts,
  on every seed. Frauds caught fall on every seed of both datasets. ULB:
  no reliable difference. The scores are uncalibrated; the result holds
  for these scores only.

## V5. Tasks E, F and G: documents

- E: the three learning documents carry a Sprint 32 version (ce2c317).
  `test_learning_docs.py`, its red proofs and `test_us_english.py` pass
  on them.
- F: the F150 draft names the paper's title (checked against
  `docs/references.md`) and adds Sprint 31's SPECTRA result. Sprint 32's
  results are not about SPECTRA, so none is added.
  `scripts/outward_readability.py` finds internal tokens only in the
  note above the email.
- G: the F111 draft's suggestion 4 adds F166's tuned CatBoost on the
  same split and seeds. Same readability result.

## V6. Phase 5 checks

- The fresh-eyes review of F188 and F185 (23 observations) was applied
  in caa5106 and bcf67ad.
- The local suite run in parallel had 9 failures from memory pressure
  (MemoryError and crashed workers). The same 9 files run serially
  passed.
- CI's full job (every test and red proof) was green on bcf67ad. Its
  result on the handover HEAD is checked at Phase 7.0.
- Dependency scan (`pip-audit` on `experiments/requirements-lock.txt`):
  no known vulnerabilities.

## V7. For the retrospective

- `update_sprint_status.py --start-task X --estimate N` did not start
  the timer when an estimate was already set, so A's 1 minute is
  understated. F's and G's 3 and 2 minutes may be understated too.
- B and C ran only their own tests before pushing, so two CI reds
  (`test_ci_workflow.py`, the missing `LONG_RUN`) reached CI.
- One F188 red proof was vacuous until CI's full job found it.
- Commit 3520a0f carries Task C's document with Task D's result.
- The parallel local suite runs out of memory on this machine.
