# F188: Do F176's Below-Greedy Gains Survive the Device's Resolution?

**Card**: F188 | **Sprint**: 32, Task C (#112) | **Metered seconds**: 0
**Entry**: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F188"
(written 2026-11-09, before any run), and its amendment of the same day
(written after the first reading, before the second)
**Results**: `experiments/phase2/results/f188_rounding.json` (the
registered reading) and `experiments/phase2/results/f188_rounding_delivered.json`
(the amendment's reading)
**Generator**: `experiments/phase2/src/f188_rounding.py`
**Source instances**: `experiments/phase2/results/f176_below_greedy.json`

## Bottom line

- **The registered reading is "kept" on two instances** (42/free and
  43/free), which by the entry means the device question stays open
  there. That reading measures gains on the rounded problem, and those
  gains are 49 to 73 times F176's: they come from the rounding (below).
- **The amendment's reading (Measured)**: at R = 200, the weights a
  device can represent, scored on the real problem, are worse than
  classical greedy's result on all six instances. On each of the three
  instances where F176 found a gain, the loss is larger than that gain:
  42/free loses 0.000024 against a gain of 0.000018, 42/mid 0.000056
  against 0.000003, 43/free 0.0012 against 0.000017.
- **What this suggests (Inferred, not a registered rule)**: a device run
  on F25's IEEE-CIS design at 200:1 cannot beat classical greedy, so
  F25's IEEE-CIS case could be closed. The amendment registered no
  decision rule, so closing it is the team lead's decision, not this
  result's. The 200:1 figure is QCi's, carried to Dirac-3S and not
  measured there; at 400:1 one instance (43/free) delivers a small gain,
  and no R above 400 was run.

## What was done

- **Instances**: F176's six IEEE-CIS instances (seeds 42-44, `free` and
  `mid`), rebuilt with F176's code; each rebuilt greedy objective
  matched F176's record before anything was read.
- **Rounding**: every coefficient rounded to the nearest multiple of
  max |coefficient| / R, at R = 100, 200 and 400 (200 is the reading).
- **Supports**: every selection F176 recorded per instance (greedy, the
  swap search, three annealing runs, SCIP), with its weights solved
  again on the rounded problem. No search was run again.
- **Check first**: on F176's exact-size check cases where greedy is not
  optimal, every gain was kept with no rounding and lost at R = 2 (7
  cases). The test can fire.

## What it found

- **The registered reading** (gain measured on the rounded problem):
  - F176 found a gain below greedy on three instances. At R = 200,
    42/mid's is lost. On 42/free and 43/free the rounded problem prefers
    another selection by 0.0009 and 0.0012: 49 and 73 times F176's gain,
    and under a tenth of one rounding step. On 42/free it is kept at
    R = 100 and 200 and lost at 400; on 43/free it is kept at all three.
    As registered, the reading is "kept" on those two.
  - A gain that grows under rounding, and does not shrink steadily as
    the rounding gets finer, is made by the rounding, not by F176's
    selection. The amendment was written to separate the two.
- **The amendment's reading** (what the device would return, scored on
  the real problem): the rounded problem's best selection, with the
  weights it gives, is worse than greedy's real result on all six
  instances at R = 100 and R = 200. The loss has two sources:
  - **The weights.** At R = 200 the rounded problem picks F176's own
    best selection on 42/free and 42/mid. Those selections beat greedy
    with their real weights; the weights solved on the rounded problem
    lose more than the gain.
  - **The pick.** On 43/free at R = 200 the rounded problem picks SCIP's
    selection, the worst of F176's six methods on the real problem. At
    R = 100 and 400 it picks the right one, so the pick changes with R.
  - On three instances (43/mid, 44/free, 44/mid) the pick is greedy
    itself, and the loss is only the rounded weights; F176 found no gain
    there.
  - At R = 400, 43/free delivers a gain; the other five do not.

## What it means

- At 200:1 the device can often find the right selection but cannot
  hold the weights finely enough to keep a gain this small, and on one
  instance it finds the wrong selection. Any Dirac-3S run on this
  formulation would read rounding, not the room F176 measured (Inferred).
  Whether that closes F25's IEEE-CIS case is the team lead's decision;
  it would reopen if the device's effective resolution were shown to be
  about 400:1 or finer.
- The general rule F188 adds: before a device run is proposed on a
  formulation, score the rounded problem's pick on the real problem.
  F104's gate asks whether the coefficients can be told apart; this asks
  whether telling them apart matters for the answer.
- Not tested: other weights (lambda), other instance sizes, R above
  400, or the device's own rounding, which QCi does not document beyond
  200:1. The step is the same on every instance (0.015 at R = 200), so
  it is set by the same largest term each time, likely the lambda
  diagonal; a different lambda would change the step (Inferred).
- The check fired only at R = 2, a coarse setting; it shows the reading
  can say "lost", not where between 2 and 200 gains start to go. Two
  check cases carry the labels 42/free and 44/free because they are the
  first 20 learners of those instances.
