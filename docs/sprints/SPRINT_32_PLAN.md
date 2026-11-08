# Sprint 32 Plan: Close a Device Question, State Results in Dollars, Tighten Two Guards

**Sprint**: 32 | **Branch**: `feature/20261108_Sprint_32`
**Planned**: 2026-11-08 | **Status**: DRAFT, for approval (D3).
Issues: A #110, B #111, C #112, D #113, E #114, F #115
**Scope**: F188, F181, F185, F194 and the F178 update (team lead
selection, 2026-11-08, D1: all five cards), then the F150 request draft
updated (D2 option 3: it is not sent, and F150 stays blocked).
**Metered seconds**: 0. No task calls a device or a paid service.

## Objective

Decide whether F25's IEEE-CIS design can still show a device result
(F188). Make the Dirac-3S-only rule a check (F181). Rank alerts by
dollars as well as by count (F185). Close the refusal gate's
line-coverage gap (F194). Then record the sprint in the learning
documents (F178) and bring the F150 request draft up to date.

- **Guards first** (F181, F194): small, and each is proven red in the
  commit that adds it.
- **Research next** (F188, F185): zero metered, from stored instances
  and stored scores.
- **F178 after every other step** (team lead, D2: "F178 should not be
  done until all the other steps complete"), so it records final
  results. **The F150 request update after F178** (D2).

## Decisions already made (team lead, 2026-11-08)

- **D1, scope**: a different set, all five cards.
- **D2, F150**: 3, "please update the request after this sprint (after
  F178 completes and F178 should not be done until all the other steps
  complete)". The timing this plan reads from it is asked in D3.

## Pre-kickoff (Phase 2)

