"""F152: Experiment 2's first scores on IEEE-CIS rolling-origin folds.

Sprint 28 Task B (#49). Zero metered seconds. The entry is
`experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "Experiment 2",
committed before any score. This module imports F105's harness for the
folds, features and controls; `ieee_harness.py` stays score-free and is
not edited.

Modes:
  pilot   one lane (LightGBM), month 4, seeds 42 and 43: the entry's
          two-seed check. The paired interval between the two seeds must
          include zero, or the interval method is too narrow for seed noise.
  full    four lanes, three months, seeds 42-46, then the analysis.
  analyze the analysis again, from the recorded full run and its per-row
          score files (each file's SHA-256 is checked against its block).

Run:  <venv python> experiments/phase2/src/f152_exp2_score.py pilot|full|analyze
"""
from __future__ import annotations

import itertools
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "experiments" / "src"))
import outcome_record as orec  # noqa: E402  (Phase 2)
import strict_json  # noqa: E402  (Phase 2)

RESULTS = ROOT / "experiments" / "phase2" / "results"
OUT = RESULTS / "f152_exp2.json"
PILOT_OUT = RESULTS / "f152_exp2_pilot.json"
HEARTBEAT = ROOT / "experiments" / "phase2" / "predictions" / "f152.heartbeat"
SEEDS = (42, 43, 44, 45, 46)
CONTROLS_SEED = 42
LANES = ("xgboost", "lightgbm", "hgb", "logistic")
FULL_MONTHS = (4, 5)
N_BOOT = 1000
PRIMARY_LEVEL = 1 - 0.05 / 2          # m = 2, Bonferroni
SECONDARY_LEVEL = 0.95


# ------------------------------------------------------------ the bootstrap
def ap_parts(y, p) -> dict:
    """Sort once; a weighted AUPRC is then O(n) per replicate."""
    y = np.asarray(y).astype(int)
    p = np.asarray(p, dtype=float)
    order = np.argsort(-p, kind="mergesort")
    ps = p[order]
    # Last index of each group of tied scores: sklearn's AP steps only at
    # distinct thresholds.
    ends = np.r_[np.nonzero(np.diff(ps))[0], len(ps) - 1]
    return {"order": order, "y": y[order], "ends": ends}


def weighted_ap(parts: dict, counts: np.ndarray) -> float:
    """Average precision with integer row weights (a bootstrap replicate)."""
    w = counts[parts["order"]].astype(float)
    tp = np.cumsum(w * parts["y"])[parts["ends"]]
    fp = np.cumsum(w * (1 - parts["y"]))[parts["ends"]]
    pos = tp[-1]
    if pos == 0:
        return float("nan")
    prec = tp / np.maximum(tp + fp, 1e-300)
    rec = tp / pos
    return float(np.sum(np.diff(np.r_[0.0, rec]) * prec))


def floor_norm(ap: float, prevalence: float) -> float:
    return (ap - prevalence) / (1 - prevalence)


def stratified_counts(y, rng) -> np.ndarray:
    y = np.asarray(y).astype(int)
    pos, neg = np.nonzero(y == 1)[0], np.nonzero(y == 0)[0]
    idx = np.r_[rng.choice(pos, len(pos)), rng.choice(neg, len(neg))]
    return np.bincount(idx, minlength=len(y))


def boot_seed_mean_delta(y, scores_a: list, scores_b: list, *, n_boot=N_BOOT,
                         level=PRIMARY_LEVEL, seed=0) -> dict:
    """Across-seed mean of floor-normalized AUPRC(A) - AUPRC(B); the same
    resampled rows for both lanes and every seed; percentile interval."""
    y = np.asarray(y).astype(int)
    prev = float(y.mean())
    pa = [ap_parts(y, s) for s in scores_a]
    pb = [ap_parts(y, s) for s in scores_b]
    ones = np.ones(len(y), dtype=int)

    def stat(c):
        return float(np.mean([floor_norm(weighted_ap(a, c), prev)
                              - floor_norm(weighted_ap(b, c), prev)
                              for a, b in zip(pa, pb)]))
    rng = np.random.default_rng(seed)
    boot = np.array([stat(stratified_counts(y, rng)) for _ in range(n_boot)])
    lo, hi = np.quantile(boot, [(1 - level) / 2, 1 - (1 - level) / 2])
    return {"estimate": stat(ones), "low": float(lo), "high": float(hi),
            "level": level, "n_boot": n_boot,
            "excludes_zero": bool(lo > 0 or hi < 0)}


