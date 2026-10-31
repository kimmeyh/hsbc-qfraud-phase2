"""F174 (Sprint 30 Task D, #78): best achievable result per algorithm on
IEEE-CIS, classical and proxy lanes (F157 part 2).

The entry is "F174" in `experiments/phase2/PREREGISTRATION_DRAFT.md`
section 6, committed before this module existed. F166's seven algorithms
and grids, imported from `f166_ulb_algorithms` unchanged, on IEEE-CIS's
month folds: every configuration is fitted on months 0-2 and chosen on
month 3; the chosen one is fitted again on months 0-3 and scored once on
month 4. Seeds 42-51, no time cap (Sprint 30 D4 and D5); seed 42 runs
first and its time is recorded.

    <venv python> experiments/phase2/src/f174_ieee_algorithms.py run
    <venv python> experiments/phase2/src/f174_ieee_algorithms.py analyze

Zero metered seconds. Writes `experiments/phase2/results/f174_ieee_algorithms.json`
through `provenance.write_result` after every seed; resumable by seed
(`provenance.start`), with `complete` true at the end and a final
`complete` line on stdout.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "experiments" / "src"))
import f166_ulb_algorithms as f166  # noqa: E402

OUT = ROOT / "experiments" / "phase2" / "results" / "f174_ieee_algorithms.json"
# F168 part 7: a long run resumes through provenance.start.
LONG_RUN = True
ALGOS = f166.ALGOS
GRIDS = f166.GRIDS
SEEDS = tuple(range(42, 52))           # D5: 10 seeds, no time cap
VAL_MONTH, TEST_MONTH = 3, 4
CONTROLS_SEED = 42                     # as F152
MI_ROWS = 50_000                       # as F160
IMPUTED = ("logreg", "svm", "rbf")


# ---------------------------------------------------------------- data
def fold_data(df, fold) -> dict:
    """One month fold: features fitted on its training months, then the
    item-4 controls on its training rows."""
    import ieee_controls
    import ieee_features
    import ieee_harness as ih
    b = ih.build_fold(df, fold)
    ytr = b["parts"]["y_train"].to_numpy().astype(int)
    yev = b["parts"]["y_eval"].to_numpy().astype(int)
    day_tr = ieee_features.add_day(b["parts"]["X_train"]).to_numpy()
    ctrl = ieee_controls.apply_item4_controls(b["X_train"], ytr, day_tr,
                                              seed=CONTROLS_SEED)
    keep = list(ctrl["features"])
    if not keep:
        raise RuntimeError(f"month {fold.eval_month}: the item-4 controls "
                           "removed every feature")
    Xtr, Xev = b["X_train"][keep], b["X_eval"][keep]
    return {"Xtr": Xtr, "Xev": Xev, "ytr": ytr, "yev": yev,
            "meta": {"eval_month": int(fold.eval_month),
                     "train_months": [int(m) for m in fold.train_months],
                     "n_train": int(len(ytr)), "n_eval": int(len(yev)),
                     "prevalence_eval": float(yev.mean()),
                     "n_features": len(keep),
                     "controls": {k: v for k, v in ctrl.items()
                                  if k != "features"}}}


def data() -> dict:
    """The validation fold (month 3) and the test fold (month 4)."""
    import data as dmod
    import ieee_loader
    import ieee_splits
    df, n_dupes = ieee_loader.dedupe_ieee(dmod.load_ieee_cis_train())
    folds = ieee_splits.rolling_origin_folds(df, n_folds=4)
    ieee_splits.assert_no_temporal_leakage(df, folds)
    by = {int(f.eval_month): f for f in folds}
    if VAL_MONTH not in by or TEST_MONTH not in by:
        raise RuntimeError(f"folds {sorted(by)} lack month {VAL_MONTH} or "
                           f"{TEST_MONTH}")
    return {"val": fold_data(df, by[VAL_MONTH]),
            "test": fold_data(df, by[TEST_MONTH]),
            "rows_after_dedupe": int(len(df)),
            "exact_duplicates_removed": int(n_dupes)}


# ---------------------------------------------------------------- models
def make(algo: str, params: dict, seed: int):
    """F166's estimator; the linear models fill missing values with the
    training median first (the entry)."""
    m = f166.make(algo, params, seed)
    if algo in IMPUTED:
        from sklearn.impute import SimpleImputer
        from sklearn.pipeline import make_pipeline
        return make_pipeline(SimpleImputer(strategy="median"), m)
    return m


def fit_classical(algo, params, seed, X, y):
    t0 = time.perf_counter()
    m = make(algo, params, seed).fit(X.to_numpy(np.float64), y)
    return m, round(time.perf_counter() - t0, 2)


def proxy_fit(config: str, seed: int, X, y) -> dict:
    """The proxy on one fold's training rows: median fill, top-k features on
    a stratified 50,000-row subsample, the serial full-pair build, the
    simplex solve."""
    import full_pair_pool as fpp
    import qubo_proxy as qp
    import data as dmod
    import pandas as pd
    t0 = time.perf_counter()
    c = qp.CONFIGS[config]
    med = X.median()
    Xf = X.fillna(med).fillna(0.0)
    sub = f166.stratified_rows(y, MI_ROWS, seed)
    cols = dmod.top_k_features(Xf.iloc[sub], pd.Series(y[sub]), c["k"],
                               seed=seed)
    y_pm1 = np.where(y == 1, 1, -1)
    lam = qp.LAMBDA_MULT * len(y_pm1)
    Xtr = Xf[cols].to_numpy(np.float32)
    clf = fpp.build_full(Xtr, y_pm1, c["schedule"], "dct",
                         weak_params=qp.seeded_weak_params(seed),
                         lambda_coef=lam)
    w = qp.solve_simplex_qp(qp.h_matrix(clf, Xtr), y_pm1, lam)

    def score(Xn):
        Z = Xn.fillna(med).fillna(0.0)[cols].to_numpy(np.float32)
        return np.clip((w @ qp.h_matrix(clf, Z) + 1.0) / 2.0, 0.0, 1.0)
    return {"score": score, "p_tr": score(X), "features": list(cols),
            "n_learners": int(len(clf.h_list)),
            "fit_s": round(time.perf_counter() - t0, 2)}


# ---------------------------------------------------------------- lanes
def lane(algo: str, seed: int, d: dict,
         pred_dir: Path | None = None) -> tuple[dict, np.ndarray]:
    """Tune on month 3, refit the chosen configuration on months 0-3,
    score month 4 once. The operating-point thresholds come from the
    tuning fit's month-3 scores (the entry)."""
    import outcome_record as orec
    from sklearn.metrics import average_precision_score
    V, T = d["val"], d["test"]
    tried, p_vas = [], []
    for params in GRIDS[algo]:
        if algo == "proxy":
            f = proxy_fit(params["config"], seed, V["Xtr"], V["ytr"])
            p_va, fit_s = f["score"](V["Xev"]), f["fit_s"]
        else:
            m, fit_s = fit_classical(algo, params, seed, V["Xtr"], V["ytr"])
            p_va = f166.scores(m, V["Xev"].to_numpy(np.float64))
        tried.append({"params": params, "fit_s": fit_s,
                      "val_auprc": float(average_precision_score(V["yev"], p_va))})
        p_vas.append(p_va)
    i = f166.choose(tried)
    t0 = time.perf_counter()
    if algo == "proxy":
        f = proxy_fit(GRIDS[algo][i]["config"], seed, T["Xtr"], T["ytr"])
        p_te, p_tr = f["score"](T["Xev"]), f["p_tr"]
        extra = {k: f[k] for k in ("features", "n_learners")}
        extra["build"] = "serial"
    else:
        m, _ = fit_classical(algo, GRIDS[algo][i], seed, T["Xtr"], T["ytr"])
        p_te = f166.scores(m, T["Xev"].to_numpy(np.float64))
        p_tr = f166.scores(m, T["Xtr"].to_numpy(np.float64))
        extra = {}
    refit_s = round(time.perf_counter() - t0, 2)
    row = {"algorithm": algo, "seed": seed, "tried": tried, "chosen": i,
           "chosen_params": tried[i]["params"], **extra, "refit_s": refit_s,
           "test": f166.fold_metrics(T["yev"], V["yev"], p_vas[i], p_te,
                                     T["ytr"], p_tr, seed),
           "outcome": orec.record(f"f174_{algo}", seed, T["yev"], p_te,
                                  y_val=V["yev"], p_val=p_vas[i],
                                  **({"pred_dir": pred_dir} if pred_dir else {}))}
    return row, p_te


