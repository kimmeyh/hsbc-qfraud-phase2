# Sprint 27 Manual Validation

**Sprint**: 27, Gates Before Reporting, and the Screens That Need No Device
**Branch**: `feature/20261018_Sprint_27` | **PR**: #32 (draft)
**Scope**: F149 (A), F104 (B), F102 (C), F112 (D), F130 (E), F103 (F),
F109 (G), F6 (H), F106 (I), F107 (J), F108 (K), F146 draft (L). Issues
#33-44.
**Metered seconds**: 0. No Dirac, Braket or other paid service was called.

This file is the durable copy. The same items are listed to the screen at
handover: a pointer to a file is not a handover.

---

## V1. Task A (F149): the F142 pre-submit guard, through the real library

- `run_dirac3s_verify.main()` hands each metered stop to a new `_run_stop`.
  A real run passes no stubs, so it is unchanged.
- Stub-fit tests cover the per-unit ledger skip, the stop cap (including
  earlier spend), a failed unit ending the stop, refusal codes 4 and 6,
  and the exit code.
- A fit runs through `metered_fit` and the real eqc-models classifier,
  with a fake at `requests.Session.request`. A changed Hamiltonian is
  refused before the file upload; the screened one reaches it.
- Both guards proven red. The stop 3 dry run's units are identical before
  and after the extraction.

## V2. Task B (F104): a public resolution gate

- `device_resolution.resolution_gate(J, C)`: A31's test that both
  coefficient spreads reach max |coefficient| / 200. The F142 runner calls
  it; `_coefficient_spread` is unchanged.
- `f104_gate_check.json`: the seeded B2 rebuild fails at 0.014 of the
  step; B4 oilgas passes at 37 times it; both hash to the Hamiltonians
  F142 sent. The check's exit code now also requires that hash match
  (code review).

## V3. Task C (F102): the Phase 2 draft's section 7

- arXiv:2604.18837 re-read. What the draft takes from it is now separated
  from what it adds (the bootstrap interval, family-wide Bonferroni,
  normalized AUPRC).
- New section 2a (one Bonferroni family per experiment) and 2b
  (equivalence margins, default 0.005 AUPRC).
- Section 5 recomputed by code: seed 42's 855 + 278 reproduces; 88-94% of
  pocket positives kept; the interval is 3-7% wider, not "about 4%".
- Still open: entries for Experiments 2-6, and the filing date (yours).

## V4. Task D (F112): Experiment 1 intervals

- Order effect: +0.0245 AUPRC, 97.5% interval [+0.0184, +0.0304],
  Wilcoxon p = 0.00195, 10 of 10 seeds. **P1 holds.**
- k effect: +0.0001, interval [-0.0034, +0.0037]. **Equivalent within
  ±0.005 (P2 holds).**
- `gate_report.md` was read, not regenerated. A test now checks that the
  recorded readings follow from the recorded figures.

## V5. Task E (F130): three lever screens on the proxy

Read `docs/phase2/F130_LEVER_SCREENS.md`.

- **No lever beats HGB on SPECTRA.**
- KNN learners move AUPRC up on oilgas (+0.012), telecom (+0.025) and
  ULB (+0.0095).
- The phase block moves it up on telecom (+0.037) and steel (+0.005, at
  the threshold, with the `in_pocket` caveat).
- Pair caps are rejected. The cap-sized cells reproduce the baseline
  exactly: they are identity controls for the new opt-in `pair_count`.
- **ULB's "beats HGB" is void.** The ULB HGB comparator is unstable under
  every setting tried (mean 0.22-0.52, seeds 0.06-0.70;
  `f130_ulb_hgb_check.json`). The cause is unverified.

## V6. Task F (F103): Tier 1 known-answer check

Read `docs/phase2/F103_TIER1_CHECK.md`.

- Real-target g2 = 0.914 ± 0.002, inside 0.94 ± 0.03. **Passes; G ran.**
- Sparse pocket JOINT - GA2M = +0.334, inside 0.37 ± 0.05; the planted
  frequencies recovered exactly.
