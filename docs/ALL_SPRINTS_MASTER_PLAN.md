# All Sprints Master Plan

Adapted 2026-08-30 from spamfilter-multi's ALL_SPRINTS_MASTER_PLAN.md structure. This document is IN THE REPOSITORY and persists across conversations. Read it before every sprint (Phase 1/2), update it after every sprint (Phase 7.7/8.2).

## Maintenance Guide

- **After each sprint (Phase 7.7 / 8.2)**: update "Last Completed Sprint"; add the sprint's row to "Past Sprint Summary" once its SUMMARY doc exists; prune shipped items from "Next Sprint Candidates"; add retro Category-14 items with new F#s.
- **During Sprint N+1 planning (Phase 3.2.1)**: create `docs/sprints/SPRINT_N_SUMMARY.md` for the just-finished sprint and link it here.
- **IDs**: F# for all features/process/tech-debt items; next available number; never reuse.
- **Estimates**: minutes/hours from recorded actuals; `[no-history]` where uncalibrated.
- `CHECKLIST-Phase2.md` is the LIVE deliverable ledger; this document is the sprint-scoping view over it. Keep them consistent; the checklist wins on deliverable truth, this file wins on sprint sequencing. (`CHECKLIST-Phase1.md` is the CLOSED Phase 1 record and is never updated. The repo-root `CHECKLIST.md` was split into three files on 2026-09-12; `CHECKLIST-Phase2-pre.md` was merged into `CHECKLIST-Phase2.md` and deleted on 2026-10-03, and items 5 and 6 of the six were corrected to match the filed proposal at the same time.)

## Past Sprint Summary

| Sprint | Summary doc | Status | Duration |
|---|---|---|---|
| 1 | docs/sprints/SPRINT_1_SUMMARY.md | [OK] Complete | ~1 day (Aug 30, 2026) |
| 2 | docs/sprints/SPRINT_2_SUMMARY.md | [OK] Complete | ~2 days (Aug 31 - Sep 2, 2026) |
| 3 | docs/sprints/SPRINT_3_SUMMARY.md | [OK] Complete | ~1.5 days (Sep 2-3, 2026) |
| 4 | docs/sprints/SPRINT_4_SUMMARY.md | [OK] Complete | ~1.5 days (Sep 3-4, 2026) |
| 5 | docs/sprints/SPRINT_5_SUMMARY.md | [OK] Complete | ~1 day (Sep 4, 2026) |
| 6 | docs/sprints/SPRINT_6_SUMMARY.md | [OK] Complete | ~1 day (Sep 5, 2026) |
| 7 | docs/sprints/SPRINT_7_SUMMARY.md | [OK] Complete | ~1 day (Sep 5, 2026) |
| 8 | docs/sprints/SPRINT_8_SUMMARY.md | [OK] Complete | ~1.5 days (Sep 6-7, 2026) |
| 9 | docs/sprints/SPRINT_9_SUMMARY.md | [OK] Complete | ~1.5 days (Sep 7-8, 2026) |
| 10 | docs/sprints/SPRINT_10_SUMMARY.md | [OK] Complete | ~1 day (Sep 9, 2026) |
| 11 | docs/sprints/SPRINT_11_SUMMARY.md | [OK] Complete | ~1.5 days (Sep 9-10, 2026) |
| 12 | docs/sprints/SPRINT_12_SUMMARY.md | [OK] Complete | ~2.5 days (Sep 10-12, 2026) |
| 13 | docs/sprints/SPRINT_13_SUMMARY.md | [OK] Complete | ~1 day (Sep 12, 2026) |
| 14 | docs/sprints/SPRINT_14_SUMMARY.md | [OK] Complete | ~2 days (Sep 12-14, 2026) |
| 15 | docs/sprints/SPRINT_15_SUMMARY.md | [OK] Complete | ~1 day (Sep 16, 2026) |
| 16 | docs/sprints/SPRINT_16_SUMMARY.md | [OK] Complete | ~1.5 days (Sep 16-17, 2026) |
| 17 | docs/sprints/SPRINT_17_SUMMARY.md | [OK] Complete | ~1 day (Sep 19, 2026) |
| 18 | docs/sprints/SPRINT_18_SUMMARY.md | [OK] Complete | ~2 days (Sep 22-23, 2026) |
| 19 | docs/sprints/SPRINT_19_SUMMARY.md | [OK] Complete | ~7 days (Sep 23-30, 2026) |
| 20 | docs/sprints/SPRINT_20_SUMMARY.md | [OK] Complete | ~4 days (Sep 30 - Oct 4, 2026) |
| 21 | docs/sprints/SPRINT_21_SUMMARY.md | [OK] Complete | ~3 days (Oct 4 - Oct 6, 2026) |
| 22 | docs/sprints/SPRINT_22_SUMMARY.md | [OK] Complete | ~2 days (Oct 6 - Oct 7, 2026) |
| 23 | docs/sprints/SPRINT_23_SUMMARY.md | [OK] Complete (Tasks C and D done in the Phase 1 repository: `as-filed` tag at 4aa17d2, repository archived; verified 2026-10-13) | ~1 day (Oct 8, 2026) |
| 24 | docs/sprints/SPRINT_24_SUMMARY.md | [OK] Complete | ~2 days (Oct 9-10, 2026) |
| 25 | docs/sprints/SPRINT_25_SUMMARY.md | [OK] Complete | ~4 days (Oct 10-13, 2026) |
| 26 | docs/sprints/SPRINT_26_SUMMARY.md | [OK] Complete | ~5 days (Oct 13-17, 2026) |
| 27 | docs/sprints/SPRINT_27_SUMMARY.md | [OK] Complete | ~2 days (Oct 18-19, 2026) |
| 28 | docs/sprints/SPRINT_28_SUMMARY.md | [OK] Complete | ~4 days (Oct 22-25, 2026) |
| 29 | docs/sprints/SPRINT_29_SUMMARY.md | [OK] Complete | ~5 days (Oct 26-30, 2026) |
| 30 | docs/sprints/SPRINT_30_SUMMARY.md | [OK] Complete | ~6 days (Oct 30 - Nov 4, 2026) |

## Last Completed Sprint

