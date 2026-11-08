"""Figures in docs/phase2 that do not resolve in their document's own pool.

F164 (Sprint 29 Task C, #66). Read by `test_phase2_figures_resolve.py`,
whose docstring gives the rules. One entry per figure per document, each
with a reason. A figure leaves this file when it leaves its document or
starts to resolve (the test fails a stale entry).

"Recomputed 2026-10-26" means the figure was recomputed from the named
file when it was registered and matched. "Not recomputed" means the
reason states the derivation and nobody has checked it. Two figures were
wrong when checked and were corrected in their documents instead
(F108's plug-in ratios; F162's "recorded" wall time).
"""
from __future__ import annotations

# Result files a document draws on without naming them, with the reason.
SOURCES: dict[str, dict[str, str]] = {
    "F144_PROXY_TWIN.md": {
        "b2_hardware.json": "B2 device AUPRC and AUROC (the hw_b2_full rows "
                            "the text cites)",
        "tuned_pool.json": "the stored free proxy's ten-seed means",
    },
    "F139_RERUN_REVIEW.md": {
        "b2_hardware.json": "B2's device AUPRC, quoted in the deep-proxy "
                            "comparison",
    },
    "SPECTRA_IMPROVEMENT_RESEARCH.md": {
        "f17_emulator_validation.json": "the F17 cost model it quotes "
                                        "(F17_EMULATOR.md)",
    },
    "DIRAC_3S_RESEARCH.md": {
        "f17_emulator_validation.json": "the F17 cost model it quotes",
    },
    "sprints/SPRINT_29_VALIDATION.md": {
        "f108_ceiling.json": "the F108 plug-in ratios corrected in V3",
        "f160_room_ieee.json": "F160's gaps in V5",
        "f162_in_pocket.json": "F162's lane times in V3",
        "f166_ulb_algorithms.json": "F166's means and seed time in V6",
    },
}

# A document whose result file holds every algorithm's numbers draws only
# on its own part (PR 63 review: one pool for F166's eight documents
# covered 74.7% of the 3-place grid). Key paths; "*" is any item.
_F166 = "f166_ulb_algorithms.json"
_F166_SHARED = (("analysis", "adjacent_pairs"), ("seed_plan",), ("seeds",))


def _f166_algo(algo: str, *extra: tuple) -> dict:
    return {_F166: (("analysis", "per_algorithm", algo),
                    ("rows", "*", "lanes", algo), ("grids", algo),
                    *_F166_SHARED, *extra)}


SCOPES: dict[str, dict[str, tuple]] = {
    "algorithms/ULB_HGB.md": _f166_algo("hgb"),
    "algorithms/ULB_LIGHTGBM.md": _f166_algo("lightgbm"),
    "algorithms/ULB_XGBOOST.md": _f166_algo("xgboost"),
    "algorithms/ULB_CATBOOST.md": _f166_algo("catboost"),
    "algorithms/ULB_LOGISTIC_REGRESSION.md": _f166_algo("logreg"),
    "algorithms/ULB_SVM.md": _f166_algo(
        "svm", ("svm_rbf_grid",), ("rbf_rows",),
        ("rows", "*", "svm_rbf_alternative"), ("analysis", "svm_form")),
    "algorithms/ULB_CVQBOOST_PROXY.md": _f166_algo("proxy", ("proxy_build",)),
    "algorithms/ULB_COMPARISON.md": {
        _F166: (("analysis",), *_F166_SHARED, ("rbf_rows",),
                ("rows", "*", "svm_rbf_alternative"))},
}

_UG3S = "QCi's Dirac-3S user guide, quoted; not a result of ours"
_UG3S_T4 = ("QCi's Dirac-3S user guide, time per sample by schedule (50 "
            "variables); not a result of ours")
_BENCH = "QCi's Dirac-3S benchmark paper or notebooks, quoted; not ours"
_PYPI = "a package or Python version from PyPI or the client docs"
_NB = "a per-sample runtime printed in QCi's published notebook, quoted"
_BRAKET = "an Amazon Braket list price, quoted (F6 pricing survey)"
_SPECTRA_PAPER = "the SPECTRA paper's Table 2 or section 6.1, quoted"
_NOT = "not recomputed"

