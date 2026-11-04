"""F174's page generator (`scripts/f174_docs.py`): it renders the eight
IEEE-CIS pages from a result, and refuses one that its fixed text does
not describe. Each refusal is proven red, on a synthetic result. The
committed pages are checked against the recorded result: a committed page
that differs from the render fails.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
THIS = Path(__file__).relative_to(ROOT).as_posix()
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))

import f174_docs as f174d  # noqa: E402
import f166_ulb_algorithms as fu  # noqa: E402


CONSTANT = ("logreg", "svm")


def _result(n: int = 8) -> dict:
    op = {k: 0.5 for k in ("precision", "recall", "specificity", "f1", "mcc",
                           "balanced_accuracy")}
    conf = {"tp": 1, "fp": 2, "tn": 3, "fn": 4}
    rows = []
    for i in range(n):
        lanes = {}
        for j, a in enumerate(fu.ALGOS):
            # The test month's own budget is 450 rows; the proxy's ties
            # flag 455 on the first seed.
            flag = 455 if a == "proxy" and i == 0 else 450
            tp = 100 + 10 * j + (0 if a in CONSTANT else i)
            budget = {"budget": 0.005, "n_budget": 450, "n_flagged": flag,
                      "confusion": {"tp": tp, "fp": flag - tp,
                                    "tn": 86850 - (flag - tp), "fn": 3150 - tp}}
            lanes[a] = {"seed": 42 + i,
                        "outcome": {"at_budget_on_test": budget},
                        "tried": [{"params": g, "val_auprc": 0.1}
                                  for g in fu.GRIDS[a]],
                        "chosen_params": fu.GRIDS[a][0],
                        # logreg and svm are the same on every seed, as a
                        # deterministic lane on fixed months is.
                        "test": {"auprc": 0.9 - 0.1 * j + (
                                     0 if a in CONSTANT else 0.001 * i),
                                 "tie_fraction": 0.5,
                                 "score_health": {"mode_share": 0.4,
                                                  "warn": a == "proxy" and i == 0},
                                 "auprc_floor_normalized": 0.5, "auc_roc": 0.5,
                                 "recall_at_budget_on_test": 0.1,
                                 "train_test_auprc_gap": 0.0,
                                 "operating_points": [
                                     {"operating_point": "max_f1_on_val",
                                      "confusion": conf, **op},
                                     {"operating_point": "alert_budget_0.005",
                                      "confusion": conf, **op}]}}
        lanes["proxy"].update(build="serial", features=list("abcdefghijklm"),
                              n_learners=91)
        rows.append({"seed": 42 + i, "lanes": lanes, "minutes": 30.0,
                     "svm_rbf_alternative": {"beats_linear_on_validation": False}})
    analysis = fu.analyze(rows, {})
    order = analysis["order_by_mean_test_auprc"]
    analysis["adjacent_pairs"] = [
        {"a": a, "b": b, "primary": "wilcoxon", "wilcoxon": {"p": 0.5},
         "mean_diff": 0.1, "reading": "no reliable difference"}
        for a, b in zip(order, order[1:])]
    analysis["adjacent_pairs"][0]["reading"] = "above"
    controls = {"adversarial_rounds": 20, "adversarial_hit_round_cap": True,
                "final_adversarial_auc": 0.99}
    meta = {"train_months": [0, 1, 2], "eval_month": 3, "n_eval": 90000,
            "prevalence_eval": 0.035, "n_features": 171, "controls": controls}
    return {"dataset": "ieee_cis", "evidence_tag": "SIM", "metered_seconds": 0,
            "complete": True, "rows": rows, "analysis": analysis,
            "svm_rbf_grid": fu.RBF_GRID, "rbf_rows": fu.RBF_ROWS,
            "folds": {"validation": meta,
                      "test": {**meta, "train_months": [0, 1, 2, 3],
                               "eval_month": 4, "n_features": 181,
                               "controls": {**controls,
                                            "adversarial_hit_round_cap": False}},
                      "exact_duplicates_removed": 0}}


def test_the_eight_pages_render_beside_ulbs():
    res = _result()
    pages = f174d.render(res)
    assert sorted(pages) == sorted([*f174d.FILES.values(), "IEEE_COMPARISON.md"])
    assert not set(pages) & set(f174d.fd.FILES.values())
    a, b = res["analysis"]["order_by_mean_test_auprc"][:2]
    assert f"{f174d.NAMES[a]} above {f174d.INNER[b]}" in pages["IEEE_COMPARISON.md"]
    assert "is not established" in pages["IEEE_COMPARISON.md"]
    assert "about 3,150 frauds" in pages["IEEE_HGB.md"]


def _refused(change, match):
    res = _result()
    change(res)
    with pytest.raises(f174d.ClaimError, match=match):
        f174d.render(res)


def test_a_result_the_text_does_not_describe_is_refused():
    _refused(lambda r: r.update(dataset="ulb"), "not ieee_cis")
    _refused(lambda r: r.update(complete=False), "not complete")
    _refused(lambda r: r["analysis"]["svm_form"].update(kept="rbf"), "not linear")
    _refused(lambda r: [ln["lanes"]["proxy"].update(build="parallel, 8 workers")
                        for ln in r["rows"]], "built serially")
    # PR 74 review: these refusals had no test.
    _refused(lambda r: r.update(evidence_tag="HW"), "not SIM")
    _refused(lambda r: r.update(metered_seconds=4), "not 0")
    _refused(lambda r: r["analysis"]["adjacent_pairs"][0].update(
        primary="welch"), "not Wilcoxon")
    _refused(lambda r: r["analysis"]["adjacent_pairs"].pop(), "adjacent pairs, "
             "not")
    _refused(lambda r: r["analysis"]["adjacent_pairs"].reverse(),
             "not the result's order")
    small = _result(4)
    with pytest.raises(f174d.ClaimError, match="fewer than 8"):
        f174d.render(small)


def test_the_refusals_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    src = ROOT / "scripts" / "f174_docs.py"
    node = f"{THIS}::test_a_result_the_text_does_not_describe_is_refused"
    for old, new, label in (
            ("    if res.get(\"dataset\") != \"ieee_cis\":\n", "    if False:\n",
             "a ULB result rendered as IEEE-CIS"),
            ("    if not res.get(\"complete\"):\n", "    if False:\n",
             "an incomplete run rendered"),
            ("    if builds != {\"serial\"}:\n", "    if False:\n",
             "a parallel build described as serial"),
            ("    if res.get(\"evidence_tag\") != \"SIM\":\n", "    if False:\n",
             "a hardware result rendered as SIM"),
            ("    if res.get(\"metered_seconds\") != 0:\n", "    if False:\n",
             "a metered run rendered as zero seconds"),
            ("    if A[\"n_seeds\"] < 8 or any(p[\"primary\"] != \"wilcoxon\" "
             "for p in pairs):\n", "    if A[\"n_seeds\"] < 8:\n",
             "a non-Wilcoxon primary test rendered"),
            ("    if len(pairs) != N_PAIRS_TESTED:\n", "    if False:\n",
             "a missing pair rendered under the full divisor"),
            ("    if [(p[\"a\"], p[\"b\"]) for p in pairs] != list(zip(order, "
             "order[1:])):\n", "    if False:\n",
             "pairs out of the result's order rendered")):
        assert_can_fail([Mutation(src, old, new, expect_occurrences=1)],
                        lambda: run_pytest(node, ROOT), label)


def test_the_pages_do_not_alter_a_copy_of_the_result():
    res = _result()
    before = copy.deepcopy(res)
    f174d.render(res)
    assert res == before


def test_a_lane_the_same_on_every_seed_is_stated():
    res = _result()
    pages = f174d.render(res)
    for a in CONSTANT:
        assert "the 8 seeds are one result" in pages[f174d.FILES[a]]
    assert "seeds are one result" not in pages["IEEE_HGB.md"]
    comp = pages["IEEE_COMPARISON.md"]
    assert ("Logistic regression against SVM: both lanes are the same "
            "on every seed, so the 8 differences are one difference "
            "repeated." in comp)
    assert ("SVM against the proxy: SVM is the same on every seed, so the "
            "test compares the proxy's seeds with one fixed value." in comp)
    assert ("CatBoost against logistic regression: logistic regression is "
            "the same on every seed, so the test compares CatBoost's seeds "
            "with one fixed value." in comp)
    assert "HGB against LightGBM:" not in comp.split("Pairs with a lane")[1]
    # A reliable pair on a repeated lane is qualified in the BLUF.
    assert "rests on a lane" not in comp
    res["analysis"]["adjacent_pairs"][4]["reading"] = "above"
    bluf = f174d.render(res)["IEEE_COMPARISON.md"].split("\n")[2]
    assert ("Of these, Logistic regression above SVM rests on a lane whose "
            "test AUPRC is the same on every seed" in bluf)


def test_the_flagged_volume_ties_and_drift_are_stated():
    pages = f174d.render(_result())
    assert ("this threshold flags 3 of 90,000 test rows; the month's own "
            "0.5% budget is 450 rows." in pages["IEEE_HGB.md"])
    assert ("can catch at most 450 of its 3,150 frauds"
            in pages["IEEE_COMPARISON.md"])
    assert ("The score-health check warns on seed 42."
            in pages["IEEE_CVQBOOST_PROXY.md"])
    assert "score-health check" not in pages["IEEE_HGB.md"]
    comp = pages["IEEE_COMPARISON.md"]
    assert ("on the tuning fold it stopped at its cap of 20 rounds" in comp
            and "on the scored fold it converged within 20 rounds" in comp)
    assert "The tuning fold keeps 171 features and the scored fold 181." in comp


def _row(page, name):
    return next(ln for ln in page.splitlines() if f"| {name} |" in ln)


def test_the_confusion_counts_at_the_test_months_budget_are_stated():
    # Sprint 30 D8: each count's range over seeds on the comparison page,
    # each seed's counts on the algorithm page, and the tie note.
    res = _result()
    pages = f174d.render(res)
    comp = pages["IEEE_COMPARISON.md"]
    tp = 100 + 10 * fu.ALGOS.index("hgb")
    assert (f"| {tp} to {tp + 7} | {450 - tp - 7} to {450 - tp} | "
            f"{86850 - 450 + tp:,} to {86850 - 450 + tp + 7:,} | "
            f"{3150 - tp - 7:,} to {3150 - tp:,} |" in _row(comp, "HGB"))
    k = 100 + 10 * fu.ALGOS.index("svm")
    assert f"| {k} to {k} | {450 - k} to {450 - k} |" in _row(comp, "SVM")
    assert (f"| 43 | {f174d.fd.params(fu.GRIDS['hgb'][0])} "
            f"| 1 / 2 / 3 / 4 | 1 / 2 / 3 / 4 | {tp + 1} / {450 - tp - 1} / "
            f"{86850 - 450 + tp + 1} / {3150 - tp - 1} |" in pages["IEEE_HGB.md"])
    assert ("so a lane can flag more rows than the budget: the proxy on 1 of "
            "8 seeds, up to 455 rows against a budget of 450. The counts "
            "include those rows." in comp)
    for r in res["rows"]:
        r["lanes"]["proxy"]["outcome"]["at_budget_on_test"]["n_flagged"] = 450
    assert "can flag more rows" not in f174d.render(res)["IEEE_COMPARISON.md"]


def test_the_confusion_counts_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    node = f"{THIS}::test_the_confusion_counts_at_the_test_months_budget_are_stated"
    shared = ROOT / "scripts" / "f166_docs.py"
    for path, old, new, label in (
            (shared, "        out.append(f\"{min(v):,} to {max(v):,}\")\n",
             "        out.append(f\"{min(v):,} to {min(v):,}\")\n",
             "a range over seeds that drops its maximum"),
            (shared, "                if b[\"n_flagged\"] > b[\"n_budget\"]]\n",
             "                if b[\"n_flagged\"] >= b[\"n_budget\"]]\n",
             "a lane at the budget named as over it"),
            (ROOT / "scripts" / "f174_docs.py",
             "{fd.counts_cell(fd.at_budget(ln)['confusion'])} |\")\n",
             "{cells[1]} |\")\n",
             "the validation threshold's counts shown as the budget's")):
        assert_can_fail([Mutation(path, old, new, expect_occurrences=1)],
                        lambda: run_pytest(node, ROOT), label)


def test_the_new_statements_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    src = ROOT / "scripts" / "f174_docs.py"
    same = f"{THIS}::test_a_lane_the_same_on_every_seed_is_stated"
    rest = f"{THIS}::test_the_flagged_volume_ties_and_drift_are_stated"
    for old, new, node, label in (
            ("    if not same_every_seed(rows, a):\n", "    if True:\n", same,
             "a lane the same on every seed left unstated"),
            ("            if {p[\"a\"], p[\"b\"]} <= same:\n",
             "            if True:\n", same,
             "a pair with one repeated lane read as both repeated"),
            ("    if rel_rep:\n", "    if False:\n", same,
             "a reliable pair on a repeated lane left unqualified"),
            ("        out.append(c[\"tp\"] + c[\"fp\"])\n",
             "        out.append(c[\"tp\"])\n", rest,
             "the flagged volume counted from true positives only"),
            ("    if not warned:\n", "    if True:\n", rest,
             "the score-health warning left out"),
            ("        how = (\"stopped at its cap of\" if c[\"adversarial_hit_round_cap\"]\n",
             "        how = (\"stopped at its cap of\" if True\n", rest,
             "a converged drift control called capped")):
        assert_can_fail([Mutation(src, old, new, expect_occurrences=1)],
                        lambda node=node: run_pytest(node, ROOT), label)


def test_the_committed_pages_are_what_the_generator_renders():
    res = json.loads(f174d.RESULT.read_text(encoding="utf-8"))
    assert f174d.fd.differing(f174d.render(res), f174d.DOCS) == []


def test_the_page_check_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    page = f174d.DOCS / "IEEE_CVQBOOST_PROXY.md"
    assert_can_fail(
        [Mutation(page, "Here the same configuration (`full`) was chosen on "
                  "every seed.",
                  "and the chosen configuration changes between seeds.",
                  expect_occurrences=1)],
        lambda: run_pytest(
            f"{THIS}::test_the_committed_pages_are_what_the_generator_renders",
            ROOT),
        "a committed IEEE-CIS page that differs from the render")
