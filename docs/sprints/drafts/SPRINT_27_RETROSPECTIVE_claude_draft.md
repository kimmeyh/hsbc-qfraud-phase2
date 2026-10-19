# Sprint 27 Retrospective: Claude Code Development Team draft

Written 2026-10-19, while the team lead's feedback was collected. The
final record is `docs/sprints/SPRINT_27_RETROSPECTIVE.md`.

1. **Effective while as Efficient as Reasonably Possible**: Good. All 12
   tasks met their acceptance with zero metered seconds. Rework: F107's
   first run refused because F107 carried its own copy of F106's
   evaluation chunk size (4,096 against 8,192) and had to run again; the
   code review's F108 and F104 fixes arrived after those runs (no
   recorded result changed); and a CRLF rewrite of `f130_levers.py`
   cost one failed injection.
2. **Testing Approach**: Good. Every new guard was proven red with
   `assert_can_fail`, and two refusals fired as designed (F107's
   exact-AUPRC check, F106's projected-runtime rule). Two scripts
   shipped without a test: F112's, found by the code review, and
   `f102_downsized_pair.py`, found only at this retrospective. Nothing
   requires a new Phase 2 script to have a test.
3. **Effort Accuracy**: Poor. 10 of 12 tasks ran with another task's
   timer open. 6 of 12 actuals are stamp gaps (A 8, B 9, C 5, H 8, K 12,
   L 3 minutes against 45-180 estimated), and 3 more (E, G, I) are
   elapsed background-run time, not work. All 12 timers started
   within 71 minutes. Sprint 26 IMP-2 now records the overlap, which is
   why the velocity rows can say so, but it did not prevent it. I, not
   the tool, chose to start timers in a batch.
4. **Planning Quality**: Very Good. Plan verification corrected six cards
   before they ran. F106's pilot rule cut its steps from 1,500 to 750
   before the full run. One miss: F107's "critical rank per shot budget"
   is undefined for classical inputs, found at task start, not at plan
   verification; the change was recorded before the run.
5. **Model Assignments**: Very Good. Main loop for the experiments and
   write-ups, long runs in the background, a code reviewer and a
   fresh-eyes reviewer with no sprint context.
6. **Communication**: Very Good. Decisions were numbered lists; the
   validation items and the 14 QCi questions were listed to the screen.
   Two small misses: a velocity note claimed something I could not
   verify (replaced before commit), and commit messages did not cite
   issue numbers (the CHANGELOG lines name the task).
7. **Requirements Clarity**: Very Good. D4 was not answered and option 1
   applied, recorded as such.
8. **Documentation**: Very Good. Every result names its file; readings
   added after a run (F108's main arm, F107's acceptance) carry dated
   notes saying so. The F109 card was retitled at the acceptance walk to
   match what ran.
9. **Process Issues**: Good. Python `write_text` turned a source file into
   CRLF on Windows, which broke an injection target. `scripts/edb_query.py`
   crashed on a cp1252 console (workaround `PYTHONIOENCODING=utf-8`). The
   heredoc-escape hook blocked two edits and named the right route.
   `score_gates.py` writes the Phase 1 record on any invocation; I did not
   run it, and `test_evidence_immutability.py` would catch a write after
   the fact.
10. **Risk Management**: Very Good. Zero metered seconds, as planned.
    F106's 3-hour limit and F107's exact-match refusal both fired before a
    wrong result was recorded.
11. **Next Sprint Readiness**: Very Good. The QCi questions are sent; F150
    waits on the authors. One open finding: the ULB HGB comparator is
    unstable (mean 0.22-0.52 AUPRC across settings), cause unverified, and
    it voids any "beats HGB on ULB" reading until explained.
12. **Architecture Maintenance**: Very Good. `pair_count` is opt-in with
    the default pool unchanged and proven equal; all new evidence is under
    `experiments/phase2/results/`; the locked files are unchanged.
13. **Minor Function Updates for the Next Sprint Plan**: none beyond the
    improvements.
14. **Function Updates for the Future Backlog**: [DEV] ULB HGB comparator
    instability -- estimated: 1.5h, priority: 20, depends on: none (IMP-7).
15. **Assigned Coding Agents Quality**: Very Good. The code review found
    the F108 stopped-seed count and the F104 exit-code gap; the fresh-eyes
    review's 14 findings were each verified, then applied.
16. **Questions to be discussed before ending the sprint**: none.
