"""F152: the Experiment 2 scorer's bootstrap and constants match the entry.

Sprint 28 Task B (#49). Synthetic inputs; the run reads IEEE-CIS and is not
run here.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest
from sklearn.metrics import average_precision_score

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "src"))

import f152_exp2_score as fs  # noqa: E402


def test_the_entry_constants():
    assert fs.SEEDS == (42, 43, 44, 45, 46)
    assert fs.LANES == ("xgboost", "lightgbm", "hgb", "logistic")
    assert fs.FULL_MONTHS == (4, 5)
    assert fs.PRIMARY_LEVEL == pytest.approx(0.975)
    assert fs.CONTROLS_SEED == 42


def test_weighted_ap_matches_sklearn_with_ties_and_weights():
    rng = np.random.default_rng(0)
    y = (rng.random(4000) < 0.05).astype(int)
    p = np.round(rng.random(4000) + 0.4 * y, 2)        # many ties
    parts = fs.ap_parts(y, p)
    assert fs.weighted_ap(parts, np.ones(4000, int)) == pytest.approx(
        average_precision_score(y, p))
    c = fs.stratified_counts(y, rng)
    assert fs.weighted_ap(parts, c) == pytest.approx(
        average_precision_score(y, p, sample_weight=c))


def test_stratified_counts_keep_the_class_totals():
    y = np.array([0] * 90 + [1] * 10)
    c = fs.stratified_counts(y, np.random.default_rng(1))
    assert c.sum() == 100 and c[y == 1].sum() == 10


def test_floor_normalization():
    assert fs.floor_norm(0.035, 0.035) == pytest.approx(0.0)
    assert fs.floor_norm(1.0, 0.035) == pytest.approx(1.0)


def test_a_real_difference_is_found_and_no_difference_is_not():
    rng = np.random.default_rng(2)
    y = (rng.random(3000) < 0.05).astype(int)
    good = [rng.random(3000) + 0.6 * y for _ in range(2)]
    poor = [rng.random(3000) + 0.1 * y for _ in range(2)]
    iv = fs.boot_seed_mean_delta(y, good, poor, n_boot=200)
    assert iv["low"] > 0 and iv["excludes_zero"]
    # Same signal, fitted independently: the pilot check's property. Pairing
    # a score with itself gives exactly 0 whatever the code does.
    good2 = [rng.random(3000) + 0.6 * y for _ in range(2)]
    same = fs.boot_seed_mean_delta(y, good, good2, n_boot=200)
    assert same["estimate"] != 0.0
    assert same["low"] < 0 < same["high"] and not same["excludes_zero"]


def _two_months():
    rng = np.random.default_rng(4)
    y1 = (rng.random(3000) < 0.05).astype(int)
    y2 = (rng.random(3000) < 0.05).astype(int)
    weak = [rng.random(3000) + 0.3 * y1 for _ in range(2)]
    strong = [rng.random(3000) + 1.5 * y2 for _ in range(2)]
    return y1, weak, y2, strong


def test_boot_change_is_month_two_minus_month_one():
    y1, weak, y2, strong = _two_months()
    up = fs.boot_change(y1, weak, y2, strong, n_boot=200)
    assert up["estimate"] > 0 and up["low"] > 0 and up["excludes_zero"]
    want = (np.mean([fs.floor_norm(average_precision_score(y2, s), y2.mean())
                     for s in strong])
            - np.mean([fs.floor_norm(average_precision_score(y1, s), y1.mean())
                       for s in weak]))
    assert up["estimate"] == pytest.approx(want)


def test_boot_change_reverses_sign_when_the_months_swap():
    y1, weak, y2, strong = _two_months()
    up = fs.boot_change(y1, weak, y2, strong, n_boot=200)
    down = fs.boot_change(y2, strong, y1, weak, n_boot=200)
    assert down["estimate"] == pytest.approx(-up["estimate"])
    assert down["high"] < 0 and down["excludes_zero"]


def test_hgb_lane_is_f151s_reference_variant():
    import f151_hgb_cause as fh
    from sklearn.ensemble import HistGradientBoostingClassifier
    ref = HistGradientBoostingClassifier(
        random_state=7, **fh.VARIANTS[fh.REFERENCE_VARIANT])
    assert fs.hgb_model(7).get_params() == ref.get_params()


def test_controls_that_keep_nothing_stop_the_fold():
    assert fs.item4_features({"features": ["a", "b"]}, 4) == ["a", "b"]
    with pytest.raises(RuntimeError, match="removed every feature"):
        fs.item4_features({"features": []}, 4)


def test_load_scores_refuses_a_replaced_file(tmp_path):
    import outcome_record as orec
    y = np.array([0, 1, 0, 1, 0])
    p = np.array([0.1, 0.9, 0.2, 0.8, 0.3])
    ts = orec.save_test_scores("f152_test", 42, y, p, pred_dir=tmp_path)
    rec = [{"outcome": {"test_scores": ts}}]
    y_back, ps = fs._load_scores(rec)            # intact: loads
    assert np.array_equal(y_back, y) and np.allclose(ps[0], p)
    # The writer never replaces a file (D13), so replace it directly.
    np.savez_compressed(tmp_path / "f152_test_42.npz", y_test=y, p_test=p[::-1])
    with pytest.raises(ValueError, match="does not match the recorded"):
        fs._load_scores(rec)


def test_writer_refuses_a_type_it_cannot_encode():
    import json
    back = json.loads(fs._dump({"n": np.int64(3), "ok": np.bool_(False)}))
    assert back == {"n": 3, "ok": False} and back["ok"] is False
    with pytest.raises(TypeError):
        fs._dump({"bad": {1, 2}})


def test_main_needs_a_mode_and_refuses_to_overwrite(tmp_path, monkeypatch):
    def no_work(*a, **k):
        raise AssertionError("main did work it should have refused")
    monkeypatch.setattr(fs, "pilot_check", no_work)
    monkeypatch.setattr(fs, "score", no_work)
    with pytest.raises(SystemExit, match="no default"):
        fs.main([])
    for mode, name in (("pilot", "PILOT_OUT"), ("full", "OUT")):
        recorded = tmp_path / f"{mode}.json"
        recorded.write_text("{}", encoding="utf-8")
        monkeypatch.setattr(fs, name, recorded)
        with pytest.raises(SystemExit, match="is recorded"):
            fs.main([mode])
        assert recorded.read_text(encoding="utf-8") == "{}"


def test_the_harness_stays_score_free():
    # The scorer imports the harness; it never edits it (F105's no-score test).
    import ieee_harness  # noqa: F401
    src = (ROOT / "experiments" / "phase2" / "src" / "ieee_harness.py").read_text(
        encoding="utf-8")
    assert "average_precision_score" not in src
