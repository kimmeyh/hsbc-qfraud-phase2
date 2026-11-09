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

No. At QCi's stated resolution of about 200:1, no device run on F25's
IEEE-CIS selection design can deliver the gains F176 found. Rounding the
problem to what the device can see costs more, on every instance, than
the largest gain F176 found (under 0.00002): the selection the rounded
problem ranks best is worse than greedy on the real problem by 0.000016
to 0.0012. F25's IEEE-CIS case can be closed on this formulation. The
200:1 figure is QCi's, carried to Dirac-3S and not measured there; at
400:1, one instance (43/free) delivers a small gain.

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
    another selection by 0.0009 and 0.0012: 50 to 70 times F176's gain,
    and under a tenth of one rounding step. On 42/free it is kept at
    R = 100 and 200 and lost at 400. As registered, the reading is
    "kept" on those two.
  - A gain that grows under rounding, and does not shrink steadily as
    the rounding gets finer, is made by the rounding, not by F176's
    selection. The amendment was written to separate the two.
- **The amendment's reading** (what the device would return, scored on
  the real problem): the rounded problem's best selection, with the
  weights it gives, is worse than greedy's real result on all six
  instances at R = 100 and R = 200. At R = 200 on 43/free the rounded
  problem picks SCIP's selection, which on the real problem is the
  worst of F176's six methods. At R = 400, 43/free delivers a gain; the
  other five do not.

## What it means

- A device that sees only 200 levels cannot tell these selections
  apart. Any Dirac-3S run on this formulation reads rounding, not
  the room F176 measured. This closes F25's IEEE-CIS case as a device
  question, unless the device's effective resolution is shown to be
  about 400:1 or finer.
- The general rule F188 adds: before a device run is proposed on a
  formulation, score the rounded problem's pick on the real problem.
  F104's gate asks whether the coefficients can be told apart; this asks
  whether telling them apart matters for the answer.
- Not tested: other weights (lambda), other instance sizes, or the
  device's own rounding, which QCi does not document beyond 200:1.