def rbf_alternative(seed: int, d: dict) -> dict:
    from sklearn.metrics import average_precision_score
    V = d["val"]
    rows = f166.stratified_rows(V["ytr"], f166.RBF_ROWS, seed)
    tried = []
    for params in f166.RBF_GRID:
        m, fit_s = fit_classical("rbf", params, seed, V["Xtr"].iloc[rows],
                                 V["ytr"][rows])
        p_va = f166.scores(m, V["Xev"].to_numpy(np.float64))
        tried.append({"params": params, "fit_s": fit_s,
                      "val_auprc": float(average_precision_score(V["yev"], p_va))})
    return {"rows": int(len(rows)), "tried": tried,
            "best_val_auprc": max(t["val_auprc"] for t in tried)}


def seed_run(seed: int, d: dict) -> dict:
    t0 = time.perf_counter()
    lanes = {}
    for algo in ALGOS:
        t1 = time.perf_counter()
        lanes[algo], _ = lane(algo, seed, d)
        lanes[algo]["lane_s"] = round(time.perf_counter() - t1, 1)
        print(f"  s{seed} {algo:9s} test auprc "
              f"{lanes[algo]['test']['auprc']:.4f} {lanes[algo]['lane_s']} s",
              flush=True)
    rbf = rbf_alternative(seed, d)
    linear_best = max(t["val_auprc"] for t in lanes["svm"]["tried"])
    rbf["beats_linear_on_validation"] = bool(rbf["best_val_auprc"] > linear_best)
    return {"seed": seed, "lanes": lanes, "svm_rbf_alternative": rbf,
            "minutes": round((time.perf_counter() - t0) / 60, 2)}


