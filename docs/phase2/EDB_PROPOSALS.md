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

A search of record values for "Dirac" (2026-10-13) found none of these.
Each is sourced in this repository:

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

## Reviewed

None yet.
