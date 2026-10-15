# F142: The First Dirac-3S Fits, Cost and a B4 Twin

**Sprint 26 Task D**, 2026-10-14 and 2026-10-15. **86.0 metered seconds**
over five fits in three stops, each approved separately (Decisions 7, 8
and 9). Rows: `experiments/phase2/results/f142_dirac3s_verify.json` (tag
HW). Readout: `experiments/phase2/results/f142_readout.json`, from
`experiments/phase2/src/f142_readout.py` (HW samples with SIM exact
solves). The entry, its falsifier band and its stopping rules were written
before any call (`experiments/phase2/PREREGISTRATION_DRAFT.md` section 6,
F142).

**Who reads this**: the team lead, and anyone quoting Dirac-3S cost or
comparing the two devices.

Device interpretations here are this project's independent findings.
QCi has not validated them.

## Bottom line

1. **On B4, Dirac-3S returned the exact optimum; Dirac-3 did not.** Weight
   cosine against the exact solve: 0.99999 and 1.0 on seeds 42 and 43,
   against Dirac-3's 0.895 and 0.901. Both fall outside the band set
   before the call, [0.8832, 0.9095], so **the falsifier fires**: "Dirac-3S
   behaves as Dirac-3 on B4" is contradicted. With 2 fits this is
   descriptive, not a test, as the entry says. The objective gap to the
   proxy optimum is at most about 1 part in 10 million; on seed 42
   the device's objective is 0.0026 lower than the reference solve's, so
   that solve is not exact at this precision. **Measured**:
   `b4[*].dirac3s.weight_cosine_vs_exact`, `objective_device`,
   `objective_exact`, `falsifier_fires`.
2. **It is not the uniform vector.** B4's exact optimum is near-uniform,
   so a plain 1/560 vector already scores cosine 0.993. Dirac-3S's
   departures from uniform correlate 0.9998 and 0.99999 with the
   optimum's, and it zeroes the same 3 learners the optimum zeroes, on
   both seeds. Dirac-3's lowest-energy samples zeroed 14-16% of learners.
   **Measured**: `deviation_correlation_vs_exact`,
   `zeros_shared_with_exact`, `dirac3.zero_fraction_lowest_energy_sample`.
   The uniform baseline was added after the result; it is the reason the
   cosine alone could not carry this point.
3. **The structure it reproduced is far below A31's weight step.** The
   optimum's median departure from uniform is about 0.00004, about 1/120
   of the 0.005 step that the 200:1 figure implies. So the returned
   weights are not limited to that step. Either Dirac-3S's effective
   output resolution is much finer than 200:1, or the returned values are
   post-processed toward the optimum. The response holds `solutions` only,
   with no raw field, and QCi states its "error correction" is a
   post-processing step. Which one is **Unverified**; question A6 asks
   about resolution. **Measured** (the departure); **Inferred** (the two
   readings).
4. **Accuracy did not change.** Test AUPRC 0.8522 and 0.8418 on Dirac-3S,
   0.8526 and 0.8408 on Dirac-3; in-segment AUPRC 0.7912 and 0.7901,
   against 0.7918 and 0.7889. Both devices remain far below the random
   control (0.974-0.976), as in Phase 1. The Dirac-3 rows were scored on
   unseeded builds of the same cell and seed, so the pools differ; the
   comparison is of the configuration, as F144's was. **Measured**.
5. **Cost.** Billed seconds equal the per-sample run times summed and
   rounded up on every job where both were recorded (4 of 5; stop 1
   predates the timing field), the rule Phase 1 measured on Dirac-3. Per
   sample at relaxation schedule 2: about 0.75 s at 91 variables, 2.6 s at
   560 and 3.83 s at 833. Per fit, against Dirac-3: B1 6 s (about 4.5),
   B4 21-22 s (34-46), B2 31 s (about 82). Queues were under 1 s, all
   late evening or after midnight. **Measured**: `cost[*]`.

## The five fits

| Stop | Unit | Variables | Screen | Metered s | Cosine vs exact | Note |
|---|---|---|---|---|---|---|
| 1 | `b1_42` | 91 | fails | 6.0 | 1.0 | uniform optimum; cost only |
| 2 | `b1_43` | 91 | fails | 6.0 | 1.0 | uniform optimum; cost only |
| 2 | `b2_42` | 833 | fails | 31.0 | 1.0 | near-uniform optimum; cost only |
| 3 | `b4_oilgas_42` | 560 | passes (37 steps) | 22.0 | 0.99999 | the twin |
| 3 | `b4_oilgas_43` | 560 | passes (37 steps) | 21.0 | 1.0 | the twin |

The re-quotes held: stop 2 spent 37 s against about 115, stop 3 spent 43
s against about 44. The first stop 1 attempt spent nothing: the runner did
not read the `.env` key name and exited before any submit (fixed in
`c39a0f4`).

## What this changes

- **A31's second half may not apply to Dirac-3S.** A31 predicted that a
  device returns a sparser vector than an optimum whose weights sit below
  the step. Dirac-3 did; Dirac-3S did not, on B2 or B4. Any plan that
  assumed forced sparsity on Dirac-3S (F126's model, F25's ridge
  discussion) should be re-read against this. **Inferred.**
- **It does not make CVQBoost better.** The returned weights moved from
  0.90 to 1.0 cosine and the test scores did not move. The binding limit
  is still the formulation (F94).
- **F104's screen still matters for reading.** B1 and B2 fail it, so their
  agreement with a uniform optimum carries no resolution information. B4
  passes, which is why only B4 separates the two readings above.
- **Cost model for Dirac-3S at schedule 2**: per-sample time grows with
  size (0.75, 2.6 and 3.83 s at 91, 560 and 833 variables). Per fit,
  Dirac-3S is dearer than Dirac-3 at 91 variables and cheaper at 560 and
  833. Three sizes, one or two fits each; not a rate for other schedules.

## Limits

- Five fits; two are the twin. No test is run on them.
- One dataset for the twin (oilgas_gasturbine).
- Every queue time was taken late at night.
- The exact optimum is F126's cached solve of the same seeded pool. The
  readout refuses to run unless the row's own cosine, computed at fit time
  against the sent Hamiltonian, matches it.
