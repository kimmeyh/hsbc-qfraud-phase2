# Sprint 34 Decisions

Each decision is written here in full before it is asked (CLAUDE.md).
A decision asked again is pasted from this file unchanged.

## Q1. The filing venue

Asked 2026-11-19 at backlog refinement Pass 2 (Phase 8.4), before D1.

**What.** The preregistration's Filing section gives the date
(2026-11-18) and "Filing venue: not set". Section 7 runs the lock step
(F102) only after the venue is recorded. This is a fact question, not a
decision: type the venue, or "not known".

**Why it matters.** D1 option 2 adds the lock step. It can run only if
the venue is known.

## D1. Which cards make up Sprint 34?

Asked 2026-11-19 at backlog refinement Pass 2 (Phase 8.4).

**What.** Sprint 34's scope, from the 2026-11-19 slate in
`docs/ALL_SPRINTS_MASTER_PLAN.md`. The submission scope set on
2026-11-16 is kept: "prep for submission and only what is directly
related to completing the document(s) to be submitted". At Sprint 33's
close the team lead said: "We will do the official filing and
experiment 3 in sprint 34".

**Why it matters.**
- F200 is the filing's first test. Its verdict decides whether F25's
  device arm can leave HOLD, which the PoC plan and report both need.
- F201 must ship before the first scored result after filing (section
  2 of the filed text). Without it, the next scored result breaks the
  filed reporting rule.
- F202 removes a false refusal in the push gate added in Sprint 33.
- F178 is updated every sprint; this update states F200's result.
- F102's lock step makes the filed text unchangeable by test. It needs
  the venue (Q1).
- The sprint target is 1-2 hours including testing.

**Kind per option.**
- Option 1: Prevention (F201 and F202 stop a broken reporting rule and
  a false refusal; F200 and F178 are planned work, not fixes).
- Option 2: Prevention (option 1, plus the lock that stops any later
  edit to the filed text).
- Option 3: Prevention (option 1), plus planned work (F199).
- Option 4: planned work only; F201's gap stays open.

**Cost per option.** Zero metered seconds in every option.
- Option 1: about 135 minutes (F200 45, F201 45, F202 15, F178 30);
  about 8 files.
- Option 2: about 195 minutes (option 1 plus F102 60); about 11 files.
- Option 3: about 195 minutes (option 1 plus F199 60); about 9 files.
- Option 4: about 75 minutes (F200 45, F178 30); about 5 files.

