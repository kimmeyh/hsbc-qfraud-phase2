# Sprint 29 Decisions

Every decision or question asked of the team lead in this sprint, in full,
as first asked. A question asked again is pasted from here unchanged: same
ID, same wording, same option numbers. If facts change after it is asked, a
dated "Changed since asked" note goes below the original; the original is
never edited. The answer is recorded under each entry.

From 2026-10-30 (team lead, Sprint 29). D1 was asked before this file
existed; its full text is in `SPRINT_29_VALIDATION.md`, Decision.

---

## D1. F156 failed, so F114 has no validated estimator. What next?

Asked 2026-10-28 at Manual Validation. Full text in
`docs/sprints/SPRINT_29_VALIDATION.md`, Decision.

**Answer (team lead, 2026-10-28): 2.** F169 carded.

---

## D2. How should IMP-1 to IMP-5 be disposed?

Asked 2026-10-29 (retrospective step 6); re-asked 2026-10-30 in this
format.

**What.** The retrospective proposes five improvements, from the classes
of defect this sprint's review found. Each one can be applied now, as a
commit on this branch before `gh pr ready`, or carded to the backlog.

- **IMP-1.** A rule's per-term tests land in the commit that adds the
  rule. The Sprint 28 IMP-5 gate moves from Phase 5 to Phase 4 in
  `docs/SPRINT_CHECKLIST.md`.
  - Why it matters: 10 compound-rule terms had no test after their commit
    (2 found at Phase 5, 8 at review), and the same class was found in
    Sprint 28. An untested term can decide a result wrongly and still
    pass.
  - Kind: Prevention.
  - Cost: about 15 minutes; 0 metered seconds; `docs/SPRINT_CHECKLIST.md`,
    `docs/SPRINT_PLANNING.md`.
- **IMP-2.** The script that writes F166's eight result pages moves from
  the session scratchpad into `scripts/`, and the pages' standard text is
  computed from the result file.
  - Why it matters: the script is lost when the session ends, so the
    pages cannot be regenerated or reviewed. The review found a claim in
    that standard text that the result does not support.
  - Kind: Prevention.
  - Cost: about 60 minutes; 0 metered seconds; a new script in
    `scripts/`, its test, and the eight pages in `docs/phase2/algorithms/`.
- **IMP-3.** `budget_s` becomes a required argument of the public parallel
  build.
  - Why it matters: the time limit added after the 9-hour F159 hang was
    applied at F159's call site only. F166 called the build without it,
    so a second hang of the same kind was possible.
  - Kind: Prevention.
  - Cost: about 20 minutes; 0 metered seconds;
    `experiments/phase2/src/f159_parallel_pool.py`,
    `experiments/phase2/src/f166_ulb_algorithms.py` and their tests.
- **IMP-4.** The commit-msg hook refuses a feat or fix commit for a task
  whose timer is not running.
  - Why it matters: effort accuracy is unmeasured for two sprints running
    (Task C had no timer; E and G started late; four timers ran
    overnight). Future estimates rest on these actuals.
  - Kind: Prevention.
  - Cost: about 30 minutes; 0 metered seconds;
    `scripts/check_commit_issue.py` and its test.
- **IMP-5.** Tests for the review's coverage items not fixed: F166's
  validation and training label checks, the "below" branch, the
  `svm_form` majority rule and `t42_min <= 0`; F156's `summarize` pass
  term and single-class refusal; F160's SCIP minimum; F159's MemoryError
  path end to end and the KeyError in `test_the_budget_can_fail`; each
  module's resume loop.
  - Why it matters: each makes a branch fail visibly. None changes a
    recorded result.
  - Kind: Workaround (detection for this code only; prevents no new
    defect).
  - Cost: about 90 minutes; 0 metered seconds; the test files of F156,
    F159, F160 and F166.

**Recommendation: 1.** It applies all four preventions now, at 125
minutes. IMP-5 goes to the backlog: it is detection only, it changes no
recorded result, and it is the largest cost.

**Options.**

1. As recommended: IMP-1, IMP-2, IMP-3 and IMP-4 now, as commits on this
   branch (about 125 minutes); IMP-5 to the backlog as a new card, F172,
   priority 40.
2. All five now (about 215 minutes).
3. IMP-1 and IMP-3 now (about 35 minutes); IMP-2, IMP-4 and IMP-5 to the
   backlog as F172-F174, priority 40.
4. All five to the backlog as F172-F176, priority 40; nothing applied now.

**Answer:** pending.