- Sprint 31 merged to `develop` (PR #92) and released to `main` (PR
  #109). No sprint issue is open. The branch is the Sprint 31 branch
  plus the refinement and selection commits.
- Working tree clean before planning. CI's full job, red proofs
  included, is green on c9da7a4, the code this branch carries; the
  commits since change documents only. The local non-proof suite ran on
  88f81ce; its result is in the run output, not restated here.
- Dependency scan, 2026-11-08: `pip-audit` on the lock file
  (`--disable-pip --no-deps`; a full resolve passed its 500 s limit)
  finds no known vulnerability. `pip list --outdated` shows minor and
  major releases (eqc-models 0.22.3, scikit-learn 1.9.1, numpy 2.5.4,
  pandas 3.1.1, pypdf 7.0.0 and others), none with an advisory; none is
  proposed.

## Plan-to-branch-state verification (3.2.2.1)

Each card was checked against the repository on 2026-11-08. Probes were
read-only, zero metered, not evidence.

- **F181: confirmed.** No module under `experiments/phase2/src/` names
  `eqc_submit.DIRAC_3` (not `DIRAC_3S`). `test_phase2_device_default.py`
  accepts a `# device named:` line for either device (its `NAMED`
  pattern, `DIRAC_3S?`, and the `ok_named` fixture that names Dirac-3).
  The stricter guard passes the current tree; its red proof needs a
  mutation that names Dirac-3.
- **F194: confirmed, one design note.** `.coveragerc` has no
  `branch = True`. `refusal_coverage.py` reads diff-cover's JSON report,
  which lists lines, not branches. With branch coverage on, the partial
  branches are in `coverage.xml` (each line's missing branches), so the
  script reads them from there beside the JSON report. CI's push job
  limit is 12 minutes (`ci.yml`); branch measurement adds time, so the
  task measures the push job before and after.
- **F188: confirmed.** `f176_below_greedy.py` rebuilds the six IEEE-CIS
  instances from F160's seeded pools and holds the solvers.
  `f176_below_greedy.json` stores each method's support, objective and
  F176's reading (best gain against greedy, for example -1.81e-05 on
  seed 42's free instance). The 200:1 figure is QCi's stated effective
  resolution, carried forward to Dirac-3S and not measured there
  (`docs/phase2/DIRAC_3S_RESEARCH.md`). So the test rounds each
  instance's coefficients to 200:1 and re-evaluates the stored
  supports; no solver is re-run at its 1,200 s SCIP cap.
- **F185: confirmed, one finding.** The champions' per-row test scores
  are on disk (`experiments/phase2/predictions/f166_*.npz` for ULB,
  `f174_*.npz` for IEEE-CIS, gitignored), as `y_test` and `p_test` with
  no row identifier. The amounts are joined by rebuilding each module's
  seeded test split; the join is accepted only if the rebuilt labels
  equal the stored `y_test` and the file's SHA-256 equals the one in the
  result's outcome block. A review cost per alert is not on record: the
  entry states the values used before any run, and reports each.
- **F178: confirmed.** The three documents are in `docs/learning/`, and
  `test_learning_docs.py` checks them.
- **F150: confirmed.** The draft
  `docs/spectra_package/F150_CONSTRUCTION_REQUEST_DRAFT.md` exists and is
  gitignored (`.gitignore` line 76). It stays gitignored.

### Show each threshold can fire (Sprint 25 IMP-2, Sprint 28 IMP-5)

- **F181.** Fires: a Phase 2 module that names `eqc_submit.DIRAC_3` on a
  `# device named:` line. Proven red in the commit that adds the rule.
- **F194.** Fires: a refusal line with a missed branch; a `REFUSING`
  print with each of the `rf"`, `fr"` and `F"` prefixes. Does not fire:
  `: raise` inside a string on an `if` line. Each proven red.
- **F188.** Fires: F176's own check instance, where greedy is not
  optimal, at a resolution coarse enough that greedy's and the
  optimum's objectives round to the same value; the test must report
  the gain as lost there, and kept with no rounding. Run before any
  IEEE-CIS instance is read.
- **F185.** Fires: a constructed case where the high-amount frauds score
  low, so the dollar ranking catches more dollars than the count ranking
  at the same review count. Also: a stored score file whose labels do
  not match the rebuilt split is refused, not joined.
- **F178.** `test_learning_docs.py`'s existing checks; each new claim
  names a tracked source.

## Tasks

| Task | Card | What | Est | Runtime | Depends on |
|---|---|---|---|---|---|
| A | F181 | The guard refuses a Phase 2 module that names `eqc_submit.DIRAC_3` (not `DIRAC_3S`), on a `# device named:` line or not; the `ok_named` fixture changed; the docstring cites D5; proven red | 15 | - | - |
| B | F194 | `branch = True`; a refusal line with a missed branch fails the gate; the three print prefixes and the string case each tested; the CI comment and the docstring no longer state the line-coverage limit; the push job measured inside its 12 minutes; each proven red | 45 | one CI push job before and after | - |
| C | F188 | Each IEEE-CIS instance's gain before and after rounding to 200:1, from F176's instance builder and stored supports; the check instance first; the finding stated for any device run proposed on that formulation; result file with provenance; a short document | 30 | seconds (no solver re-run) | - |
| D | F185 | Entry first (review costs stated); the count ranking and the dollar ranking at the same review count on ULB (`Amount`) and IEEE-CIS (`TransactionAmt`), from the stored champion scores, joined only after the label and SHA-256 checks; dollars caught and confusion counts for each; result file with provenance and an outcome block; a short document | 60 | minutes (stored scores) | - |
| E | F178 | The per-sprint update: each document's next version and change list; C's and D's results under "What our experiments showed"; their placeholders in "Experiments planned" replaced; Sprint 33's planned runs added | 30 | - | every other step (D3) |
| F | F150 | The request draft updated with this sprint's results and the paper's title (`docs/references.md`); not sent | 15 | - | E |

**Derived total: 195 minutes of work**, the sum of the task estimates
(15 + 45 + 30 + 60 + 30 + 15): the five card estimates (180) plus the
F150 update at D2 option 2's 15 minutes. At Sprint 31's ratio of
actual to estimated minutes, 1.62 (range 0.04 to 4.75 by task), that is
about 315 minutes, unverified. Phase 3, the reviews and the
retrospective are not in these figures. The sprint is past the 1-2 hour
target; the team lead chose it (D1).

How each estimate was set (`docs/VELOCITY_LOG.md`): all five cards are
`[no-history]`; card estimates are kept, not reduced or inflated.
**Allowances**: none. E is prose about results, but only two new
results, each from a file this sprint writes.

### Task order

1. **A** (F181), then **B** (F194).
2. **C** (F188), then **D** (F185).
3. Phase 5: the suite by risk, the plan's criteria walked, fresh-eyes
   fixes.
4. **E** (F178), after every step that can change a result (D3).
5. **F** (F150), after E.

## Risks

- **F194 adds branch measurement to CI's push job.** If the job passes
  its 12-minute limit, branch coverage is measured on the changed files
  only, and the limit is not raised without a decision.
- **F185's join.** Amounts come from a rebuilt split. The label and
  SHA-256 checks refuse a mismatch; a refused dataset is reported as
  refused, not fixed by hand.
- **F185's review cost.** Not on record. The entry fixes the values
  before any score is read; the dollar ranking is reported at each.
- **F188's resolution.** 200:1 is QCi's stated figure, unmeasured on
  Dirac-3S. The result says so, and reports one coarser and one finer
  resolution beside it so the reading does not hang on one number.
- **D2's timing.** If "after this sprint" meant Sprint 33, D3 option 3
  moves the F150 update there.
- **CI is red until approval.** `test_phase3_artifacts.py` requires the
  issues and the approval once the status is `phase_3_planning`. That
  red is expected.

## Model assignments

Main loop (Opus, top tier) for all tasks. The suite runs in the
background, each run writing to a named file that is read in full when
it finishes.

## Definition of Done

- Every task's acceptance criteria are met.
- Each new rule, refusal and reported state has its own test, proven red
  in the commit that adds it.
- CI's full job is green on the final HEAD.
- Manual Validation items are listed on screen and saved in
  `SPRINT_32_VALIDATION.md`.
- Retrospective, `SPRINT_32_SUMMARY.md` at Sprint 33 planning, and the
  master plan updated.
