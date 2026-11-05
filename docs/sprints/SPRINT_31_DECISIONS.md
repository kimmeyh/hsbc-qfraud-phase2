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
