# Sprint 32 Decisions

Every decision or question asked of the team lead in this sprint, in full,
as first asked. A question asked again is pasted from here unchanged: same
ID, same wording, same option numbers. If facts change after it is asked, a
dated "Changed since asked" note goes below the original; the original is
never edited. The answer is recorded under each entry.

---

## D1. Which cards make up Sprint 32?

Asked 2026-11-08 at backlog refinement Pass 2 (Phase 8.4).

**What.** Sprint 32's scope, from the 2026-11-08 slate in
`docs/ALL_SPRINTS_MASTER_PLAN.md`.

**Why it matters.**
- The time target is 1-2 hours a sprint, all testing included (team
  lead). Sprint 31 took 2,613 active minutes against 1,614 estimated, a
  ratio of 1.62 over its 13 estimated tasks. Single tasks ran from 0.04
  to 4.75. A sprint near the target holds about 75 minutes of card
  estimates.
- F188 decides something for 30 minutes. F176 found selections below
  greedy on IEEE-CIS by under 2e-05. If those gains do not survive the
  device's 200:1 resolution, no device run on F25's IEEE-CIS design can
  show a result, and F25's HOLD can become a close.
- F181 makes the team lead's Sprint 31 D5 rule ("this and all future
  runs will be on the Dirace-3S") a check, not only a written rule. No
  module breaks it today.
- F178's update is a standing Phase 5 step (`SPRINT_CHECKLIST.md`). It
  runs in every sprint, so it is counted in every option.
- F185 is the first card that states results in dollars, the measure a
  bank uses. It is 60 minutes and takes the sprint past the target.
- F194 closes the line-coverage gap that Sprint 31's short review found
  in the refusal gate. No occurrence is known.

**Cards.** Minutes are card estimates, all `[no-history]`; 0 metered
seconds in every card. Calibrated minutes use Sprint 31's ratio of 1.62
and are estimates, unverified. Phase 3 planning, the reviews and the
retrospective are not in these figures.
- F188, the rounding test on the IEEE-CIS selection instances: 30m;
  about 4 files (a module, its test, a result file, a document).
  Research.
- F181, the device-default guard enforces Dirac-3S only: 15m; 1 file
  (`test_phase2_device_default.py`). Prevention.
- F178, the per-sprint learning-document update: 30m; 3 files (the
  three documents in `docs/learning/`). A deliverable.
- F185, a cost-weighted alert budget: 60m; about 4 files. Research.
- F194, the refusal gate measures branches and reads every print
  prefix: 45m; about 4 files (`.coveragerc`, `refusal_coverage.py`, its
  test, `ci.yml`). Prevention.

**Kind per option.** Every option carries F181, a Prevention. Option 3
adds F194, a second Prevention. No option carries a Workaround.

**Cost per option.**
- Option 1: 75 minutes by card, about 120 calibrated; 0 metered
  seconds; about 8 files.
- Option 2: 135 minutes by card, about 220 calibrated; 0 metered
  seconds; about 12 files.
- Option 3: 120 minutes by card, about 195 calibrated; 0 metered
  seconds; about 12 files.

**Recommendation: 1.** It is the only option inside the 1-2 hour
target at Sprint 31's ratio. F188 is the cheapest card that can close a
question: it decides whether F25 on IEEE-CIS still has a device case.
F181 enforces a rule the team lead has already set, for 15 minutes.
F185 and F194 lead the next slate (priorities 18 and 26).

**Options.**

1. F188, F181 and the F178 update (75 minutes by card).
2. F188, F181, the F178 update and F185 (135 minutes by card).
3. F188, F181, the F178 update and F194 (120 minutes by card).

**Answer (team lead, 2026-11-08): a different set, all five cards.**
Verbatim: "d1. do these:", followed by the five card lines of the
terminal summary pasted unchanged (F188 30m, F181 15m, F178 30m, F185
60m, F194 45m). Sprint 32 is F188, F181, F185, F194 and the F178 update:
195 minutes by card with the F150 request update below (180 plus 15),
about 315 calibrated at 1.62; 0 metered seconds. This is past the 1-2
hour target; the team lead chose it with F185's line saying so. Order
from D2's answer: F178 runs after every other step, and the F150 request
update after F178.

