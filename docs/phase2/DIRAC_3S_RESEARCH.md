# F138: What Dirac-3S Changes, Before Any Further Dirac-3 Seconds

**Sprint 25 Task A** (#13) | **Date**: 2026-10-13 | Zero metered seconds
(no device call was made; the balance read is a GET)

**Who reads this, and what they decide.** The team lead, and F139 straight
after it. The decision is which Dirac-3 work runs next, on which device, at
what cost, and whether any past run should be repeated.

## Bottom line

- **Dirac-3S is opt-in, by name, and our code cannot reach it today.** The
  QCi client libraries released 2026-10-05 and 2026-10-07 add a device
  called `dirac-3s`. Our pinned versions (`qci-client` 5.0.2,
  `eqc-models` 0.21.0) do not know it, and every job this repository has
  sent named `dirac-3`. Reaching Dirac-3S needs both packages bumped and
  one argument added to the solver.
- **The bigger device is the expansion configuration.** "Nearly 10,000
  variables" is QCi's figure for a base module plus one expansion module
  (9,980 at second order). The base module alone is 949, the same ceiling
  as Dirac-3. Which configuration serves the cloud `dirac-3s` queue is
  **not stated** in any source read. That one fact decides whether
  telecom_churn (987 variables) can run.
- **Higher orders are not new.** Dirac-3's own guide already listed orders
  1 to 5 with the same base ceilings (135 variables at 3rd order, 39 at
  4th, 19 at 5th). Only the expansion module's ceilings are new (580, 145
  and 55).
- **The resolution limit is unchanged**: about 200:1 (23 dB). B2's failure
  mode (A31) applies to Dirac-3S exactly as it did to Dirac-3.
- **Our cost model cannot be carried over.** The guide gives per-sample
  times only for a 50-variable problem. Pricing any Dirac-3S block needs
  one measured fit, which F139 should plan as the first step of any
  re-run.
- **No amendment to the frozen Phase 1 preregistration is needed** to run
  on Dirac-3S, provided the results are reported as Phase 2 rows naming
  the device, never as new cells of a Phase 1 gate (inference from
  section 11; see question 6).

## Sources read

| Source | How read | Date or version |
|---|---|---|
| Dirac-3S User Guide, Rev A, `QCi-QMS-900-000001` (EvidenceBasedDB `References/QCi-site/systems/Dirac_3S_Users_Guide_Rev_A-1.pdf`) | In full, 38 pages, with `pypdf` | "September 2026, Revision A" |
| `qci-client` 5.0.3 and `eqc-models` 0.22.1 wheels from PyPI | Downloaded to a scratch folder and diffed against the pinned versions; not installed | Uploaded 2026-10-05 and 2026-10-07 |
| The pinned `qci-client` 5.0.2 and `eqc-models` 0.21.0 | Read in `.venv/Lib/site-packages` | As installed |
| QCi's notice of 2026-10-09 | `docs/qci_package/2026-10-09_qci_dirac3s_and_seconds.pdf` (gitignored) | 2026-10-09 |
| `experiments/PREREGISTRATION.md` sections 10 and 11 | Read | FROZEN |
| QCi web pages and the example notebook | Background sweep; see "QCi web sources" below | 2026-10-13 |

EvidenceBasedDB was read only. Nothing was written there.

## The seven questions

### 1. Which device serves this account, and how is it chosen?

**Chosen by name, per job.** Verified in the packages:

- `qci-client` 5.0.3 adds `DeviceType.DIRAC3S = "dirac-3s"` and accepts it
  for both continuous (`sample-hamiltonian`) and integer
  (`sample-hamiltonian-integer`) jobs. Its docstring: the device type "may
  be "dirac-3s" and, unlike the "dirac-3" alias, is not remapped to a
  device-specific name". It also drops 5.0.2's `dirac-3.2` device type.
- `eqc-models` 0.22.1 replaces the solver's `generation` argument with
  `sampler_type`, whose "only allowed value is 'dirac-3s'", described as
  "enabling access to special queues". It requires `qci-client>=5.0.3`.
- Our code never names a device. The classifiers inside `eqc-models`
  construct `Dirac3CloudSolver()` with no arguments (`eqc_submit.py:162`
  holds that class as its substitution point), and `run_integer_probe.py`
  calls `Dirac3IntegerCloudSolver()` the same way. So every job this
  repository has sent went to the default `dirac-3`.

**Not stated in any source read**: whether the `dirac-3` queue itself now
runs on upgraded hardware, and whether this account may use `dirac-3s`.
QCi's notice says "Dirac-3S is available" and points to the notebook; it
does not say what the `dirac-3` name now serves. **A question for QCi.**

### 2. The variable ceiling

From the guide's Table 2 ("Dirac-3S Hardware Characteristics"):

| Order | Base module | Base + 1 expansion module |
|---|---|---|
| 2nd | 949 | 9,980 |
| 3rd | 135 | 580 |
| 4th | 39 | 145 |
| 5th | 19 | 55 |

- The base module's 949 equals the Dirac-3 ceiling in amendment A2. On the
  base module, telecom_churn at schedule 3 (987 variables) still cannot
  run.
