# F103: SPECTRA Tier 1 known-answer check on UCI Steel

Sprint 27 Task F, 2026-10-18. Zero metered seconds. The entry is the
Phase 2 draft's section 6, "F103", committed before the first run
(`a05ae94`). Every figure below is in
`experiments/phase2/results/f103_tier1.json` (five seeds, 42-46);
the one-seed pilot is `f103_tier1_pilot.json`.

## BLUF

**The gating check passes, so Task G (F109) runs.** The reimplemented
trained-frequency GAM reaches 0.914 ROC-AUC on the real target (SD 0.002
over five seeds), inside the paper's 0.94 with the entry's tolerance of
0.03. The sparse pocket also reproduces. Both dense-substrate values
miss; most plausibly our rebuild from the paper's text differs from the
authors' construction (Inferred). Those two values do not gate (entry), and
F150 repeats the check on the authors' construction once they send it.

## Results (Measured)

- **Permuted-label reference, run first**: every lane at chance (GAM
  0.510, GA2M 0.499, HGB 0.495, JOINT 0.495); Tier 1 returns `refuse`
  (g3 and g4 fail). The pipeline finds nothing where there is nothing.
- **Real target (g2, gating)**: GAM 0.914 ± 0.002 against 0.94 ± 0.03.
  **Within.** HGB reaches 0.9998-1.0000, JOINT 0.992-0.994.
- **Sparse pocket, JOINT minus GA2M**: +0.334 (SD 0.033) against +0.37
  ± 0.05. **Within.** The first JOINT term recovers the planted
  frequencies (3.7, 5.1, 6.8) exactly on all five seeds, inside the
  entry's 0.05 of the paper's (3.67, 5.13, 6.83).
- **Dense substrate, HGB minus GAM**: +0.230 (SD 0.034) against +0.15
  ± 0.05. **Outside.**
- **Dense substrate, JOINT minus GA2M**: +0.227 (SD 0.043) against
  +0.00 ± 0.05. **Outside.**
- **Run time**: 1,021 s for five seeds; JOINT is about 96% of it.

## Reading

- **The real target's Tier 1 verdict is `candidate`, and that agrees
  with the paper.** Tier 1 is permissive by design (Algorithm 1, lines
  7-8); the paper refuses this target at Tier 2's gate g6, where HGB
  reaches 0.999 and its quantum model 0.910 (section 6.1, Table 2). Our
  HGB at 0.9998-1.0000 is the same wall. Tier 2 is not reimplemented.
- **The dense mismatch is in the substrate, not the lanes (Inferred).**
  The paper's dense-substrate lanes are GAM 0.548, GA2M 0.582, HGB
  0.699, JOINT 0.587 (Table 2). Ours are GAM 0.55-0.60, HGB 0.76-0.87,
  JOINT 0.80-0.89. The same lanes reproduce the sparse pocket's planted
  term and the real target, so the gap is most plausibly in what the text
  leaves open about the substrate: the coupling distribution, the
  Trotter scheme, the field order and the label threshold, each fixed by
  the entry rather than taken from the authors. F150 settles this.
- **Pilot against full run.** The one-seed pilot put the sparse gap at
  +0.309, outside its tolerance; the five-seed mean is inside. The
  entry's check is on the mean, as written.
- **Release phases.** The released phase columns are the paper's recipe
  plus zero-mean jitter (SD about 0.02 rad on four phases and 0.17 rad
  on the reactive phase, which departs by up to 0.69 rad), so
  phases are rebuilt from the raw fields (entry; `release_phase_jitter`
  in the results file).

## What this does not settle

- Tier 2 (the quantum lane and g6, g7) is not reimplemented, and SPECTRA's
  own code is proprietary; this check is of Tier 1 only.
- g1 has no published value; ours is an exploratory estimator, reported
  and not checked.
- The paper's "joint ratio 9.9" is undefined in its text and not checked.
