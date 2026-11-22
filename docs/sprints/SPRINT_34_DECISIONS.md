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
