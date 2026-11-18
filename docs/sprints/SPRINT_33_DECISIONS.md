# Sprint 33 Decisions

Every decision or question asked of the team lead in this sprint, in full,
as first asked. A question asked again is pasted from here unchanged: same
ID, same wording, same option numbers. If facts change after it is asked, a
dated "Changed since asked" note goes below the original; the original is
never edited. The answer is recorded under each entry.

---

## D1. Which document(s) does "the document(s) to be submitted" mean?

Asked 2026-11-16 at backlog refinement Pass 2 (Phase 8.4).

**What.** The team lead set the refinement scope on 2026-11-16: "Will
include prep for submission and only what is directly related to
completing the document(s) to be submitted." This repository does not
name a Phase 2 document to be submitted. It does not record whether the
team was selected for the PoC, and the Phase 2 brief is not in it.

**Why it matters.**
- The answer decides which cards are in the slate. D2's options differ
  by this answer.
- `docs/phase2/PHASE2_POC_PLAN_DRAFT.md` names one outward document: the
  PoC report, its stage 3 (PoC weeks 12-14), for Review and Close from
  1 Mar 2027 (roadmap page). The cards that feed it are F199 (new), F198,
  F13, F102, F197 and F157.
- `docs/phase2/PHASE2_POC_PLAN.md` (F13) is the plan for the PoC window.
  Whether the program asks for it as a submission is not recorded here
  (unverified).

**Kind per option.** Not applicable: this is a scope question, not a
fix.

**Cost per option.** None to answer. Each option's cards are costed in
D2.

**Recommendation: 1.** The PoC report is the one outward document the
plan draft names. A skeleton of it (F199) shows every gap before the
PoC's runs start.

**Options.**

1. The PoC report: stage 3 of `PHASE2_POC_PLAN_DRAFT.md`, submitted for
   Review and Close (from 1 Mar 2027).
2. The PoC plan: `docs/phase2/PHASE2_POC_PLAN.md` (F13), with the brief's
   terms replacing the draft's assumptions [A1]-[A8].
3. Both the PoC report (1) and the PoC plan (2).

---

## D2. Which cards make up Sprint 33?

Asked 2026-11-16 at backlog refinement Pass 2 (Phase 8.4), with D1. Its
options are written separately for each D1 answer.

**What.** Sprint 33's scope, from the 2026-11-16 slate in
`docs/ALL_SPRINTS_MASTER_PLAN.md`, under the team lead's submission
scope.

**Why it matters.**
- The time target is 1-2 hours a sprint, all testing included (team
  lead). Sprint 32 recorded 188 active minutes against 345 estimated,
  but five of its ten rows are understated (their timers started late),
  so no calibration ratio is applied here.
- F199 writes the PoC report's skeleton: one section per filed
  commitment, its sources, its state and its gaps. Every later card can
  then be picked from a named gap.
- F198 decides whether any device run on F25's formulation can show a
  result at finer resolution or another ridge weight. That is the open
  question in the report's Experiment 3 section, the one device
  experiment.
- F197 adds an Experiment 5 reading. The report can already state F121's
  result as it stands.
- F13 needs the brief's terms, which are not in this repository. The
  team lead would supply them.
- F178's per-sprint learning-document update is a standing Phase 5 step,
  but it does not complete a submitted document. No option carries it,
  so under this scope Sprint 33 skips that step.

**Cards.** Minutes are card estimates, all `[no-history]`; 0 metered
seconds in every card. Phase 3 planning, the reviews and the
retrospective are not in these figures.
- F199, the PoC report skeleton: 60m; about 2 files (the draft, the
  figure registry if a figure needs it). A deliverable.
- F198, F188 extended: 30m; about 4 files (an entry amendment, the
  module or its options, a result file, a document). Research.
- F197, the Experiment 5 re-entry draft: 60m; 1-2 files (a new entry, a
  saturation check). Research.
