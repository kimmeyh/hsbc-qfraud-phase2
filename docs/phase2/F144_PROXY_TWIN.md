# F144: Dirac-3 Does Not Beat Its Own Proxy on B2's Configuration

**Sprint 26 Task C**, 2026-10-14. Zero metered seconds. Evidence:
`experiments/phase2/results/f144_proxy_twin.json` (tag SIM), from
`experiments/phase2/src/f144_proxy_twin.py`. The test, its order and its
alpha were written in the Phase 2 draft before any twin pool was built
(`experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F144",
committed in `3949ff7`).

**Who reads this**: the team lead, and anyone citing B2, the campaign's
only positive result at scale.

## Bottom line

1. **B2's device rows equal an exact classical solve of the same
   configuration.** Across seeds 42-51, Dirac-3's test AUPRC minus the
   twin's is +0.0002 on average: Wilcoxon signed-rank p = 0.92, bootstrap
   95% interval -0.0009 to +0.0016, t-interval -0.0013 to +0.0018. The
   test does not reject. **Measured** (SIM for the twin, HW for the device
   rows): `device_vs_twin`.
2. **So B2's gain is the configuration's, not the device's.** The twin
   (k=17, weak-classifier schedule 3, 833 variables) scores 0.7925 mean
   AUPRC and the device 0.7928, against 0.7681 for the stored `free`
   proxy pools (k=13, 91 variables). The step up comes with the larger
   pool and is reproduced without a device. **Measured** (means over the
   10 seeds' rows). This confirms F64's decomposition and F139's reading
   ("B2's gain is a pool effect") with a direct, same-configuration twin.
3. **The comparison is readable.** The drift reference, stored `free`
   pools against unseeded rebuilds of them, differs by -0.0007 (Wilcoxon
   p = 0.70; bootstrap -0.0024 to +0.0007), so build drift does not
   produce an effect on this scale. **Measured**: `drift_reference`.
4. **The scoring matches Phase 1's.** Scored by this script, the stored
   `free` pools reproduce Phase 1's own proxy rows exactly (largest
   difference 0.0). **Measured**:
   `scoring_check_max_abs_diff_vs_phase1_rows`.

**What this does not show.** It does not show the device solved B2's
Hamiltonian well: A31 found B2's diffuse weights fall below the device's
weight resolution, and B2's weight cosine against the exact solve was
0.83. It shows that whatever the device returned, it ranked test
transactions as well as the exact optimum did, no better. The twin uses
the configuration, not B2's own pools, which were never stored.
**Inferred**, from A31 and the stated design.

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
- **F142's B2 fit stays a cost and queue measurement**, as planned. Its
  accuracy has no device question left to answer.
- **F112 (Experiment 1, isolate the k=17 confound)** can use the twin's
  pools as its order-3, k=17 cell at no further cost.
