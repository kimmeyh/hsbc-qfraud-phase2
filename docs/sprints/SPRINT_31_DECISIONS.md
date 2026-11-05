# Sprint 31 Decisions

Every decision or question asked of the team lead in this sprint, in full,
as first asked. A question asked again is pasted from here unchanged: same
ID, same wording, same option numbers. If facts change after it is asked, a
dated "Changed since asked" note goes below the original; the original is
never edited. The answer is recorded under each entry.

---

## D1. Which cards make up Sprint 31?

Asked 2026-11-04 at backlog refinement Pass 2 (Phase 8.4).

**What.** Sprint 31's scope, from the 2026-11-04 slate in
`docs/ALL_SPRINTS_MASTER_PLAN.md`.

**Why it matters.**
- Testing time is now the largest cost in a sprint. In Sprint 30, the
  approval of D10 was followed by about 87 minutes before `gh pr ready`,
  against the team lead's target of development time plus about 15. A
  local full suite took 48.9 minutes (F177's measurement). F180 finds
  where that time goes and what can be cut without losing a guard; F177
  then makes the cuts. F180 comes first, because its findings choose
  F177's levers.
- The status file can still lose an update when two commands write at
  once (F179). It is the record the commit hook and the task timers read.
- F178's first versions have not been written. Its card puts its update
  step before Manual Validation every sprint, so the step has nothing to
  update until the first versions exist.
- F114 is unblocked. F169 is the first ceiling method to pass F108's
  rule, so the real-data step can run. It is the result the F169, F170
  and F171 work was for.

**Cards.** Minutes are card estimates; 0 metered seconds unless stated.
File counts are estimates.
- F180, deep analysis of all testing: 180m; about 5 files (the analysis
  document, the inventory script, its test, the checklist, this file).
  Prevention.
- F177, the full suite in about 5 minutes: up to 240m; about 10 files.
  Prevention. Its levers are chosen by a decision written from F180's
  findings, mid-sprint; a lever not chosen is not built, so 240m is a
  ceiling.
- F179, the status file's lock and the review-task order: 45m; 3 files.
  Prevention.
- F178, three learning documents, first versions: 180m; about 5 files
  (three documents, a link-and-claim test, the checklist step). A
  deliverable, neither Prevention nor Workaround. The first versions exist
  by Sprint 31 Phase 5, so the per-sprint update step runs from Sprint 32.
- F114, ceiling estimate on real data with F169's method: 90m (the
  real-data step; the validation step is spent); about 4 files.
- F155, the 1,300-variable Dirac-3S ceiling probe: 30m; about 4 metered
  seconds (a floor, not a bound); 3 files. It stops for its own
  per-block approval (Criterion H).

**Kind per option.** Options 1, 2 and 3 carry the same three Preventions
(F180, F177, F179). Options 1 and 3 add F178 (a deliverable) and F114
(research). No option carries a Workaround.

**Cost per option.**
- Option 1: 735 minutes by card estimate; 0 metered seconds; about 27
  files.
- Option 2: 465 minutes; 0 metered seconds; about 18 files.
- Option 3: 765 minutes; about 4 metered seconds behind their own approval
  stop; about 30 files.
- Option 4: whatever set is named.

**Estimate accuracy, measured.** Sprint 30's active-minute ratios (actual
over estimate, `docs/VELOCITY_LOG.md`) run from 0.02 to 0.38 across the
twelve rows that have an estimate. Four rows are flagged "cause
unverified"; two research rows ran their computation in the background,
so their active minutes leave the run time out. Only three tasks were
taken with `--estimate`. These ratios are not converted into a work
forecast here: F180 parts 3 and 4 measure where the time goes, and that is
what settles the cause. The card totals above are the estimates as carded.

**Recommendation: 1.** It gives:
- the testing analysis and its cuts, which is the team lead's stated
  priority after Sprint 30, in the right order (F180, then F177);
- the status-file lock that the timers and the commit hook rely on;
- the first versions of the learning documents, so their per-sprint step
  can start;
- the ceiling result the last two sprints built toward.

All of it at zero metered seconds. F155 is not in it: QCi said the
expansion would come "in the coming weeks" on 2026-10-21, and no newer
word is recorded here, so the probe is better run when QCi says it is
live. F102 is not a card in it: each selected experiment writes its own
entry, and the filing date is the team lead's. F13's content waits for
the finalist notification.

