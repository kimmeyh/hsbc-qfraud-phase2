# Proposed Changes to the Evidence Library, Found From This Repository

**Living list** (F147 maintains it) | **Started**: 2026-10-13, Sprint 25

The evidence library is the team lead's EvidenceBasedDB repository and its
database. This repository never writes to it. When work here finds a record
that looks wrong, stale or missing, it is listed below for a session
running **in that repository** to review, accept or reject under its own
process. Each item names the record id, what was found, the evidence, and
the proposed change. The database was opened read-only (`mode=ro`) to find
these.

Status values: **open** (not yet reviewed there), **accepted**,
**rejected**. Only a session in that repository changes a status.

## Open

### P1. A stale allocation record

- **Record**: `hsbc-dirac3-allocation-1681-after-sizing-probes`
  (context `hsbc-2026`, updated 2026-10-03).
- **Found**: it states the remaining Dirac-3 balance as of late September.
  QCi added seconds to the account on 2026-10-09 (QCi's notice, filed in
  this repository's gitignored `docs/qci_package/`). The record is true of
  its date and wrong as a current balance.
- **Proposed**: keep it as a dated historical record, and add a newer
  record sourced from `experiments/results/allocation_reads.json` in this
  repository, which is the only file here that owns balance figures. (This
  proposal deliberately states no figure.)

### P2. Device interpretations need QCi's requested framing

- **Records**: `dirac3-matches-exact-optimum-on-convex-cvqboost`,
  `dirac3-fidelity-test-is-near-trivial-on-convex-formulation` (context
  `platform:dirac-3` only).
- **Found**: on 2026-09-25 QCi asked that our device-related
  interpretations be described as independent findings, not conclusions
  validated by QCi, until its review is complete. The team lead agreed.
  Both records are this project's findings about the device, and neither
  says so.
- **Proposed**: state in each that it is the project's independent
  finding, not validated by QCi; add the `hsbc-2026` context beside
  `platform:dirac-3`.

### P3. Findings from Sprint 25 with no record

Searched 2026-10-13: assertion values and ids, case-insensitive substring,
for "dirac-3s", "device_type", "sampler_type", "benchmark", "Table 6",
"fork", "device_usage", "billed", "floor", "cardinality", "tied",
"uniform", "sample size", "oracle", "router", "false positive", "XGBoost"
and "CVQBoost". No assertion states any of the findings below. Two
partial overlaps: `dirac3-fidelity-test-is-near-trivial-on-convex-formulation`
records uniform weights at lambda = 0, not across sample sizes; and the
"dirac-3s" hits are guide facts, none naming the selector. Each finding is
sourced in this repository:

- **Dirac-3S is chosen by name**: `device_type="dirac-3s"`, needing
  `qci-client` 5.0.3 and `eqc-models` 0.22.1; the earlier clients cannot
  reach it. (`docs/phase2/DIRAC_3S_RESEARCH.md` question 1)
- **QCi's Dirac-3S benchmark report contradicts itself**: zero gap claimed
  on every synthetic instance, two of eight missed in its Table 6.
  (`docs/phase2/DIRAC_3S_RESEARCH.md`, web sources)
- **`eqc-models` 0.22.1 still forces `fork`** and still exposes no named
  billed-seconds field. (`docs/phase2/DIRAC_UNDERSTANDINGS.md` section 3)
- **On the training fold, CVQBoost's cardinality problem has many tied
  optima at the objective's floor `-1 + 2/m`.**
  (`docs/phase2/F94_EXP3_CONTROLS.md`; evidence tag SIM)
- **CVQBoost's weights stay uniform at every sample size tested.**
  (`docs/phase2/F29_SAMPLE_SIZE.md`; SIM)
- **The per-transaction oracle gap over XGBoost comes almost entirely from
  dropping false positives, not from fraud CVQBoost catches.**
  (`docs/phase2/F113_ORACLE_GAP.md`; SIM)

Whether each belongs in the library, and in which context, is that
repository's decision.

**Re-searched 2026-10-14** with `scripts/edb_query.py` (F147): the
benchmark contradiction now has a record,
`dirac3s-all-optimal-headline-contradicted-by-own-table` (updated
2026-10-13). The other five findings still have none. This note does not
change P3's status; only that repository does.

### P4. This project's own device measurements, missing or unscoped

Found while building `scripts/edb_query.py` (F147, Sprint 26). Searched
2026-10-14, assertion values and ids, case-insensitive, for "b4",
"spectra", "dynamic range", "per fit", "device_type" and "sampler_type".

- **Missing: B4's device result on SPECTRA.** Dynamic range 8.1-8.4 dB
  against the 23 dB limit; weight cosine against the exact solve
  0.892-0.901 on oilgas_gasturbine, seeds 42-46.
  (`experiments/results/b4_hardware.json`, fields `dynamic_range_db` and
  `weight_cosine_vs_classical`; evidence tag HW)
- **Missing: Dirac-3 continuous cost per fit at our sizes.** 4-5 s at 91
  variables (B1, 11 fits), 71-92 s at 833 (B2, 11 fits).
  (`experiments/results/results.json`, `hw_b1_dct` and `hw_b2_full` rows,
  `metered_seconds`; HW)
- **Missing: A31, the resolution finding.** On the ten frozen ULB pools,
  no coefficient difference is resolvable at 200:1 (diagonal 510,705,
  off-diagonals spanning at most 20.0, against a resolvable difference of
  2,554), so hardware agreeing with the proxy there carries no fidelity
  information. On B2, the diffuse optimum's weights (about 0.0012) fall
  below the about 0.005 weight resolution, so the device returns a sparser
  solution. (`experiments/PREREGISTRATION.md` amendments A31 and A32)
- **Missing: Dirac-3S is selected by `device_type="dirac-3s"`**, through
  `eqc-models` 0.22.1's `sampler_type`. (`docs/phase2/
  DIRAC_UNDERSTANDINGS.md`, "Checked offline")
- **Scope: `dirac3-matches-exact-optimum-on-convex-cvqboost`** states
  cosines of 0.975-0.999 without naming the dataset. They are ULB's. B4's
  SPECTRA cosines are lower (above), so the record reads as more general
  than its evidence. Proposed: name ULB in the value.

These are this project's independent findings, not validated by QCi (see
P2).

## Reviewed

None yet.
