# Red proofs and risk-based testing (Sprint 31 D8 follow-up)

Written 2026-11-05 at the team lead's request under D8: explain what the
red proofs are and why they run so often, and research risk-based
testing. D8's options are revised only after the team lead has read
this. Counts are from `docs/testing/F180_TEST_INVENTORY.md` as
generated on 2026-11-05.

## BLUF

- **A red proof is a test of a test.** It breaks the code a guard
  protects, runs the guard, and requires the guard to fail. It shows the
  guard CAN fail. It does not test the product.
- **The team lead's reading is correct.** A proof's answer can change
  only when its own test, the file it breaks, or the shared machinery it
  uses changes. Re-running an unchanged proof shows nothing new. All five
  recorded proof failures in Sprints 28-30 were of that kind.
- **This repository tests by habit, not by risk.** Every push runs every
  non-proof test. Every Phase 5 runs every proof. The inventory labels
  some files "high impact", but nothing uses the label to choose what runs.
- **Practice elsewhere** (ISTQB, Google, Microsoft): analyze what a
  change can affect, run those tests and the high-risk ones, and run
  everything on a set schedule as the safety net. Mutation checks (our
  proofs) run on changed code only. Google measured that only 1.23% of
  its test executions found a breakage, and set out to re-run the
  tests that almost never fail less often.

## 1. What a red proof is

A guard is an ordinary test that protects something: for example
`test_evidence_immutability.py` fails if Phase 1 evidence is written. A
guard that cannot fail is worse than none, because it reads green while
protecting nothing. This happened three times in two sprints (CLAUDE.md,
"Prove it FAILS").

A red proof (`injection.assert_can_fail`) does four things:
1. It edits one named file: a `Mutation(file, target, replacement)`,
   for example removing a line of the check the guard protects.
2. It confirms the edit landed (the target is gone, the bytes changed).
3. It runs the guard in a fresh pytest process and requires it to FAIL.
4. It restores the file's exact bytes.

The per-file proof counts are in the inventory's "Proofs" column.
Each proof starts a new Python process; on this workstation a start with
the scientific imports takes 18-22 s, which is why a full local proof
run is projected at about 8 hours (F180 analysis, Part 2).

The technique is mutation testing, applied by hand to chosen lines:
inject a fault and check that a test detects it (the method Petrovic
and Ivankovic describe at Google, ICSE-SEIP 2018).

## 2. When a proof's answer can change

A proof's result depends on:
- **a. its test file** (the assertion can be weakened);
- **b. the file it mutates** (the target can move, so the mutation no
  longer matches; `expect_occurrences` turns this into an error);
- **c. the shared machinery**: `injection.py`, `conftest.py`;
- **d. anything else the guard reads**: a helper module it imports, a
  data file, a fixture, a library version.

a, b and c can be found from `git diff` against `origin/develop`. d
cannot be found exactly without tracing what each test reads. The five
recorded proof failures in Sprints 28-30 were all a, b or c (F180
analysis, Part 5; inferred from the recorded cases only).

So the answer to "do they need to run so often": **no, not for the
reason they run now.** An unchanged proof re-run proves again what it
proved last time. The one reason to re-run all of them occasionally is
case d, and that needs a scheduled full run, not one per change.

## 3. Risk-based testing: what the sources say

**ISTQB Certified Tester Foundation Level v4.0.1** (2024-09-15), the
standard syllabus:
- Principle 2: exhaustive testing is impossible; test techniques, test
  case prioritization and risk-based testing should focus the test
  effort.
- Section 5.2.1: a risk has a likelihood and an impact; together they
  give the risk level, and "the higher the risk level, the more
  important is its treatment".
- Section 5.2.3: product risk analysis exists "to focus the test effort
  in a way that minimizes the residual level of product risk".
- Section 5.2.4: responses include mitigation by testing and also risk
  acceptance; mitigation means choosing the test techniques, coverage
  levels and test types for each risk.
- Section 2.2.3: "It is advisable first to perform an impact analysis to
  recognize the extent of the regression testing." Automated regression
  tests belong in CI.

**Microsoft, Test Impact Analysis** (Azure Pipelines documentation,
updated 2026-05-07): for each commit it runs only the impacted tests,
plus previously failing and newly added ones. When it cannot tell what a
change affects, it falls back to running all tests. It recommends
running all tests "at a configured periodicity", and checking the
selection by running both the selected tests and the full suite.

