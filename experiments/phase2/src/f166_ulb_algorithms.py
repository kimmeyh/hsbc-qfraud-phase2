"""F166 (Sprint 29 Task F, #69): best achievable result per algorithm on
ULB, classical and proxy lanes (F157 part 1).

The entry is "F166" in `experiments/phase2/PREREGISTRATION_DRAFT.md`
section 6, committed before this module existed (15775da). Seven
algorithms, each tuned per seed on the validation fold over the
configurations the entry names, each scored once on the test fold.

Seed 42 runs first, timed; the seed count is
`min(10, floor(120 / t42))`, at least 3 (Decision 3, option 1).

    <venv python> experiments/phase2/src/f166_ulb_algorithms.py run
    <venv python> experiments/phase2/src/f166_ulb_algorithms.py analyze

Zero metered seconds. Writes `experiments/phase2/results/f166_ulb_algorithms.json`
through `provenance.write_result` after every seed; resumable by seed
(`provenance.run_id_for`), with `complete` true at the end.
"""
from __future__ import annotations

import itertools
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "experiments" / "src"))

OUT = ROOT / "experiments" / "phase2" / "results" / "f166_ulb_algorithms.json"
F159 = ROOT / "experiments" / "phase2" / "results" / "f159_parallel_pool.json"
ALGOS = ("hgb", "lightgbm", "xgboost", "catboost", "logreg", "svm", "proxy")
FIRST_SEED = 42
CAP_MIN = 120.0
MAX_SEEDS, MIN_SEEDS = 10, 3
ALPHA = 0.05
N_PAIRS = len(ALGOS) - 1           # adjacent pairs in the mean order
WILCOXON_MIN_SEEDS = 8             # 2 / 2^8 = 0.0078 < 0.05 / 6
N_BOOT = 2000
RBF_ROWS = 20_000
PROXY_CONFIGS = ("free", "mid", "full")


def _product(**axes) -> list[dict]:
    keys = list(axes)
    return [dict(zip(keys, v)) for v in itertools.product(*axes.values())]


GRIDS = {
    "hgb": _product(l2_regularization=[0.0, 1.0], learning_rate=[0.05, 0.1],
                    max_leaf_nodes=[15, 31]),
    "lightgbm": _product(num_leaves=[15, 63], learning_rate=[0.05, 0.1],
                         reg_lambda=[0.0, 1.0]),
    "xgboost": _product(max_depth=[3, 6], learning_rate=[0.1, 0.3],
                        n_estimators=[100, 300]),
    "catboost": _product(depth=[4, 6], learning_rate=[0.05, 0.1],
                         l2_leaf_reg=[3, 10]),
    "logreg": _product(C=[0.01, 0.1, 1.0, 10.0],
                       class_weight=[None, "balanced"]),
    "svm": _product(C=[0.001, 0.01, 0.1, 1.0],
                    class_weight=[None, "balanced"]),
    "proxy": [{"config": c} for c in PROXY_CONFIGS],
}
RBF_GRID = _product(C=[1.0, 10.0])


# ---------------------------------------------------------------- models
def make(algo: str, params: dict, seed: int):
    """The estimator for one classical configuration."""
    p = dict(params)
    if algo == "hgb":
        from sklearn.ensemble import HistGradientBoostingClassifier
        return HistGradientBoostingClassifier(random_state=seed, **p)
    if algo == "lightgbm":
        from lightgbm import LGBMClassifier
        return LGBMClassifier(n_estimators=300, random_state=seed,
                              verbose=-1, **p)
    if algo == "xgboost":
        from xgboost import XGBClassifier
        return XGBClassifier(random_state=seed, n_jobs=-1, **p)
    if algo == "catboost":
        from catboost import CatBoostClassifier
        return CatBoostClassifier(iterations=500, random_seed=seed,
                                  verbose=False, **p)
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    if algo == "logreg":
        from sklearn.linear_model import LogisticRegression
        return make_pipeline(StandardScaler(),
                             LogisticRegression(max_iter=2000, **p))
    if algo == "svm":
        from sklearn.svm import LinearSVC
        return make_pipeline(StandardScaler(),
                             LinearSVC(random_state=seed, **p))
    if algo == "rbf":
        from sklearn.svm import SVC
        return make_pipeline(StandardScaler(),
                             SVC(kernel="rbf", gamma="scale",
                                 random_state=seed, **p))
    raise ValueError(f"unknown algorithm {algo!r}")


