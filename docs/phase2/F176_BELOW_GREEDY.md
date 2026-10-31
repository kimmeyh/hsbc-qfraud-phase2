# F176: can a classical solver get below greedy on F160's IEEE-CIS instances?

Sprint 30 Task E (#79). Evidence: `experiments/phase2/results/f176_below_greedy.json`
(SIM, 0 metered seconds), generator `experiments/phase2/src/f176_below_greedy.py`.
Entry: the 2026-10-31 amendment to "Experiment 3" in
`experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, written before
the module existed (f74125d).

## Result

**Yes, on 3 of 6 instances, by very little.** The best selection found is
more than 1e-6 below greedy's objective on 42/free, 42/mid and 43/free.
On 43/mid, 44/free and 44/mid nothing beat greedy.

- **The gains are tiny next to the room.** On 42/free, simulated
  annealing from greedy (seed 43) reached -0.702763 against greedy's
  -0.702745; the gap to the floor stays about 0.097. The largest gain on
  any instance is under 2e-05, less than a five-thousandth of the gap between greedy and
  the floor.
- **Which methods did it.** Simulated annealing from greedy on both
  `free` instances (m 10, 60 learners); the swap search on 42/mid (m 25,
  136 learners).
- **SCIP did not beat greedy anywhere.** It stopped at its 1,200 s cap on
  all six, with a selection above greedy's (for example -0.701759 on
  42/free).
- **SCIP's dual bound tightens the room only on the `mid` instances.**
  There it is above the floor of -0.92 (for example -0.9026 on 42/mid),
  so the room bound is about 0.081-0.084, not 0.098. On the `free`
  instances the dual bound is below the floor of -0.8, so the floor
  stays the bound.
- **The rebuild matched.** Each instance's greedy objective equals F160's
  recorded one within 1e-9, so these are F160's instances.

## The check, and what it shows about the method

On 26 small instances (20 learners choosing 4, solved exactly by
enumeration: the first 20 learners of each of the six instances, and 20
seeded random-sign instances), greedy is above the exact optimum on 7.
"Below greedy" can fire: the swap search reaches the exact optimum on 4
of the 7 (42/free, 44/free, random_0, random_11).

**On the other 3 (random_4, random_7 and random_12) the swap search stays
at greedy's value.** A one-for-one swap search is a local method: it
stops where no single swap improves. The module reads the amendment's
"on a case where greedy is above the exact optimum, the swap search must
reach it" as at least one case, and the check passes on that reading.
The misses matter for the three IEEE-CIS instances where nothing beat
greedy: there, "nothing below greedy" does not show that greedy is
optimal.

## What the result does not show

- **Not that the room is reachable in a useful amount.** The found gains
  are about 1e-05 against a room bound near 0.08-0.097. The rest of the
  room is not shown to exist: the floor and the dual bound are bounds,
  not attained values.
- **Not that greedy is optimal on the other three.** See the check above.
- No test score is computed; this is about the objective only.

## What it changes

- The amendment's reading: below greedy on some instance shows the room
  can be reached, so the device question becomes whether Dirac-3S reaches
  it faster or further. Reasonable inference, not tested: gains of about
  1e-05 may sit below what the device resolves (F104's resolution gate),
  so a device run would need to show it resolves differences of that
  size before it could show it goes further.
