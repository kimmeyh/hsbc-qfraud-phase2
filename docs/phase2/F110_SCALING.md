# Experiment 6 (F110): training time against sample count, the result

Sprint 28 Task E (#52), 2026-10-22. Zero metered seconds. The entry is
`experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "Experiment 6",
committed before any timing, with a dated implementation note and a dated
correction, both made before any slope. Every figure below is in
`experiments/phase2/results/f110_scaling.json`. Code:
`experiments/phase2/src/f110_scaling.py`; test:
`experiments/src/test_f110_scaling.py`. Evidence tag `SIM`. Wall clock on
this machine (32 logical processors); the pool is built serially
(`full_pair_pool.py`, the entry's implementation note).

## BLUF

**P1 is false at both cell sizes. The pool build is the largest part at
every row count, as predicted, but it grows faster than linearly in rows.**
Its log-log slope is about 1.4, and both 97.5% intervals are above the
predicted band [0.7, 1.3].

**P2 holds at 833 variables. At 91 variables it fails under the committed
rule, because the timer cannot measure that solve.** At 833 variables the
solve is flat in rows, at about 0.35 s. At 91 variables it takes 0 to 4 ms,
and 9 of 20 solves are below the timer's resolution. The interval is
therefore too wide to read. This is a failure of measurement, not evidence
that the solve grows.

**At full rows, a serial 833-variable build takes about 13 minutes.** That
is close to the hardware plan's 735.4 s. The full training at about
150,000 rows is several hundred seconds on this proxy, against the paper's
2 s (see "Beside the predictions").

## Results (Measured, `SIM`)

Five seeds per cell (42-46), four row fractions, 20 runs per cell. The
833-variable pilot (seed 42) projected 79.4 minutes for seeds 43-46,
inside the 120-minute cap, so the five-seed run went ahead. It took
82.4 minutes.

- **Pool build, slope (97.5% interval)**:
  - 91 variables: 1.40 [1.35, 1.45]. P1 band [0.7, 1.3]: outside.
  - 833 variables: 1.44 [1.38, 1.49]. Outside.
  - The build is the largest part at every fraction in both cells.
- **Hamiltonian construction (H plus J), slope**, reported with no
  prediction:
  - 91 variables: 0.93 [0.86, 0.99].
  - 833 variables: 0.95 [0.84, 1.06].
- **Solve, slope**:
  - 91 variables: 0.03 [-1.06, 1.13]. P2 band [-0.2, 0.2]: outside, by
    width. 9 of 20 solves were clamped (`solve_clamped`); the slope uses
    a 0.1 ms floor for those rows, as the code states.
  - 833 variables: -0.03 [-0.13, 0.07]. Inside. No solve was clamped.
- **Mean seconds by fraction, 91 variables** (17,023 / 42,559 / 85,118 /
  170,235 rows):
  - build 2.41 / 8.68 / 22.8 / 59.6
  - construction 0.06 / 0.12 / 0.24 / 0.51
  - solve 0.001 / 0.001 / 0.001 / 0.002
- **Mean seconds by fraction, 833 variables**, same rows:
  - build 28.4 / 115 / 301 / 773
  - construction 0.58 / 0.99 / 2.07 / 5.12
  - solve 0.40 / 0.35 / 0.37 / 0.36
- **Spread across seeds at full rows**: build 58.2-62.0 s (91 variables),
  745-812 s (833 variables).

## Beside the predictions (the entry's two comparisons)

- **The hardware plan's 12 minutes.** Our serial build at 833 variables
  and full rows is 773 s on average (745-812 s), about 5% above the plan's
  single 735.4 s build (`SPRINT_12_PLAN.md`). Inferred, unverified: the
  plan's build was serial too, because a build parallel across 32
  processors would be expected to be much faster. The plan did not record
  how it built the pool, so this stays an inference.
- **The paper's 2 s at 150,000 rows.** Our 100% fraction has 170,235
  rows. Scaled to 150,000 rows along the measured build slope, the full
  training is about 650 s at 833 variables and about 50 s at 91 variables.
  That scaling is an inference from the fitted slope, not a measurement.
  If the build were divided by the processor count (32), an ideal that a
  real parallel build does not reach, the 833-variable training would
  still be about 20 s; the 91-variable training would be about 2 s. The
  comparison is not like for like: the paper's pool size, weak
  learners and hardware are not stated in what we hold
  (`docs/evidence-inventory.md`, section 3a), and its 2 s may exclude the
  pool build. That is unverified.

## What this changes

- **The cost of a device fit at 833 variables is the build, not the
  device.** About 13 minutes of serial CPU per fit at full rows, against
  0.35 s for the proxy solve. Halving the training rows cuts the build by
  about 2.7 times, not 2 times, because the slope is about 1.4.
- **P1's linear growth is refuted for this builder.** A plan that scales
  the build linearly in rows underestimates it at larger row counts.
- **P2 at 91 variables needs a finer timer or repeated solves** before it
  can be read. The committed rule's result stands as recorded: fail.

## What was not done

- No device arm. The entry excludes it from this sprint.
- No parallel build. The library's parallel builder needs `fork`, which
  Windows lacks, and the only Linux venv does not match the lock
  (`docs/ENVIRONMENT.md`).
- The two rows timed before the dated correction were discarded and are
  not in the result file. The entry records why.
