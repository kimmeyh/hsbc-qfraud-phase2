"""F151: why F130's ULB HGB comparator was unstable, by one setting at a time.

Sprint 28 Task A (#48). Zero metered seconds. F130's exact preparation
(`qubo_proxy._prep(seed, 13)`: deduplicated ULB, 60/20/20 stratified, the
13 mutual-information features) and its five seeds (42-46). Each variant
moves one HistGradientBoosting setting from the default, so a variant that
closes the spread names the setting.

"The spread closes" (Sprint 28 plan, "Show each threshold can fire"),
fixed before this run: over the five seeds, SD of test AUPRC at most 0.03
AND range at most 0.10 AND mean within 0.03 of Phase 1's XGBoost matched13
on the same seeds (read from `experiments/results/results.json`, about
0.816). The level term is there because F130's "no early stopping" row was
stable at 0.219.

Every row carries an outcome block (F154 standing rule).

Run:  <venv python> experiments/phase2/src/f151_hgb_cause.py
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

OUT = ROOT / "experiments" / "phase2" / "results" / "f151_hgb_cause.json"
RESULTS = ROOT / "experiments" / "results" / "results.json"
SEEDS = (42, 43, 44, 45, 46)
K = 13
XGB_MATCHED13 = "03999a57a5107f44"      # Phase 1 xgboost, matched13 features
SD_MAX, RANGE_MAX, LEVEL_TOL = 0.03, 0.10, 0.03

# One setting moved from the default per variant, except the last, which
# combines the two single moves so later tasks can choose between them.
VARIANTS = {
    "default": {},
    "l2_0p1": {"l2_regularization": 0.1},
    "l2_1p0": {"l2_regularization": 1.0},
    "no_early_stopping": {"early_stopping": False},
    "l2_1p0_no_early_stopping": {"l2_regularization": 1.0, "early_stopping": False},
}


def reference_level(rows: list[dict] | None = None) -> float:
    rows = rows if rows is not None else \
        json.loads(RESULTS.read_text(encoding="utf-8"))["rows"]
    v = [r["metrics"]["auprc"] for r in rows
         if r.get("config_hash") == XGB_MATCHED13 and r.get("seed") in SEEDS
         and r.get("protocol") == "stratified"]
    if len(v) != len(SEEDS):
        raise ValueError(f"expected {len(SEEDS)} reference rows, found {len(v)}")
    return float(np.mean(v))


def spread_closes(auprcs: list[float], level: float) -> dict:
    a = np.asarray(auprcs, dtype=float)
    sd, rng, mean = float(a.std(ddof=1)), float(a.max() - a.min()), float(a.mean())
    return {"mean": mean, "sd": sd, "range": rng, "reference_level": level,
            "sd_ok": sd <= SD_MAX, "range_ok": rng <= RANGE_MAX,
            "level_ok": abs(mean - level) <= LEVEL_TOL,
            "closes": bool(sd <= SD_MAX and rng <= RANGE_MAX
                           and abs(mean - level) <= LEVEL_TOL)}


def run() -> dict:
    from sklearn.ensemble import HistGradientBoostingClassifier
    from sklearn.metrics import average_precision_score, roc_auc_score
    import qubo_proxy as qp
    level = reference_level()
    rows = []
    for seed in SEEDS:
        split, cols, Xtr, Xva, Xte, _ = qp._prep(seed, K)
        ytr, yva, yte = (s.to_numpy() for s in (split.y_train, split.y_val, split.y_test))
        for name, kw in VARIANTS.items():
            t0 = time.time()
            m = HistGradientBoostingClassifier(random_state=seed, **kw).fit(Xtr, ytr)
            p_te, p_va = m.predict_proba(Xte)[:, 1], m.predict_proba(Xva)[:, 1]
            rows.append({
                "seed": seed, "variant": name, "params": kw,
                "n_iter": int(m.n_iter_),
                "test_auprc": float(average_precision_score(yte, p_te)),
                "test_auc_roc": float(roc_auc_score(yte, p_te)),
                "val_auprc": float(average_precision_score(yva, p_va)),
                "features": list(cols),
                "elapsed_s": round(time.time() - t0, 1),
                "outcome": orec.record(f"f151_hgb_{name}", seed, yte, p_te,
                                       y_val=yva, p_val=p_va)})
            print(f"  s{seed} {name:26s} iter {rows[-1]['n_iter']:4d} "
                  f"auprc {rows[-1]['test_auprc']:.4f}", flush=True)
    summary = {n: {**spread_closes([r["test_auprc"] for r in rows if r["variant"] == n],
                                   level),
                   "n_iter": [r["n_iter"] for r in rows if r["variant"] == n]}
               for n in VARIANTS}
    return {"generator": "experiments/phase2/src/f151_hgb_cause.py",
            "card": "F151", "sprint": 28, "evidence_tag": "SIM",
            "metered_seconds": 0, "seeds": list(SEEDS), "k": K,
            "preparation": "qubo_proxy._prep(seed, 13), unchanged (F130's)",
            "rule": {"sd_max": SD_MAX, "range_max": RANGE_MAX,
                     "level_tolerance": LEVEL_TOL,
                     "reference": f"results.json config_hash {XGB_MATCHED13}"},
            "rows": rows, "summary": summary}


F130 = ROOT / "experiments" / "phase2" / "results" / "f130_levers.json"
REFERENCE_VARIANT = "l2_1p0"            # the single move that closes the spread


def restate_f130(f151_rows: list[dict], f130: dict | None = None) -> dict:
    """F130's ULB variants against the stable HGB, paired by seed (95% t).

    F130 voided its "beats HGB" because its HGB was the unstable default.
    Same preparation, same seeds, so the pairing holds."""
    from scipy import stats
    f130 = f130 if f130 is not None else json.loads(F130.read_text(encoding="utf-8"))
    ref = {r["seed"]: r["test_auprc"] for r in f151_rows
           if r["variant"] == REFERENCE_VARIANT}
    out = {}
    rows = f130["ulb_full"]["rows"]
    for v in sorted({r["variant"] for r in rows}):
        d = [r["test_auprc"] - ref[r["seed"]] for r in rows if r["variant"] == v]
        a = np.asarray(d)
        half = float(stats.t.ppf(0.975, len(a) - 1) * a.std(ddof=1) / np.sqrt(len(a)))
        out[v] = {"n_seeds": len(a), "mean_delta_vs_stable_hgb": float(a.mean()),
                  "ci95": [float(a.mean() - half), float(a.mean() + half)],
                  "per_seed": [float(x) for x in a]}
    return {"reference": f"f151 variant {REFERENCE_VARIANT}",
            "source": "experiments/phase2/results/f130_levers.json ulb_full",
            "variants": out}


def main() -> None:
    if "--restate-only" in sys.argv:
        res = json.loads(OUT.read_text(encoding="utf-8"))
        res["f130_restated"] = restate_f130(res["rows"])
        OUT.write_text(json.dumps(res, indent=1), encoding="utf-8")
        print(json.dumps(res["f130_restated"]["variants"], indent=1))
        return
    res = run()
    res["f130_restated"] = restate_f130(res["rows"])
    tmp = OUT.with_suffix(".tmp.json")
    tmp.write_text(json.dumps(res, indent=1), encoding="utf-8")
    tmp.replace(OUT)
    for n, s in res["summary"].items():
        print(f"{n:26s} mean {s['mean']:.3f} sd {s['sd']:.3f} range {s['range']:.3f} "
              f"closes {s['closes']}")


if __name__ == "__main__":
    main()
