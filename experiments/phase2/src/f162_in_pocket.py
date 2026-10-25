"""F162: inside the SPECTRA pocket, does the CVQBoost proxy beat HGB and XGBoost?

Sprint 28 Task M (#59). Zero metered seconds. The entry is
`experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F162", committed
before any score (9b7f770).

Protocol (the SPECTRA authors' recommendation, 2026-10-23): covariates plus
phases only, `target`, `target_real` and `in_pocket` never features
(`spectra_segment._prep_spectra` asserts it); label `target`; AUPRC and
ROC-AUC overall and inside the pocket (`in_pocket` = 1) separately.

Three lanes per (cell, seed), each fitted on the training fold only:
  proxy    the frozen cell's CVQBoost configuration, pool seeded
  hgb      HistGradientBoostingClassifier(l2_regularization=1.0), F151
  xgboost  XGBClassifier at library defaults

Primary (m = 6): per cell, proxy minus hgb and proxy minus xgboost in
in-pocket AUPRC, exact two-sided Wilcoxon over seeds at 0.05 / 6, with the
t interval at 1 - 0.05 / 6 beside it.

Modes (one is required; there is no default):
  run      seed 42 on every cell first, timed; the seed count (10, or 8 if
           seed 42 projects ten above the cap) is recorded from the time
           alone; then the rest. Resumable: a (cell, seed) on file is
           skipped, never fitted twice. Saved after every (cell, seed).
  analyze  the primary and secondary results, from the recorded rows

Run:  <venv python> experiments/phase2/src/f162_in_pocket.py run|analyze
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
import outcome_record as orec  # noqa: E402  (Phase 2)
import strict_json  # noqa: E402  (Phase 2)

OUT = ROOT / "experiments" / "phase2" / "results" / "f162_in_pocket.json"
CELLS = ("telecom_churn", "energy_steel", "oilgas_gasturbine")
LANES = ("proxy", "hgb", "xgboost")
COMPARISONS = (("proxy", "hgb"), ("proxy", "xgboost"))
SEEDS_FULL = tuple(range(42, 52))
SEEDS_CUT = tuple(range(42, 50))     # k = 8: the Wilcoxon floor for m = 6
FIRST_SEED = 42
CAP_MIN = 120.0
M = len(CELLS) * len(COMPARISONS)
ALPHA = 0.05
HGB_L2 = 1.0
LABELS = ("target", "target_real", "in_pocket")


# ------------------------------------------------------------------ data
def check_features(cols) -> None:
    leaked = sorted(set(cols) & set(LABELS))
    if leaked:
        raise ValueError(f"label columns among the features: {leaked}")


def prepare(name: str, seed: int) -> dict:
    import spectra_segment as ss
    cell = ss.frozen_cell_by_name(name)
    split, cols = ss._prep_spectra(name, seed)
    check_features(cols)
    if len(cols) != cell["config"]["n_features"]:
        raise ValueError(f"{name}: {len(cols)} features, the frozen cell "
                         f"has {cell['config']['n_features']}")

    def X(df):
        return ss.coerce_features_to_numeric(df[cols]).to_numpy(dtype="float32")

    return {"cell": cell, "features": cols,
            "Xtr": X(split.X_train), "Xva": X(split.X_val), "Xte": X(split.X_test),
            "ytr": split.y_train.to_numpy().astype(int),
            "yva": split.y_val.to_numpy().astype(int),
            "yte": split.y_test.to_numpy().astype(int),
            "pocket": split.X_test[ss.SEGMENT_FLAG].to_numpy().astype(bool)}


# ----------------------------------------------------------------- lanes
def fit_proxy(d: dict, seed: int) -> dict:
    import qubo_proxy as qp
    c = d["cell"]["config"]
    y_pm1 = np.where(d["ytr"] == 1, 1, -1)
    lam = c["lambda_coef_alpha"] * len(y_pm1)
    clf = qp.build_pool(d["Xtr"], y_pm1, c["weak_cls_schedule"], "dct",
                        "sequential",
                        weak_params=qp.seeded_weak_params(seed, c["weak_cls_params"]),
                        lambda_coef=lam)
    w = qp.solve_simplex_qp(qp.h_matrix(clf, d["Xtr"]), y_pm1, lam)

    def score(X):
        return np.clip((w @ qp.h_matrix(clf, X) + 1.0) / 2.0, 0.0, 1.0)

    return {"p_tr": score(d["Xtr"]), "p_va": score(d["Xva"]), "p_te": score(d["Xte"]),
            "n_learners": int(len(clf.h_list)),
            "n_nonzero_weights": int((np.asarray(w) > 1e-9).sum())}


def hgb_model(seed: int):
    from sklearn.ensemble import HistGradientBoostingClassifier
    return HistGradientBoostingClassifier(l2_regularization=HGB_L2, random_state=seed)


def xgb_model(seed: int):
    from xgboost import XGBClassifier
    return XGBClassifier(random_state=seed)


def fit_classical(model, d: dict) -> dict:
    m = model.fit(d["Xtr"], d["ytr"])
    return {k: m.predict_proba(d[x])[:, 1]
            for k, x in (("p_tr", "Xtr"), ("p_va", "Xva"), ("p_te", "Xte"))}


# --------------------------------------------------------------- scoring
def pocket_metrics(y, p, mask) -> dict:
    from sklearn.metrics import average_precision_score, roc_auc_score
    y, p, mask = np.asarray(y), np.asarray(p), np.asarray(mask, dtype=bool)
    ys, ps = y[mask], p[mask]
    if ys.min() == ys.max():
        raise ValueError("the pocket holds one class; AUPRC is undefined")
    prev = float(ys.mean())
    ap = float(average_precision_score(ys, ps))
    return {"n": int(mask.sum()), "n_positives": int(ys.sum()), "prevalence": prev,
            "auprc": ap, "auprc_normalized": (ap - prev) / (1.0 - prev),
            "auc_roc": float(roc_auc_score(ys, ps))}


def score_lane(lane: str, name: str, seed: int, d: dict, fit: dict,
               seconds: float, pred_dir: Path = orec.PRED_DIR) -> dict:
    from sklearn.metrics import average_precision_score, roc_auc_score
    ap_tr = float(average_precision_score(d["ytr"], fit["p_tr"]))
    ap_te = float(average_precision_score(d["yte"], fit["p_te"]))
    row = {"cell": name, "seed": seed, "lane": lane,
           "n_features": len(d["features"]), "features": list(d["features"]),
           "test_auprc": ap_te, "test_auc_roc": float(roc_auc_score(d["yte"], fit["p_te"])),
           "train_auprc": ap_tr, "train_test_gap_auprc": ap_tr - ap_te,
           "pocket": pocket_metrics(d["yte"], fit["p_te"], d["pocket"]),
           "seconds": round(seconds, 1),
           "outcome": orec.record(f"f162_{name}_{lane}", seed, d["yte"], fit["p_te"],
                                  y_val=d["yva"], p_val=fit["p_va"], pred_dir=pred_dir)}
    row.update({k: fit[k] for k in ("n_learners", "n_nonzero_weights") if k in fit})
    return row


def paired_pocket(d: dict, fits: dict) -> dict:
    """Per-seed paired bootstrap on in-pocket AUPRC (secondary)."""
    import metrics
    m = d["pocket"]
    out = {}
    for a, b in COMPARISONS + (("hgb", "xgboost"),):
        ci = metrics.paired_delta_ci(d["yte"][m], fits[a]["p_te"][m],
                                     fits[b]["p_te"][m], "auprc")
        out[f"{a}_minus_{b}"] = {k: ci[k] for k in ("diff", "ci95", "excludes_zero")}
    return out


def run_cell(name: str, seed: int) -> dict:
    d = prepare(name, seed)
    fits, rows = {}, []
    for lane in LANES:
        t0 = time.perf_counter()
        fits[lane] = (fit_proxy(d, seed) if lane == "proxy" else
                      fit_classical(hgb_model(seed) if lane == "hgb"
                                    else xgb_model(seed), d))
        rows.append(score_lane(lane, name, seed, d, fits[lane],
                               time.perf_counter() - t0))
    return {"rows": rows, "pair": {"cell": name, "seed": seed,
                                   "bootstrap": paired_pocket(d, fits)}}


# ------------------------------------------------------------- the seeds
def choose_seeds(first_seed_minutes: float) -> dict:
    projected = first_seed_minutes * len(SEEDS_FULL)
    seeds = SEEDS_FULL if projected <= CAP_MIN else SEEDS_CUT
    return {"first_seed_minutes": first_seed_minutes,
            "projected_minutes_ten_seeds": projected, "cap_minutes": CAP_MIN,
            "seeds": list(seeds)}


# --------------------------------------------------------------- the run
def provenance() -> dict:
    """The commit and library versions the rows were made with (Sprint 28
    D4: results can be reproduced). `generator_clean` is False when this
    file differs from that commit."""
    import subprocess
    import sklearn
    import xgboost

    def git(*a):
        return subprocess.run(["git", *a], cwd=ROOT, capture_output=True,
                              text=True, check=True).stdout.strip()

    rel = Path(__file__).resolve().relative_to(ROOT).as_posix()
    return {"generator_commit": git("rev-parse", "HEAD"),
            "generator_clean": git("status", "--porcelain", "--", rel) == "",
            "versions": {"python": sys.version.split()[0], "numpy": np.__version__,
                         "scikit-learn": sklearn.__version__,
                         "xgboost": xgboost.__version__}}


def _load() -> dict:
    if OUT.exists():
        return json.loads(OUT.read_text(encoding="utf-8"))
    return {"generator": "experiments/phase2/src/f162_in_pocket.py", "card": "F162",
            "sprint": 28, "evidence_tag": "SIM", "metered_seconds": 0,
            "provenance": provenance(),
            "entry": "experiments/phase2/PREREGISTRATION_DRAFT.md section 6, F162",
            "lanes": {"proxy": "frozen cell config, seeded pool, simplex solve",
                      "hgb": f"HistGradientBoostingClassifier(l2_regularization={HGB_L2})",
                      "xgboost": "XGBClassifier() defaults"},
            "rows": [], "pairs": []}


def _save(doc: dict) -> None:
    tmp = OUT.with_suffix(".tmp.json")
    tmp.write_text(json.dumps(doc, indent=1, default=strict_json.numpy_scalar),
                   encoding="utf-8")
    tmp.replace(OUT)


def _done(doc: dict) -> set:
    return {(p["cell"], p["seed"]) for p in doc["pairs"]}


def _add(doc: dict, name: str, seed: int) -> None:
    t0 = time.perf_counter()
    out = run_cell(name, seed)
    doc["rows"].extend(out["rows"])
    doc["pairs"].append({**out["pair"],
                         "wall_s": round(time.perf_counter() - t0, 1)})
    _save(doc)
    print(f"  {name} s{seed}: " + "  ".join(
        f"{r['lane']} pocket {r['pocket']['auprc']:.4f}" for r in out["rows"]),
        flush=True)


def run() -> None:
    doc = _load()
    if "seed_choice" not in doc:
        for name in CELLS:
            if (name, FIRST_SEED) not in _done(doc):
                _add(doc, name, FIRST_SEED)
        first = [p for p in doc["pairs"] if p["seed"] == FIRST_SEED]
        if len(first) != len(CELLS):
            raise SystemExit("seed 42 is not complete on every cell")
        # From each recorded pair's own wall time, so a resumed run still
        # projects from all of seed 42, not from the part timed now.
        doc["seed_choice"] = choose_seeds(sum(p["wall_s"] for p in first) / 60.0)
        _save(doc)
    for seed in doc["seed_choice"]["seeds"]:
        for name in CELLS:
            if (name, seed) not in _done(doc):
                _add(doc, name, seed)
    doc["analysis"] = analyze(doc)
    _save(doc)


# --------------------------------------------------------------- analysis
def compare(diffs: list[float]) -> dict:
    """Wilcoxon (exact, two-sided) and the t interval, at the family level."""
    from scipy.stats import wilcoxon
    import metrics
    d = np.asarray(diffs, dtype=float)
    if len(d) < 2 or not np.isfinite(d).all():
        raise ValueError("need at least two finite paired differences")
    w = wilcoxon(d, alternative="two-sided", method="exact")
    t = metrics.seed_mean_t_interval(list(d), alpha=ALPHA / M)
    reject = bool(w.pvalue <= ALPHA / M)
    lo, hi = t["ci95"]
    if reject and lo > 0:
        reading = "proxy above"
    elif reject and hi < 0:
        reading = "proxy below"
    else:
        reading = "no reliable difference"
    return {"n_seeds": len(d), "mean": float(d.mean()), "wilcoxon_p": float(w.pvalue),
            "alpha_family": ALPHA / M, "interval": [lo, hi],
            "interval_level": 1 - ALPHA / M, "reading": reading}


def analyze(doc: dict) -> dict:
    by = {(r["cell"], r["seed"], r["lane"]): r for r in doc["rows"]}
    seeds = doc.get("seed_choice", {}).get("seeds")
    if not seeds:
        raise ValueError("no seed choice recorded")
    missing = [(c, s, ln) for c in CELLS for s in seeds for ln in LANES
               if (c, s, ln) not in by]
    if missing:
        raise ValueError(f"{len(missing)} rows missing, first {missing[:3]}")
    out = {"seeds": seeds, "primary": {}, "secondary": {}}
    for c in CELLS:
        def v(lane, key):
            return [by[(c, s, lane)]["pocket"][key] for s in seeds]
        prim, sec = {}, {}
        for a, b in COMPARISONS:
            diffs = [x - y for x, y in zip(v(a, "auprc"), v(b, "auprc"))]
            prim[f"{a}_minus_{b}"] = compare(diffs)
        for a, b in COMPARISONS + (("hgb", "xgboost"),):
            sec[f"{a}_minus_{b}_pocket_auc_roc_mean"] = float(np.mean(
                [x - y for x, y in zip(v(a, "auc_roc"), v(b, "auc_roc"))]))
            sec[f"{a}_minus_{b}_pocket_auprc_normalized_mean"] = float(np.mean(
                [x - y for x, y in zip(v(a, "auprc_normalized"),
                                       v(b, "auprc_normalized"))]))
        sec["hgb_minus_xgboost_pocket_auprc_mean"] = float(np.mean(
            [x - y for x, y in zip(v("hgb", "auprc"), v("xgboost", "auprc"))]))
        sec["lanes"] = {ln: {
            "pocket_auprc_mean": float(np.mean(v(ln, "auprc"))),
            "pocket_auc_roc_mean": float(np.mean(v(ln, "auc_roc"))),
            "test_auprc_mean": float(np.mean([by[(c, s, ln)]["test_auprc"] for s in seeds])),
            "test_auc_roc_mean": float(np.mean([by[(c, s, ln)]["test_auc_roc"] for s in seeds])),
            "train_test_gap_auprc_mean": float(np.mean(
                [by[(c, s, ln)]["train_test_gap_auprc"] for s in seeds]))}
            for ln in LANES}
        sec["pocket_positives_by_seed"] = {
            str(s): by[(c, s, "proxy")]["pocket"]["n_positives"] for s in seeds}
        out["primary"][c] = prim
        out["secondary"][c] = sec
    above = [c for c in CELLS
             if any(p["reading"] == "proxy above" for p in out["primary"][c].values())]
    out["cells_with_proxy_above"] = above
    out["falsifier"] = {c: c not in above for c in CELLS}
    return out


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        raise SystemExit("usage: f162_in_pocket.py run|analyze (no default)")
    mode = argv[0]
    if mode == "run":
        run()
    elif mode == "analyze":
        doc = _load()
        doc["analysis"] = analyze(doc)
        _save(doc)
        print(json.dumps(doc["analysis"]["primary"], indent=1))
    else:
        raise SystemExit(f"unknown mode {mode!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
