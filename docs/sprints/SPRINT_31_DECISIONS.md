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

**Answer (team lead, 2026-11-05): not yet chosen.** "Can you explain
what the 'proofs' are and why they are important to run so often as it
would appear to me they only need to run once or if something about
them changed. Can you also research 'risk based testing' with regard to
development testing, software engineering and agile development best
practices as it appears that we are testing without regard to the
risk-related need of each test for each change or each sprint. Then
update the options after I have time to review what you found regarding
the proofs and risk based testing." The options above stay as asked;
revised options follow as a dated "Changed since asked" note after the
team lead's review.

**Changed since asked (2026-11-05, 18:40).** Two facts changed.

- **The local full run is shorter than projected.** D8 said a local
  run with every proof was projected at about 8 hours (from a run
  stopped at 8% after 40 minutes). Today's full local run, every proof
  included, finished in 4,774 s, 79.6 minutes (3,181 passed, 7 failed;
  scratchpad junit report used for the inventory). Inferred, not
  tested: the workstation was less loaded. The cost is still real: an
  hour and twenty minutes, against CI's 12.
- **The research** (`docs/testing/F180_PROOFS_AND_RISK_BASED_TESTING.md`,
  which the team lead asked for): a proof's answer changes only when its
  test, the file it mutates or the shared machinery changes, so
  re-running an unchanged proof shows nothing new. ISTQB, Microsoft and
  Google select tests by change and risk and keep a scheduled full run
  as the safety net. Today's two proof failures fit that: the f169 proof
  failed because a file it mutates changed (b would run it); the f159
  proof failed because of start-up time, with no file of its own changed
  (b would skip it, and nothing would be lost).

**Revised options**, built on that: change selection (b) plus the full
run moved to CI (a) is the risk-based core; c is the only check that
the per-term rule was applied; d and e only shorten what remains.

**Kind.** Revised option 1: Prevention. Revised option 2: Prevention for
the run time, Workaround for the untested branches. Revised option 3:
Prevention (the original option 1). Revised option 4: none.

**Cost** (0 metered seconds in each; per-item minutes as asked):
- Revised 1, a, b, c and f: about 180 minutes, about 9 files, 2 new
  dependencies (coverage, diff-cover).
- Revised 2, a, b and f: about 120 minutes, about 6 files, no new
  dependency.
- Revised 3, all six: about 240 minutes, about 12 files, 3 new
  dependencies (the original option 1).
- Revised 4: 0 minutes now; F177 returns to the backlog.

**Recommendation: revised 1.** b is the risk-based selection the
research supports, a keeps every proof running once per sprint on CI,
and c checks the untested-branch rule instead of trusting it. d is
left out: once b takes the unchanged proofs out of the local run, the
remainder is the non-proof tests (39:34 measured), and each test that
writes the tree or uses git would have to be checked before it could
run in parallel. If c's subprocess measurement shows it cannot see the
hook and script tests, the build stops c and reports it.

**Revised options.**

1. Build a, b, c and f in Task C: CI's full job replaces the local
   Phase 5 full run, a proof runs locally only when its own files
   changed, diff coverage in CI's push job, and the start-up timing
   script (about 180 minutes, 2 new dependencies: coverage,
   diff-cover).
2. Build a, b and f in Task C, without diff coverage (about 120
   minutes, no new dependency).
3. Build a, b, c, d, e and f in Task C, as first asked (about 240
   minutes, 3 new dependencies: coverage, diff-cover, pytest-xdist).
4. Build none in Sprint 31; F177 returns to the backlog with this
   analysis attached.

**Team lead, 2026-11-05 19:00, verbatim:** "d8. no change due to the
test run today. continue as previously instructed". No option chosen
yet; D8 stays open and is asked again with the revised options.