**Options.**

1. As recommended: F180, F177, F179, F178 and F114 (735 minutes, 0
   metered seconds). F177's levers are chosen by a decision written from
   F180's findings.
2. Testing and tooling only: F180, F177 and F179 (465 minutes, 0 metered
   seconds). F178 and F114 stay in the backlog at priorities 12 and 16.
3. Option 1 plus F155, the 1,300-variable probe (765 minutes; about 4
   metered seconds, asked for separately with its call count and seconds
   before it runs).
4. A different set: reply 4 followed by the F numbers to include.

**Answer (team lead, 2026-11-04): a different set (option 4).** Sprint 31
is F180, F177, F178, F179, F114, F155, F157, F150, F95, F121 and F13, with
this instruction for F13: "Last item in sprint after other results are
known. Update plan for Phase 2, then update the backlog based on updated
priorities." F155 and F95 each stop for their own per-block approval
(Criterion H). F150 is carded as blocked and F121 as HOLD; how each runs
is settled at plan verification.

---

## D2. F157: which part runs in Sprint 31?

Asked 2026-11-04 at Phase 3 plan verification.

**What.** F157 was selected without a part named. Parts 1 (ULB) and 2
(IEEE-CIS) shipped as F166 and F174. The card's remaining work is the
other datasets already used and the device and QNN lanes. The datasets on
disk besides ULB and IEEE-CIS are SPECTRA's four: energy_steel,
oilgas_gasturbine, telecom_churn and maintenance_ai4i
(`experiments/data/spectra/`).

**Why it matters.** Each part is about 240 minutes of work plus a long
run (F174's seed 42 took 65.42 minutes). Device lanes spend metered
seconds and need their own approval. Without a named part, the task
cannot be estimated or started.

**Kind.** Scope; no option is Prevention or Workaround.

**Cost per option.**
- Option 1: 240 minutes; runtime set from a timed seed-42 pilot on each
  dataset; 0 metered seconds; about 12 files (four comparison pages and
  their algorithm pages from the tracked generator).
- Option 2: 200 minutes; the same pilot rule; 0 metered seconds; about 10
  files.
- Option 3: 0 minutes.

**Recommendation: 1.** It completes the classical and proxy lanes on
every dataset this project has used, at zero metered seconds, with the
same protocol and generator as F166 and F174. The device and QNN lanes
then have a tuned classical reference on every dataset before any
metered or simulated lane is planned.

**Options.**

1. SPECTRA part: F166's protocol and lanes (HGB, LightGBM, XGBoost,
   CatBoost, logistic regression, SVM, CVQBoost proxy) on all four SPECTRA
   datasets, seeds set from each dataset's timed seed-42 pilot, pages from
   the tracked generator (240 minutes, 0 metered seconds).
2. The same on the three SPECTRA cells with device history only
   (telecom_churn, energy_steel, oilgas_gasturbine), not maintenance_ai4i
   (200 minutes, 0 metered seconds).
3. F157 leaves Sprint 31 and stays in the backlog at priority 30.

**Changed since asked (2026-11-04).** The team lead asked what F157 has
done and not done, and whether the rest is worth doing. Found:

- **Done under F157's protocol**: seven lanes (HGB, LightGBM, XGBoost,
  CatBoost, logistic regression, SVM, CVQBoost proxy) on ULB (F166) and
  IEEE-CIS (F174).
- **Not done under it**: SPECTRA's four datasets (partial earlier work:
  F100's classical bar, F162's three lanes inside the pocket on three
  cells); the CVQBoost device lane (Phase 1 B1-B4 and F142 ran frozen
  configurations, not a tuned lane); QSVM (Phase 1 B5 on ULB: test AUPRC
  mean 0.212, "cheap and weak", `docs/B4_B5_HARDWARE_RESULT.md`); QNN
  (F106's statevector circuit on ULB only, eight seeds, inconclusive,
  because its test fold held 99 positives, `docs/phase2/F106_DEQUANTIZATION.md`).
- The QNN lane is the only one with a different hypothesis class, and
  F106's inconclusive reading also holds F116 on HOLD. A run with more
  test positives is not among options 1-3, so it is added here as
  option 4. Options 1-3 are unchanged.