REGISTERED: dict[str, dict[str, str]] = {
    "DIRAC_3S_RESEARCH.md": {
        "0.236": _UG3S_T4, "0.420": _UG3S_T4, "1.093": _UG3S_T4,
        "1.278": _UG3S_T4,
        "3.04": "ratio of the guide's schedule 4 to schedule 2 time "
                "(1.278 / 0.420), arithmetic on quoted figures",
        "3.33": _UG3S + " (default mean photon number, 3.33e-4)",
        "6.67": _UG3S + " (mean photon number range, 6.67e-5 to 6.67e-3)",
        "7.56": _BENCH + " (Table 6 gaps)", "9.59": _BENCH + " (Table 6 gaps)",
        "1.8": _BENCH + " (on-premises per-sample time)",
        "2.3": "QCi's portfolio ratio range, quoted (2.3x-5.3x)",
        "5.3": "QCi's portfolio ratio range, quoted (2.3x-5.3x)",
        "3.4": "QCi's portfolio ratio, quoted (3.4x)",
        "2.4": _NB + " (QPLIB_2761, n = 500)",
        "5.5": _NB + " (QPLIB_2761, n = 500)",
        "0.6": "Phase 1's Dirac-3 per-sample cost, rounded from the "
               "hardware plan's measured costs; not recomputed",
        "11.27": "B2's per-sample cost at 833 variables (Phase 1 hardware "
                 "plan); not recomputed",
    },
    "DIRAC_3S_SITE_SWEEP.md": {
        "0.0": "a 0.0 gap in the benchmark paper's Table 5, quoted",
        "0.0000667": _UG3S + " (item F29, MPN range)",
        "0.0066666": _UG3S + " (item F29, MPN range)",
        "3.33": _UG3S + " (item F31, MPN default)",
        "6.67": _UG3S + " (Table 3, quoted)",
        "0.236": _UG3S_T4 + " (item F42)", "0.420": _UG3S_T4 + " (item F42)",
        "1.093": _UG3S_T4 + " (item F42)", "1.278": _UG3S_T4 + " (item F42)",
        "0.22": _PYPI + " (eqc-models 0.22.x)",
        "3.10": _PYPI, "3.11": _PYPI, "3.14": _PYPI, "3.9": _PYPI,
        "3.2": "the device name \"dirac-3.2\" removed from qci-client "
               "(item F46)",
        "3.8": "UG3S section number, quoted with the platform note",
        "4.2": "the benchmark paper's section number (sections 3.2 and 4.2)",
        "1.4": _BENCH + " (item F67, speed ratio range)",
        "7.1": _BENCH + " (item F67, speed ratio range)",
        "7.56": _BENCH + " (item F63, Table 6 gaps)",
        "9.59": _BENCH + " (item F63, Table 6 gaps)",
        "1.8": _NB + " (item F44)", "2.3": _NB + " (item F44)",
        "2.4": _NB + " (item F44)", "5.5": _NB + " (item F44)",
        "13.8": _NB + " (item F44)", "27.9": _NB + " (item F44)",
        "13.75": _NB, "16.28": _NB, "16.34": _NB, "16.52": _NB,
        "17.34": _NB, "18.12": _NB, "20.14": _NB, "21.61": _NB,
        "25.03": _NB, "27.94": _NB,
        "15.0": "Hexaly 15.0, a solver version named by the benchmark paper",
        "599.0": "the client documentation's allocation example (item F41)",
        "600.0": "the client documentation's allocation example (item F41)",
    },
    "DIRAC_UNDERSTANDINGS.md": {
        "-0.0032": "a CI endpoint quoted from QCI_EQC_MODELS_FEEDBACK.md "
                   "section 5; unsigned, it had matched 1/315 by chance "
                   "(PR 63 review); " + _NOT,
        "0.420": _UG3S_T4, "1.093": _UG3S_T4, "1.278": _UG3S_T4,
        "0.7926": "deep proxy ten-seed mean from results.json; matches "
                  "F144_PROXY_TWIN.md; not recomputed here",
        "1.3": "an inferred cost ratio, labeled Inferred in the text",
        "1.6": "how far a discarded two-point cost line missed, from the "
               "hardware plan's sizing calls; not recomputed",
        "4.5": "Dirac-3 B1 cost per fit, 99 s over 22 fits (text); "
               "arithmetic, not recomputed",
        "11.27": "B2's per-sample cost at 833 variables (Phase 1 hardware "
                 "plan); not recomputed",
        "2553.5": "the resolvable difference (energy range over the 0.005 "
                  "step) stated with its derivation; not recomputed",
    },
    "F103_TIER1_CHECK.md": {
        "0.548": _SPECTRA_PAPER, "0.582": _SPECTRA_PAPER,
        "0.587": _SPECTRA_PAPER, "0.699": _SPECTRA_PAPER,
        "0.910": _SPECTRA_PAPER, "0.999": _SPECTRA_PAPER,
        "9.9": "the SPECTRA paper's \"joint ratio\", quoted as undefined",
    },
    "F105_IEEE_HARNESS.md": {
        "0.60": "the audit's correlation target, a setting",
        "4.4": "wall-clock minutes of the controls, from the run log; "
               "timing keys are not evidence",
        "5.9": "wall-clock minutes of the controls, from the run log; "
               "timing keys are not evidence",
    },
    "F106_DEQUANTIZATION.md": {
        "0.533": "a ten-seed mean of the stored per-seed values; " + _NOT,
        "0.673": "RFF twin ten-seed mean AUPRC; " + _NOT,
        "0.699": "circuit ten-seed mean AUPRC; " + _NOT,
        "0.704": "GAM twin ten-seed mean AUPRC; " + _NOT,
        "2.39": "summed single-qubit entropy, ten-seed mean; " + _NOT,
        "99.17": "the interval level, 1 - 0.05/6 (the family's Bonferroni "
                 "split), a setting",
    },
    "F108_CEILING_VALIDATION.md": {
        "0.00002": "realized minus posterior Bayes error, per seed; " + _NOT,
        "1.053": "plug-in over Bayes error, seed 45; recomputed 2026-10-26",
        "1.097": "plug-in over Bayes error (seed 44 none arm; flip arm "
                 "maximum); recomputed 2026-10-26",
        "1.106": "plug-in over Bayes error, seed 42; recomputed 2026-10-26",
        "1.116": "plug-in over Bayes error, seed 46; recomputed 2026-10-26",
        "1.119": "plug-in over Bayes error, seed 43; recomputed 2026-10-26",
        "1.076": "plug-in over Bayes error, flip arm minimum; recomputed "
                 "2026-10-26",
        "1.105": "a superseded value, quoted in the 2026-10-26 correction",
        "1.114": "a superseded value, quoted in the 2026-10-26 correction",
        "1.118": "a superseded value, quoted in the 2026-10-26 correction",
        "1.075": "a superseded value, quoted in the 2026-10-26 correction",
        "1.098": "a superseded value, quoted in the 2026-10-26 correction",
        "1.75": "n_transactions in millions, minimum; recomputed 2026-10-26",
        "1.77": "n_transactions in millions, mean; recomputed 2026-10-26",
        "1.80": "n_transactions in millions, maximum; recomputed 2026-10-26",
    },
    "F109_TIER1_LADDER.md": {
        "0.079": "mean g4 gap before aggregation, from the pilot; " + _NOT,
        "0.112": "mean g4 gap after aggregation; " + _NOT,
        "0.679": "IEEE-CIS GAM seed mean, one aggregation; " + _NOT,
        "0.704": "IEEE-CIS GAM seed mean, the other aggregation; " + _NOT,
        "0.713": "an IEEE-CIS lane seed mean; " + _NOT,
        "0.731": "an IEEE-CIS lane seed mean; " + _NOT,
        "0.734": "an IEEE-CIS lane seed mean; " + _NOT,
        "0.816": "IEEE-CIS HGB seed mean; " + _NOT,
        "0.851": "telecom lane seed mean; " + _NOT,
        "0.878": "telecom lane seed mean; " + _NOT,
        "0.892": "ai4i lane seed mean; " + _NOT,
        "0.927": "a lane seed mean; " + _NOT,
        "0.944": "oilgas lane seed mean; " + _NOT,
    },
    "F110_SCALING.md": {
        "-0.2": "the P2 band's lower edge, a setting",
        "2.7": "2 to the build slope (1.437 at 833 variables gives 2.71); "
               "recomputed 2026-10-26",
        "82.4": "total_s of the 833-variable runs, seeds 43-46, in minutes; "
                "recomputed 2026-10-26",
        "735.4": "the hardware plan's Experiment 6 figure, quoted",
    },
    "F111_LOKE_PROTOCOL.md": {
        "0.051": "the published 0.8108 minus the protocol A mean (0.760); "
                 "arithmetic",
        "0.8108": "the source paper's published KNN AUC-PR, quoted",
        "34.8": "the pilot projection for protocol A, per seed; "
                "recomputed 2026-10-26 from the pilot block",
        "37.2": "the pilot projection for protocol B, per seed; "
                "recomputed 2026-10-26 from the pilot block",
        "82.5": "the sum of every row's seconds, in minutes; recomputed "
                "2026-10-26",
        "303.5": "a transaction amount named as an example duplicate",
    },
    "F113_ORACLE_GAP.md": {
        "1.05": "one fraud as recall points at 95 frauds a fold (100/95)",
        "2.1": "oracle gap in recall points, ten-seed minimum; " + _NOT,
        "3.6": "a mean gap in recall points; " + _NOT,
        "4.4": "recall points added by a stated reassignment; " + _NOT,
    },
    "F115_INTEGER_COST_SCALING.md": {
        "1.4": "probe_deep over probe_high levels, arithmetic on stored "
               "probe sizes; " + _NOT,
        "2.5": "probe_high over probe_deep variables (150 / 60)",
    },
    "F126_SPARSITY_RULE.md": {
        "0.008": "an across-seed SD range; " + _NOT,
        "0.033": "an across-seed SD range; " + _NOT,
        "0.07": "a rule's predicted zero fraction; " + _NOT,
        "0.17": "zero fraction range on two seeds; " + _NOT,
        "0.19": "zero fraction range on two seeds; " + _NOT,
        "0.553": "R2 table cell; " + _NOT,
        "0.61": "share of zeros among tied learners, by seed; " + _NOT,
        "0.943": "tie share by seed; " + _NOT,
        "0.945": "tie share by seed; " + _NOT,
        "1.020": "a threshold tau, a setting",
        "1.023": "tied weight times n, by seed; " + _NOT,
        "1.024": "a threshold tau, a setting",
        "1.025": "tied weight times n, by seed; " + _NOT,
    },
    "F130_LEVER_SCREENS.md": {
        "-0.008": "F151's interval endpoint, quoted from F151_HGB_COMPARATOR.md",
        "0.027": "F151's difference, quoted from F151_HGB_COMPARATOR.md",
        "-0.046": "F151's interval endpoint, quoted from F151_HGB_COMPARATOR.md",
        "0.8108": "the source paper's published KNN AUC-PR, quoted",
        "0.99": "a feature AUC range, quoted from F101_IN_POCKET_PROVENANCE.md",
    },
    "F139_RERUN_REVIEW.md": {
        "0.0072": "the device-to-proxy difference from the Phase 1 record; "
                  + _NOT,
        "0.7926": "deep proxy ten-seed mean from results.json; matches "
                  "F144_PROXY_TWIN.md; not recomputed here",
        "0.900": "the G0b Spearman correlation from the Phase 1 record; "
                 + _NOT,
        "8.1": "B4 Hamiltonian dynamic range in dB; " + _NOT,
        "8.4": "B4 Hamiltonian dynamic range in dB; " + _NOT,
    },
    "F142_DIRAC3S_VERIFY.md": {
        "0.0000001": "the step every returned weight is a multiple of, "
                     "read from the device responses",
        "0.032": "a weight's relative error, in percent; " + _NOT,
        "4.5": "Dirac-3 B1 cost per fit, 99 s over 22 fits; arithmetic",
    },
    "F144_PROXY_TWIN.md": {
        "-0.0003": "the ten-seed mean of device minus same-pool solve over "
                   "results.json's hw_b2_full rows; unsigned, it had matched "
                   "an unrelated 0.00026 by chance (PR 63 review); " + _NOT,
        "0.7678": "stored free proxy floor-normalized AUPRC, ten-seed mean "
                  "of f144_proxy_twin.json ref_stored; recomputed 2026-10-26",
        "0.7682": "Phase 1 mid cell ten-seed mean (results.json); " + _NOT,
        "0.7922": "twin floor-normalized AUPRC, ten-seed mean; recomputed "
                  "2026-10-26",
        "0.7925": "twin AUPRC, ten-seed mean; recomputed 2026-10-26",
        "0.7926": "Phase 1 deep cell ten-seed mean (results.json); " + _NOT,
    },
    "F147_EVIDENCE_LIBRARY_DIRAC3S.md": {
        "0.420": _UG3S_T4,
        "3.4": "8 samples times the guide's 0.420 s; arithmetic",
    },
    "F151_HGB_COMPARATOR.md": {
        "0.0849": "0.03 x sqrt(8), stated in the text; arithmetic",
        "0.246": "an SD from a probe the text names as not stored; " + _NOT,
    },
    "F152_EXP2_RESULT.md": {
        "0.003": "agreement with the pilot, a difference of means; " + _NOT,
        "0.021": "agreement with the pilot, a difference of means; " + _NOT,
    },
    "F162_IN_POCKET.md": {
        "28.5": "a wall time the result file does not record; marked "
                "unverified in the text",
        "20.5": "the sum of the rows' seconds, in minutes; recomputed "
                "2026-10-26",
    },
    "F17_EMULATOR.md": {
        "0.0034": "device-to-exact AUPRC difference, maximum; " + _NOT,
        "1.227": "the fitted cost constant c, 1.227e-4; " + _NOT,
        "2.2": "a ratio range, per seed; " + _NOT,
        "2.4": "a zero-fraction ratio; " + _NOT,
        "2.5": "the pre-correction range, quoted as corrected",
        "3.8": "the cost model's schedule-4 factor, a setting of the model",
        "41.2": "mean device metered seconds, oilgas; recomputed 2026-10-26",
        "82.4": "B2 cost per fit at 833 variables, 906 s over 11 fits; "
                "arithmetic",
        "86.8": "mean device metered seconds, telecom; recomputed 2026-10-26",
    },
    "F20_SOFT_VOTES_RESULT.md": {
        "1.9": "scikit-learn 1.9, a package version",
    },
    "F29_SAMPLE_SIZE.md": {
        "0.0024": "largest mean difference across fractions; " + _NOT,
        "0.0064": "largest within-seed difference; " + _NOT,
        "0.8049": "a repeat run's AUPRC, from results.json; " + _NOT,
        "0.8056": "a repeat run's AUPRC, from results.json; " + _NOT,
        "0.90": "mean L1 between random starts, quoted from a design note; "
                + _NOT,
        "0.99999999999994": "minimum cosine_to_full, floored; recomputed "
                            "2026-10-26",
    },
    "sprints/SPRINT_29_VALIDATION.md": {
        **{f: "a corrected F108 plug-in ratio or range end, as registered "
              "for F108_CEILING_VALIDATION.md; recomputed 2026-10-26"
           for f in ("1.106", "1.116", "1.119", "1.076", "1.097")},
        **{f: "a superseded F108 value V3 quotes as what was corrected; "
              "wrong by design"
           for f in ("1.105", "1.114", "1.118", "1.075", "1.098")},
        "20.5": "F162's lane seconds summed, in minutes, as registered for "
                "F162_IN_POCKET.md; recomputed 2026-10-26",
        "28.5": "F162's superseded wall time, quoted as what was corrected",
        "99.7": "this machine's commit limit in GB, read from Windows; "
                "not a result",
    },
    "F6_GATE_BASED_ARM.md": {
        "-0.005": "the dequantization threshold, the negative of the 0.005 "
                  "setting",
        "0.000425": _BRAKET, "0.00145": _BRAKET, "0.0235": _BRAKET,
        "0.075": _BRAKET, "0.08": _BRAKET, "0.30": _BRAKET,
        "0.00375": "SV1's 3-second minimum at $0.075 a minute; arithmetic",
        "0.73": "one row on Rigetti Cepheus at list prices; arithmetic",
        "1.75": "one row on IQM Garnet at list prices; arithmetic",
        "200.30": "a stated job's cost at list prices; arithmetic",
        "0.11": "a cited paper's Table 3 complexity value, quoted",
    },
    "F94_EXP3_CONTROLS.md": {
        "0.0016": "gap from best found to the floor (validation), per "
                  "instance; " + _NOT,
        "0.0018": "gap from best found to the floor, per instance; " + _NOT,
        "0.0021": "gap from best found to the floor, per instance; " + _NOT,
        "0.0023": "gap from best found to the floor, per instance; " + _NOT,
        "0.0025": "gap from best found to the floor, per instance; " + _NOT,
        "0.0026": "gap from best found to the floor, per instance; " + _NOT,
        "0.10": "test AUPRC moved by ties among equal selections; " + _NOT,
        "0.33": "data term share of the objective, in percent; " + _NOT,
        "99.63": "rows a learner pair agrees on, in percent; " + _NOT,
        "99.92": "rows a learner pair agrees on, in percent; " + _NOT,
    },
    "F114_REAL_CEILING.md": {
        "0.00049": "the check's distance, |estimate - test fraud rate| "
                   "(0.0011828 - 0.0016741) from f114_real_ceiling_lr05.json; "
                   "recomputed 2026-11-05",
    },
    "F157_QNN_IEEE.md": {
        "-0.005": "the entry's decision line, a preregistered threshold, "
                  "not a result",
        "99.17": "the Bonferroni interval level 1 - 0.05/6, in percent, a "
                 "preregistered setting, not a result",
    },
}
