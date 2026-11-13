# Sprint 32 Retrospective: Claude Code Development Team draft

Written 2026-11-13 while the Phase 6 reviews ran. Copied into
`docs/sprints/SPRINT_32_RETROSPECTIVE.md` at step 3.

1. **Effective while as Efficient as Reasonably Possible**: Good. All
   seven tasks met their acceptance criteria with zero metered seconds,
   and both results answer the question their card asked. Rework: two CI
   reds (5027f4f, c692eac) and one vacuous red proof (fixed in bcf67ad),
   each found by CI, not by me before the push. The fresh-eyes review
   caught three wrong claims in the F188 document before handover.
2. **Testing Approach**: Good. Every new rule has its own test and red
   proof, and `assert_can_fail` caught the vacuous proof as designed.
   But the local check the checklist names for a task
   (`scripts/select_proofs.py --tests --base HEAD`) was skipped in Tasks B
   and C, so two failures reached CI that it would have caught. The
   parallel Phase 5 suite ran out of memory on this machine (9 files);
   the serial rerun of the same files passed.
3. **Effort Accuracy**: Good. 150 recorded active minutes against 210
   estimated. B (37 of 45) and E (36 of 30) were close. C ran over (47 of
   30) because of the amendment's second reading; D ran under (24 of 60)
   and overlapped C. A's 1 minute is wrong: the timer did not start
   (`--start-task A --estimate 15` with the estimate already set). F's 3
   and G's 2 minutes leave out reading time spent before each timer
   started.
4. **Planning Quality**: Very Good. Each task had a "show it can fire"
   line before it ran, and both checks fired first. D3's ordering (E
   after every other step, then F and G) worked as written.
5. **Model Assignments**: Very Good. The main loop did all tasks; one
   fresh-eyes reviewer found 23 observations, three of them material.
6. **Communication**: Good. The handover listed only actions, with full
   paths, and D4 was written to the file before it was asked. One gap:
   commit 3520a0f's message names only Task D but carries Task C's
   document too.
7. **Requirements Clarity**: Very Good. D2's "after this sprint" had two
   readings; D3 asked which, and the answer added Task G.
8. **Documentation**: Very Good. Both result documents state what was
   registered and what came after it, and the F188 amendment is dated
   and logged in the preregistration draft. The learning documents carry
   both results with sources the tests check.
9. **Process Issues**: Good. Three tooling frictions: the timer flag
   above; a CHANGELOG hook block left Task C's files staged, and they
   went into Task D's commit; `test_no_proofs_under_xdist.py` runs near
   its 300 s limit under load.
10. **Risk Management**: Very Good. The F188 reading that could have
    closed F25 was not used to close it: the registered rule said
    "open", and D4 left the call to the team lead. F185's document
    states its unverified unit and its dependence on calibration.
11. **Next Sprint Readiness**: Very Good. F198 is carded from D4; no
    Sprint 33 run is preregistered yet, and the learning documents say
    so.
12. **Architecture Maintenance**: Very Good. Both new modules use
    `provenance.start` and `write_result`, carry outcome blocks, and
    declare `LONG_RUN` (after the CI red). The frozen preregistration was
    not touched.
13. **Minor Function Updates for the Next Sprint Plan**: [Claude] fix
    `update_sprint_status.py` so `--start-task X --estimate N` starts the
    timer when an estimate is already set -- target: Sprint 33 plan,
    est: 15m (proposed as a retrospective item instead, if taken now).
14. **Function Updates for the Future Backlog**: [Claude] F198, carded
    at D4 -- estimated: 30m, priority: 10, depends on: nothing.
15. **Assigned Coding Agents Quality**: Very Good. The fresh-eyes
    reviewer's three material findings were all real and all fixed; no
    finding needed rework.
16. **Questions to be discussed before ending the sprint**: none.
