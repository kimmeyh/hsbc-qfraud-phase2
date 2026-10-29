# Sprint 29 Retrospective, Claude Code Development Team draft

Drafted 2026-10-28 while the PR #63 reviews ran (protocol step 2). The
review findings are added in step 5, in `SPRINT_29_RETROSPECTIVE.md`.

### 1. Effective while as Efficient as Reasonably Possible
Good. All nine tasks met their acceptance with zero metered seconds, and
four of the five experiments gave a decisive reading (F156 fails, F158's
cascade is below, F160 passes, F166 ranks two pairs). The largest loss
was F159's resume, which hung for 9 hours (12:10am to 8:58am) with no
in-process time limit; fixed in 94f079e with a 2-times-serial budget.
Phase 5 found six corrections in documents written this sprint (a14c644),
each before handover.

### 2. Testing Approach
Good. Every new guard was proven red with `assert_can_fail`. The Phase 5
gate from Sprint 28 IMP-5 (one test per term of a compound rule) worked:
it found two compound rules shipped without a per-term test, F158's step
2 condition and F166's parallel gate `complete` term (92d89b6, a14c644).
It found them at Phase 5, not when the rules were written, so the rule
is applied late.

### 3. Effort Accuracy
Poor, as a measurement. Actual over estimate, minutes: A 2042/60, B
622/60, C none/270, D 2647/90, E 53/75, F 158/240, G 6/150, H 2036/60,
I 17/45. A, H, D and B ran across the overnight break or the F159 hang;
C's timer was never started; E and G started only when their runs began.
Only F and I are as measured, both under estimate (0.66, 0.38). Same
class as Sprint 28 (K and H read 1 minute; D4 had no timer).

### 4. Planning Quality
Very Good. Decisions 1-3 were settled before execution and each entry
was committed before its first score. Decision 3's seed rule set F166's
seeds from a measured time, and gave 10.

### 5. Model Assignments
Very Good. The main loop kept every run and decision; the review agents
work on the draft PR with the evidence files excluded.

### 6. Communication
Good. One status footer was typed by hand and caught by the Stop hook
(the real time was 9:20am, not the typed 9:31am). The F159 hang mechanism
was reported as inferred, not shown, after a first draft stated it as
shown.

### 7. Requirements Clarity
Very Good. The plan's "both venvs" for Task I named a second venv that
does not exist on this machine; reported, not assumed.

### 8. Documentation
Good. F164 now checks each Phase 2 figure against its own document's
results, and caught two older documents. Integers and prose stay outside
it: the CHANGELOG count 18 (for 17) was found by reading, not by a check.

### 9. Process Issues
Good. The F159 hang ran 9 hours unseen because nothing checked the run's
heartbeat while the session was idle overnight; F168 (Sprint 30) covers
a recurring wake-up that would see it. Hooks worked as designed: a typed
footer and `${...}` in a Python command were each blocked.

### 10. Risk Management
Very Good. Zero metered seconds. The `MemoryError` at 32 workers was
recorded as unverified in cause, not called out of memory.

### 11. Next Sprint Readiness
Very Good. F168 is assigned to Sprint 30; F169-F171 are carded from
Manual Validation with their dependencies.

### 12. Architecture Maintenance
Very Good. `provenance.run_id_for` gives a resumed run one id, used for
real by F159; shared `experiments/src` code kept Phase 1 behavior as the
default.

### 13. Minor Function Updates for the Next Sprint Plan
None beyond the improvements below.

### 14. Function Updates for the Future Backlog
F169, F170 and F171, carded at Manual Validation.

### 15. Assigned Coding Agents Quality
No issues -- expectations met. No coding agents were assigned this
sprint; the review agents are scored in step 5.

### 16. Questions to be discussed before ending the sprint
none
