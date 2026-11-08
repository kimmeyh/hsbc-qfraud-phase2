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
