# Dirac-3 and Dirac-3S: What We Understand, What We Would Change, What We Would Ask

**Living document, F146** (permanent, on HOLD between updates) | **First
draft**: 2026-10-13, Sprint 25 | Zero metered seconds

**Who reads this, and what they decide.** The team lead, before any
message to QCi and before any Dirac-3S block is approved. It is the one
place this repository keeps (1) what we understand about both devices and
how well each item is established, (2) the improvements we would suggest
for Dirac-3S, and (3) the questions for QCi. **This file owns the question
list**; `docs/phase2/DIRAC_3S_RESEARCH.md` points here.

**Standing constraint from QCi (2026-09-25).** Until its review of our
materials is complete, QCi asked that we describe our interpretations of
the device as our own independent findings, not as conclusions QCi has
validated. The team lead agreed the same day. Every item below
marked **Measured** or **Inferred** is our independent finding. None is
validated by QCi. (Source: the correspondence in `docs/qci_package/`,
gitignored.)

**Nothing in this file has been sent to QCi.** Sending is the team lead's
action. Anything sent is filed in `docs/qci_package/`, and its status is
updated here.

## How each item is labeled

- **Measured**: we measured it on the device. Cites the result file or
  write-up. Evidence tag `HW`.
- **Measured (SIM)**: we measured it on a classical solve of the same
  Hamiltonian. Evidence tag `SIM`.
- **QCi states**: in a QCi document, with the section. Not checked by us.
- **Independent**: a source outside QCi and outside this project.
- **Checked offline**: we ran the client code with no device call. True of
  the request we send, not of the device. (Added 2026-10-14.)
- **Inferred**: our reasoning from the items above. Says what it rests on.
- **Unverified**: believed, not checked. Says what would settle it.

Where EvidenceBasedDB holds the same item, its record id is given as
`EDB: <id>`. EvidenceBasedDB was read only.

---

## 1. Dirac-3: what we understand

### Measured by us

- **It solves our convex problem to the exact optimum's quality.** On the
  Phase 1 CVQBoost formulation, hardware minus the exact classical solve of
  the same Hamiltonian was -0.0010 AUPRC (CI -0.0032 to +0.0012), weight
  cosine 0.975 to 0.999. (`docs/QCI_EQC_MODELS_FEEDBACK.md` section 5;
  EDB: `dirac3-matches-exact-optimum-on-convex-cvqboost`)
- **That test was nearly trivial, at small pool sizes.** The formulation
  is strictly convex and, with the ridge, its optimum is near-uniform
  weights. (Corrected 2026-10-14: this line said "even at lambda = 0";
  amendment A27 withdrew that, since at lambda = 0 the optimum is a face of
  the simplex and the ridge selects the near-uniform point.) The match holds
  up to 91 variables (cosine 0.975-0.999). It does not hold at 560-833:
  cosine 0.89-0.90 on B4 oilgas (560), 0.83-0.85 on B4 telecom (816) and
  0.82-0.83 on B2 (833, ULB), falling with pool size across datasets, as
  A31's weight-resolution limit predicts. **Measured** (`results.json`
  `fidelity.weight_cosine`; `b4_hardware.json`). (EDB:
  `dirac3-fidelity-test-is-near-trivial-on-convex-formulation`, which still
  carries the withdrawn clause; `docs/phase2/EDB_PROPOSALS.md` P4)
- **It never returned an answer better than the certified optimum.**
  Hardware objectives were 0.013% to 0.413% above the exact minimum.
  Within-fit energy spread: median 0.020%, maximum 0.343%, over 48 fits.
  (`docs/QCI_EQC_MODELS_FEEDBACK.md` section 4)
- **It was reliable.** 61 Phase 1 fits, zero failures, zero retries.
  (`docs/QCI_EQC_MODELS_FEEDBACK.md` section 4)
- **Our Hamiltonians are below its stated resolution (A31).** On the ten
  frozen pools, off-diagonal coefficients differ by at most 20.0, against a
  resolvable difference of 2,553.5. Agreement with the proxy on those pools
  carries no fidelity information. (`experiments/PREREGISTRATION.md` A31;
  `docs/QCI_EQC_MODELS_FEEDBACK.md` section 6)