**Answer (team lead, 2026-11-05 19:10), verbatim:** "I answered the
question as no changes. continue as if you would before the question
was asked." Not read as an option choice. A first reading as revised
option 4 was shown and the team lead said it is incorrect: "I
previously answerd a d8 questions with what should be done this
sprint." The session record and this file hold no earlier Sprint 31 D8
option answer (the two earlier "D8 1" answers are Sprint 26's and
Sprint 30's D8s, on other questions). D8 is asked again, unchanged
since its 18:40 note.

**Answer (team lead, 2026-11-05 19:15): build all six, a-f.** The team
lead pasted the six changes a-f with "I believe these are the 6
changes I asked for prior to this sprint", so "no changes" means the
plan is unchanged: the original option 1, which is revised option 3
(about 240 minutes; coverage, diff-cover and pytest-xdist added to the
lock). The team lead also noted the D8 shown at 17:58 had no question
in it: its numbered options did not reach the screen. Task C builds
a-f.

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

**Answer (team lead, 2026-11-05): 1.** F155 stop 1 approved: one
Dirac-3S call, one attempt.

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

**Answer (team lead, 2026-11-05): 1.** F95 stop 1 approved: one
Dirac-3S call, `b1_dct_42` at schedule 4, one attempt. Stop 2 is asked
after this fit's cost is known.

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

**Answer (team lead, 2026-11-05): 1.**

---

## D12. F95 stop 2: send the other three schedule-4 fits to Dirac-3S? (Criterion H)

Asked 2026-11-05 at Phase 4, after F95 stop 1 (D10 option 1). Entry:
"F95" in `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6. Stop 1:
`experiments/phase2/results/f95_schedule4.json`. Dry run:
`experiments/phase2/results/f95_dry_run_stop2.json`.

**What.** Stop 1 ran `b1_dct_42` at relaxation schedule 4 on Dirac-3S:
18.0 metered seconds, three times its schedule-2 twin's 6.0 s (F142
`b1_42`), and every one of the 8 samples within about 5e-08 of the
reference optimum, so no change from schedule 2. Stop 2 is the other
three fits D5 option 3 named, 8 samples each, schedule 4, one attempt
each, in this order:
- `b1_dct_43`: B1's configuration, 91 variables, ULB seed 43, `dct`,
  alpha 2. Its schedule-2 twin is F142's `b1_43` (hash matched in the
  dry run).
- `g0b_3_42`: 45 variables, `lg`, alpha 4, seed 42. No Dirac-3S twin;
  Dirac-3 history only.
- `b1_lg_42`: 45 variables, `lg`, alpha 0.5, seed 42. No Dirac-3S twin;
  Dirac-3 history only.

**Why it matters.** Stop 1 gives one 91-variable point. The second B1
fit tests whether "no change" repeats on another seed with a Dirac-3S
twin; the two 45-variable fits are the card's `lg` fits, with Dirac-3
history only, so they test schedule 4 at a second size and a second
weak-classifier type.

**Kind per option.** None (a measurement).

**Cost per option.**
- Option 1: 3 calls. `b1_dct_43`: 18 s, **measured** at this
  configuration (stop 1's call: same size, samples and schedule;
  `qpu_cost_model.quote(91, 8, relaxation_schedule=4)` over
  `f95_schedule4.json`). The two 45-variable fits: **unknown** (no
  Dirac-3S call within 2x of 45 variables); bounded by call count, 2
  calls. Inferred, not measured: at about 2.24 s per sample for 91
  variables, a 45-variable fit is likely at or under 18 s. Card cap 120 s,
  18 s spent, so 102 s remain; the runner stops between units once the
  cap is reached. One attempt each, never retried.
- Option 2: 1 call, `b1_dct_43` only, 18 s measured.
- Option 3: 0.

**Recommendation: 1.** It completes the four fits the team lead chose
in D5, and the card's cap bounds the unknown cost.

**Options.**

1. Approve F95 stop 2: three Dirac-3S calls, `b1_dct_43` (18 s
   measured), `g0b_3_42` and `b1_lg_42` (unknown, bounded by 2 calls and
   the card's 102 s remaining cap); one attempt each.
2. Approve `b1_dct_43` only: one Dirac-3S call, 18 s measured.
3. Do not run F95 stop 2; F95 is reported on stop 1.

**Answer (team lead, 2026-11-05): 1.** F95 stop 2 approved: three
Dirac-3S calls, `b1_dct_43`, `g0b_3_42` and `b1_lg_42`, one attempt
each, within the card's 102 s remaining cap.

---

## D13. F114: the re-run overwrote the first run's score files. How is it repaired? (Criterion 7)

Asked 2026-11-05 at Phase 4, after the F114 re-run (D11 option 1).

**What.** `outcome_record.record` saves each row's test scores to
`experiments/phase2/predictions/<name>_<seed>.npz` (gitignored) and the
result records the file's SHA-256. The re-run (`f114_real_ceiling.py
--lr05`, 7850a60) kept the first run's record name, `f114_<dataset>`,
so at 10:05 it replaced the first run's ULB score files for seeds
42-50. The first result (`f114_real_ceiling.json`) is unchanged, but
its nine recorded hashes no longer match the files on disk; the
re-run's result (`f114_real_ceiling_lr05.json`) matches the files now
there. My code defect: the new mode needed its own record name, and no
test checked it. `save_test_scores` replaces a file without checking
what it held, so no guard stopped it. `test_outcome_record_required.py`
reports it after the fact: its stale-hash test names the nine files and
stays red on this workstation until they are restored (the files are
gitignored, so CI does not see them).

**Recoverable, checked.** The files are byte-reproducible (numpy writes
a fixed zip date). A scratch rebuild of the first run's nine ULB fits
(`f169_plugin_bins.make('lgbm_bins', seed)` on `f114_real_ceiling.ulb`)
matched all nine recorded SHA-256 values exactly. Nothing in the
repository was written by the check.

**Why it matters.** A recorded result whose evidence file has been
replaced cannot be re-checked by anyone, and the next module that
reuses a record name will do the same, silently. Under Criterion 4's
precedence rule this is not fixed and re-run without a decision.

**Kind per option.** Option 1: Prevention (the writer refuses the
replacement for every module) plus repair. Option 2: Workaround
(repair only). Option 3: Workaround (records the break, fixes nothing).

**Cost per option** (0 metered seconds in each):
- Option 1: about 45 minutes. (a) `save_test_scores` refuses to replace
  an existing file whose bytes differ, naming the file, with a test and
  a red proof; (b) the `--lr05` mode records as `f114lr05_<dataset>`;
  (c) the re-run's result is re-run with `replace=` stating why (about
  2 minutes of fits; deterministic), and every figure and hash compared
  with the current file before it is accepted; (d) the first run's nine
  files restored at their original paths from the verified rebuild. About
  5 files.
- Option 2: about 30 minutes: (b), (c) and (d) only. About 3 files.
- Option 3: about 10 minutes: a dated note in `docs/phase2/F114_REAL_CEILING.md`
  and the first result's document that the nine files were replaced and
  how to rebuild them; no file changes.

**Recommendation: 1.** The repair restores both runs' evidence exactly,
and the writer change stops the same overwrite in any module.

**Options.**

1. Make `save_test_scores` refuse to replace a different file (with a
   red proof), give the re-run the record name `f114lr05_<dataset>`,
   re-run it with `replace=` and check every figure and hash against the
   current result, and restore the first run's nine files from the
   verified rebuild (about 45 minutes).
2. The same without the `save_test_scores` change (about 30 minutes).
3. Record the break and the rebuild method only; change no file (about
   10 minutes).

**Answer (team lead, 2026-11-05).** Verbatim: "change the name of the
new (at rate .05) to something differnt. Ensure that in the future when
picking file names, ensure the filename does not exist first, altering
the filename as needed (preventetive). Can the overwritten file be
retrieved from a prior github commit and if so, do that."
Carried out as: (a) the `--lr05` mode records as `f114lr05_<dataset>`;
(b) `save_test_scores` never replaces a file: when the name is taken by
different bytes it writes the next free name (`<name>_<seed>_v2.npz`,
`_v3`, ...) and records that path; identical bytes reuse the file;
(c) git cannot retrieve the files: `experiments/phase2/predictions/` is
gitignored (`.gitignore` line 91) and no commit on any branch touches
it. The nine files are restored from the scratch rebuild, whose SHA-256
values match all nine recorded ones byte for byte.

**Follow-up (team lead, 2026-11-06, Manual Validation),** after a fuller
explanation of D13 was given on screen. Verbatim: "D13. OK"

---

## D14. F157 SPECTRA: the entry's rule keeps the RBF SVM, and the SVM lane scored only the linear form. What is reported? (Criterion 7)

Asked 2026-11-05 at Phase 4, after the F157 SPECTRA run completed.

**What.** The entry ("F157 SPECTRA part", which takes F166's rule
unchanged) keeps the RBF SVM as the SVM lane's form if its best
validation AUPRC beats the linear form's on a majority of seeds. It did
so on every dataset: 6 of 10 seeds on energy_steel, 10 of 10 on
oilgas_gasturbine, 10 of 10 on telecom_churn and 7 of 10 on
maintenance_ai4i. The RBF form was fitted on validation only, so it has
no test score; every SVM figure, the SVM's rank and the two pairs
touching it are the linear form's. F166's module stops before marking a
run complete when this happens (`f166_ulb_algorithms.rbf_kept`, added
after the PR 63 review). The SPECTRA module I wrote records it
(`svm_lane_is_kept_form` false) and marks the run complete. That is my
departure from F166's protocol, and the entry does not permit it.

**Size of the gap.** Where the RBF fit worked, it led by a wide margin
on validation: for example oilgas_gasturbine about 0.85 against 0.78,
telecom_churn about 0.84 against 0.66, energy_steel about 0.87 against
0.69. On energy_steel seeds 42, 44, 45 and 46 the RBF validation AUPRC
equals the positive rate (no ranking); those count as linear wins, so
they do not add to the RBF majority. The other six lanes are unaffected.

**What is done, not waiting on this.** The 32 pages are generated
(`scripts/f157_spectra_docs.py`, with tests). Every SVM page and every
comparison page states that the SVM figures are the linear form, not the
form the rule keeps. They are not committed until this is answered.

**Why it matters.** As recorded, the comparison pages rank an SVM that
the entry's own rule set aside, and on three datasets the SVM's place
in the order could change. Publishing it as complete repeats the defect
F166's guard was added to stop.

**Kind per option.** Option 1: Prevention (the module gets F166's guard
and the kept form is scored). Option 2: Workaround (reports the gap
openly; scores nothing new). Option 3: Workaround (withholds the SVM
lane only).

**Cost per option** (0 metered seconds in each):
- Option 1: about 60 minutes. A dated amendment to the F157 SPECTRA
  entry, committed before any RBF test score: per seed, the RBF form at
  its validation-chosen `C`, fitted on the same subsample, scored on the
  test fold with an outcome block, becomes the SVM lane where the rule
  keeps RBF. The module calls a guard like `rbf_kept` for any lane it
  cannot score. Fits: 40 at about 0.05 to 9 s each, under 5 minutes in
  all. The analysis is recomputed, the result replaced with `replace=`
  stating why, and the pages regenerated. About 5 files.
- Option 2: about 15 minutes. Commit the pages as generated, plus a
  dated note in the entry that this part departed from F166's stop rule
  and why; the result keeps `complete` true. About 3 files.
- Option 3: about 30 minutes. Re-render with the SVM lane removed from
  the order, the pairs and the pages (six algorithms, five pairs per
  dataset), with a dated note in the entry. About 4 files.

**Recommendation: 1.** It scores the form the rule keeps, at under five
minutes of local fits, and adds the guard so the next module cannot do
the same. Options 2 and 3 leave the comparison without the SVM the
entry asked for.

**Options.**

1. Write a dated amendment, score the kept RBF form on the test fold per
   seed, add F166's stop guard to the SPECTRA module, replace the result
   with `replace=` stating why, and regenerate the 32 pages (about 60
   minutes, 0 metered seconds).
2. Commit the pages as they are, with the linear-form statement, and
   add a dated note to the entry recording the departure (about 15
   minutes).
3. Remove the SVM lane from the SPECTRA order, pairs and pages, with a
   dated note in the entry (about 30 minutes).

**Answer (team lead, 2026-11-05): 1.**

## D15. F177 change c: diff coverage at 100% is red on this branch, mostly on code only a real run executes. What does the gate require?

Asked 2026-11-05 at the end of Phase 4, after CI's first diff-coverage
report (run 42147689802 on eb8b438).

**What.** Change c (D8) fails CI's push job when a changed line in
`experiments/src`, `experiments/phase2/src`, `scripts` or
`.claude/hooks` is run by no test. The measurement works: code the
tests run in a subprocess is counted (`update_sprint_status.py`, run
that way, is at 95.1%). On this branch it reports 1,311 changed lines,
474 not run (63%), in 10 files:

- Run-only code, which needs the real data or a device and which no CI
  test can run: `exp5_router.py` 42.1%, `f157_qnn_ieee.py` 32.1%,
  `f157_spectra_algorithms.py` 48.0%, `f114_real_ceiling.py` 70.3%,
  `run_dirac3s_units.py` 61.0%. Most of their missing lines are the
  `run` and `main` paths.
- Gaps a test can close: some refusals in those same modules (for
  example `f157_spectra_algorithms.py` line 165, the refusal of an RBF
  refit whose validation AUPRC differs), and `f157_spectra_docs.py`
  90.7% (two `ClaimError`s, lines 66 and 82), `select_proofs.py` 62.5%
  (its `--run` path), `env_check.py` 76.6%, `update_sprint_status.py`
  95.1%, `f169_plugin_bins.py` 97.6%.

**Why it matters.** At 100% the push job is red on every sprint that
adds an experiment module, so the check reads as noise and is ignored,
which is worse than no check. The gaps in the second group are the
defect class change c exists for (37 untested branches reached review
in Sprints 28-30). The close-out hook blocks the completion claim while
CI is red, so this sprint cannot close with the gate as it is.

**Kind per option.** Option 1: Prevention. Option 2: Workaround now,
Prevention from Sprint 32. Option 3: Workaround.

**Cost per option** (0 metered seconds in each):
- Option 1: about 240 minutes, this sprint. Each run-only function gets
  `# pragma: no cover` with its reason on the same line ("run-only:
  needs the raw data" or "run-only: device call"); a new guard test
  fails a pragma with no reason, proven red. Every other uncovered
  line gets a test, each refusal proven red. The gate stays at 100%.
  About 15 files.
- Option 2: about 20 minutes, this sprint. The diff-coverage step
  reports and does not fail (`continue-on-error: true`) for Sprint 31.
  New card F182, "the run-only marks and the missing tests" (option 1's
  work, about 240 minutes), for Sprint 32 refinement; the step fails
  again when F182 ships. About 3 files.
- Option 3: about 15 minutes. Remove the diff-coverage step and its
  guard; keep `.coveragerc` for local use. About 3 files.

**Recommendation: 1.** It keeps the check that finds untested
refusals, and the reason on each pragma keeps an exclusion visible in
review. It costs about four hours before Manual Validation. Option 2 is
the choice if that time is better spent in Sprint 32: it loses one
sprint of the gate, not the gate.

**Options**

1. Build it now: run-only pragmas with reasons, a guard on the reasons,
   tests for every other uncovered line; the gate stays at 100%
   (about 240 minutes).
2. Report only for Sprint 31 (`continue-on-error: true`); card F182 for
   the pragmas and tests in Sprint 32; the gate fails again when F182
   ships (about 20 minutes now).
3. Remove the diff-coverage step and its guard (about 15 minutes).

**Changed since asked (2026-11-06).** Tasks M and N added code. On
107dd75 (CI run 42176650858) the step reports 1,434 changed lines, 478
not run (67%), in 11 files; `scripts/suite_times.py` (95.9%) is new to
the list, and `run_dirac3s_units.py` is at 65.9%. The rest of the push
job, and CI's full job with every red proof, are green on 107dd75, so
this step is the only red check. The options, costs and recommendation
are unchanged.

**Answer (team lead, 2026-11-06, Manual Validation).** Verbatim: "D15.
There is no way to justify 4 hours of this type of testing every sprint
or in any sprint and certainly not multiple times per sprint. Sprints
should only be taking 1-2 hours including all the testing needed. What
other options are possible, including removing or adjusting this test
requirement """ fails when any changed line of code is not run by a
test""""
None of D15's options is taken. The new options are D16. One fact for
the record: D15 option 1's 240 minutes was a one-time catch-up on this
branch's 478 lines; after it, a sprint would have paid only for its own
new lines. The answer rules it out for any sprint either way.

---

## D16. Diff coverage: what replaces the 100% gate? (follows D15)

Asked 2026-11-06 at Manual Validation, after D15's answer.

**What.** CI's push job fails when a changed line in `experiments/src`,
`experiments/phase2/src`, `scripts` or `.claude/hooks` is run by no
test (F177 change c). On cdb8471 (CI run 42194486482), 478 of 1,434
changed lines are not run. Counted from that run's report
(`--show-uncovered`) against the source: **19 of the 478 are refusal
lines** (`raise`, `SystemExit`, `sys.exit`), in 10 files. Some of the 19
are a `main` function's usage refusal. The other 459 lines are mostly
the `run` and `main` paths of experiment modules, which need the raw
data or a device and which no CI test can run.

**Why it matters.** The class change c exists for is the untested
refusal, term or state: 37 reached review in Sprints 28-30
(`docs/testing/F180_TESTING_ANALYSIS.md` Part 2). A gate on every line
is red on every sprint that adds an experiment module, so it is noise.
A gate on refusal lines only is aimed at that class and is red only
when a new refusal has no test, which the per-term rule already
requires. Measuring coverage also slows the push job: its Tests step
took 5:44 on cdb8471 against 2:04 without coverage on 0fc2004. The
team lead's target is a sprint of 1-2 hours including all testing.

**Kind per option.** Option 1: Prevention. Option 2: Prevention from
Sprint 32, Workaround for Sprint 31. Option 3: Workaround (a report,
nothing fails). Option 4: Workaround (the check is gone).

**Cost per option** (0 metered seconds in each; minutes are estimates,
unverified until done):
- Option 1: about 90 minutes this sprint. A filter script (about 30
  minutes, with a test and a red proof) makes the step fail only on an
  untested changed refusal line and list the other untested lines
  without failing; tests for this branch's 19 refusal lines (about 60
  minutes). Then, per sprint, a test for each new refusal, already the
  per-term rule. About 12 files.
