# Sprint 33 Manual Validation

**Sprint**: 33
**Branch**: `feature/20261116_Sprint_33` | **PR**: #122 (draft)
**Scope**: F13 (A), F102 (B and D), F178 (C), the fresh-eyes review
fixes (E). Issues #123-#127, all closed.
**Metered seconds**: 0. No device, Braket or other paid service was
called.
**Sprint goal** (team lead): "have the Phase 2 registration document
ready to submit."

This file is the durable copy. The same items are listed to the screen at
handover: a pointer to a file is not a handover.

## Actions for the team lead

- **A1. Review the preregistration draft before filing.** Read these
  parts first: "Filing" and "How to read the identifiers" (top of the
  file); section 6's table (State and Result columns); the "State at
  filing" paragraph that opens each of Experiments 1-6; section 7; the
  last two revision-log rows.
  `D:\Data\Harold\github\hsbc-qfraud-phase2\experiments\phase2\PREREGISTRATION_DRAFT.md`
- **A2. Confirm or correct the assumptions the filing rests on**,
  A1-A12, in the "Assumption register" at the end of the PoC plan
  draft. Four of them are new and need your judgment most: A9 (venue and
  date not set), A10 (the team proceeds to the PoC), A11 (filed without
  the brief; changes by dated amendment) and A12 (the reader can open
  this repository; if not, the card and sprint numbers do not resolve).
  `D:\Data\Harold\github\hsbc-qfraud-phase2\docs\phase2\PHASE2_POC_PLAN_DRAFT.md`
- **A3. After any change you or a reviewer make to the draft**, add a
  revision-log row dated that day, then run the drift guard. Replace
  `<venv python>` with the interpreter `docs/ENVIRONMENT.md` gives:

  ```
  <venv python> -m pytest -p no:xdist -m "not proof" `
    experiments\src\test_phase2_prereg_draft.py
  ```

  A red result names the term that broke (a missing row or entry, a
  state outside Run / Partly run / To run, an untracked result file, a
  missing filing field, an uncited assumption, an open section 7 item,
  no new revision-log row, or an unresolved figure).
- **A4. When you file, tell me the filing date and venue.** I then fill
  the Filing section and do the lock step section 7 lists (a tag at the
  filing commit, a hash test and the document-of-record hook). Until
  then both fields say "not set", as you asked.
- **A5. Judge the learning documents' 2026-11-16 version.** No new result. Each
  "Experiments planned" section gains a Sprint 33 paragraph, and every
  F188 passage now gives your Sprint 32 D4 decision. Plain-terms
  version, sections 6 and 7:
  `D:\Data\Harold\github\hsbc-qfraud-phase2\docs\learning\ML QML and QC Understandings about Quantum Advantage - Laymen terms.md`

## Team lead's answers (2026-11-17)

- A1: an adversarial review of the draft, run by Fable, before the
  team lead's own review. The draft is still open: every word can
  change, and each change is accounted for (a revision-log row, the
  drift guard, and the PoC plan draft where the change touches it).
- A2: all twelve assumptions confirmed as written.
- A3, A4, A5: ok.
- Added: an outside machine learning expert's review of the plain-terms
  learning document, applied as its 2026-11-17 version (author and use
  of artificial intelligence tools, executive summary, insurance,
  which version to read, why SPECTRA). Decision D4 (one learning
  document or three) asked. The two expert versions are reviewed next.
- New fact: this repository and EvidenceBasedDB are public.

## For information (no action needed)

---

## V1. Task A (F13): the PoC plan's assumptions (2bb6393)

- Each assumption A1-A8 now gives its basis and what replaces it. A9-A12
  added. Sprint 32's results placed: F188 and D4 under Experiment 3,
  F185 under the metrics. The "before notification" list is closed with
  each item's outcome. A revision log added.

## V2. Task B (F102): the draft ready to file (07de0a7)

- A "Filing" section: date and venue not set; the assumptions cited;
  what filing commits to ("Run" entries are reported, not
  re-registered).
- An identifiers section. Assumptions are always written "assumption
  An", because bare "A" numbers name Phase 1 amendments.
- Section 6's table, dated 2026-11-16: 25 rows, each with a State and a
  Result. Experiments 3 and 6 are "Partly run"; every other row is
  "Run". No row is "To run".
- Section 7: only two filing steps stay open (date and venue; the lock).
- `outward_readability.py`: the remaining hits are the identifier
  classes the new section resolves. No other class was rewritten.

## V3. Task D (F102): the drift guard (8682ea7)

- `experiments/src/test_phase2_prereg_draft.py`: a consistency guard,
  not a byte lock. Ten terms, each proven red by breaking the draft or
  the PoC plan.
- Six figures in the draft resolve to no file it names. Each is
  registered with a checked reason (a Phase 1 quote, a DOI, a projection,
  a hardware-plan quote, a derivation, a refused run's value). The guard
  fails if one of them later resolves or leaves the document.

## V4. Task E: fresh-eyes review fixes (f62bb6c, #127)

- The F188 passages name both readings: the registered reading ("kept"
  on two instances, by gains the rounding made) and the amendment's
  ("worse than greedy on all six"). They also say 200:1 is QCi's Dirac-3
  figure, not measured on Dirac-3S.
- Experiment 5: four scorable segments (C, R, H, S), not three.
- The guard now reads a citation wrapped across lines and refuses a
  revision-log date in the future, each with a proof.

## V5. Task C (F178): learning documents, 2026-11-16 version (b37e1e5)

- See A5.

## V6. Phase 5 checks

- CI's full job, red proofs included: green on b37e1e5.
- Changed-file tests and proofs: passed locally on b37e1e5 (the run
  recorded for the pre-push hook).
- Plan Definition of Done walked:
  - every task's acceptance criteria: met (V1-V5);
  - each readiness term has its own test, proven red in the commit that
    adds it: met (8682ea7, f62bb6c);
  - CI full job green on the final HEAD: met;
  - Manual Validation items listed on screen and saved here: met;
  - retrospective, summary and master plan: after this step.

## V7. For the retrospective

- Every task timer understates its work (A 6, B 12, D 14, C 4, E 1
  minutes). E's timer started after its edits were done, because the
  commit hook refused a review fix with no running timer and the status
  tool would not restart the finished Task D. The hook's message names
  `--resume-task`, which only works for a paused task. The path that
  works is a new task with its own issue.
- The revision-log proof went vacuous when the review fix added a second
  row with the same date as the row it back-dated. It now moves the
  change date past the newest row instead.
