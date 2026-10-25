# Sprint 28 Retrospective, Claude Development Team draft

Written 2026-10-24 after the team lead's feedback arrived. The draft was put
on hold while the reviews and D4 ran (D5), so it was not written in parallel
as step 2 asks; the lines are the same ones recorded in
`docs/sprints/SPRINT_28_RETROSPECTIVE.md`.

1. Effective: Good. 13 tasks met acceptance, zero metered seconds. Rework: four reviews returned 46 findings, fixed in 28bdbcd, a78901b and f98ea2f; CI ran red on eight commits (39f9943 to f98ea2f, 3 h 41 min) from a docstring; one injection mutation in f111 launched the real experiment and was stopped.
2. Testing: Good. Every new guard proven red; but four reviewers found the outcome exempt list could grow, three compound rules had no test per term, and this retrospective found the same grow-able lists in test_device_store_required.py (39f9943).
3. Effort: Poor. 572 measured minutes against 1,120 estimated; K and H read 1 minute because their timers started at the commit; E and D are background wall clock; F111's runtime projection was about 10 times the recorded 82.5 minutes; D4 was never timed.
4. Planning: Very Good. Decisions 1-6 settled before execution; the "show each threshold can fire" rule existed and was applied to data, not to tests.
5. Model assignments: Very Good.
6. Communication: Good. D4 parts 1 and 2 and the F162 work were reported done while CI was red and unchecked.
7. Requirements: Very Good.
8. Documentation: Good. Seven review findings were document figures that the result files do not support.
9. Process: Good. CI red unnoticed; D4 had no issue and no timer; hooks blocked a heredoc, a typed footer and a commit without a CHANGELOG entry as designed; one agent stopped at the session limit.
10. Risk: Very Good. Zero metered seconds; the SPECTRA leak was traced to the label columns and this repository shown clean.
11. Next sprint readiness: Very Good.
12. Architecture: Good. device_store and provenance land before any Phase 2 device run; their frozen lists need the IMP-1 pin.
13. Minor: none beyond the improvements.
14. Backlog: IMP-6 and IMP-7 if approved as backlog.
15. Agents: Very Good. Review findings were specific and checkable; the backfill agent stopped at the session limit and finished after a resume.
16. Questions: none.