- Option 2: about 30 minutes this sprint: the filter, report-only for
  Sprint 31 (`continue-on-error: true`). Card F182, "tests for Sprint
  31's 19 untested refusal lines" (about 60 minutes), for Sprint 32; the
  step fails again when F182 ships. About 4 files now.
- Option 3: about 20 minutes. The step never fails; it writes the
  untested refusal lines to the job summary, and the Phase 5 review
  lists them. The push job keeps the coverage slowdown. About 3 files.
- Option 4: about 15 minutes. Remove the diff-coverage step, its guard
  and the coverage measurement; keep `.coveragerc` for local use. The
  push job returns to about 3 minutes. Untested refusals are found by
  review only, as in Sprints 28-30. About 4 files.

**Recommendation: 2.** It keeps a gate aimed at the one class it
catches well, costs about 30 minutes now, and moves the 60-minute
catch-up to Sprint 32, where it can be sized into the sprint. Option 1
does the same work now, in a sprint that is already long. Option 3 is
a report nothing makes anyone read. Option 4 is the cheapest and gives
up the check.

**Options**

1. Refusal lines only, now: the step fails only on an untested changed
   `raise`/`SystemExit` line and lists the rest; tests for this branch's
   19 refusal lines (about 90 minutes now).
2. Refusal lines only, from Sprint 32: build the filter now, report-only
   for Sprint 31; card F182 for the 19 refusal tests in Sprint 32; the
   step fails again when F182 ships (about 30 minutes now).
