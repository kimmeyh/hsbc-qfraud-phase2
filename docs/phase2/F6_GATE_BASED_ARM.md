# F6: a gate-based arm on Braket, what is possible and what is worth doing

Sprint 27 Task H, 2026-10-18. A written analysis, not a build. Zero metered
seconds; no paid AWS service was called.

## BLUF

**Recommendation: pursue narrowly, meaning simulation only.** Run F106
and F107 on a local NumPy statevector, at zero cost. F106 sets a
sandwich-encoded circuit against the complete classical bar on identical
phase features. F107 predicts, from sampled shots, where shot noise
would erase what the circuit learned. Plan no Braket hardware time from
this analysis; F116 and F117 stay on HOLD.

- **Why not decline.** The proposal's section 7 commits to a gate-based
  arm, and one cheap, falsifiable test answers whether the arm has any
  work to do. It costs nothing metered.
- **Why not pursue fully.** At every width we can afford, the circuit is
  exactly simulable on a laptop, so no hardware result can show a
  computational effect. Any value lies in the circuit's hypothesis class,
  and a classical simulation answers that question completely. Hardware
  would add noise and cost, nothing else.
- **The stated risk is real.** Phase 1's null came from a formulation in
  which the solver had nothing to win (a convex objective). A gate-based
  classifier moves the question from "can the device optimize better"
  to "does this circuit's function class fit fraud better". The Fourier
  Wall paper predicts that payments data refuses that second question too.
  F106 tests the prediction directly instead of assuming it.

Each claim below carries a label: Measured, Inferred or Unverified
(Phase 2 draft, section 2).

## 1. Which encodings are not provably classical

- **Provably classical (a published theorem, not our measurement).** The Inverse Born Rule
  Equivalence (Zajac et al., arXiv:2602.21350v2, Theorem 1): any
  real-valued amplitude encoding, composed with a data-independent unitary
  and a basis measurement, yields exactly the classical quadratic forms
  `c(x)^T A c(x)`. Probability loading, general real amplitude encoding,
  plain `Ry` angle encoding with CNOTs, and `Ry`-only re-uploading all
  have phase complexity C = 0 and a zero Berry connection (its Table 3).
  Angle encoding stays useful, because its basis is trigonometric, but its
  function class is a finite Fourier series that a classical model can
  write down.
- **Not provably classical.** Encodings with data-dependent complex
  phases: the sandwich encoding `RY(x/2) e^{-i lambda ZZ} RY(x/2)` and
  Hamiltonian encoding `e^{-iH(x)t}` (C = 0.26 and 0.11 in its Table 3).
  Data re-uploading also escapes the theorem, by breaking its
  data-independent premise.
- **"Not provably classical" is not "quantum".** The theorem is one-sided:
  C = 0 rules an effect out; C > 0 is necessary, not sufficient (its
  section 7). The Fourier Wall paper (arXiv:2607.15815) supplies the other
  side: an angle-encoded circuit is a partial Fourier series, and an
  entangling encoding only adds joint frequencies. Trained-frequency GAM
  and GA2M, trees, an order-matched joint twin and random Fourier features
  each dequantize one region of that spectrum. A circuit is a candidate
  only where all of them fail at once (its conditions C1-C5).
- **So the first candidate is the sandwich encoding** with a nearest-
  neighbor ZZ ring. It has C > 0, it injects joint frequencies through its
  entangling layer, and the IBR paper's own experiments use it at 2-3
  qubits (its section 6).

## 2. What runs free, and what needs paid time

Checked 2026-10-18 against `aws.amazon.com/braket/pricing` and the Braket
developer guide's device list (the pages carry no effective date):

- **Free**: the SDK's local simulators (`braket_sv`, `braket_dm`), which
  run on our machine, and any NumPy statevector. No gate library is
  installed in this repository (`braket`, `qiskit`, `pennylane` and
  `classiq` absent, rechecked 2026-10-18), so F106 uses NumPy, as the
  IBR paper's own experiments did.
- **Paid, managed simulators**: SV1 at $0.075 per minute, billed per
  millisecond with a 3-second minimum per task; DM1 is listed. The free
  tier is one hour of on-demand simulation a month for the first 12
  months.
- **Paid, hardware**: $0.30 per task on every QPU, plus per shot: IQM
  Garnet $0.00145, IQM Emerald $0.0016, Rigetti Cepheus $0.000425, AQT
  IBEX-Q1 $0.0235, IonQ Forte $0.08 (2,500-shot minimum with error
  mitigation).
- **What that means for a classifier (Inferred, arithmetic).** Each
  scored row is a separate circuit, so a task per row. At 1,000 shots,
  one row costs $1.75 on IQM Garnet and $0.73 on Rigetti Cepheus; at
  IonQ Forte's 2,500-shot minimum it costs $200.30. Scoring ULB's test fold (about 57,000 rows) once would
  cost about $41,000 on Rigetti and $100,000 on Garnet, before any
  training. Even SV1's 3-second minimum is $0.00375 a row. Hardware
  scoring at Phase 1's scale is not affordable; at best a subsample of a
  few hundred rows is.

## 3. Does a gate formulation fix what Phase 1 hit, or move it