- **At 833 variables it returned sparser weights than the optimum.** Weight
  cosine 0.83, exact zeros in all eleven fits. That configuration (B2) gave
  +0.0256 AUPRC on ten of ten seeds, but the gain is a pool effect: the
  classical `deep` proxy reaches 0.7926 against B2's 0.7928.
  (`docs/F64_LADDER_DECOMPOSITION.md`; `docs/phase2/F139_RERUN_REVIEW.md`)
- **B4's Hamiltonians are within its range** (8.1 to 8.4 dB against the
  23 dB limit). They are the only ones of ours where a device comparison
  can carry fidelity information. (`docs/phase2/F139_RERUN_REVIEW.md`)
- **Cost tracks problem size, and is stable at a given size.** Per call:
  4.0 s minimum, 5.0 s median on the small free-tier problems; about 0.6 s
  per sample for B3; 11.27 s per sample for B2 at 833 variables; 84 to 90 s
  per fit for B4 at 816. (`docs/QCI_EQC_MODELS_FEEDBACK.md` section 4;
  `docs/phase2/DIRAC_3S_RESEARCH.md` question 3; F143)
- **Integer-solver cost tracks variables, not levels.** Five sizing probes
  on 2026-09-23. A two-point cost line was off by 1.6 and 4.1 times on the
  next two calls. (EDB: `dirac3-integer-cost-tracks-variables-not-levels`,
  `dirac3-integer-cost-per-level-line-falsified`)
- **The free tier caps continuous jobs at 100 variables**, a limit the
  documentation did not state. (`docs/QCI_EQC_MODELS_FEEDBACK.md` section 1)
- **Untested levers.** Every Phase 1 fit ran relaxation schedule 2. No
  block has set the quantum fluctuation coefficient or the mean photon
  number, although the pinned client already passes both.
  (`docs/phase2/DIRAC_3S_RESEARCH.md` question 4)

### Measured on the classical proxy, and true for any device

- **On the training fold, as every device run built it, the cardinality
  problem has many tied optima.** Every method reaches the objective's
  floor, `-1 + 2/m`. On the validation fold the best selection found is
  within 0.0016 to 0.0026 of the floor, and greedy finds it in seconds.
  (`docs/phase2/F94_EXP3_CONTROLS.md`)
- **Inferred from that**: a better device cannot show an advantage on our
  current Hamiltonians. The formulation must change first (held-out
  predictions, a deliberate ridge weight; F25).

### QCi states

- Variable ceiling by order, all-to-all: 949 (2nd), 135 (3rd), 39 (4th),
  19 (5th). (Dirac-3 User Guide v0.0.4; EDB:
  `dirac3-variable-ceiling-falls-with-interaction-order`)
- Effective analog resolution about 200:1 (23 dB). (EDB:
  `dirac3-analog-resolution-about-200-to-1`)
- Integer variables take values 0 to 16; more states need the continuous
  solver. (EDB: `dirac3-integer-variables-bounded-0-to-16`)
- It returns a sub-optimal answer at a measurable rate; the guide's worked
  example found the optimum in 23 of 100 trials. (EDB:
  `dirac3-returns-suboptimal-answers-at-a-measurable-rate`)
- Mechanism, in QCi authors' own words: no entanglement is used; photons
  are measured in every feedback loop, which "rules out a quantum
  advantage" for that version; the coupling is computed in an FPGA; the
  optics could in principle be simulated classically; weak coherent states
  stand in for Fock states. (EDB: `dirac3-does-not-use-entanglement`,
  `dirac3-per-loop-measurement-rules-out-quantum-advantage`,
  `dirac3-variable-coupling-computed-in-fpga`,
  `dirac3-optics-could-be-classically-simulated`,
  `dirac3-uses-weak-coherent-states-not-fock-states`)

### Independent sources