3. Report only, permanently: the step never fails and lists untested
   refusal lines in the job summary for the Phase 5 review (about 20
   minutes).
4. Remove the diff-coverage step, its guard and the coverage
   measurement (about 15 minutes).

**Answer (team lead, 2026-11-06, Manual Validation): 1.** Verbatim:
"A3. a" and then "i chose option a." The terminal shows a numbered
list nested under a bullet with letters, so "a" is option 1.

**Changed since asked (2026-11-06).** Option 1 is built. Two facts
changed while it was built.

- 10 of the 19 untested refusal lines on this branch were module entry
  lines (`raise SystemExit(main())` and `sys.exit(main(...))`). They
  refuse nothing: they return the exit code of `main`. The check
  (`scripts/refusal_coverage.py`) treats them as ordinary lines, and a
  proof shows the rule can fail.
- The other 9 are real refusals. Each now has a test and a red proof:
  `f157_qnn_ieee.py` line 185, `f157_spectra_algorithms.py` line 355,
  `run_dirac3s_units.py` lines 165, 212 and 355, `env_check.py` line 44,
  `f157_spectra_docs.py` lines 68 and 84, and `select_proofs.py` line 42.
- The push job's Diff coverage step writes the diff-cover report as JSON
  and runs `scripts/refusal_coverage.py` on it. The step has no
  `--fail-under`. `test_ci_workflow.py` fails if either changes.

