# F95: relaxation schedule 4 on Dirac-3S

Sprint 31 Task J (#102), 2026-11-05. Entry: "F95" in
`experiments/phase2/PREREGISTRATION_DRAFT.md` section 6. Evidence:
`experiments/phase2/results/f95_schedule4.json` (evidence tag HW,
complete), each response stored under
`experiments/phase2/results/device_samples/`. Approved per stop: D10
option 1 (stop 1) and D12 option 1 (stop 2).

## BLUF

**Schedule 4 made no difference on any of the four fits and cost about
three times as much per sample.** Every one of the 32 samples sits at
the reference optimum to solver precision, as schedule 2 does. The card
used 67.0 of its 120 metered seconds. Schedule 4 can be left out of
later device plans for pools of this kind.

## Results (Measured)

Four fits, 8 samples each, one attempt each, none retried:

- `b1_dct_42`, 91 variables (stop 1): 18.0 s; schedule-2 twin F142
  `b1_42`, 6.0 s.
- `b1_dct_43`, 91 variables (stop 2): 18.0 s; schedule-2 twin F142
  `b1_43`, 6.0 s.
- `g0b_3_42`, 45 variables, `lg` learners (stop 2): 15.0 s; Dirac-3
  history only.
- `b1_lg_42`, 45 variables, `lg` learners (stop 2): 16.0 s; Dirac-3
  history only.

Per fit, the relative gap of each sample to the reference optimum
(`gap_min`, `gap_range` in each row) is under 3e-07 in size. The
smallest gaps are slightly below zero, at or below the reference, which
is the device's numeric resolution, not a better solution.

## Reading

- **What the entry lets us say**: on two B1 91-variable pools and two
  45-variable `lg` pools, schedule 4 finds the same optimum schedule 2
  finds. "No change" was the expected result.
- **Cost**: 2.2 s per sample at 91 variables and about 1.8 to 2.0 s at
  45 variables (`device_timing` in each row). The 91-variable twins at
  schedule 2 took 6.0 s for their 8 samples
  (`experiments/phase2/results/f142_dirac3s_verify.json`).
- **Limits**: four fits, two sizes and two learner types. A pool where
  schedule 2 misses the optimum would be the case where schedule 4 could
  help; none of these is such a pool.

## What this changes

- Device plans stay at schedule 2. F95 closes.
