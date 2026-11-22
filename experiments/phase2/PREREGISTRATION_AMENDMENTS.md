# Phase 2 Preregistration: Amendments After Filing

**What this file is.** The Phase 2 preregistration was submitted for
filing on 2026-11-18. The submitted text is locked and is never edited.
Every change, result note, new entry or filing fact written after
filing goes here, as a dated entry, in the order it was written. This is
the model the Phase 1 preregistration used: the protocol locked first,
then amendments written as the work went along (team lead, 2026-11-22,
Sprint 34 D2).

**The locked files.** `experiments/src/test_phase2_prereg_filed.py`
fails on any change to them.

- `experiments/phase2/PREREGISTRATION_SUBMITTED_2026-11-18.md`: the
  text sent on 2026-11-18, restored byte for byte from commit b8e2c0e.
  The tag `phase2-prereg-filed` points at that commit (entry P2-A2).
- `experiments/phase2/PREREGISTRATION_FINAL.md` and
  `experiments/phase2/PREREGISTRATION_DRAFT.md`: the two copies as they
  stood when the lock was added. They differ from the sent text in
  section 7's lock wording and two revision-log rows, added at 09:18
  after the review of PR #122 (entry P2-A2). Result files and modules
  cite the draft by name, so it keeps its name.

**If a new submission is asked for.** It is built from the sent text and
the entries below, as a new document. None of the locked files is
changed for it.

**The rule for each entry** (`experiments/src/test_phase2_prereg_amendments.py`
checks the form):

- A heading `### P2-A<n>. <date>: <title>`, numbered from 1 with no gap,
  dated YYYY-MM-DD, never later than the day it is committed, and never
  earlier than the entry above it.
- A `- **Filed section**:` line naming the section of the filed text the
  entry changes or adds to.
- A `- **Kind**:` line, one of: procedure, filing fact, result note,
  amendment, new entry.
- An amendment or a new entry is committed before the run it governs;
  git records that order. A result note names its result file.
- An entry is not edited after it is committed. A correction is a new
  entry that names the one it corrects.

## Entries

### P2-A1. 2026-11-22: Post-filing text goes in this file, not in the filed text

- **Filed section**: 7, "Open, filing step: lock the filed version"
- **Kind**: procedure
- **Decided by**: the team lead, Sprint 34 D2 option 1 (2026-11-22)

The filed section 7 says amendments are "appended below" an
"## Amendments" heading in the filed file, and that the lock step runs
after the filing venue is recorded. Both are changed here, before any
amendment was written:

- No heading is added to any locked file. Every amendment is an entry
  in this file. The team lead, 2026-11-22: "neither as filed copy
  (phase 1 and phase 2) should ever be changed. Keep track of
  amendments for what we do later."
- The lock is added now, with the Filing section's venue line reading
  "not set" (Sprint 34 D3 option 1). The venue is not known (Sprint 34
  Q1). When it is known, it is recorded here as a "filing fact" entry.

What does not change: every commitment in the filed "What filing
commits to" and every rule in sections 1 to 6 stands as filed. An entry
here may add to them; it does not remove one.

### P2-A2. 2026-11-22: Which text was submitted

- **Filed section**: Filing
- **Kind**: filing fact
- **Decided by**: the team lead, Sprint 34 Q2 (2026-11-22)

The team lead sent the preregistration at 9:01am EST on 2026-11-18
("the one I said I sent on 11/18/2026 9:01am EST"). The last commit
before then is b8e2c0e (08:54:50 -0500); the next is c3d3c00 (09:18:27
-0500). The sent text is taken to be b8e2c0e's. This is an inference
from the commit times: text changed but not committed before 9:01 would
not be in b8e2c0e, and nothing records such a change.

- At b8e2c0e the FINAL and draft copies are byte-identical, SHA-256
  `3d09845dbffae163d6819a9bdd3970843c8dafeee987034cb42aa2a1286019d6`.
  `PREREGISTRATION_SUBMITTED_2026-11-18.md` holds those bytes.
- c3d3c00 changed both copies after the send: section 7's lock item
  gained the wording on when the lock runs, where the heading goes and
  the byte-identical check (from the PR #122 review), and the revision
  log gained two rows. Nothing in sections 1 to 6 changed. The copies
  are locked as they are; the sent text is the SUBMITTED file.
- The permanent link is the tag `phase2-prereg-filed` at b8e2c0e.