---

## D17. Test time: what runs where, so a sprint fits 1-2 hours? (V3)

Asked 2026-11-06 at Manual Validation, after the team lead's V3
comments: the CI full job must be faster than 20 minutes; a 20-minute
local non-proof run is too slow; "Can we run 5% each time via CI (on a
server) once per sprint" for the proofs; and V13's question about more
than one proof per file.

**What.** Measured this sprint:
- Local non-proof run: 962 s in parallel plus 506 s serial, about 24.5
  minutes (107dd75's code, 2026-11-06).
- Local red proofs: 4 h 11 min when shared code (`conftest.py`) changed,
  because change b then selects all 161 proof files.
- CI push job (every non-proof test): 6:45 on cdb8471, Tests step 5:44
  with coverage measured; 3:08 before coverage.
- CI full job (every test and every proof): 921 s of tests on 107dd75's
  second attempt; the first hit the 20-minute limit. About 500 of CI's
  657 s on 075c3ac were proofs (F180 Part 3).

What F180's risk-based analysis found (Parts 5 and 7): a proof tests the
test, not the code, so it shows nothing new unless its own test file,
the file it breaks, or the proof machinery changed. Each of the five
recorded proof failures in Sprints 28-30 was in a proof whose own files
had changed. Changed-files selection with a fallback is Microsoft's Test
Impact Analysis design; mutation testing in practice runs on changed
lines only (Petrovic and Ivankovic, ICSE-SEIP 2018). The local machine's
slowness is per-file cost (about 4-11 ms per file operation, low CPU),
inferred from on-access antivirus scanning, unverified.

**The proposed policy (options 1 and 2 build it):**
- (a) **Local: changed files only.** No local full non-proof run. A
  change runs the tests of the changed files and the repository guards
  that scan a changed directory. Target under 5 minutes; measured when
  built.
- (b) **CI push job: unchanged**, every non-proof test on every push.
  It is the safety net for (a), and runs on the server, not here.
- (c) **Proofs: on CI only, once per sprint at Phase 5, and at ready
  for review.** The full job runs the proofs the branch selects (own
  test or broken file changed), plus a 5% rotating sample of the rest:
  the sprint number picks the slice, so every proof runs at least once
  in 20 sprints. A shared-machinery change no longer selects all 161; it
  selects the sample plus the proofs of the proof machinery itself.
  Expected full job well under 20 minutes; measured when built.
- (d) **No two proofs with the same break** (V13): a guard fails two
  proofs that make the same mutation (same file, same old text, same new
  text). More than one proof per test file stays allowed, because each
  proof shows that one check can fail: a file with five refusals needs
  five. The defect in V13 was two proofs running at the same time, which
  the xdist refusal (62db122) already stops.

**What it gives up.** A proof made stale by an unrelated change can go
unseen for up to 20 sprints (the recorded cases were all caught by
changed-files selection). A local change can miss a test that depends
on a changed file only indirectly; the push job finds it minutes later.
A Windows-only failure is found only by a local run of the affected
files.

**Why it matters.** Under the current policy, testing alone can exceed
the 1-2 hour sprint target several times over.

**Kind per option.** Options 1 and 2: Prevention. Option 3: Workaround.

**Cost per option** (0 metered seconds in each; estimates, unverified):
- Option 1: about 120 minutes this sprint: (a) a changed-files test
  selector, (c) the sample and the shared-machinery change in
  `select_proofs.py` and the full job's selection in `ci.yml`, (d) the
  duplicate guard, each with a test and a red proof, and the checklist
  steps. About 8 files.
- Option 2: about 5 minutes now: card F183 with (a)-(d), about 120
  minutes, at the top of Sprint 32's plan. Sprint 31 closes under the
  current policy (its tests are already run).
- Option 3: no change.

**Recommendation: 2.** The work is the same, and Sprint 31's testing is
already done, so building it now saves nothing in this sprint and makes
it longer. In Sprint 32 it is the first task, so that sprint's own tests
run under the new policy.

**Options**

1. Build (a)-(d) now, in Sprint 31 (about 120 minutes).
2. Card F183 with (a)-(d) for the top of Sprint 32 (about 5 minutes
   now, about 120 minutes in Sprint 32).
3. No change to the test policy.

**Answer (team lead, 2026-11-06, Manual Validation): 1.** Verbatim:
"a4. a" and then "i chose option a." The terminal shows a numbered
list nested under a bullet with letters, so "a" is option 1.

**Changed since asked (2026-11-06).** Option 1 is built. One figure
above is wrong, and the full job changed shape.

- "161 proof files" is wrong. 161 was the count of proof tests. At
  cdb8471 there were 56 proof files; there are 58 now.
- The CI full job now runs every non-proof test, then the red proofs
  that `scripts/select_proofs.py --sample --run` selects: the proofs of
  each test file whose test or named file changed, plus this sprint's
  rotating sample of one proof file in 20. The proof step runs even when
  a test failed.
- A shared-machinery change (`injection.py`, a `conftest.py`,
  `pytest.ini`) selects only the test files that name it.
- Locally, `scripts/select_proofs.py --tests` runs the non-proof tests
  of the changed files, the files that name them, the tests that name a
  changed directory, and the repository guards (`test_us_english.py`,
  `test_evidence_immutability.py`). The folder rule counts only a
  changed non-Python file in a folder two or more levels deep: before
  that, almost every test named `docs` or `experiments/src`, and one
  task's change selected 110 of 163 files. With it, one task's change
  (`--base HEAD`) selects 30, which ran in 4 minutes 46 seconds. The
  whole sprint selects 99, so (a)'s
  under-5-minute target holds for a task, not at Phase 5; the Phase 5
  local run stays the parallel run.
- `test_no_duplicate_proofs.py` fails when two red proofs make the same
  mutation to the same file (change d). The repository has none now.

---

## D18. Backlog: which proposals from the learning-document review become cards? (A1)

Asked 2026-11-06 at Manual Validation, after the team lead's A1 review
asked: "Have you made any updates to the Phase 2 planning or backlog
based on what we learned in creating these 3 documents? if not, can you
propose changes and priorities for approval." No such update had been
made. The review also asked for a deep dive into investigation data and
for an experiment with superposition, entanglement and interference on
all the datasets.

**What.** Nine proposals, none carded yet. Each would be a new card in
`docs/ALL_SPRINTS_MASTER_PLAN.md`. Priority is the backlog's number
(lower runs sooner; F180 is 9, F114 16, F181 20, F157 30). All estimates
are [no-history] and unverified; every one costs 0 metered seconds.

From the team lead's review (group A):
- **F184. Data used, or usable, for fraud investigation** (~90m,
  research document). What banks, card networks and investigators
  record; which fields the public datasets lack; which of the team
  lead's suggestions (card, customer and advertising identifiers and
  histories, address, product, merchant, customer device, social media)
  are lawful and obtainable. Priority 25.