- F13, the PoC plan with the brief's terms: 75m; 2 files (the plan and
  the draft). A deliverable.

**Kind per option.** No option carries a Prevention or a Workaround:
each card is a deliverable or research toward the submitted
document(s).

**Cost per option.**
- Option 1: 90 minutes by card; 0 metered seconds; about 6 files.
- Option 2: 60 minutes by card; 0 metered seconds; about 2 files.
- Option 3: 150 minutes by card; 0 metered seconds; about 8 files.
- Option 4: 75 minutes by card; 0 metered seconds; 2 files.
- Option 5: 135 minutes by card; 0 metered seconds; about 4 files.

**Recommendation.** If D1 is 1: option 1. If D1 is 2: option 4. If D1 is
3: option 5. Option 1 fits the 1-2 hour target and pairs the report's
map with the one experiment question still open on it. Option 5 is
above the target by card estimate; it is recommended for D1 = 3 because
both documents are then in scope and F13 cannot start without the
brief anyway.

**Options.**

If D1 is 1 (the PoC report):

1. F199 and F198 (90 minutes by card).
2. F199 only (60 minutes by card).
3. F199, F198 and F197 (150 minutes by card).

If D1 is 2 (the PoC plan):

4. F13 only, with the team lead supplying the brief (75 minutes by
   card).

If D1 is 3 (both):

5. F199 and F13, with the team lead supplying the brief (135 minutes by
   card).

**Changed since asked (2026-11-16).** The team lead proposed a scope
instead of answering D1 and D2: F13, F199, F102 and an F178 update, with
the goal "the Phase 2 registration document ready to submit". D1 and D2
are superseded by D3.

---

## D3. Sprint 33 scope for the goal "Phase 2 registration document ready to submit"

Asked 2026-11-16, in discussion of the team lead's proposed scope.

**What.** The team lead proposed F13, F199, F102 and an F178 update.
The registration document is `experiments/phase2/PREREGISTRATION_DRAFT.md`
(card F102).

**Why it matters.**
- F102 is the goal. Its section 7 lists what remains before filing: one
  item is stale (it says Experiments 2-6 have no entry; section 6 shows
  all six written), and one is the filing date and venue, the team
  lead's decision. Its 3h estimate is from 2026-10-13, when the draft
  was new; the remaining work is smaller (about 120m, unverified).
- F13 replaces the PoC plan's assumptions with the brief's terms. The
  brief is not in this repository. Without it, F13 cannot do that work.
  With it, the brief's data and metrics terms ([A2]) can change section
  2 of the draft, so F13 should run before F102 is closed.
- F199 is a skeleton of the PoC report, not of the registration
  document. One part of it serves the goal: a check that each of the six
  filed commitments has a current entry. That check can be part of F102.
- F178's update does not serve the goal. It is the team lead's standing
  step and is cheap.
- The four cards total about 360 minutes by card estimate, three times
  the 1-2 hour target.

**Kind per option.** No option carries a Prevention or a Workaround:
each card is a deliverable.

**Cost per option.**
- Option 1: about 360 minutes by card (F13 75, F199 60, F102 180, F178
  45); 0 metered seconds; about 9 files.
- Option 2: about 240 minutes by card (F102 120, F13 75, F178 45); 0
  metered seconds; about 6 files.
- Option 3: about 165 minutes by card (F102 120, F178 45); 0 metered
  seconds; about 4 files.

**Recommendation.** Option 2 if the brief can be placed in this
repository this sprint; option 3 if not. F199 is deferred in both: it
serves the PoC report, and its coverage check moves into F102.

**Options.**

