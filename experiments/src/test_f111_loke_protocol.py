"""F111: Experiment 4's harness matches its entry.

Sprint 28 Task D (#51). Synthetic inputs; the ULB runs are not run here.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "src"))

import f111_loke_protocol as fl  # noqa: E402


def test_the_entry_constants():
    assert fl.SEEDS == tuple(range(42, 52)) and fl.SENS_SEEDS == (42, 43, 44)
    assert (fl.RATIO, fl.SENS_RATIO) == (0.02, 0.05)
    assert fl.KNN_PARAMS == {"n_neighbors": 15}
    assert (fl.SCHEDULE, fl.LAMBDA, fl.HGB_L2) == (2, 0.0, 1.0)
    assert fl.VAL_EVAL_TEST_SIZE == 0.67 and fl.CAP_MIN == 120.0
    assert (fl.TARGET, fl.TOLERANCE) == (0.8108, 0.03)


def _imbalanced(n=3000, pos=30, seed=0):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, 4))
    y = np.zeros(n, dtype=int)
    y[:pos] = 1
    X[:pos] += 2.0
    return X, y


def test_smote_tomek_reaches_the_ratio_with_the_codes_neighbors():
    X, y = _imbalanced()
    Xr, yr, info = fl.smote_tomek(X, y, 0.02, 42)
    assert info["applied"] and info["k_neighbors"] == 10
    # SMOTE reaches 0.02 of the majority; the Tomek step then removes
    # linked rows of both classes, so the count lands at or a little under.
    assert info["pos_before"] * 1.5 < info["pos_after"] <= 0.02 * info["neg_before"] + 1
    assert len(yr) == len(Xr) and yr.sum() == info["pos_after"]


def test_smote_tomek_is_skipped_when_already_balanced():
    X, y = _imbalanced(n=1000, pos=100)
    Xr, yr, info = fl.smote_tomek(X, y, 0.02, 42)
    assert not info["applied"] and Xr is X


def test_duplicates_counts_exact_copies_including_the_label():
    X = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    y = np.array([0, 1, 0])
    Xq = np.array([[1.0, 2.0], [3.0, 4.0], [3.0, 4.0], [9.0, 9.0]])
    yq = np.array([0, 1, 0, 0])            # the third differs by label only
    assert fl.duplicates_in_train(X, y, Xq, yq) == 2
    # Same features, every label flipped: no exact copies.
    assert fl.duplicates_in_train(X[:2], y[:2], X[:2], 1 - y[:2]) == 0


def test_score_is_monotone_in_w_dot_h():
    rng = np.random.default_rng(0)
    H = np.where(rng.random((5, 200)) < 0.5, 1.0, -1.0)
    w = rng.dirichlet(np.ones(5))
    raw = w @ H
    assert np.array_equal(np.argsort(fl.score(w, H), kind="stable"),
                          np.argsort(raw, kind="stable"))
    assert fl.score(w, H).min() >= 0 and fl.score(w, H).max() <= 1


def test_paired_interval_matches_a_hand_computed_t():
    from scipy import stats
    a = [0.80, 0.82, 0.79, 0.81]
    b = [0.78, 0.80, 0.78, 0.80]
    r = fl.paired(a, b)
    d = np.subtract(a, b)
    half = stats.t.ppf(0.975, 3) * d.std(ddof=1) / 2
    assert r["mean"] == pytest.approx(0.015)
    assert (r["low"], r["high"]) == pytest.approx((0.015 - half, 0.015 + half))
    assert r["excludes_zero"]


def _rows(knn_a, knn_b, hgb_a=0.8, hgb_b=0.8):
    rows = []
    for i, s in enumerate(fl.SEEDS):
        for p, ratio, lane, v in (("A", 0.02, "knn", knn_a[i]), ("B", None, "knn", knn_b[i]),
                                  ("A", 0.02, "hgb", hgb_a), ("B", None, "hgb", hgb_b)):
            rows.append({"protocol": p, "ratio": ratio, "lane": lane, "seed": s,
                         "test_auprc": v + (0.001 * i if lane == "hgb" else 0),
                         "eval_duplicates_in_train": 3 if p == "A" else 0})
    return {"rows": rows}


def test_analysis_pairs_by_seed_and_reads_consistency():
    knn_b = [0.77 + 0.002 * i for i in range(10)]
    knn_a = [v + 0.03 + (0.001 if i % 2 else -0.001) for i, v in enumerate(knn_b)]
    out = fl.analyze(_rows(knn_a, knn_b))
    assert out["knn_A_minus_B"]["mean"] == pytest.approx(0.03)
    assert out["knn_A_minus_B"]["excludes_zero"]
    assert out["consistent_with_0_8108"] is True       # mean 0.809
    assert out["eval_duplicates_in_train_A"][0] == (42, 3)


def test_a_far_mean_is_not_consistent():
    out = fl.analyze(_rows([0.70] * 10, [0.70] * 10))
    assert out["consistent_with_0_8108"] is False


def test_projection_adds_preparation_and_counts_the_sensitivity_seeds():
    p = {k: {"seconds": 6.0, "prep_seconds_full": 30.0, "full_train": 100,
             "pilot_train": 10, "full_query": 200, "pilot_query": 20}
         for k in ("A", "B")}
    # lane 6 s x 10 x 10 = 600 s per seed, plus 30 s preparation
    assert fl.projection_min(p) == pytest.approx((630 * 13 + 630 * 10) / 60)


def _no_real_work(monkeypatch):
    # A run() that wrongly proceeds must fail fast, not start the real
    # 825-minute experiment (a mutation did exactly that once).
    def refuse(*a, **k):
        raise AssertionError("run() reached real work")
    monkeypatch.setattr(fl, "protocol_a", refuse)
    monkeypatch.setattr(fl, "protocol_b", refuse)


def test_run_refuses_without_a_passing_pilot(tmp_path, monkeypatch):
    _no_real_work(monkeypatch)
    monkeypatch.setattr(fl, "OUT", tmp_path / "f111.json")
    with pytest.raises(SystemExit, match="Manual Validation"):
        fl.run()


def test_an_over_cap_run_needs_a_recorded_approval(tmp_path, monkeypatch):
    import json
    _no_real_work(monkeypatch)
    out = tmp_path / "f111.json"
    monkeypatch.setattr(fl, "OUT", out)
    with pytest.raises(SystemExit, match="no pilot"):
        fl.approve("DV2")
    out.write_text(json.dumps({"rows": [], "pilot": {"projected_minutes": 824.6,
                                                     "run": False}}))
    with pytest.raises(SystemExit, match="Manual Validation"):
        fl.run()
    with pytest.raises(SystemExit, match="names the decision"):
        fl.approve("  ")
    a = fl.approve("Sprint 28 DV2")
    assert a["reference"] == "Sprint 28 DV2" and a["projected_minutes"] == 824.6
    with pytest.raises(SystemExit, match="already recorded"):
        fl.approve("again")
    monkeypatch.setattr(fl, "SEEDS", ())
    monkeypatch.setattr(fl, "SENS_SEEDS", ())
    fl.run()                                   # approved: no refusal


def test_main_needs_an_explicit_mode(tmp_path, monkeypatch):
    _no_real_work(monkeypatch)
    monkeypatch.setattr(fl, "OUT", tmp_path / "f111.json")
    with pytest.raises(SystemExit, match="no default"):
        fl.main([])
    assert not (tmp_path / "f111.json").exists()


def test_a_recorded_pilot_is_never_rerun(tmp_path, monkeypatch):
    import json
    _no_real_work(monkeypatch)                 # a broken guard dies here
    out = tmp_path / "f111.json"
    monkeypatch.setattr(fl, "OUT", out)
    doc = {"rows": [], "pilot": {"projected_minutes": 824.6, "run": False,
                                 "over_cap_approval": {"reference": "DV2"}}}
    out.write_text(json.dumps(doc))
    with pytest.raises(SystemExit, match="already recorded"):
        fl.main(["pilot"])
    assert json.loads(out.read_text()) == doc   # approval kept, file untouched


def test_run_resumes_only_the_missing_keys(tmp_path, monkeypatch):
    import json
    out = tmp_path / "f111.json"
    monkeypatch.setattr(fl, "OUT", out)
    monkeypatch.setattr(fl, "SEEDS", (42, 43))
    monkeypatch.setattr(fl, "SENS_SEEDS", (42,))
    calls = {"a": 0, "b": 0, "knn": 0, "hgb": 0}

    def prot_a(seed, ratio=fl.RATIO, frac=None):
        calls["a"] += 1
        return {"protocol": "A", "ratio": ratio}

    def prot_b(seed, frac=None):
        calls["b"] += 1
        return {"protocol": "B", "ratio": None}

    def knn(d):
        calls["knn"] += 1
        return {}

    def hgb(d, seed):
        calls["hgb"] += 1
        return {}

    def row(d, lane, seed, o):
        return {"protocol": d["protocol"], "ratio": d["ratio"], "lane": lane,
                "seed": seed, "test_auprc": 0.8, "eval_duplicates_in_train": 0}
    for name, f in (("protocol_a", prot_a), ("protocol_b", prot_b),
                    ("knn_lane", knn), ("hgb_lane", hgb), ("_row", row)):
        monkeypatch.setattr(fl, name, f)
    present = [row({"protocol": "A", "ratio": 0.02}, lane, 42, None)
               for lane in ("knn", "hgb")]              # (42, A) complete
    present.append(row({"protocol": "B", "ratio": None}, "knn", 42, None))
    out.write_text(json.dumps({"rows": present, "pilot": {"run": True}}))
    fl.run()
    # Missing: B hgb 42; A and B for 43 (4 rows); A 0.05 for 42 (2 rows).
    assert calls == {"a": 2, "b": 2, "knn": 3, "hgb": 4}
    doc = json.loads(out.read_text())
    keys = [fl._key(r) for r in doc["rows"]]
    assert len(keys) == len(set(keys)) and set(keys) == fl.planned_keys()
    assert doc["run_sessions"][-1]["rows_added"] == 7
    a = fl.analyze(doc)
    assert a["complete"] and a["n_missing_rows"] == 0


def test_analysis_records_completeness_and_the_sensitivity_count():
    knn_b = [0.77 + 0.002 * i for i in range(10)]
    doc = _rows([v + 0.03 for v in knn_b], knn_b)
    out = fl.analyze(doc)
    assert not out["complete"] and out["n_missing_rows"] == 6
    assert out["sensitivity_r005"]["knn"] == {"mean": None, "n": 0, "seeds": []}
    doc["rows"].append({"protocol": "A", "ratio": 0.05, "lane": "knn", "seed": 43,
                        "test_auprc": 0.7, "eval_duplicates_in_train": 0})
    s = fl.analyze(doc)["sensitivity_r005"]["knn"]
    assert s == {"mean": pytest.approx(0.7), "n": 1, "seeds": [43]}
