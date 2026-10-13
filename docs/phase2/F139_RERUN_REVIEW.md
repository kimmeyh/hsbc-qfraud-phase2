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
ceiling and the same 200:1 resolution; its cost at our sizes is unmeasured.

## Bottom line

- **Two verify runs are worth their seconds; nothing earns a full re-run
  yet.** Verify B1 on 2 fits, which gives the first Dirac-3S cost and
  fidelity point cheaply, then B2 on 3 fits, which tests the campaign's
  only positive result and stores what B2 lost. About 260 s at Dirac-3
  rates, capped at 460 s.
- **Expect no better predictions from the same formulation.** Every
  continuous block solved a convex problem whose exact optimum the proxy
  already has, and B4 matched its proxy within 0.0072 AUPRC. A device that
  finds that optimum more reliably moves the answer toward the proxy, not
  beyond it. B2 is the exception worth testing, because its gain came from
  the device NOT reaching the proxy's optimum.
- **The new hardware's headline capabilities do not fit this problem
  well.** Higher orders (3rd to 5th) have tiny ceilings and no natural
  place in a boosting objective that is quadratic by construction. More
  variables collide with the unchanged 200:1 resolution limit. The one
  sized case that the larger ceiling unlocks is telecom_churn at 987
  variables, and it depends on QCi confirming which configuration the
  cloud serves.
- **F129 should not run.** Recommendation below.

## The runs

Fits, seconds and configuration from `docs/QPU_RECONCILIATION.md`,
`docs/RESULTS_MEMO.md`, `docs/INTEGER_PROBE_RESULT.md`,
`docs/B4_B5_HARDWARE_RESULT.md`, `docs/sprints/SPRINT_6_SUMMARY.md` and the
amendment log in `experiments/PREREGISTRATION.md`.

| Run | Date | Fits | Seconds | What it was | Recommendation | Seconds now |
|---|---|---|---|---|---|---|
| G0b | 2026-09-03 | 5 | 21 | Proxy-vs-device config ranking, free tier, 25-91 variables; Spearman 0.900 | **No re-run** | 0 |
| B1 | 2026-09-03 | 22 | 99 | ULB free-tier configs, 78/91 variables, 10 seeds + temporal; device matched proxy | **Verify, 2 fits** | ~10 (cap 60) |
| F32 | 2026-09-05 | 10 | 43 | B1's config again, persisted predictions for operating points | **No re-run** | 0 |
| A21 probe | 2026-09-09 | 1 | 10 | Showed the 100-variable cap was a free-tier limit | **No re-run**; a new ceiling probe only after QCi answers | 0 |
| B3, first run | 2026-09-10 | 12 | 61 | IEEE-CIS reduced recipe; withdrawn for a design error (A23) | **No re-run** | 0 |
| B3, published | 2026-09-10 | 12 | 62 | The corrected IEEE-CIS run | **No re-run** | 0 |
| B2 | 2026-09-10 | 11 | 906 | ULB full config, 833 variables; +0.0256 AUPRC over B1's arm on 10 of 10 seeds; samples lost (QCi 404) | **Verify, 3 fits**; full re-run only if the verify reproduces the direction | ~250 (cap 400) |
| Integer probes | 2026-09-23 | 6 calls | 280 | Synthetic cost probes for the integer path, 8-150 variables | **Verify 2 probes**, as F25's pre-flight, not now | 0 now; ~195 with F25 |
| B5 | 2026-10-06 | 12 | 13 | QSVM arms on ULB | **No re-run** | 0 |
| B4 | 2026-10-06 | 10 | 640 | SPECTRA, schedule 3, 816/560 variables; H5 did not reproduce; device within 0.0072 of proxy | **No re-run** | 0 |

**Recommended now: about 260 s at Dirac-3 rates, capped at 460 s.** The
integer verify (about 195 s) is deferred to F25.

## Why each recommendation

- **G0b, F32**: both measured how closely the device tracks the proxy on
  B1's small configurations. B1's verify answers the same question for
  Dirac-3S, so repeating them adds nothing.
- **B1, verify 2 fits** (`hw_b1_dct`, seeds 42 and 43): the cheapest
  possible Dirac-3S fit at a size we have measured many times (4-5 s per
  fit on Dirac-3). It yields three things at once: the first Dirac-3S cost
  point, fidelity against the exact proxy optimum on the identical
  Hamiltonian, and a direct twin of a Dirac-3 fit. Every later quote
  depends on that cost point.
- **A21**: its question is answered. Whether Dirac-3S's cloud queue exceeds
  949 is a different question, best asked of QCi first, because a probe
  above the ceiling may simply be refused.