# ---------------------------------------------------------------- run
def _doc(rows, folds, complete=False):
    return {"card": "F174", "sprint": 30, "phase": 2, "evidence_tag": "SIM",
            "metered_seconds": 0, "dataset": "ieee_cis",
            "entry": "experiments/phase2/PREREGISTRATION_DRAFT.md section 6, "
                     "F174",
            "protocol": {"tune": f"fit months 0-2, choose on month {VAL_MONTH}",
                         "test": f"refit months 0-3, score month {TEST_MONTH}",
                         "thresholds": "from the tuning fit's month-3 scores",
                         "seed_varies": "model random state and the proxy's "
                                        "feature-ranking subsample only"},
            "grids": GRIDS, "svm_rbf_grid": f166.RBF_GRID,
            "rbf_rows": f166.RBF_ROWS, "mi_rows": MI_ROWS,
            "seed_plan": {"rule": "Sprint 30 D4 and D5: 10 seeds, no time cap",
                          "seeds": list(SEEDS),
                          "t42_minutes": next((r["minutes"] for r in rows
                                               if r["seed"] == 42), None)},
            "folds": folds, "seeds": [r["seed"] for r in rows], "rows": rows,
            "complete": complete}


def run() -> None:
    import provenance
    rid, resume = provenance.start(OUT)
    prior = json.loads(OUT.read_text(encoding="utf-8")) if resume else {}
    rows = prior.get("rows", [])
    t0 = time.perf_counter()
    d = data()
    folds = {"validation": d["val"]["meta"], "test": d["test"]["meta"],
             "rows_after_dedupe": d["rows_after_dedupe"],
             "exact_duplicates_removed": d["exact_duplicates_removed"]}
    print(f"folds built in {round(time.perf_counter() - t0)} s:",
          json.dumps({k: v for k, v in folds.items()
                      if k in ("rows_after_dedupe",)}), flush=True)
    for seed in SEEDS:
        if seed in {r["seed"] for r in rows}:
            continue           # resume: never refit a seed
        rows.append(seed_run(seed, d))
        provenance.write_result(OUT, _doc(rows, folds), __file__,
                                [r["seed"] for r in rows], rid)
        print(f"seed {seed} done, {rows[-1]['minutes']} min", flush=True)
    doc = _doc(rows, folds, complete=True)
    doc["analysis"] = f166.analyze(rows, f166.load_scores(rows))
    f166.rbf_kept(doc["analysis"])
    provenance.write_result(OUT, doc, __file__, [r["seed"] for r in rows], rid)
    print("complete", flush=True)


def main(argv=None) -> int:
    mode = (argv or sys.argv[1:] or [""])[0]
    if mode == "run":
        run()
    elif mode == "analyze":
        doc = json.loads(OUT.read_text(encoding="utf-8"))
        print(json.dumps(f166.analyze(doc["rows"], f166.load_scores(doc["rows"])),
                         indent=1))
    else:
        raise SystemExit("mode required: run | analyze")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
