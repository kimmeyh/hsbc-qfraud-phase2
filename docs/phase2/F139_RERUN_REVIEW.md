# F139: Every Dirac-3 Run, Reviewed for Dirac-3S

**Sprint 25 Task B** (#14) | **Date**: 2026-10-13 | Zero metered seconds.
Nothing in this document runs. Every re-run it recommends is a card with
its own per-block approval (Criterion H).

**Who reads this, and what they decide.** The team lead decides which
Dirac-3S runs to approve, in what order, and at what cap. The balance they
are spent against is the last read in
`experiments/results/allocation_reads.json`; this document states no
balance.

**Built on F138** (`docs/phase2/DIRAC_3S_RESEARCH.md`): Dirac-3S is chosen
by name and needs a client bump; its base module has the same 949-variable
ceiling and states the same 23 dB maximum dynamic range; its cost at our
sizes is unmeasured.

**Revised the same day after the fresh-eyes review** (Sprint 25 Phase 5):
the B2 rationale, the B1 rationale, the B4 recommendation and the F129
reasoning changed. The changes are listed at the end.

## Bottom line

- **Three small verify runs, about 170 s at Dirac-3 rates, capped at
  360 s.** B1 on 2 fits (a cheap first cost and queue point), B2 on 1 fit
  (the cost at 833 variables, with every sample stored), and B4 on 2
  oilgas_gasturbine fits (the one fidelity test that means anything, on a
  Hamiltonian the device can resolve, with a direct Dirac-3 twin).
- **No full re-run.** Every continuous block solved a convex problem, and
  two facts limit what a better device could change. On the ULB pools (G0b,
  B1, F32, B2) the Hamiltonian is below the device's resolution, so the
  device returns near-uniform weights whatever it is (A31). On B4, which
  the device could resolve, it already matched its proxy within 0.0072
  AUPRC.
- **B2's gain is a pool effect, not a device effect.** The exact classical
  `deep` proxy (k=13, order 3) scores 0.7926 against B2's 0.7928, and
  `docs/F64_LADDER_DECOMPOSITION.md` attributes the gain to three-feature
  learners. No proxy twin of B2's own pool (k=17, order 3) exists, so the
  device against its proxy has never been compared on B2. A zero-cost card
  for that twin (F144) comes before any B2 comparison.
- **F129 should not run.** B4's verify gives the fidelity test F129 would
  have given, with an existing Dirac-3 twin.

## The runs

Fits, seconds and configuration from `docs/QPU_RECONCILIATION.md`,
`docs/RESULTS_MEMO.md`, `docs/INTEGER_PROBE_RESULT.md`,
`docs/B4_B5_HARDWARE_RESULT.md`, `docs/sprints/SPRINT_6_SUMMARY.md` and the
amendment log in `experiments/PREREGISTRATION.md`.

| Run | Date | Fits | Seconds | What it was | Recommendation | Seconds now |
|---|---|---|---|---|---|---|
| G0b | 2026-09-03 | 5 | 21 | Proxy-vs-device config ranking, free tier; Spearman 0.900 | **No re-run** | 0 |
| B1 | 2026-09-03 | 22 | 99 | ULB free-tier configs, 91 (dct) and 45 (lg) variables, full-pair, 10 seeds + temporal | **Verify, 2 fits**: cost and queue only | ~10 (cap 60) |
| F32 | 2026-09-05 | 10 | 43 | B1's config again, persisted predictions for operating points | **No re-run** | 0 |
| A21 probe | 2026-09-09 | 1 | 10 | Showed the 100-variable cap was a free-tier limit | **No re-run**; ask QCi about the cloud ceiling instead | 0 |
| B3, first run | 2026-09-10 | 12 | 61 | IEEE-CIS reduced recipe; withdrawn (A23) | **No re-run** | 0 |
| B3, published | 2026-09-10 | 12 | 62 | The corrected IEEE-CIS run | **No re-run** | 0 |
| B2 | 2026-09-10 | 11 | 906 | ULB full config, 833 variables; +0.0256 AUPRC over B1's arm on 10 of 10 seeds (a different pool); samples lost (QCi 404) | **Verify, 1 fit**: cost at 833 and full samples; no comparison until F144 | ~82 (cap 150) |
| Integer probes | 2026-09-23 | 6 calls | 280 | Synthetic cost probes for the integer path, 8-150 variables | **Verify 2 probes**, as F25's first step, not now | 0 now; ~195 with F25 |
| B5 | 2026-10-06 | 12 | 13 | QSVM arms on ULB | **No re-run** | 0 |
| B4 | 2026-10-06 | 10 | 640 | SPECTRA, schedule 3: oilgas_gasturbine at 560 variables, telecom_churn at 816 (with `age` dropped); H5 did not reproduce; device within 0.0072 of proxy | **Verify, 2 fits** (oilgas_gasturbine, seeds 42-43): the fidelity twin | ~80 (cap 150) |

**Recommended now: about 172 s at Dirac-3 rates, capped at 360 s.** The
integer verify (about 195 s) is deferred to F25.

## Why each recommendation

- **G0b, F32**: both measured how closely the device tracks the proxy on
  B1's pools, where A31 shows agreement carries no fidelity information
  (the Hamiltonian is below the device's resolution). Nothing to repeat.
- **B1, verify 2 fits** (`hw_b1_dct`, 91 variables, seeds 42 and 43): the
  cheapest Dirac-3S fit at a size measured many times on Dirac-3 (4-5 s per
  fit). It gives the first Dirac-3S cost and queue-wait point. **It is not a
  fidelity test**, for A31's reason.
- **A21**: whether the cloud `dirac-3s` queue exceeds 949 variables is a
  question for QCi first; a probe above the ceiling may simply be refused.
- **B3 (both)**: the first run was withdrawn for a pool-construction
  mismatch (A23) and is superseded. IEEE-CIS is Experiment 2's dataset, and
  the Phase 2 hardware plan runs Experiment 2 on the classical proxy at zero
  device seconds (`HARDWARE_PLAN_PHASE_2.md`, sizing table).
- **B2, verify 1 fit** (seed 42, 833 variables, every sample and job id
  stored): the Dirac-3S cost at our largest size, which every large block
  needs before it is quoted, and a stored copy of what B2 lost. It does
  **not** test B2's gain. That gain is measured against B1's arm, which used
  a different pool, and the classical `deep` proxy reaches the same AUPRC
  without the device. Whether the device's forced sparsity (A31) helps at
  833 variables can be asked only against a proxy twin of B2's own pool
  (F144, zero metered). A comparison run is a later card, after F144.
- **Integer probes, verify 2** (`probe_mid_hi` 60 variables, `probe_high`
  150 variables): the integer cost model was measured on Dirac-3, and F25 is
  the only card that uses it. Re-measure it as F25's first step.
- **B5**: QSVM is not in the Phase 2 plan, and 13 s bought a result that
  does not depend on the device.
- **B4, verify 2 fits** (oilgas_gasturbine, 560 variables, seeds 42 and 43):
  B4's Hamiltonians are at 8.1-8.4 dB, inside the 23 dB limit
  (`B4_B5_HARDWARE_RESULT.md`), so the device's answer depends on the
  problem. Repeating two of them on Dirac-3S gives a device-to-device twin on
  identical Hamiltonians: weight cosine, objective gap to the proxy optimum,
  and in-pocket AUPRC, against rows already on record. That is the fidelity
  test, and B4's cheapest cell (34-46 s per fit on Dirac-3) keeps it small.

## F129: recommend it does not run

F129 asked whether the device reproduces the proxy on a sparse SPECTRA
problem (energy_steel with leaf regularization). F128 removed the case for
it as a route to advantage. The B4 verify answers the fidelity question on
Dirac-3S more cleanly, because it has a Dirac-3 twin on identical
Hamiltonians. **Recommendation: close F129.** That is the team lead's call
(Sprint 25 D2). **Decided 2026-10-13 at Manual Validation: F129 closed.**

**Closing F129 strands F121**, whose hold is "until F128 and F129 report".
F121 then needs a new hold condition or a decision at the same refinement.
F113 (this sprint) is evidence for that decision: it found no
CVQBoost-specific complementarity with XGBoost.

## What the new hardware allows, and whether it is worth doing

- **3rd to 5th order problems.** Not new: Dirac-3 already listed orders 1
  to 5 at the same base ceilings (F138). CVQBoost's objective is quadratic
  by construction; "order 3" in this project means learners over feature
  triples, built before the device sees anything. **No card.**
- **More variables (up to 9,980 with an expansion module).** Larger pools
  force the device to return sparser weights than the optimum (A31). Whether
  that helps or hurts is the experimental question, and B2 at 833 variables
  gave the campaign's best AUPRC, though F64 attributes that to the pool.
  The one sized case is telecom_churn with all 18 features: 987 variables
  in the full-pair build. B4 ran it at 816 with `age` dropped. **One card,
  on HOLD until QCi confirms the cloud configuration**; it would add the
  dropped feature's effect, on cells where B4's in-segment edge was already
  negative.
- **Quantum fluctuation coefficient and mean photon number.** Exposed by the
  pinned client already, never set by any block here. **Folded into F25's
  design.**

## New cards (numbered in the master plan)

- **F141. Dirac-3S client support**: the package bumps, `sampler_type`, a
  device field on every hardware row, and the proxy-identity check. About
  1h, zero metered. Gates F142.
- **F142. Dirac-3S verify block**: B1 2 fits, B2 1 fit, B4 2 fits; about
  172 s at Dirac-3 rates, cap 360 s; stops after the first B1 fit to
  re-quote. B1 and B2 fail the F104 resolution screen by design (their
  purpose is cost); the Phase 2 draft's screen rule makes that exception
  explicit.
- **F143. telecom_churn with all 18 features (987 variables) on Dirac-3S.**
  At least 450 s; the rate at 987 variables is unmeasured. HOLD until QCi
  confirms the cloud ceiling.
- **F144. The proxy twin of B2's pool** (k=17, order 3, full pair, 833
  variables), zero metered. The comparison B2 never had.
- **F145. Why the pool build is not reproducible from its seed** (F29),
  zero metered.

## The Phase 2 hardware plan's sizing

`docs/HARDWARE_PLAN_PHASE_2.md` is FINAL. Its Experiment 3, 5 and 6 rows
were priced at Dirac-3's measured rates. None can be re-priced until F142
measures Dirac-3S. The document is not edited; if the rates differ, the
corrected sizing goes in a new document, as F115 does for its cost-scaling
sentence.

## Comparisons and the preregistration

Every Dirac-3S result above is a dated Phase 2 row naming its device. A
Dirac-3 against Dirac-3S comparison (the B4 twins) is a Phase 2 result with
its own entry in the Phase 2 preregistration draft (F102). It is never
reported as a new cell of a Phase 1 gate, which section 11 of the frozen
preregistration would make a deviation.

## What changed after the fresh-eyes review

- **B2**: the first version said B2's gain "came from the device NOT
  reaching the proxy's optimum" and set a full re-run trigger on all 3
  seeds favoring the larger configuration. Both were wrong: the gain is a
  pool effect (F64; the classical `deep` proxy reaches the same AUPRC), and
  the trigger would fire on any device. Now 1 fit, for cost, and F144 first.
- **B1**: the first version claimed fidelity against the proxy. A31 says
  agreement on that pool carries no fidelity information. Now cost only.
- **B4**: was "no re-run". Now the fidelity twin, because its Hamiltonians
  are the only resolvable ones on record.
- **Sizes**: B1 is 91 and 45 variables in the full-pair build, not 78/91
  (A25 had corrected this). telecom_churn did run on Dirac-3, at 816 with a
  feature dropped.
- **The A31 reading**: "larger pools make A31's limit worse" was the
  reading the master plan says must not be repeated. Rewritten above.
