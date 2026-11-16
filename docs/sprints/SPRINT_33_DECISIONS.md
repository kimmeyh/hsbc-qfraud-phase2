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
