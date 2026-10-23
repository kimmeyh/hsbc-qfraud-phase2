"""F162: the in-pocket head-to-head (experiments/phase2/src/f162_in_pocket.py).

Synthetic data and stubs, except one leak check on the real telecom_churn
file, skipped where the SPECTRA files are absent (CI).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "src"))
import f162_in_pocket as fp  # noqa: E402


# ------------------------------------------------------------------ leaks
@pytest.mark.parametrize("label", ["target", "target_real", "in_pocket"])
def test_check_features_refuses_each_label(label):
    with pytest.raises(ValueError, match="label columns"):
        fp.check_features(["x1", label, "x2"])


def test_prepare_on_real_data_has_no_label_and_the_frozen_width():
    import data
    if not (data.SPECTRA_DIR / "spectra_telecom_churn.csv").exists():
        pytest.skip("SPECTRA files not present")
    d = fp.prepare("telecom_churn", 42)
    assert not set(d["features"]) & set(fp.LABELS)
    assert "age" not in d["features"]                 # the frozen cell's drop
    assert d["Xtr"].shape[1] == d["cell"]["config"]["n_features"] == 17
    assert len(d["pocket"]) == len(d["yte"]) and d["pocket"].any()


# ---------------------------------------------------------------- metrics
def test_pocket_metrics_scores_only_the_pocket():
    y = np.array([1, 0, 1, 0, 1, 1, 0, 0])
    p = np.array([0.9, 0.1, 0.8, 0.2, 0.1, 0.2, 0.9, 0.8])
    mask = np.array([1, 1, 1, 1, 0, 0, 0, 0], dtype=bool)   # perfect inside
    m = fp.pocket_metrics(y, p, mask)
    assert m["n"] == 4 and m["n_positives"] == 2 and m["prevalence"] == 0.5
    assert m["auprc"] == 1.0 and m["auprc_normalized"] == 1.0 and m["auc_roc"] == 1.0


def test_pocket_metrics_refuses_a_one_class_pocket():
    with pytest.raises(ValueError, match="one class"):
        fp.pocket_metrics(np.array([1, 1, 0]), np.array([0.5, 0.6, 0.1]),
                          np.array([1, 1, 0], dtype=bool))


# ------------------------------------------------------------------ seeds
def test_choose_seeds_cuts_to_eight_only_above_the_cap():
    assert fp.choose_seeds(12.0)["seeds"] == list(range(42, 52))
    assert fp.choose_seeds(12.1)["seeds"] == list(range(42, 50))
    assert fp.M == 6 and len(fp.SEEDS_CUT) == 8          # 2 / 2^8 <= 0.05 / 6


# ----------------------------------------------------------- the decision
def test_compare_reads_each_direction_and_the_seed_floor():
    up = [0.05, 0.04, 0.06, 0.05, 0.03, 0.07, 0.05, 0.04, 0.06, 0.05]
    assert fp.compare(up)["reading"] == "proxy above"
    assert fp.compare([-x for x in up])["reading"] == "proxy below"
    mixed = [0.05, -0.04, 0.06, -0.05, 0.03, -0.07, 0.05, -0.04, 0.06, -0.05]
    assert fp.compare(mixed)["reading"] == "no reliable difference"
    # Five seeds all one way: exact p = 0.0625, above 0.05 / 6, so no claim.
    five = fp.compare(up[:5])
    assert five["wilcoxon_p"] == pytest.approx(0.0625)
    assert five["reading"] == "no reliable difference"


def test_compare_needs_the_interval_on_the_same_side():
    # Wilcoxon rejects on signs; a mean pulled across zero by one large
    # negative keeps the interval spanning zero, so no claim.
    d = [0.01] * 9 + [-0.5]
    r = fp.compare(d)
    assert r["interval"][0] < 0 < r["interval"][1]
    assert r["reading"] == "no reliable difference"


def _row(cell, seed, lane, ap, auc=0.8, n_pos=60):
    return {"cell": cell, "seed": seed, "lane": lane, "test_auprc": ap,
            "test_auc_roc": auc, "train_test_gap_auprc": 0.1,
            "pocket": {"auprc": ap, "auc_roc": auc, "auprc_normalized": ap - 0.1,
                       "n_positives": n_pos}}


def _doc(proxy_edge=0.0, seeds=tuple(range(42, 52))):
    rows = []
    for c in fp.CELLS:
        for i, s in enumerate(seeds):
            base = 0.7 + 0.01 * i
            rows += [_row(c, s, "proxy", base + proxy_edge + 0.001 * (i % 3)),
                     _row(c, s, "hgb", base), _row(c, s, "xgboost", base - 0.01)]
    return {"rows": rows, "seed_choice": {"seeds": list(seeds)}}


def test_analyze_finds_a_proxy_edge_and_the_falsifier_follows():
    a = fp.analyze(_doc(proxy_edge=0.05))
    assert a["cells_with_proxy_above"] == list(fp.CELLS)
    assert not any(a["falsifier"].values())
    a0 = fp.analyze(_doc(proxy_edge=-0.05))
    assert a0["cells_with_proxy_above"] == [] and all(a0["falsifier"].values())
    assert a0["primary"]["energy_steel"]["proxy_minus_hgb"]["reading"] == "proxy below"


def test_analyze_refuses_a_missing_row():
    doc = _doc()
    doc["rows"].pop()
    with pytest.raises(ValueError, match="missing"):
        fp.analyze(doc)


# ------------------------------------------------------------- the lanes
def test_proxy_pool_is_seeded_and_uses_the_frozen_config(monkeypatch):
    import qubo_proxy as qp
    seen = {}

    class Clf:
        h_list = [0, 1, 2]

    def build_pool(X, y, schedule, wtype, build, weak_params=None, lambda_coef=None):
        seen.update(schedule=schedule, wtype=wtype, build=build,
                    weak_params=weak_params, lam=lambda_coef)
        return Clf()

    monkeypatch.setattr(qp, "build_pool", build_pool)
    monkeypatch.setattr(qp, "h_matrix", lambda clf, X: np.zeros((3, len(X))))
    monkeypatch.setattr(qp, "solve_simplex_qp", lambda H, y, lam: np.array([0.5, 0.5, 0.0]))
    cfg = {"weak_cls_schedule": 3, "lambda_coef_alpha": 2.0, "weak_cls_params": {}}
    d = {"cell": {"config": cfg}, "Xtr": np.zeros((10, 2)), "Xva": np.zeros((4, 2)),
         "Xte": np.zeros((5, 2)), "ytr": np.array([0, 1] * 5)}
    out = fp.fit_proxy(d, 47)
    assert seen["weak_params"] == {"random_state": 47}
    assert (seen["schedule"], seen["wtype"], seen["build"]) == (3, "dct", "sequential")
    assert seen["lam"] == 20.0 and out["n_nonzero_weights"] == 2
    assert out["p_te"].shape == (5,)


def test_classical_lanes_are_the_entrys_settings():
    assert fp.hgb_model(43).get_params()["l2_regularization"] == 1.0
    assert fp.hgb_model(43).get_params()["random_state"] == 43
    x = fp.xgb_model(44).get_params()
    assert x["random_state"] == 44 and x["n_estimators"] is None   # library default


def test_score_lane_carries_an_outcome_block(tmp_path):
    rng = np.random.default_rng(0)
    yte = np.array([0, 1] * 20)
    d = {"features": ["a", "b"], "ytr": np.array([0, 1] * 10), "yte": yte,
         "yva": np.array([0, 1] * 10), "pocket": np.arange(40) < 20}
    fit = {"p_tr": rng.random(20), "p_va": rng.random(20), "p_te": rng.random(40)}
    row = fp.score_lane("hgb", "energy_steel", 42, d, fit, 1.23, pred_dir=tmp_path)
    ts = row["outcome"]["test_scores"]
    assert Path(ROOT / ts["path"]).exists() or Path(ts["path"]).exists()
    assert row["outcome"]["operating_points_from_validation"]
    assert row["pocket"]["n"] == 20 and row["features"] == ["a", "b"]


# --------------------------------------------------------------- the run
def _stub_cell(calls):
    def run_cell(name, seed):
        calls.append((name, seed))
        return {"rows": [{"cell": name, "seed": seed, "lane": ln,
                          "pocket": {"auprc": 0.5}} for ln in fp.LANES],
                "pair": {"cell": name, "seed": seed, "bootstrap": {}}}
    return run_cell


def test_run_fits_each_cell_seed_once_and_resumes(tmp_path, monkeypatch):
    monkeypatch.setattr(fp, "OUT", tmp_path / "f162.json")
    monkeypatch.setattr(fp, "analyze", lambda doc: {"stub": True})
    calls = []
    monkeypatch.setattr(fp, "run_cell", _stub_cell(calls))
    fp.run()
    assert len(calls) == len(set(calls)) == 3 * 10      # fast seed 42: ten seeds
    doc = json.loads(fp.OUT.read_text(encoding="utf-8"))
    doc["pairs"] = [p for p in doc["pairs"] if p["seed"] != 51]
    doc["rows"] = [r for r in doc["rows"] if r["seed"] != 51]
    fp.OUT.write_text(json.dumps(doc), encoding="utf-8")
    calls.clear()
    fp.run()
    assert sorted(calls) == sorted((c, 51) for c in fp.CELLS)


def test_a_slow_first_seed_cuts_the_run_to_eight(tmp_path, monkeypatch):
    monkeypatch.setattr(fp, "OUT", tmp_path / "f162.json")
    monkeypatch.setattr(fp, "analyze", lambda doc: {"stub": True})
    calls = []
    monkeypatch.setattr(fp, "run_cell", _stub_cell(calls))
    doc = fp._load()
    doc["pairs"] = [{"cell": c, "seed": 42, "bootstrap": {}, "wall_s": 300.0}
                    for c in fp.CELLS]                   # 15 min x 10 > 120
    fp._save(doc)
    fp.run()
    doc = json.loads(fp.OUT.read_text(encoding="utf-8"))
    assert doc["seed_choice"]["seeds"] == list(range(42, 50))
    assert {s for _, s in calls} == set(range(43, 50))


def test_main_needs_a_mode():
    with pytest.raises(SystemExit, match="no default"):
        fp.main([])
    with pytest.raises(SystemExit, match="unknown mode"):
        fp.main(["pilot"])