- The continuous solver's sum constraint is R in [1, 10000]. The integer
  solver's levels are given as `{0, ..., 15}` in Table 1 and as
  `0 <= v_i <= 16` in section 5.1; the guide contradicts itself by one
  level.
- The "nearly 10,000 variables" figure is the expansion configuration.
  **Which configuration the cloud serves is not stated** (question for
  QCi).
- "Max number of variables" is stated per order. Whether the integer
  solver's budget is still the sum of levels (`sum(upper_bound + 1)`, as
  `integer_path.py` reads it for Dirac-3) or now a variable count is
  **not stated**.

### 3. Cost per fit: does the F17 cost model still hold?

**It cannot be checked from the sources.** The guide's only timing figure
is section 5.5's Table 4, for "a basic 50 variable sum constraint problem",
average time per sample:

| Relaxation schedule | Seconds per sample |
|---|---|
| 1 | 0.236 |
| 2 | 0.420 |
| 3 | 1.093 |
| 4 | 1.278 |

- The guide does not say this table was measured on Dirac-3S hardware,
  and Dirac-3's guide did not carry it (web sources, below).
- Our measured Dirac-3 costs are at other sizes: about 0.6 s per sample
  for B3, and 11.27 s per sample for B2 at 833 variables. No figure at our
  sizes exists for Dirac-3S, so the F17 model (81.7 s per fit at 816
  variables) can be neither confirmed nor replaced from documents.
- **One measured Dirac-3S fit at a known size is the cheapest way to
  settle it.** F139 should put one at the front of any re-run.
- Schedule 4 against schedule 2 is 3.04x in this table. F95 priced its
  schedule-4 check from a 3.4x ratio (range 2.3x-5.3x) in QCi's portfolio
  example. 3.04x sits inside that range, so F95's estimate (about 60 s,
  range 40-110) is not changed by this, but it was derived for Dirac-3.
- How the cloud meters Dirac-3S, and whether it differs from Dirac-3, is
  **not stated** in the guide.

### 4. Relaxation schedules, samples and the integer limit

From the guide's Table 3 ("control parameters, valid ranges, and default
settings"):

| Parameter | Range | Default |
|---|---|---|
| Dynamic range | up to 23 dB | System-defined |
| Quantum fluctuation coefficient | 1-100 | 1 (continuous), 15 (integer) |
| Mean photon number | 6.67e-5 to 6.67e-3 | 3.33e-4 |
| Relaxation schedule | 1, 2, 3, 4 | 1 |
| Number of samples | 1-100 (cloud maximum 100) | 1 |

- The schedules are the same four. Higher schedules give the system longer
  to settle, and the guide's QPLIB example shows more samples escaping
  local minima as the schedule rises.
- **Quantum fluctuation coefficient and mean photon number are not new to
  our software**: the pinned `qci-client` 5.0.2 already passes both, and
  its comment says each "overrides value defined implicitly by
  relaxation_schedule". No block in this repository has set either. They
  are untested levers.
- The integer limit: 16 or 17 levels per variable (see question 2). The
  949 figure in `integer_path.DEVICE_LEVEL_CEILING` matches the base
  module's 2nd-order ceiling. Whether it still bounds the level sum is
  open.

### 5. Do the pinned clients support Dirac-3S, and what changes in our code?

**No.** The pinned `qci-client` 5.0.2 has no `dirac-3s` device type, and
`eqc-models` 0.21.0 has no `sampler_type` argument. To use Dirac-3S:

1. Bump `eqc-models` to 0.22.1 and `qci-client` to 5.0.3 in
   `requirements.txt` and the lock file. Both are under two weeks old on
   2026-10-13.
2. Construct the solver with `sampler_type="dirac-3s"`. For the
   classifiers that means substituting `cb.Dirac3CloudSolver` at the point
   `eqc_submit.py` already uses; for integer jobs, passing it to
   `Dirac3IntegerCloudSolver` directly.
3. Record the device on every row. Today a row cannot say which device
   produced it, because only one existed. F133's `job_id` rule should gain
   a `device_type` field before the first Dirac-3S row is written.
4. Re-run the proxy-identity check: `qubo_proxy.py` replicates the
   Hamiltonian "read from eqc-models 0.21.0 source". A version bump must
   confirm the Hamiltonian is unchanged before any proxy comparison.

`metered_call.py` reads cost from the response and needs no change unless
QCi bills Dirac-3S differently (not stated).

### 6. Does a device change need a `PREREGISTRATION.md` amendment?

**Not to run on Dirac-3S, if the results are reported as Phase 2.** This is
inference from the frozen text, not a ruling:

- Section 10 is the Phase 1 hardware grid, and every block in it has run.
- Section 11 lets an amendment add exploratory analyses, and forbids adding
  cells to an existing hypothesis after its data is observed. A Dirac-3S
  re-run of B2 or B4 reported AS a Phase 1 gate cell would add a cell to
  an observed hypothesis: a reported **deviation**, not an amendment.