- Dense substrate misses both values (+0.230 against 0.15; +0.227 against
  0.00). Most plausibly our rebuild differs from the authors' (Inferred);
  F150 repeats it when they send theirs.

## V7. Task G (F109): Tier 1 on six datasets

Read `docs/phase2/F109_TIER1_LADDER.md`.

- **The g4 prediction is not falsified.** g4 >= 0.02 on 0, 2 and 1 of 5
  seeds on ULB, IEEE-CIS before and after aggregation; 3 were needed.
  IEEE-CIS before aggregation is one seed short.
- Tier 1 says `candidate` on 32 of 35 dataset-seeds. It does not refuse
  fraud.
- The UID aggregation raises every IEEE-CIS lane (HGB 0.758 to 0.816) and
  lowers g4.

## V8. Task H (F6): the gate-based arm

Read `docs/phase2/F6_GATE_BASED_ARM.md`.

- **Recommendation: pursue narrowly, meaning simulation only.** No Braket
  hardware time; F116 and F117 stay on HOLD.
- `docs/references.md` paper paths corrected.

## V9. Task I (F106): the circuit against its classical twins

Read `docs/phase2/F106_DEQUANTIZATION.md`.

- **Inconclusive.** No twin's 99.17% interval clears the -0.005 margin,
  so the circuit is not shown dequantized. The circuit does not beat every
  twin either.
- Below the circuit: logistic regression (-0.037), JOINT (-0.074), RFF
  (-0.026).
- Level, inside wide intervals: GAM (+0.005), GA2M (+0.006), HGB (+0.020,
  ahead on 6 of 8 seeds). 99 test positives per seed set the width.
- The JOINT twin overfits (0.625, below its GA2M base; Inferred), so it is
  not the complete bar here.
- The encoding is phase-active (C = 0.53).
- **The step count was cut from 1,500 to 750** by the pilot's timing
  (projected 17,913 s against the 3-hour limit). The cut was recorded in
  the entry before the run (`a6b743f`). The run took 8,640 s.

## V10. Task J (F107): the shot budget

Read `docs/phase2/F107_SHOT_BUDGET.md`.

- **About 10,000 shots per row or more** keep test AUPRC within 0.005 of
  the exact statevector: 10,000 on 4 of 8 seeds, above 10,000 on 3. One
  seed reads 100, by luck (it is 0.054 short at 1,000).
- The prediction (100-10,000) holds on 5 of 8 seeds.
- The measure is noisy: AUPRC does not rise steadily with the shot count
  on 99 test positives.
- Effective Schmidt rank 1.7-3.2 of a possible 16.
- **The plan's acceptance changed.** It asked for "the critical rank per
  shot budget". The source (Wang et al., arXiv:2306.03481) defines that
  rank for entangled quantum training data, which a classical-input
  classifier does not have. J measured the shot budget instead (card and
  entry, before the run). A rank curve needs F116, on HOLD.
- **The first run refused correctly.** A different evaluation chunk size
  moved the exact AUPRC by 1.5e-4. F107 now uses F106's chunk size,
  recorded in the entry before any result (`6d551af`).

## V11. Task K (F108): ceiling methods against a known ceiling

Read `docs/phase2/F108_CEILING_VALIDATION.md`.

- The generator is exact on every seed.
- **No ceiling method recovers the known ceiling on the main arm in 4 of
  5 seeds**, so none is used on real data and F114 has no method yet.
- Requiring the main arm is a reading added after the run; the entry
  carries a dated note saying so.
- Default HGB misses the zero-ceiling reference (AUPRC 0.01-0.03 against
  1.0).

## V12. Task L (F146): the QCi questions draft

`docs/qci_package/F146_QCI_QUESTIONS_DRAFT.md` (gitignored, unsent). The
14 questions are listed to the screen at handover. Sending it is your
action. Delete the notes marked "delete before sending" first.
