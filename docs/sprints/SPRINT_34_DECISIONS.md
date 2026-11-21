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