- **B3 (both)**: the first run was withdrawn for a pool-construction
  mismatch (A23) and is superseded by the published run. IEEE-CIS is
  Experiment 2's dataset, and the Phase 2 hardware plan runs Experiment 2
  on the classical proxy at zero device seconds
  (`HARDWARE_PLAN_PHASE_2.md`, sizing table). No planned work needs a
  device result on IEEE-CIS.
- **B2, verify 3 fits** (seeds 42-44, 833 variables, every sample and job
  id stored): B2's gain is the only positive result at scale, and A31
  explains it as the device returning sparser weights than the proxy
  optimum because of the 200:1 resolution limit. Dirac-3S has the same
  limit (F138), so the mechanism predicts the gain should reproduce. If it
  does not, the B2 finding is device-specific and must be described that
  way. B2's samples were lost, so a verify run also recovers what the
  original cannot supply. **Full re-run (11 fits, about 906 s) only if all
  3 seeds favor the larger configuration again.**
- **Integer probes, verify 2** (`probe_mid_hi` 60 variables, `probe_high`
  150 variables): the integer cost model was measured on Dirac-3 and F25 is
  the only card that uses it. Re-measure it as F25's first step, not
  before F25 is ready to run.
- **B5**: QSVM is not in the Phase 2 plan, and 13 s bought a result that
  does not depend on the device.
- **B4**: the replication failed on all 8 scoreable cells and the device
  matched its proxy. Dirac-3S reaching the proxy's optimum more reliably
  would reproduce the failure, not reverse it.

## F129: recommend it does not run

F129 asked whether the device reproduces the proxy on a sparse,
better-scoring SPECTRA problem (energy_steel with leaf regularization).
F128 removed the case for it as a route to advantage, and B4 already showed
the device matching its proxy within 0.0072 AUPRC at 816 variables. The B1
and B2 verify runs measure device-against-proxy fidelity on Dirac-3S
directly. **Recommendation: close F129, or hold it with no planned run.**
That is the team lead's call (Sprint 25 D2).

## What the new hardware allows, and whether it is worth doing

- **3rd to 5th order problems.** The base module takes 135 variables at
  3rd order, 39 at 4th and 19 at 5th; one expansion module takes 580, 145
  and 55. CVQBoost's objective, `w'(HH^T + lambda*I)w - 2(Hy)'w`, is
  quadratic by construction; a higher-order term has no role in it. "Order
  3" in this project means weak learners over feature triples, built
  classically before the device sees anything (F102 states both meanings).
  **No card.** A higher-order formulation would be a new research question,
  not a better run of an existing one.
- **More variables (up to 9,980 with an expansion module).** Larger pools
  make A31's limit worse: weight spread over more than about 200 learners
  is not representable at 200:1, whatever the ceiling. The one sized case
  is telecom_churn at schedule 3, 987 variables, which could not run on
  Dirac-3. **One card, on HOLD until QCi confirms the cloud configuration.**
- **Quantum fluctuation coefficient and mean photon number.** Exposed by the
  pinned client already, never set by any block here. On a convex problem
  they should not matter; on F25's non-convex integer problem they might.
  **Folded into F25's design**, not a separate card.

## New cards (numbered in the master plan)

- **F141. Dirac-3S client support**: bump `eqc-models` to 0.22.1 and
  `qci-client` to 5.0.3; construct solvers with `sampler_type="dirac-3s"`;
  a `device_type` field on every Phase 2 hardware row; re-check that the
  proxy Hamiltonian is unchanged. About 1h, zero metered. Gates F142.
- **F142. Dirac-3S verify block: B1 2 fits, then B2 3 fits.** About 260 s at
  Dirac-3 rates, cap 460 s; stops after the first B1 fit to re-quote.
  Depends on F141 and per-block approval.
- **F143. telecom_churn at 987 variables on Dirac-3S** (5 seeds; about 450 s
  at Dirac-3's 816-variable rate, unmeasured on Dirac-3S). HOLD until QCi
  confirms the cloud queue exceeds 949 variables.

## The Phase 2 hardware plan's sizing

`docs/HARDWARE_PLAN_PHASE_2.md` is FINAL. Its Experiment 3, 5 and 6 rows
were priced at Dirac-3's measured rates. None can be re-priced until F142's
first fit measures Dirac-3S. The document is not edited; if the rates
differ, the corrected sizing goes in a new document, as F115 does for its
cost-scaling sentence.

## Comparisons and the preregistration

Every Dirac-3S result above is a dated Phase 2 row naming its device. A
Dirac-3 against Dirac-3S comparison (B1 and B2 twins) is a Phase 2 result
with its own entry in the Phase 2 preregistration draft (F102). It is never
reported as a new cell of a Phase 1 gate, which section 11 of the frozen
preregistration would make a deviation.