def scores(model, X) -> np.ndarray:
    """Probabilities; a linear SVM's margins through the logistic map, which
    is monotone, so ranks, AUPRC and thresholds are unchanged and the
    scores lie in [0, 1] as `metrics.summarize` needs."""
    if hasattr(model, "predict_proba"):
        return model.predict_proba(X)[:, 1]
    from scipy.special import expit
    return expit(model.decision_function(X))


def data(seed: int) -> dict:
    import data as dmod
    df = dmod.load_ulb().drop_duplicates().reset_index(drop=True)
    s = dmod.stratified_split(df, seed)
    return {"Xtr": s.X_train.to_numpy(np.float64), "Xva": s.X_val.to_numpy(np.float64),
            "Xte": s.X_test.to_numpy(np.float64),
            "ytr": s.y_train.to_numpy().astype(int),
            "yva": s.y_val.to_numpy().astype(int),
            "yte": s.y_test.to_numpy().astype(int)}


def stratified_rows(y: np.ndarray, size: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    keep = []
    for c in (0, 1):
        idx = np.nonzero(y == c)[0]
        k = max(1, int(round(size * len(idx) / len(y))))
        keep.append(rng.choice(idx, min(k, len(idx)), replace=False))
    return np.sort(np.concatenate(keep))


def fit_classical(algo: str, params: dict, seed: int, d: dict,
                  rows: np.ndarray | None = None) -> dict:
    t0 = time.perf_counter()
    Xtr, ytr = (d["Xtr"], d["ytr"]) if rows is None \
        else (d["Xtr"][rows], d["ytr"][rows])
    m = make(algo, params, seed).fit(Xtr, ytr)
    out = {"model": m, "p_va": scores(m, d["Xva"])}
    out["fit_s"] = round(time.perf_counter() - t0, 2)
    return out


def parallel_ok(path: Path = F159) -> dict:
    """F159's verdict: the parallel build only if its result is complete
    and records equal pools at every fraction."""
    if not path.exists():
        return {"use": False, "why": "F159 result absent"}
    doc = json.loads(path.read_text(encoding="utf-8"))
    if not doc.get("complete"):
        return {"use": False, "why": "F159 result not complete"}
    a = doc["analysis"]
    if not a.get("all_equal"):
        return {"use": False, "why": "F159 records an unequal pool"}
    full = a.get("1.0", {}).get("speedup", {})
    best = max(full, key=full.get) if full else None
    if best is None:
        return {"use": False, "why": "F159 records no parallel speed-up at "
                                     "full rows"}
    import f159_parallel_pool as f159
    # The build runs under F159's watchdog, at F159's budget for full rows
    # (PR 63 review: the 32-worker pool once wedged for 9 hours).
    return {"use": True, "workers": int(best),
            "budget_s": f159.BUDGET_X * a["1.0"]["serial_s"],
            "why": "F159 complete with equal pools at every fraction"}


def fit_proxy(config: str, seed: int, par: dict) -> dict:
    import full_pair_pool as fpp
    import qubo_proxy as qp
    t0 = time.perf_counter()
    c = qp.CONFIGS[config]
    split, cols, Xtr, Xva, Xte, y_pm1 = qp._prep(seed, c["k"])
    lam = qp.LAMBDA_MULT * len(y_pm1)
    if config == "full" and par["use"]:
        import f159_parallel_pool as f159
        clf, _ = f159.build_with_budget(par["budget_s"], Xtr, y_pm1,
                                        c["schedule"], "dct", seed,
                                        workers=par["workers"],
                                        lambda_coef=lam)
        build = f"parallel, {par['workers']} workers"
    else:
        clf = fpp.build_full(Xtr, y_pm1, c["schedule"], "dct",
                             weak_params=qp.seeded_weak_params(seed),
                             lambda_coef=lam)
        build = "serial"
    w = qp.solve_simplex_qp(qp.h_matrix(clf, Xtr), y_pm1, lam)

    def score(X):
        return np.clip((w @ qp.h_matrix(clf, X) + 1.0) / 2.0, 0.0, 1.0)

    return {"p_tr": score(Xtr), "p_va": score(Xva), "p_te": score(Xte),
            "yva": split.y_val.to_numpy().astype(int),
            "yte": split.y_test.to_numpy().astype(int),
            "features": list(cols), "build": build,
            "n_learners": int(len(clf.h_list)),
            "fit_s": round(time.perf_counter() - t0, 2)}


# ---------------------------------------------------------------- metrics
def op_metrics(y, p, threshold: float, label: str) -> dict:
    import metrics
    from sklearn.metrics import balanced_accuracy_score, matthews_corrcoef
    op = metrics.evaluate_at(y, p, threshold, label)
    c = op["confusion"]
    yhat = (np.asarray(p) >= threshold).astype(int)
    op["specificity"] = c["tn"] / (c["tn"] + c["fp"]) if c["tn"] + c["fp"] else 0.0
    op["mcc"] = float(matthews_corrcoef(y, yhat))
    op["balanced_accuracy"] = float(balanced_accuracy_score(y, yhat))
    return op


def fold_metrics(y, p_va_y, p_va, p_te, p_tr_y, p_tr, seed) -> dict:
    import metrics
    import outcome_record as orec
    from sklearn.metrics import average_precision_score
    s = metrics.summarize(y, p_va_y, p_va, p_te, seed=seed)
    prev = float(np.mean(y))
    s["operating_points"] = [
        op_metrics(y, p_te, metrics.threshold_max_f1(p_va_y, p_va), "max_f1_on_val"),
        op_metrics(y, p_te, metrics.threshold_alert_budget(p_va, orec.ALERT_BUDGET),
                   f"alert_budget_{orec.ALERT_BUDGET}")]
    s["auprc_floor_normalized"] = (s["auprc"] - prev) / (1 - prev)
    s["recall_at_budget_on_test"] = float(
        orec.flagged_at_budget(p_te)[np.asarray(y) == 1].mean())
    s["train_auprc"] = float(average_precision_score(p_tr_y, p_tr))
    s["train_test_auprc_gap"] = s["train_auprc"] - s["auprc"]
    s.pop("calibration", None)          # not among F157's metrics
    return s


# ---------------------------------------------------------------- lanes
def choose(tried: list[dict]) -> int:
    """Index of the highest validation AUPRC; ties go to the first listed."""
    best = max(t["val_auprc"] for t in tried)
    return next(i for i, t in enumerate(tried) if t["val_auprc"] == best)


def lane(algo: str, seed: int, d: dict, par: dict) -> tuple[dict, np.ndarray]:
    import outcome_record as orec
    from sklearn.metrics import average_precision_score
    tried, fits = [], []
    for params in GRIDS[algo]:
        if algo == "proxy":
            f = fit_proxy(params["config"], seed, par)
            yva = f["yva"]
            if not np.array_equal(f["yte"], d["yte"]):
                raise ValueError("the proxy's test rows are not the split's")
        else:
            f = fit_classical(algo, params, seed, d)
            yva = d["yva"]
        tried.append({"params": params, "fit_s": f["fit_s"],
                      "val_auprc": float(average_precision_score(yva, f["p_va"]))})
        fits.append(f)
    i = choose(tried)
    f = fits[i]
    if algo == "proxy":
        p_te, p_tr, ytr = f["p_te"], f["p_tr"], d["ytr"]
        extra = {k: f[k] for k in ("features", "build", "n_learners")}
    else:
        p_te, p_tr, ytr = scores(f["model"], d["Xte"]), \
            scores(f["model"], d["Xtr"]), d["ytr"]
        extra = {}
    row = {"algorithm": algo, "seed": seed, "tried": tried, "chosen": i,
           "chosen_params": tried[i]["params"], **extra,
           "test": fold_metrics(d["yte"], d["yva"], f["p_va"], p_te, ytr,
                                p_tr, seed),
           "outcome": orec.record(f"f166_{algo}", seed, d["yte"], p_te,
                                  y_val=d["yva"], p_val=f["p_va"])}
    return row, p_te


def rbf_alternative(seed: int, d: dict) -> dict:
    from sklearn.metrics import average_precision_score
    rows = stratified_rows(d["ytr"], RBF_ROWS, seed)
    tried = []
    for params in RBF_GRID:
        f = fit_classical("rbf", params, seed, d, rows)
        tried.append({"params": params, "fit_s": f["fit_s"],
                      "val_auprc": float(average_precision_score(d["yva"], f["p_va"]))})
    return {"rows": int(len(rows)), "tried": tried,
            "best_val_auprc": max(t["val_auprc"] for t in tried)}


def seed_run(seed: int, par: dict) -> tuple[dict, dict]:
    t0 = time.perf_counter()
    d = data(seed)
    lanes, p_test = {}, {}
    for algo in ALGOS:
        t1 = time.perf_counter()
        lanes[algo], p_test[algo] = lane(algo, seed, d, par)
        lanes[algo]["lane_s"] = round(time.perf_counter() - t1, 1)
        print(f"  s{seed} {algo:9s} test auprc {lanes[algo]['test']['auprc']:.4f}"
              f" {lanes[algo]['lane_s']} s", flush=True)
    rbf = rbf_alternative(seed, d)
    linear_best = max(t["val_auprc"] for t in lanes["svm"]["tried"])
    rbf["beats_linear_on_validation"] = bool(rbf["best_val_auprc"] > linear_best)
    row = {"seed": seed, "lanes": lanes, "svm_rbf_alternative": rbf,
           "minutes": round((time.perf_counter() - t0) / 60, 2)}
    return row, {"y": d["yte"], **p_test}


def choose_seeds(t42_min: float) -> dict:
    n = min(MAX_SEEDS, math.floor(CAP_MIN / t42_min)) if t42_min > 0 else MAX_SEEDS
    n = max(MIN_SEEDS, n)
    return {"t42_minutes": t42_min, "n_seeds": n,
            "seeds": list(range(FIRST_SEED, FIRST_SEED + n)),
            "projected_minutes": round(n * t42_min, 1),
            "over_cap": n * t42_min > CAP_MIN,
            "below_section2_five_seeds": n < 5}


# ---------------------------------------------------------------- analysis
def t_summary(values) -> dict:
    from scipy import stats
    v = np.asarray(values, dtype=float)
    n = len(v)
    mean = float(v.mean())
    sd = float(v.std(ddof=1)) if n > 1 else float("nan")
    half = float(stats.t.ppf(0.975, n - 1) * sd / math.sqrt(n)) if n > 1 else float("nan")
    return {"n": n, "mean": mean, "sd": sd, "t95": [mean - half, mean + half]}


def boot_seed_mean_diff(y_by_seed, pa_by_seed, pb_by_seed,
                        n_boot: int = N_BOOT, seed: int = 0) -> np.ndarray:
    """Draws of the seed-mean AUPRC difference; test rows resampled within
    each seed, stratified, the same rows for both algorithms."""
    import metrics
    from sklearn.metrics import average_precision_score as ap
    rng = np.random.default_rng(seed)
    draws = np.zeros(n_boot)
    for y, pa, pb in zip(y_by_seed, pa_by_seed, pb_by_seed):
        idx = metrics.stratified_indices(y, rng, n_boot)
        draws += np.array([ap(y[i], pa[i]) - ap(y[i], pb[i]) for i in idx])
    return draws / len(y_by_seed)


def pair_test(diffs, draws, n: int) -> dict:
    from scipy import stats
    level = 1 - ALPHA / N_PAIRS
    lo, hi = np.quantile(draws, [(1 - level) / 2, 1 - (1 - level) / 2])
    boot = {"low": float(lo), "high": float(hi), "level": level,
            "rejects": bool(lo > 0 or hi < 0)}
    v = np.asarray(diffs, dtype=float)
    if np.all(v == 0):
        wil = {"p": 1.0, "rejects": False, "note": "every difference is zero"}
    else:
        p = float(stats.wilcoxon(v, alternative="two-sided", method="exact").pvalue)
        wil = {"p": p, "rejects": p < ALPHA / N_PAIRS}
    primary = "wilcoxon" if n >= WILCOXON_MIN_SEEDS else "bootstrap"
    rejects = (wil if primary == "wilcoxon" else boot)["rejects"]
    return {"primary": primary, "wilcoxon": wil, "bootstrap": boot,
            "mean_diff": float(v.mean()),
            "reading": ("above" if rejects and v.mean() > 0 else
                        "below" if rejects else "no reliable difference")}


def analyze(rows: list[dict], scores_by_seed: dict) -> dict:
    n = len(rows)
    per_algo = {}
    for a in ALGOS:
        t = [r["lanes"][a]["test"] for r in rows]
        per_algo[a] = {k: t_summary([x[k] for x in t]) for k in
                       ("auprc", "auprc_floor_normalized", "auc_roc",
                        "recall_at_budget_on_test", "train_test_auprc_gap")}
        for op in (0, 1):
            name = t[0]["operating_points"][op]["operating_point"]
            per_algo[a][name] = {k: t_summary([x["operating_points"][op][k] for x in t])
                                 for k in ("precision", "recall", "specificity",
                                           "f1", "mcc", "balanced_accuracy")}
    order = sorted(ALGOS, key=lambda a: -per_algo[a]["auprc"]["mean"])
    seeds = [r["seed"] for r in rows]
    pairs = []
    if all(s in scores_by_seed for s in seeds):
        for a, b in zip(order, order[1:]):
            diffs = [r["lanes"][a]["test"]["auprc"] - r["lanes"][b]["test"]["auprc"]
                     for r in rows]
            draws = boot_seed_mean_diff([scores_by_seed[s]["y"] for s in seeds],
                                        [scores_by_seed[s][a] for s in seeds],
                                        [scores_by_seed[s][b] for s in seeds])
            pairs.append({"a": a, "b": b, **pair_test(diffs, draws, n)})
    rbf_wins = sum(r["svm_rbf_alternative"]["beats_linear_on_validation"] for r in rows)
    return {"n_seeds": n, "order_by_mean_test_auprc": order,
            "per_algorithm": per_algo, "adjacent_pairs": pairs,
            "svm_form": {"rbf_beats_linear_seeds": rbf_wins,
                         "kept": "rbf" if rbf_wins > n / 2 else "linear"}}


# ---------------------------------------------------------------- run
def load_scores(rows: list[dict]) -> dict:
    """Per-seed test labels and scores, read back from the outcome blocks'
    saved files."""
    out = {}
    for r in rows:
        s = {}
        for a in ALGOS:
            f = ROOT / r["lanes"][a]["outcome"]["test_scores"]["path"]
            z = np.load(f)
            s[a] = np.asarray(z["p_test"], dtype=float)
            s["y"] = np.asarray(z["y_test"]).astype(int)
        out[r["seed"]] = s
    return out


def _doc(rows, plan, par, complete=False):
    doc = {"card": "F166", "sprint": 29, "phase": 2, "evidence_tag": "SIM",
           "metered_seconds": 0, "dataset": "ulb",
           "entry": "experiments/phase2/PREREGISTRATION_DRAFT.md section 6, "
                    "F166 (15775da)",
           "grids": GRIDS, "svm_rbf_grid": RBF_GRID, "rbf_rows": RBF_ROWS,
           "proxy_build": par, "seed_plan": plan,
           "seeds": [r["seed"] for r in rows], "rows": rows,
           "complete": complete}
    return doc


def run() -> None:
    import provenance
    rid, resume = provenance.start(OUT)
    prior = json.loads(OUT.read_text(encoding="utf-8")) if resume else {}
    rows, plan = prior.get("rows", []), prior.get("seed_plan")
    par = prior.get("proxy_build") or parallel_ok()
    print("proxy build", par, flush=True)
    done = {r["seed"] for r in rows}
    if FIRST_SEED not in done:
        row, _ = seed_run(FIRST_SEED, par)
        rows.append(row)
        plan = choose_seeds(row["minutes"])
        provenance.write_result(OUT, _doc(rows, plan, par), __file__,
                                [r["seed"] for r in rows], rid)
        print("seed plan", json.dumps(plan), flush=True)
    for seed in plan["seeds"]:
        if seed in {r["seed"] for r in rows}:
            continue           # resume: never refit a seed
        row, _ = seed_run(seed, par)
        rows.append(row)
        provenance.write_result(OUT, _doc(rows, plan, par), __file__,
                                [r["seed"] for r in rows], rid)
    doc = _doc(rows, plan, par, complete=True)
    doc["analysis"] = analyze(rows, load_scores(rows))
    rbf_kept(doc["analysis"])
    provenance.write_result(OUT, doc, __file__, [r["seed"] for r in rows], rid)
    print("complete", flush=True)


def rbf_kept(analysis: dict) -> None:
    """The entry keeps the RBF form as the SVM lane's if it wins on most
    seeds. The lane scores LinearSVC only, so a kept RBF would rank the
    linear SVM under an RBF label (PR 63 review). Stop before `complete`
    instead; the seeds stay recorded for a lane that scores RBF."""
    if analysis["svm_form"]["kept"] == "rbf":
        raise RuntimeError(
            "the RBF SVM won on most seeds, and the svm lane scores the "
            "linear SVM only; the run is not marked complete")


def main(argv=None) -> int:
    mode = (argv or sys.argv[1:] or [""])[0]
    if mode == "run":
        import f159_parallel_pool as f159
        try:
            run()
        except BaseException:
            f159.leave_if_abandoned(failed=True)    # a watchdog fired
            raise
        f159.leave_if_abandoned(failed=False)
    elif mode == "analyze":
        doc = json.loads(OUT.read_text(encoding="utf-8"))
        print(json.dumps(analyze(doc["rows"], load_scores(doc["rows"])), indent=1))
    else:
        raise SystemExit("mode required: run | analyze")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