---

## D2. F150: was the construction request to the SPECTRA authors sent?

Asked 2026-11-08 at backlog refinement Pass 2 (Phase 8.4). This is
Sprint 31 D4, asked again as that answer said ("D4 delay to next
sprint"). Its wording and option numbers are D4's, unchanged.

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

Note (2026-11-08): option 3's "leaves Sprint 31" is D4's wording, kept
unchanged. Today it means F150 is not in Sprint 32 and stays blocked.

**Answer (team lead, 2026-11-08): 3, with an instruction.** Verbatim: "d2
3 please update the request after this sprint (after F178 completes and
F178 should not be done until all the other steps complete)". Read as:
the request was not sent and is not sent now; F150's rebuild stays
blocked. The draft
(`docs/spectra_package/F150_CONSTRUCTION_REQUEST_DRAFT.md`, gitignored)
is updated as Sprint 32's last task, after F178, with this sprint's
results; it is not sent. F178 runs after every other task and step that
can change a result. If "after this sprint" meant Sprint 33, the plan
approval (D3) offers that.

---

## D3. Is the Sprint 32 plan approved, and when do F178 and the F150 update run?

Asked 2026-11-08 at Phase 3 planning (3.7).

**What.** Approval of `docs/sprints/SPRINT_32_PLAN.md`: tasks A (F181),
B (F194), C (F188), D (F185), E (F178) and F (the F150 request update),
195 minutes by card, 0 metered seconds. The options differ only in when
E and F run, because D2's answer can be read two ways: "after this
sprint" (Sprint 33), or "after F178 completes" (the end of Sprint 32).

**Why it matters.**
- The checklist runs F178 in Phase 5, before Manual Validation, so the
  team lead reviews it there. D2 says F178 waits until "all the other
  steps complete". Phase 5's suite and fresh-eyes fixes are the last
  steps that can change a result before Manual Validation; the Phase 6
  PR review fixes can also change one, rarely.
- The F150 update needs only the sprint's results. Done in Sprint 32,
  the team lead sees it at Manual Validation (option 1) or with the
  ready PR (option 2). In Sprint 33 it is a card there.

**Kind.** Scope and order; no option is Prevention or Workaround.

**Cost per option.** 195 minutes by card in options 1 and 2; 180 in
option 3 (the F150 update, 15 minutes, moves to Sprint 33). 0 metered
seconds in each. Files: about 15, the same in each.

**Recommendation: 1.** F178 then records every result the sprint
produces, and the team lead reviews it and the request draft at Manual
Validation, as the checklist intends. Option 2 leaves both unreviewed
until the PR is ready. Option 3 is right only if "after this sprint"
meant Sprint 33.

**Options.**

1. Approve the plan as written: E (F178) after Phase 5's suite and
   fresh-eyes fixes, then F (the F150 update), both before the Manual
   Validation handover.
2. Approve with E and F moved after the retrospective (Phase 7), before
   the PR is marked ready; neither is in Manual Validation.
3. Approve with E as in option 1, and F removed from Sprint 32: the
   F150 update becomes a Sprint 33 candidate on F150's card.

**Answer (team lead, 2026-11-08): approved as amended.** Verbatim:
"After task E, can you also update F111_feedback_draft.md |", followed by
the standing approval: "Sprint plan approved as amended (with any
comments I provided), proceed with execution. All Sprint tasks and
sub-tasks are approved. Do not stop between tasks as they are all
approved, please continue to complete all tasks and without addition
approvals until Manual Validation, providing your recommendation for
Manual Validation steps. Do not stop to ask questions unless meeting the
criteria in \docs\SPRINT_STOPPING_CRITERIA.md If questions must be
asked, ask as late as possible - do everything that can be done (all
tasks and parts of tasks, without the answer to the question(s), then
ask the question(s)". No option digit was given; the plan runs as
written (option 1's order), with one task added: G, the F111 feedback
draft (`docs/loke_package/F111_FEEDBACK_DRAFT.md`, gitignored) updated
after E with the results since 2026-10-23, not sent.

---

## D4. F25: close its IEEE-CIS design after F188, or keep it on HOLD?

Asked 2026-11-10 at the Manual Validation handover (Phase 5.3). F188's
document leaves this to the team lead
(`docs/phase2/F188_ROUNDING.md`, "What it means").

**What.** F188 rounded F176's six IEEE-CIS selection instances to the
device's 200:1 resolution. Its two readings disagree:
- The registered reading (gain measured on the rounded problem) is
  "kept" on 42/free and 43/free. By the entry, the device question
  stays open there. Those gains are 49 and 73 times F176's, made by the
  rounding.
- The amendment's reading (the rounded problem's pick and weights,
  scored on the real problem) is worse than greedy on all six at
  R = 200. On the three instances where F176 found a gain, the loss is
  larger than the gain. The amendment was written after the first
  reading and set no decision rule.

F25's card is on HOLD; its HOLD reason (F102, the Phase 2
preregistration, not filed) is unchanged by F188.