- **F185. A cost-weighted alert budget** (~60m). Rank by expected
  dollars saved net of review cost (EvidenceBasedDB
  `hoppner-instance-threshold`, high) on ULB's Amount and IEEE-CIS's
  TransactionAmt, against today's count-based 0.5% budget, using the
  stored scores. Priority 18.
- **F186. Card-testing sequences** (~90m). On an IEEE-CIS card-holder
  key: small-then-large pairs within 24 hours, their fraud rate, and the
  lift of velocity features at the budget. ULB has no card field.
  Priority 22.
- **F187. A circuit with all three quantum properties and many
  non-Clifford gates** (~120m, simulation only). Widths 8 to 20,
  non-Clifford count stepped past exact statevector cost; ULB, IEEE-CIS
  month 4 and SPECTRA's four datasets on the quantum-enhanced `target`
  label; the six F106 twins, HGB and a kernel surrogate. Gate-based
  hardware only if a circuit beats every twin, under its own approval.
  Related to F116 and F117 (HOLD). Priority 45.

From EvidenceBasedDB's ranked memo (group B):
- **F188. Rounding test** (~30m): round each IEEE-CIS selection instance
  to 200:1 and see whether F176's under-2e-05 gains survive. If not, no
  device run on that formulation can show anything. Priority 24.
