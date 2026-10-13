<!-- Committed 2026-10-13 (Sprint 25 Phase 5) so the web-source claims in DIRAC_3S_RESEARCH.md can be traced. Written by a background research agent on 2026-10-13; one notebook quote that carried a QCi employee's home-directory path is shortened. -->

# F138 site sweep: Dirac-3 / Dirac-3S changes since 2026-09-24

Sweep date: 2026-10-13. Read-only. No QCi API call was made. Pages were fetched with curl and
the PDFs were read with pypdf. The client packages were compared by downloading the PyPI source
archives (qci-client 5.0.2 vs 5.0.3, eqc-models 0.21.0 vs 0.22.1) and diffing them. No package
code was run.

Labels used below:
- **States**: the source says this, and the quote is verbatim.
- **Inference**: my reading or comparison. The source does not say it.
- **Derived from package source**: read from the PyPI sdist, not from a web page.

Abbreviations for the long URLs:
- `QCDOC` = https://quantumcomputinginc.com/learn/developer-resources/entropy-quantum-optimization/qci-client-software-package/v5.0.3/dirac-3s-dirac-3s
  (the "latest" path, `.../qci-client-software-package/latest/dirac-3s-dirac-3s`, serves the same text)
- `UG3S` = Dirac-3S User Guide PDF, September 2026 Rev A, doc QCi-QMS-900-000001, PDF CreationDate 2026-09-24 16:32Z:
  https://downloads.ctfassets.net/i1dyhzbyi8ad/2VeAf10vbdBBmVTpsuXdHt/8a48612546bf80fe0a30538d77bc60f3/Dirac_3S_Users_Guide_Rev_A-1.pdf
- `BENCH` = Dirac-3S Technical Reference: Continuous Solver Benchmarking PDF, September 2026 Rev A, doc QCi-QMS-900-000004, PDF CreationDate 2026-09-23 17:17Z:
  https://assets.ctfassets.net/i1dyhzbyi8ad/4RB85lp462hwxVlZeU8HAq/29abae2661809867dc42dbfaa6b6239b/Dirac_3S_Continuous_Solver_Benchmarking.pdf
  (a second asset URL, `.../3OHZKqDGOW9q2UuXVRqrA3/.../Dirac_3S_Continuous_Solver_Benchmarking.pdf`, is byte-identical)
