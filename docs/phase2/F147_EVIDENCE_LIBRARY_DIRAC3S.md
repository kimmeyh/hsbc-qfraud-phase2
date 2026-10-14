# What the Evidence Library Says Before the First Dirac-3S Fits (F147)

**Sprint 26 Task E**, 2026-10-14. Written with `scripts/edb_query.py`, the
read-only query tool this task built, against the evidence library as it
stood that day. The library was opened read-only; nothing was written to
it. Record ids are cited as `EDB: <id>`. Labels follow
`docs/phase2/DIRAC_UNDERSTANDINGS.md`.

**Who reads this**: the team lead, before approving F142's three Dirac-3S
stops (`docs/sprints/SPRINT_26_PLAN.md`, Task D). It says what the library
already holds that bears on how those fits will be read.

## Bottom line

1. **The B4 fidelity twin cannot be read as a hard test of the device.**
   The library records our own Phase 1 finding that CVQBoost's
   formulation is strictly convex on the simplex and nearly degenerate, so
   any solver reproduces its optimum (`EDB:
   dirac3-fidelity-test-is-near-trivial-on-convex-formulation`, PROJ,
   high). A Dirac-3S weight cosine inside Dirac-3's range says the device
   solved an easy problem the same way; it does not show the two devices
   are equivalent on hard ones. **Inferred**, from that record and from
   amendment A31 (no coefficient difference on the frozen ULB pools is
   resolvable at 200:1), which the library does not yet hold. The
   leading alternative, that B4's sequential schedule-3 SPECTRA pools are
   harder than ULB's, is not ruled out: B4's recorded cosines on oilgas
   (0.892-0.901, `experiments/results/b4_hardware.json`,
   `weight_cosine_vs_classical`) sit well below the 0.975-0.999 the
   library records for ULB (`EDB:
   dirac3-matches-exact-optimum-on-convex-cvqboost`, HW). F142 reports
   the cosine as descriptive, as its plan already says.
2. **Read every returned sample, not only the best.** QCi's own Dirac-3S
   review warns that best-of-batch tables hide per-sample success rates
   as low as about one in ten (`EDB:
   dirac3s-best-of-batch-hides-low-per-sample-success`, QCi states), and
   QCi states the device is not an exact solver (`EDB:
   dirac3s-not-an-exact-solver`). F142's rows keep all samples (F133), so
   the per-sample spread is reportable at no extra device cost.
3. **A cost prior for stop 1, from QCi's table.** QCi gives 0.420 s per
   sample at relaxation schedule 2 on a 50-variable problem, without pre-
   and post-processing (`EDB: dirac3s-time-per-sample-by-schedule`, QCi
   states). At 8 samples that is about 3.4 s of sampling for B1 (91
   variables), beside B1's 4-5 s per fit on Dirac-3 (`results.json`,
   `hw_b1_dct`, `metered_seconds`). **Inferred**: QCi's figure excludes
   processing and is for a smaller problem; stop 1 measures the real
   cost, and every later stop is re-quoted from it.
4. **The resolution limit is the same stated figure.** The Dirac-3S guide
   repeats Dirac-3's 200:1 (23 dB) effective resolution (`EDB:
   dirac3s-analog-resolution-about-200-to-1`, QCi states; it supports
   `EDB: dirac3-analog-resolution-about-200-to-1`). So the B4 screen
   applies unchanged; Dirac-3S's effective resolution is unmeasured.

## What the library does not hold

Searched 2026-10-14, assertion values and ids, case-insensitive: "b4",
"spectra", "dynamic range", "per fit", "device_type", "sampler_type",
"fork", "billed", "oracle". None of these finds a record of:

- B4's measured dynamic range (8.1-8.4 dB) or its weight cosines;
- Dirac-3's per-fit cost at our sizes (B1 4-5 s, B2 71-92 s);
- A31: on the frozen ULB pools no coefficient difference is resolvable
  at 200:1, so agreement there carries no fidelity information, and B2's
  diffuse weights fall below the weight resolution;
- how Dirac-3S is selected (`device_type="dirac-3s"`).

These are proposed in `docs/phase2/EDB_PROPOSALS.md` (P4), for a session
in that repository to decide.

## Records cited

All read 2026-10-14 with `python scripts/edb_query.py show <id>`.

- `dirac3-fidelity-test-is-near-trivial-on-convex-formulation`
- `dirac3-matches-exact-optimum-on-convex-cvqboost`
- `dirac3s-best-of-batch-hides-low-per-sample-success`
- `dirac3s-not-an-exact-solver`
- `dirac3s-time-per-sample-by-schedule`
- `dirac3s-analog-resolution-about-200-to-1`
- `dirac3-analog-resolution-about-200-to-1`