- **F189. Solver sweep on the first design** (~45m): F176's solvers and
  a cardinality-penalty sweep on the ULB instances. Priority 50.
- **F190. Equal-feature comparison** (~60m): every classical lane on the
  proxy's 17 features, ULB and IEEE-CIS. Priority 35.
- **F191. Kernel copy and qubit sweep** (~120m): a classical surrogate
  for any quantum kernel, and kernel concentration from 2 to 14 qubits
  on fraud features. Priority 55.
- **F192. Bank-scale timing** (~120m): classical training and scoring at
  1, 10 and 100 million rows, beside a quantum step's loading and shot
  cost. Priority 40.

**Why it matters.** The documents now name these as next steps; without
cards they are not planned, and the team lead's two requests (the data
deep dive and the three-property experiment) have no home. Group A
answers questions a bank would ask first (money saved, card testing,
which data). Group B decides whether further device work can show
anything (F188 first).

**Kind per option.** Options 1 and 2: Prevention (the backlog records
the work, so it is planned and not lost). Option 3: Workaround.

**Cost per option** (0 metered seconds in each):
- Option 1: about 20 minutes now, one file (`ALL_SPRINTS_MASTER_PLAN.md`)
  plus the CHANGELOG: nine cards at the priorities above.
- Option 2: about 10 minutes now, the same file: F184-F187 only; group B
  stays as text in the learning documents.
- Option 3: no change.

**Recommendation: 1.** Group B's F188 is the cheapest test that decides
whether any further device run is worth approving, so it belongs in the
backlog beside group A.

**Options**

1. Add all nine cards, F184-F192, at the priorities above.
2. Add F184-F187 only, at the priorities above.
3. Add no cards.

**Answer (team lead, 2026-11-06): 1.** Verbatim: "D18 option 1 (all 9 cards)". Cards F184-F192 are added to `ALL_SPRINTS_MASTER_PLAN.md` at the priorities above.

---

## D19. Retrospective: what happens to the review findings not fixed in Task P?

Asked 2026-11-07 at the Phase 7 retrospective (step 6).

**What.** The PR 92 reviews found about 25 points. Task P fixed the six
that could write a wrong record or leave the merged HEAD ungated (961e564).
Three groups remain, listed in full in `SPRINT_31_RETROSPECTIVE.md`,
"Review findings not fixed":
- (a) Prove the Sprint 31 refusals red: proofs for thirteen tested refusals
  and terms, and two runner refusal tests moved onto temporary paths with
  stubs first, because a proof of either today would write into
  `experiments/phase2/results/` or open a device client. About 90 minutes.
- (b) The refusal gate sees `print("REFUSING: ..."); return N` and
  one-line raises, with a test for each such line the change shows. About
  60 minutes.
- (c) The latent set: eight defects that no recorded run has hit
  (Experiment 5's score path, F114 `--lr05`'s stage-1 check, `run_rbf`'s
  seeds, `provenance.start(replace=)` with `resumable`, `os.link` cleanup,
  two `f157_spectra_docs` branches, Experiment 5's untested `edges()` and
  `accept()` refusals). About 120 minutes.

**Why it matters.** Fixing all three now adds about 270 minutes to a
sprint already at 2,893 active minutes against a 1-2 hour target. Left
uncarded, (a) and (b) leave refusals the D16 gate exists for unchecked.
None changes a recorded result: the reviewers checked the three runs the
latent set could touch.

**Kind.** Options 1 and 2: Prevention (carded with acceptance criteria,
so each is built and proven). Option 3: Prevention now, at the cost of
the sprint time. Option 4: Workaround.

**Cost.** Option 1: about 10 minutes now (one card, F194, with all three
groups, priority 12). Option 2: about 10 minutes now (two cards: F194 for
(a) and (b) at priority 12, F195 for (c) at priority 28). Option 3: about
270 minutes now. Option 4: none.

**Recommendation: 2.** (a) and (b) complete D16's gate and belong at the
top of Sprint 32; (c) is latent and can wait behind the experiments.

**Options**

1. Card all three groups as F194, priority 12.
2. Card (a) and (b) as F194, priority 12, and (c) as F195, priority 28.
3. Fix all three now, in Sprint 31.
4. Card nothing; the findings stay in the retrospective only.

**Changed since asked (2026-11-07, 5:45pm).** Group (b) is done: the team
lead's D20 answer chose i3 alternative b, which is group (b), and it is
in ca774e7. The options above keep their numbers and now cover (a) and
(c) only: option 1 cards (a) and (c) as F194; option 2 cards (a) as F194
and (c) as F195; option 3 fixes (a) and (c) now, about 210 minutes;
option 4 is unchanged. The recommendation stays 2.

**Changed since asked (2026-11-07, 6:40pm).** The team lead asked for
retrospective items in the format of `SPRINT_RETROSPECTIVE.md` step 5.
D19 is now two items in `SPRINT_31_RETROSPECTIVE.md`, "Open items":
i6 (group a) and i7 (group c), answered by letter. Option 1 is closest
to i6 a with i7 b (both at priority 12, as two cards); option 2 is i6 a and i7 a; option 3 is i6 b and i7 c;
option 4 is i6 e and i7 e.