**Sprint 30: Measure the Work, Survive the Limits, Then Test the Ceiling
and the Room** (Oct 30 - Nov 4, 2026; PR #74, main PR #91). Delivered **F173, F175,
F168, F174, F176, F169, F170, F171, F172**, the Phase 5 fresh-eyes fixes,
the Manual Validation fixes (D8: TP, FP, TN and FN on the comparison
pages), the CI cut to a 3:08 push job with the red proofs in a full job
(D9), the PR 74 review fixes and retrospective IMP-1 to IMP-5 (D10, all
applied). F177 and F178 carded. Zero metered seconds. F174: on IEEE-CIS
month 4 the order by mean test AUPRC is LightGBM, HGB, CatBoost, XGBoost,
the proxy, SVM, logistic regression; four of six adjacent pairs differ
reliably. F176: below greedy on 3 of 6 IEEE-CIS instances, each by under
2e-05. F169: both plug-ins pass F108's rule. F170: the ULB frauds missed
by all sit among legitimate rows. F171: not shown, because 4 IEEE-CIS
families are compared with 12 ULB families. Records: `SPRINT_30_PLAN.md`,
`SPRINT_30_VALIDATION.md`, `SPRINT_30_DECISIONS.md`,
`SPRINT_30_RETROSPECTIVE.md`, `SPRINT_30_SUMMARY.md` (written at Sprint
31 planning).

### Sprint 29: Make the Tools Repeatable, Then Find the Best Each Model Can Do
(Oct 25 - Oct 30, 2026; PR #63). Delivered **F165, F159, F164, F156,
F160, F166, F158, F167** and the pypdf bump, the PR 63 review fixes
(`provenance.start` refuses a rerun over a recorded result before any
work), the decisions file rule (`SPRINT_n_DECISIONS.md`) and retrospective
IMP-1 to IMP-4 (F172 carded). F169, F170 and F171 carded at Manual
Validation. Zero metered seconds. F159: every parallel pool equals the
serial pool on the validation rows. F156: the Henze-Penrose bound fails,
so F114 stays blocked (F169 next). F160: Experiment 3 has room on
IEEE-CIS, so F25's design reopens there; no solver has yet beaten greedy.
F166: on ULB two adjacent pairs differ reliably (the CVQBoost proxy above
the linear SVM, the SVM above logistic regression). F158: the per-type
cascade is below one model. Records: `SPRINT_29_PLAN.md`,
`SPRINT_29_VALIDATION.md`, `SPRINT_29_DECISIONS.md`,
`SPRINT_29_RETROSPECTIVE.md`, `SPRINT_29_SUMMARY.md` (written at Sprint 30
planning).

### Sprint 28: Experiment Entries First, Then Their First Measurements
(Oct 22 - Oct 25, 2026; PR #46). Delivered **F154, F115, F151, F13
(skeleton), F114, F152, F153, F110, F111, F162**, F146 and F150 drafts,
the pypdf bump, D4 (every device job stored in full, every new result with
its provenance) and retrospective IMP-1, 2, 4, 5 and 6 (F164 carded).
Zero metered seconds. F151: `l2_regularization=1.0` alone stabilizes ULB's
HGB. F152: P1 holds on IEEE-CIS months 4 and 5. F153: the Experiment 3
proxy design fails on all six instances. F110: P1 is false; P2 holds at
833 variables. F111: the KNN lane is not consistent with 0.8108 under
either protocol. F114: still blocked. F162: inside the SPECTRA pocket the
proxy is not reliably above HGB or XGBoost on any cell. Records:
`SPRINT_28_PLAN.md`, `SPRINT_28_VALIDATION.md`,
`SPRINT_28_RETROSPECTIVE.md`, `SPRINT_28_SUMMARY.md` (written at
Sprint 29 planning).

### Sprint 27: Gates Before Reporting, and the Screens That Need No Device
(Oct 18 - Oct 19, 2026; PR #32, main PR #45). Delivered **F149, F104, F102 (section 7;
the card stays open), F112, F130, F103, F109, F6, F106, F107, F108**, an
F146 update (the QCi questions, sent by the team lead 2026-10-18) and
retrospective IMP-3, IMP-6 and IMP-7 (F151 carded). Zero metered seconds.
F112: P1 holds and P2 is equivalent within 0.005. F130: no lever beats HGB
on SPECTRA, and ULB's HGB comparator is unstable (F151). F103 passes on the
real target and the sparse pocket; the dense substrate misses (F150).
F109: the g4 prediction is not falsified. F6: pursue the gate-based arm in
simulation only. F106 is inconclusive. F107: about 10,000 shots per row or
more. F108: no ceiling method is validated. Records: `SPRINT_27_PLAN.md`,
`SPRINT_27_VALIDATION.md`, `SPRINT_27_RETROSPECTIVE.md`,
`SPRINT_27_SUMMARY.md` (written at Sprint 28 planning).

### Sprint 26: Reach Dirac-3S, Measure It, and Make the Proxy Repeatable
(Oct 13 - Oct 16, 2026; PR #21, main PR #31). Delivered **F141, F145, F144, F142, F147,
F126, F105** and two F146 updates (more than the two planned), Task I
(Decision 10: the cross-repo guard covers sibling Claude Code project
directories; EvidenceBasedDB is read freely), Decision 11 (Dirac-3S is the
Phase 2 default device) and retrospective IMP-1 to IMP-5. F142 spent 86.0
Dirac-3S seconds over 5 fits against about 172 planned: on B4 Dirac-3S
returned the reference optimum where Dirac-3 did not, with test AUPRC
unchanged. F144: Dirac-3 does not beat its own proxy on B2. F126's rule
fails. F105's harness passes every leakage audit; no score. Open: QCi
question A6 (output resolution), and F126 and F25 read against Dirac-3S.
Records: `SPRINT_26_PLAN.md`, `SPRINT_26_VALIDATION.md`,
`SPRINT_26_RETROSPECTIVE.md`, `SPRINT_26_SUMMARY.md`.

### Sprint 25: Learn the New Device, Then Build What Runs on Any Device
(Oct 10 - Oct 13, 2026; PR #12, main PR #20). Delivered **F138, F139, F102 (first
draft; the card stays open), F113, F29, F94**, Task G added at Manual
Validation (F146's document; F147 carded), and retrospective improvements
IMP-1 to IMP-4. 172 measured minutes against 750 estimated, zero metered
seconds. Dirac-3S needs a client bump to reach (F141) and a measured fit to
price (F142). F113 found nothing that supports a router; F29 closes; F94
found the training-fold Hamiltonian has many tied optima, so F25 must
choose its ridge weight and build on held-out predictions. F129 closed by
the team lead; F121 needs a new hold condition at Sprint 26 refinement.
Records: `SPRINT_25_PLAN.md`, `SPRINT_25_VALIDATION.md`,
`SPRINT_25_RETROSPECTIVE.md`, `SPRINT_25_SUMMARY.md`.

### Sprint 24: Close the Boundary, Fix the Tooling, Sweep the Lever (Oct 9 -
Oct 10, 2026; PR #2, the first sprint in this repository). Delivered
**F131, F136, F132, F134, F133, F135, F128, F137**, plus retrospective
improvements IMP-1 (one owner for the Dirac-3 balance) and IMP-4. 84
measured minutes against 290 estimated, zero metered seconds. **F128 fired
its premise falsifier**: no leaf value beats HGB with a CI excluding zero
on any dataset; F129 is re-scored at the next refinement. QCi loaded the
account on 2026-10-09 and announced Dirac-3S: F138 and F139 lead Sprint 25
and gate every Dirac-3 card. Records: `SPRINT_24_PLAN.md`,
`SPRINT_24_VALIDATION.md`, `SPRINT_24_RETROSPECTIVE.md` and
`SPRINT_24_SUMMARY.md` (written 2026-10-13, Sprint 25 Phase 3.2.1).

### Sprint 23: Restore the Repository as Filed** (Oct 8, 2026; ran in the
Phase 1 repository, PR #167 there, still draft). Delivered F127's Task A
(restore dry run) and Task B (the sprint record). Its record is on this
repository's `feature/20261007_Sprint_23` at c3d9ec3: plan, validation and
retrospective in `docs/sprints/`. **Tasks C and D (the restore commit and
the `as-filed` tag) ran in the Phase 1 repository**: the `as-filed` tag is
at 4aa17d2 and the repository is archived (verified read-only 2026-10-13).
Its three improvements are carded here as F134, F135 and F136.

Summary: `docs/sprints/SPRINT_23_SUMMARY.md` (written 2026-10-09, Sprint 24
Phase 3.2.1). Its issues #168-171 live in the Phase 1 repository and are
that session's to close; nothing here touches them.

### Sprint 22: Separate the Phases, Then Look for Better Numbers** (Oct 6 -
Oct 7, 2026; PR #159, main PR #166). Delivered **F123, IMP-3, F124, F17, F20, F125**.
256 minutes recorded against 980 estimated, zero metered seconds. The record
is `docs/sprints/SPRINT_22_SUMMARY.md`, with the retrospective and
`SPRINT_22_VALIDATION.md` beside it.

**F124's ranked list is approved and gates every device run**: leaf
regularization first, at parity with HGB on energy_steel only. **Phase 2
moves to its own private repository** (team lead, Manual Validation): F127
is first after the merge, and this repository is then restored as filed and
archived. B2's full device samples are not recoverable (QCi 404).

### Sprint 21: The SPECTRA Block, and a Bar That Can Read It (Oct 4 - Oct 6,
2026; PR #152). Delivered **F90, F100, F101, F122**. 454 minutes against 750
estimated, plus **653 metered seconds** (B5 13 + B4 640), reconciled against
the device balance, 1,675 s to 1,022 s. The record is
`docs/sprints/SPRINT_21_SUMMARY.md`.

**The H5 replication did not reproduce on the device.** The in-segment edge
against the matched control is negative on all 8 scoreable cells, and the
device matches its classical proxy within 0.0072 in-pocket AUPRC on every
cell. energy_steel is `unscoreable`: its matched control is infeasible. HGB
and GA2M beat the proxy on every cell (F100); `in_pocket` is predictable
from the phase features at AUC 0.93-0.99 (F101).

**F123 and F124 were registered by the team lead**: separating Phase 2 files
from Phase 1's, and researching what to try before any further Dirac-3 run.
Every open card that can spend device seconds depends on F124.

### Sprint 20: Make the Suite Readable Again (Sep 30 - Oct 4, 2026; PR #146
to develop, PR #151 to main). Delivered **F97, F93, F98, F99** in 161
minutes against 171, zero metered seconds. The suite went green in a
planning window for the first time, and the close-out hook can no longer be
silenced by a slow network. The record is `docs/sprints/SPRINT_20_SUMMARY.md`.

### Sprint 19: Send the QCi Package Clean (Sep 23-30, 2026; PR #141 to
develop, PR #145 to main). Delivered **F92**. **The package was SENT 2026-09-25
at 12:23 PM** -- that was the objective. Task C was not approved and became
F96, since closed as overtaken; a fresh-context review found fourteen
cross-document disagreements, eight fixed. Zero metered seconds. The record is
`docs/sprints/SPRINT_19_SUMMARY.md`, `SPRINT_19_RETROSPECTIVE.md` and
`SPRINT_19_VALIDATION.md`; this section only points at them.

**THE FOUR PACKAGE DOCUMENTS ARE NOW FINAL** (team lead, 2026-09-27) and will
never change again. The memo is preserved as its `.htm` export with the
`_files` sidecar and as `Phase 1 - QCi memo AS SENT 2026-09-25.md`; its
thirteen wording guards were retired because the draft they read was deleted.
The guards on `QCI_EQC_MODELS_FEEDBACK.md` and `HARDWARE_PLAN_PHASE_2.md`
are KEPT: both sources are present and green, and on frozen text those guards
are the only thing that would notice an accidental edit.

**Known and permanent: the schedule-4 gap.** The memo commits to a ~60 s
schedule-4 check against the 1,681 seconds then held; the attached hardware
plan does not mention it. Verified with `pypdf`: the sent PDF contains 1,681,
7,319, 7,500 and 9,000 and does not contain "schedule 4". Both documents are
final, so this is recorded rather than fixed.

Sprint 18: The First Phase 2 Evidence, and the Cost of the Ask (Sep 22-23,
2026; PR #139 to develop, PR #140 to main). Delivered **F87, F64, F88, F89**,
plus **F91** and a second integer probe round added mid-sprint. F2b deferred to
F90 before execution. The record is `docs/sprints/SPRINT_18_SUMMARY.md` and
`docs/sprints/SPRINT_18_RETROSPECTIVE.md`.

(Rolled 2026-09-23 in the Phase 8 sweep. This section had still described
Sprint 14 through four later sprints, because the Sprint 15, 16 and 17 sweeps
rolled `sprint_status.json` and not this heading. The Sprint 14 narrative that
stood here lives in SPRINT_14_SUMMARY.md.)

**What this document is, and is not** (team lead, 2026-09-15). The official
record of a sprint is five files: `SPRINT_n_PLAN.md`, the review/retrospective,
`SPRINT_n_SUMMARY.md`, `CHANGELOG.md` and `README.md`. This is a PLANNING
document. Its history section is convenience, not the audit trail, and it
REFERENCES those five rather than restating their numbers. Where a number does
appear here it needs to be right once, at backlog refinement, not continuously;
a stale PR number in a completion stub is not a defect worth a commit. Suite
counts are never restated anywhere: run the suite.

Why this is written down: a PR review asked for ten deleted completion stubs to
be restored as "the surviving audit trail". They were not. The summaries are.
Restoring them would have re-created ten copies of numbers owned elsewhere.

## Targeted roadmap (team lead, 2026-09-03; each sprint's scope is re-validated at its own refinement)

| Sprint | Dates | Targeted scope | Gate |
|---|---|---|---|
| 4 | Sep 3-5 | [DONE] F22, F21, F2 (per-block approval), F7 | -- |
| 5 | Sep 4 | [DONE] F8, F9, F27, F26, F28, F19 | -- |
| 6 | Sep 5 | [DONE] F31, F3 prep, F23, F24, F32 | -- |
| 7 | Sep 5-6 | [DONE] F33, F34, QCi/paper update | -- |
| 8 | Sep 6-7 | [DONE] **F3** (IEEE-CIS, all four tasks) + paper updates; F36 attempted and FAILED | -- |
| 9 | Sep 7-8 | [DONE] F4 (H6, measured null), F14, F16; **QCi package SENT** 2026-09-08 09:59 | -- |
| 10 | Sep 9 | [DONE] **F40** (segmentation) re-scoped to F40 only; gate-report undercount fixed (27/120 -> the true 37/163); 8 correctness findings from two adversarial reviews; 13 PR-review findings addressed | F37/F38 deferred to 11 |
| 11 | Sep 9-10 | [DONE] **F41** (A20, mechanism corrected), **F42** (+0.0319 decomposed: the gain is class weighting, not diversity), **F43**, **F44**, **F45**, **F35**, plus **F46** (A21, ceiling LIFTED) and **F47** added mid-sprint; 15 review findings addressed | F37 and the fresh-eyes review deferred to 12 |
| 12 | Sep 10-12 | [DONE] **F2b B2 and B3** on Dirac-3 (23 fits, 968 metered s), **F37**, **F38**, and **F49-F63** from three external reviews. F10 NOT reached | Evidence freeze held; F10 carries to Finalize |
| 13 | Sep 12 | [DONE] **F10**: evidence walk, requirements-matrix walk, confidentiality scan, final render, and the SUBMISSION -- filed 2026-09-12, three days early. F64 selected then withdrawn | **SUBMITTED**; 9 defects found and corrected |
| 14 | Sep 12-14 | [DONE] **F68-F72** plus **F48, F65, F66, F67**; two ADRs accepted for the Evidence Based DB. Two dead hooks found and fixed | **20 review findings**, all addressed; 2 vacuous guards caught by review |

**THE PHASE 1 ROADMAP IS COMPLETE (2026-09-12).** Every row above is [DONE] and
the submission is filed. The table described a run to a deadline; that deadline
has passed in our favor and the roadmap no longer describes any pending work.

What replaces it, recorded so the next refinement does not invent a schedule:
the judging window is **16 Sep to 14 Nov 2026**, with finalists announced
mid-November (Guidelines s2). Nothing we do changes the Phase 1 outcome, and no
backlog item is time-bound any more. The remaining items are tech debt, tooling,
and Phase 2 preparation, and they should be scheduled on value rather than
against a date.

The one exception is **F13, Phase 2 PoC sprint planning**, which becomes live
only on acceptance and is correctly held until then.

**Sprint 12 sequencing, DECIDED 2026-09-09 (Sprint 11 improvement 5) rather than under deadline pressure.** The order is forced by two dependencies, not by preference:

1. **Dirac-3 work first, if any is approved.** It produces new evidence, and evidence changes the documents. Run it in the evening window: measured queue wait is a 0.7s median after 19:00 local against the 52 minutes a 14:33 submission cost
2. **Then F38.** The page cut must run against FINAL content or it runs twice. This is why F38 has grown at every measurement
3. **Then F37.** Making the repository public is IRREVERSIBLE. Nothing that could still change a document should follow it
4. **Then F10**, the submission itself, which depends on all three

If the calendar forces a cut, drop the Dirac-3 work: it is the only one of the four that is not a submission blocker.

Renumbered 2026-09-05: the team lead noted the project is running more than one sprint per day, so F33 took Sprint 7 and F3 moved to Sprint 8 rather than competing for the same hours. A submittable paper exists after Sprint 5; every later sprint adds evidence and re-runs the review loop on the diff. The "still time" gate is a calendar lookup against the Sep 12 evidence freeze.

RESTORED 2026-09-06: this section was destroyed by a card-pruning script during the Sprint 7 close-out (commit c40038d) and again in the Sprint 8 sweep before the loss was noticed. Both scripts deleted from a shipped card's header until the next card header, and a `## ` section heading that fell inside that span went with it. The prune step now stops at any `## ` heading, and this recovery came from commit be1198c.

## Deferred to Phase 2 (team lead, 2026-09-05)

**Does F33 change the Phase 2 priority?** Held until after the submission is
approved. The open question, recorded now so it is not re-derived later: F33
measured the optimizer contributing only +0.0043 over uniform weights even on a
well-constructed pool, while fit-time learner tuning moved absolute accuracy by
+0.0198 at matched size. That is an argument that the leverage in this
formulation sits in pool construction rather than in the optimization step, and
it bears directly on whether the cardinality-constrained integer experiment (F25)
remains the first Phase 2 experiment or yields to pool work. Both readings are
defensible on the current evidence: the integer formulation is the one where a
classical solve is NOT trivially available, so a small optimizer contribution on
a CONVEX problem does not predict a small one on an NP-hard problem. Deciding
now would be deciding without the evidence that Phase 2 exists to gather.

**NEW EVIDENCE 2026-09-11 (Sprint 12, F57/A31), recorded without deciding.** The
200:1 resolution finding bears directly on this question and points toward F25.
On all ten B2 pools the diagonal of J is 510,705 while off-diagonals span at most
20.0, against a resolvable difference of 2,554: nothing in the CONTINUOUS problem
is visible to the device. Quantised at that resolution the off-diagonal collapses
to one distinct value and the minimiser is uniform to 2e-15. The same limit
explains B2's 0.83 weight cosine -- a diffuse optimum over 833 learners averages
0.0012 per weight against a 0.005 resolution and is not representable.

That is an argument that the continuous formulation is the wrong ask of this
hardware, not that the optimizer has little leverage. A device that cannot spread
weight over ~200 learners has a native problem class, and it is
cardinality-constrained selection -- F25. It does NOT resolve the F33 reading
above, which is about where leverage sits rather than which formulation the
device can represent. Both are still open and the decision still waits for
Phase 2.

## Next Sprint Candidates

### Experiments (Stage 3 of the master timeline; submission-ready Sep 8)

(F1 classical evidence campaign and F18 Dirac-3 notes mining: COMPLETED in Sprint 3, merged via PR #13; history in SPRINT_3_SUMMARY.md. Removed from candidates per convention. F1 residual -- the section-6 CVQBoost proxy tuning -- continues as F22.)

(F22 CVQBoost proxy tuning and F2 hardware blocks B1+G0b: COMPLETED in Sprint 4, merged via PR #21; history in SPRINT_4_SUMMARY.md. F21 baseline research and F7 results memo likewise complete. Removed from candidates per convention. F2's remaining blocks B2/B3/B4/B5 continue as F2b below, gated on the QCi grant.)

(F68 freeze the submitted artifacts: COMPLETED in Sprint 14, merged via PR #94.
Both Edit-matcher hooks had never run; fixed, injection-proven, and guarded by
test_hook_registration.py. Removed from candidates per convention.)

(F69 README rebuilt for a public repository: COMPLETED in Sprint 14. Executing it
found an uninstallable lock file and a test that crashed where its peers skipped.
Removed from candidates per convention.)

(F70 CHANGELOG backfilled and wired into the close-out: COMPLETED in Sprint 14.
Workflow step 8.1.1 now runs before backlog refinement. Removed per convention.)

(F73 the submission explained at an 8th-grade level, and F74 its outline:
COMPLETED in Sprint 15. `docs/explainer/THE_SUBMISSION_EXPLAINED.md`, seven
sections, with the falsifier result recorded alongside it in
FALSIFIER_RESULT.md. See SPRINT_15_SUMMARY.md and CHANGELOG.md. Removed from
candidates per convention.)

(F87 the integer-solver sizing probe, F64 the k=17 order-2 ladder cell,
F91 the fourth ladder corner, F88 the false-finding mechanism and F89 the
injection helper: COMPLETED in Sprint 18. See SPRINT_18_SUMMARY.md and
CHANGELOG.md. Removed from candidates per convention.

Three findings outlived their cards and are recorded there:

- **B2's +0.0256 is attributed, not bounded.** F91 supplied the fourth corner:
  subset order carries the gain and feature count contributes nothing
  measurable. `docs/F64_LADDER_DECOMPOSITION.md` owns the figures.
- **Integer cost tracks VARIABLES, not the level budget**, from a controlled
  pair across five measured points. No high-variable point near the ceiling
  was run, so none is quoted. `docs/INTEGER_PROBE_RESULT.md` owns the figures.
- **Three metered calls were made against a two-call approval.** The runner
  had no idempotency check; it now has one, and Criterion H requires it before
  any metered runner's first approval.)

**F93. Reconcile the SPECTRA block: one card, one configuration, one cost -- CLOSED 2026-10-03 (decision made: F90 approved)**
- **CLOSED in the 2026-10-03 refinement.** The team lead approved F90 on 2026-10-03, which is the decision this card waited for; F2b's B4 line and F5 closed into F90 the same day. The card stays in place because `test_spectra_reconciliation.py` requires every SPECTRA record to remain findable and to point at the reconciliation
- **Sprint 20 delivered the reconciliation, not the decision.** All four
  records are now side by side in `docs/SPECTRA_BLOCK_RECONCILIATION.md` with
  their provenance, plus the tension the card did not know about: the sent
  hardware plan quotes 270 s while F90's configuration costs about 1,236 s,
  which is 4.6x the figure in the vendor's hands and 74% of the remaining
  balance. Four options are laid out. The choice is Class 3 and remains the
  team lead's
- Phase: Experiments / Phase 2 evidence (added 2026-09-23, Sprint 18 Phase 8 refinement)
- Platform: docs (SPECTRA, Dirac-3 planning only)
- **Four records describe the same SPECTRA block and disagree.** F2b quotes B4 at 15 fits and ~450 s; F90 at schedule 3, 833 variables, ~1,236 s; F5 (HOLD) at 3 cells x 5 seeds; and the hardware plan sent toward QCi sizes Experiment 5, segment transfer, at 30 fits of 91-136 variables, about 270 s. F90 alone would spend 74% of the 1,681 s balance, while the draft QCi memo tells QCi the balance goes to a schedule-4 check and Experiment 5 at "a few hundred seconds"
- This enables: any metered SPECTRA spend, and an honest F92. This prevents: spending 1,236 s on a block the vendor has been told costs 270 s
- Acceptance: the team lead picks one configuration (schedule 2 at 91-136 variables, or schedule 3 at 833) with the reason recorded; F2b and F5 closed into the survivor; the survivor's cost labeled measured or extrapolated; the hardware plan's Experiment 5 row either matches it or is flagged for F92
- Depends on: nothing. The configuration choice is the team lead's (Class 3)

**F95. Relaxation schedule 4 on the residual (~1h build + approval, metered, cost unmeasured) Priority 160**
- **F138 re-check (2026-10-13, `docs/phase2/DIRAC_3S_RESEARCH.md`)**: the four schedules are unchanged on Dirac-3S. The Dirac-3S guide's 50-variable table puts schedule 4 at 3.04x schedule 2, inside this card's 2.3x-5.3x range, so the estimate below stands, but it was derived on Dirac-3 and the guide does not say its table was measured on Dirac-3S. Re-quote from F142's first measured Dirac-3S fit
- **Default device is now Dirac-3S (2026-10-16, Sprint 26 Decision 11).** This card's run goes to Dirac-3S unless its entry says why not. Its seconds estimate is a Dirac-3 figure; re-price it at refinement from F142's measured Dirac-3S costs with `qpu_cost_model.quote(n_variables, n_samples, relaxation_schedule=4)` (Sprint 26 IMP-5); today it returns unknown, because no Dirac-3S call has run at schedule 4, so the block is bounded by call count
- **Pass 2 finding (2026-10-18)**. **Measured**: F142's B1 fits on Dirac-3S at schedule 2, seeds 42 and 43 at 91 variables, are seeded rebuilds of the same configuration as this card's B1 dct pools (not the frozen pools themselves). They reached the reference optimum: objective gaps of +0.0007 and -0.011 on about -166,494 (relative 4.5e-9 and -6.7e-8), weight cosine 1.0 (`experiments/phase2/results/f142_dirac3s_verify.json`). Seed 43's device objective is below the reference's, which places the reference within its solve tolerance there, not the device beyond an optimum. **Inferred**: on Dirac-3S there may be no schedule-2 residual for schedule 4 to close in this configuration, so under the Dirac-3S default this card could measure nothing. The memo's question was asked of Dirac-3, where the gap was 0.413% (G0b). Answering it as promised needs Dirac-3 named on a `# device named:` line; the alternative is to report F142's rows as the Dirac-3S answer. That is a scope decision for the team lead, not a correction
- **UNBLOCKED 2026-09-25**: the hold was "until the QCi memo is sent", and it
  was sent 2026-09-25 at 12:23 PM. The sent memo commits to this check, so it
  is now promised work rather than optional
- Phase: Experiments (added 2026-09-23; promised in the QCi memo and carded nowhere)
- Platform: Dirac-3
- The feedback document's open question 1, "Would relaxation schedule 4 close the residual?", is still open: every Phase 1 fit ran schedule 2, frozen before the grant. The memo names it as a use of the remaining balance
- **Four fits at 45-91 variables**, enumerated in the HELD note below. Schedule-2 cost there is 4-9 s per fit, measured; **schedule-4 cost is unmeasured**, so the block opens with one fit to establish the rate (the F87 pattern). (Corrected 2026-09-27: this bullet said "about five fits at 91-136 variables" while the note below enumerated four, one of them at 45 variables. IMP-4 directs future readers to trust this card's numbers rather than re-derive them, so a card contradicting itself undercuts the rule that cites it. Found by both PR #141 reviews.)
- Acceptance: the runner is idempotent before its first approval (Criterion H); per-fit residual against the proxy optimum reported as `[HW]` rows beside their schedule-2 twins
- Depends on: a measured Dirac-3S rate at schedule 4 (corrected 2026-10-18, Pass 1: F141 and F142 are spent, both shipped in Sprint 26; F142 measured schedule 2 only, so `quote(..., relaxation_schedule=4)` still returns unknown and this block is bounded by call count) (corrected 2026-10-13, Pass 1: the F138-then-F139 gate is spent, both reported in Sprint 25; the F124 rank-1-first gate is spent too, because rank 1's device pilot, F129, was closed); per-block team-lead approval (Criterion H)
- **HELD until the QCi memo (F92) is sent** (team lead, 2026-09-23). Case and cost worked out at refinement, recorded so it is not re-derived: 4 fits on frozen pools that already have schedule-2 and exact-optimum twins (B1 dct seeds 42 and 43 at 91 variables; the G0b fit with the 0.413% gap; B1 lg seed 42 at 45 variables), stopping after fit 1 to re-quote if the rate exceeds 27 s. About 60 s, range 40-110 s, cap 120 s. Extrapolated, low confidence: measured schedule-2 cost of 4-5 s per fit times the 3.4x schedule-4 ratio (range 2.3x-5.3x) in QCi's portfolio example, a problem of unstated size. The per-fit data suggests the residual is a fixed offset (all 8 samples clustered well above the optimum), which predicts schedule 4 will NOT close it; that is inference, and the run is what settles it

**F90. F2b at the configuration that can actually show an effect: B5, then B4 at schedule 3 -- CLOSED 2026-10-06 (Sprint 21: B5 and B4 ran; the H5 replication did not reproduce)**
- **CLOSED.** B5 12 fits / 13 s and B4 10 feasible cells / 640 s ran on Dirac-3 on 2026-10-06. The in-segment edge against the matched control is negative on all 8 scoreable cells, and the device matches its classical proxy within 0.0072 in-pocket AUPRC. `docs/B4_B5_HARDWARE_RESULT.md` is the record. The card stays in place because `test_spectra_reconciliation.py` requires every SPECTRA record to remain findable
- Phase: Experiments / Phase 2 evidence. **This is the replication half of Experiment 5, Segment transfer (H5)** (proposal section 5; the 2026-10-03 checklist correction). A failure of H5 is the third condition the proposal names as retiring the approach. The transfer half is F121. Sprints with F100 and F101, which make its result readable
- Platform: SPECTRA, Dirac-3
**The four records are reconciled in `docs/SPECTRA_BLOCK_RECONCILIATION.md` (F93, 2026-10-02), which also records that QCi was SENT 30 fits at 91-136 variables for 270 s. The configuration choice is open and is the team lead's.**
- **SUPERSEDES F2b's sizing.** F2b quotes B4 at "15 fits, ~450 s" from the original grid. That grid was proven wrong by 2.3x at 833 variables in Sprint 12 (assumed ~40 s, cost 91 s), and the schedule choice underneath it was never stated. This card carries the measured figure and names the configuration.
- **APPROVED 2026-10-03 and scheduled for the next sprint** (team lead): he ran SPECTRA on another computer and Dirac-3 won in almost all cases, and directs the analysis matching prior Dirac-3 quantum-enhanced datasets to run next. That result is `[UNVERIFIED -- OFF-REPOSITORY]` here until its configuration, fits, seeds and arm are brought in, which is the next sprint's first task. F2b's B4 line and F5 close into this card. See `docs/SPECTRA_BLOCK_RECONCILIATION.md`
- **THE TUNED CONFIGURATION IS WHAT WINS, AND IT IS NOT THE ONE OUR LOSS FIGURE DESCRIBES.** Consulted for planning only (a prior-campaign findings document the team lead holds outside this repository; nothing copied in, not cited as evidence): the in-segment wins come from schedule 3 with 8 samples, relaxation schedule 2, and a ridge of about 2x the record count, which our own `qubo_proxy.py` already uses (`LAMBDA_MULT = 2.0`). Relaxation schedule 4 cost about 3.8x more per sample for no measurable accuracy gain, and shallower weak learners hurt badly -- so the Sprint 18 instinct to leave schedule at 2 was right for the RELAXATION schedule and wrong only if confused with the WEAK-CLASSIFIER schedule. Two different knobs, similar names
- **CAVEAT TO CARRY, now in the acceptance criterion below**: those in-segment wins came with a train-to-test gap well above XGBoost's on the `target` cells, one case dropping from 0.98 train to 0.59 test. The wins are real and fragile. Any Phase 2 claim from this block must report the train-test gap beside the win. (Corrected 2026-10-03: this bullet said "three to eight times XGBoost's on every `target` cell", copying the summary line of the off-repository findings document. That document's own table gives ratios of 83, 7.6, 8.2 and 1.7, so the summary is wrong at both ends. The ratios come from the 2026-09-30 EvidenceBasedDB check of that document; they are not evidence in this repository)
- **THE ACCURACY FIGURES BELOW ARE PROXY, NOT DEVICE.** Checked 2026-10-03: `experiments/results/spectra_proxy_dry_run.json` holds 15 rows, and the preregistration names the origin at line 46 (FourierWall2, 2026-08-04). **CORRECTED 2026-10-05: the "13 of 13 scored cells" this bullet claimed is 8 of 13.** The five energy_steel rows report a control of 927-950 positives drawn from a complement holding only 832-864, which is impossible: they predate the complement-pool correction (`775942b`) and their controls overlapped the segment they controlled for. energy_steel is `unscoreable` for Phase 1. The 8 feasible cells are all still negative, so the direction holds and the completeness does not. See `docs/SPECTRA_CONTROL_FEASIBILITY.md`. They are sourced -- but every row is `evidence_tag: PROJ`, `metered_seconds: 0`. **This repository has never run SPECTRA on Dirac-3.** So "schedule 2 lost 8 of 8" means the PROXY lost in-segment, and says nothing about the device. The team lead's 2026-10-03 device run does not contradict it; it tests the arm we never tested. The COST anchor in the next bullet is measured and stands
- **B4 runs at schedule 3.** In the prior SPECTRA work, schedule 2 reportedly lost overall 8 of 8 to the classical arm with only ~3 in-segment metrics won; schedule 3 -- which adds three-feature interactions -- took CVQBoost to in-segment ROC 5 of 7 and PR 6 of 7, and to an overall win on energy_steel. Schedule 3 is the accuracy lever. **A schedule-2 block would spend real seconds reproducing a configuration already known to lose, which is not a cheap experiment but a worthless one.**
- **COST. CORRECTED 2026-10-05 at the Sprint 21 capability pre-flight; the variable count and the per-cell sizing were both wrong.** The formula `n + C(n,2) + C(n,3)` is the **`full`** pair-build. `data.qubo_vars` (amendment A2) caps pairs at `n(n-3)/2` for the **`sequential`** build, which the B4 request states is **mandatory on Windows**, so singles+pairs total `C(n,2)` exactly. The cells are therefore **816 / 816 / 560**, not 833 / 833 / 575, and `spectra_proxy_dry_run.json` records exactly those counts. B4 is also THREE cells, not one at a single size, so pricing all 15 fits at one rate was wrong in the expensive direction:
  - **B2 is the anchor and its configuration matches B4's exactly** -- `num_samples=8`, `relaxation_schedule=2`, `weak_cls_schedule=3` -- differing only in `pair_build` (`full`, so 833 vars) and dataset. 11 metered fits, 906 s, **71-92 s/fit, mean 82.4** (`[HW]`, results.json).
  - **B4 at the anchor rate: 10 fits at 816 + 5 at 560 = about 1,084-1,235 s, 65-74% of the 1,681 remaining**, leaving 446-597 s. The low end scales linearly from the anchor; the high end prices every fit at the anchor itself. Provenance: `measured` for the 816 cells (816 is 98% of the anchor's 833), `extrapolated` for the 560 cell, which sits BELOW the anchor where the cost curve is not linear -- the metered rate per variable runs 49-556 ms/var below 100 variables against 99 ms/var at 833, so a floor applies and 560 may cost more than a linear read suggests.
  - **UNRESOLVED COST CONFLICT, and it is a factor of 2.4.** `HARDWARE_REQUEST_B4.md` line 43 prices this block from FourierWall2's measured rollout at **26-34 s/fit for 560-816 vars at this exact ns/rx/schedule**, giving an expected total of ~390-510 s, and cites the preregistration section 10 envelope of ~450 s. Our own B2 measured 76-91 s/fit at the same configuration. Both are described as measured; they cannot both price B4. The B4 request is the document QCi holds a plan against, so this must be settled BEFORE the block runs, not after. B5 running first is what settles it cheaply.
  - **B5 (QSVM, 12 fits): 15-62 s.** Provenance: `extrapolated` from B3's 5.2 s/fit.
  - Run B5 FIRST. It is cheap and it exercises the approval and ledger path before the expensive block.
- **THE A31 READING THAT MUST NOT BE REPEATED.** The Sprint 18 plan first argued that A31's ~200-learner resolution limit made schedule 3 a worse experiment. That is backwards. A31 predicts the MECHANISM -- weight over more than ~200 learners is not representable, so the device returns something sparser -- not a bad OUTCOME. B2 ran at 833 variables with weight cosine 0.83 and produced the campaign's ONLY positive result at scale, +0.0256 on ten of ten seeds. The sparsified answer was better. Whether that repeats on SPECTRA is the actual experiment.
- **Sizing note for any later cell**: telecom_churn at schedule 3 is 987 variables, over the ~940 usable ceiling. It needs one feature dropped (18 -> 17 gives 833) or it cannot run at all. energy_steel (833), oilgas (575) and maintenance (298) fit.
- **Reconcile with F5 BEFORE B4 runs.** F5 (SPECTRA in-segment replication) is the same block from another angle and they must not both be scheduled. F5's HOLD reason names a QCi grant that "has only been acknowledged, not granted"; the grant arrived 2026-09-09 and 1,681 s remained (2026-09-23). That gate was stale and is corrected on the F5 card (Phase 8 sweep, 2026-09-23).
- **Acceptance**: B5 and B4 complete as `[HW]` rows with metered seconds from the response; the in-segment result reported against the matched random-segment control per H5(ii); the schedule-3 configuration stated with its variable count; and the weight cosine recorded, since forced sparsity is the expected mechanism rather than a defect.
- **Acceptance, added 2026-10-03**: (a) the F100 complete classical bar reported on the same rows; (b) repeats reported as mean and standard deviation, not single runs; (c) every returned sample stored, not only the lowest-energy one, so F20's multi-sample ensembling costs no further device time; (d) the train-test gap beside every win
- **Cost against the sent figure**: at the corrected sizing the block is about 4.0-4.6x the 270 s the sent hardware plan states for Experiment 5 (`docs/SPECTRA_BLOCK_RECONCILIATION.md`). After F90, about **446-597 s** of the 1,681 remain, which does not cover Experiment 3; Experiment 3 depends on the additional 7,500 s asked of QCi
- **This is an allocation DECISION, not an estimate.** About 1,084-1,235 s of 1,681 leaves 446-597 s for everything else. It stops for per-block approval with the figure quoted (Criterion H), B5 first and B4 separately.
- Depends on: **nothing outstanding.** Per-block team-lead approval was given 2026-10-05 for B5 and B4 together, with all Dirac-3 calls directed to wait for the 18:00 local window. (Corrected TWICE, and the second correction was mine to make: on 2026-10-04 this line said "reconciliation with F5", which F5's closure on 2026-10-03 had already satisfied. My replacement then said the card was BLOCKED on the off-repository result being "brought in" -- but **the configuration was already brought in on 2026-10-03** and is the bullet four lines above: schedule 3, 8 samples, relaxation schedule 2, ridge 2x the record count. `spectra_segment.FROZEN_CELLS` encodes exactly that, and so does B2's `hw_config`, which is why 82.4 s/fit anchors at all. I had turned a CITATION restriction -- those AUC figures are not evidence in this repository -- into a MISSING INPUT, which is a different thing. B4 generates its own `[HW]` numbers and never needed the off-repository ones.)

**F2b. Hardware campaign, remaining blocks B4 and B5 -- CLOSED 2026-10-03 into F90**
- **CLOSED in the 2026-10-03 refinement.** B4's line closed into F90 earlier the same day, and F90's title is "B5, then B4", so the B5 line here duplicated it. Nothing is lost: B5 runs first inside F90. The card stays in place because `test_spectra_reconciliation.py` requires every SPECTRA record to remain findable
- Phase: Experiments
- Platform: Dirac-3
- **B1 + G0b DONE** (Sprint 4, 120 QPU s). **B2 DONE** (Sprint 12, 11 fits, 906 s, A24). **B3 DONE** (Sprint 12, 12 fits, 62 s, A23 after the A22 withdrawal and matched re-run). Only B4 and B5 remain
- **B4's line here is CLOSED into F90 (2026-10-03).** Its "15 fits, ~450 s" was from the original grid, with the schedule never recorded, so the figure could not be repaired -- there is no way to tell what it was costing. F90 carries the measured cost. **B5** (QSVM sign-augmented, 12 fits, ~15 s) remains here and is cheap enough to run inside any remaining balance
- B4 overlaps **F5** (SPECTRA in-segment replication), which sits in HOLD. They are the same block from two angles and should be reconciled before either is scheduled
  **The four records are reconciled in `docs/SPECTRA_BLOCK_RECONCILIATION.md` (F93, 2026-10-02), which also records that QCi was SENT 30 fits at 91-136 variables for 270 s. The configuration choice is open and is the team lead's.**
- Neither is a submission blocker. Both are post-submission work on the current calendar
- Depends on: per-block team-lead approval (Criterion H); allocation balance
- **The billing rule is now validated far outside its anchors.** B2's first fit at 833 variables, degree 3 cost 91 metered seconds where the grid assumed ~40. `ceil(sum(runtime))` predicted it exactly (runtime sum 90.152 s, balance 2929 -> 2838). Per-sample cost 11.27 s against B3's ~0.6 s, an **18.8x** step. Use measured per-sample cost, not the original grid, for any B4 estimate


(F65 per-fit artifact write: COMPLETED in Sprint 14. Also fixed a dry run that
overwrote committed evidence. Removed from candidates per convention.)

(F77 build the Evidence Based DB, F75 the 20-paper ADR checkpoint, and F76 the
shared-vocabulary guard: MOVED to the `kimmeyh/EvidenceBasedDB` repository
2026-09-16 by the team lead. All three are that repository's work, not this
one's. F77 builds its store; F75 reviews its schema against its own papers; F76
guards ITS ADR-0004 and ADR-0005, whose live copies live there. The copies here
are frozen and carry a banner saying so. Tracked in that repository's own
backlog. Removed from candidates per convention.)

(F78 the PowerShell-to-Python conversion, F79 the retrospective gate, and F80
the open-question falsifier re-run: COMPLETED in Sprint 16. See
SPRINT_16_SUMMARY.md and CHANGELOG.md. Two findings outlived their cards and are
recorded there: F79's defect was an exemption never revoked rather than a
missing check, and the confidentiality scan reported clean on any single-line
file. Removed from candidates per convention.)

(F82 the escape-eaten class, F83 the venv parity question, F84 the environment
in the row schema, F85 the gate-report rename and F86 the QCi post-submission
package: COMPLETED in Sprint 17. F81 CLOSED by the team lead. See
SPRINT_17_SUMMARY.md and CHANGELOG.md. Removed from candidates per convention.

Four findings outlived their cards and are recorded there rather than here:

- **F83's Appendix C question resolved in the document's favor.** "Python
  3.12, Linux" is accurate AND enforced in code -- run_hardware.py and
  tune_proxy.py hard-exit on any non-POSIX platform, because the full-pair pool
  build needs fork. No submitted document needed correcting. The suite is now
  identical on both platforms; the count is not restated here, per
  `docs/VENV_PARITY.md`, which owns that evidence. Run the suite.
- **The cross-repository guard had never run in CI.** 15 of its 17 cases
  skipped on non-Windows for a PowerShell reason that stopped applying when
  F78 converted the hooks. CI is ubuntu-latest, so the boundary rule was
  enforced on one workstation and nowhere else.
- **render_all.py rebuilt the three SUBMITTED PDFs on any invocation**, and the
  first fix's override flag was used within minutes to get an unrelated test
  running. No override exists now.
- **The QPU arithmetic does not subtract**, and the reconciliation is at
  docs/QPU_RECONCILIATION.md so it is not re-derived a fourth time.)

**F36. Pandoc Lua filter: floating tables for the submission PDFs -- CLOSED 2026-09-07, FAILED**
- **VERDICT: the filter works; the problem it was built for did not exist.** The premise (preserved in the review doc, because it is wrong in an instructive way) rested on a CHARACTER-COUNT page-fill measurement, and a table-heavy page always looks short by that measure. Measured as vertical extent, every page cited below was already full: 724 / 680 / 680 / 682pt of a 792pt page, zero free space anywhere. The appendix was over its limit because it had too much content
- **Failed criterion 1** (appendix 3 pages with the filter, 4 without): 4 and 4. **Failed criterion 6** (other documents unchanged), which is worse: floating tables in a table-dense document COSTS a page, taking gate_report.pdf from 3 to 4. Criteria 2, 3, 4, 5 and 7 pass
- Filter RETAINED but UNREGISTERED at `scripts/pandoc/float-tables.lua`, opt-in through `render-pdf.ps1 -LuaFilter`, which nothing passes. `render-all.ps1` is unchanged. Do not enable it without reading `docs/reviews/f36-float-tables-outcome.md`
- **What the card actually produced, and it is worth more than the filter**: `scripts/page-fill-report.py` now measures vertical extent in points instead of counting characters, and excludes the page-number folio, which sat at the same depth on every page and so made every page report zero free space -- including a nearly empty last page, the one case the tool exists to flag. `experiments/src/test_page_fill_report.py` covers both defects and all four tests fail against the previous implementation
- **The appendix DID reach 3 pages**, by the team lead's two suggestions: set pipe-table column widths from the longest cell each column holds (every table used `|---|---|`, giving "30" and "[SIM]" the same width as a sentence; removed 9 of 20 spilled lines with no content change), and move reference material to the public repository. It has since gone back to 4 with the B.1 compound-falsification statement, tracked as F38
- **Process lesson**: the card's dry run could not have failed. Deleting five tables removes their content AND their space, so the document was always going to shrink. It never distinguished "tables take room" from "tables waste room". A check that cannot fail is not evidence

The original card body is pruned as shipped. Its premise, the seven
acceptance criteria and the full failure analysis are preserved in
docs/reviews/f36-float-tables-outcome.md.

(F38 appendix to 3 pages AND proposal to 6: COMPLETED in Sprint 12, merged via PR #75.
proposal 6 of 6, appendix 3 of 3, team profile 1 of 1. Removed from candidates per convention.)

(F39 Evidence Based Database investigation and design: COMPLETED in Sprint 14 as
ADR-0014, ACCEPTED with early-innovation status and a 20-paper checkpoint.
Building is a SEPARATE card and is not authorised by the ADR. Removed per
convention; F75 actions the checkpoint.)

### Phase 2 (pre-notification preparation and the committed experiments)

Added in the 2026-10-03 refinement, which merged `CHECKLIST-Phase2-pre.md` into
`CHECKLIST-Phase2.md` and carded every Phase 2 item that had no card. Source:
the team lead's Phase 2 planning documents (held outside this repository;
consulted for planning, not cited as evidence). Priority order follows the
team lead's 2026-10-03 decision that field advancement leads if it conflicts
with the track outcome: F90 and the cards that make it readable first, then the
preregistration framework that gates all reporting, then the zero-cost screens,
then the builds for the committed experiments. Estimates are `[no-history]`.

(F123 phase separation, F124 SPECTRA lever research, F125 close-out hook ref,
F17 Dirac-3 emulator and F20 soft votes: COMPLETED in Sprint 22, merged via
PR #159 (main PR #166). See SPRINT_22_SUMMARY.md and CHANGELOG.md. Removed
from candidates per convention. F124's approved ranked list,
`docs/phase2/SPECTRA_IMPROVEMENT_RESEARCH.md`, now gates every device card
below: rank 1, leaf regularization, is tested first. F17's follow-up is F126;
F123's layout is superseded by F127.)

(F141 Dirac-3S client support, F142 the Dirac-3S verify block, F144 the
proxy twin of B2, F145 seeded pool builds, F147 the evidence-library query
tool, F126 the sparsity rule and F105 the IEEE-CIS harness: COMPLETED in
Sprint 26, merged via PR #21 (main PR #31). F142 spent 86.0 Dirac-3S seconds
over 5 fits; on B4 Dirac-3S returned the reference optimum. F126's rule
failed; F105 reports no score until F102 names its entry. See
SPRINT_26_PLAN.md, SPRINT_26_VALIDATION.md, SPRINT_26_RETROSPECTIVE.md and
CHANGELOG.md. Their gates on other cards are marked spent below (Pass 1,
2026-10-18). Removed from candidates per convention.)

(F149 the F142 runner tests, F104 the resolution gate, F112 Experiment 1's
intervals, F130 the lever screens, F103 the Tier 1 known-answer check, F109
the six-dataset ladder, F6 the gate-based arm analysis, F106 the
dequantization check, F107 the shot budget and F108 the ceiling harness:
COMPLETED in Sprint 27, merged via PR #32 (main PR #45), zero metered
seconds. Selected 2026-10-18 with an F146 update; the QCi questions were
sent 2026-10-18. F102's section 7 also shipped; the card stays open.
Findings that bind other cards are recorded on them: F150 (F103's dense
substrate), F151 (F130's ULB comparator), F114 (F108 validated no method),
F116 (F106 inconclusive). See SPRINT_27_PLAN.md, SPRINT_27_VALIDATION.md,
SPRINT_27_RETROSPECTIVE.md and CHANGELOG.md. Removed from candidates per
convention (Pass 1, 2026-10-19).)

(F154 outcome records, F151 the ULB HGB comparator, F152 Experiment 2,
F153 Experiment 3's proxy design, F111 the Loke harness, F110 Experiment
6's scaling, F162 the in-pocket head-to-head and F115 integer cost
scaling: COMPLETED in Sprint 28, merged via PR #46 (main PR #62), zero
metered seconds. F13's skeleton and F146's update also shipped; both
cards stay open. F114 and F150 stayed blocked. Findings that bind other
cards are recorded on them: F25 and F160 (F153's design fails), F159
(F110's serial build is the cost), F161 (F162 justified no device block),
F114 and F156 (calibration does not move the estimate), F157 (F151's
stable HGB, F154's outcome rule). See SPRINT_28_PLAN.md,
SPRINT_28_VALIDATION.md, SPRINT_28_RETROSPECTIVE.md and CHANGELOG.md.
Removed from candidates per convention (Pass 1, 2026-10-25).)

(F165 a resumed run keeps its id, F159 the parallel pool build, F164
Phase 2 figures resolve, F156 the Henze-Penrose bound, F160 Experiment
3's room on IEEE-CIS, F166 F157 part 1 on ULB, F158 fraud types and F167
the PoC plan draft: COMPLETED in Sprint 29, merged via PR #63 (main PR
#73), zero metered seconds. Findings that bind other cards are recorded
on them: F114 and F169 (F156 fails), F25 (F160 reopens its design on
IEEE-CIS), F157 (F166 is part 1), F170 and F171 (F158 step 3), F13
(F167's draft), F168 (F165 spent). F172 and F173 carded by the
retrospective. See SPRINT_29_PLAN.md, SPRINT_29_VALIDATION.md,
SPRINT_29_DECISIONS.md, SPRINT_29_RETROSPECTIVE.md and CHANGELOG.md.
Removed from candidates per convention (Pass 1, 2026-10-30).)

(F168 agent work survives a usage limit, F173 the commit's own task
timer, F175 timers stop counting breaks, F172 the Sprint 29 review's
coverage gaps, F176 below greedy on IEEE-CIS, F169 the second ceiling
estimator, F170 ULB's missed frauds' neighbors, F171 F158 step 3 on
IEEE-CIS and F174 F157 part 2 on IEEE-CIS: COMPLETED in Sprint 30,
merged via PR #74 (main PR #91), zero metered seconds. Added during the
sprint: CI's red proofs moved to a full job on ready for review (F177's
CI part, Task L). Findings that bind other cards are recorded on them:
F114 (F169 passes; unblocked), F157 (F174 is part 2), F25 (F176).
F177, F178, F179 and F180 carded during the sprint. See
SPRINT_30_PLAN.md, SPRINT_30_VALIDATION.md, SPRINT_30_DECISIONS.md,
SPRINT_30_RETROSPECTIVE.md and CHANGELOG.md. Removed from candidates per
convention (Pass 1, 2026-11-04).)

**Selected for Sprint 31** (team lead, 2026-11-04, D1 option 4; D2-D6 answered the same day): F180,
F177, F178, F179, F114, F155, F157, F150, F95, F121 and F13, with F13
last ("after other results are known"). Each part still open is a
decision in `docs/sprints/SPRINT_31_DECISIONS.md` (D2-D6). Plan:
`docs/sprints/SPRINT_31_PLAN.md` (draft).

**F146. Dirac-3 and Dirac-3S understandings, suggested improvements and QCi questions: keep current (~0.5h per update, zero metered) Priority HOLD (permanent)**
- Phase: Phase 2, standing (added 2026-10-13 by the team lead during Sprint 25 Manual Validation)
- Platform: N/A (document)
- The living document is `docs/phase2/DIRAC_UNDERSTANDINGS.md`. First draft 2026-10-13: what we understand about each device, each item labeled Measured, QCi states, Independent, Inferred or Unverified; nine suggested improvements for Dirac-3S; two questions pending since 2026-09-25 and twelve not yet sent. It owns the QCi question list
- **Permanent. It never closes.** It re-opens for an update when any of these happens: QCi answers a question or sends new material; QCi publishes a new guide, client release or benchmark; F141 bumps the clients; F142's first Dirac-3S fit returns; a sprint finds a fact that changes an item. Each update adds a revision-log row
- Sending anything to QCi is the team lead's action; anything sent is filed in the gitignored `docs/qci_package/`
- Acceptance per update: the triggering fact placed under the right label with its source; the revision log updated
- Depends on: the triggers above
- **Sprint 27 Task L (2026-10-18)**: a send-ready draft of P1-P2 (follow-up) and A1-A12 is at `docs/qci_package/F146_QCI_QUESTIONS_DRAFT.md` (gitignored, not sent). None dropped: F142 bears on A3, A6 and A12 but answers none, so those three now cite the measurement. Its message body passes `scripts/outward_readability.py`; the two hits are in the notes marked for deletion. Sending is the team lead's action
- **Sent 2026-10-18** by the team lead (filed in `docs/qci_package/`); section 4 of `DIRAC_UNDERSTANDINGS.md` records it. The next F146 update is QCi's answer
- **Answered 2026-10-20** (update 2026-10-21): QCi answered A1-A12 and P2; P1 was referred to the eqc-models contact and stays open. Recorded in section 4 of `DIRAC_UNDERSTANDINGS.md`. Consequences for other cards are on F143 (A1), F25 (A4), F30 (A5) and F153 (A7)
- **P1 answered 2026-10-21** by QCi's eqc-models contact, and closed (recorded 2026-10-22, `DIRAC_UNDERSTANDINGS.md` section 4). No question is pending (corrected 2026-10-25, Sprint 29 planning: the line above still read "stays open")

**F143. telecom_churn with all 18 features (987 variables) on Dirac-3S (~1h + at least 450 metered s, unmeasured at 987) Priority HOLD**
- Phase: Phase 2 (added 2026-10-13 by F139, Sprint 25)
- Platform: SPECTRA, Dirac-3S
- The one sized case Dirac-3S's larger ceiling unlocks: telecom_churn at schedule 3 with all 18 features, 987 variables in the full-pair build, 5 seeds. B4 ran it on Dirac-3 at 816 variables with `age` dropped, and its in-segment edges were negative; this adds the dropped feature. At least 450 s: Dirac-3 cost 84-90 s per fit at 816 variables, and the rate at 987 is unmeasured
- **HOLD until QCi confirms the cloud `dirac-3s` queue exceeds 949 variables.** The base module's ceiling is 949; only the expansion configuration reaches 9,980, and no source says which serves the cloud (F138). The question (A1) was sent 2026-10-18; no answer yet (Pass 1, 2026-10-19). **Answered 2026-10-20: base unit plus expansion module serves the cloud queue**, whose guide ceiling is 9,980. QCi named the configuration, not a variable figure, so whether that meets this hold is the team lead's call (Pass 2). **Team lead, 2026-10-22 (Sprint 28 Decision 7, option 2): the hold stays.** The expansion unit is installed but not fully implemented, so the cloud queue is still, temporarily, at 949 variables. Re-run at 987 when it moves to 9,980. F155 is the probe that detects the change
- **Re-price at refinement (2026-10-16, Sprint 26 IMP-5)**: the "at least 450 s" is a Dirac-3 figure. `qpu_cost_model.quote(987, 8)` quotes from F142's Dirac-3S fits and flags 987 as above its largest anchor, so its high end is a floor, not a bound
- Depends on: QCi's answer; per-block approval (Criterion H) (corrected 2026-10-18, Pass 1: F141 and F142's measured rate are spent, both shipped in Sprint 26)
- **2026-11-05 (Sprint 31, F155): the hold condition is met.** The cloud `dirac-3s` queue accepted a 1,350-variable continuous job, all 1,350 entries returned (`experiments/phase2/results/f155_variable_ceiling.json`). 987 is under that size. The probe shows a job that size is accepted, not that a 987-variable pool solves well: F155's weights came back near flat. Priority to be set at refinement

(F138 Dirac-3S research, F139 the re-run review, F113 the oracle-gap test,
F29 sample-size insensitivity and F94 Experiment 3's classical controls:
COMPLETED in Sprint 25, merged via PR #12 (main PR #20). F102's first draft
also shipped; the card stays open as a living draft. See
SPRINT_25_PLAN.md, SPRINT_25_VALIDATION.md, SPRINT_25_RETROSPECTIVE.md and
CHANGELOG.md. Findings that bind other cards are recorded on them: F141-F145
carded by F139 and F29; F25 carries F94's design findings; F129 closed on
F139's recommendation. Removed from candidates per convention.)

(F127 Phase 2's own repository, Phase 1 restored as filed and archived:
COMPLETED. Steps (2)-(5) ran in Sprint 23 and here; steps (6) and (7) ran in
the Phase 1 repository, verified read-only 2026-10-13: the `as-filed` tag is
at 4aa17d2 and the repository is archived. Removed from candidates per
convention.)

(F131 hermetic CI-status test, F136 task start times, F132 this repository's
boundary, F134 pre-commit blocks without patterns, F133 job_id on device rows,
F135 complete decision options, F128 the leaf-regularization sweep and F137
the pypdf bump: COMPLETED in Sprint 24, merged via PR #2 (main PR #11). See
SPRINT_24_PLAN.md, SPRINT_24_RETROSPECTIVE.md and CHANGELOG.md. Selected
2026-10-09 (D1 option 1; D5 added F137). D4 made `develop` the GitHub
default branch; it was briefly `main` on 2026-10-10 and is `develop` again.
**F128 fired its premise falsifier**: no `min_samples_leaf` value beats HGB
with a CI excluding zero on any dataset (`docs/phase2/SPECTRA_IMPROVEMENT_RESEARCH.md`
section 6). Removed from candidates per convention.)

(F140 CI on release PRs into `main`: CANCELED 2026-10-13 by the team lead
at Sprint 25 selection. "None of the 100 PR's so far ... has never been a
match", so CI on the release PR would duplicate the `develop` run for no
value. Removed from candidates.)

(F129 rank-1 device pilot, energy_steel with leaf regularization on Dirac-3: CLOSED 2026-10-13 by the team lead at Sprint 25 Manual Validation, on F139's recommendation (`docs/phase2/F139_RERUN_REVIEW.md`). F142's B4 verify twin answers its fidelity question on Dirac-3S, on a resolvable Hamiltonian with Dirac-3 rows already on record. No metered seconds were spent on it. Removed from candidates; F121's hold condition, which waited for it, needs a new one at the next refinement.)

**F102. Phase 2 preregistration framework (~3h [no-history], zero metered) Priority 30**
- **Pass 1 (2026-10-25)**: Sprint 28 wrote section 6 entries for Experiments 2, 3, 4 and 6 (F152, F153, F111, F110), and for F154 and F162. Experiment 5 has no entry; its transfer half is F121, on HOLD. The filing date is still open (team lead)
- **Sprint 27 Task C (2026-10-18, #35)**: section 7's items done or dated in `experiments/phase2/PREREGISTRATION_DRAFT.md`. arXiv:2604.18837 re-read: nested CV, Wilcoxon and the 0.0625 floor at 5 pairs are the paper's; the bootstrap interval, family-wide Bonferroni and normalized AUPRC are this project's (the paper reports no interval and applies Bonferroni once). New sections 2a (one Bonferroni family per experiment; seeds needed per family size) and 2b (equivalence against a margin, default 0.005 AUPRC). Section 5 recomputed by code (`f102_downsized_pair.json`): seed 42's 855 + 278 reproduces; 88-94% of pocket positives kept; the interval 3-7% wider, not "about 4%" on every seed. Experiment 1's entry (F112) written before its intervals. Still open: entries for Experiments 2-6 as their cards are selected; the filing date (team lead)
- **Sprint 26 (team lead, Decision 1 option 1, 2026-10-14)**: not selected. F142 and F144 each write their own section 6 entry in the Phase 2 draft before their runs; this card stays open for the framework
- Phase: Phase 2 preparation (the checklist's Deliverable)
- Platform: docs
- A per-experiment preregistration template and one reporting standard for every Phase 2 result: nested CV, Wilcoxon signed-rank, Bonferroni correction and multi-seed sensitivity (arXiv:2604.18837); AUPRC normalized by its closed-form floor with AUROC beside it; the F104 resolution screen as a gate before any metered block; and the two meanings of "order 3" stated (weak learners over feature triples in pool construction, against a QUBO that is quadratic on the device)
- This enables: every Phase 2 card below reporting honestly. This prevents: results seen before the protocol is fixed
- **MUST SPECIFY THE IN-SEGMENT CONTROL AS A DOWNSIZED MATCHED PAIR (team lead, 2026-10-05).** Phase 1's H5(ii) control draws a size-and-rate-matched segment from the complement, and on energy_steel that is arithmetically impossible: the pocket holds 918-950 of the test fold's positives while the complement holds 832-864, on all five seeds (`docs/SPECTRA_CONTROL_FEASIBILITY.md`). Phase 2 fixes this by **downsizing BOTH sides** to what the complement supports, keeping size and rate matched on each: 855 positives + 278 negatives per side on seed 42, retaining 88-94% of the pocket's positives, with the AUC interval widening by only about 4%. Verified feasible on all five seeds.
  - **Both sides then become random draws, so the comparison is REPEATED** (about 20 draws) and reported as a mean with its spread. Phase 1 draws the control once against a fixed segment, which cannot distinguish a real in-segment effect from one that depends on which rows were drawn. Repeating costs nothing: it is classical computation over device output already paid for.
  - **Why this is specification and not a retrofit.** `experiments/PREREGISTRATION.md` stays FROZEN and is NOT amended: section 11 forbids an amendment that changes a gate's pass/fail criterion, and H5(ii)'s control IS that criterion, so the change would be a reported DEVIATION. Phase 1 reports energy_steel `unscoreable` instead, which the gate table already has a column for. The design is motivated by a STRUCTURAL property of the dataset (the pocket's share of positives), not tuned against any result, and Phase 2's SPECTRA data does not exist yet. This paragraph exists so a reviewer sees the distinction was made deliberately rather than discovered later.
  - A Phase 2 preregistration binds only from its filing (a November date, to be set), so this file may be revised freely until then.
- **A living draft (team lead, 2026-10-13, Sprint 25 selection)**: this card creates a DRAFT that is updated across several sprints until Phase 2 is approved and a filing date is set. Sprint 25 delivers the first draft, not the filed document. **First draft committed 2026-10-13: `experiments/phase2/PREREGISTRATION_DRAFT.md`**; its section 7 lists what remains before filing. The card stays open
- Acceptance: the template committed; each later experiment card names its preregistration file before it runs. `experiments/PREREGISTRATION.md` stays FROZEN; this is a new document. The downsized-matched-pair control and the repeated-draw reporting are both written into it, with the feasibility arithmetic and the reason it is not a Phase 1 amendment
- Depends on: nothing

**F150. SPECTRA substrates rebuilt to the authors' construction, and the F103 check repeated (~30m request draft; rebuild ~2h after the reply [no-history], zero metered) Priority 41, blocked**
- Phase: Phase 2 preparation (cross-domain study; added 2026-10-18 by the team lead with Sprint 27 Decision 1)
- Platform: SPECTRA
- Sprint 27's F103 rebuilds the paper's sparse pocket and dense substrate from its description. This card builds the same two substrates as the authors construct them, as close a duplicate as their details allow, and repeats the four published values: JOINT minus GA2M +0.37 and +0.00, HGB minus GAM +0.15, joint ratio 9.9
- Acceptance: each value against the paper's with F103's tolerances; each difference from F103's rebuild named and explained
- Depends on: the authors sending how the substrates are constructed (the construction request in `CHECKLIST-Phase2.md`, still open); F103 spent (corrected 2026-10-19, Pass 1: shipped in Sprint 27)

**F155. Dirac-3S variable-ceiling probe: does the cloud queue accept 950 variables? (~30m, about 4 metered s) Priority 60**
- **2026-11-05 (Sprint 31 Task I, D9 option 1): run.** Accepted at 1,350 variables, all entries returned, 6.0 metered s against a 4 s floor quote (`experiments/phase2/results/f155_variable_ceiling.json`). Leaves the backlog at Sprint 31 close-out
- Phase: Phase 2 (added 2026-10-22 by the team lead, Sprint 28 Decision 7)
- Platform: Dirac-3S
- The team lead: the expansion unit is installed but not fully implemented, so the cloud `dirac-3s` queue is still, temporarily, at 949 variables. One minimal job at **950** variables (949 is inside both limits and cannot tell them apart): one sample, schedule 2. Accepted means the limit is now above 949 and F143 can come off HOLD; rejected means it is still 949
- Cost: `qpu_cost_model.quote(950, 1)` gives 3-4 s from three Dirac-3S anchors; 950 is above the largest anchor (833), so 4 s is a floor, not a bound. Whether a rejected job is billed is **unverified**, and whether the client rejects it before submission is unverified
- Depends on: per-block approval (Criterion H). Re-run when QCi says the expansion is live, or at a cadence the team lead sets
- **2026-10-22 (Sprint 28 Task K): 950 may no longer separate the limits.** QCi's reply of 2026-10-21 raised the integer solver to 954 levels on both devices, with Dirac-3S to 9,980 "in the coming weeks" (`docs/phase2/DIRAC_UNDERSTANDINGS.md` section 4). If the continuous ceiling moved with it (inferred, unverified), a 950-variable job is accepted before the expansion is live. The probe size is a Manual Validation decision: 955 (just above 954) or 987 (F143's own size, which answers whether F143 fits under any intermediate limit). `qpu_cost_model.quote` gives 3-4 s for each, a floor above the 833 anchor. Not run
- **2026-10-23 (team lead, Sprint 28 Manual Validation, DV1): the probe is 1,300 variables**, above both 954 and F143's 987, so an accepted job shows the queue has moved past both. `qpu_cost_model.quote(1300, 1)` gives 4 s from one Dirac-3S anchor (833, the only one within 2x); above that anchor, 4 s is a floor, not a bound. The run still needs its own per-block approval (Criterion H)
- **2026-10-23 (Sprint 28 D4, storage prevention)**: the probe runs from a new runner under `experiments/phase2/src`, through `device_store.saving` with a `hamiltonian` declaration, so the full response and the problem's arrays are stored. `probe_variable_ceiling.py` is a frozen Phase 1 module and is not reused for it (`test_device_store_required.py`)

**F157. Best achievable result per algorithm per dataset, every metric, one document each (~epic; size at refinement [no-history], proxy and classical first) Priority 30**
- Phase: Phase 2 (added 2026-10-23 by the team lead, Sprint 28 Manual Validation, after F151 and F152)
- Platform: ULB, IEEE-CIS, then the other datasets already used
- For each algorithm (HGB, LightGBM, XGBoost, CatBoost, logistic regression, SVM, CVQBoost proxy and device, QSVM, QNN), find the best settings under one protocol per dataset, and record the alternatives tried and why each was kept or dropped. Every result reports TP, FP, TN and FN at the 0.5% alert budget and at validation-chosen thresholds, precision, recall, specificity, F1, MCC, balanced accuracy, AUC-PR and ROC-AUC, each with its interval over seeds
- Output: one document per dataset per algorithm under `docs/phase2/algorithms/`, plus one comparison page per dataset that references them (numbers live in the result files, per the official-record rule)
- Split at refinement into one card per dataset; device lanes need per-block approval (Criterion H)
- Depends on: F102 for reporting; the F154 outcome rule supplies the confusion counts (corrected 2026-10-25, Pass 1: F154 is spent, shipped in Sprint 28 as a standing rule in CLAUDE.md)
- **Pass 1 (2026-10-30)**: part 1, ULB, shipped as F166 in Sprint 29 (`docs/phase2/algorithms/`, pages from `scripts/f166_docs.py`). Part 2, IEEE-CIS, carded at Pass 2 as F174
- **Pass 1 (2026-11-04)**: part 2 shipped as F174 in Sprint 30 (`docs/phase2/algorithms/IEEE_COMPARISON.md`, 10 seeds; XGBoost, SVM and logistic regression are deterministic on fixed months, so their seeds repeat one result). Remaining: device lanes and QNN, and the other datasets already used, each a card when selected

**F161. B4 re-run on Dirac-3S, all ten cells (~60m plus device time, about 210-310 metered s) Priority 90, low; decide near the end of Phase 2**
- Phase: Phase 2, late (added 2026-10-23 by the team lead, Sprint 28 Phase 6)
- Platform: Dirac-3S
- Scope: Phase 1's B4 block (CVQBoost on SPECTRA, telecom_churn and oilgas_gasturbine, seeds 42-46, label `target`, covariates plus phases, in-segment edge against the matched random control) repeated on Dirac-3S. F142 re-ran two B4 oilgas fits on Dirac-3S; this is the full ten. Pools are built seeded (`qubo_proxy.seeded_weak_params`, F145), so they are new pools and not byte-identical to Phase 1's unseeded ones; the comparison is lane against lane, not fit against fit. Every per-row score and every device sample is stored (F154 rule; the Sprint 28 storage prevention)
- Run condition (team lead, 2026-10-23), both parts: (1) near the end of Phase 2 it is judged valuable, OR different results are expected from Dirac-3S than from Dirac-3 (decided then); AND (2) the allocation balance is above 1,500 QPU seconds
- Cost: `qpu_cost_model.quote(560 or 816, 8, relaxation_schedule=2)` gives 21-31 s per fit from three Dirac-3S anchors, so about 210-310 s for ten fits; F142's two B4 fits on Dirac-3S measured 22.0 and 21.0 s. Re-quote at the time
- Depends on: per-block approval (Criterion H); the run condition above
- **Pass 1 (2026-10-25)**: F162 (Sprint 28) found the proxy not reliably above HGB or XGBoost inside the pocket on any cell, and its card said a null justifies no device block (`docs/phase2/F162_IN_POCKET.md`). Run condition (1) is judged against that result

**F114. Ceiling estimates on real data: learning-curve floor and label noise (~60m to validate one method, +90m real data if it passes [no-history], zero metered) Priority 16**
- **Pass 2 (2026-11-04)**: priority 140 to 16. 140 was its blocked priority; unblocked, it is the payoff of the F169-F171 ceiling work, with 90m left
- **Pass 1 (2026-11-04): unblocked.** F169 (Sprint 30 Task F) is the first method to pass F108's rule on the main arm: LightGBM with 4,095 bins on 5 of 5 seeds, HGB without early stopping on 4 of 5. LightGBM's reference-arm passes are degenerate, so the method rests on the main and flip arms (`docs/phase2/F169_PLUGIN_BINS.md`). The 60m "validate one method" step is spent; the 90m real-data step is what remains. F170 found ULB's frauds missed by every model have mostly legitimate neighbors (consistent with an information limit); F171 did not show a smaller missed group on IEEE-CIS (4 families against ULB's 12). Both are read beside this card's result
- Phase: Phase 2 preparation (ceiling methodology)
- Platform: ULB, IEEE-CIS
- Fit `a*N^(-b) + c` against N_positives within a fixed time window; confident learning with the diagonal-dominance condition tested and reported when it fails. Report intervals, not points
- Depends on: a ceiling method that passes F108's harness (corrected 2026-10-19, Pass 1: F108 shipped in Sprint 27 and validated none, so this card is blocked, not ready). F156 is the candidate (corrected 2026-10-25, Pass 1: the calibrated plug-in failed in Sprint 28). **2026-10-28: F156 failed (Sprint 29 Task D); F169 is the next candidate (team lead, Sprint 29 Decision D1 option 2)**
- **2026-10-18 (Sprint 27 Task K)**: F108 validated none of the four methods on its main arm, including this card's `a*N^(-b) + c` floor (1 of 5 seeds on error; unstable on AUPRC). Under F108's rule this card has no method to run on real data until one passes F108's harness
- **2026-10-22 (Sprint 28 Task G)**: an isotonic-calibrated plug-in on F151's stable HGB, under a dated F108 amendment, recovers 2 of 5 seeds on the main arm, the same as F108's default plug-in; calibration does not move the estimate. **Still blocked.** The next candidate is a different estimator, not a re-scaled one (`docs/phase2/F114_CALIBRATED_PLUGIN.md`)

**F13. Phase 2 PoC sprint planning (~75m timebox for the skeleton) Priority 180**
- **2026-10-22 (Sprint 28 Task J, #56)**: skeleton written, `docs/phase2/PHASE2_POC_PLAN.md`. Dates now sourced: program roadmap page, team lead's screenshot of 2026-10-22 (PoC 17 Nov 2026 - 28 Feb 2027; Review and Close 1 Mar - 30 Apr 2027). The content after notification stays open
- Phase: Phase 2 (Nov 17 - Feb 28, if selected)
- Platform: All
- Braket hardware validation, IEEE-CIS at scale, calibrated deployment per the routing architecture; plan built on acceptance
- **OFF HOLD 2026-10-05 (team lead): waiting is no longer a HOLD reason for Phase 2 work.** Scored 180, last in the numeric set, because the *content* of the plan still depends on finalist notification --- but the card is now schedulable rather than parked, and much of the preparation it names is already carded (F102 preregistration framework, F6 Braket, F105 IEEE-CIS at scale, F118-F120 deployment)
- Depends on: nothing to start the skeleton; the dataset-specific content needs finalist notification
- **Pass 1 (2026-10-30)**: F167 (Sprint 29) wrote the full plan on labeled assumptions, `docs/phase2/PHASE2_POC_PLAN_DRAFT.md`. On notification this card replaces those assumptions with the brief's terms; the skeleton is unchanged

**F177. The full suite in about 5 minutes, with no guard lost (~240m [no-history], zero metered) Priority 10**
- Phase: tooling (added 2026-11-01 at Sprint 30 Phase 5, team lead: "full suite testing needs to be effective yet as efficient as reasonably possible. 40 minutes is way too long as it should be taking about 5 minutes"). For Sprint 31
- Platform: N/A (tests, CI and process docs)
- Measured 2026-11-01 (one local run on the Sprint 30 final HEAD, `--durations=0 --junitxml`, 32 cores, run serially): 48.9 minutes wall, 48.7 summed per test
  - **Red proofs are 72% of the time (34.9 min).** Tests named as proofs (`*_can_fail` and similar) run `injection.assert_can_fail`, which starts a new pytest process per mutation. A nested start costs about 3 s before the target runs (pytest start-up, then `conftest.py`'s evidence check: list, dirty check and SHA-256 of the 277 tracked evidence files, at start and again at finish, about 0.7 s). Several targets are slow themselves: `test_outcome_record_required`'s targets parse every result file, so each of its proofs takes 16-70 s. Proofs not named as proofs (`_proof(...)` in `test_outcome_record_required`) add about 2 more minutes
  - **The rest is 13.8 min.** Tests under 2 s each take 2.4 min in total. 13 tests of 10 s or more take 7.9 min, led by real-pipeline runs: `test_ieee_runner_correctness` shuffled-label control (95 s), `test_run_hardware_b5` dry run (78 s), two `test_render_all` renders (45 s each), `test_integer_probe` (29 s and 19 s), `test_f160_room_ieee` (23 s), F159's pool equality (15 s)
  - **By file**: `test_outcome_record_required` 5.2 min, `test_backfill_outcomes` 3.3, `test_f166_ulb_algorithms` 3.3, `test_f159_parallel_pool` 2.5, `test_f160_room_ieee` 2.2; the top 10 files are 52% of the time
  - Only one file carries the `slow` marker, so `-m "not slow"` removes almost nothing. pytest-xdist is not installed
- Levers, each to be measured, with what it gives up:
  1. **Run a red proof when its guard or target changes, not every run.** A proof shows a guard CAN fail; it needs re-running when the guard, its test or its mutated file changes. Mark proofs `redproof`; the everyday full suite runs the proofs whose files the branch's diff against `origin/develop` touches; CI and Phase 5 run all. Gives up: a guard weakened by a change in a file its proof does not name is caught at Phase 5 or CI, not at once. Saves up to about 35 min per local run
  2. **Run the non-proof tests in parallel** (pytest-xdist, 32 cores). Proofs must stay serial and alone: they edit real source files, and a parallel test reading the same file sees the mutation (the two Sprint 30 injection-restore failures, under concurrent runs). Gives up nothing if the parallel tests are safe; each test that writes the tree or uses git must be checked first. A new declared dependency
  3. **Make each nested run cheap.** Skip `conftest.py`'s evidence hash in a nested run (the outer session already checks it, so the guard is kept), and give slow targets a cheap form (for example, parse result files once per session, not per test). Saves the per-start cost on every proof, including at Phase 5 and in CI
  4. **Mark the real-pipeline tests `slow`** (the 13 above that are not proofs) and run them in CI and at Phase 5. Gives up: a pipeline break found at Phase 5 or CI, not locally. About 6 min
  5. **Combine and remove duplicates.** The two `test_render_all` tests each render the package (one shared render saves about 45 s); the six exempt-list proofs in `test_outcome_record_required` all target one node; each file's proofs to be checked for two mutations of one term
- Target: the everyday full suite under about 5 minutes; the complete suite (every proof and slow test) at Phase 5 and in CI, made as short as levers 2, 3 and 5 allow. CI stays inside its 20-minute limit
- Acceptance: a tracked timing report (`scripts/suite_times.py`, from `--junitxml`) so the before and after are reproducible; each lever measured; no guard removed without its replacement named; every changed guard proven red; `SPRINT_CHECKLIST.md` and `SPRINT_EXECUTION_WORKFLOW.md` say which suite runs when
- Depends on: nothing. Informs every sprint's Phase 4 and Phase 5 time. F180's analysis (Sprint 31) comes first and may change which levers are taken
- **Sprint 30 Task L (2026-11-01, #86, team lead D9)**: the CI part is taken in Sprint 30: the red proofs left the per-push CI job and run in a full job on ready for review. Levers 1-5 for the local full suite stay with this card for Sprint 31

**F178. Three learning documents, versioned and updated every sprint (~180m first versions [no-history], then ~30-60m per sprint, zero metered) Priority 12, ONGOING**
- Phase: knowledge record (added 2026-11-01 by the team lead, Sprint 30 Manual Validation)
- Platform: docs
- Goal: a reader can come to this repository and learn what we have learned; we record our knowledge over time; it is a faster resource when the work continues. Aim: any advantage, quantum or classical, for credit card fraud detection (more true positives, fewer false negatives)
- **Doc 1**, "ML QML and QC Understandings about Quantum Advantage - Laymen terms.md": 10th-grade level, for readers familiar with math, science, physics, computer science, ML and QC but expert in none. Appendices: definitions, acronyms, Quantum Computing, Machine Learning, Quantum Machine Learning. Each acronym is spelled out at its first use, is in the acronym appendix, and links to it at every use. Each technical term links to its appendix entry. Examples use credit card fraud ML first, other ML or QC where needed
- **Doc 2**, "ML QML and QC Understandings about Quantum Advantage - ML Expert.md": for readers with undergraduate-or-above or professional ML and data-science experience. Links to Doc 1 for acronyms, terms and phrases; its own appendices only for what Doc 1 does not have
- **Doc 3**, "ML QML and QC Understandings about Quantum Advantage - QC Expert.md": for readers with undergraduate-or-above or professional QC experience, not necessarily ML or QML. Links to Doc 1, and to Doc 2 for what Doc 2 has; its own appendices only for the rest
- Content, in each document at its reader's level: what we have learned about quantum computing; about machine learning; about quantum machine learning (what we know for sure, potential algorithms, potential experiments that would show what QML can do); about gaining quantum advantage on quantum computers; about credit card fraud and fraud in general (what it is, known patterns, the data needed to find it, how companies use ML against it and what matters to them); experiments planned that could move us toward an advantage; experiments not yet planned that could give learning or an advantage. Every dataset, model and hardware platform tested is covered. Everything learned in Phase 1 and Phase 2 is somewhere in the documents
- **Evidence tiers**: what our experiments proved or nearly proved is stated above, and separately from, what outside research says. Each experimental claim names its result file or document; each outside claim names its source (EvidenceBasedDB, read-only via `scripts/edb_query.py`, for papers and stored copies)
- **Versioning**: each sprint's update is a new version number in the document, with a dated change list; git keeps every version. Updated at the step before Manual Validation every sprint, in parallel with the PR reviews and the full suite
- Example content named by the team lead: `docs/spikes/F118_WHAT_THE_STORE_SAYS.md` in the EvidenceBasedDB repository (`D:\Data\Harold\github\EvidenceBasedDB`; the store and papers are under `D:\Data\Harold\EvidenceBasedDB`). It is generated by that repository's `scripts/f118_themes.py`. Its form, read 2026-11-02: a bottom line first; every count dated as a snapshot with the command that refreshes it; outside claims graded (HIGH, LOW) and named by store entry; this repository's own results (Phase 1 and 2 nulls, F176) stated beside them; the next steps ranked by cost and decisiveness
- Open to the agent team's feedback on format, content, sections, relative value and research avenues, collected at each retrospective ("include definitions of ...", "needs an index section covering ...")
- Acceptance (first version): the three documents exist with version 1.0 and a change list; each acronym and linked term resolves to an appendix anchor (a test fails a broken link or an acronym used before it is spelled out); each experimental claim names a tracked result file or document (the same resolution check as `test_phase2_figures_resolve.py`); `SPRINT_CHECKLIST.md` Phase 5 has the update step
- Depends on: nothing. Informs: every sprint's Phase 5; the PoC plan

**F180. Deep analysis of all testing: effective, as efficient and as quick as reasonably possible (~180m [no-history], zero metered) Priority 9**
- Phase: tooling and process (added 2026-11-04 by the team lead after Sprint 30's retrospective improvements: "backlog deep analysis of all testing for next sprint - effective while as efficient as reasonably possible and as quickly as reasonably possible"). For Sprint 31, before F177's levers are chosen
- Platform: N/A (tests, hooks, CI and process docs)
- Why, measured in Sprint 30 (team lead, 2026-11-04: from an improvement's approval, the time should be its development time plus about 15 minutes; it was about 87 minutes from the D10 answer to `gh pr ready`):
  - Local runs dominate: Task N's eight non-proof test files took 13:18 and its five proofs 17:41; Task M's four proofs took 41 minutes and four more 1:43; CI's push job runs the whole non-proof suite in 3:08 (0fc2004). The local slowness is not explained
  - Steps ran one after another: write, local tests, local proofs, commit, review, fix, CI. The review (14 minutes, uncapped brief), the tests and CI could overlap
  - Effectiveness gaps still reach review: PR 74's review found 9 untested refusals and states, after the per-term rule (Sprint 28 IMP-5, Sprint 29 IMP-1); one proof targeted a line that had moved (the injection refused, as designed); one Sprint 30 full-suite failure was never identified
- Scope: every test and guard in `experiments/src/`, the hooks and CI, and the order the sprint process runs them in
  1. **Inventory**: per test file, what it guards, its kind (unit, guard, red proof, real pipeline, document check), its local and CI time, where it runs (local, push job, full job, Phase 5) and the last time it caught a real defect (from git history and the retrospectives)
  2. **Effectiveness**: guards that cannot fail or duplicate another; defect classes found by reviews in Sprints 28-30 that no test caught, and the cheapest test that would have; proofs that go red for an unrelated reason
  3. **Efficiency**: the cost of each kind by place (local against CI's 2-core runner); why local runs are slow (measure: one proof run locally and on CI, interpreter start, `conftest.py`'s evidence hash, antivirus or disk on D:)
  4. **Speed (cycle time)**: the timeline from an approved change to a verified commit, for Sprint 30 Tasks M, N and O, with what could run in parallel: proofs on CI's full job by hand while the PR is a draft (`workflow_dispatch`), the short review started at push with its 10-minute cap, only the changed files' non-proof tests run locally
  5. **Red proofs: purpose and re-run policy** (team lead, 2026-11-04: "red tests are to ensure the tests are written effectively, correct? Do red tests need to be re-run every time or is once sufficient"). A red proof (`injection.assert_can_fail`) shows that a test CAN fail: it breaks the guarded code and the test must go red. It checks the test, not the code, so it adds nothing on a run where neither changed. Once is not enough for the life of the test, though: a proof goes stale when (a) the guarded code changes, so its mutation target moves or is removed (Sprint 30: `test_the_required_job_can_fail` targeted a line that IMP-1 rewrote; the injection refused, as designed); (b) the test changes, so a weakened assertion could pass under the mutation; (c) a shared helper or fixture changes. The analysis sets the policy from evidence: re-run a proof when its test file, its mutated file or a helper either imports changes (the diff against `origin/develop`; F177 lever 1), and all proofs once per sprint on CI's full job at ready for review; it measures what the every-run policy has caught that the changed-files policy would not (git history of proof failures). Outside practice, for comparison: Google runs mutation analysis incrementally, on the changed lines of each change at code review, not on the whole code base each time (Petrović and Ivanković, ICSE-SEIP 2018; Petrović, Ivanković, Fraser and Just, IEEE TSE 2021)
  6. **Which full run is needed, and where** (team lead, 2026-11-04: "Do we really need a CI run if we did full suite tests before Manual Validation?"). Today two full runs happen: the local Phase 5 run and CI's full job at ready for review. CI's is the one to keep: it is a clean Linux checkout, it is the run the close-out hook requires, and it runs after the last change. Evidence from the same day: CI's full job on d4129e4 failed `test_timer_guards_can_fail`, a proof whose mutated file c116f23 had changed after Manual Validation (fixed in a428b92, issue #90). The analysis decides whether the local Phase 5 run is replaced by CI's full job started by hand (`workflow_dispatch`) before Manual Validation, and measures the cost of each
  7. **Risk-based testing: which ideas apply** (team lead, 2026-11-04: "research 'risk based testing' and determine if any of the ideas should/could be applied ... more efficient while still being very effective"). Risk-based testing sets the intensity and order of testing by risk level, the product of a failure's likelihood and its impact (ISTQB CTFL syllabus v4.0.1, section 5.2; ISO/IEC/IEEE 29119-2 puts risk identification and analysis inside test planning). The proposals below are inferences from those sources and from industry selection work; the analysis tests each against this repository's history before it is recommended:
     - **Apply: a risk tier per test file.** Impact is high where a missed defect damages a record or the confidentiality boundary: evidence immutability, submitted artifacts, provenance and the result writer, device store, Criterion H, the pre-commit and cross-repo hooks. Likelihood is high where code changes often or was changed recently by several hands; Google found that very few tests fail, that failures sit close to the code they test, and that frequently changed code breaks more (Memon et al., ICSE-SEIP 2017). The inventory (part 1) gets a tier column: high-impact tests run on every push; the rest run when their files change
     - **Apply: changed-files selection with a safe fallback (test impact analysis).** Run the tests whose own file or imported modules changed, the tests that failed last time and new tests; fall back to everything when a shared file changes (`conftest.py`, `injection.py`, the requirements). This is Microsoft's Test Impact Analysis design (impacted, previously failing and new tests, with a full-run fallback). The cost is safety: a missed dependency skips a needed test, so CI's full job at ready stays the backstop. This is the mechanism for F177 lever 1 and for the red-proof policy in part 5; issue #90 above is a case it would have caught at commit time
     - **Apply: order by risk and by last failure.** pytest's `--ff` (failed first) runs last time's failures first, and `-x` stops at the first failure; in a local run this gives the answer that matters in the first minute instead of the last
     - **Do not apply: learned (predictive) test selection.** Facebook's model halved test cost while still reporting over 99.9% of faulty changes (Machalica et al., ICSE-SEIP 2019), but it is trained on a large history of test outcomes; this repository's failures are too few to train on. Recorded so it is not re-proposed without that history
     - **Measure before deciding: the full job on high-risk changes only.** Today it runs once, at ready for review. The analysis checks whether a high-impact file changed during a sprint should also trigger it (by hand, `workflow_dispatch`) at the commit, rather than waiting for ready
     - Sources: [ISTQB CTFL syllabus v4.0.1](https://www.istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf); [Felderer et al., risk-based testing and ISO/IEC/IEEE 29119](https://arxiv.org/abs/1905.10676) (the standard itself is paywalled and was not read); [Memon et al. 2017](https://research.google/pubs/taming-google-scale-continuous-testing/); [Microsoft Test Impact Analysis](https://learn.microsoft.com/en-ie/previous-versions/azure/devops/pipelines/test/test-impact-analysis?view=tfs-2017); [Machalica et al. 2019](https://arxiv.org/abs/1810.05286)
- Deliverable: `docs/phase2/F180_TESTING_ANALYSIS.md` with the inventory as a tracked table generated by a script (reproducible), the findings, and recommendations each with what it gives up; the recommendations asked as one decision in `SPRINT_31_DECISIONS.md`, prevention first. Taken recommendations land as F177's levers or new cards
- Acceptance: the inventory covers every test file (a test fails a new test file missing from it); each timing is measured, not estimated; the Sprint 30 timeline is reconstructed from `sprint_status.json`, the CI runs and the commit times; target stated: an approved small change verified and committed in its development time plus about 15 minutes
- Depends on: nothing. Informs: F177, every sprint's Phase 4 to 7

**F179. The status file's update cannot lose another's change; the review task follows finish and pause (~45m [no-history], zero metered) Priority 14**
- Phase: tooling (added 2026-11-04, Sprint 30 Task O, from the one short review of the retrospective improvement commit d792731)
- Platform: N/A (scripts and tests)
- **Pass 2 (2026-11-04)**: priority 40 to 14, to sprint with F180 and F177 (process tooling the team lead's cycle-time target depends on)
- `scripts/update_sprint_status.py` refuses a write when the status file changed after it was read, through a per-process temporary file and `os.replace`. That narrows the window and does not close it: two updates can both pass the check before either replaces, and the second wins silently. On Windows, `os.replace` raises `PermissionError` while a reader holds the file open, so the user sees a traceback, not the refusal
- `--review-task` is evaluated before `--pause-task` and `--finish-task` in the same command, so `--finish-task J --review-task M` is refused although J finishes in that command. Fail-safe; it costs a second command
- Acceptance: an exclusive lock (an `O_CREAT | O_EXCL` lock file beside the status file, with a stale-lock message naming the file) around the whole read, change and write; a test with two processes in which neither change is lost, proven red; a `PermissionError` on replace reported as a refusal; `--review-task` applied after pause and finish, with a test of the one-command case
- Depends on: nothing

**F181. The device-default guard enforces Dirac-3S only (~15m [no-history], zero metered) Priority 20**
- Phase: tooling (added 2026-11-04 at Sprint 31 planning, from D5 and D7)
- Platform: N/A (tests)
- The team lead's rule from Sprint 31 D5: "this and all future runs will be on the Dirace-3S" (`SPRINT_EXECUTION_WORKFLOW.md`, standing hardware rule). `experiments/src/test_phase2_device_default.py` still accepts a Phase 2 module that names Dirac-3 on a `# device named:` line, so the rule is written and not checked. Offered as Task M in D7; the approval named no option, so it is carded here
- Acceptance: the guard refuses any module under `experiments/phase2/src/` that names `eqc_submit.DIRAC_3` (not `DIRAC_3S`), proven red in the same commit; the module docstring cites D5
- Depends on: nothing

### Paper (Stages 4-6)

### Finalize (Stages 7-8)

(F35 interpretation-layer tests, F41 mechanism correction (A20), F42 review findings, F43 IEEE-CIS AUC-ROC, F44 figure resolution, F45 evidence guard, F46 QCi grant and ceiling probe (A21), F47 metered-call wrapper: ALL COMPLETED in Sprint 11, merged via PR #66 (main PR #70); history in SPRINT_11_SUMMARY.md. Removed from candidates per convention.)

(F66 Copilot reviewer-request procedure: COMPLETED in Sprint 14, and CORRECTED
again during it: the working call is GraphQL requestReviews with botIds, not
userIds, and REST returns HTTP 200 while attaching nothing. Removed per convention.)

(F48 shell-metacharacter hook: COMPLETED in Sprint 14 after three iterations, each
correction driven by a false positive against a real command. Removed from
candidates per convention.)

(F71 CHECKLIST restructure and F72 reference-paper library: COMPLETED in Sprint 14.
See SPRINT_14_SUMMARY.md and CHANGELOG.md. F72's design is ADR-0015, whose live copy
moved to EvidenceBasedDB; its build is F77. Removed from candidates per convention.)

### External (team-lead-owned, parallel)

(F11 QCi sponsorship letter send: COMPLETED by the team lead 2026-08-30. F12 portal verification and F15 best-practices/ADR review: COMPLETED in Sprint 2, merged via PR #2; history in SPRINT_2_SUMMARY.md. All three removed from candidates per convention.)

(F4 H6 representation arm, F14 eqc-models feedback package, and F16 minimal CI: COMPLETED in Sprint 9, merged via PR #53 (main PR #54); history in SPRINT_9_SUMMARY.md. All three removed from candidates per convention.)

### HOLD Items (post-submission)

**THE HOLD CONDITION EXPIRED 2026-09-12 when the submission was filed.** Every
item below was held for one reason -- it must not compete with the submission --
and that reason is gone. They are NOT automatically live: "no longer blocked" is
not "selected", and the team lead sets priority. But they should be read as
candidates at the next refinement rather than skipped as held. (F39 was on this list and is
now done: ADR-0014 was accepted in Sprint 14 and its build is F77.)

Flagged rather than re-prioritized: re-scoring nine cards is a scope decision,
not a sweep correction.


**F5. SPECTRA in-segment replication, block B4 -- CLOSED into F90 (2026-10-03)**
- **CLOSED.** F93's reconciliation established that F5, F2b's B4 line and F90 are the same block from three angles. The team lead approved the block on 2026-10-03 and F90 is the surviving card. Nothing here is lost: F5's angle was in-segment replication at 3 cells x 5 seeds, which F90's card now carries as a sizing input rather than a separate item
- Phase: Experiments (moved to HOLD by team lead 2026-09-08 at Sprint 10 refinement)
- Platform: SPECTRA, Dirac-3
- 3 strongest cells x 5 seeds; random-segment negative control machinery reused for fraud transfer
- **Why HOLD**: originally, the QCi grant, then only acknowledged. **That reason is stale**: the grant arrived 2026-09-09 and 1,681 s remained (2026-09-23). The live reason is that F90 is the same block from another angle and must be reconciled with it before either is scheduled (corrected in the Phase 8 sweep, 2026-09-23)
  **The four records are reconciled in `docs/SPECTRA_BLOCK_RECONCILIATION.md` (F93, 2026-10-02), which also records that QCi was SENT 30 fits at 91-136 variables for 270 s. The configuration choice is open and is the team lead's.**
- Depends on: QCi grant; F2 approval pattern

**F25. Non-convex CVQBoost: cardinality-constrained weak-learner selection on Dirac-3 (~4h investigation + hardware) Priority HOLD**
- **QCi answer (2026-10-20, A4)**: 16 levels per variable, values 0 to 15 (hedged: "I assume"); the sum-of-levels budget was not answered directly
- **F138 and F139 re-check (2026-10-13)**: the Dirac-3S guide gives 16 or 17 integer levels per variable (it contradicts itself), and a total-levels limit with no number. The integer cost model was measured on Dirac-3; F139 recommends re-measuring it with 2 of the 2026-09-23 probes (`probe_mid_hi`, `probe_high`; about 195 s at Dirac-3 rates) as this card's first step. The quantum fluctuation coefficient and mean photon number, never set here, belong in this card's design: on a non-convex problem they may matter. F94 (Sprint 25) supplies the controls
- **F94's findings bind this design (2026-10-13, `docs/phase2/F94_EXP3_CONTROLS.md`)**: (1) on the training fold the dct learners memorize the data, many selections reach the objective's floor `-1 + 2/m`, and no solver can be told from greedy, so build the Hamiltonian on held-out predictions; (2) with `lambda = 2 * rows` the data term is at most 0.33% of the objective and the best selection found is already within 0.0026 of the floor, so the ridge weight must be chosen so the fit to the labels matters; (3) the bar is greedy (equivalent to annealing, seconds per instance), reported against the floor; (4) run F104's screen on the chosen Hamiltonians before sizing
- Phase: Phase 2, **Experiment 3 device run** (team-lead approved 2026-09-03; the direct consequence of the Sprint 4 degeneracy finding)
- **Pass 1 (2026-10-25)**: F153 (Sprint 28) found the proxy design fails on all six ULB instances: no room between greedy and the objective floor (`docs/phase2/F153_EXP3_DESIGN.md`). This card stays parked; F160's check on IEEE-CIS is what could reopen its design
- **Design reopened 2026-10-28 (F160, Sprint 29 Task E)**: on IEEE-CIS the gap from greedy to the floor is about 0.1 on all six instances against the 0.01 rule, so F153's falsifier does not fire there and the design may proceed on IEEE-CIS. F104's gate passes there; the guide-based resolution check fails on every instance, as on the control. Open for the design: SCIP found nothing below greedy within 300 s, so the room is shown only to the floor, a bound. The HOLD reason (F102 not filed) stands
- **Pass 1 (2026-11-04)**: F176 (Sprint 30 Task E) found selections below greedy on 3 of 6 IEEE-CIS instances, each by under 2e-05 against a room bound near 0.08-0.097; SCIP at 1,200 s did not beat greedy. The room is reachable only by a sliver so far, and the swap search missed the optimum in 3 of 7 checked cases (`docs/phase2/F176_BELOW_GREEDY.md`). The HOLD reason (F102 not filed) is unchanged
- **HOLD reason, restated 2026-10-03**: needs F102 (preregistration), F94 (controls) and the allocation. **Corrected 2026-10-13 (Pass 1): F94 shipped in Sprint 25 and the allocation arrived 2026-10-09; F102 (a draft, not yet filed) is the hold reason left.** Sized at 3,070 s in the sent hardware plan; after F90 about 445 s of the 1,681 remain (**corrected 2026-10-06: F90 ran and the measured balance fell to 1,022 s**). **2026-10-10: QCi granted the 7,500 s on 2026-10-09, so the allocation no longer blocks this card**; the balance is in `experiments/results/allocation_reads.json`
- Platform: Dirac-3 integer/qudit solver, local proxy for the relaxation only
- **Default device is now Dirac-3S (2026-10-16, Sprint 26 Decision 11).** Experiment 3 already names Dirac-3S (draft section 6). The integer cost model and the 3,070 s sizing are Dirac-3 figures; F139's two re-measurement probes run on Dirac-3S and re-price this card. `qpu_cost_model.quote()` (Sprint 26 IMP-5) covers the continuous solver only; integer-solver cost needs those probes
- The Sprint 4 evidence: the continuous-weight formulation is strictly convex AND nearly degenerate, so an exact classical proxy matches the hardware at small pool sizes. **Corrected 2026-10-14 (Sprint 26 fresh-eyes review)**: this line said "uniform weights even at lambda = 0", which A27 withdrew (at lambda = 0 the optimum is a face of the simplex; the ridge selects the near-uniform point); and the match holds to 91 variables only, with weight cosine falling to 0.82-0.90 at 560-833 variables (B4, B2), as A31's weight resolution predicts. The formulation where that stops being true is combinatorial selection: choose the best subset of m weak learners from a pool of n (cardinality or L0 sparsity constraint), optionally with integer weights -- NP-hard, no exact classical proxy, and the native problem class for Dirac-3's integer solver (num_levels budget against the documented 949 device limit)
- Design sketch: same H matrix and objective, plus a cardinality constraint; classical comparators become greedy/forward selection, L1-then-threshold, and a MIP solver at small n; the honest question is solution QUALITY at fixed wall-clock, not just feasibility
- Expected value: this is the concrete "where quantum optimization is necessary rather than optional" program the Phase 1 paper points at, and the strongest technical item for the QCi conversation
- Depends on: **F104's gate (`device_resolution.resolution_gate`, shipped in Sprint 27, corrected 2026-10-19, Pass 1) run on the chosen Hamiltonians before any device fit** (corrected 2026-10-18, Pass 1: F141 is spent, shipped in Sprint 26) (corrected 2026-10-13, Pass 1: the F138-then-F139 gate is spent, both reported in Sprint 25; the F124 rank-1-first gate is spent, because rank 1's device pilot, F129, was closed; the QCi grant arrived 2026-10-09); Phase 2 preregistration (F102); pairs with F17 (simulator) and F20 (soft votes)

**F30. Concurrent Dirac-3 submission with bounded in-flight requests (~4h build + 1h dry run) Priority HOLD**
- **QCi answer (2026-10-20, A5)**: Dirac-3 and Dirac-3S are two separate devices, both running 24x7, and the account can use either. There are no special-queue hours
- **F138 re-check (2026-10-13)**: `eqc-models` 0.22.1 describes Dirac-3S as "special queues", with no stated hours. The queue measurements below were taken on `dirac-3` and may not apply to `dirac-3s`
- Phase: Phase 2 preparation / infrastructure (team-lead request 2026-09-04)
- Platform: Dirac-3 (offline-testable; gated live vetting of 2-3 calls only)
- **Default device is now Dirac-3S (2026-10-16, Sprint 26 Decision 11).** Live vetting goes to Dirac-3S. F142 measured its queue under 1 s on all five jobs, all late at night, so this card's premise (queue wait dominates) is unmeasured on Dirac-3S in the daytime
- Dirac-3 queues one job at a time, so a 4-5 QPU s fit cost ~85 s of wall clock in Sprint 4; nearly all elapsed time is queue wait. Multiple requests CAN be enqueued concurrently, via separate processes or async submission inside one program
- Design: a BOUNDED window (default 4) of in-flight requests, topping up by one as each completes. Metered calls cannot be wasted, so the window is deliberately small: a reboot or network failure risks only the in-flight requests, never a 20-call block
- Crash safety: a durable job ledger records submission intent and job ids before each call, so a restart retrieves results for in-flight jobs instead of re-billing them
- Preserves every existing guard: spend caps computed against projected spend INCLUDING in-flight requests, frozen identical-config retry rule, B1 hash verification, unparseable-billing charge
- Fully tested offline first (fake client simulating queue latency, out-of-order completion, crash-restart, failed job, unreadable billing); only then 2-3 real calls at window size 2, on explicit approval
- Full card drafted at docs/sprints/drafts/F30_CARD_DRAFT.md
- **Measured queue behavior, 2026-09-09**: the F46 probe submitted at 14:33 local was still queued 52 minutes later, having spent ~97 CPU-seconds on its local pool build. Flat CPU against growing wall clock is the signature of queue wait, not computation. The team lead reports the queue is ALMOST ALWAYS EMPTY AFTER 5PM LOCAL, so wall-clock cost is a function of WHEN a block runs, not what it computes
- **The team lead's intent for this card**: enqueue 4 or more jobs at once so they run CONSECUTIVELY, raising the odds they execute back to back rather than each paying a fresh queue wait. That is a different and stronger value case than the throughput argument below
- Value was judged to arrive with Phase 2 volume (81+ fit grids), and that judgment was made against a free tier with 163 spent seconds. With 3,000 granted seconds (F46) and queue wait as the binding cost rather than device seconds, the case is stronger: whenever a session needs more than one or two fits, serial submission wastes most of the wall clock. Still not recommended BEFORE submission, on calendar grounds alone
- Depends on: nothing to build; live vetting needs F141, spent (corrected 2026-10-18, Pass 1: shipped in Sprint 26) (corrected 2026-10-13, Pass 1: the F138-then-F139 gate and the F124 rank-1-first gate are both spent); live vetting needs team-lead approval (Criterion H)

**F121. Experiment 5 transfer half and router acceptance (~unknown) Priority HOLD**
- Phase: Phase 2, Experiment 5 (added 2026-10-03). Transfer of the in-segment result to fraud segments, judged by the proposal's router criterion: at least one point of recall at the 0.5% budget above the classical champion, out of time, on prespecified segments, against a matched random-segment control
- HOLD until F90 reports. Bounded in advance by F113. **Corrected 2026-10-06 (Pass 1): F90 has reported** -- the replication half did not reproduce on the device (`docs/B4_B5_HARDWARE_RESULT.md`). The stated hold reason is spent; whether the transfer half is still worth running after a failed replication is a scope question for Pass 2, not a correction. **Decided 2026-10-06 (team lead, 3.1): stays on HOLD until F124 reports.** **Corrected 2026-10-07 (Pass 1): F124 has reported** -- no lever beats HGB with a CI that excludes zero on any dataset (`docs/phase2/SPECTRA_IMPROVEMENT_RESEARCH.md`). This hold reason is spent too; whether the transfer half runs is a Pass 2 scope question. **Decided 2026-10-08 (team lead, Sprint 23 refinement): stays on HOLD until F128 and F129 report.** **Corrected 2026-10-10 (Pass 1): F128 has reported** (its premise falsifier fired); F129 has not run, so the hold stands. **2026-10-13 (Sprint 25)**: F139 recommends closing F129, which would leave this hold unmeetable; a new condition or a decision is needed at the same refinement. **F129 CLOSED 2026-10-13 (team lead, Sprint 25 Manual Validation), so this hold can no longer be met. A new condition, or a decision to close or run the transfer half, is due at the Sprint 26 refinement.** **Decided 2026-10-14 (team lead, Sprint 26 Decision 2): stays on HOLD until a Phase 2 run, proxy or device, shows an in-segment edge over the matched control with an interval excluding zero.** F113 found no CVQBoost-specific complementarity with XGBoost (`docs/phase2/F113_ORACLE_GAP.md`): evidence for that decision.


**F116. G2 entanglement ablation on the SV1 simulator (~3h [no-history]) Priority HOLD**
- Phase: Phase 2, gate-based arm (added 2026-10-03). Joint entangling terms ON against OFF, all else identical, with a paired bootstrap CI on the gap
- HOLD until F106 shows the circuit is not dequantized. **2026-10-19 (Pass 1): F106 reported inconclusive in Sprint 27** (not shown dequantized, and level with GAM, GA2M and HGB inside wide intervals), so the hold condition is neither met nor ruled out. Whether a larger test fold should settle F106 first is a Pass 2 scope question

**F117. G4 noise as regularizer: DM1 simulator, then the cheapest hardware (~4h + paid Braket time) Priority HOLD**
- Phase: Phase 2, gate-based arm (added 2026-10-03). Per-gate error rates 0.000 to 0.015; the published prediction for a tuned baseline is degradation
- HOLD: Phase 2, needs paid Braket time and F116

**F118. Latency benchmark p50/p95/p99 against the 100-300 ms envelope (D10) (~unknown) Priority HOLD**
- Phase: Phase 2, resourcing (added 2026-10-03, from the checklist). Phase 1 states the envelope as a target, not a measurement
- HOLD until the Phase 2 brief

**F119. Calibration layer fit (D1) (~unknown) Priority HOLD**
- Phase: Phase 2, resourcing (added 2026-10-03, from the checklist). Phase 1 specifies the layer and does not fit it
- HOLD until the Phase 2 brief

**F120. Structural feedback audit: delay, censorship, corruption, decline rate (~unknown) Priority HOLD**
- Phase: Phase 2, ceiling methodology (added 2026-10-03). Proxies for the four impairments in the payments-network regret floor (arXiv:2605.27557); that paper gives no estimation procedure
- HOLD: most proxies need sponsor data that a public dataset does not carry. Say so plainly where one cannot be estimated