**Google, TAP** (Memon, Gao, Nguyen, Dhanda, Nickell, Siemborski and
Micco, "Taming Google-Scale Continuous Testing", ICSE-SEIP 2017; read
from the paper): TAP runs the tests a change affects. Of 5.5 million
affected tests in the period studied, only 63K ever failed; only 1.23%
of test executions found a breakage; tests more than 10 dependency
edges from the changed code "hardly ever break". The paper's goal was
to re-run tests that are "highly unlikely to fail" less often. This is
the likelihood half of risk, measured from history.

**Google, mutation testing** (Petrovic, Ivankovic, Fraser and Just,
"Practical Mutation Testing at Scale", IEEE TSE 2021): mutants are made
"only [in] changed code during code review, rather than the entire code
base"; used by more than 24,000 developers on more than 1,000 projects.

**Agile practice.** The ISTQB syllabus places automated regression tests
in each iteration's CI. In the sources above the common pattern is one
fast, selected set per change and the full set on a schedule. Not found:
a primary source that sets a frequency for that full run. Microsoft
leaves it to configuration.

Not verified: secondary sources claim risk-based testing finds a set
percentage more critical defects; no primary study was found, so no
figure is used here.

## 4. This repository against that practice

What is risk-based today:
- The inventory gives each file a risk tier; the "high" files guard
  documents of record, evidence, confidentiality and metered runs
  (`HIGH_IMPACT` in `scripts/test_inventory.py`). That is impact only;
  no likelihood is recorded.
- Metered device runs carry the strictest control (Criterion H): the
  highest-impact risk gets the strongest response.

What is not:
- **Selection by change: none.** Every push runs every non-proof test,
  whatever the change touched: a typo fix in a document runs the
  hardware guards.
- **Proofs by change: none.** Every Phase 5 runs every proof.
- **Likelihood: not used.** The inventory records each file's last fix,
  which is a likelihood signal (ISTQB principle 4: defects cluster), but
  nothing reads it.
- **Risk acceptance: never stated.** ISTQB lists accepting a risk as a
  response. Here every test is treated as must-run every time, so the
  cost of a low-risk test equals that of a high-risk one.

## 5. What a risk-based policy would look like here (for discussion, not yet options)

- **Per change (push)**: the tests the changed files can affect (by
  file: a test file, the modules it imports, the documents it reads),
  plus every high-impact guard always, plus any test that failed last
  time. If the change touches something the selection cannot reason
  about (a hook, `conftest.py`, the lock file, CI), run everything:
  Microsoft's "safe fallback".
- **Proofs**: only those whose test file, mutated file or shared
  machinery changed (D8's change b).
- **Scheduled full run**: every test and every proof, once per sprint on
  CI's full job at Phase 5 (D8's change a), as the net for case d.
  Measured 12:06 on CI.
- **Likelihood**: raise a file's tier while it has had a fix within the
  last few sprints; this is what the inventory's "last fix" column
  supports. Google's measure (how often a test has ever failed when
  affected) is the same idea at scale.
- **Check the selection**: per Microsoft, compare a selected run against
  the full run on the same commit at least once, and record any test the
  selection missed.

## Sources

- ISTQB, Certified Tester Foundation Level Syllabus v4.0.1 (2024-09-15):
  https://www.istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf
  (principles 2 and 4; sections 2.2.3, 5.2.1, 5.2.3, 5.2.4)
- Microsoft Learn, "Use Test Impact Analysis", Azure Pipelines (updated
  2026-05-07):
  https://learn.microsoft.com/en-us/azure/devops/pipelines/test/test-impact-analysis
- Memon et al., "Taming Google-Scale Continuous Testing", ICSE-SEIP 2017:
  https://huang.isis.vanderbilt.edu/cs8395-f23/paper/google-testing-icse-seip-17.pdf
- Petrovic, Ivankovic, Fraser and Just, "Practical Mutation Testing at
  Scale: A view from Google", IEEE TSE 2021:
  https://research.google/pubs/practical-mutation-testing-at-scale-a-view-from-google/
- Petrovic and Ivankovic, "State of Mutation Testing at Google",
  ICSE-SEIP 2018 (cited in the F180 analysis, Part 5).