def boot_change(y1, scores1: list, y2, scores2: list, *, n_boot=N_BOOT,
                level=PRIMARY_LEVEL, seed=0) -> dict:
    """Month 2 minus month 1 of one lane's across-seed mean floor-normalized
    AUPRC; the months are independent samples, each resampled on its own."""
    def side(y, scores):
        y = np.asarray(y).astype(int)
        return y, float(y.mean()), [ap_parts(y, s) for s in scores]
    (ya, pva, a), (yb, pvb, b) = side(y1, scores1), side(y2, scores2)

    def mean_norm(parts, c, prev):
        return float(np.mean([floor_norm(weighted_ap(p, c), prev) for p in parts]))
    rng = np.random.default_rng(seed)
    boot = np.array([mean_norm(b, stratified_counts(yb, rng), pvb)
                     - mean_norm(a, stratified_counts(ya, rng), pva)
                     for _ in range(n_boot)])
    lo, hi = np.quantile(boot, [(1 - level) / 2, 1 - (1 - level) / 2])
    est = mean_norm(b, np.ones(len(yb), int), pvb) - mean_norm(a, np.ones(len(ya), int), pva)
    return {"estimate": est, "low": float(lo), "high": float(hi), "level": level,
            "n_boot": n_boot, "excludes_zero": bool(lo > 0 or hi < 0)}


# ------------------------------------------------------------ the lanes
def hgb_model(seed: int):
    """F151's stable HGB (its REFERENCE_VARIANT, l2_regularization=1.0);
    every other setting at its default."""
    from sklearn.ensemble import HistGradientBoostingClassifier
    return HistGradientBoostingClassifier(l2_regularization=1.0, random_state=seed)


def item4_features(ctrl: dict, em: int) -> list:
    """The features the item-4 controls kept. None kept is a stop, never a
    fall back to every column: that would fit on the uncontrolled set."""
    if not ctrl["features"]:
        raise RuntimeError(f"month {em}: the item-4 controls removed every "
                           "feature; the fold cannot be scored as controlled")
    return list(ctrl["features"])


def fit_predict(lane: str, Xtr, ytr, Xev, seed: int):
    t0 = time.time()
    if lane in ("xgboost", "lightgbm"):
        import run_ieee                                      # Phase 1, read-only
        cfg = dict(run_ieee.ARMS[lane], **run_ieee._weight_kwargs(lane, ytr),
                   random_state=seed)
        if lane == "xgboost":
            from xgboost import XGBClassifier
            m = XGBClassifier(**cfg)
        else:
            from lightgbm import LGBMClassifier
            m = LGBMClassifier(**cfg)
    elif lane == "hgb":
        m = hgb_model(seed)
    elif lane == "logistic":
        from sklearn.impute import SimpleImputer
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import StandardScaler
        m = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(),
                          LogisticRegression(class_weight="balanced", max_iter=2000,
                                             random_state=seed))
    else:
        raise ValueError(f"unknown lane {lane!r}")
    m.fit(Xtr, ytr)
    return m.predict_proba(Xev)[:, 1], round(time.time() - t0, 1)


def _beat(stage: str, **kw) -> None:
    HEARTBEAT.parent.mkdir(parents=True, exist_ok=True)
    with HEARTBEAT.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"t": time.strftime("%H:%M:%S"), "stage": stage, **kw}) + "\n")


def score(lanes=LANES, seeds=SEEDS, months=None) -> dict:
    """Fit and score; every lane, month and seed gets an outcome block."""
    import data
    import ieee_controls
    import ieee_features
    import ieee_harness as ih
    import ieee_loader
    from sklearn.metrics import average_precision_score, roc_auc_score
    HEARTBEAT.unlink(missing_ok=True)
    df, n_dupes = ieee_loader.dedupe_ieee(data.load_ieee_cis_train())
    _beat("loaded", rows=len(df))
    out = {"folds": [], "scores": {}}
    for fold in ih.folds_for(df):
        em = int(fold.eval_month)
        if months is not None and em not in months:
            continue
        b = ih.build_fold(df, fold)
        ytr = b["parts"]["y_train"].to_numpy()
        yev = b["parts"]["y_eval"].to_numpy().astype(int)
        day_tr = ieee_features.add_day(b["parts"]["X_train"]).to_numpy()
        ctrl = ieee_controls.apply_item4_controls(b["X_train"], ytr, day_tr,
                                                  seed=CONTROLS_SEED)
        keep = item4_features(ctrl, em)
        _beat("controls", eval_month=em, kept=len(keep))
        out["folds"].append({
            "eval_month": em, "n_train": int(len(ytr)), "n_eval": int(len(yev)),
            "prevalence": float(yev.mean()), "n_features": len(keep),
            "controls": {k: v for k, v in ctrl.items() if k != "features"}})
        for lane in lanes:
            for seed in seeds:
                p, fit_s = fit_predict(lane, b["X_train"][keep], ytr,
                                       b["X_eval"][keep], seed)
                ap = float(average_precision_score(yev, p))
                out["scores"].setdefault(str(em), {}).setdefault(lane, []).append({
                    "seed": seed, "auprc": ap,
                    "norm_auprc": floor_norm(ap, float(yev.mean())),
                    "auroc": float(roc_auc_score(yev, p)), "fit_s": fit_s,
                    "outcome": orec.record(f"f152_{lane}_m{em}", seed, yev, p)})
                _beat("fit", eval_month=em, lane=lane, seed=seed, fit_s=fit_s)
    out["rows_after_dedupe"] = len(df)
    out["exact_duplicates_removed"] = n_dupes
    return out