- Reported as a dated Phase 2 row, naming the device, it touches no Phase 1
  claim. That is the pattern every Phase 2 card already follows.
- So F102's draft must require a device field on every Phase 2 hardware
  row, and any Dirac-3 against Dirac-3S comparison is a Phase 2 result
  with its own preregistration entry.

### 7. Queue timing

**The stored memory may not apply.** The note that the queue is usually
empty after 5 pm local was measured on `dirac-3`. `eqc-models` 0.22.1
describes `dirac-3s` as "special queues". Their timing is not stated. The
first Dirac-3S fit should record its queue wait.

## QCi web sources

A background sweep of quantumcomputinginc.com, PyPI and QCi's public GitHub
on 2026-10-13 recorded 71 findings, each with its URL and a verbatim quote.
The ones that change or extend the answers above:

- **What QCi calls it.** The `qci-client` 5.0.3 docs: "dirac-3s is QCi's
  second generation Dirac-3 device". The press release of 2026-10-01: "the
  next-generation of its Dirac-3 quantum optimization machine", first
  customer shipment "expected in November 2026". The product page at the
  old Dirac-3 address is now titled Dirac-3S. No source says the cloud
  `dirac-3` device is retired.
- **The cloud docs name the selector.** "Pass device_type="dirac-3s" in the
  job_params dictionary". Unknown keys are "dropped from the job body
  without warning", so a misspelled parameter fails silently. `eqc-models`
  0.22.1 ships a script, `check_dirac3s.py`, built on
  `Dirac3ContinuousCloudSolver(sampler_type="dirac-3s")`.
- **"Nearly 10,000" is a narrow claim.** The 9,980-variable demonstrations
  were 2nd-order continuous problems on base plus one expansion module,
  with sum constraint 100, relaxation schedule 1 and the best of 10
  samples. The press release frames it as "a 10x increase over QCi's
  current 1,000-variable system".
- **Degree support is unchanged.** Dirac-3's guide (v0.0.04, 2025) already
  listed orders 1 to 5 with ceilings 949, 949, 135, 39 and 19. Dirac-3S's
  base module matches them exactly.
- **The timing table may not be Dirac-3S data.** The guide does not say
  where Table 4 was measured, and Dirac-3's guide did not carry it. Much of
  the new guide's body text still says "Dirac-3".
- **Dirac-3S times at larger sizes**, from QCi's own benchmark notebooks,
  run on-premises through `eqc-direct`, not the cloud: about 1.8-2.3 s per
  sample at 171 variables, 2.4-5.5 s at 500, 14-28 s at 2,000, and 144-232
  s for one sample at 9,980. These are different problems from ours and a
  different access path; they are not a cost model for this repository.
- **Billing.** The product page's FAQ still names only "Dirac-1, Dirac-2,
  or Dirac-3", with run time charged and queue time free. Nothing states
  how Dirac-3S is billed.
- **QCi's benchmark report is internally inconsistent.** Its summary claims
  a zero optimality gap on every synthetic instance; its Table 6 shows two
  of eight missed (7.56% and 9.59%), and its conclusion says "seven of
  eight" and "six of eight". It compares Dirac-3S with classical solvers
  only, never with Dirac-3. It lists the interface as "cloud API" while
  every published notebook ran on-premises. **No source compares Dirac-3S
  with Dirac-3**, so "better answers" is not yet a documented claim.
- **The notebook QCi's notice pointed to.** No cloud-API Dirac-3S notebook
  was found. The cloud example code is the `qci-client` 5.0.3 page
  "dirac-3s"; the three live notebooks are on-premises benchmarks. A
  software-interface notebook was published on GitHub on 2026-09-28 and
  removed on 2026-09-30.
- **New since the 2026-09-24 scrape**: the press release (2026-10-01),
  `qci-client` 5.0.3 and its docs (2026-10-05), `eqc-direct` 2.0.3
  (2026-10-06, since yanked from PyPI, no reason given), `eqc-models`
  0.22.1 (2026-10-07). The user guide and the benchmark notebooks are dated
  2026-09-24 itself; whether they predate that day's scrape cannot be told.

The full findings list is a working file of this sprint and is not
committed. The source URLs are on the pages named above.

## What this changes in the backlog

- **F129, F95, F25, F30**: each still waits for F139. Each card's cost was
  derived on Dirac-3 and must be re-quoted from one measured Dirac-3S fit.
- **F104** (resolution screen): unchanged. The 200:1 limit is the same.
- **A new card is needed** for the client bump in question 5 (both
  packages, `sampler_type`, a device field on rows, the proxy-identity
  re-check). Any Dirac-3S run depends on it. F139 numbers it.
- **Questions for QCi**, for the team lead to send if wanted: (a) which
  configuration serves the cloud `dirac-3s` queue, base or base plus
  expansion; (b) whether `dirac-3` now runs on upgraded hardware; (c)
  whether Dirac-3S is billed differently; (d) whether the integer budget
  is still the sum of levels, and whether the limit is 16 or 17 levels;
  (e) whether this account may use the `dirac-3s` "special queues", and
  their hours.