**Recommendation: 1.** It does what the team lead named for Sprint 34
that can run now (Experiment 3's rule), closes the reporting gap the
filing opened (F201) before any new score, and stays near the 1-2 hour
target. Choose option 2 instead if Q1 gives a venue: the lock is then
unblocked and is the other half of "the official filing".

**Options.**

1. F200, F201, F202 and the F178 update.
2. F200, F201, F202, the F178 update and F102's lock step, with the
   venue from Q1. Only if Q1 gives a venue.
3. F200, F201, F202, the F178 update and F199.
4. F200 and the F178 update.

**Answers (team lead, 2026-11-21, at planning).**
- Q1: "not known yet".
- D1: none of options 1-4. The team lead set the scope directly:
  "Sprint 34 Scope should include the below items": F200, F201, F202,
  F178, F102, F198, F197 and F157. With it, verbatim: "this is the first
  sprint after submitting pre-registration for Phase 2. It is possible
  that we will be asked to update the pre-registration after receiving
  additional information from the Quantum Insider team. We will want to
  preserve what has been submitted so far and provide new document with
  updates if we are asked to submit again."

## Q2. Which text was submitted?

Asked 2026-11-21 at planning (Phase 3), with D2-D4.

**What.** `experiments/phase2/PREREGISTRATION_FINAL.md` changed in three
commits on 2026-11-18. A lock must hash the bytes that were actually
sent. This is a fact question.
- d96ad30 (08:35): the first copy. Filing date and venue "not set".
- b8e2c0e (08:54): the filing date set to 2026-11-18.
- c3d3c00 (09:18): section 7's lock wording from the PR #122 review,
  and two revision-log rows. This is the current file.

**Why it matters.** D3 option 1 locks the text named here. If the sent
text is an earlier commit, the current file is not what was submitted.

**Options.**

1. c3d3c00, the current file.
2. b8e2c0e.
3. d96ad30.
4. Not known.

## D2. Where does text written after filing go?

Asked 2026-11-21 at planning (Phase 3).

**What.** Four selected cards write preregistration text after filing:
F200's result note (Experiment 3), F198's amendment before its run,
F197's new Experiment 5 entry, and the venue when it is known. The filed
section 7 says amendments are appended below an "## Amendments" heading
in the filed file. The team lead's note says to preserve what was
submitted, and to provide a new document with updates if asked to
submit again.

**Why it matters.** Text written into a filed copy changes the bytes
that were submitted. Text kept apart from it leaves the submitted text
whole and gives the next submission its source.

**Kind per option.**
- Option 1: Prevention. Neither filed copy is ever edited.
- Option 2: Prevention for the submitted copy only; the working copy
  changes.
- Option 3: Workaround. It follows the filed section 7 wording, and
  changes the submitted copy's bytes.

**Cost per option.** Zero metered seconds in every option.
- Option 1: about 15 minutes; 2 files (the new file, the drift guard).
- Option 2: about 20 minutes; 2 files (the draft, the drift guard: its
  byte-identical term becomes "the draft above the heading equals
  FINAL").
- Option 3: about 15 minutes; 3 files (both copies, the drift guard).

**Recommendation: 1.** It does exactly what the note asks: the submitted
text stays byte for byte, and every later change is in one dated file
that a new submission is built from. Its first entry records that it
departs from section 7's "appended below that heading" wording, and why.

**Options.**

1. A new file, `experiments/phase2/PREREGISTRATION_AMENDMENTS.md`. Each
   entry is dated and names the filed section it changes or adds to.
   `PREREGISTRATION_DRAFT.md` and `PREREGISTRATION_FINAL.md` are not
   edited. A new submission, if asked for, is built from the two then.
2. An "## Amendments" heading appended to `PREREGISTRATION_DRAFT.md`
   only, with every later change below it. `PREREGISTRATION_FINAL.md`
   is not edited.
3. An "## Amendments" heading appended to both copies, with every later
   change below it in both (the filed section 7 wording).

## D3. Lock the filed text now, before the venue is known?

Asked 2026-11-21 at planning (Phase 3), beside D2. Its option 1 is
written for each D2 answer.

**What.** F102's lock step: a tag, a hash test
(`experiments/src/test_phase2_prereg_filed.py`) with a proof that an
edited copy fails, and the document-of-record hook
(`.claude/hooks/block_reactive_amendment.py`) extended to the Phase 2
copies. The filed section 7 says the lock runs after the venue is
recorded, so the venue line is inside the locked text. The venue is
not known (Q1).

**Why it matters.** Until the lock, only the drift guard protects the
text, and it allows edits that add a revision-log row. The hash test
is the only check that fails on any edit. Locking now leaves the venue
line reading "not set" in the locked text; the venue is then recorded
outside it.

**Kind per option.**
- Option 1: Prevention.
- Option 2: Workaround (waits for a fact that may come late).

**Cost per option.** Zero metered seconds.
- Option 1: about 60 minutes; about 5 files (the test, the hook, its
  test, the drift guard, CHANGELOG) and one tag.
- Option 2: 0 minutes now; about 60 when the venue is known.

**Recommendation: 1.** The note asks to preserve the submitted text; a
hash test is what makes that hold. The venue is a fact about the filing,
not part of the text sent, so recording it outside the hashed text loses
nothing.

**Options.**

1. Lock now. The tag `phase2-prereg-filed` at the commit Q2 names (if
   Q2 is 4, at c3d3c00, with the reason in the tag message). The hook
   blocks edits to both copies. What the hash test covers, by D2 answer:
   - D2 option 1: both copies, every byte.
   - D2 option 2: FINAL every byte; the draft's text above its heading.
   - D2 option 3: both copies' text above the heading.
   The venue, when known, is a dated entry where D2 puts later text.
2. Hold the lock until the venue is known. F102 is not worked this
   sprint; the drift guard stays the only protection.

## D4. Which part of F157 is worked this sprint?

Asked 2026-11-21 at planning (Phase 3).

**What.** F157 is an epic. Its classical and proxy lanes are done on
ULB, IEEE-CIS and SPECTRA. What remains is the device lanes (CVQBoost
on Dirac-3S) and QSVM. Its card says to split it into one card per
dataset at refinement, and every device lane needs per-block approval
(Criterion H). `experiments/phase2/src/dirac3_emulator.py` runs a real
`QSVMClassifier` fit against a fitted model of the device, spending
nothing; its runtime on ULB is not measured.

**Why it matters.** The sprint is already about 5 hours without F157,
against a 1-2 hour target. A scored lane needs a complete entry before
its first result (filed commitment 3) and must run after F201.

**Kind per option.**
- Option 1: planned work (splits the epic into cards that can be
  selected).
- Option 2: planned work, plus one result.
- Option 3: none (de-scoped).

**Cost per option.** Zero metered seconds in every option.
- Option 1: about 45 minutes; 1 file (the master plan).
- Option 2: about 150 minutes [no-history]: option 1, a 5-minute
  emulator spike, an entry, the run and one page. Runtime not sized
  until the spike. About 5 files.
- Option 3: 0 minutes.

**Recommendation: 1.** The card asks for the split first, the device
lanes cannot run without approvals, and option 2's runtime is unsized.
The split gives each remaining lane a quoted cost (from
`qpu_cost_model.quote`), so a later sprint can select one.

**Options.**

1. Split only: one card per remaining lane and dataset (Dirac-3S
   CVQBoost on ULB, IEEE-CIS and SPECTRA; QSVM on the emulator; QSVM on
   Dirac-3S), each with its estimate, metered-second quote and entry
   needs. No result this sprint.
2. Option 1, plus QSVM on ULB on the emulator: a 5-minute spike first,
   then an entry where D2 puts it, then the run after F201, then
   `docs/phase2/algorithms/ULB_QSVM_EMULATED.md`.
3. F157 not worked this sprint.

## Answers to Q2, D2, D3 and D4 (team lead, 2026-11-22)

Verbatim:

> q2. have not been accepted into phase 2 yet. We may have more time to
> fill out the pre-registration. Please keep a permanent link and n
> unchangeable copy for the one I said I sent on 11/18/2026 9:01am EST.
> Agree - neither as filed copy (phase 1 and phase 2) should ever be
> changed. Keep track of amendments for what we do later.
> d2. If it is already clear how this should happen, do it as best
> possible with the information we have. Otherwise, A document similar
> to what we did in phase 1 where we locked in what we were going to do
> in phase 1, then wrote amendments as we went along. We may never have
> to submit it and do not need to worry about a length. Is that
> possible? Please propose how for my review. This seems to make the
> most sense: option 1.
> d3. 1
> d4. 1
> Do all of these: [Tasks A-I as planned]

**How Q2 is applied (inference, stated so it can be checked).** The
text sent at 9:01am EST on 2026-11-18 is taken to be commit b8e2c0e
(08:54:50 -0500), the last commit before 9:01; the next, c3d3c00, is
09:18:27. The reflog shows no other commit between them. Text edited
but not committed before 9:01 would not be in b8e2c0e; nothing records
such an edit.
- At b8e2c0e, `PREREGISTRATION_FINAL.md` and `PREREGISTRATION_DRAFT.md`
  are byte-identical (SHA-256 3d09845d...).
- **The current FINAL file is not the text sent.** c3d3c00 added
  section 7's lock wording from the PR #122 review and two revision-log
  rows after 9:01.
- So, and without editing either existing copy: the sent bytes are
  kept as a third file, `experiments/phase2/PREREGISTRATION_SUBMITTED_2026-11-18.md`,
  restored from b8e2c0e; the tag `phase2-prereg-filed` points at
  b8e2c0e, which gives the permanent link; the hash test locks all
  three files as they are now. The amendments file's first entries
  record which file is the sent text and why FINAL differs.

**Changed since asked (2026-11-22).** D3 option 1 named "both copies";
Q2's answer adds the third, sent copy to the lock. D2 option 1 is
applied as the team lead's Phase 1 model asks: the filed text locked,
amendments written as the work goes, in one dated file.

## D5. How does "What we learned this sprint" join the learning documents?

Asked 2026-11-23 (team lead's request during Sprint 34 Phase 4, card
F209).

- **What**: each sprint will state, before Manual Validation, what it
  taught us about machine learning, quantum machine learning, quantum
  computing and fraud detection, in `SPRINT_n_SUMMARY.md`. The question
  is how that joins the three learning documents in `docs/learning/`,
  which the team lead proposed as a "Sprint N updates" section near the
  bottom.
- **Why it matters**: the documents are organized by topic, and every
  result already goes in under its topic each sprint (F178). Each
  document also already has a dated "Change list" (at the end in the
  plain-terms version, near the top in the other two). A second dated
  log beside it would hold the same sprint's facts twice per document,
  six times in all, at three reading levels; CLAUDE.md's rule is that a
  number has one owning file and the rest refer to it.
- **Options**:

1. One dated section, not two. Each document's "Change list" becomes
   "Sprint updates", at the end of the document. Each sprint's entry
   states, at that document's reader level, what was learned (two to
   five bullets, each linking to its topic section), then what changed
   in the document, and links to the sprint summary's "What we learned"
   section for the figures. Kind: Prevention (one log per document; the
   figures stay in one file). Cost: about 25 minutes once (move two
   lists to the end, rename the heading in three documents and in
   `test_learning_docs.py`'s check and in `SPRINT_CHECKLIST.md`), then
   about 10 minutes per sprint inside F178's update. Zero metered.
2. A new "Sprint N updates" section near the end of each document,
   beside the existing change list, which stays as it is. Kind:
   Workaround (does what was asked; two dated logs per document). Cost:
   about 10 minutes once, about 15 minutes per sprint. Zero metered.
3. No new section in the learning documents. The sprint summary holds
   "What we learned"; each change-list entry gains one link to it.
   Kind: Workaround (cheapest; a reader of the documents sees no
   learning summary, only a link). Cost: about 5 minutes per sprint.
   Zero metered.

- **Recommendation**: option 1. It gives the reader the per-sprint
  summary the team lead asked for, near the bottom, at their level, and
  keeps one dated log per document instead of two. Its one-time cost is
  the heading rename and the guard that checks it.

## Answers to Q3 and D5 (team lead, 2026-11-23)

Verbatim: "Didn't remember the dated "Change List" existed - nothing new
needed."

- **D5**: no new section and no change to the learning documents. Each
  document's existing dated change list stays the per-sprint record
  there. (Closest to option 3, without its added link.)
- **Q3**: not answered directly. The answer withdraws only the
  learning-document section, so the original request stands as read:
  card F209, run this sprint as Task J before Manual Validation, its
  section in `SPRINT_34_SUMMARY.md`, and a step in
  `docs/SPRINT_CHECKLIST.md` Phase 5.

## Answers to Q3 and D5 (team lead, 2026-11-23)

Verbatim: "Didn't remember the dated "Change List" existed - nothing new
needed." Then: "no F209 is not needed as it, essentially, already
existss".

- **D5**: no new section and no change to the learning documents. Each
  document's existing dated change list stays the per-sprint record.
- **Q3**: no card F209 and no Task J. F178's per-sprint update of the
  learning documents, with its dated change lists, already does this.

## Q4. Scope of the change-list rewrite

Asked 2026-11-23. The team lead's feedback on the learning documents'
change lists (verbatim): "they are not detailed enough. The changes
should not reference backlog items or sprints by themselves, but what
the feature was doing (sentence or paragraph), it would still be
helpful to mention the feature name and/or sprint # in the text from
reader cross-reference ease. None of these are sufficient".

As read: every change-list entry in the three documents in
`docs/learning/` (plain terms 1.0 to 1.6; machine learning expert and
quantum computing expert 1.0 to 1.5) is rewritten so it says, in a
sentence or a paragraph at that document's reader level, what the work
did and what it found or changed. A card or sprint number appears only
beside that text, for cross-reference. Sprint 34's new entry is written
the same way. The rule goes into `docs/SPRINT_CHECKLIST.md`'s F178
step so later sprints follow it. All of it is done in Task I this
sprint (estimate raised from its plan figure by about 45 minutes; zero
metered).

1. Yes, as read
2. No

**Answer (team lead, 2026-11-23)**: "1". Yes, as read.

## D6. When does Experiment 5b run?

Asked 2026-11-23, at Manual Validation (Sprint 34 Task G, F197).

- **What**: Experiment 5b's entry (amendment P2-A3,
  `experiments/phase2/PREREGISTRATION_AMENDMENTS.md`) was committed
  before any score under its measure, and its saturation check (P2-A5)
  shows the new measure, average precision within each ProductCD
  segment, has room on every segment. The plan said "no run": the run
  waits for the team lead's approval of the entry. The run needs a new
  module (the Experiment 5 router with the new measure, its per-term
  tests and proofs) and then reads stored scores only.
- **Why it matters**: Experiment 5 found no segment worth routing to
  the proxy, but its measure was at its maximum for the champion on
  four of five segments, so it could not have found one there. Until
  5b runs, "routing does not help" rests on a measure that could not
  show help. Each option below costs zero metered seconds.
- **Options**:

1. Approve the entry as written, and build and run Experiment 5b in
   Sprint 35 as F197's remaining part. Kind: Prevention (the question
   is answered with a measure that can show a difference). Cost: about
   75 minutes in Sprint 35 (module, tests and proofs about 60, run
   under 10, document about 10); zero metered; about 4 files.