- An independent group reproduced QCi's published Dirac-3 benchmarks with
  classical solvers on a consumer CPU. Low certainty. (EDB:
  `classical-solvers-match-dirac3-published-benchmarks`)
- A stratification study found Dirac-3's answer behind a GPU Ising machine
  and a genetic algorithm. Low certainty. (EDB:
  `dirac3-stratification-falls-short-ballin-2026`)
- The favorable Dirac-3 papers are QCi-authored, including the fraud paper
  that reports 0.8108 AUC-PR on the ULB dataset. (EDB:
  `favorable-dirac3-papers-are-qci-authored`,
  `cvqboost-knn-aucpr-0-8108-kaggle-fraud`)

### Unverified

- **Queue timing.** A stored note says the `dirac-3` queue is usually empty
  after 5 pm local. It is dated and was not re-measured. The next metered
  block's queue waits settle it.

---

## 2. Dirac-3S: what we understand

Nothing in this section is measured. No job has run on Dirac-3S.
Full sources: `docs/phase2/DIRAC_3S_RESEARCH.md` and
`docs/phase2/DIRAC_3S_SITE_SWEEP.md`.

### QCi states

- **It is "QCi's second generation Dirac-3 device"**, chosen per job by
  `device_type="dirac-3s"`. It needs `qci-client` 5.0.3 and `eqc-models`
  0.22.1 (`sampler_type="dirac-3s"`). Both are pinned from 2026-10-14
  (F141). (Client docs; checked against the wheels.)
- **Unknown job parameters are "dropped from the job body without
  warning".** A misspelled device name would run silently on the default.
  (Client docs, through the site sweep; not re-checked.)
- **Ceilings**: the base module equals Dirac-3 (949, 135, 39, 19). With one
  expansion module: 9,980, 580, 145 and 55. (Guide Table 2; EDB:
  `dirac3s-variable-ceiling-by-configuration`)
- **Resolution**: the same 23 dB maximum and the same about 200:1 sentence
  as the Dirac-3 guide. (EDB: `dirac3s-analog-resolution-about-200-to-1`)
- **It is not an exact solver**; the best returned sample is the answer.
  (EDB: `dirac3s-not-an-exact-solver`)
- **"Error correction" is a post-processing step** on the returned
  samples; raw values come back too. (EDB:
  `dirac3s-error-correction-is-a-post-processing-step`)
- **The same four relaxation schedules.** Per-sample times for one
  50-variable problem: 0.236, 0.420, 1.093 and 1.278 s for schedules 1 to
  4. (Guide Table 4; EDB: `dirac3s-time-per-sample-by-schedule`)
- **Sum constraint R from 1 to 10,000**; a larger R spreads the same
  resolution more thinly. (EDB: `dirac3s-sum-constraint-1-to-10000`)
- **Hardware**: base module one 5U unit at 100 W; with one expansion
  module, two units under 1,500 W. Not yet CE or FCC certified. (EDB:
  `dirac3s-power-and-size-by-configuration`,
  `dirac3s-not-yet-ce-or-fcc-compliant`)
