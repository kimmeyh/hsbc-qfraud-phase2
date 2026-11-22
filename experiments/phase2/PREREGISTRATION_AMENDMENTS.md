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

### P2-A3. 2026-11-22: Experiment 5 re-entry, a segment measure that does not saturate

- **Filed section**: 6, a new entry beside Experiment 5 (F121)
- **Kind**: new entry
- **Decided by**: the team lead selected F197 for Sprint 34 (2026-11-21).
  The saturation check below runs at once; the run waits for the team
  lead's approval of this entry.

Written 2026-11-22 (Sprint 34 Task G, #141), before any score under its
measure is computed. Experiment 5's result is known: no segment was
accepted, recall at the 0.5% budget within the segment saturated on C,
R, H and S (the champion's alerts were all frauds), and the proxy was
below the champion on C and H on all ten seeds
(`docs/phase2/EXP5_ROUTER.md`). This entry changes the measure only;
every other choice is Experiment 5's, so the two can be read together.

- **ID and card**: Experiment 5b, F197.
- **Question**: on prespecified fraud segments, out of time, does routing
  a segment to the CVQBoost proxy give at least 0.01 of average precision
  (AUPRC) within the segment over the classical champion, beyond what a
  matched random segment gives?
- **Hypothesis and prediction**: no transfer, for Experiment 5's reasons
  (F162, F113, F174), and because the proxy was below the champion on C
  and H under the first measure. The prediction is that no segment is
  accepted.
- **Falsifier**: any segment accepted by the rule below, with the
  classical reference check passed.
- **Data and splits**: Experiment 5's. F174's stored month-4 test scores
  (85,302 rows), seeds 42-51, no new fit; the row-alignment check first,
  and the run stops if any stored label vector differs.
- **Arms**: Experiment 5's. Champion F174's LightGBM lane; proxy F174's
  proxy lane; classical reference F174's HGB lane. Each configuration
  was chosen per seed on month 3.
- **Primary metric and test**: the **in-segment edge** of lane L on a row
  set R is L's AUPRC on R (`sklearn.metrics.average_precision_score`)
  minus the champion's AUPRC on R. AUPRC ranks every row of R, so it has
  room above the champion wherever the champion's AUPRC is below 1. The
  control, its 20 draws and their seeds (`numpy.random.default_rng(1000 x
  seed + segment index)`), the downsizing, and the router criterion are
  Experiment 5's: S is **accepted** when the mean in-segment edge over
  the 10 seeds is at least 0.01 and the 99% t interval (1 - 0.05 / 5) of
  segment edge minus control edge lies wholly above 0. The exact
  two-sided Wilcoxon p-value is reported beside it, as secondary
  (section 2a: 10 seeds reach 2 / 2^10, below 0.05 / 5).
- **Saturation check, before the run** (`experiments/phase2/src/f197_saturation.py`,
  champion scores only): a segment has room when the champion's AUPRC on
  it is at most 0.99 on every seed. A segment without room is reported
  as saturated under this measure too and is not scored. The check's
  reference: on the same scores, Experiment 5's measure must saturate on
  at least one segment; if it does not, the check cannot tell the two
  measures apart and the result says so.
- **Multiplicity**: one family, the five ProductCD segments, m = 5,
  Bonferroni 0.05 / 5. It is not combined with Experiment 5's family.
- **Device**: none. Zero metered seconds.
- **Stopping rules**: the alignment check fails, the run stops. The
  classical reference check runs first: the same criterion with HGB in
  the proxy's place; if HGB is accepted on any segment, the run stops
  before any proxy figure is computed and a redesign is written as a
  decision. A segment that cannot be scored (no feasible control, as W
  was) or has no room is reported as such.
- **What is reported whatever the result**: per segment and seed, the
  rows and positives in S and in the control, any downsizing, each
  lane's AUPRC within S, both edges, the interval, the Wilcoxon p-value
  and accepted or not; the saturation check; the alignment check; an
  outcome block per lane and seed (with the 0.1% budget).
- **Output**: `experiments/phase2/results/exp5b_router.json` (`SIM`) and
  `docs/phase2/EXP5B_ROUTER.md`.