**Why it matters.** Closing F25 ends the one device experiment that
could show a solver difference on a non-convex problem; it reopens only
by a new card. Keeping it on HOLD costs nothing now, because F102 holds
it anyway. Three facts are untested: the 200:1 figure on Dirac-3S (it
is QCi's, from Dirac-3), other ridge weights (the step is set by the
same largest term on every instance, likely the ridge diagonal), and
R above 400 (at 400, 43/free delivers a small gain).

**Kind.**
- Option 1: neither; a scope decision.
- Option 2: Prevention. F188's check becomes a precondition on the card,
  so no device run on this or a similar formulation is proposed without
  it.
- Option 3: Prevention, as option 2, plus more evidence before any
  close.

**Cost per option.**
- Option 1: 5 minutes now, one file (`docs/ALL_SPRINTS_MASTER_PLAN.md`).
- Option 2: 5 minutes now, the same file.
- Option 3: 10 minutes now, the same file; the new card about 30
  classical minutes in a later sprint, zero metered seconds.

**Recommendation: 2.** The registered rule says "open", and the reading
that says "closed" came after it, with no rule. Two of the facts it
rests on (200:1 on Dirac-3S, the ridge weight) are untested. Option 2
keeps the card where F102 already holds it and makes F188's check a
condition of any device proposal, which is the Prevention. Option 1 is
not chosen because it closes on an unregistered reading. Option 3 is
not chosen now because the card is held by F102 regardless; F198 can be
carded when F102 is filed.

**Options.**

1. Close F25. Its card in `docs/ALL_SPRINTS_MASTER_PLAN.md` gets
   "Closed 2026-11-10 (Sprint 32 D4): F188 found that at 200:1 the
   rounded problem's answer, scored on the real problem, is worse than
   greedy on all six IEEE-CIS instances", and moves to the completed
   record. It reopens only by a new card.
2. Keep F25 on HOLD. Its card gets a "Sprint 32 (F188)" line with both
   readings, and its "Depends on" adds: "before any device run on this
   formulation, F188's delivered reading (the rounded problem's pick,
   scored on the real problem) must beat greedy at R = 200".
3. Option 2, plus a new card, F198, priority 10: F188's two readings on
   the same six instances with F176's ridge multiplier at 0.1, 1 and 10
   times its recorded value, and R = 800 and 1,600; zero metered
   seconds; about 30 minutes.

**Answer (team lead, 2026-11-13): 3.** Verbatim: "d4 3". F25 stays on
HOLD; its card gets a "Sprint 32 (F188)" line with both readings and the
F188 condition in "Depends on"; F198 is carded at priority 10 as option
3 states.

**Changed since asked (2026-11-17, Sprint 33 D6).** An outside review
found that at R = 200 the rounded problem's pick is greedy's own
selection on three of the six instances and still scores worse than
greedy, so "the delivered reading beats greedy" could not pass there.
The team lead chose Sprint 33 D6 option 1: the condition now compares
the pick against greedy's selection solved the same way (on the rounded
problem, scored on the real one), with a gain of more than 1e-6 on at
least one of the six instances at R = 200. Other ridge weights,
resolutions or datasets (F198) each need a dated amendment before their
run. The answer above is unchanged.