- `PROD` = https://quantumcomputinginc.com/products/systems/dirac-3 (page title is now "Dirac-3S - Quantum Computing Inc")
- `PR` = https://quantumcomputinginc.com/news/press-releases/2026/quantum-computing-inc.-announces-dirac-3s-advancing-speed-scale-and-solutions-for-quantum-optimization
  (dated OCTOBER 01, 2026; the PR Newswire copy at https://www.prnewswire.com/news-releases/quantum-computing-inc-announces-dirac-3s-scaling-to-nearly-10-000-variables-302895913.html, "Oct 01, 2026, 08:30 ET", has the same text)
- `UG3` = old Dirac-3 User Guide PDF v0.0.04, CreationDate 2025-05-19, used only as a baseline:
  https://assets.ctfassets.net/i1dyhzbyi8ad/55XZTIVzzgNorw3OT6SrLF/f728a6ac69c41900bd9344cb36c96008/Dirac_3_Users_Guide_v0_0_04.pdf

---

## 1. Separate device or upgrade? How a user selects it

The sources disagree on the wording. I report all of them and do not choose one.

- **F1 (States).** The client docs call it a second-generation Dirac-3 device, selected by name.
  URL: QCDOC. Quote: "dirac-3s is QCi's second generation Dirac-3 device." No page date (qci-client v5.0.3 docs).
- **F2 (States).** The client docs say it runs the same two qudit problem types as dirac-3.
  URL: QCDOC. Quote: "It runs the same two qudit problem types as dirac-3, namely the normalized-qudit (continuous) and qudit (integer)"
- **F3 (States).** The press release calls it the next generation of Dirac-3, and calls the first shipment an "upgrade".
  URL: PR. Quotes: "today announced Dirac-3S, the next-generation of its Dirac-3 quantum optimization machine" and "First customer shipment of Dirac-3S upgrade expected in Q4 2026". Date: 2026-10-01.
- **F4 (States).** The press release calls Dirac-3 the "first-generation" machine.
  URL: PR. Quote: "Dirac-3S builds on QCi's first-generation Dirac-3 quantum optimization machine". Date: 2026-10-01.
- **F5 (States).** The product page keeps the Dirac-3 URL, but its title and content are now Dirac-3S.
  URL: PROD. Quote (meta description): "Introducing the Dirac-3S, QCi's latest quantum optimization machine". No page date.
  **Inference:** Dirac-3S is a separate cloud device name (`dirac-3s`) next to `dirac-3`. As hardware, it is sold as the next generation of Dirac-3. No source says that cloud Dirac-3 is retired or replaced.
- **F6 (States).** Selection is by `device_type="dirac-3s"` in `job_params`, passed to `build_job_body`.
  URL: QCDOC. Quote: "Pass device_type=\"dirac-3s\" in the job_params dictionary given to build_job_body"
- **F7 (States).** Job type names do not change: `sample-hamiltonian` (continuous) and `sample-hamiltonian-integer` (integer).
  URL: QCDOC. Quote: "dirac-3s accepts both qudit job types."
- **F8 (States).** Every other job type is rejected on dirac-3s.
  URL: QCDOC. Quote: "Every other job type is restricted to qubit devices. Pairing one with dirac-3s raises ValueError"
- **F9 (States).** `dirac-3s` is passed through literally. `dirac-3` is an alias that the client rewrites to `dirac-3_normalized_qudit` or `dirac-3_qudit`.
  URL: QCDOC. Quote: "dirac-3s is passed through literally and is never rewritten."
- **F10 (States).** Job metrics are keyed by the submitted device name, so code must not hardcode "dirac-3".
  URL: QCDOC. Quote: "job metrics, which are keyed by the device name that was actually submitted rather than the one that was requested"
- **F11 (States).** The valid device names listed in the client error message.
  URL: QCDOC. Quote: "must be one of ('dirac-1', 'dirac-3', 'dirac-3s', 'dirac-3_normalized_qudit', 'dirac-3_qudit')"
- **F12 (States).** In eqc-models, the switch is `sampler_type="dirac-3s"` on a Dirac-3 solver class.
  URL: https://pypi.org/project/eqc-models/0.22.1/ (sdist `eqc_models/solvers/qciclient.py`, derived from package source). Quote: "only allowed value is 'dirac-3s'." The shipped script `scripts/check_dirac3s.py` uses `Dirac3ContinuousCloudSolver(sampler_type="dirac-3s")`.
- **F13 (States).** The minimum client version is qci-client 5.0.3. `dirac-3s` does not exist in 5.0.2.
  URL: https://pypi.org/project/qci-client/5.0.3/ (derived from package source, `qci_client/optimization/enum.py`). The 5.0.2 enum has `DIRAC3_2 = "dirac-3.2"`; 5.0.3 replaces it with `DIRAC3S = "dirac-3s"`. eqc-models 0.22.1 also pins `qci-client>=5.0.3, <6`.

## 2. Variable ceilings: continuous and integer, Dirac-3S vs Dirac-3

- **F14 (States).** Dirac-3S hardware ceilings by polynomial order, for the base configuration and for base plus 1 expansion module: 2nd order 949 / 9980; 3rd order 135 / 580; 4th order 39 / 145; 5th order 19 / 55.
  URL: PROD and UG3S Table 2. Quote (UG3S): "Max number of variables 2nd Order 949 9980". UG3S date: September 2026 Rev A.
- **F15 (States).** The old Dirac-3 ceilings are 949 / 949 / 135 / 39 / 19 for orders 1 to 5 (quasi-continuous).
  URL: UG3. Quote: "Order of Correlation Maximum Number of Variables (Quasi-continuous) First 949 Second 949 Third 135". The Dirac-3 spec sheet also states 949.
  URL: https://quantumcomputinginc.com/learn/support/spec-sheets/dirac-3-spec-sheet. Quote: "Maximum Number of Variables 949".
  **Inference:** the Dirac-3S base configuration has exactly the Dirac-3 ceilings at every order. All of the gain comes from the expansion module.
- **F16 (States).** The press release frames "nearly 10,000" as a 10x increase over a 1,000-variable system, and conditions it on one expansion module.
  URL: PR. Quotes: "a 10x increase over QCi's current 1,000-variable system" and "configurations supporting up to 9,980 variables with one Expansion Module".
- **F17 (States).** The 9,980-variable demonstrations were quadratic (StQP), continuous, with sum constraint R = 100, relaxation_schedule 1, and best of 10 samples.
  URL: BENCH section 3.2 and 4.2. Quotes: "R sum constraint (fixed at100)" and "We ran Dirac-3S onrelaxation_schedule=1." (spacing as extracted from the PDF)
  **Inference:** "nearly 10,000 variables" applies to 2nd-order continuous problems on base + 1 expansion module. It does not apply to higher orders (580 at 3rd order) or to the base unit (949).
- **F18 (States).** Additional expansion modules are possible, but no ceiling is given for them.
  URL: UG3S Table 2 footnote. Quote: "Additional expansion configurations above 1 module can be customized to meet larger problem sizes."
- **F19 (States).** The continuous sum constraint range is R in [1, 10000]. This is unchanged from Dirac-3.
  URL: QCDOC. Quote: "Range: 1 to 10000, inclusive." (sum_constraint). The same range appears in UG3S Table 1 and in UG3.
- **F20 (States, internally inconsistent).** For the integer solver, UG3S Table 1 says v_i in {0, ..., 15}, but UG3S section 5.1 says 0 <= v_i <= 16.
  URL: UG3S. Quotes: "Integer Solverv i ∈{0, . . . , 15}" (Table 1) and "vi ∈N, 0≤v i ≤16" (section 5.1). Section 5.1 also says: "For problems requiring more than 16 states, the continuous solver is recommended."
  UG3 has the same 0 <= v_i <= 16 text. **Inference:** the per-variable level cap is 16 levels (values 0 to 15) or 17. The documents conflict, and no source settles it.
- **F21 (States).** There is a limit on the total number of integer levels, but no number is given.
  URL: removed software-interface notebook (see F59). Quote: "Total number of integer levels from input variables `num_levels` exceed limit" (error code 19).
  The same error code is also in UG3, so this limit is not new and not specific to 3S.
- **F22 (Unanswered).** The ceiling of the cloud `dirac-3s` device is not stated. The sources do not say whether the cloud device is a base unit (949) or base + 1 expansion module (9980). QCDOC gives no variable limit.

## 3. Supported polynomial degree

- **F23 (States).** Dirac-3S supports 2nd to 5th order correlation, on both configurations.
  URL: PROD. Quote: "Order of Correlation 2nd Order to 5th Order". The headline on PROD also lists "1st 2nd 3rd 4th 5th order problems".
- **F24 (States).** The objective is a polynomial with linear through quintic terms.
  URL: BENCH section 2.1. Quote: "directly optimizes polynomial objective functions containing first- through fifth-order interactions"
- **F25 (States).** The cloud client accepts degree above 2 on dirac-3s. The integer example uses max_degree 4.
  URL: QCDOC. Quote: "The polynomial spans degrees 2 through 4 over two variables, so every idx list has length 4"
  **Inference:** the supported degree did not change from Dirac-3. UG3 also listed orders 1 to 5. Only the per-order ceilings with an expansion module are new.

## 4. Relaxation schedules, num_samples, parameters and defaults

- **F26 (States).** num_samples: range 1 to 100, default 1.
  URL: QCDOC. Quote: "Range: 1 to 100, inclusive. Default: 1."
- **F27 (States).** The cap of 100 applies to cloud devices only. On-premises devices have no cap.
  URL: UG3S section 5.6. Quote: "User devices are not subject to the sample maximum of 100 that exists for cloud devices." This sentence is not in UG3.
- **F28 (States).** relaxation_schedule: range 1 to 4, default 1. It is a preset that tunes a group of device parameters.
  URL: QCDOC. Quote: "Tunes a group of device parameters as a preset. Higher schedules give better solution quality at the cost of longer"
- **F29 (States).** mean_photon_number range is 0.0000667 to 0.0066666. It overrides the schedule preset and is accepted by both job types.
  URL: QCDOC. Quote: "Advanced. Overrides the value that relaxation_schedule would otherwise set implicitly."
- **F30 (States).** quantum_fluctuation_coefficient range is 1 to 100. It is also an override.
  URL: QCDOC. Quote: "Advanced. Also overrides a value implied by relaxation_schedule."
- **F31 (States).** Defaults table in UG3S: QFC 1 (continuous) and 15 (integer); MPN 3.33e-4; schedule 1; samples 1; dynamic range "system-defined".
  URL: UG3S Table 3. Quote: "Mean Photon Number Sets the average optical energy level during optimization. 6.67×10 −5 to 6.67×10 −3 3.33×10 −4"
  **Inference:** these are the Dirac-3 values carried forward. UG3 gave per-schedule integer QFC values (schedule 3 = 33). UG3S lists only a flat 15, so that detail is lost or changed. No source says which is correct for 3S.
- **F32 (States, not new in 5.0.3).** MPN and QFC were already passed through in qci-client 5.0.2.
  Derived from package source: both 5.0.2 and 5.0.3 `client.py` copy `mean_photon_number` and `quantum_fluctuation_coefficient` into device_config.
- **F33 (States).** The client does not range-check values. The API rejects out-of-range values, and unknown keys are dropped silently.
  URL: QCDOC. Quote: "Unrecognized keys are dropped from the job body without warning"
- **F34 (States, not new in 5.0.3).** solution_precision is no longer supported and is ignored with a UserWarning.
  URL: QCDOC. Quote: "The solution_precision parameter is no longer supported." Derived from package source: the same warning is already in qci-client 5.0.2 (2026-08-11). Only the doc page is new.
- **F35 (States).** num_levels is required for integer jobs.
  URL: QCDOC. Quote: "Required by sample-hamiltonian-integer. Omitting it raises"

## 5. Precision, dynamic range, resolution

- **F36 (States).** Effective analog resolution is about 200:1, or 23 dB. Digital readout range is about 70 dB. This is unchanged text.
  URL: UG3S section 5.3. Quote: "effective analog resolution limit, which is approximately 200:1, or 23 dB." UG3 has the same sentence.
  **Inference:** the precision is not re-specified for 3S. UG3S section 5 still says "Dirac-3" in its body text.
- **F37 (States).** Coefficients and solutions are float32.
  URL: UG3S section 4. Quote: "Numbers, including integers, should be floats with 32-bit (or less) precision"
- **F38 (States).** The benchmark tested at about 10 dB and about 20 dB coefficient contrast. It says ub = 100 approaches the edge of the supported range.
  URL: BENCH section 3.2 and 4.2. Quotes: "Whenub is 10, the dynamic range is∼10 dB, and forub=100, the dynamic range is∼20 dB." and "even as problem coefficients approach the edge of the system's supported dynamic range"
- **F39 (States).** At larger R, precision falls because the number of resolution levels is fixed.
  URL: UG3S section 5.1. Quote: "increasing the solution space without increasing resolution granularity reduces effective precision."

## 6. Pricing, billing, runtime per sample

- **F40 (States).** Time allocation is sold in blocks and deducted by run time only. Queue time is not charged. The FAQ names Dirac-1, -2 and -3 only.
  URL: PROD FAQ. Quote: "can be used on any of Dirac-1, Dirac-2, or Dirac-3 that are available on QCi's cloud". No Dirac-3S billing statement was found anywhere.
- **F41 (States, documentation example).** The client doc shows the allocation balance falling from 600.0 s to 599.0 s for a 2-variable job.
  URL: QCDOC. Quote: "Dirac allocation balance = 599.0 s". **Inference:** the job IDs in that example are sequential placeholders (`...40001`, `...40002`), so treat it as illustrative and unverified.
- **F42 (States, new in UG3S).** Average time per sample by schedule, on a 50-variable sum-constraint problem, excluding pre- and post-processing: schedule 1 = 0.236 s, 2 = 0.420 s, 3 = 1.093 s, 4 = 1.278 s.
  URL: UG3S Table 4. Quote: "Schedule Average time per sample (s) 1 0.236 2 0.420 3 1.093 4 1.278". This table is not in UG3. UG3S does not say whether it was measured on 3S hardware.
- **F43 (States).** 9,980-variable planted instances: one sample took 232 s at ub = 10 and 144 s at ub = 100. Ten samples took 1691 s and 844 s. Times include pre-processing, device time and post-processing.
  URL: BENCH Tables 5 and 6. Quote: "Time reported for Dirac-3S includes pre-process + device-time + post-process"
- **F44 (States).** Per-sample device runtimes in the published notebooks: planted n = 2000, about 13.8 to 27.9 s; QPLIB_2761 (n = 500), about 2.4 to 5.5 s; keller4 (n = 171), about 1.8 to 2.3 s.
  URLs: https://quantumcomputinginc.com/learn/benchmarking/planted/dirac-3s-planted-benchmarking ; .../learn/benchmarking/qplib/dirac-3s-qplib-benchmarking ; .../learn/benchmarking/max-clique/dirac-3s-max-clique-benchmarking.
  Quote (planted): "Dirac-3 all samples runtimes:[27.94, 20.14, 18.12, 16.52, 21.61, 17.34, 16.28, 13.75, 16.34, 25.03]"
  **Inference:** for n = 2000 the notebook's best sample took 27.9 s, but BENCH Table 5 reports 12 s for one sample and 166 s for ten on what appears to be the same instance. These do not match, so the runs are probably different.
- **F45 (States).** Run time scales roughly linearly with problem size and with the schedule (old FAQ text, still on PROD).
  URL: PROD. Quote: "In general, the time required scales linearly to the size of the problem, but the selected schedule can have an effect"

## 7. Client library versions and changes

Breaking renames come first, because they affect existing code.

- **F46 (Derived from package source).** qci-client 5.0.3 REMOVED `DeviceType.DIRAC3_2 = "dirac-3.2"` and added `DIRAC3S = "dirac-3s"`. Code that used "dirac-3.2" breaks on upgrade.
  URL: https://pypi.org/project/qci-client/5.0.3/. Diff of `qci_client/optimization/enum.py`: `-    DIRAC3_2 = "dirac-3.2"` / `+    DIRAC3S = "dirac-3s"`.
- **F47 (Derived from package source).** eqc-models 0.22.1 REMOVED the `generation` keyword and added `sampler_type`. Code that used `generation=2` breaks.
  URL: https://pypi.org/project/eqc-models/0.22.1/. Quote (docstring): "optional value allowing the sampler type to be updated at run time, enabling access to special queues."
- **F48 (States).** qci-client 5.0.3 was uploaded 2026-10-05 and requires Python >=3.9, <3.14. 5.0.2 was uploaded 2026-08-11. There is no 5.0.1 on PyPI.
  URL: https://pypi.org/project/qci-client/ and https://pypi.org/pypi/qci-client/json. The docs dependencies page says: "qci-client v5.0.3 requires python >=3.9, <3.14."
- **F49 (Derived from package source).** Other 5.0.3 changes:
  (a) An `ssl_verify` argument and a `QCI_SSL_VERIFY` env var were added.
  (b) Integer jobs on `dirac-3s` are no longer forced to `dirac-3_qudit`, and `dirac-3s` was added to the qudit device set. In 5.0.2 the integer branch always remapped to `dirac-3_qudit`.
  (c) `get_job_metrics` now adds a "dirac-3" alias key next to the specific device key.
  (d) `build_job_body` docstring now documents the return value.
  A new test file, `tests/optimization/test_client_dirac3s.py`, was added. No changelog or release notes exist on PyPI or on the site.
- **F50 (States).** eqc-models 0.22.1 was uploaded 2026-10-07. It is the only 0.22.x release on PyPI; there is no 0.22.0. It requires Python >=3.10, <3.14.
  URL: https://pypi.org/pypi/eqc-models/json.
- **F51 (Derived from package source).** Other eqc-models 0.22.1 changes:
  (a) It now requires `qci-client>=5.0.3, <6` (was `>=5, <6`).
  (b) It adds `BinaryStQP` (`eqc_models/solvers/stqp.py`) and the `Dirac3BinaryStQPCloudSolver` and `Dirac3BinaryStQPDirectSolver` classes.
  (c) It adds the scripts `binary_stqp_small.py`, `binary_stqp_large.py` and `check_dirac3s.py`.
  The PyPI description still names only Dirac-1 and Dirac-3 solvers.
- **F52 (States).** The site's eqc-models docs lag behind PyPI: the "latest" docs download is v0.21.0.
  URL: https://quantumcomputinginc.com/learn/developer-resources/entropy-quantum-optimization/eqc-models-software-package/latest (download link `.../eqc-models-software-package/v0.21.0.zip`).
- **F53 (States).** eqc-direct 2.0.3 was uploaded to PyPI on 2026-10-06 and is YANKED. Latest non-yanked is 2.0.2. eqc-models 0.22.1 pins `eqc-direct==2.0.2` for Python < 3.11.
  URL: https://pypi.org/project/eqc-direct/. The benchmark notebooks ran on eqc-direct 2.0.3. Quote (planted notebook output, home-directory prefix removed): "eqc-direc-2.0.3/.venv/lib/python3.10/site-packages/eqc_direct/client.py:565"
- **F54 (States, inconsistent).** The software rows in the docs disagree.
  PROD says "qci-client API, Python ≥ 3.9 and < 3.14" for cloud. UG3S Table 2 says "On-cloud eqc-client API" (probably a typo for qci-client). UG3S section 6 says eqc-direct "supports Python version 3.8, 3.9, and 3.10", while PyPI eqc-direct requires ">=3.9,<3.11".

## 8. Queue and availability

- **F55 (States, two statements of different precision).** First customer shipment: the subhead says "Q4 2026" and the body says "November 2026". November is inside Q4, so the two are consistent.
  URL: PR. Quotes: "First customer shipment of Dirac-3S upgrade expected in Q4 2026" and "The first customer shipment of Dirac-3S is expected in November 2026."
- **F56 (States).** It can be deployed on-premises or in the cloud.
  URL: PR and PROD. Quote: "The platform can be deployed on-premises or in the cloud and integrated into AI/ML pipelines"
- **F57 (States).** The only Dirac-3S queue statement found is the eqc-models docstring about "special queues" (see F47). No public statement covers cloud queue availability, access eligibility or hours.
  **Inference:** "special queues" suggests that cloud `dirac-3s` access may be restricted. This is unverified.
- **F58 (States).** A trial cloud access page exists, but it gives no Dirac-3S terms.
  URL: https://quantumcomputinginc.com/products/systems/dirac-3/trial-cloud-access. Quote (meta): "Create an account and get access to the Dirac systems through our cloud environment."

## 9. Example notebooks

- **F59 (States).** A "Dirac-3S Technical Reference: Software Interface" notebook was added to GitHub qci-enablement/qci-data on 2026-09-28 (commit e3c71eb2) and REMOVED on 2026-09-30 (commit 3a5f62e2). I read it from git history. It is not live.
  It is an on-prem eqc-direct guide: device IP, lock, `solve_sum_constrained`, an error-code table and an admin CLI. Quote: "*September 2026, Revision A". The live web page https://quantumcomputinginc.com/learn/module/dirac-3s-technical-reference/dirac-3s-software-interface has no body text. Its "Download" link points to the benchmarking PDF, not to a software interface document.
- **F60 (States).** The three live Dirac-3S notebooks are benchmarks. They use on-prem eqc-direct, not the cloud API. They were committed 2026-09-24, 15:30Z to 16:25Z.
  URLs: see F44. Quote: "from eqc_direct.client import EqcClient" with `ip_address="172.18.15.110"`. Source: https://raw.githubusercontent.com/qci-enablement/qci-data/main/learn/Benchmarking/Planted/Dirac-3S%20Planted%20Benchmarking.ipynb (and the QPLIB and Max Clique equivalents).
  **Inference:** the cloud example code is the HTML page QCDOC. It contains a continuous example and an integer example. No cloud-API Dirac-3S notebook was found.

## 10. Benchmark and accuracy claims

- **F61 (Unanswered, direct answer).** No published source benchmarks Dirac-3S against Dirac-3. BENCH compares Dirac-3S only with Hexaly 15.0 and multi-start projected gradient descent.
  URL: BENCH section 1. Quote: "The T echnical Reference benchmarks Dirac-3S against two complementary classical baselines."
- **F62 (States).** Key finding: zero optimality gap on all synthetic instances from 2,000 to 9,980 variables.
  URL: BENCH section 1. Quote: "the only solver among the evaluated methods to achieve zero optimality gap across all synthetic benchmark instances"
- **F63 (States, contradicts F62).** In Table 6 (ub = 100), Dirac-3S missed 2 of 8 instances (gaps 7.56% and 9.59%). The conclusion gives a different count again.
  URL: BENCH section 6. Quote: "reaching the planted optimum on seven of eight instances atub=10and six of eight atub=100"
  **Inference:** Table 5 shows 0.0 gap on all 8 at ub = 10, section 5.2 says "all", and section 6 says "seven of eight". The paper is internally inconsistent. Also, the press release claim "the only evaluated solver to achieve the optimal solution across all tested instances" is not supported by Table 6.
- **F64 (States).** The max-clique advantage depends on taking the best of four schedules. With one fixed schedule the solvers are nearly identical.
  URL: BENCH section 6. Quote: "the maximum-clique advantage is a best-of-four-relaxation-schedules advantage."
  Quote: "When restricted to a single fixed schedule, the three solvers exhibit nearly identical aggregate performance."
- **F65 (States).** None of the three solvers competes with a dedicated max-clique algorithm.
  URL: BENCH section 5.3. Quote: "none of the three solvers is competitive with a dedicated combinatorial maximum-clique algorithm."
- **F66 (States).** On QPLIB, all solvers match the best known values to at least five significant figures. Dirac-3S placed 96 of 100 samples at the optimum on QPLIB_0018.
  URL: BENCH section 6. Quote: "ForQPLIB_0018, Dirac-3S places 96 of 100 samples at the optimum"
- **F67 (States).** At ub = 10, PGD is 3 to 63 times faster than Dirac-3S. At ub = 100 and n >= 6000, Dirac-3S is 1.4 to 7.1 times faster.
  URL: BENCH section 6. Quote: "Atub=10, PGD is 3–63 times faster than Dirac-3S while solving fewer planted instances to optimality"
- **F68 (States, inconsistent with F60).** BENCH Table 2 lists the Dirac-3S interface as "cloud API", but every published notebook uses on-prem eqc-direct over gRPC to a LAN IP.
  URL: BENCH Table 2. Quote: "Interface cloud API Python API NumPy". **Inference:** the 9,980-variable results were most likely produced on-prem.
- **F69 (States).** The benchmark covers simplex-constrained continuous quadratic problems only. QUBO, integer and mixed-integer reports are promised later.
  URL: BENCH section 1. Quote: "should not be interpreted as a comprehensive evaluation of all optimization problem classes."
- **F70 (States).** The product page claims the strongest overall performance on DIMACS.
  URL: PROD. Quote: "Dirac-3S achieved the strongest overall performance across the DIMACS benchmark suite."
- **F71 (States).** BENCH section 4.1 says the QPLIB runs used "Dirac-3", while the tables label them Dirac-3S.
  URL: BENCH section 4.1. Quote: "We run Dirac-3 onrelaxation_schedule=1with 100 samples." **Inference:** this is probably an editing slip, but it leaves the device identity of those runs uncertain.

---

## Pages found

All quantumcomputinginc.com pages were fetched with curl on 2026-10-13. These are Next.js pages; the body text is in the server-rendered HTML.

- 200 https://quantumcomputinginc.com/learn/module/dirac-3s-technical-reference (index only, no technical body)
- 200 https://quantumcomputinginc.com/learn/module/dirac-3s-technical-reference/dirac-3s-user-guide (no body text; embeds or links the UG3S PDF)
- 200 https://quantumcomputinginc.com/learn/module/dirac-3s-technical-reference/dirac-3s-software-interface (no body; meta "September 2026, Revision A"; Download link goes to the benchmarking PDF)
- 200 https://quantumcomputinginc.com/learn/developer-resources/entropy-quantum-optimization/dirac-3s-software-interface (same as above)
- 200 https://quantumcomputinginc.com/learn/module/dirac-3s-technical-reference/dirac-3s-benchmarking (links BENCH)
- 200 https://quantumcomputinginc.com/learn/module/dirac-3s-technical-reference/motzkin-straus-optimization-on-an-entropy-computing-platform (links PDF; PDF not extracted)
- 200 https://quantumcomputinginc.com/learn/module/dirac-3s-technical-reference/standard-quadratic-formulations-of-many-np-problems-a-simplex-based-compilation-framework-for-combinatorial-optimization (links PDF; PDF not extracted)
- 200 PROD https://quantumcomputinginc.com/products/systems/dirac-3
- 200 https://quantumcomputinginc.com/products/systems/dirac-3/trial-cloud-access
- 200 PR https://quantumcomputinginc.com/news/press-releases/2026/quantum-computing-inc.-announces-dirac-3s-advancing-speed-scale-and-solutions-for-quantum-optimization (dated 2026-10-01)
- 200 https://www.prnewswire.com/news-releases/quantum-computing-inc-announces-dirac-3s-scaling-to-nearly-10-000-variables-302895913.html (dated 2026-10-01 08:30 ET)
- 200 https://quantumcomputinginc.com/news (lists the Dirac-3S release, Oct 1, 2026; no other Dirac-3S news items)
- 200 https://quantumcomputinginc.com/learn (lists the Dirac-3S Technical Reference module)
- 200 https://quantumcomputinginc.com/learn/module/introduction-to-dirac-3 (no Dirac-3S content)
- 200 https://quantumcomputinginc.com/learn/support/spec-sheets/dirac-3-spec-sheet (Dirac-3 baseline, 949 variables)
- 200 https://quantumcomputinginc.com/learn/support/user-guides/dirac-3-user-guide (links UG3)
- 200 QCDOC .../qci-client-software-package/v5.0.3/dirac-3s-dirac-3s (and the .../latest/... copy)
- 200 https://quantumcomputinginc.com/learn/developer-resources/entropy-quantum-optimization/qci-client-software-package/v5.0.3
- 200 .../qci-client-software-package/v5.0.3/getting-started
- 200 .../qci-client-software-package/v5.0.3/basic-usage
- 200 .../qci-client-software-package/v5.0.3/dependencies
- 200 .../qci-client-software-package/v5.0.3/qci-client/qci-client.optimization (DeviceType enum includes DIRAC3S)
- 200 .../eqc-models-software-package/latest and .../latest/getting-started (docs at v0.21.0)
- 200 https://quantumcomputinginc.com/learn/benchmarking/planted/dirac-3s-planted-benchmarking
- 200 https://quantumcomputinginc.com/learn/benchmarking/qplib/dirac-3s-qplib-benchmarking
- 200 https://quantumcomputinginc.com/learn/benchmarking/max-clique/dirac-3s-max-clique-benchmarking
- 200 UG3S PDF (38 pages, created 2026-09-24 16:32Z)
- 200 BENCH PDF (24 pages, created 2026-09-23 17:17Z; two asset URLs, identical bytes)
- 200 UG3 PDF (Dirac-3 v0.0.04, created 2025-05-19; baseline only)
- 200 https://pypi.org/project/qci-client/ and /pypi/qci-client/json (latest 5.0.3, 2026-10-05)
- 200 https://pypi.org/project/eqc-models/ and /pypi/eqc-models/json (latest 0.22.1, 2026-10-07; no 0.22.0)
- 200 https://pypi.org/project/eqc-direct/ and /pypi/eqc-direct/json (2.0.3 uploaded 2026-10-06, YANKED; latest 2.0.2)
- 200 PyPI sdists: qci_client-5.0.2.tar.gz, qci_client-5.0.3.tar.gz, eqc_models-0.21.0.tar.gz, eqc_models-0.22.1.tar.gz (downloaded and diffed, not run)
- 200 GitHub API: repos/qci-enablement/qci-data commits since 2026-09-24 (11 commits):
  - 2026-10-06T16:09:40Z ce2367af Merge pull request #135 from qci-enablement/add-latest-qci-client-docs
  - 2026-10-06T15:53:16Z 5ff7ab1a Create v5.0.3.zip
  - 2026-10-01T12:06:48Z c1531bf3 Merge pull request #133 from qci-enablement/remove-data
  - 2026-10-01T12:05:42Z c2a4671f remove data
  - 2026-10-01T11:54:54Z ad1fdc72 Merge pull request #132 from qci-enablement/benchmarking-data
  - 2026-09-30T15:10:30Z 3a5f62e2 removed software interface
  - 2026-09-28T18:48:50Z e3c71eb2 added software interface
  - 2026-09-24T16:55:13Z 1c9dc6df Added benchmark-data notebooks
  - 2026-09-24T16:25:28Z 4f32e48f updated max click
  - 2026-09-24T15:43:41Z 85ea88b6 updated notebooks
  - 2026-09-24T15:30:46Z 90f7d08b adding benchmark data
- 200 https://raw.githubusercontent.com/qci-enablement/qci-data/e3c71eb2/learn/Developer-resources/Entropy-quantum-optimization/dirac-3s-software-interface.ipynb (removed 2026-09-30; fetched from git history)

Pages that appear new or changed since 2026-09-24, where a date is visible:
- PR and PR Newswire (2026-10-01).
- QCDOC and all qci-client v5.0.3 doc pages (v5.0.3.zip committed to qci-data 2026-10-06).
- qci-client 5.0.3 (2026-10-05), eqc-direct 2.0.3 (2026-10-06, yanked), eqc-models 0.22.1 (2026-10-07).
- Software-interface notebook (added 2026-09-28, removed 2026-09-30).
- qci-data commit c2a4671f "remove data" (2026-10-01): it removed the `benchmarking-data/*` notebooks, which were added 2026-09-24 16:55Z.
- Benchmark notebooks under `learn/Benchmarking/` and UG3S were created on 2026-09-24 itself. Whether they existed before or after the previous scrape that day cannot be told from the timestamps.
- The PROD page has no date. Its Dirac-3S content is consistent with the 2026-10-01 launch, but I could not verify when it changed.

## Unanswered

- Which hardware configuration (base 949 or base + 1 expansion 9980) the cloud `dirac-3s` device runs. Not stated anywhere.
- Whether Dirac-3S cloud time bills at the same rate as Dirac-3, or from the same allocation. The FAQ names only Dirac-1/2/3.
- Who can access the cloud `dirac-3s` device, and its queue or hours. Only "special queues" (eqc-models docstring) was found.
- The integer per-variable level cap (16 or 17 levels; see F20) and the total-levels limit (no number given).
- Any Dirac-3S vs Dirac-3 accuracy or speed comparison. None was published.
- Whether the UG3S parameter defaults (QFC, MPN) and Table 4 timings were measured on Dirac-3S hardware or carried forward from Dirac-3.
- Release notes or a changelog for qci-client 5.0.3 or eqc-models 0.22.1. None was found on PyPI or the site; the changes above come from diffing the source.
- Why eqc-direct 2.0.3 was yanked. PyPI gives no reason.

## Total

Total findings: 71 (F1 to F71). This includes 2 negative findings: F22 (cloud ceiling not stated) and F61 (no Dirac-3S vs Dirac-3 benchmark).
