# F198: F188's Readings at Other Ridge Weights and Resolutions

Sprint 34 Task F (#140). Entry: amendment P2-A4 in
`experiments/phase2/PREREGISTRATION_AMENDMENTS.md`, committed before
the run (f03a99d). Result: `experiments/phase2/results/f198_extended.json`
(`SIM`, zero metered seconds). Generator:
`experiments/phase2/src/f198_extended.py`.

## Bottom line

- **No setting gives a gain that holds across resolutions.** Over 90
  settings (six instances, three ridge weights, five resolutions R), the
  filed release comparison passes on 17. No instance passes at all five
  R under any weight, and the passes do not grow or shrink with R in
  any order: 42/free at weight 1 passes at R = 100 and 1,600 and not
  between.
- **The gains are small.** The largest release-comparison gain is
  2.4e-05 (weight 1, R = 100, 42/free), about 3 parts in 100,000 of the
  objective. Six settings exceed 1e-05; all are on 42/free or 43/free.
- **Three instances never pass.** 43/mid, 44/free and 44/mid pass at no
  weight and no R.
- **This is descriptive.** It makes no test (P2-A4). It does not change
  the release rule's verdict at the filed setting (P2-A6), and no
  setting here opens the device arm: any device call needs its own
  dated amendment and per-block approval.

## What was run

F176's six IEEE-CIS selection instances (seeds 42-44, `free` and `mid`),
rebuilt with F176's code. The ridge weight was F176's 2.0 times 0.1, 1
and 10; R was 100, 200, 400, 800 and 1,600. F176's recorded supports
were reused, so at weights other than 1 they are candidates, not that
problem's best supports; greedy was rebuilt at each weight. Three
readings per setting:

- **Registered** (F188's first reading): best other support minus
  greedy, both on the rounded problem. "Kept" when below -1e-6.
- **Delivered** (F188's amendment): the rounded problem's pick, its
  weights solved on the rounded problem, scored on the real objective,
  against greedy solved on the real objective.
- **Release comparison** (the filed rule's form): the pick against
  greedy, both solved on the rounded problem and scored on the real
  objective. "Passes" when below -1e-6.

F188's check that "lost" can fire ran first at each weight: on all
three it was kept on every case unrounded and lost at R = 2 on seven
cases, so it can fire.

## Counts, out of 30 settings per weight

| Weight factor | Registered kept | Delivered | Release passes |
|---|---|---|---|
| 0.1 | 14 | 1 | 4 |
| 1 | 10 | 3 | 8 |
| 10 | 14 | 3 | 5 |
| All (of 90) | 38 | 7 | 17 |

The registered reading is "kept" far more often than the other two.
F188 found why: on the rounded problem the gain is mostly made by the
rounding, so that reading is not evidence of a gain on the real
problem.

## Where the release comparison passes

Per instance and weight, R = 100, 200, 400, 800, 1,600 (P = passes):

| Weight factor | Instance | Pattern |
|---|---|---|
| 0.1 | 42/free | `...PP` |
| 0.1 | 42/mid | `.P...` |
| 0.1 | 43/free | `..P..` |
| 1 | 42/free | `P...P` |
| 1 | 42/mid | `PP..P` |
| 1 | 43/free | `P.PP.` |
| 10 | 42/free | `...P.` |
| 10 | 42/mid | `..P.P` |
| 10 | 43/free | `...PP` |

Every other instance and weight passes at no R. At the filed setting
(weight 1, R = 200) only 42/mid passes, which agrees with the release
rule's own result (P2-A6).

## What it means

A device that resolves each coefficient to 1 part in R would see these
problems' best supports change with R in no stable direction, and the
best it could deliver over greedy is a few parts in 100,000 of the
objective. Gains of that size are near the tolerance and are not shown
to change any fraud-detection metric; none was computed. This bears on
whether F25's device arm is worth device seconds, which is a
refinement question for the team lead.

## Limits

- The supports are F176's, found at weight 1. At weights 0.1 and 10 a
  fresh search might find other supports; none was run (P2-A4).
- Six instances from one dataset (IEEE-CIS), one fold.
- The 200:1 resolution is QCi's figure for Dirac-3, carried to
  Dirac-3S and not measured there (F188).
