# Sprint 27 Plan: Gates Before Reporting, and the Screens That Need No Device

**Sprint**: 27 | **Branch**: `feature/20261018_Sprint_27`
**Planned**: 2026-10-18 | **Status**: DRAFT, awaiting approval
**Scope**: F149, F130, F102, F112, F103, F104, F6, F106, F107, F108 and
F109 (team lead selection, 2026-10-18), plus an F146 update (D3 option 1:
draft the unsent QCi questions for the team lead to send, presented with
Manual Validation)
**Metered Dirac seconds**: **0**. No task calls a device. No task calls a
paid AWS service.

## Objective

Build the gates that every Phase 2 result has to pass, and run the screens
that need no device.

- **F149, then F104**: test the F142 runner where the PR #21 review found
  gaps, then move its resolution screen into a shared, tested gate.
- **F102, then F112**: close the preregistration draft's open items, then
  report Experiment 1's interval under it.
- **F130**: three proxy levers against HGB.
- **F103, then F109**: reimplement SPECTRA Tier 1, check it against the
  paper's published value, then run it across the datasets on disk.
- **F6, then F106 and F107**: decide whether a gate-based arm is worth
  running; if it is, run its two first checks on a simulator.
- **F108**: a fraud simulator with a known ceiling, to validate ceiling
  methods before F114 uses them on real data.
- **F146**: the QCi question draft.

## Decisions already made (team lead, 2026-10-18)

- **Scope**: as above. F95 was not selected; its device question stays
  open on its card.
- **D2**: completed sprint issues are closed by Claude without asking.
  #22-30 are closed.
- **D3**: option 1, the F146 draft, presented with Manual Validation.
- Priority numbers unchanged: F149 12, F130 24, F102 30, F112 32, F103
  40, F104 52, F6 70, F106 72, F107 74, F108 80, F109 90, F146 HOLD
  (permanent). Task order below is by dependency, not by number.

## Pre-kickoff (Phase 2)

