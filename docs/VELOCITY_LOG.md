# Velocity Actuals Log

**Purpose**: Recorded estimate-vs-actual per task, feeding SPRINT_PLANNING.md estimation (Sprint 2 retro improvement 6). Record at task completion; recompute patterns at retro Category 3.
**Audience**: Sprint planning sessions.
**Last Updated**: 2026-10-10 (Sprint 24 rows; measured-row rule, F136; Sprint 23 row added 2026-10-08; rows 15-22 added 2026-10-07, IMP-7 Sprint 22 retrospective)

| Sprint | Task | Type | Estimate | Actual | Ratio | Note |
|---|---|---|---|---|---|---|
| 2 | F15 review + ADR system | research+docs | 180m | ~45m | 0.25 | agent-assisted research |
| 3 | Task A (F18 notes mining) | research+docs | 60m | ~35m | 0.6 | 2 items pre-completed |
| 3 | B pre-flights (Optuna smoke, WSL spike) | spike | 10m | ~25m | 2.5 | WSL python3.12 install + quoting detours |
| 3 | B1 runner build+smoke | code | 90m | ~50m | 0.6 | tune.py skeleton existed |
| 3 | B5 proxy module + tests | code | 120m | ~75m | 0.6 | eqc source reading included |
| 3 | ADRs 0005-0010 | docs | 90m | ~40m | 0.45 | modules already existed to cite |
| 3 | Hook ports + registration + payload tests | tooling | 60m | ~30m | 0.5 | sources adapted, not rewritten |
| 3 | B1 tuning studies (unattended) | compute | 240-480m | 256m | ~0.8 | CatBoost slowest (56m full); CPU shared with proxy track |
| 3 | B2-B4 refits + gate scoring | compute+code | 100m | ~95m | 0.95 | incl. one checkpoint-key fix + relaunch |
| 3 | B6 A3 side-by-side (builds+solves) | compute | 60m + 60m timebox | ~75m | 0.6 | WSL setup consumed the timebox's first half |
| 3 | B7 hardware request doc | docs | 30m | ~20m | 0.7 | |
| 4 | Task A (F22) A1 health flags + A2 harness + smoke | code | 110m | ~70m | 0.65 | |
| 4 | Task A (F22) 100-trial study (unattended, WSL) | compute | 120-240m | ~85m | 0.5 | fork builds + H cache |
| 4 | Task A (F22) refits + rank + report updates | code+compute | 60m | ~45m | 0.75 | |
| 4 | Task B (F21) research memo (agent) | research | 120m | ~9m agent + 15m fold-in | 0.2 | primary-source finds decisive |
| 4 | Task D (F7) memo + checklist walk + positive control | docs | 120m | ~60m | 0.5 | |
| 4 | Task C (F2) hardware runner + 27 metered fits | code+compute | 240m | ~150m | 0.6 | 0 failures, 0 retries; 120 QPU s |
| 12 | F49-F63 review-response cards (15 cards) | code+docs | ~360m | ~370m | ~1.0 | estimated from a completed analysis, not mid-review |
| 12 | F2b B2 block (11 metered fits) | compute | ~450 QPU s | 906 QPU s | 2.0 | frozen grid assumed ~40 s/fit; measured 82 s. See F2b card |
| 12 | F2b B3 block (12 metered fits, matched re-run) | compute | ~650 QPU s | 62 QPU s | 0.1 | reduced recipe far cheaper per sample than B2 |
| 12 | F38 page limits | docs | 45m (first card) | ~5x that, across 4 re-measures | >5 | an estimate that grows 5x across one sprint is not an estimate |
| 12 | F37 repository public | tooling | 45m | ~45m | 1.0 | pre-flip secret scan across 259 commits included |
| 13 | Task A evidence walk (agent + own verification) | verify | 90m | ~90m | 1.0 | agent 15m in parallel; found 6 document defects |
| 13 | Task B requirements-matrix walk, 92 rows | verify | 60m | ~60m | 1.0 | found 6 stale rows, 4 unknown before the walk |
| 13 | Task C confidentiality scan + compliance walk | verify | 30m | ~30m | 1.0 | scripted; 0 HIGH |
| 13 | Task D final render + page check | build | 20m | ~20m | 1.0 | run 3x in total as findings landed |
| 13 | UNPLANNED: 6 approved corrections, A32, backout, 2 re-renders | code+docs | 0m | ~60m | n/a | findings-driven; the 30% allowance now exists for this |
| 14 | F68 freeze artifacts + two dead hooks | tooling | 120m | ~150m | 1.25 | grew: new hook + test class |
| 14 | F69 README rebuilt, executed on a fresh clone | docs | 120m | ~120m | 1.0 | found 2 defects the working tree hid |
| 14 | F70 CHANGELOG backfill + workflow step | docs | 90m | ~90m | 1.0 | guard threshold wrong on first write |
| 14 | F71 CHECKLIST split into three | docs | 90m | ~60m | 0.7 | |
| 14 | F48, F65, F66, F67 tooling cards | tooling | 165m | ~180m | 1.1 | F48 took three iterations |
| 14 | F39 + F72 ADRs (design only) | design | 420m | ~600m | 1.4 | four team-lead corrections mid-design |
| 14 | UNPLANNED: 20 review findings | fix | 0m | ~120m | n/a | 2 vacuous guards; the 30% allowance did not cover it |
| 15-19 | (per-task actuals not recorded) | n/a | n/a | n/a | n/a | the log lapsed after Sprint 14; Sprint 19 recorded two of three tasks, in its summary only |
| 20 | Task A (F97) five tests stop reading live state | tooling | 40m | 52m | 1.3 | `SPRINT_20_SUMMARY.md`; first sprint with complete per-task actuals |
| 20 | Task B (F93) one SPECTRA configuration | analysis | 60m | 47m | 0.8 | |
| 20 | Task C (F98) hook timeout budget | tooling | 30m | 34m | 1.1 | |
| 20 | Task D (F99) tracked hash for correspondence | tooling | 20m | 28m | 1.4 | |
| 21 | Task A (F90) bring in the device result | verify | 45m | 0m | 0 | already satisfied |
| 21 | Task B (F122) four guards rewritten | tooling | 45m | 58m | 1.3 | |
| 21 | Task C (F90) B5 and B4 on Dirac-3 | code+compute | 240m | 229m | 0.95 | plus 653 device seconds |
| 21 | Task D (F100) classical bar | code+compute | 360m | 133m | 0.37 | `[no-history]` |
| 21 | Task E (F101) in-pocket provenance | analysis | 60m | 34m | 0.57 | |
| 22 | Task A (F123) phase separation document | design+docs | 120m | 30m | 0.25 | later superseded at validation (F127) |
| 22 | Task B (IMP-3) suite may not change evidence | tooling | 30m | 32m | 1.1 | includes hardening after a security review |
| 22 | Task F (F125) close-out hook ref | tooling | 20m | 45m | 2.25 | the card's diagnosis was incomplete |
| 22 | Tasks D+E (F17 emulator, F20 soft votes) | research+code | 570m | 54m | 0.09 | run in parallel, not separable; includes D's 20m acceptance test (corrected in PR #159 review from 34m, 0.06) |
| 22 | Task C (F124) SPECTRA lever research | research | 240m | 95m | 0.4 | `[no-history]` |
| 22 | UNPLANNED: Manual Validation rounds 1-3 | docs+decisions | 0m | 45m | n/a | B2 recovery attempt, F126/F127 carded |
| 22 | UNPLANNED: retrospective and improvements IMP-1 to IMP-7 | process+tooling | 0m | 70m | n/a | IMP-3's tracked pre-commit hook was the code item |
| 22 | UNPLANNED: second security review, 12 findings fixed | fix | 0m | 55m | n/a | evidence guard moved to the root conftest |
| 22 | UNPLANNED: PR #159 code review, 15 findings fixed | fix | 0m | 85m | n/a | 1 critical: the confidentiality scan missed renamed files |
| 23 | Task A (F127) restore dry run | tooling | 45m | 20m | 0.44 | actual judged at completion, no start time recorded (Sprint 23 IMP-3); Tasks C and D run after this row |
| 24 | Task A (F131) hermetic CI-status test | tooling | 30m | 3m | 0.10 | start taken from the clock by hand |
| 24 | Task B (F136) task start times | tooling | 20m | 1m | 0.05 | start typed by hand before the tool existed; not fully measured |
| 24 | Task C (F132) Phase 1 boundary | tooling | 90m | 12m | 0.13 | measured |
| 24 | Task D (F134) pre-commit blocks without patterns | tooling | 30m | 2m | 0.07 | measured |
| 24 | Task E (F133) job_id on device rows | tooling | 40m | 2m | 0.05 | measured |
| 24 | Task F (F135) complete decision options | process | 10m | 1m | 0.1 | measured |
| 24 | Task G (F128) leaf sweep | research+code | 50m | 29m | 0.58 | measured; includes the 26m run; `[no-history]` |
| 24 | Task H (F137) pypdf bump | tooling | 20m | 34m | 1.7 | measured; waited for G's run, which used the same venv |
| 24 | UNPLANNED: code review (6 findings) and fresh-eyes review (8) | fix+docs | 0m | not timed | n/a | review time was not task-timed; IMP-2 to time it was declined |
| 25 | Task A (F138) Dirac-3S research | research | 120m | 16m | 0.13 | measured; the QCi site sweep ran in the background |
| 25 | Task B (F139) Dirac-3 re-run review | research | 120m | 5m | 0.04 | measured; drew on A's sweep |
| 25 | Task C (F102) Phase 2 preregistration, first draft | docs | 120m | 5m | 0.04 | measured; drew on A's sweep |
| 25 | Task D (F113) oracle-gap test | research+code | 90m | 5m | 0.06 | measured |
| 25 | Task E (F29) sample-size insensitivity | research+code | 60m | 12m | 0.2 | measured; run in the background |
| 25 | Task F (F94) Experiment 3 controls with SCIP | research+code | 240m | 129m | 0.54 | measured; includes the run, stopped twice |
| 25 | UNPLANNED: code review (10), fresh-eyes reviews (24 and 15) and their fixes | fix+docs | 0m | not timed | n/a | changed four committed conclusions |
| 25 | UNPLANNED: Task G (F146 document, F147 card), added at Manual Validation | docs | 0m | not timed | n/a | no start stamped before the work began |
| 26 | Task A (F141) client bump, Dirac-3S selector | tooling | 45m | 75m | 1.67 | measured; two venvs and the lock |
| 26 | Task B (F145) seeded weak learners | tooling | 30m | 3m | 0.1 | measured, understated: the test was written before the timer started |
| 26 | Task C (F144) proxy twin of B2 | research+code | 45m | 24m | 0.53 | measured; overlapped E, F, G and D (IMP-2) |
| 26 | Task D (F142) Dirac-3S verify, three metered stops | research+code | 80m | 884m | n/a | measured elapsed, not work: three approval waits and an evening gap (IMP-2) |
| 26 | Task E (F147) evidence-library query tool | tooling | 120m | 3m | n/a | measured stamp gap; ran alongside F and G, so not a work time (IMP-2) |
| 26 | Task F (F126) sparsity rule, held-out test | research+code | 60m | 9m | 0.15 | measured; overlapped G and D |
| 26 | Task G (F105) IEEE-CIS harness | research+code | 240m | 66m | 0.28 | measured; audit run in the background |
| 26 | Task H (F146) understandings updates | docs | 60m | not timed | n/a | no start stamped; the updates fell inside D's span |
| 26 | UNPLANNED: Task I (Decision 10) cross-repo guard, EvidenceBasedDB reads | fix+docs | 30m | 18m | 0.6 | stamps written by hand, not through the tool (IMP-2) |
| 26 | UNPLANNED: Decision 11 (Dirac-3S default) and retrospective IMP-1 to IMP-5 | fix+tooling | 0m | not timed | n/a | at Manual Validation and the retrospective |
| 27 | Task A (F149) pre-submit guard through the real library | tooling | 120m | 8m | 0.07 | measured stamp gap; E's runs in the background |
| 27 | Task B (F104) public resolution gate | tooling | 60m | 9m | 0.15 | measured stamp gap; overlapped E |
| 27 | Task C (F102) draft section 7 | docs | 90m | 5m | 0.06 | measured stamp gap; overlapped E |
| 27 | Task D (F112) Experiment 1 intervals | research+code | 45m | 22m | 0.49 | measured; overlapped E |
| 27 | Task E (F130) lever screens | research+code | 120m | 87m | 0.73 | measured elapsed, mostly background runs; overlapped B-L |
| 27 | Task F (F103) Tier 1 known-answer check | research+code | 300m | 39m | 0.13 | measured; overlapped D and E |
| 27 | Task G (F109) Tier 1 on six datasets | research+code | 150m | 84m | 0.56 | measured elapsed; a 62-minute background run |
| 27 | Task H (F6) gate-based arm analysis | docs | 120m | 8m | 0.07 | measured stamp gap; the analysis overlapped D-F |
| 27 | Task I (F106) circuit against twins | research+code | 120m | 193m | n/a | measured elapsed, not work: a 37-minute pilot and a 144-minute run |
| 27 | Task J (F107) shot budget | research+code | 120m | 23m | 0.19 | measured, pause excluded (paused for F106's run) |
| 27 | Task K (F108) ceiling validation | research+code | 180m | 12m | 0.07 | measured stamp gap, not a work time; overlapped E, F and I |
| 27 | Task L (F146) QCi questions draft | docs | 45m | 3m | 0.07 | measured stamp gap |
| 28 | Task A (F151) ULB HGB comparator cause | research+code | 50m | 8m | 0.16 | measured; overlapped I and J |
| 28 | Task B (F152) Experiment 2 entry and first score | research+code | 110m | 46m | 0.42 | measured; overlapped C-L |
| 28 | Task C (F153) Experiment 3 entry and proxy design | research+code | 150m | 70m | 0.47 | measured; overlapped B, E-L |
| 28 | Task D (F111) Experiment 4 harness and run | research+code | 130m | 180m | n/a | measured elapsed, not work: the run above the cap (DV2) in the background |
| 28 | Task E (F110) Experiment 6 scaling | research+code | 100m | 198m | n/a | measured elapsed, not work: the pilot and the 833-variable runs in the background |
| 28 | Task F (F154) confusion counts and the outcome rule | research+code | 190m | 12m | 0.06 | measured stamp gap; first task |
| 28 | Task G (F114) calibrated plug-in | research+code | 60m | 8m | 0.13 | measured; overlapped B, C, E |
| 28 | Task H (F150) construction request draft | docs | 30m | 1m | n/a | measured from the commit, after the work |
| 28 | Task I (F115) integer cost scaling | docs | 45m | 3m | 0.07 | measured; overlapped A |
| 28 | Task J (F13) PoC plan skeleton | docs | 75m | 4m | 0.05 | measured; overlapped A |
| 28 | Task K (F146) QCi drafts | docs | 45m | 1m | n/a | measured from the commit, after the work |
| 28 | Task L pypdf 6.20.0 to 6.21.1 | tooling | 45m | 2m | 0.04 | measured; overlapped B, C, E |
| 28 | Task M (F162) in-pocket head-to-head | research+code | 90m | 39m | 0.43 | measured; a 28.5-minute run inside it |
| 28 | D4 storage prevention (#60) | tooling | none | not measured | n/a | added at Manual Validation; no timer or issue until the retrospective (IMP-4) |
| 28 | Task R retrospective IMP-1, 2, 4, 5, 6 | tooling | 195m | 16m | 0.08 | measured |
| 29 | Task A (F165) resumed run keeps its id | tooling | 60m | 2042m | n/a | measured elapsed, not work: the timer ran across the overnight breaks |
| 29 | Task B (F159) parallel pool build timed | research+code | 60m | 622m | n/a | measured elapsed, not work: includes the 9-hour hang (12:10am to 8:58am) |
| 29 | Task C (F164) Phase 2 figures resolve | tooling | 270m | not measured | n/a | timer never started (IMP-4; F173) |
| 29 | Task D (F156) Henze-Penrose bound | research+code | 90m | 2647m | n/a | measured elapsed, not work: across the overnight breaks |
| 29 | Task E (F160) Experiment 3 room on IEEE-CIS | research+code | 75m | 53m | n/a | measured from the run's start only; code written earlier with no timer |
| 29 | Task F (F166) best result per algorithm on ULB | research+code | 240m | 158m | 0.66 | measured; overlapped E and G |
| 29 | Task G (F158) fraud types | research+code | 150m | 6m | n/a | measured from the run's start only; code written earlier with no timer |
| 29 | Task H (F167) PoC plan draft | docs | 60m | 2036m | n/a | measured elapsed, not work: across the overnight breaks |
| 29 | Task I pypdf 6.21.1 to 6.21.2 | tooling | 45m | 17m | 0.38 | measured |
| 29 | Task J PR 63 review fixes | tooling | none | 69m | n/a | measured; not planned |
| 29 | Task K retrospective IMP-1 to IMP-4 and their review fixes | tooling | 125m | 55m | 0.44 | measured; two full suite runs inside it |
| 30 | Task A (F173) the commit's own task timer | tooling | 45m | 10m | n/a | measured; finished before F175 kept elapsed; 0.22 of its estimate, cause unverified (retrospective IMP-3) |
| 30 | Task B (F175) active and elapsed minutes | tooling | 60m | 11m | n/a | measured, active, 11m elapsed; under a fifth of its estimate, cause unverified |
| 30 | Task C (F168) restarts are safe | tooling | 240m | 15m | n/a | measured, active, 15m elapsed; under a fifth of its estimate, cause unverified |
| 30 | Task D (F174) best per algorithm on IEEE-CIS | research+code | 240m | 31m | n/a | measured, active, 678m elapsed; the 10-seed run worked in the background with no tool call |
| 30 | Task E (F176) below greedy on IEEE-CIS | research+code | 90m | 2m | n/a | measured, active, 143m elapsed; the SCIP runs worked in the background |
| 30 | Task F (F169) plug-in bins | research+code | 120m | 2m | n/a | measured, active, 41m elapsed |
| 30 | Task G (F170) missed frauds' neighbors | research+code | 30m | 6m | n/a | measured, active, 40m elapsed |
| 30 | Task H (F171) missed by all on IEEE-CIS | research+code | 60m | 13m | n/a | measured, active, 34m elapsed |
| 30 | Task I (F172) Sprint 29 coverage tests | tooling | 90m | 14m | n/a | measured, active, 14m elapsed; under a fifth of its estimate, cause unverified |
| 30 | Task J Phase 5 fresh-eyes fixes | tooling | none | 12m | n/a | measured, active, 12m elapsed; not planned |
| 30 | Task K Manual Validation fixes and D8 | tooling | none | 46m | n/a | measured, active, 56m elapsed; not planned |
| 30 | Task L CI under 5 minutes (D9) | tooling | none | 162m | n/a | measured, active, 276m elapsed; not planned |
| 30 | Task M PR 74 review fixes | tooling | none | 156m | n/a | measured, active, 285m elapsed; not planned; two local proof runs of 41m and 1h43m inside it |
| 30 | Task N retrospective IMP-1 to IMP-5 (D10) | tooling | 160m | 60m | 0.38 | measured, active, 60m elapsed; the first task with `--estimate` |

**Measured and judged rows (F136, Sprint 24).** From Sprint 24 on, every
task's actual is computed from a recorded start
(`update_sprint_status.py --start-task` / `--finish-task`), and its Note
says **measured**. Every earlier row, and any later row whose Note does not
say measured, is an actual judged at completion. A `~` before an actual
marks a judged value that was also approximate.

**Active and elapsed minutes (F175, Sprint 30).** From Sprint 30 on,
`--finish-task` records the actual as ACTIVE minutes in `task_actuals`:
elapsed time less pauses and less every gap of more than 30 minutes with
no tool call in `.claude/activity.log` (written by
`.claude/hooks/log_task_activity.py` while a timer runs). The elapsed
minutes are kept in `task_elapsed`. A row's Note says **measured, active**
and gives the elapsed minutes beside it, so Sprint 30 rows compare with
earlier ones. A finish with no activity log falls back to elapsed less
pauses and says so; such a row's Note says **measured, elapsed**.

**Pattern, recomputed at the Sprint 22 retrospective.** Tooling cards land
near their estimate (ratio 0.95-1.4 in Sprints 20-22; a wrong diagnosis
doubles one). Research and analysis cards marked `[no-history]` ran at
0.09-0.57 of their estimate in Sprints 21-22: they were sized as if every
branch would be explored, and the evidence cut most branches early. The
estimation rule in `SPRINT_PLANNING.md` now applies this.