- **"It should provide much better results"** (QCi's notice, 2026-10-09).
  A vendor claim. No source compares Dirac-3S with Dirac-3.

### Checked offline (F141, 2026-10-14)

Run in both venvs (Windows, and WSL `/root/eqc-venv`) with the client's
three network calls replaced. Tests: `test_response_serialization.py`,
`test_qubo_proxy.py`.

- **The request names `dirac-3s` unchanged.** qci-client's own
  `build_job_body` puts it in `device_config` as given. The `dirac-3` alias
  is rewritten to `dirac-3_normalized_qudit`.
- **The Hamiltonian is unchanged.** The `ml/` and `base/` sources of
  `eqc-models` are identical in 0.21.0 and 0.22.1, and the J and C a
  CVQBoost fit sends equal the proxy's exactly.
- **0.22.1 removes the `generation` constructor argument.** The class
  attribute remains; when set, it is appended to the device name as
  `<sampler_type>.<generation>`. `sampler_type` accepts only `dirac-3s`,
  and only on a Dirac-3 solver.
- **The library sends the model's own `num_samples`**, not the argument to
  `solve` (0.21.0 and 0.22.1 alike). A dry run records the value from the
  request body for this reason.
- **Job metrics are read by the device name in the request.** A Dirac-3S
  result's timing is looked up under `dirac-3s`. Whether QCi's metrics use
  that key is **unverified**; F142's first fit settles it.

### What QCi's own documents get wrong or leave open

- The guide reuses Dirac-3 text and figures, with Dirac-3 headings. (EDB:
  `dirac3s-guide-reuses-dirac-3-text-and-figures`)
- It gives two integer ranges, 0 to 15 and 0 to 16. (EDB:
  `dirac3s-guide-gives-two-integer-ranges`)
- It says on-premises has no 100-sample cap, and its own table caps samples
  at 100. (EDB: `dirac3s-on-premises-has-no-100-sample-cap`)
- Its worked example (97 of 100) is not the Dirac-3 example (23 of 100);
  the problems differ. (EDB: `dirac3s-worked-example-is-not-like-for-like`)
- The benchmark report claims a zero gap on every synthetic instance; its
  own Table 6 shows two of eight missed. It compares only with classical
  solvers. (`docs/phase2/DIRAC_3S_RESEARCH.md`, web sources)
- On-premises benchmark times (about 2 s per sample at 171 variables, 14
  to 28 s at 2,000) are a different access path and different problems
  from ours. They are not a cost model.

### Not known, and what settles each

- **Which configuration serves the cloud queue.** Only QCi can say
  (question A1). It decides whether F143 (987 variables) can run.
- **Cost and billing at our sizes.** F142's first fit measures cost;
  billing is question A3.
- **Effective resolution.** Question A6, and F142's B4 twin.
- **Queue hours for the "special queues".** Question A5; F142 records the
  waits.

### Inferred: what Dirac-3S changes for us

- **On the base module, nothing about our size limits.** Our ceilings are
  Dirac-3's. Only the expansion configuration lifts them.
- **If the resolution is unchanged, A31 applies unchanged.** B1 and B2's
  coefficient spreads stay below it; only B4's pass (37 times the step,
  `experiments/phase2/results/f142_dry_run.json`). B4's optimum weights
  (about 0.0018) still sit below the weight resolution, A31's second half,
  so F142's B4 fits compare the two devices on a sparsified problem, not
  on a fully resolvable one. (Scoped 2026-10-14, Sprint 26 fresh-eyes
  review.)
- **The binding limit is our formulation, not the device** (section 1,
  F94). A Dirac-3S result on the current Hamiltonians cannot beat greedy by
  more than the 0.0016 to 0.0026 left to the floor.

---

## 3. Suggested improvements for Dirac-3S

Draft suggestions to QCi. Each names the evidence behind it. **None has
been sent.** They follow the format of our Phase 1 feedback
(`docs/QCI_EQC_MODELS_FEEDBACK.md`, filed 2026-09-12; not edited here).

### Still open from our Phase 1 feedback

Checked on 2026-10-13 against the `eqc-models` 0.22.1 wheel (downloaded,
not installed). Items 1 and 2 re-checked on 2026-10-14 against 0.22.1 as
installed (F141): both still hold.

1. **The billed seconds are still not a named field.**
   `eqc_models/base/results.py` is unchanged from 0.21.0 apart from line
   endings. `SolutionResults` has no `device_usage_s` attribute; a caller
   must index the raw response. (Phase 1 item 2.)
2. **Pool construction still forces `fork`.**
   `ml/classifierqboost.py` calls `set_start_method("fork", force=True)` in
   three places, so it still fails on Windows. (Phase 1 item 3.)
3. **The free-tier continuous ceiling**: whether the documentation now
   states it is **unverified**. Settled by reading the current free-tier
   page. (Phase 1 item 1.)

### New for Dirac-3S

4. **Reject unknown job parameters.** A misspelled `device_type` is
   dropped silently and the job runs on the default device. A
   device-selection key is exactly the one that must fail loudly.