- Sprint 26 merged to `develop` (PR #21, `3dced65`) and released to
  `main` (PR #31, `a95e590`). The branch content before this sprint's
  commits equals `develop`. Issues #22-30 are closed.
- Full suite run 2026-10-18, before this plan existed: one failure,
  `test_phase3_artifacts.py`, because the status file already names this
  plan's path. It is rerun after this plan is committed.
- Dependency scan: `pip-audit` (through `uvx`) on the lock file finds no
  known vulnerability, 2026-10-18. No bump is planned.

## Plan-to-branch-state verification (3.2.2.1)

Each card was checked against the repository, the installed packages and
the sources it names on 2026-10-18. **Six cards cannot run as carded.**
Each correction below replaces the card's text in this plan, and the card
is corrected in the same commit as the task that meets it.

- **F149: confirmed; one card claim narrowed.**
  - Return codes 4 (allocation unreadable) and 6 (an `enforce` unit fails
    the screen) are raised in `run_dirac3s_verify.main()` BEFORE the stop
    loop (lines 526-540), not inside it (542-571). So `_run_stop` spans
    522-572. It takes the screened units, a balance reader and the fit
    callable as arguments.
  - `qci_client` sends every request through `requests.Session.request`
    (`requests_futures` and the auth client both reach it). `eqc_models`
    builds a new `QciClient` on every access, so an instance patch cannot
    work. The fake goes at `requests.Session.request`. `responses` and
    `requests_mock` are not installed, so the fake is hand-written and no
    dependency is added.
- **F104: one card claim corrected.** The frozen B2 pools were never
  stored. `experiments/results/pools/` holds B1 (`h_*_free_dct_full`), and
  the `mid` and `deep` pools only. The card's "flags the frozen B2 pools"
  becomes "flags a seeded rebuild of B2's configuration", built by
  `run_dirac3s_verify.offline()` for unit `b2_42`. The gate wraps
  `device_resolution._coefficient_spread`. It never calls
  `device_resolution.main()`, which writes `experiments/results/`
  (boundary rule 3). It lives in `experiments/src/device_resolution.py` as
  a public function, opt-in, with Phase 1 behavior unchanged (rule 4).
- **F102: the template is already there; the card's remaining work is
  smaller.** Every item the card lists is present in
  `experiments/phase2/PREREGISTRATION_DRAFT.md`: the template (section 1),
  nested CV, Wilcoxon, Bonferroni, multi-seed, the AUPRC floor (section
  2), "order 3" (section 3), the F104 gate (section 4), and the downsized
  pair with about 20 draws (section 5). What remains is its own section 7:
  re-read arXiv:2604.18837 against section 2; recompute section 5's
  figures from code on all five seeds; set the multiplicity families; set
  equivalence margins; write F112's section 6 entry. The filing date stays
  the team lead's. Re-estimated from 180 to 90 minutes.
- **F112: confirmed; one method point.** `docs/F64_LADDER_DECOMPOSITION.md`
  reports seed-mean t-intervals, not a bootstrap. `metrics.paired_delta_ci`
  (paired, stratified, BCa) exists and needs per-row predictions; those
  are under `experiments/results/predictions/` for three proxy cells, 10
  seeds each. The interval is computed into `experiments/phase2/results/`.
  `score_gates.py` prints `Proxy cell used:` at line 251, today
  `cvqboost_proxy/deep/dct/full`. F112 writes no Phase 1 row, so it cannot
  re-key that cell. The diff is still checked before publishing, as the
  card says.
- **F130: three card claims corrected.**
  - **Rank 6 as carded cannot run.** `eqc_models`' `topNPairs` asserts at
    most d(d-3)/2 pairs: 119 at 17 features (energy_steel, telecom), 90 at
    15 (oilgas). Pair counts of 200 and 400 raise on every dataset; 100
    raises on oilgas. `weak_cls_pair_count` is honored only by the
    sequential builder, and `qubo_proxy.build_pool` does not pass it yet,
    so it gains an opt-in argument. Decision 3 sets the values.
  - **Seeded KNN raises.** `qubo_proxy.seeded_weak_params` adds
    `random_state`, which `KNeighborsClassifier` rejects. KNN is
    deterministic, so a KNN build skips the seed, with a test.
  - **Rank 3 is partly done.** F124's confirm already ran KNN on 5 seeds on
    energy_steel. What remains is 5 seeds on oilgas and telecom, and ULB.
    `lever_screen.py` has no ULB path. A KNN pool build on ULB is the
    O(n_train x n_query) term that missed 47x in Sprint 8, so ULB runs a
    timed pilot first (10% stratified sample, one seed). The full 5 seeds
    run only if the pilot projects them at 60 minutes or less. If not, the
    pilot's timing is the reported result.
  - **Rank 5 config provenance.** `qfe.FourierWallPhaseEncoder` was built
    for ULB: one calendar column, one period. Only energy_steel has raw
    cyclic columns (NSM, day of week, day of year). The SPECTRA files
    already carry `*_phase` columns, used today as raw angles. So rank 5
    is: cos/sin plus train-only whitening of the existing phase columns,
    on all three datasets. **Leakage risk**: `in_pocket` is predictable
    from the phase features at AUC 0.93-0.99 (`docs/F101_IN_POCKET_PROVENANCE.md`),
    so a rank 5 gain is reported with that caveat beside it.
- **F103: the acceptance as carded cannot be met.**
  - The paper (arXiv:2607.15815, read from the copy in the evidence
    library) defines five Tier 1 gates, g1-g5 (Algorithm 1, p.4). It
    publishes **one** Tier 1 value for the real Steel target: the
    Fourier-classifier ROC-AUC, **g2 = 0.94** (section 6.1). Other gate
    values appear only for its two semi-synthetic substrates: the sparse
    pocket's JOINT minus GA2M +0.37, and the dense substrate's HGB minus
    GAM +0.15, joint ratio 9.9 and JOINT minus GA2M +0.00 (p.8).
  - **No Tier 1 code exists** in this repository, `FourierWall2` or
    `ForrierWall`. SPECTRA is proprietary to its authors. F103 is a
    reimplementation from the paper's description. The paper leaves open
    the spectral estimate for g1, the g2 classifier, and JOINT's term
    budget and grid. Each choice is recorded before the first run.
  - **Both JOINT twins in this repository are one-dimensional**
    (`run_h6._fit_joint`, `f100_lane_pilot`): one frequency per column.
    The paper's JOINT searches joint frequency vectors across columns. So
    g4 needs a new k-way JOINT; the existing twin would compute it wrongly.
  - `spectra_energy_steel.csv`'s `target_real` has base rate 0.2075
    (7,272 of 35,040), which matches the paper's 0.21. It is very likely
    the paper's target; that is not proven, because `Load_Type` is not in
    the file.
  - Decision 1 sets the known answers.
- **F109: two card claims corrected.**
  - **The "seven-dataset ladder" is defined nowhere.** The phrase arrived
    with the card in `a299ad2` (2026-10-03) with no list. Six datasets are
    on disk: four SPECTRA, IEEE-CIS and ULB. **This plan uses those six**
    and retitles the card. Say so at approval if you want a seventh (raw
    UCI Steel or the paper's dense substrate).
  - It depends on F103's implementation and on F103 passing. IEEE-CIS
    (590,540 training rows) under a k-way scan is unsized: `[unbounded]`,
    so a pilot on a 10% sample runs first.
- **F6: confirmed; one repository error found.** No gate library is
  installed (`braket`, `qiskit`, `pennylane` all absent). `references.md`
  line 7 says the papers are in `docs/papers/`, which does not exist. The
  Fourier Wall PDF is in the evidence library; the Inverse Born Rule paper
  (arXiv:2602.21350v2) is fetched from arXiv. F6 corrects that line.
- **F106 and F107: platform corrected; both depend on F6.**
  - SV1, which F107 names, is a **paid** AWS simulator: $0.075 per minute,
    3-second minimum per task (aws.amazon.com/braket/pricing, fetched
    2026-10-18). No AWS credentials exist on this machine, and
    `docs/requirements-matrix.md` line 63 (D12) says no Braket runs before
    acceptance. **This plan runs both on a NumPy statevector in the
    project venv**: zero cost, no new dependency. Any Braket SDK install
    or SV1 call would need its own approval.
  - F106's "matches the circuit" had no margin. The margin is set in its
    section 6 entry before the run, as the draft's section 7 requires.
  - Both start only if F6 recommends pursue. Decision 4 sets what happens
    otherwise.
- **F108: two constraints found.** The Fraud Detection Handbook's
  transaction simulator is not on disk. Its code is GPL-3.0 (prose CC
  BY-SA 4.0). This repository is public, so **this plan writes a
  clean-room generator from the handbook's published rules**, cited, with
  no handbook code copied. The handbook's scenario 1 (any amount over 220
  is fraud) is deterministic in a visible feature, so it is switched off
  for the hidden-state ceiling. It is kept as the zero-ceiling reference
  below.
- **F146: confirmed.** `docs/phase2/DIRAC_UNDERSTANDINGS.md` section 4
  lists P1 and P2 (asked 2026-09-25, no answer) and A1-A12 (not sent).
  F142's measurements may answer some; the draft drops those and says
  why.
- **Found, not opened**: the F103 pre-flight found files named
  `spectra-tier1-spec.md` in two planning folders under the Phase 1
  project's name. That project is read on request only, so they were not
  opened. Decision 2 asks.

### Show each threshold can fire (Sprint 25 IMP-2)

- **F130, the lever bar.** The paired percentile CI over 5 seed deltas
  was run on F128's rows on disk: a same-model reference.
  - Leaf 10 minus leaf 5, the same model one setting apart: the CI
    **excludes zero** on all three datasets (energy_steel +0.0020
    [0.0005, 0.0035]; oilgas +0.0015 [0.0010, 0.0019]; telecom -0.0188
    [-0.0266, -0.0118]). So "the lever moves AUPRC" on a CI alone fires
    on a 0.002 change. **A lever moves AUPRC only if its mean change
    against the baseline pool is at least 0.005 AND its CI excludes
    zero.** Two of the three reference pairs fall below that margin.
  - The acceptance bar, "beats HGB with a CI excluding zero", was also
    run on the same rows: none of the 12 leaf configurations passes it
    (energy_steel CIs all include zero; oilgas and telecom all below
    HGB). So it does not fire on a lever that does nothing.
- **F104, the gate.** F142's dry run on disk already shows the split: B1
  at 0.005 of the resolvable step and B2 at 0.014 fail; B4 oilgas at 37
  times the step passes. The gate's test is proven red with
  `assert_can_fail`.
- **F103, the known answer.** No data exists yet. **First run that shows
  it**: g2 on `target_real` with the labels permuted must fall to chance
  (ROC-AUC 0.55 or less), before the real g2 is read against 0.94.
- **F108, the ceiling.** No data exists yet. **First run that shows it**:
  with scenario 1 on, and nothing hidden, the Bayes error of the
  scenario-1 frauds is about zero. The ceiling method must recover that,
  and must report a nonzero error once terminal and customer state are
  withheld. A method that reports the same ceiling both ways is rejected.
- **F106, the dequantization margin.** No data exists yet. **First run
  that shows it**: the twin against itself on two seeds must sit inside
  the margin; if it does not, the margin is too tight for the noise.
- **F112, F107, F109**: descriptive, no threshold. F109's per-gate
  thresholds are the paper's, fixed globally.
- **F149**: both tests proven red with `assert_can_fail`.
- **F102, F6, F146**: no measured premise.

## Tasks

| Task | Card | What | Est | Runtime | Depends on |
|---|---|---|---|---|---|
| A | F149 | Full-library test of the F142 pre-submit guard with a fake at `requests.Session.request`; `_run_stop` extracted (lines 522-572) and tested with a stub fit, codes 4 and 6 | 120 | - | - |
| B | F104 | Public resolution gate in `device_resolution.py` wrapping `_coefficient_spread`; the F142 runner calls it; test against a seeded B2 rebuild and B4 | 60 | ~5 (one 833-variable build) | A |
| C | F102 | Section 7 items: arXiv:2604.18837 re-read, section 5 recomputed from code on 5 seeds, multiplicity families, equivalence margins, F112's section 6 entry | 90 | ~2 | - |
| D | F112 | Paired bootstrap interval (`paired_delta_ci`) on the k and order effects, 10 seeds, as a Phase 2 result | 45 | ~10 (BCa, 10 seeds) | C |
| E | F130 | Rank 3 KNN 5 seeds on oilgas and telecom, ULB pilot; rank 5 cos/sin plus whitening on the phase columns; rank 6 per Decision 3 | 120 | ~50 (about 40 s per cell, 70 cells; KNN unmeasured: one-cell pilot first) + ULB pilot | - |
| F | F103 | Tier 1 g1-g5 reimplemented, k-way JOINT new; known-answer check per Decision 1; 5 seeds | 180 | under 50 (estimate; one-seed pilot first) | - |
| G | F109 | Tier 1 on the six datasets on disk; the phase pipeline on classical models alone; gates before and after the IEEE-CIS UID aggregation | 150 | `[unbounded]` on IEEE-CIS: 10% pilot first | F passes |
| H | F6 | Written analysis and recommendation (pursue, pursue narrowly, decline); `references.md` line 7 corrected | 120 | - | - |
| I | F106 | RFF surrogate and an order-matched JOINT twin against the circuit, NumPy statevector; margin set first | 120 | unsized until H names the qubit count: pilot first | H pursue |
| J | F107 | Prediction error against effective Schmidt rank and shot count, NumPy statevector | 120 | as I | H pursue |
| K | F108 | Clean-room simulator; terminal and customer state withheld; label noise at known rates; one ceiling method checked against the known ceiling | 180 | ~25 (3-5 min per seed, 5 seeds; noise injection is cheap) | - |
| L | F146 | QCi message draft: P1 and P2 follow-up, A1-A12 less any F142 answered; outward-readability check; filed in the gitignored `docs/qci_package/` | 45 | - | - |

**Derived total: 1,350 minutes of work**, the sum of the 12 task
estimates (120 + 60 + 90 + 45 + 120 + 180 + 150 + 120 + 120 + 120 + 180
+ 45), with Decisions 1 and 3 at their recommended options. Each other
option's total is on the option. Two conditional reductions are not in
the total: if F6 does not recommend pursue, I and J (240) do not run; if
F103 fails its check, G (150) does not run.

Runtime is separate. E's and K's runs go to the background, each with a
heartbeat file before any run over 30 minutes. A full suite run takes
about 10 minutes.

How each estimate was set (`docs/VELOCITY_LOG.md` read first; medians
over Sprints 24-26):

- **Tooling (A, B)**: median ratio 0.10, from 7 rows (0.05-1.70). The two
  rows above 1.0 are the infrastructure tasks (Sprint 24's pypdf bump at
  1.7, Sprint 26's client bump at 1.67). A builds new test infrastructure
  (an HTTP fake), so it stays at the card's 120. B is set at the card's
  60, because it moves a function that a metered runner depends on.
- **Research+code (D, E, F, G, I, J, K)**: median ratio 0.28, from 7 rows
  (0.06-0.58). Each is sized to its first decisive measurement, not every
  branch: D 45 of 60; E 120 of 120, because it adds two code paths and a
  ULB path; F 180 of 240 (the g2 check, plus g1, g3-g5 computed);
  G 150 of 360 (reuses F's code); I and J 120 each of 180 and 240 (the
  first step after H names the encoding); K 180 of 360 (the generator and
  one method against the known ceiling).
- **Docs and research writing (C, H, L)**: three docs and research rows in
  Sprint 25 ran at 0.04-0.13, drawing on a sweep done earlier. C, H and L
  have no such sweep, so C is 90 of 180, H is 120 of the card's half day,
  and L is 45 at the card's rate of 30 per update plus the draft.

**Allowances**: none carried. Writing (C, H, L) is 255 of 1,350 minutes
and verification (F) is 180, so neither dominates the sprint.

### Task order

1. **A** (F149), then **B** (F104): both touch the F142 runner.
2. **C** (F102), then **D** (F112).
3. **E** (F130): its runs go to the background after A starts.
4. **F** (F103), then **G** (F109) if F passes.
5. **H** (F6), then **I** (F106) and **J** (F107) if H recommends pursue.
6. **K** (F108): its generation runs in the background.
7. **L** (F146): drafted after the others; presented at Manual
   Validation.

### Task A detail (F149)

- A fake at `requests.Session.request` answers the QCi endpoints the
  real client calls (auth token, files, jobs, job status and metrics,
  allocations). A fit runs through `eqc_submit.metered_fit` and the real
  `QBoostClassifier` with the F142 guard installed by
  `eqc_submit.device(wrap=)`. No device call is possible: the fake raises
  on any URL it does not know.
- `_run_stop(units, screened, balance, fit)` holds what `main()` does from
  line 522: the nothing-to-do exit, code 6, code 4 and the loop.
- **Acceptance**: the guard test fails when the guard is removed from the
  wrap, and the loop test fails when a unit with a ledger entry is
  resubmitted, both proven red with `assert_can_fail`; codes 4 and 6
  tested; the F142 dry run's output byte-identical before and after.

### Task B detail (F104)

- `device_resolution.resolution_gate(J, C)` returns the two spreads over
  the resolvable step and a pass flag. `run_dirac3s_verify.resolution_screen`
  calls it. `_coefficient_spread` is unchanged, so Phase 1's figures are
  unchanged.
- **Acceptance**: the gate flags a seeded rebuild of B2's configuration
  (unit `b2_42`, built offline into `experiments/phase2/results/`, not
  stored in git if over the size limit) and passes B4 oilgas; proven red
  with `assert_can_fail`; the Phase 2 draft's section 4 names the gate;
  the F104 card's B2 wording is corrected.

### Task C detail (F102)

- Section 2 checked against arXiv:2604.18837. Section 5's downsized-pair
  figures recomputed by code on seeds 42-46, with the code committed.
  Multiplicity families named and each entry's seed count set against
  them. Equivalence margins defined for verify and twin entries. F112's
  section 6 entry.
- **Acceptance**: each section 7 item is closed or moved to a dated
  open-item line with its reason; the revision log updated;
  `experiments/PREREGISTRATION.md` untouched.

### Task D detail (F112)

- `metrics.paired_delta_ci` on the k effect (k13 against k17 at order 2
  and 3) and the order effect, per seed, then across 10 seeds, from the
  stored predictions. Rows to `experiments/phase2/results/` with evidence
  tag `SIM`.
- **Acceptance**: both intervals reported under the section 6 entry; the
  `Proxy cell used:` line diffed before and after.

### Task E detail (F130)

- Rank 3: `weak_type="knn"`, no seed, 5 seeds on oilgas and telecom
  through `lever_screen.py`. ULB: the timed pilot, then 5 seeds only if
  projected at 60 minutes or less.
- Rank 5: cos/sin of each `*_phase` column plus train-only whitening, the
  pool rebuilt, 5 seeds, three datasets.
- Rank 6: `build_pool(weak_cls_pair_count=...)` opt-in, sequential build,
  values per Decision 3, 5 seeds, three datasets.
- **Acceptance**: each lever against HGB on the same splits with its
  paired CI; "beats HGB" only with a CI excluding zero; "moves AUPRC" only
  with a mean change of at least 0.005 and a CI excluding zero; a lever
  that does neither is recorded as rejected. The seeded-KNN skip has a
  test. The `in_pocket` caveat sits beside any rank 5 gain.

### Task F detail (F103)

- g1 (off-grid spectral mass, Eq. 4), g2 (a trained-frequency Fourier
  classifier), g3 (HGB minus an additive model), g4 (a k-way JOINT minus
  GA2M), g5 (qubit count). Every choice the paper leaves open is written
  in the module's docstring and the section 6 entry before the first run.
- **Acceptance per Decision 1.** The permuted-label reference runs first.
  If the check fails, the cause is recorded and G does not run.

### Task G detail (F109)

- Tier 1 on the six datasets on disk; the phase pipeline on classical
  models alone; g1-g5 before and after the IEEE-CIS UID aggregation
  (`ieee_features.UIDAggregates`). The 10% pilot runs first.
- **Acceptance**: all five gate values per dataset, with seeds; the
  before-and-after pair for IEEE-CIS; the card retitled to six datasets.

### Task H detail (F6)

- The card's questions: which encodings are not provably classical; what
  the free local simulators support against paid time; whether a gate
  formulation addresses Phase 1's convex objective or relocates it; which
  diagnostics separate a real effect from a reparameterization; the
  cheapest falsifiable first experiment.
- **Acceptance**: a written analysis with a recommendation; a pursue
  names the encoding, the diagnostic, the cost and the falsifier before
  any code is written; `references.md` line 7 corrected.

### Task I detail (F106)

- The circuit's encoding as H names it, simulated on a NumPy statevector.
  An RFF surrogate (`sklearn.kernel_approximation.RBFSampler`) and an
  order-matched JOINT twin (reusing F's k-way JOINT) on identical
  features. The margin is set in the section 6 entry first.
- **Acceptance**: if either matches the circuit within the margin, the
  circuit is reported dequantized and F116 stays on HOLD.

### Task J detail (F107)

- Prediction error against effective Schmidt rank and shot count, with
  the critical rank at each shot budget, on a NumPy statevector with
  sampled shots.
- **Acceptance**: the curve and the critical rank per shot budget,
  reported as a prediction, not as a hardware result.

### Task K detail (F108)

- A generator written from the handbook's published rules (customer and
  terminal profiles, transactions, scenarios 2 and 3; scenario 1 as the
  zero-ceiling reference). Compromised-terminal and compromised-customer
  state withheld from the features. Label noise injected at known rates.
- **Acceptance**: the induced Bayes error is computed from the hidden
  state; one ceiling method recovers it within a margin set before the
  run, or is recorded as failing; the zero-ceiling reference is reported
  beside it.

### Task L detail (F146)

- Audience: QCi's technical contacts, who must be able to answer each
  question without our internal terms. A follow-up on P1 and P2, and
  A1-A12 less any that F142's measurements answer, each with one line of
  why we ask.
- **Acceptance**: the draft passes `scripts/outward_readability.py`; it
  is saved in the gitignored `docs/qci_package/`; it is listed at Manual
  Validation for the team lead to send or change. The revision log of
  `DIRAC_UNDERSTANDINGS.md` records the draft.

## Decisions at approval

Each is independent of the others, and each option names its total.

**Decision 1. F103's known answers**

1. The known answer is g2 = 0.94 on `target_real`, with a tolerance of
   0.03 ROC-AUC. g1, g3, g4 and g5 are computed and reported, with no
   published value to check them against. G runs if g2 is within the
   tolerance. Total 1,350 minutes. (Recommended)
2. Option 1, and also rebuild the paper's sparse pocket and dense
   substrate and check their four published values: JOINT minus GA2M
   +0.37 and +0.00 (tolerance 0.05), HGB minus GAM +0.15 (tolerance
   0.05), joint ratio 9.9 (tolerance 1.0). F gains 120 minutes. Total
   1,470.
3. Hold F103 and F109 until the SPECTRA authors' construction details
   arrive. Both return to the backlog at 40 and 90. Total 1,020.

**Decision 2. The two `spectra-tier1-spec.md` files in the Phase 1
project's planning folders**

1. Yes: read both, read-only, at the start of Task F. Nothing there is
   written.
2. No: do not open them.

**Decision 3. F130 rank 6 pair counts** (sequential build; the default
is the maximum, 119 at 17 features and 90 at 15)

1. 30, 60 and 90 on all three datasets. Total 1,350. (Recommended)
2. 60, 90 and 119 on energy_steel and telecom; 45, 60 and 90 on oilgas.
   Total 1,350.
3. Drop rank 6 from this sprint; it stays on the F130 card with the cap
   recorded. Total 1,330.

**Decision 4. F106 and F107 if F6 does not recommend pursue**

1. Pre-authorized: they return to the backlog at 72 and 74 with F6's
   reason, and the sprint continues without stopping. The total falls by
   240. (Recommended)
2. Stop when F6 is written and ask.

**Decision 5. The plan**

1. Approve the plan as written, with Decisions 1-4 applied.
2. Do not approve yet. I revise it from your comments and present it
   again.

## Risks

- **Size.** 1,350 minutes is nearly twice Sprint 26's 700.
  Research cards have run at 0.06-0.58 of estimate. Each `[no-history]`
  card is sized to its first decisive step, and two conditional gates (F6
  and F103) can remove 390 minutes.
- **F103 is a reimplementation of a proprietary method.** A g2 near 0.94
  shows our version matches on that one value, not that it is SPECTRA.
  The write-up says so.
- **KNN and k-way runtimes are unmeasured.** Each runs a timed pilot
  before its full run; no unsized run starts.
- **Shared code changes** (`qubo_proxy.build_pool`, `device_resolution`)
  are opt-in, with Phase 1 behavior the default (rule 4).
  `test_evidence_immutability.py` and `test_document_figures_resolve.py`
  are the check.
- **A public repository and GPL code.** K writes its own generator.
- **Local memory.** Sprint 25 hit the Windows commit limit during
  tests. CI on the draft PR is the arbiter.
- **CI goes red between this plan and approval.**
  `test_phase3_artifacts.py` requires the PR, issues and approval once the
  status is `phase_3_planning`. That red is expected. Any other failure
  goes to a background agent at the 3.3.2 checkpoint.
- **Session continuity.** Every decision and finding lands in a committed
  file.

## Model assignments

Main loop for all tasks. E's and K's runs, and the suite, run in the
background, each writing to a named file that is read in full when it
finishes.

## Definition of Done

- Every task's acceptance criteria, as corrected above, are met.
- Each new test is proven to fail before it is trusted.
- The full suite passes locally, and CI is green on the final HEAD.
- Manual Validation items, including the F146 draft, are listed on screen
  and saved in `SPRINT_27_VALIDATION.md`.
- Retrospective, `SPRINT_27_SUMMARY.md` at Sprint 28 planning, and the
  velocity log rows from measured start times.