def _load_scores(rec: dict) -> tuple[np.ndarray, list]:
    """Labels and per-seed scores back from the saved outcome files. Each
    file must still hash to its block's SHA-256: the pilot and the full run
    write the same names, so a later run can replace a file silently."""
    ps, y = [], None
    for r in rec:
        ts = r["outcome"]["test_scores"]
        path = ROOT / ts["path"]
        got = orec.sha256_of(path)
        if got != ts["sha256"]:
            raise ValueError(f"{ts['path']}: SHA-256 {got} does not match the "
                             f"recorded {ts['sha256']}; the file was replaced")
        z = np.load(path)
        y = z["y_test"].astype(int) if y is None else y
        if not np.array_equal(y, z["y_test"]):
            raise ValueError("seeds disagree on the evaluation labels")
        ps.append(z["p_test"])
    return y, ps


def analyze(s: dict) -> dict:
    sc = s["scores"]
    p1 = {}
    for em in FULL_MONTHS:
        y, xg = _load_scores(sc[str(em)]["xgboost"])
        _, lg = _load_scores(sc[str(em)]["logistic"])
        p1[str(em)] = boot_seed_mean_delta(y, xg, lg, seed=em)
    p1_holds = all(v["low"] > 0 for v in p1.values())
    y4, x4 = _load_scores(sc["4"]["xgboost"])
    y5, x5 = _load_scores(sc["5"]["xgboost"])
    p2 = boot_change(y4, x4, y5, x5, seed=45)
    secondary = {}
    for em, lanes in sc.items():
        for a, b in itertools.combinations(sorted(lanes), 2):
            y, pa = _load_scores(lanes[a])
            _, pb = _load_scores(lanes[b])
            secondary[f"m{em}:{a}-{b}"] = boot_seed_mean_delta(
                y, pa, pb, level=SECONDARY_LEVEL, seed=int(em))
    per_lane = {em: {lane: {k: float(np.mean([r[k] for r in rows]))
                            for k in ("auprc", "norm_auprc", "auroc")}
                     | {"norm_auprc_sd": float(np.std([r["norm_auprc"] for r in rows],
                                                      ddof=1))}
                     for lane, rows in lanes.items()}
                for em, lanes in sc.items()}
    return {"P1_xgboost_minus_logistic": p1, "P1_holds": p1_holds,
            "P2_xgboost_change_m4_to_m5": p2, "secondary_pairs": secondary,
            "per_lane_means": per_lane}


def pilot_check() -> dict:
    """LightGBM, month 4, seeds 42 and 43: the between-seed interval."""
    s = score(lanes=("lightgbm",), seeds=(42, 43), months=(4,))
    y, ps = _load_scores(s["scores"]["4"]["lightgbm"])
    iv = boot_seed_mean_delta(y, [ps[0]], [ps[1]], level=SECONDARY_LEVEL, seed=1)
    return {**_header(), "mode": "pilot", **s, "between_seed_interval": iv,
            "check_passes": not iv["excludes_zero"]}


def _header() -> dict:
    return {"generator": "experiments/phase2/src/f152_exp2_score.py",
            "card": "F152", "sprint": 28, "evidence_tag": "SIM",
            "metered_seconds": 0,
            "entry": "experiments/phase2/PREREGISTRATION_DRAFT.md section 6, Experiment 2",
            "seeds": list(SEEDS), "controls_seed": CONTROLS_SEED,
            "drift_treatment": "stated limit: Phase 1's adversarial control at its cap"}


def _dump(res: dict) -> str:
    return json.dumps(res, indent=1, default=strict_json.numpy_scalar)


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        raise SystemExit("usage: f152_exp2_score.py pilot|full|analyze "
                         "(no default)")
    mode = argv[0]
    if mode in ("pilot", "full"):
        out = PILOT_OUT if mode == "pilot" else OUT
        if out.exists():
            raise SystemExit(f"{out.name} is recorded; {mode} would "
                             "overwrite it and its per-row score files")
    if mode == "pilot":
        res = pilot_check()
        PILOT_OUT.write_text(_dump(res), encoding="utf-8")
        print(json.dumps(res["between_seed_interval"]), res["check_passes"])
    elif mode == "full":
        s = score()
        res = {**_header(), "mode": "full", **s}
        OUT.write_text(_dump(res), encoding="utf-8")
        res["analysis"] = analyze(s)
        OUT.write_text(_dump(res), encoding="utf-8")
        a = res["analysis"]
        print("P1", json.dumps(a["P1_xgboost_minus_logistic"]), "holds", a["P1_holds"])
        print("P2", json.dumps(a["P2_xgboost_change_m4_to_m5"]))
    elif mode == "analyze":
        res = json.loads(OUT.read_text(encoding="utf-8"))
        res["analysis"] = analyze(res)
        OUT.write_text(_dump(res), encoding="utf-8")
    else:
        raise SystemExit(f"unknown mode {mode!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