1. As proposed: F13, F199, F102 and the F178 update.
2. F102 (resized, with F199's coverage check), F13 with the brief, and
   the F178 update. F199 deferred.
3. F102 (resized, with F199's coverage check) and the F178 update. F13
   and F199 deferred.

Asked with D3, as questions of fact: Q1, can the Phase 2 brief go into
this repository this sprint? Q2, where and to whom is the preregistration
submitted? Q3, should the filed document separate "registered and already
run, with result" from "registered, to be run in the PoC"?

**Answer (team lead, 2026-11-16): 2.** Verbatim: "q1 we are going to have
to file without the brief. Make assumptions as best possible. q2. don't
know yet. leave blank and changable until notified otherwise.  We will
have to make assumptions about all missing information. q3. yes d3. 2".
So F13 runs on stated best-possible assumptions in place of the brief;
the filing venue and date stay blank and changeable; section 6 separates
run entries from entries to run.

## D4. One learning document or three?

Asked 2026-11-17, at Manual Validation, after an outside machine learning
expert's review of the plain-terms learning document.

**What.** The learning documents are three files: plain terms, machine
learning expert and quantum computing expert. The reviewer did not know
which to read, read the plain-terms one, and worried that the expert
versions held something important. The reviewer suggested one combined
document. The plain-terms document's 2026-11-17 version now says "read
this one", and that the expert versions cover the same experiments with
more method detail. Almost every result file the expert versions cite is
cited in the plain-terms version too; the exceptions are
`docs/RESULTS_MEMO.md`, `experiments/phase2/results/f158_fraud_types.json`
and `docs/sprints/SPRINT_26_SUMMARY.md` (checked 2026-11-17).

**Why it matters.** Three files mean every update is made three times
(Sprint 33 Task C was), and a reader must choose. One file removes the
choice and the triple upkeep, but it is longer, and the expert detail
must be marked so a general reader can skip it. The answer also sets how
the team lead's coming review of the two expert versions is done: as a
review of two files, or as a merge.

**Kind per option.**
- Option 1: Prevention (one file cannot drift from another, and the
  reader has no choice to make).
- Option 2: Workaround (the "which to read" note answers the reader;
  the triple upkeep stays).

**Cost per option.**
- Option 1: about 90 minutes; 0 metered seconds; 4 files (the
  plain-terms document; the two expert documents, removed, with links to
  them redirected; `experiments/src/test_learning_docs.py`, whose
  three-document checks and proofs change).
- Option 2: 0 minutes now (already done); each later update stays three
  edits.

**Recommendation.** Option 1, after the team lead's review of the expert
versions, so that review's feedback is applied once, in the merged file.
The plain-terms version already holds the most results, so it is the
base.

**Options.**

1. Combine: the plain-terms document becomes the only learning document.
   The expert versions' extra method detail moves into it under marked
   "For machine learning experts" and "For quantum computing experts"
   parts, the two expert files are removed, and the guard checks one
   file. Done after the team lead's review of the expert versions.
2. Keep three documents, with the plain-terms document's "which version
   to read" note.

**Answer (team lead, 2026-11-17): 2.** Three documents stay.

## D5. How to apply the adversarial review of the preregistration draft

Asked 2026-11-17, at Manual Validation (action A1).

**What.** A Fable adversarial review of
`experiments/phase2/PREREGISTRATION_DRAFT.md` (read at 0a0e658) found 8
Blockers, 14 Major and 9 Minor findings, R1 to R31. Every figure it
checked against a result file matched. The Blockers are statements that
were true of a working draft and are false of a filing (R1 "fixed
before any Phase 2 result is seen"; R2 "no Phase 2 SPECTRA result exists
yet"; R3 "every Phase 2 experiment gets one entry"), a filing that
commits to no fully specified future test (R4), a device release rule
with no decision rule (R5), state paragraphs that spell out the
predictions that held and only link the ones that failed (R6), private
vendor material reachable from the draft (R7), and per-row score files
the entries depend on that are not tracked (R8). R5 and R7 are asked
separately (D6, D7). I checked R1, R2, R3, R7, R8 and R10 against the
files myself; each holds.

**Why it matters.** The draft is not filed, so every word can change. A
filed preregistration that says its designs were fixed before any
result was seen, when 23 of its 25 rows had already run, is the first
thing an outside reviewer attacks. Each fix is text: an in-place edit
for the header, Filing, sections 1 to 5, the table and the state
paragraphs; a dated note under an entry that has already run (the
draft's own rule). One revision-log row dated 2026-11-17 covers them.

**Kind per option.**
- Option 1: Prevention (the claims a reviewer would attack are fixed
  before filing, and section 1's rule is restated so later entries meet
  it).
- Option 2: Workaround (the Minor findings stay open for your review).
- Option 3: Workaround (nothing changes until you read the findings).

**Cost per option.**
- Option 1: about 90 minutes; 0 metered seconds; 4 files (the draft, the
  PoC plan draft, the guard's registered figures if a new decimal is
  needed, CHANGELOG).
- Option 2: about 70 minutes; 0 metered seconds; the same 4 files.
- Option 3: 0 minutes now.

**Recommendation.** Option 1. The Minor findings are cheap, and leaving
them means a second revision round on the day of filing.

**Options.**

1. Apply every finding except R5 and R7 (each its own decision) as the
   review proposes, then rerun the drift guard and its proofs and a
   fresh-eyes check of the changed text.
2. Apply the Blocker and Major findings except R5 and R7; leave R23 to
   R31 for the team lead's own review.
3. Apply nothing yet; the team lead reads the findings first.

**Answer (team lead, 2026-11-17): 1.** Applied as Task F (#128).

## D6. Experiment 3's device release rule (changes Sprint 32 D4's basis)

Asked 2026-11-17, at Manual Validation.

**What.** Sprint 32 D4 holds F25 until "F188's delivered reading beats
greedy at 200:1". The review (R5) found that the delivered reading
compares the rounded problem's pick, with weights solved on the rounded
problem, against greedy solved on the unrounded problem. On three of the
six instances the pick is greedy's own selection and still scores worse,
so the comparison measures the rounding of the weights as well as the
selection, and no selection can pass on those instances. The rule also
does not say on how many instances, by what margin, or how F198's other
ridge weights and resolutions count. (Checked by the reviewer against
`experiments/phase2/results/f188_rounding_delivered.json`; I have not
rechecked it.)

**Why it matters.** As written, the rule cannot be passed on half its
instances, and an analyst can vary ridge weight and resolution until it
passes. Either is a defect a reviewer finds.

**Kind per option.**
- Option 1: Prevention (a fixed, passable rule, with variants as dated
  amendments).
- Option 2: Workaround (the defect is disclosed and stays).

**Cost per option.**
- Option 1: about 20 minutes; 0 metered seconds; 3 files (the draft, the
  PoC plan draft, `docs/phase2/F188_ROUNDING.md`) plus a "Changed since
  asked" note under Sprint 32 D4.
- Option 2: about 10 minutes; 0 metered seconds; 2 files.

**Recommendation.** Option 1. It keeps the intent of D4 (no device run
until a gain survives the device's resolution) and makes it testable.

**Options.**

1. Replace the rule with: on F176's six instances at R = 200, the
   rounded problem's pick delivers a gain of more than 1e-6 against
   greedy's selection solved the same way (on the rounded problem,
   scored on the real one), on at least one instance. Any other ridge
   weight, resolution or dataset (F198) is a new dated amendment written
   before its run.
2. Keep D4's rule as worded, and add the caveat that on three of the
   six instances the pick is greedy's own selection.

**Answer (team lead, 2026-11-17): 1.** Applied as Task F (#128), with a
"Changed since asked" note under Sprint 32 D4.

## D7. Private material in the now-public repository

Asked 2026-11-17, at Manual Validation.

**What.** The repository became public on 2026-11-17. The review (R7)
found tracked text that may not be meant for the public: the substance
of QCi's answers to our questions, with quotes from QCi staff
(`docs/phase2/DIRAC_UNDERSTANDINGS.md`); the device-time allocation
request and grant (`docs/HARDWARE_PLAN_PHASE_2.md` and sprint records);
and the account balance in device call logs and the cost ledger. The
same file records QCi's standing request of 2026-09-25 that we present
our device readings as our own findings, not as conclusions QCi
validated; the draft says "QCi confirmed it on 2026-10-21". The filed
team profile in `docs/paper/` carries the team lead's personal email
address. The review found no credentials. Removing text now does not
remove it from the public history.

**Why it matters.** It may break QCi's request and expose commercial
terms and personal contact details. Each day public widens the copies.

**Kind per option.**
- Option 1: Prevention (exposure stops first; each item is then decided
  with the facts).
- Option 2: Workaround (the current text goes; the history keeps it).
- Option 3: Workaround (nothing changes until QCi is asked).

**Cost per option.**
- Option 1: your action in GitHub settings (about 2 minutes), then about
  30 minutes for me to list every tracked item with its location; 0
  metered seconds; no file changed until you decide each item.
- Option 2: about 40 minutes; 0 metered seconds; 3 files (the draft,
  `docs/phase2/DIRAC_UNDERSTANDINGS.md`, `docs/HARDWARE_PLAN_PHASE_2.md`).
- Option 3: 0 minutes now.

**Recommendation.** Option 1. Only you know what QCi has agreed to, and
making the repository private again is the one step that stops further
copies while that is checked.

**Options.**

1. You set this repository private again now (GitHub, Settings, Danger
   Zone, Change visibility). I then list every tracked item with QCi
   correspondence, commercial terms or personal details, for a decision
   on each before it is public again.
2. Keep it public. I remove the draft's two QCi attributions (R7's
   wording), the Q&A substance in `docs/phase2/DIRAC_UNDERSTANDINGS.md`
   and the allocation figures in `docs/HARDWARE_PLAN_PHASE_2.md` in a
   new commit. The balance fields in evidence files and the filed team
   profile stay, because evidence files and documents of record are not
   edited.
3. Keep it public and change nothing until you have checked with QCi.

**Answer (team lead, 2026-11-17), none of the three as written.**
Verbatim: "I though the qci correspondence folder was gitignored? if
so, would that work. Otherwise we have a non-repository directory
D:\Data\Harold\hsbc-quantum-fraud-2026 and would that work? definately
keeping it public but private correspoondance with QCi if at all
possible. docs/phase2/DIRAC_UNDERSTANDINGS.md and
docs/HARDWARE_PLAN_PHASE_2.md can be public". So: the repository stays
public; the correspondence stays private; the two named documents stay
as they are. Checked 2026-11-17: `docs/qci_package/` is gitignored
(`.gitignore` line 70), and no file under any `qci_package` path is in
any commit, so the received correspondence was never public. The draft's
two QCi attributions are reworded to our own reading in Task F, per
QCi's standing request of 2026-09-25 recorded in
`docs/phase2/DIRAC_UNDERSTANDINGS.md`. One gap is asked as D8.

## D8. Three outgoing QCi letters in the public git history

Asked 2026-11-17, at Manual Validation, after D7's answer.

**What.** QCi's own correspondence was never committed (D7). But three
of our OUTGOING drafts to QCi were tracked, two from the first commit
(2026-08-30) and `docs/paper/qci_cover.md` from d9d7dad (2026-09-04),
until commit 8151ddf (2026-09-17, "Move the QCi correspondence out of the
public repository"): `docs/paper/qci_cover.md` ("Dirac-3 Expanded
Access: The Commercial Case", a request for 30,000 QPU seconds),
`docs/qci-sponsorship-request.md` and `docs/qci-sponsorship-email.html`
(the sponsorship request and its email form). They hold the team lead's
words and our commercial ask; I found no text written by QCi in them.
Because the repository is public, every commit before 8151ddf, and so
these three files, can be read now. The tag `qci-letter-sent-20260908`
also points into that history.

**Why it matters.** The ask and its terms are visible to anyone who
browses the history. Removing them means rewriting every commit since
the first, which changes every commit hash. This repository's documents
cite commit hashes as evidence (for example, the preregistration draft's
"git records that order", and Experiment 4's source commit), so those
citations would stop resolving. GitHub also keeps pull-request refs and
cached views, which only GitHub Support can purge.

**Kind per option.**
- Option 1: Workaround (the letters stay readable in history).
- Option 2: Prevention (the letters leave the history), at the cost of
  every cited commit hash.

**Cost per option.**
- Option 1: 0 minutes; 0 files.
- Option 2: about 60 minutes for me, plus a request you send to GitHub
  Support; every branch and tag rewritten and force-pushed (each force
  push is your approval); every commit hash cited in this repository's
  documents re-mapped or marked stale.

**Recommendation.** Option 1. The files are your own outgoing request,
with no QCi text, and the request was sent; the cost of option 2 falls
on the evidence trail the preregistration relies on.

**Options.**

1. Leave the history as it is. The three letters stay readable in the
   commits before 8151ddf.
2. Rewrite the history to remove the three files from every commit
   (git filter-repo), force-push every branch and tag, ask GitHub
   Support to purge cached views and pull-request refs, and re-map every
   commit hash cited in this repository's documents.

**Answer (team lead, 2026-11-18): 1.** The history stays as it is.

## D9. A second review of the preregistration draft, by a different method

Asked 2026-11-18, at Manual Validation (team lead: "How can I do a
second review of the draft, but using a somewhat different approach so
that we can find thing that may not have been found the last time").

**What.** The first review (Fable, 2026-11-17) was one free-form
adversarial read with full repository access, in priority order. It
sampled: its "not checked" list names F94, F107, F108's arms, F156,
F169, several "already seen" figures and every external paper. A second
review finds most when it changes the method, the access or the model.

**Why it matters.** Each method has blind spots. A reader with the
repository fills gaps a filing reader cannot. A sampled check misses
what it did not sample. A free-form read finds what looks wrong, not
what is missing against a standard.

**Kind per option.** All three are Prevention (each targets a class the
first review could not see).

**Cost per option.**
- Option 1: about 30 minutes; one agent; 0 metered seconds; no file
  changed until findings are approved.
- Option 2: about 60 to 90 minutes; 6 to 8 agents in parallel, which is
  a multi-agent workflow you must opt into; 0 metered seconds.
- Option 3: about 40 minutes; one agent; 0 metered seconds.

**Recommendation.** Option 1, on the draft as it stands after Task F,
run by a different model from the first review (Opus). It is the
cheapest, and it tests the draft as the filing's reader will meet it.

**Options.**

1. Cold reader: a reviewer gets only the draft's text, with no
   repository, playing the program's judge. It reports every term,
   identifier or claim it cannot understand or check, and every place it
   must take the team's word.
2. Exhaustive claim audit: a script lists every sentence in the draft
   with a figure, a verdict or a citation; agents check each one against
   its source, entry by entry, including the first review's "not
   checked" list and the external papers' public text.
3. Standard and gaming: a reviewer scores each section 6 entry against
   the OSF Preregistration template's items, then tries to reach a
   favorable result inside the written rules: every choice still free
   after filing, and a way to pass Experiment 3's release rule.
4. Options 1 and 3 together, in parallel (two agents, about 40 minutes).

**Answer (team lead, 2026-11-18): 2, with a change.** Verbatim: "d9. 2
however not using super-agent mode, just several agents all running
opus 5.5 - OK if it takes 7 hours". So: no multi-agent workflow; several
separate agents, each on Opus 5.5, each read only, one per block of the
draft. Up to 7 hours is acceptable.
