# F142: The First Dirac-3S Fits, Cost and a B4 Twin

**Sprint 26 Task D**, 2026-10-14 and 2026-10-15. **86.0 metered seconds**
over five fits in three stops, each approved separately (Decisions 7, 8
and 9). Rows: `experiments/phase2/results/f142_dirac3s_verify.json` (tag
HW). Readout: `experiments/phase2/results/f142_readout.json`, from
`experiments/phase2/src/f142_readout.py` (HW samples with SIM exact
solves). The entry, its falsifier band and its stopping rules were written
before any call (`experiments/phase2/PREREGISTRATION_DRAFT.md` section 6,
F142). Revised the same day after a fresh-eyes review (9 findings, all
addressed); everything in the readout's `b4_structure` was added then.

**Who reads this**: the team lead, and anyone quoting Dirac-3S cost or
comparing the two devices.

Device interpretations here are this project's independent findings.
QCi has not validated them.

**Two kinds of resolution.** *Input* resolution is whether the device can
tell the Hamiltonian's coefficients apart; A31's spread test (the F104
screen) checks it. *Output* resolution is how finely the returned weights
can differ; A31's second half put it at the 0.005 step implied by 200:1.
B1 and B2 fail the input test; B4 passes it. All three say something
about output resolution.

## Bottom line

1. **On B4, Dirac-3S returned the reference optimum in every sample;
   Dirac-3 did not.** Weight cosine against the reference QP solve:
   0.999993 and 0.9999999 on seeds 42 and 43, the same in all 8 samples
   of each job, against Dirac-3's 0.895 and 0.901. Both fall outside the
   band set before the call, [0.8832, 0.9095], so **the falsifier fires**:
   "Dirac-3S behaves as Dirac-3 on B4" is contradicted. With 2 fits this
   is descriptive, not a test. The Dirac-3 figures come from unseeded
   builds of the same cell and seed (different pools, each scored against
   its own solve), and the baselines in item 2 were run on Dirac-3S only.
   **Measured**: `b4[*]`, `b4_structure[*].per_sample`, `falsifier_fires`.
2. **It is the optimum's structure, not a near-uniform guess.** B4's
   optimum has 438 and 442 of 560 weights on one plateau; 122 and 118 lie
   below it, 3 of them zero. Two baselines, both added after the result:
   - a plain 1/560 vector scores cosine 0.993;
   - a vector uniform except at the optimum's 3 zeros scores 0.9957 and
     0.9953, and its departures from uniform correlate only 0.62 and 0.60
     with the optimum's.

   Dirac-3S's departures correlate 0.99976 and 0.99999, and every sample
   zeroes the same 3 learners as the optimum. Dirac-3's lowest-energy
   samples zeroed 14-16% of learners. **Measured**: `b4_structure[*]`,
   `b4[*].dirac3.zero_fraction_lowest_energy_sample`.
3. **The returned weights are far finer than the 0.005 output step.**
   Every Dirac-3S weight is within 0.000094 (seed 42) and 0.0000062 (seed
   43) of the reference, about 1/53 and 1/800 of the step. **Measured**
   (`max_abs_error_vs_exact`, `max_abs_error_in_a31_steps`). Three more
   facts bear on why:
   - the 8 samples of each job agree to 0.0000003 in every weight, and
     to 0.0000005 or better on all five jobs (`cost[*]` and
     `b4_structure[*]`, `max_spread_between_samples_per_weight`);
   - every returned value on all five jobs is a multiple of 0.0000001
     (`all_values_on_1e-7_grid`); the best B4 sample holds only 93 and 96
     distinct values;
   - sample sums run from 0.99999 to 1.000003.

   **Inferred**: these weigh toward post-processing (for example a
   normalization or projection onto the sum constraint, or QCi's stated
   "error correction" step) rather than an analog output resolution of
   about 1 part in 10 million, repeated exactly across stochastic samples.
   **Unverified which.** QCi states raw values come back too; this cloud
   response has no raw-values field (`results` holds `counts`, `energies`
   and `solutions`). Question A6 asks about resolution.
4. **Accuracy did not change.** On the same seeded pools, the reference
   solve and the device score the same test AUPRC: 0.85224 and 0.85225
   (seed 42), 0.84180 and 0.84180 (seed 43) (`test_auprc_scored_from_pool`).
   Against Dirac-3's rows (different pools): 0.8526 and 0.8408; in-segment
   AUPRC 0.7912 and 0.7901 against 0.7918 and 0.7889. Both devices remain
   far below the random control (0.974-0.976), as in Phase 1. **Measured.**
5. **The reference solve is not exact at this precision.** The 8 samples
   cannot be ranked: reported energies are single precision, about 0.006
   below the recomputed objective, and order the samples differently from
   it. Device objective minus reference: -0.0029 to -0.0025 on seed 42,
   -0.00036 to +0.00013 on seed 43, so the device beats the reference on
   both seeds, in at least one sample. The reference (accelerated
   projected gradient) is less converged on seed 42: its gradient spread
   on the support is 16, against 1.1 on seed 43. Seed 42's 0.999993 is
   limited by the reference, not the device. **Measured**:
   `per_sample[*].objective_minus_reference`,
   `reference_solve_kkt_gradient_spread_on_support`.
6. **Cost.** Billed seconds equal the per-sample run times summed and
   rounded up on every job where both were recorded (4 of 5; stop 1
   predates the timing field), the rule Phase 1 measured on Dirac-3. Per
   sample at relaxation schedule 2: about 0.75 s at 91 variables, 2.6 s at
   560 and 3.83 s at 833. Per fit, against Dirac-3: B1 6 s (about 4.5),
   B4 21-22 s (34-46), B2 31 s (about 82). Queues were under 1 s, all
   late evening or after midnight. **Measured**: `cost[*]`.

## The five fits

| Stop | Unit | Variables | Input screen | Metered s | Cosine vs reference | Note |
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

- **A31's second half (output resolution) does not describe Dirac-3S's
  returned values.** A31 predicted a sparser vector than an optimum whose
  weights sit below the step. Dirac-3 returned one; Dirac-3S did not, on
  B2 (weights of 0.0012, about a quarter step, returned within 0.032%) or
  B4. Plans that assumed forced sparsity on Dirac-3S (F126's model, F25's
  ridge discussion) should be re-read against this. Whether the device or
  a post-processing step produces it is open (item 3). **Inferred.**
- **Input resolution is a separate question, and only B4 tests it.** B1
  and B2 fail the spread screen: the device may see a nearly symmetric
  problem, whose answer is uniform, so their uniform returns say nothing
  about input resolution. B4 passes the screen, and its returned weights
  follow coefficient differences of about 37 steps.
- **It does not make CVQBoost better.** On the same pools, the device and
  the reference score the same AUPRC. The binding limit is still the
  formulation (F94).
- **Cost model for Dirac-3S at schedule 2**: per-sample time grows with
  size (0.75, 2.6 and 3.83 s at 91, 560 and 833 variables). Per fit,
  Dirac-3S is dearer than Dirac-3 at 91 variables and cheaper at 560 and
  833. Three sizes, one or two fits each; not a rate for other schedules.

## Limits

- Five fits; two are the twin. No test is run on them.
- One dataset for the twin (oilgas_gasturbine).
- Every queue time was taken late at night.
- The reference optimum is F126's cached solve of the same seeded pool.
  The readout refuses unless the row's own cosine matches it, and rebuilds
  each pool and refuses unless its Hamiltonian hashes to the one the dry
  run recorded and the runner sent.