---

## D20. Retrospective: which improvements are applied now?

Asked 2026-11-07 at the Phase 7 retrospective (step 6). The five
proposals are in full in `SPRINT_31_RETROSPECTIVE.md`, "Improvements
proposed".

**What.**
- IMP-1: a refusal test stubs what the refusal protects (a Phase 4
  checklist line). About 5 minutes.
- IMP-2: a result is marked complete only by a check that it is (a
  guard). About 60 minutes; red on arrival until D19's (c) is fixed.
- IMP-3: the refusal gate sees the repository's refusal forms. The same
  work as D19's (b).
- IMP-4: Phase 3 states the plan's total beside the 1-2 hour target and,
  when it is over, asks the scope as a decision with a cut option. About
  10 minutes.
- IMP-5: a research estimate uses the median ratio of the last three
  sprints' measured research rows. About 10 minutes.

**Why it matters.** IMP-4 and IMP-5 answer category 3 (Poor): this sprint
ran 1.69 times its estimate and far over the time target. IMP-1 answers
the proof that ran without end for 83 minutes.

**Kind.** All Prevention.

**Cost.** Option 1: about 25 minutes now, three files
(`SPRINT_CHECKLIST.md`, `SPRINT_PLANNING.md`, the CHANGELOG), and IMP-2
and IMP-3 to the backlog. Option 2: about 85 minutes now. Option 3: about
5 minutes now (all five to the backlog).

**Recommendation: 1.** IMP-1, 4 and 5 are text rules that cost minutes;
IMP-2 needs D19's (c) first, and IMP-3 is D19's (b).

**Options**

1. Apply IMP-1, IMP-4 and IMP-5 now; IMP-2 and IMP-3 to the backlog.
2. Apply all five now.
3. Apply none now; all five to the backlog.

**Changed since asked (2026-11-07, 4:55pm).** At the team lead's request,
the improvements are now in the ADR review format
(`SPRINT_RETROSPECTIVE.md` step 5) and numbered i1 to i5. IMP-1 is i1,
and so on to IMP-5, which is i5. Each now has alternatives a, b and c
with pros and cons, in `SPRINT_31_RETROSPECTIVE.md`, "Improvements
proposed". Option "applied now" means alternative a of that improvement.
The options above and their numbers do not change, and neither does the
recommendation (1).

**Answer (team lead, 2026-11-07), per improvement, not a numbered
option.** Verbatim: "i1. a i2. b i3. b i4. not needed - skip i5. not
needed. skip". So:
- i1, alternative a, now: the Phase 4 checklist line.
- i2, alternative b, now: the complete-check test, with the open places
  listed as exceptions until D19 group (c) fixes them.
- i3, alternative b, now: the refusal gate sees `REFUSING` lines and
  one-line raises, with a test for each such line the branch changed.
  This is D19 group (b), done now.
- i4: skipped.
- i5: skipped.

---

## D21. Retrospective: i2 cannot be built as answered; which way now?

Asked 2026-11-07 at the Phase 7 retrospective (step 7), after the team
lead's D20 answer "i2. b".

**What.** i2 alternative b was "build the complete-check test now, with
the two known open places as exceptions". A scan of
`experiments/phase2/src/` finds 18 places that write a literal
`complete: True`. 5 have a refusal earlier in the same function. 13 do
not: `f114_real_ceiling.main`, `f157_spectra_algorithms.run` and
`run_rbf`, `f158_fraud_types.main`, `f160_room_ieee.main`,
`f166_ulb_algorithms.run`, `f169_plugin_bins.main_lr05` and `main`,
`f170_missed_neighbors.main`, `f171_budgets.main`,
`f171_missed_ieee.main`, `f174_ieee_algorithms.run` and
`run_dirac3s_units.dry_run`. So the exception list holds 13 places, not
2. Most write "complete" after a loop over the whole plan, so they may
be complete by construction; the reviews found two real gaps
(`main_lr05`, `run_rbf`).

**Why it matters.** The test stops a new partial run from being recorded
as complete. The exception list decides how much of that protection
reaches the existing code now.

**Kind.** Option 1: Prevention for new code; the 13 stay as they are
until reviewed. Option 2: Prevention, complete. Option 3: Workaround
(nothing now).

**Cost.** Option 1: about 45 minutes, a new test file plus the
regenerated test inventory; the 13 are listed with the repository's
shrink-only pattern (`frozen_list.check`), so a place can leave the list
and never join it. Option 2: about 3 hours: option 1, then each of the
13 gets a check before it or a stated reason why it is complete by
construction. Option 3: about 10 minutes, a new card F196, priority 28,
with i2's alternatives b and c recorded in it.

**Recommendation: 1.** It gives what b was chosen for, new cases stopped
now, at about 45 minutes. It extends the existing frozen-list pattern,
and the list can only shrink. Option 2 adds about 2 hours to a sprint
already far over its target.

**Options**

1. Build the test now with all 13 places as a shrink-only exception list.
2. Build the test now and review all 13 places now (about 3 hours).
3. Do not build it now; card it as F196, priority 28.

**Changed since asked (2026-11-07, 6:40pm).** The team lead asked for
retrospective items in the format of `SPRINT_RETROSPECTIVE.md` step 5.
D21 is now item i2 in `SPRINT_31_RETROSPECTIVE.md`, "Open items",
answered by letter. Option 1 is i2 a, option 2 is i2 b, option 3 is
i2 c. New: d (the check inside `provenance.write_result`, card F196),
e (skip and track) and f (skip). The recommendation stays the same (a).