- **What Phase 1 hit (Measured).** CVQBoost's objective is a convex
  quadratic on the simplex. The classical proxy solves it exactly, so the
  device could at best match the proxy, and on resolvable pools it did
  (F142 stop 3; F144: Dirac-3 does not beat its own proxy on B2).
- **What a gate classifier changes (Inferred).** Its training landscape is
  non-convex, but nothing in this repository asks the device to optimize
  it better. The only route to a win is the circuit's function class:
  whether the encoded model fits fraud labels better than every classical
  model on the same features. That is a question about the data's
  spectrum, and the Fourier Wall's Tier 1 is built to answer it in
  minutes, without a circuit.
- **So the problem is relocated, not solved.** The Fourier Wall's own
  spec for fraud (`spectra-tier1-spec.md`, section 3) predicts `refuse`:
  chargebacks are an operational process, not an interacting physical
  one, and only three of the candidate phase fields are genuine cycles.
  That prediction is Unverified until F109 runs Tier 1 on ULB and
  IEEE-CIS (this sprint, Task G).
- **And width removes any computational claim (Inferred, from both
  papers).** F103's g5 budget is 14 qubits, one per encoded feature. A
  2^14 statevector is 16,384 amplitudes, which a laptop evaluates in
  milliseconds; F106's 8-qubit circuit has 256. The Fourier Wall paper
  says the same of its own 7-site result: "nothing quantum is claimed
  and no hardness exists at this width". A gate-based arm here
  can only test inductive bias, and the exact simulator reproduces any
  inductive-bias result.

## 4. Diagnostics that separate a real effect from a reparameterization

A circuit result counts as more than a reparameterization only if all
three hold, in this order (each is necessary):

1. **The encoding has quantum content**: phase complexity C > 0 and a
   nonzero Berry connection |A| over the data (IBR, Definitions 5-7). Mode
   mutual information I is reported but is not sufficient: `Ry`
   re-uploading has I = 0.72 with C = 0.
2. **No classical twin matches it on identical features**: the complete
   bar of the Fourier Wall paper, reused from F103 (logistic regression,
   trained-frequency GAM, GA2M, HGB, the k-way JOINT), plus a random
   Fourier feature surrogate (`sklearn.kernel_approximation.RBFSampler`).
   If any twin reaches the circuit within the margin set before the run,
   the circuit is dequantized.
3. **The effect is carried by the entangling encoding**: an ON minus OFF
   ablation of the ZZ layer, all else identical, with a paired interval
   (F116, on HOLD until 2 holds).

## 5. The cheapest falsifiable first experiment

**F106, simulation only, zero metered seconds.**

- **Encoding**: sandwich, `RY(phi_j / 2)` on each qubit, a ZZ ring with
  one trainable `lambda`, `RY(phi_j / 2)` again; three re-upload layers
  with trainable `Ry-Rz` rotations between them; readout `<Z_0>`.
- **Features**: the top 8 ULB features by Phase 1's selection
  (`data.top_k_features`), rank-phased by the Fourier Wall recipe (F103's
  `rank_phase`), so 8 qubits and a 256-amplitude statevector. The same
  phases go to every classical twin.
- **Data**: a stratified ULB subsample sized by a timing pilot; seeds
  42-46; AUPRC primary, with ROC-AUC beside it.
- **Margin, set before the run**: the Phase 2 draft's default, 0.005
  AUPRC (section 2b). Dequantized if the best twin's paired interval
  against the circuit lies above -0.005.
- **Falsifier**: the circuit is dequantized (stop; F116 stays on HOLD),
  or C = 0 on the data (the encoding was built wrong).
- **Cost**: zero metered; a few hours of laptop time. Hardware is not
  part of this experiment.

**F107 runs beside F106, also on the NumPy statevector.** Its output, the
critical Schmidt rank at each shot budget, is a prediction of a hardware
outcome, not a hardware result. It costs nothing, and it is the number a
later hardware decision would need. It informs that decision only if a
circuit survives F106.

## 6. What this does not settle

- **Unverified**: whether Tier 1 refuses ULB and IEEE-CIS. F109 settles
  it this sprint; a refusal makes F106's dequantization the expected
  outcome, not a reason to skip it.
- **Unverified**: Braket prices on any date after 2026-10-18; the pricing
  page carries no effective date.
- **Not covered**: Classiq, which the memo also names. The same width
  argument applies to any gate-based platform at these qubit counts.

## Sources

- Zajac, Cybulski, Dziewit, Kulpa, "The Inverse Born Rule Equivalence",
  arXiv:2602.21350v2, 14 Jun 2026: read in full from the evidence
  library's copy (`Papers/inverse-born-rule-2602.21350v2.pdf`; record
  `zajac-2026-inverse-born-rule-equivalence`).
- Mancilla and Tagliani, "The Fourier Wall", arXiv:2607.15815v1: sections
  2-6 and 9, read in full for F103.
- `spectra-tier1-spec.md` (Phase 1 project planning folders, read-only,
  team lead Decision 2, 2026-10-18).
- AWS, "Amazon Braket pricing", https://aws.amazon.com/braket/pricing/,
  and "Amazon Braket supported regions and devices",
  https://docs.aws.amazon.com/braket/latest/developerguide/braket-devices.html,
  both fetched 2026-10-18.
