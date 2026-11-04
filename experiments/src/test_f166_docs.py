"""F166's documents come from a tracked generator (Sprint 29 IMP-2).

`scripts/f166_docs.py` renders the eight pages in `docs/phase2/algorithms/`
from `f166_ulb_algorithms.json`. A committed page that differs from the
render fails here, and each statement the fixed text makes is computed
from the result or refused (`ClaimError`) when the result does not
support it.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "f166_docs.py"
THIS = Path(__file__).relative_to(ROOT).as_posix()
sys.path.insert(0, str(ROOT / "scripts"))

import f166_docs as fd  # noqa: E402


def _res():
    return json.loads(fd.RESULT.read_text(encoding="utf-8"))


def test_the_committed_pages_are_what_the_generator_renders():
    assert fd.differing(fd.render(_res()), fd.DOCS) == []


def test_the_limits_line_follows_the_seeds_choices():
    # The PR 63 review: the proxy page said the choice changes between
    # seeds, and `full` was chosen on every seed.
    res = _res()
    assert "Here the same configuration (`full`) was chosen on every seed." \
        in fd.algo_doc(res, "proxy")
    assert "the chosen configuration changes between seeds" \
        in fd.algo_doc(res, "hgb")
    for r in res["rows"]:
        r["lanes"]["hgb"]["chosen_params"] = {"max_leaf_nodes": 31}
    assert "Here the same configuration (max_leaf_nodes 31) was chosen" \
        in fd.algo_doc(res, "hgb")


def test_a_proxy_statement_the_result_does_not_support_is_refused():
    res = _res()
    res["rows"][3]["lanes"]["proxy"]["chosen_params"] = {"config": "mid"}
    with pytest.raises(fd.ClaimError, match="every seed"):
        fd.render(res)
    res = _res()
    res["rows"][0]["lanes"]["proxy"]["build"] = "serial"
    with pytest.raises(fd.ClaimError, match="parallel build"):
        fd.render(res)


def test_the_balanced_count_is_counted():
    res = _res()
    assert "No seed chose `class_weight` balanced." in fd.algo_doc(res, "svm")
    res["rows"][0]["lanes"]["svm"]["chosen_params"]["class_weight"] = "balanced"
    assert "1 of 10 seeds chose `class_weight` balanced." \
        in fd.algo_doc(res, "svm")


def test_the_comparison_statements_follow_the_result():
    res = _res()
    text = fd.comparison(res)
    assert ("the order among CatBoost, LightGBM, XGBoost, HGB and the proxy "
            "is not established") in text
    assert "HGB against the proxy has the smallest p" in text
    order = res["analysis"]["order_by_mean_test_auprc"]
    swapped = copy.deepcopy(res)
    a = swapped["analysis"]
    a["order_by_mean_test_auprc"] = new = order[:4] + ["svm", "proxy", "logreg"]
    with pytest.raises(fd.ClaimError, match="not the result's order"):
        fd.comparison(swapped)
    # With the pairs following the new order, the BLUF's own check refuses.
    for p, (x, y) in zip(a["adjacent_pairs"], zip(new, new[1:])):
        p["a"], p["b"] = x, y
    with pytest.raises(fd.ClaimError, match="BLUF"):
        fd.comparison(swapped)


@pytest.mark.parametrize("change, match", [
    (lambda r: r.update(evidence_tag="HW"), "evidence tag"),
    (lambda r: r.update(metered_seconds=4), "metered seconds"),
    (lambda r: r["analysis"]["svm_form"].update(kept="rbf"), "SVM form"),
    (lambda r: r["analysis"]["adjacent_pairs"][0].update(primary="bootstrap"),
     "Wilcoxon"),
    (lambda r: r["analysis"].update(n_seeds=5), "Wilcoxon"),
])
def test_a_fixed_statement_the_result_does_not_support_is_refused(change,
                                                                  match):
    res = _res()
    change(res)
    with pytest.raises(fd.ClaimError, match=match):
        fd.render(res)
    near = copy.deepcopy(res)
    near["analysis"]["adjacent_pairs"][3]["wilcoxon"]["p"] = 0.001
    with pytest.raises(fd.ClaimError, match="Bonferroni"):
        fd.comparison(near)


def test_the_unestablished_runs_split_at_a_reliable_pair():
    order = ["a", "b", "c", "d"]
    pairs = [{"a": "a", "b": "b", "reading": fd.NO_DIFF},
             {"a": "b", "b": "c", "reading": "above"},
             {"a": "c", "b": "d", "reading": fd.NO_DIFF}]
    assert fd.unestablished(order, pairs) == [["a", "b"], ["c", "d"]]


def test_the_confusion_counts_at_the_test_folds_budget_are_stated():
    # Sprint 30 D8, on the recorded result: the outcome block's counts at
    # the test fold's own budget, read here without the generator.
    res = _res()
    pages = fd.render(res)
    lanes = [r["lanes"]["proxy"] for r in res["rows"]]
    c = [ln["outcome"]["at_budget_on_test"]["confusion"] for ln in lanes]
    row = next(ln for ln in pages[fd.COMPARISON].splitlines()
               if "| CVQBoost proxy |" in ln)
    cells = [x.strip() for x in row.split("|")]
    want = []
    for k in ("tp", "fp", "tn", "fn"):
        v = [x[k] for x in c]
        want.append(f"{min(v):,} to {max(v):,}")
    assert cells[6:10] == want
    first = c[0]
    assert (f"| {first['tp']} / {first['fp']} / {first['tn']} / {first['fn']} |\n"
            in pages[fd.FILES["proxy"]])
    over = sum(ln["outcome"]["at_budget_on_test"]["n_flagged"]
               > ln["outcome"]["at_budget_on_test"]["n_budget"] for ln in lanes)
    # Both branches, so the test does not assume the recorded result has
    # over-budget seeds (PR 74 review, Sprint 30 IMP-5).
    if over:
        assert (f"the proxy on {over} of {len(lanes)} seeds"
                in pages[fd.COMPARISON])
    else:
        assert "the proxy on " not in pages[fd.COMPARISON]


def test_no_lane_over_its_budget_writes_no_tie_note():
    within = {"n_flagged": 450, "n_budget": 450}
    over = {"n_flagged": 455, "n_budget": 450}

    def rows(b):
        return [{"lanes": {"proxy": {"outcome": {"at_budget_on_test": b}}}}]
    assert fd.over_budget_line(rows(within), ["proxy"], "test fold") is None
    assert "on 1 of 1 seeds, up to 455 rows" in fd.over_budget_line(
        rows(over), ["proxy"], "test fold")


def test_the_page_check_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    page = fd.DOCS / "ULB_CVQBOOST_PROXY.md"
    assert_can_fail(
        [Mutation(page, "Here the same configuration (`full`) was chosen on "
                  "every seed.",
                  "and the chosen configuration changes between seeds.",
                  expect_occurrences=1)],
        lambda: run_pytest(
            f"{THIS}::test_the_committed_pages_are_what_the_generator_renders",
            ROOT),
        "a committed page that differs from the render")
    assert_can_fail(
        # One choice read as "every seed" when the seeds chose more than one:
        # the claim is then written with no refusal.
        [Mutation(SCRIPT, "    return json.loads(next(iter(counts))) if "
                  "len(counts) == 1 else None\n",
                  "    return json.loads(next(iter(counts)))\n",
                  expect_occurrences=1)],
        lambda: run_pytest(
            f"{THIS}::test_a_proxy_statement_the_result_does_not_support_"
            "is_refused", ROOT),
        "a proxy claim the result does not support")
    for old, new, label in (
            ("{counts_cell(at_budget(l)['confusion'])} |\")\n",
             "{cells[1]} |\")\n",
             "the validation threshold's counts shown as the test fold's"),
            ("f\"{tp} | {fp} | {tn} | {fn} | [{FILES[a]}]",
             "f\"{fp} | {tp} | {tn} | {fn} | [{FILES[a]}]",
             "the comparison's counts in the wrong columns")):
        assert_can_fail(
            [Mutation(SCRIPT, old, new, expect_occurrences=1)],
            lambda: run_pytest(
                f"{THIS}::test_the_confusion_counts_at_the_test_folds_budget_"
                "are_stated", ROOT),
            label)
    assert_can_fail(
        [Mutation(SCRIPT, "    if wrong:\n        raise ClaimError",
                  "    if False:\n        raise ClaimError",
                  expect_occurrences=1)],
        lambda: run_pytest(
            f"{THIS}::test_a_fixed_statement_the_result_does_not_support_"
            "is_refused", ROOT),
        "a fixed statement the result does not support")
    assert_can_fail(
        [Mutation(SCRIPT, "            and order[len(BOOSTING):] == "
                  "[\"proxy\", \"svm\", \"logreg\"]):\n",
                  "            or True):\n", expect_occurrences=1)],
        lambda: run_pytest(
            f"{THIS}::test_the_comparison_statements_follow_the_result",
            ROOT),
        "a BLUF order the result does not have")
