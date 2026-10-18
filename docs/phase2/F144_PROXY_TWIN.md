# F144: Dirac-3 Does Not Beat Its Own Proxy on B2's Configuration

**Sprint 26 Task C**, 2026-10-14. Zero metered seconds. Evidence:
`experiments/phase2/results/f144_proxy_twin.json` (tag SIM), from
`experiments/phase2/src/f144_proxy_twin.py`. The test, its order and its
alpha were written in the Phase 2 draft before any twin pool was built
(`experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F144",
committed in `3949ff7`). Revised the same day after a fresh-eyes review
(16 findings, all addressed here or in the draft).

**Who reads this**: the team lead, and anyone citing B2, the campaign's
only positive result at scale.

## Bottom line

1. **Across seeds 42-51, B2's Dirac-3 rows and the twin differ by +0.0002
   test AUPRC on average.** The twin is an exact classical solve of a
   rebuilt pool of B2's configuration. Wilcoxon signed-rank p = 0.92;
   bootstrap 95% interval -0.0009 to +0.0016; t-interval -0.0013 to
   +0.0018. The test does not reject. **Measured** (SIM for the twin, HW
   for the device rows): `device_vs_twin`.
2. **So the device can account for at most a small part of B2's gain.**
   The t-interval's upper bound, +0.0018, is about 7% of B2's +0.0256 gain
   over B1 (amendment A24). Failing to reject does not show the device and
   the twin are equal; it bounds how much the device could add.
   **Inferred**, from the measured interval.
3. **The same answer without any rebuild.** Each B2 row also records an
   exact solve of the device's OWN pool, scored on the validation fold
   (`fidelity.proxy_val_auprc_same_pool`, written by `run_hardware.py`).
   Device minus that solve, 10 seeds: mean -0.0003, Wilcoxon p = 0.63.
   **Measured** (`experiments/results/results.json`, `hw_b2_full` rows).
   This has none of the twin's rebuild confound, and agrees with it.
4. **The step comes from schedule 3's three-feature learners, not from
   pool size.** Phase 1's own proxy cells (stratified, 10 seeds each):
   `free` (k=13, schedule 2) 0.7681; `mid` (k=17, schedule 2, 153
   variables) 0.7682, no step; `deep` (k=13, schedule 3, 377 variables)
   0.7926, the whole step; the twin (k=17, schedule 3) 0.7925. **Measured**
   (proxy rows in `results.json`; twin in `f144_proxy_twin.json`). This
   confirms F64 and F139 ("B2's gain is a pool effect") and names the
   factor.
5. **What the drift reference shows, and what it does not.** Stored
   `free` pools against unseeded rebuilds differ by -0.0007 on average
   (Wilcoxon p = 0.70): no systematic bias, such as a library change,
   between the Phase 1 pools and today's builds. **Measured**:
   `drift_reference`. It does not show the drift is small: its true mean
   is zero by construction, and its per-seed spread (SD 0.0027) is the same
   size as the device-twin differences (SD 0.0022). It was measured on the
   91-variable `free` pool; at 833 variables, with 680 three-feature
   learners, it is not measured. Point 3's same-pool comparison is why the
   conclusion does not depend on it. **Inferred.**
6. **The scoring matches Phase 1's.** Scored by this script, the stored
   `free` pools reproduce Phase 1's own proxy rows exactly (largest
   difference 0.0; the script now refuses to write a result otherwise).
   **Measured**: `scoring_check_max_abs_diff_vs_phase1_rows`.

**What this does not show.** It does not show the device solved B2's
Hamiltonian well. B2's weight cosine against the exact solve was 0.82-0.83
(mean 0.827, 11 fits), and A31 found B2's diffuse weights fall below the
device's weight resolution. It shows that whatever the device returned,
it ranked test transactions about as well as an exact solve of a rebuilt
pool of the same configuration, and as well as an exact solve of its own
pool on validation. **Inferred**, from A31, A24 and points 1 and 3.

## Secondary metrics (preregistered)

Means over seeds 42-51, from `f144_proxy_twin.json` and the `hw_b2_full`
rows:

| Arm | Test AUPRC | Floor-normalized AUPRC | AUROC |
|---|---|---|---|
| B2 device (Dirac-3) | 0.7928 | not computed | 0.9423 |
| Twin (exact, seeded pool) | 0.7925 | 0.7922 | 0.9441 |
| Stored `free` proxy | 0.7681 | 0.7678 | 0.9210 |

AUROC is weak evidence here: A24 found about 92% of B2's scores tied.

## Per seed (test AUPRC)

| Seed | B2 device (Dirac-3) | Twin (exact, seeded pool) | Stored `free` proxy | `free` rebuilt |
|---|---|---|---|---|
| 42 | 0.8231 | 0.8245 | 0.8073 | 0.8093 |
| 43 | 0.7821 | 0.7829 | 0.7645 | 0.7619 |
| 44 | 0.7695 | 0.7641 | 0.7448 | 0.7381 |
| 45 | 0.8097 | 0.8089 | 0.7812 | 0.7821 |
| 46 | 0.7716 | 0.7701 | 0.7580 | 0.7583 |
| 47 | 0.7919 | 0.7939 | 0.7640 | 0.7615 |
| 48 | 0.8548 | 0.8567 | 0.8251 | 0.8238 |
| 49 | 0.7977 | 0.7976 | 0.7765 | 0.7781 |
| 50 | 0.7646 | 0.7648 | 0.7386 | 0.7384 |
| 51 | 0.7626 | 0.7621 | 0.7214 | 0.7230 |

## What changes

- **B2 no longer supports a device claim.** Any document that reads
  B2's result as evidence for Dirac-3 should cite this. Phase 1's filed
  documents are not edited (CLAUDE.md, the Phase 1 boundary); this is a
  dated Phase 2 result.
- **F142's B2 fit stays a cost and queue measurement**, as planned.
- **F112 (Experiment 1, the k=17 decomposition) may have less to answer.**
  The `deep` cell already separates order 3 from k at proxy level (point
  4). Re-check its question at the next refinement.
- **Future verify entries set an equivalence margin before the run**, so
  a drift reference can be read on size, not only on bias (draft section
  7).