2. Approve the entry as written, and build and run it now, in Sprint
   34, before the retrospective. Kind: Prevention. Cost: the same
   about 75 minutes, added to a sprint already past its 1-2 hour
   target; zero metered; about 4 files.
3. Do not run it; F197 closes with the saturation check, and Experiment
   5's null stands with its saturation note. Kind: Workaround (the
   question stays open). Cost: about 5 minutes (the card closed with
   a note).

- **Recommendation**: option 1. The entry is committed and its check
  passed, so nothing is lost by waiting a sprint, and Sprint 34 is
  already past its time target. Option 2 is the same work sooner, at
  the cost of a longer sprint.

## D7. Protect the filing tags on GitHub itself?

Asked 2026-11-23, at Manual Validation (from the PR #134 review).

- **What**: the tags `phase2-prereg-filed` (b8e2c0e, the Phase 2
  preregistration as sent, your permanent link) and `prereg-freeze`
  (95751b9, cited in Phase 1's filed Appendix B) are guarded only by
  this repository's local Claude Code hook. GitHub has no ruleset on
  the repository (`gh api repos/kimmeyh/hsbc-qfraud-phase2/rulesets`
  returns none), so a push from any other client, or a session without
  the hook, could move or delete either tag. The review also found four
  command shapes the hook missed; they are now blocked and tested.
- **Why it matters**: the permanent link is the thing you asked to keep
  unchangeable. A local hook protects against this session's mistakes,
  not against every path to the remote.
- **Options**:

1. I add a GitHub tag ruleset now with `gh api`: target tags
   `refs/tags/phase2-prereg-filed` and `refs/tags/prereg-freeze`,
   rules "restrict deletions" and "restrict updates", enforcement
   active, no bypass. Then I verify by reading the ruleset back. Kind:
   Prevention (the remote refuses the change, whatever the client).
   Cost: about 10 minutes; one repository setting, visible on the
   public repository; zero metered.
2. You add the same ruleset yourself in GitHub (Settings, Rules,
   Rulesets, New tag ruleset). Kind: Prevention. Cost: about 10 minutes
   of your time.
3. Keep the local hook only. Kind: Workaround. Cost: none now.

- **Recommendation**: option 1. It closes the gap at the remote, where
  every client meets it, and it is a setting you can remove later.
