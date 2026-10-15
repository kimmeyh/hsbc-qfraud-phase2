# Sprint 26 Manual Validation

**Sprint**: 26, Reach Dirac-3S, Measure It, and Make the Proxy Repeatable
**Branch**: `feature/20261013_Sprint_26` | **PR**: #21 (draft)
**Scope**: F141 (A), F145 (B), F144 (C), F142 (D), F147 (E), F126 (F),
F105 (G), F146 (H). Issues #22-29.
**Metered Dirac-3S seconds**: stop 1 spent 6.0 (row `metered_seconds`,
`experiments/phase2/results/f142_dirac3s_verify.json`). Stops 2 and 3 are
recorded in V4 as they were decided.

This file is the durable copy. The same items are listed to the screen at
handover: a pointer to a file is not a handover.

---

## V1. Task A (F141): our code reaches Dirac-3S

Read `CHANGELOG.md` (2026-10-14, F141) and the "Checked offline" part of
`docs/phase2/DIRAC_UNDERSTANDINGS.md` section 2.

- `qci-client` 5.0.3 and `eqc-models` 0.22.1 are pinned in the
  requirements and the lock, whose header has a dated line saying so
  (Decision 5 rule 5). Both venvs are updated (Windows `.venv`, WSL
  `/root/eqc-venv`).
- `eqc_submit.device("dirac-3s")` sends a fit to Dirac-3S; Dirac-3 stays
  the default. A dry run builds the library's real request body, and it
  names `dirac-3s`.
- The Hamiltonian is unchanged between the versions: a test holds the J
  and C a fit sends equal to the proxy's.
- Phase 2 device rows must name `device_type` (row-schema test, proven
  red).

## V2. Task B (F145): a pool build repeats from its seed, when asked

- `build --seeded-learners` and `qubo_proxy.seeded_weak_params` are
  opt-in. Phase 1 builds never pass them, so their behavior is unchanged.
- Two seeded builds are byte-identical on all three folds.
- Unseeded builds still drift: `experiments/phase2/results/f145_build_drift.json`
  (64 of 78 learners differ on ULB; the figure varies by run). The Phase 2
  draft's section 7 records this as a known limit of Phase 1 pools.

## V3. Task C (F144): Dirac-3 does not beat its own proxy on B2

Read `docs/phase2/F144_PROXY_TWIN.md`.

- **Device minus twin: +0.0002 AUPRC** over seeds 42-51 (Wilcoxon p =
  0.92; t-interval -0.0013 to +0.0018). The device can account for at most
  about 7% of B2's +0.0256 gain.
- **The same-pool comparison agrees** with no rebuild at all: -0.0003, p =
  0.63.
- **The step comes from schedule 3's three-feature learners**, not from
  pool size: `deep` 0.7926, the twin 0.7925, `mid` 0.7682, `free` 0.7681.
- The drift reference shows no bias (p = 0.70), but its spread is the
  same size as the device-twin spread; the note says what that does and
  does not show.
- The F144 entry was written before any twin pool was built. A dated
  post-result correction note sits below it; the entry is unchanged.

## V4. Task D (F142): the first Dirac-3S fits

Read the "Measured" part of `docs/phase2/DIRAC_UNDERSTANDINGS.md` section
2, and the F142 entry in `experiments/phase2/PREREGISTRATION_DRAFT.md`
section 6.

- **Stop 1 (Decision 7, approved)**: one B1 fit, job
  `6ad04e0b358b23d0cb3727a5`. **6.0 metered seconds** (expected about 5,
  cap 60). The response's `device_usage_s` is also 6. Queued to running
  in 0.06 s; the run was late evening.
- **Cost and queue evidence only.** B1 fails A31's spread test and its
  optimum is uniform, so its weight cosine of 1.0 is not a fidelity
  result.
- **The first attempt spent nothing.** The runner did not accept the
  `.env` key name `QCI_API_KEY`, so it exited before any submit. Fixed to
  match `run_hardware.py` (commit `c39a0f4`, test proven red), then run.
- **Every stop is idempotent and capped**: one attempt per unit, a pre-
  submit check of the Hamiltonian and the B4 screen, the raw response
  saved before post-processing, and no unit resubmitted once it has a row
  or a ledger entry.
- Stops 2 and 3: see the decisions at the end of this file.

## V5. Task E (F147): the evidence-library query tool

Read `docs/phase2/F147_EVIDENCE_LIBRARY_DIRAC3S.md`.

- `scripts/edb_query.py` opens the library read-only, two independent
  ways. A test proves a write fails, red only when both are removed.