5. **Name the hardware in every result.** Return the device, its
   generation and its configuration (base or expanded) in the job
   response. Today a result cannot say which device produced it.
6. **Check resolution before submission.** Warn when a Hamiltonian's
   coefficient differences fall below the effective resolution, or return
   the coefficients as loaded. Our A31 finding cost a withdrawn claim; a
   warning would have caught it on the first call.
7. **Publish a like-for-like comparison** of Dirac-3 and Dirac-3S on the
   same problems, with the effective resolution measured on Dirac-3S.
   "Much better results" has no published basis yet.
8. **Correct the guide**: Dirac-3 headings and figure captions, the two
   integer ranges, the on-premises sample cap, and where Table 4 was
   measured. Correct the benchmark report's summary to match its Table 6.
9. **Offer a cost estimate before submission**: expected device seconds
   for a given size, order and schedule. Name Dirac-3S in the billing FAQ.

---

## 4. Questions for QCi

### Asked 2026-09-25, under QCi review, no answer as of 2026-10-13

- **P1.** Is our reading of the Hamiltonian correct: `J = HH^T + lambda*I`,
  `C = -2Hy`, sum constraint 1.0, `w >= 0`?
- **P2.** Is our reading of the 200:1 resolution finding correct?

Do not ask these again. Follow up on them if the review has no answer by
the next message.

### Not yet sent

From F138 (`docs/phase2/DIRAC_3S_RESEARCH.md`, questions (a) to (f)):

- **A1.** Which configuration serves the cloud `dirac-3s` queue: base, or
  base plus expansion?
- **A2.** Does the `dirac-3` device name now run on upgraded hardware?
- **A3.** Is Dirac-3S billed differently from Dirac-3?
- **A4.** Is the integer budget still the sum of levels, and is the limit
  16 or 17 levels per variable?
- **A5.** May this account use the `dirac-3s` "special queues", and in
  what hours?
- **A6.** Is Dirac-3S's effective resolution the same about 200:1 as
  Dirac-3's, or is that only its stated maximum?

New:

- **A7.** What is the 200:1 relative to: the largest coefficient of the
  whole Hamiltonian, of its quadratic part, or something else? Is the
  Hamiltonian rescaled before it is loaded?
- **A8.** Will the `dirac-3` name be retired or remapped to Dirac-3S, and
  with what notice? Our Phase 1 results name `dirac-3`.
- **A9.** Was the guide's Table 4 measured on Dirac-3S, and on the cloud or
  on-premises?
- **A10.** What comparison supports "much better results"? On which
  problem class?
- **A11.** Is the cloud cap still 100 samples per job on `dirac-3s`?
- **A12.** Can a job be repeated with the same sampling seed, or is every
  run's randomness fixed by the hardware?

---

## 5. When this file is updated

F146 is permanent and stays on HOLD. It re-opens when any of these happens:

- QCi answers any question above, or sends new material.
- QCi publishes a new guide revision, client release or benchmark.
- F141 bumps the clients (re-check section 3, items 1 and 2).
- F142's first Dirac-3S fit returns (cost, queue wait, B4 fidelity).
- A sprint finds a fact that changes an item above.

Each update adds a row to the revision log and moves items between labels
(for example, from Unverified to Measured).

## Revision log

| Date | Sprint | Change |
|---|---|---|
| 2026-10-13 | 25 | First draft: understandings for both devices, nine suggested improvements, two pending and twelve unsent questions |
| 2026-10-14 | 26 | F141 bump: clients pinned; new label "Checked offline"; five offline findings for Dirac-3S (request body, Hamiltonian identity, `generation` argument removed, `num_samples` source, metrics key); section 3 items 1 and 2 re-checked |
| 2026-10-14 | 26 | Fresh-eyes review: the "nearly trivial" fidelity item drops the lambda = 0 clause (A27) and is scoped to small pools, with the cosine falling with pool size; the B4 item scoped to A31's weight-resolution half |