4. QNN part: F106's circuit and twins under an entry written first, on a
   larger positive count (IEEE-CIS, or ULB with more test positives; the
   entry chooses and says why), seeds set from a timed seed-42 pilot (about
   120 minutes [no-history] plus the run; F106's eight ULB seeds took 8,640
   s; 0 metered seconds, a local statevector).

Options 1 and 4 do not conflict: "1 and 4" runs both (about 360 minutes
plus both runs). Updated recommendation: 4 if one part is taken, because
it is the open quantum question at zero metered cost; 1 and 4 if both
fit.

**Answer (team lead, 2026-11-04): "d2 1 and 4".** F157 runs two parts in
Sprint 31: the SPECTRA part (option 1, 240 minutes) and the QNN part
(option 4, about 120 minutes [no-history]), both 0 metered seconds.

---

## D3. F121: the hold condition is not met. What runs?

Asked 2026-11-04 at Phase 3 plan verification.

**What.** F121 is on HOLD "until a Phase 2 run, proxy or device, shows an
in-segment edge over the matched control with an interval excluding
zero" (team lead, Sprint 26 Decision 2). No Phase 2 result document
records that comparison: F162 compared the proxy with HGB and XGBoost
inside the pocket, not with a matched control. F162 stored every lane's
per-row test scores, for 3 SPECTRA cells over seeds 42-51
(`experiments/phase2/predictions/f162_*.npz`, `y_test` and `p_test`), and
the pocket flag is rebuilt from the same seeded split. So the hold
condition itself can be tested from files on disk, with no new fit.

**Why it matters.** Running Experiment 5 while its hold stands would set
aside a decision of record. Testing the condition settles whether the
hold can lift, with evidence, at low cost. Writing Experiment 5's entry
now means it is ready the day the hold lifts, and fixed before any result
is seen.

**Kind.** Option 1 is Prevention: the hold is decided by a recorded test,
and the entry exists before any Experiment 5 run. Option 2 is a
Workaround: it runs the experiment past its hold. Option 3 is Prevention
for the entry only.

**Cost per option.**
- Option 1: 60 minutes; a few minutes of computation on stored scores; 0
  metered seconds; about 4 files (an entry, a module, its test, a result
  document).
- Option 2: about 180 minutes plus a run sized by a pilot; 0 metered
  seconds; about 6 files.
- Option 3: 30 minutes; 0 metered seconds; 1 file.
- Option 4: 0 minutes.

**Recommendation: 1.** It answers the hold question with a measurement,
under an entry written before the run, using the downsized matched
control that F102's draft specifies. If the condition is met, the hold
lifts on evidence and Experiment 5's run is a later card; if not, the
hold stands with a reason that is no longer only a decision.

**Options.**

