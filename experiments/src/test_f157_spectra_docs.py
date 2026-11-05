"""F157 SPECTRA part's page generator (`scripts/f157_spectra_docs.py`):
it renders one page per dataset and algorithm and one comparison page per
dataset, and refuses a result its fixed text does not describe. Each
refusal is proven red on a mutated copy of the recorded result. The
committed pages are checked against the recorded result: a committed
page that differs from the render fails.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import f157_spectra_docs as sd  # noqa: E402

RESULT = sd.RESULT


@pytest.fixture(scope="module")
def recorded() -> dict:
    if not RESULT.exists():
        pytest.skip("the F157 SPECTRA result is not recorded")
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_committed_pages_match_the_render(recorded):
    pages = sd.render(recorded)
    assert len(pages) == len(sd.DATASETS) * (len(sd.SUFFIX) + 1)
    assert sd.fd.differing(pages, sd.DOCS) == []


def test_a_changed_page_is_found(recorded, tmp_path):
    """Proof for the check above: one changed byte is reported."""
    pages = sd.render(recorded)
    for n, t in pages.items():
        (tmp_path / n).write_text(t, encoding="utf-8", newline="\n")
    assert sd.fd.differing(pages, tmp_path) == []
    name = sd.comparison_page("energy_steel")
    (tmp_path / name).write_text(pages[name] + "x", encoding="utf-8",
                                 newline="\n")
    assert sd.fd.differing(pages, tmp_path) == [name]


@pytest.mark.parametrize("change, phrase", [
    (lambda r: r.update(part="ULB"), "part"),
    (lambda r: r.update(evidence_tag="DEVICE"), "evidence tag"),
    (lambda r: r.update(metered_seconds=4.0), "metered seconds"),
    (lambda r: r.update(complete=False), "not complete"),
    (lambda r: r.update(datasets=r["datasets"][:3]), "datasets"),
    (lambda r: r["analysis"]["energy_steel"].update(n_seeds=7), "Wilcoxon"),
    (lambda r: r["analysis"]["telecom_churn"]["adjacent_pairs"][0]
     .update(primary="paired_t"), "Wilcoxon"),
    (lambda r: r["analysis"]["maintenance_ai4i"]["adjacent_pairs"].pop(),
     "adjacent pairs"),
])
def test_fixed_text_refuses_a_result_it_does_not_describe(recorded, change,
                                                          phrase):
    sd.check_fixed_text(recorded)  # the recorded result passes
    bad = copy.deepcopy(recorded)
    change(bad)
    with pytest.raises(sd.ClaimError, match=phrase):
        sd.render(bad)


def test_pairs_out_of_order_are_refused(recorded):
    sd.comparison(recorded, "energy_steel")
    bad = copy.deepcopy(recorded)
    pairs = bad["analysis"]["energy_steel"]["adjacent_pairs"]
    pairs[0], pairs[1] = pairs[1], pairs[0]
    with pytest.raises(sd.ClaimError, match="not the result's order"):
        sd.comparison(bad, "energy_steel")


def test_a_non_serial_proxy_build_is_refused(recorded):
    rows = sd.rows_of(recorded, "energy_steel")
    sd.proxy_paragraph(rows)
    bad = copy.deepcopy(rows)
    bad[0]["lanes"]["proxy"]["build"] = "parallel"
    with pytest.raises(sd.ClaimError, match="serially"):
        sd.proxy_paragraph(bad)


def test_the_svm_line_says_when_the_lane_is_not_the_kept_form():
    rbf = {"svm_form": {"kept": "rbf", "rbf_beats_linear_seeds": 6},
           "svm_lane_is_kept_form": False}
    lin = {"svm_form": {"kept": "linear", "rbf_beats_linear_seeds": 2},
           "svm_lane_is_kept_form": True}
    assert "not the form the rule keeps" in sd.svm_form_line(rbf, 10)
    assert "not the form the rule keeps" not in sd.svm_form_line(lin, 10)
    rbf["svm_lane_is_kept_form"] = True
    with pytest.raises(sd.ClaimError, match="disagrees"):
        sd.svm_form_line(rbf, 10)


def test_the_comparison_bluf_names_the_svm_form_gap(recorded):
    for ds in sd.DATASETS:
        text = sd.comparison(recorded, ds).split("\n\n")[1]
        kept = recorded["analysis"][ds]["svm_lane_is_kept_form"]
        assert ("did not keep" in text) is (not kept), ds


def test_a_no_ranking_rbf_win_is_refused(recorded):
    sd.algo_doc(recorded, "energy_steel", "svm")
    bad = copy.deepcopy(recorded)
    row = next(r for r in bad["rows"]
               if r["dataset"] == "energy_steel" and r["seed"] == 42)
    row["svm_rbf_alternative"]["beats_linear_on_validation"] = True
    with pytest.raises(sd.ClaimError, match="RBF win"):
        sd.algo_doc(bad, "energy_steel", "svm")


def test_degenerate_rbf_seeds_are_found():
    rows = [{"seed": 42, "svm_rbf_alternative": {"best_val_auprc": 0.25428},
             "lanes": {"svm": {"test": {"prevalence": 0.254281}}}},
            {"seed": 43, "svm_rbf_alternative": {"best_val_auprc": 0.61},
             "lanes": {"svm": {"test": {"prevalence": 0.254281}}}}]
    assert sd.degenerate_seeds(rows) == [42]
