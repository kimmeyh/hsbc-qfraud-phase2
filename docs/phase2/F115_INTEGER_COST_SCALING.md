# F115: Integer Cost Scaling, Stated Correctly

**Sprint 28 Task I (#55).** Zero metered seconds. Audience: QCi, and anyone
who sizes integer-solver jobs from `docs/HARDWARE_PLAN_PHASE_2.md`.

## Bottom line

- **At a fixed level budget, integer cost grows more slowly than the
  variable count.** The fit in the hardware plan, `vars^0.75 x
  levels^0.52`, has a variable exponent below 1. **Measured**:
  `experiments/phase2/results/f115_cost_scaling.json`,
  `two_factor_fit.vars_exponent` (0.75).
- **Cost grows faster than the variable count only when the level budget
  grows with it.** That is the case when every variable has the same upper
  bound, as in four of the five probes (levels = 4 x variables). Then the
  exponents add: about 1.27. **Measured**: `two_factor_fit.exponent_sum`
  and `sum_only_fit_on_proportional_points`.
- **The hardware plan's sentence "Cost is also superlinear in variables"
  (`docs/HARDWARE_PLAN_PHASE_2.md`, line 160) is therefore true only for
  that case.** As written, it reads as a statement at a fixed level
  budget, and there the fit says the opposite. The document is FINAL
  (team lead, 2026-09-27) and was sent to QCi, so it is not edited. This
  document is the correction.
- **The split between the two exponents rests on one probe.** Four probes
  lie on the line levels = 4 x variables, so they fix only the sum.
  `probe_deep` (60 variables, 840 levels) is the only point off that line,
  and the fit passes through it exactly. So 0.75 and 0.52 are each as good
  as one measurement. **Measured**: `points_off_the_line` is
  `["probe_deep"]`, and its `relative_miss` is zero.

## What stays true

- **The controlled pair is the finding, and it stands.** `probe_deep`
  carries 1.4x more levels than `probe_high` and 2.5x fewer variables, and
  cost 2.3x less (71 s against 165 s). Variables drive cost more than
  levels. `docs/INTEGER_PROBE_RESULT.md` says this, and also calls the
  exponents "indicative only".
- **`INTEGER_PROBE_RESULT.md` is not edited.** Its line "The cost is
  superlinear in variables" sits in the section on why the round-1 line
  failed. Every round-1 and round-2 probe it discusses there had levels
  growing with variables, so in context it is true.
- **Sizing practice is unchanged**: price a block on variables and levels
  together, from measured anchors, never on levels alone.

## How the numbers were made

`experiments/phase2/src/f115_cost_scaling.py` reads
`experiments/results/integer_probe.json` (read only). `probe_small` ran
twice at the same cost and counts once, so there are five points. Least
squares on `log seconds = a + b log variables + c log levels` gives
b = 0.75, c = 0.52, R^2 0.953; the worst point misses by 45%.
`experiments/src/test_f115_cost_scaling.py` reproduces these from the
probe file and checks that only `probe_deep` sets the split.

## What would make the exponents firm

More probes off the levels = 4 x variables line: for example the same
variable count at two level budgets, at two sizes. Each costs metered
seconds and needs its own per-block approval. Nothing in this sprint
proposes them.

## Optional paragraph for QCi (Task K)

Task K's reply to QCi's review offer carries this as an optional
paragraph, for the team lead to keep or cut:

> One correction to our hardware plan. It says integer cost is
> "superlinear in variables". Our own fit, `vars^0.75 x levels^0.52`, is
> sublinear in variables at a fixed level budget; it is superlinear only
> when the level budget grows with the variable count. Also, four of our
> five probes had levels equal to 4 x variables, so the split between the
> two exponents rests on one probe. The controlled comparison (more
> levels and fewer variables cost less) is the result we stand behind.