1. Test the hold condition: an entry first (the in-segment edge against
   F102's downsized matched control, repeated draws, interval rule), then
   the test on F162's stored proxy scores over 3 cells and 10 seeds; and
   Experiment 5's entry written as a draft. The hold lifts only if the
   condition is met (60 minutes, 0 metered seconds).
2. Lift the hold: write Experiment 5's entry and run its transfer half on
   the proxy, pilot first (about 180 minutes plus the run, 0 metered
   seconds).
3. Keep the hold and write Experiment 5's entry as a draft only, with no
   measurement (30 minutes, 0 metered seconds).
4. F121 leaves Sprint 31 and stays on HOLD.

**Answer (team lead, 2026-11-04): 2.** Verbatim: "D3 2 - run the whole
d5 experiment so we can learn what is new or is verified". Recorded as:
the hold of record (Sprint 26 Decision 2) is set aside by this answer.
Experiment 5 (F121) runs in full on the proxy: its entry written first,
then the transfer half judged by the router criterion (at least one point
of recall at the 0.5% budget above the classical champion, out of time,
on prespecified segments, against a matched random-segment control),
pilot first. "d5" is read as Experiment 5, F121's experiment; the reading
is stated in the plan so it can be corrected.

---

## D4. F150: was the construction request to the SPECTRA authors sent?

Asked 2026-11-04 at Phase 3 plan verification.

**What.** Sprint 28 drafted the request,
`docs/spectra_package/F150_CONSTRUCTION_REQUEST_DRAFT.md` (gitignored),
and handed it to the team lead to check the paper's title and then send,
change or discard. This repository records no send and no reply. F150's
rebuild is blocked until the authors reply.

**Why it matters.** If it was sent, the task waits for a reply. If not,
the request can go now. The paper's title is now recorded in
`docs/references.md` (Mancilla and Tagliani, "The Fourier Wall",
arXiv:2607.15815), so the check Sprint 28 left open can be done here.

**Kind.** A fact, then scope; no option is Prevention or Workaround.

**Cost per option.**
- Option 1: 0 minutes now; the rebuild, about 120 minutes, only if the
  reply arrives before Phase 5.
- Option 2: 15 minutes now; the same contingent rebuild.
- Option 3: 0 minutes.

**Recommendation.** None on the fact, which only the team lead knows. If
it was not sent, 2: the draft is ready, the title can be checked here,
and nothing else unblocks F150.

**Options.**

1. It was sent: reply 1 followed by the date sent. The task waits for
   the reply and rebuilds only if it arrives before Phase 5.
2. It was not sent: I check the draft against the paper's title and
   against F109's later findings, and hand it to you to send. The rebuild
   runs only if the reply arrives before Phase 5 (15 minutes now).
3. It was not sent and is not to be sent: F150 leaves Sprint 31 and stays
   blocked.

**Answer (team lead, 2026-11-04): "D4 delay to next sprint".** None of
the listed options. F150 leaves Sprint 31 and is carried to Sprint 32's
refinement at priority 41; whether the request was sent is asked again
then.

---

## D5. F95: on which device does schedule 4 run?

Asked 2026-11-04 at Phase 3 plan verification.

**What.** F95 is the check promised in the QCi memo sent 2026-09-25:
"Would relaxation schedule 4 close the residual?" The residual was
measured on Dirac-3 (0.413% on the G0b fit). Since Sprint 26 Decision 11
the default device is Dirac-3S, and F142's Dirac-3S fits of the same B1
configuration at schedule 2 already reached the reference optimum
(relative gaps 4.5e-9 and -6.7e-8,
`experiments/phase2/results/f142_dirac3s_verify.json`). So on Dirac-3S
there may be no residual for schedule 4 to close (inferred).

**Why it matters.** A Dirac-3S run may measure nothing. A Dirac-3 run
answers the question as the memo asked it. Each costs metered seconds and
stops for its own approval.

**Kind.** Scope; no option is Prevention or Workaround.

**Cost per option.**
- Option 1: 30 minutes; 0 metered seconds; 1 file.
- Option 2: 60 minutes to build; about 60 metered seconds, range 40-110,
  cap 120 (the card's Dirac-3 figures: schedule-2 cost of 4-5 s per fit
  times QCi's 3.4x schedule-4 ratio, low confidence); 4 fits, stopping
  after fit 1 to re-quote if it exceeds 27 s; about 4 files.
- Option 3: 60 minutes to build; cost unknown,
  `qpu_cost_model.quote(91, 1, relaxation_schedule=4)` returns unknown
  for Dirac-3S, so the block is bounded by its 4 calls and stops after
  fit 1 to re-quote; about 4 files.

**Recommendation: 2.** It answers the promised question on the device it
was asked about. Dirac-3 is still available to this account (QCi,
2026-10-20, A5). The entry names Dirac-3 on a `# device named:` line with
this reason. Option 1 answers a different question; option 3 may measure
nothing.

**Options.**

1. Report F142's Dirac-3S rows as the Dirac-3S answer and close F95,
   with no metered seconds (30 minutes).
2. Run the four promised fits on Dirac-3 at schedule 4, through the
   proven runner path, stopping after fit 1 to re-quote; about 60 metered
   seconds (range 40-110, cap 120), asked for separately with its call
   count and seconds before it runs (60 minutes to build).
3. Run the four fits on Dirac-3S at schedule 4, bounded by 4 calls and
   stopping after fit 1 to re-quote; cost unknown, asked for separately
   before it runs (60 minutes to build).

**Answer (team lead, 2026-11-04): "1 and 3".** Verbatim: "d5 this and
all future runs will be on the Dirace-3S 1 and 3". F95 reports F142's
Dirac-3S rows as the schedule-2 answer (option 1) and runs the four fits
on Dirac-3S at schedule 4, bounded by 4 calls, stopping after fit 1 to
re-quote, behind its own approval (option 3). 90 minutes. **Standing
rule from this answer: this run and every future device run go to
Dirac-3S.** Recorded in `SPRINT_EXECUTION_WORKFLOW.md`'s standing
hardware rule.

---

## D6. pypdf 6.21.2 has 7 known vulnerabilities. Is the bump in Sprint 31?

Asked 2026-11-04 at Phase 2 pre-kickoff (dependency scan).

**What.** `pip-audit` on `experiments/requirements-lock.txt`
(2026-11-04) reports 7 advisories against pypdf 6.21.2: four fixed in
6.21.3 and three in 6.21.4. pypdf is a declared dependency, read by the
submission-artifact tests. It is not in the selected scope.

**Why it matters.** The repository reads PDFs with a library that has
known advisories. Sprints 28 and 29 each took a pypdf bump as a task
(Sprint 29's measured 17 minutes active against 45 estimated). The
defined-scope rule means a bump is added only by the team lead's answer.

**Kind.** Option 1 is a Workaround: it closes these advisories, not the
next ones. The Prevention, a dependency audit in CI, is not proposed
here: it would add a network call to every CI run, and F180's inventory
is where CI's checks are decided.

**Cost per option.**
- Option 1: 45 minutes (card estimate as before); 0 metered seconds; 2
  files (the lock and its header line).
- Option 2: 0 minutes now.

**Recommendation: 1.** Seven advisories, a bump within the same minor
line, and a task this project has done twice before at low cost.

**Options.**

1. Add the bump to Sprint 31: pypdf 6.21.2 to 6.21.4 in the lock, with
   a dated header line, and the submission-artifact tests run without
   re-rendering any submitted PDF (45 minutes, 0 metered seconds).
2. Leave it out: a backlog card at priority 20.

**Answer (team lead, 2026-11-04): 1.** The bump is Task D of Sprint 31.

---

## D7. Is the Sprint 31 plan approved?

Asked 2026-11-04 at Phase 3.7.

**What.** Approval of `docs/sprints/SPRINT_31_PLAN.md` as written after
D2-D6: Tasks A-L, 1,569 minutes by card estimate, and two Dirac-3S
blocks (F155 about 4 s, a floor; F95 bounded by 4 calls, fit 1 approved
alone), each stopping for its own approval. The plan reads D3's "the
whole d5 experiment" as Experiment 5 (F121) run in full on the proxy,
with its hold set aside.

**Why it matters.** Execution, the task issues and the first task file
all wait on approval. One gap is open: D5's new rule, "this and all
future runs will be on the Dirace-3S", is written in
`SPRINT_EXECUTION_WORKFLOW.md`, but `test_phase2_device_default.py`
still accepts a Phase 2 module that names Dirac-3 with a reason. A rule
kept only in a document is the kind this repository has had to replace
with a check.

**Kind per option.** Option 1: none. Option 2: Prevention (the rule is
checked, not remembered). Option 3: as named.

**Cost per option.**
- Option 1: 1,569 minutes; the two blocks above; about 60 files (task estimates: A 3, B 5, C 10, D 2, E 4, F 12, G 4, H 5, I 3, J 4, K 5, L 3).
- Option 2: 1,584 minutes (plus 15 for the guard, as Task M); the same
  blocks; 1 more file.
- Option 3: whatever the changes cost.

**Recommendation: 2.** It turns D5's standing rule into a test in the
sprint that made it, at 15 minutes, before the two device builds are
written.

**Options.**

1. Approved as written: Tasks A-L, 1,569 minutes; D3 read as Experiment
   5 in full on the proxy.
2. Approved, with Task M added: `test_phase2_device_default.py` refuses
   any Phase 2 module that names Dirac-3, its red proof in the same commit
   (15 minutes; 1,584 in total).
3. Approved with changes: reply 3 followed by the changes.

**Answer (team lead, 2026-11-04).** Verbatim: "Sprint plan approved as
amended (with any comments I provided), proceed with execution. All
Sprint tasks and sub-tasks are approved. Do not stop between tasks as
they are all approved, please continue to complete all tasks and without
addition approvals until Manual Validation, providing your
recommendation for Manual Validation steps. Do not stop to ask questions
unless meeting the criteria in \docs\SPRINT_STOPPING_CRITERIA.md. If
questions must be asked, ask as late as possible - do everything that
can be done (all tasks and parts of tasks, without the answer to the
question(s), then ask the question(s)". Recorded as option 1: no option
digit names Task M, and the defined-scope rule keeps an unselected item
out, so the guard tightening is carded as F181 for refinement. The two
Dirac-3S blocks still stop for their own approval (Criterion H, which no
general approval replaces); both are built and dry-run first, and asked
for as late as possible.

---

## D8. F180: which testing changes does F177 (Task C) build?

Asked 2026-11-05 at Phase 4, Task B done. The analysis is
`docs/testing/F180_TESTING_ANALYSIS.md`; the inventory is
`docs/testing/F180_TEST_INVENTORY.md`.

**What.** F180 measured the suite. CI's full job ran every test, the red
proofs included, in 12:06 (run 41982345324). Locally the same tests take
17.7 times longer, because this workstation is slow to start a Python
process (`import numpy, pandas, sklearn` took 18-22 s with the machine
idle). A local run with every proof is projected at about 8 hours today.
37 untested refusals, terms and states reached review in Sprints 28-30.
F177 builds only the changes chosen here. The changes, prevention first:
- **a. CI's full job replaces the local Phase 5 full run.** Phase 5
  starts it by hand (`gh workflow run ci.yml --ref <branch>`) and reads
  it with `scripts/check_ci_status.py --require-job full`. Gives up: a
  Windows-only defect is found only by a local run of the changed files.
- **b. A red proof runs locally only when its files changed**: its test
  file, a file its mutations name, `injection.py` or `conftest.py`,
  against `origin/develop`. Every proof still runs on CI's full job.
  Gives up: a guard weakened by a file its proof does not name is found
  at CI, not at once.
- **c. Diff coverage**: coverage.py plus diff-cover in CI's push job,
  failing when a changed line in `scripts/`, `experiments/src/`,
  `experiments/phase2/src/` or `.claude/hooks/` is not executed. This is
  the check that the per-term rule was applied. Two new declared
  dependencies. Gives up: lines run only inside a subprocess may read as
  not covered unless coverage's subprocess support is set up
  (**unverified** for this suite; the build measures it first).
- **d. The local non-proof tests run in parallel** with pytest-xdist
  (`--dist loadfile`). Proofs stay serial and alone. One new declared
  dependency. Gives up: each test that writes the tree or uses git must
  be checked first and grouped or kept serial.
- **e. The short review and CI's full job start at push, in parallel**,
  the review with its time cap (process documents only).
- **f. `scripts/env_check.py`**: times a Python start, the scientific
  imports and a file stat, and prints them beside the 2026-11-05 values,
  so a slow machine is seen before a run, not during it.

Not in the options, because they are not changes F177 builds: the team
lead may exempt the repository and the venv from Norton and Defender
real-time scanning, which would test the inferred cause. F177's lever 3
(skip the nested evidence hash) is not recommended: it saves under a
second per start against 8-35 s.

**Why it matters.** Sprint 30 took about 86 minutes from an approved
change to `gh pr ready`, against the target of its development time
plus about 15. The local full run is the step the team lead waits on
before Manual Validation, and today it cannot finish in a working day.
Untested branches keep reaching review because the rule against them is
applied by hand.

**Kind per option.** Option 1: Prevention (a, b, c and f stop the slow
run and the untested branch recurring; d and e shorten what remains).
Option 2: Prevention for the time, Workaround for effectiveness
(untested branches are still found only by review). Option 3:
Workaround (process only; nothing checks the rule). Option 4: none.

**Cost per option** (F177's estimate is up to 240 minutes; 0 metered
seconds in every option):
- Option 1, a-f: about 240 minutes (a 30, b 60, c 60, d 45, e 15,
  f 30); about 12 files; 3 new dependencies in the lock.
- Option 2, a, b, d, e, f: about 180 minutes; about 9 files; 1 new
  dependency.
- Option 3, a, b, e: about 105 minutes; about 6 files; no new
  dependency.
- Option 4: 0 minutes now; F177 returns to the backlog.

**Recommendation: 1.** a and b remove the hours-long local run, which
is the largest measured cost. c is the only change that checks the
per-term rule instead of trusting it, and the 37 untested branches are
the largest class a test can catch. If c's subprocess measurement shows
it cannot see the hook and script tests, the build stops c and reports
it, rather than ship a check that reads green on untested lines.

**Options.**

1. Build a, b, c, d, e and f in Task C (about 240 minutes, 3 new
   dependencies: coverage, diff-cover, pytest-xdist).
2. Build a, b, d, e and f in Task C, without diff coverage (about 180
   minutes, 1 new dependency: pytest-xdist).
3. Build a, b and e in Task C, process and selection only (about 105
   minutes, no new dependency).
4. Build none in Sprint 31; F177 returns to the backlog with this
   analysis attached.

---

## D9. F155: send the 1,350-variable probe to Dirac-3S? (Criterion H)

Asked 2026-11-05 at Phase 4, Task I built and dry-run. Entry: "F155" in
`experiments/phase2/PREREGISTRATION_DRAFT.md` section 6. Dry run:
`experiments/phase2/results/f155_dry_run_stop1.json`.

**What.** One Dirac-3S job tests whether the cloud queue accepts a
continuous job above 954 and 987 variables. The team lead set the size
at 1,300 (Sprint 28 DV1). A CVQBoost pool cannot have 1,300 variables:
order 3 gives 1,159 at 19 features and 1,350 at 20. The built unit is
the 1,350-variable pool (ULB, seed 42, 20 features, order 3, `dct`,
seeded), one sample, schedule 2, sent through F142's proven path with
`device_store`. Accepted means the returned solution has 1,350 entries.

**Why it matters.** F143 (987 variables) stays on HOLD until a job above
949 is shown to be accepted. 1,350 answers the same question as 1,300:
it is above both 954 and 987. An exact 1,300 needs a bare Hamiltonian,
a send path no Phase 2 runner has used.

**Kind per option.** Option 1: none (a measurement). Option 2: none (a
different measurement path). Option 3: none.

**Cost per option.**
- Option 1: 1 call. `qpu_cost_model.quote(1350, 1)` gives 4 s from one
  Dirac-3S anchor (833 variables); 1,350 is above it, so 4 s is a floor,
  not a bound. Whether a rejected job is billed is unverified. One
  attempt, never retried. The dry run built the pool (1,350 variables, as
  the entry states) in about 2.5 minutes under WSL; a metered run builds
  it twice (screen, then send), so about 5 minutes pass before the call.
  The pool fails A31's resolution screen; the entry reports it and does
  not read accuracy, so it does not block the probe.
- Option 2: about 45 minutes to build and test a bare-Hamiltonian unit
  and its dry run, then this approval asked again; the same 1 call.
- Option 3: 0.

**Recommendation: 1.** It answers the question the size was chosen for,
on the send path already proven on Dirac-3S, at one call.

**Options.**

1. Approve F155 stop 1: one Dirac-3S call, the 1,350-variable pool, one
   sample, schedule 2; quote 4 s (a floor); one attempt.
2. Build an exact 1,300-variable bare Hamiltonian unit first (about 45
   minutes), then ask again with its dry run.
3. Do not run F155 in Sprint 31.

---

## D10. F95 stop 1: send fit 1 at relaxation schedule 4 to Dirac-3S? (Criterion H)

Asked 2026-11-05 at Phase 4, Task J built and dry-run. Entry: "F95" in
`experiments/phase2/PREREGISTRATION_DRAFT.md` section 6. Dry run:
`experiments/phase2/results/f95_dry_run_stop1.json`.

**What.** Fit 1 of the four D5 option 3 named: `b1_dct_42` (B1's
configuration, 91 variables, ULB seed 42, `dct`, alpha 2, seeded), 8
samples, relaxation schedule 4, on Dirac-3S. Its schedule-2 twin is
F142's `b1_42`. Rebuilt offline on 2026-11-05, the twin's pool matches
F142's recorded hash, and its 8 stored samples lie within about 6e-08
(relative) of the reference optimum: no schedule-2 residual. "No change"
at schedule 4 is the expected result. Stop 2 (the other three fits) is
asked after this fit's cost is known.

**Why it matters.** It answers the question promised in the QCi memo of
2026-09-25 on the device now in use, and it measures schedule 4's cost
on Dirac-3S, which no call has measured.

**Kind.** None (a measurement).

**Cost per option.**
- Option 1: 1 call. `qpu_cost_model.quote(91, 8,
  relaxation_schedule=4)` returns unknown: no Dirac-3S call has run at
  schedule 4. F95's card estimate, derived on Dirac-3: 4-5 s per fit at
  schedule 2 times 3.4 (range 2.3-5.3) for schedule 4, about 15 s per
  fit, low confidence. The card's re-quote line is 27 s per fit; the
  card's cap is 120 s over all four fits. One attempt, never retried.
- Option 2: 0.

**Recommendation: 1.** One fit establishes the rate at a bounded cost
before the other three are asked.

**Options.**

1. Approve F95 stop 1: one Dirac-3S call, `b1_dct_42` at schedule 4, 8
   samples; cost unknown, about 15 s by the card's Dirac-3 estimate.
2. Do not run F95 in Sprint 31.

---

## D11. F114: the preregistered estimator does not train on ULB. What next?

Asked 2026-11-05 at Phase 4, Task E run stopped after nine ULB seeds.

**What.** F114 runs F169's `lgbm_bins` plug-in (LightGBM, 100 trees,
learning rate 0.1, 4,095 bins), fixed by the 2026-11-05 F108 amendment.
On ULB:
- The shuffled-label check **failed**: estimate 0.0011 against a test
  fraud rate of 0.0017, margin 0.0005
  (`experiments/phase2/results/f114_real_ceiling.json`, `check`). By the
  entry, no F114 figure is reported as a ceiling.
- On real labels the fit **collapsed** on every recorded seed: seeds 42
  to 50 give test AUPRC from 0.002 to 0.327, and every error (0.0032 to
  0.0109) is worse than flagging nothing (the same file, `rows`). The run
  was stopped before seed 51; IEEE-CIS has not run.
- A scratch diagnosis on seed 42 (not a tracked result; reproduced by
  fitting `LGBMClassifier` on `f114_real_ceiling.ulb(42)`): at learning
  rate 0.1 the model does not fit even its training rows (training AUPRC
  0.067 at 4,095 bins, 0.317 at 255). At 0.05 it trains (test AUPRC 0.742
  at 4,095 bins, 0.723 at 255). Boosting at a high rate on 0.17% positives
  diverges; F169 validated the estimator on a simulator, where it did not.

**Why it matters.** The failed check may be the collapse, not the
method: an estimator that cannot fit cannot be judged by the check. A
changed learning rate is a new estimator, so F169's simulator validation
does not cover it, and the entry would need a dated amendment before any
new figure.

**Kind per option.** Option 1: Prevention (the estimator is re-validated
where it was validated, then used; the amendment is written first).
Option 2: Workaround (the result is recorded as it stands). Option 3:
Workaround.

**Cost per option.**
- Option 1: about 60 minutes: F169's simulator check re-run at learning
  rate 0.05 (`f169_plugin_bins.py`; its recorded fits total about 1
  minute, plus its data build), a dated amendment to the F108 entry, then
  F114 re-run from the check (ULB seed 42's fit took 1.1 s and the check's
  20.8 s; IEEE-CIS not yet timed). 0 metered seconds.
- Option 2: about 20 minutes: the F114 result document says the check
  failed and the estimator collapsed on ULB; F114 returns to the backlog
  with this finding. 0 metered seconds.
- Option 3: about 40 minutes plus IEEE-CIS's run time: IEEE-CIS run as
  the entry stands (descriptive only, since the check failed), then the
  document of option 2.

**Recommendation: 1.** The check cannot answer its question while the
estimator does not fit, and re-validating on the simulator keeps F108's
rule: no real-data figure from an estimator the simulator has not passed.

**Options.**

1. Re-validate `lgbm_bins` at learning rate 0.05 on F169's simulator; if
   it passes F108's rule, write a dated F108 amendment and re-run F114
   from the shuffled-label check (about 60 minutes, 0 metered seconds).
2. Record F114 as run (check failed, estimator collapsed on ULB) in a
   result document and return the card to the backlog (about 20
   minutes).
3. Run IEEE-CIS as the entry stands, descriptive only, then record as in
   option 2 (about 40 minutes plus IEEE-CIS's run time).
