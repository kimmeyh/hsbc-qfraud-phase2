"""F157 SPECTRA part (Sprint 31 Task F, #98): the seed rule, the pocket
split of the secondary metric, and F166's grids imported unchanged, each
term proven red.

No model is fit here.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
PHASE2 = ROOT / "experiments" / "phase2" / "src"
SRC = PHASE2 / "f157_spectra_algorithms.py"
THIS = Path(__file__).relative_to(ROOT).as_posix()
sys.path.insert(0, str(PHASE2))

import f157_spectra_algorithms as f157  # noqa: E402
import f166_ulb_algorithms as f166  # noqa: E402


def test_the_seed_count_follows_seed_42s_time_at_60_minutes():
    assert f157.choose_seeds(5.0)["n_seeds"] == 10        # floor 12, cap 10
    assert f157.choose_seeds(10.0)["n_seeds"] == 6        # floor(60 / 10)
    p = f157.choose_seeds(40.0)                            # floor 1.5
    assert (p["n_seeds"], p["over_cap"]) == (3, True)
    assert f157.choose_seeds(10.0)["below_section2_five_seeds"] is False
    assert f157.choose_seeds(15.0)["below_section2_five_seeds"] is True


def test_the_pocket_metric_splits_the_test_rows():
    y = np.array([1, 0, 0, 1, 0, 0, 0, 1])
    p = np.array([0.9, 0.1, 0.2, 0.3, 0.8, 0.1, 0.2, 0.7])
    m = np.array([True, True, True, True, False, False, False, False])
    out = f157.pocket_auprc(y, p, m)
    assert out["in_pocket"] == 1.0
    # Outside: the one positive ranks second, under a negative.
    assert abs(out["out_of_pocket"] - 0.5) < 1e-12
    # A side with no positive has no AUPRC, rather than a fabricated one.
    y2 = np.array([1, 1, 0, 0, 0, 0, 0, 0])
    assert f157.pocket_auprc(y2, p, ~m)["in_pocket"] is None


def test_the_grids_and_datasets_are_the_entrys():
    assert f157.GRIDS is f166.GRIDS and f157.ALGOS == f166.ALGOS
    assert set(f157.DATASETS) == {"energy_steel", "oilgas_gasturbine",
                                  "telecom_churn", "maintenance_ai4i"}


def _rows(rbf_wins: int, n: int = 4, form: str | None = None) -> list[dict]:
    rows = []
    for i in range(n):
        svm = {} if form is None else {"form": form}
        rows.append({"dataset": "telecom_churn", "seed": 42 + i,
                     "lanes": {"svm": svm},
                     "svm_rbf_alternative": {
                         "beats_linear_on_validation": i < rbf_wins}})
    return rows


def test_a_kept_form_the_lane_did_not_score_is_refused(monkeypatch):
    """D14: the rule keeps RBF on most seeds and the lane scored the linear
    form, so the analysis stops before any figure (F166's `rbf_kept`)."""
    import pytest
    reached = []

    def analyze(rows, scores):
        if scores:              # the second call: the figures
            reached.append(True)
        wins = sum(r["svm_rbf_alternative"]["beats_linear_on_validation"]
                   for r in rows)
        return {"svm_form": {"kept": "rbf" if wins > len(rows) / 2
                             else "linear"}}
    monkeypatch.setattr(f166, "analyze", analyze)
    monkeypatch.setattr(f166, "load_scores", lambda rows: {"any": 1})
    with pytest.raises(f157.FormNotScored, match="keeps the rbf SVM"):
        f157.analyze_dataset(_rows(3))
    with pytest.raises(f157.FormNotScored, match="keeps the linear SVM"):
        f157.analyze_dataset(_rows(1, form="rbf"))
    with pytest.raises(f157.FormNotScored, match="mixes forms"):
        rows = _rows(3, form="rbf")
        rows[0]["lanes"]["svm"] = {}
        f157.analyze_dataset(rows)
    assert reached == []


def test_the_rbf_refit_must_match_the_recorded_validation(monkeypatch):
    import pytest
    y = np.array([0, 1] * 10)
    X = __import__("pandas").DataFrame({"a": np.arange(20.0)})
    d = {"val": {"Xtr": X, "ytr": y, "Xev": X, "yev": y},
         "test": {"Xtr": X, "ytr": y, "Xev": X, "yev": y},
         "pocket": np.zeros(20, bool)}
    monkeypatch.setattr(f166, "stratified_rows", lambda y, n, s: np.arange(20))
    monkeypatch.setattr(f157.f174, "fit_classical", lambda *a: ("m", 0.1))
    monkeypatch.setattr(f166, "scores", lambda m, X: X[:, 0])
    rec = {"rows": 20, "tried": [{"val_auprc": 0.123}, {"val_auprc": 0.5}]}
    with pytest.raises(RuntimeError, match="nothing scored"):
        f157.rbf_lane("telecom_churn", 42, d, rec)
    rec["rows"] = 19
    with pytest.raises(RuntimeError, match="subsample"):
        f157.rbf_lane("telecom_churn", 42, d, rec)


def test_the_rbf_mode_writes_only_its_own_file(monkeypatch, tmp_path):
    """The recorded result is read and never written; the new file holds
    the kept form in the SVM lane and the linear rows as `svm_linear`."""
    import json
    import provenance
    src = tmp_path / "recorded.json"
    rows = _rows(3)
    for r in rows:
        r["lanes"]["svm"] = {"tried": [], "form_marker": "linear"}
    src.write_text(json.dumps({"rows": rows, "seed_plans": {}}),
                   encoding="utf-8")
    before = src.read_bytes()
    monkeypatch.setattr(f157, "OUT", src)
    monkeypatch.setattr(f157, "OUT_RBF", tmp_path / "rbf.json")
    monkeypatch.setattr(f157, "DATASETS", ("telecom_churn",))
    monkeypatch.setattr(f157, "data", lambda name, seed: {})
    monkeypatch.setattr(f157, "rbf_lane", lambda name, seed, d, rec: {
        "form": "rbf", "test": {"auprc": 0.5}})
    monkeypatch.setattr(f157, "analyze_dataset", lambda rows: {"ok": 1})
    monkeypatch.setattr(f166, "analyze", lambda rows, s: {
        "svm_form": {"kept": "rbf"}})
    written = []
    monkeypatch.setattr(provenance, "start", lambda p: ("rid", False))
    monkeypatch.setattr(provenance, "write_result",
                        lambda p, doc, *a, **k: written.append((p, doc)))
    f157.run_rbf()
    assert src.read_bytes() == before
    assert {p for p, _ in written} == {tmp_path / "rbf.json"}
    final = written[-1][1]
    assert final["complete"] is True and final["source_result"] == "recorded.json"
    assert all(r["lanes"]["svm"]["form"] == "rbf" and
               r["lanes"]["svm_linear"]["form_marker"] == "linear"
               for r in final["rows"])


def test_the_rules_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest

    def test(name):
        return lambda: run_pytest(f"{THIS}::{name}", ROOT)
    assert_can_fail([Mutation(SRC, "    if kept != scored:\n",
                              "    if False:\n", expect_occurrences=1)],
                    test("test_a_kept_form_the_lane_did_not_score_is_refused"),
                    "a kept form the lane did not score, analyzed")
    assert_can_fail([Mutation(SRC, "    if not np.allclose(got, want, rtol=0, "
                              "atol=1e-12):\n", "    if False:\n",
                              expect_occurrences=1)],
                    test("test_the_rbf_refit_must_match_the_recorded_"
                         "validation"),
                    "an RBF refit that differs from the recorded fit")
    assert_can_fail([Mutation(SRC, "            r[\"lanes\"][\"svm_linear\"] = "
                              "r[\"lanes\"][\"svm\"]\n", "            pass\n",
                              expect_occurrences=1)],
                    test("test_the_rbf_mode_writes_only_its_own_file"),
                    "the linear rows dropped")
    assert_can_fail([Mutation(SRC, "CAP_MIN = 60.0\n", "CAP_MIN = 120.0\n",
                              expect_occurrences=1)],
                    test("test_the_seed_count_follows_seed_42s_time_at_60_"
                         "minutes"),
                    "F166's 120 minutes kept")
    assert_can_fail([Mutation(SRC, "MAX_SEEDS, MIN_SEEDS = 10, 3\n",
                              "MAX_SEEDS, MIN_SEEDS = 10, 1\n",
                              expect_occurrences=1)],
                    test("test_the_seed_count_follows_seed_42s_time_at_60_"
                         "minutes"),
                    "a seed floor under 3")
    assert_can_fail([Mutation(SRC,
                              "                     if m.any() and 0 < "
                              "y[m].sum() < m.sum() else None)\n",
                              "                     if m.any() else None)\n",
                              expect_occurrences=1)],
                    test("test_the_pocket_metric_splits_the_test_rows"),
                    "an AUPRC on a side with no positive")


# Sprint 31 D16 option 1: each changed refusal has a test and a proof.

def test_an_unknown_mode_is_refused():
    import pytest
    with pytest.raises(SystemExit, match="mode required: run | rbf | analyze"):
        f157.main(["nope"])


def test_the_mode_refusal_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    assert_can_fail([Mutation(
        SRC, '        raise SystemExit("mode required: run | rbf | analyze")\n',
        "        pass\n", expect_occurrences=1)],
        lambda: run_pytest(f"{THIS}::test_an_unknown_mode_is_refused", ROOT),
        "an unknown mode not refused")