- The note cites seven records that bear on F142. The main one: the
  CVQBoost fidelity match holds only at small pools (cosine 0.975-0.999 up
  to 91 variables, 0.82-0.90 at 560-833).
- `docs/phase2/EDB_PROPOSALS.md` gains P4, for a session in
  EvidenceBasedDB. Nothing was written to the library.

## V6. Task F (F126): a threshold rule does not predict the device's zeros

Read `docs/phase2/F126_SPARSITY_RULE.md`.

- **The pre-set rule fails.** Fitted on oilgas, it predicts telecom within
  0.016; fitted on telecom, it misses oilgas by 0.847. It had to pass
  both ways.
- On oilgas the exact optimum is near-uniform, so the rule fits only in a
  tau window about 0.002 wide. Telecom's fit cannot locate it.
- About 94% of learners sit near the tie, and at least about 60% of the
  device's zeros fall in that group. A rebuild alternative stays open.

## V7. Task G (F105): the Experiment 2 harness on IEEE-CIS, no score

Read `docs/phase2/F105_IEEE_HARNESS.md`.

- **Every audit passes on all three folds**, 590,537 rows: no feature
  encodes the entity key; aggregates do not move when evaluation values
  are scrambled; frequency columns match training-only recomputation;
  random-halves AUC 0.499-0.500 (limit 0.55).
- **The drift is larger than Phase 1's control removes**: the adversarial
  control stops at its 20-round cap at 0.945, 0.888 and 0.887, the same
  values Phase 1 recorded. Experiment 2's entry must decide how to treat
  it.
- **Month 6 holds only 8,111 rows.** Experiment 2's entry must say whether
  it counts as a fold.
- No model score is computed anywhere; a test enforces it.

## V8. Task H (F146): the Dirac understandings, kept current

- First update after A: clients pinned, a "Checked offline" label, five
  offline findings.
- Second update after stop 1: section 2 gains "Measured" (cost, queue,
  device name and metrics key confirmed, B1 not a fidelity result).

## V9. What the reviews found

- **Code review: 16 findings, all addressed** before any Dirac-3S call.
  The metered path gained opt-in single attempts, a `NoRetry` exception
  and a zero-cost charge; the runner gained the pre-submit check, the
  raw-response save, row-before-scoring, the lock and the cap seeded from
  earlier spend.
- **Fresh-eyes evidence review: 16 findings, all addressed.** It found a
  Sprint 25 error: "uniform even at lambda = 0" had been withdrawn by A27.
  Corrected in `F29_SAMPLE_SIZE.md`, the Phase 2 draft section 2,
  `DIRAC_UNDERSTANDINGS.md`, the master plan's F25, F147 and P4. The
  fidelity match is now scoped to pools of up to 91 variables.
- Every new guard was proven red before it was trusted.

## Acceptance criteria, walked

- **F141**: offline dry run names `dirac-3s` in both venvs, no device
  call; row-schema test proven red; proxy identity on 0.22.1. **Met.**
- **F145**: two seeded builds byte-identical, proven red by removing the
  seed; drift recorded in the draft's section 7. **Met.**
- **F144**: paired difference against B2's 10 device rows with its
  interval; whether the device beats its proxy; stated that this twins the
  configuration, not B2's unstored pools. **Met.**
- **F142**: rows are dated Phase 2 rows naming the device, never Phase 1
  gate cells; B1 reported as cost and queue only, with its failed screen
  beside it. **Met for stop 1.** B2 and B4 depend on stops 2 and 3.
- **F147**: a text query and an id lookup on the live library; a write
  through the tool fails, proven red; one note cites its records;
  `EDB_PROPOSALS.md` updated; nothing written to the library. **Met.**
- **F126**: held-out error against 0.05 in both directions; fit and test
  never on the same fits. **Met** (the rule fails).
- **F105**: harness built and tested; random-halves AUC at most 0.55; no
  score reported. **Met.**
- **F146**: two updates, each with a revision-log row. **Met.**

## Metered decisions (Criterion H)

- **Decision 7, stop 1** (1 call, about 5 s, cap 60): approved 2026-10-14,
  option 1. Spent 6.0 s.
- **Decision 8, stop 2** (2 calls, re-quoted from stop 1): asked
  2026-10-15. Recorded here when answered.

## Effort, measured

From `.claude/sprint_status.json` `task_actuals` (minutes): A 75, B 3,
C 24, E 3, F 9, G 66. B is understated: its test was written before its
timer started. D and H are recorded at close.
