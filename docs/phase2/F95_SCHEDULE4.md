# F95: relaxation schedule 4 on Dirac-3S

Sprint 31 Task J (#102), 2026-11-05. Entry: "F95" in
`experiments/phase2/PREREGISTRATION_DRAFT.md` section 6. Evidence:
`experiments/phase2/results/f95_schedule4.json` (evidence tag HW,
complete), each response stored under
`experiments/phase2/results/device_samples/`; the entry's reading
against each twin, computed offline from stored samples, in
`experiments/phase2/results/f95_schedule4_twins.json` (Sprint 31 Task M,
#105). Approved per stop: D10 option 1 (stop 1) and D12 option 1
(stop 2).

## BLUF

**On the two fits with a Dirac-3S schedule-2 twin, schedule 4 does not
change the reading, by the entry's test; those two pools cannot tell
schedules apart, so this is weak evidence about schedule 4.** Both
twin-compared pools fail the resolution screen: their coefficients
spread over about 1/200 of what the device resolves, so any answer
scores near the optimum. The two 45-variable fits pass the screen but
have no same-device twin; their only schedule-2 history is on Dirac-3,
on another device, so they are reported beside it, not compared. The
card used 67.0 of its 120 metered seconds. There is no evidence for
schedule 4 on pools of this kind; device plans stay at schedule 2.

## Results (Measured)

Four fits, 8 samples each, one attempt each, none retried. Wall time
includes the queue.

- `b1_dct_42`, 91 variables (stop 1): 18.0 s, wall 31.8 s, job
  `6aec8ad8358b23d0cb37424b`. Screen: fail. Twin F142 `b1_42`,
  schedule 2, 6.0 s.
- `b1_dct_43`, 91 variables (stop 2): 18.0 s, wall 34.2 s, job
  `6aed0d9c358b23d0cb374256`. Screen: fail. Twin F142 `b1_43`,
  schedule 2, 6.0 s.
- `g0b_3_42`, 45 variables, `lg` learners (stop 2): 15.0 s, wall
  28.0 s, job `6aed0ddb358b23d0cb374257`. Screen: pass. Dirac-3
  schedule-2 history: 0.4133% gap to the exact optimum
  (`experiments/results/hw_dispersion.json`).
- `b1_lg_42`, 45 variables, `lg` learners (stop 2): 16.0 s, wall
  30.0 s, job `6aed0e12358b23d0cb374258`. Screen: pass. Dirac-3
  schedule-2 history: 0.0153%.

Per fit, the relative gap of each sample to the reference optimum
(`gap_min`, `gap_range` in each row) is under 3e-07 in size. Every
fit's best sample is slightly below zero, at or below the reference.
That is the reference solve's numeric tolerance, not a better solution.

The entry's test, for the two units with a twin
(`f95_schedule4_twins.json`): schedule 4 changes the reading only if
its best-sample gap differs from the twin's by more than the range of
the twin's per-sample gaps, recomputed from the twin's stored samples.
On `b1_dct_42` the difference is about 3e-15 against a twin range of
about 6e-08; on `b1_dct_43`, about -9e-09 against about 5e-08.
Neither changes the reading.

## Reading

- **What the entry lets us say**: on the two B1 91-variable pools,
  schedule 4 finds what schedule 2 finds. "No change" was the expected
  result. Both pools fail the resolution screen, so they could not have
  shown a difference; the test is weak here.
- **The 45-variable fits**: on Dirac-3S at schedule 4 they sit at the
  optimum; on Dirac-3 at schedule 2, `g0b_3_42` was 0.4133% away. The
  device and the schedule changed together, so this shows neither "no
  change" nor "schedule 4 helped".
- **Cost**: at 91 variables, 2.2 s per sample against the twins' 6.0 s
  for 8 samples (`experiments/phase2/results/f142_dirac3s_verify.json`),
  about three times as much. At 45 variables, 1.8 to
  2.0 s per sample, with no Dirac-3S schedule-2 cost to compare. Each
  call was quoted at 10 s in the ledger and cost 15 to 18 s; a later
  schedule-4 quote starts from these measured costs.
- **Limits**: four fits, two sizes and two learner types. The case where
  schedule 4 could help is a pool that passes the screen and where
  schedule 2 misses the optimum on the same device; none of these is
  such a pool.
- **Environment**: the device runs used the WSL interpreter that holds
  the QCi client (`/root/eqc-venv`), not this repository's locked one,
  as F142's did; its versions are in each result's provenance block.

## What this changes

- Device plans stay at schedule 2. F95 closes. A schedule test that can
  discriminate needs a pool that passes the screen with a same-device
  schedule-2 twin that misses the optimum; none is carded.
