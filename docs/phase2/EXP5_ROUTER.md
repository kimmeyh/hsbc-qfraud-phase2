# Experiment 5: segment transfer and router acceptance, on the proxy

Sprint 31 Task H (#100), F121. Run 2026-11-05 on F174's stored month-4
scores: zero metered seconds, no model fitted. The entry is "Experiment 5"
in `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, committed
before the module and before any score below. The hold of record was set
aside by the team lead (Sprint 31 D3 option 2). Every figure here is in
`experiments/phase2/results/exp5_router.json`.

## BLUF

**No segment is accepted, for the proxy or for the classical reference.**
The router criterion (a mean edge of at least 0.01 over the champion,
LightGBM, and a 99% interval of edge minus the matched control wholly
above 0) accepts no ProductCD segment for HGB and none for the CVQBoost
proxy. The reference check passed its purpose: HGB was not accepted, so
the run went on to the proxy, as the entry sets.

**The measure cannot show an edge on most segments.** On segments C, R
and S, the champion's recall within the segment is already as high as the
segment's 0.5% alert budget allows: every alert is a fraud. A lane can tie
it and cannot beat it, so its edge is 0 or below by construction. Segment
W cannot be scored at all. This is a property of the design, found after
the result, and it is the main thing this run teaches.

## What ran

- **Alignment check**: passed; every lane's stored labels match the
  champion's row for row.
- **Segments** (test rows on month 4): W 69,566; C 8,874; R 3,245;
  H 2,270; S 1,347.
- **Seeds**: 42 to 51; 20 control draws per seed.

## The classical reference (HGB in the proxy's place)

- **W**: not feasible on any seed. Its matched control draws a segment of
  the same size from the rows outside W, and only 15,736 test rows lie
  outside it, against W's 69,566.
- **C**: mean edge 0.0; edge minus control 0.000125, interval
  [0.0000337, 0.000216]. The interval is above 0 and the edge is below
  0.01: not accepted.
- **R**: mean edge 0.0; edge minus control 0.00211, interval [0.00067,
  0.00355]. The same pattern: not accepted.
- **H**: mean edge -0.0037; interval [-0.0081, 0.0011]. Not accepted.
- **S**: mean edge -0.0047; interval [-0.0195, 0.0118]. Not accepted.

The minimum-edge clause is what kept HGB out on C and R. With the
interval clause alone, the criterion would have accepted the classical
reference on two segments, and so could not have told a proxy edge from
a tie.

## The proxy (CVQBoost, F174's stored scores)

- **W**: not feasible, as above.
- **C**: mean edge -0.0069; interval [-0.0084, -0.0034]. Below the
  champion, reliably.
- **R**: mean edge 0.0; interval [0.0025, 0.0047]. Not accepted.
- **H**: mean edge -0.0126; interval [-0.0140, -0.0066]. Below the
  champion, reliably.
- **S**: mean edge 0.0; interval [0.0006, 0.0034]. Not accepted.

## Why most edges are exactly 0

At a 0.5% budget a segment's alerts are few: about 44 on C, 16 on R, 11
on H and 6 on S, against 1,123, 161, 135 and 86 frauds. On C the
champion's recall within the segment is 0.0401 (seed 42), on R 0.106 and
on S 0.0814: each is the alerts it is allowed divided by the frauds, so
every alert is a fraud. HGB and the proxy reach the same figure on R and
S, and HGB on C, which is why their mean edges are 0.0 to the stated
places. Only on H, where the champion misses, and on C for the proxy, do
the lanes differ, and there they are below it. (The alert counts are
rounded from 0.5% of the segment's rows; ties at the threshold can add
one, which is why a recall can sit slightly above that ratio.)

A segment router can only gain where the champion's top alerts are not
all fraud. At this budget that is rare on IEEE-CIS month 4, so recall at
the budget within a segment is a weak measure here. This was not foreseen
in the entry. A redesign is a matter for the backlog: for example, the
budget set per segment from its own rate, or a measure that ranks beyond
the budget (AUPRC within the segment). It is not applied to this result.

## Reading

- Experiment 5, as preregistered, does not support a segment router on
  IEEE-CIS month 4, for the proxy or for HGB.
- The result is reported under a set-aside hold (D3). It neither lifts
  nor confirms the hold's original condition, which asked for a Phase 2
  run showing a segment edge.
- Outcome blocks (confusion counts at the 0.5% budget, per-row score
  hashes) are in the result file's `outcomes`.
