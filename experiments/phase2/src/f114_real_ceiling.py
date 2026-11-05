"""F114 (Sprint 31 Task E, #97): F169's plug-in on ULB and IEEE-CIS.

The entry is the 2026-11-05 amendment to "F108" in
`experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, committed before
this module existed. The estimator is F169's `lgbm_bins`
(`f169_plugin_bins.make`, imported): LightGBM, 100 trees, 4,095 bins, no
early stopping, fit on the whole training window. The plug-in is the
mean of min(p, 1 - p) on the test rows.

Order, as the entry sets it:
  1. the shuffled-label check, ULB seed 42: training labels permuted, the
     plug-in must sit within max(0.0005, 0.10 x q) of the test fraud
     rate q; if it does not, no estimate is reported as a ceiling;
  2. per dataset, seed 42 timed, then the seed count
     n = min(10, floor(60 / t42)), at least 5, seeds 42 to 41 + n.

    <venv python> experiments/phase2/src/f114_real_ceiling.py

Zero metered seconds. Writes `experiments/phase2/results/f114_real_ceiling.json`
through `provenance.write_result` after each step; resumable, `complete`
true at the end and a final `complete` line on stdout.
"""
from __future__ import annotations

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
import f108_ceiling as fc  # noqa: E402  (the margin, not edited)

OUT = ROOT / "experiments" / "phase2" / "results" / "f114_real_ceiling.json"
# F168 part 7: a long run resumes through provenance.start.
LONG_RUN = True
DATASETS = ("ulb", "ieee")
SEEDS = tuple(range(42, 52))
MIN_SEEDS = 5
BUDGET_MIN = 60
CHECK_SEED = 42


# ------------------------------------------------------------------ data
def ulb(seed: int) -> dict:
    """F166's ULB split: duplicates dropped, stratified 60/20/20."""
    import data as dmod
    df = dmod.load_ulb().drop_duplicates().reset_index(drop=True)
    s = dmod.stratified_split(df, seed)
    return {"Xtr": s.X_train.to_numpy(np.float64),
            "ytr": s.y_train.to_numpy().astype(int),
            "Xte": s.X_test.to_numpy(np.float64),
            "yte": s.y_test.to_numpy().astype(int)}


_IEEE: dict | None = None


def ieee(seed: int) -> dict:
    """F174's month-4 fold, fixed for every seed; built once."""
    global _IEEE
    if _IEEE is None:
        import data as dmod
        import f174_ieee_algorithms as f174
        import ieee_loader
        import ieee_splits
        df, _ = ieee_loader.dedupe_ieee(dmod.load_ieee_cis_train())
        folds = ieee_splits.rolling_origin_folds(df, n_folds=4)
        ieee_splits.assert_no_temporal_leakage(df, folds)
        fold = {int(f.eval_month): f for f in folds}[f174.TEST_MONTH]
        b = f174.fold_data(df, fold)
        _IEEE = {"Xtr": b["Xtr"], "ytr": b["ytr"], "Xte": b["Xev"],
                 "yte": b["yev"], "meta": b["meta"]}
    return _IEEE


LOADERS = {"ulb": ulb, "ieee": ieee}


# ------------------------------------------------------------- the rules
def margin(q: float) -> float:
    """F108's margin with the test fraud rate q as the true value."""
    return max(fc.MARGIN_ABS, fc.MARGIN_REL * q)


def check_passes(estimate: float, q: float) -> bool:
    return abs(estimate - q) <= margin(q)


def seed_count(t42_min: float) -> int:
    """n = min(10, floor(60 / t42)), at least 5."""
    if t42_min <= 0:
        return len(SEEDS)
    return max(MIN_SEEDS, min(len(SEEDS), math.floor(BUDGET_MIN / t42_min)))


def t_interval(values) -> dict:
    from scipy import stats
    v = np.asarray(values, dtype=float)
    n = len(v)
    mean = float(v.mean())
    if n < 2:
        return {"n": n, "mean": mean, "sd": None, "ci95": None}
    sd = float(v.std(ddof=1))
    h = float(stats.t.ppf(0.975, n - 1)) * sd / math.sqrt(n)
    return {"n": n, "mean": mean, "sd": sd, "ci95": [mean - h, mean + h]}


# --------------------------------------------------------------- fitting
def plugin_scores(Xtr, ytr, Xte, seed: int) -> np.ndarray:
    import f169_plugin_bins as f169
    return f169.make("lgbm_bins", seed).fit(Xtr, ytr).predict_proba(Xte)[:, 1]


def shuffle_check() -> dict:
    d = ulb(CHECK_SEED)
    rng = np.random.default_rng(CHECK_SEED)
    t0 = time.perf_counter()
    p = plugin_scores(d["Xtr"], rng.permutation(d["ytr"]), d["Xte"],
                      CHECK_SEED)
    est = float(np.mean(np.minimum(p, 1 - p)))
    q = float(d["yte"].mean())
    return {"dataset": "ulb", "seed": CHECK_SEED, "estimate": est,
            "test_fraud_rate": q, "margin": margin(q),
            "pass": check_passes(est, q),
            "fit_s": round(time.perf_counter() - t0, 1)}


def seed_row(dataset: str, seed: int) -> dict:
    import outcome_record as orec
    from sklearn.metrics import average_precision_score
    t0 = time.perf_counter()
    d = LOADERS[dataset](seed)
    load_s = time.perf_counter() - t0
    p = plugin_scores(d["Xtr"], d["ytr"], d["Xte"], seed)
    y = d["yte"]
    est = float(np.mean(np.minimum(p, 1 - p)))
    achieved = float(np.mean((p >= 0.5).astype(int) != y))
    row = {"dataset": dataset, "seed": seed, "n_train": int(len(d["ytr"])),
           "n_test": int(len(y)), "test_positives": int(y.sum()),
           "test_fraud_rate": float(y.mean()), "estimate": est,
           "achieved_error": achieved, "consistency_gap": est - achieved,
           "auprc": float(average_precision_score(y, p)),
           "load_s": round(load_s, 1),
           "fit_s": round(time.perf_counter() - t0 - load_s, 1),
           "outcome": orec.record(f"f114_{dataset}", seed, y, p)}
    print(f"  {dataset} s{seed}: est {est:.5f} achieved {achieved:.5f} "
          f"q {row['test_fraud_rate']:.5f} auprc {row['auprc']:.3f} "
          f"{row['fit_s']} s", flush=True)
    return row


# ------------------------------------------------------------- reporting
def summarize(check: dict | None, rows: list[dict]) -> dict:
    out = {}
    for ds in DATASETS:
        live = [r for r in rows if r["dataset"] == ds]
        if not live:
            continue
        gap = t_interval([r["consistency_gap"] for r in live])
        out[ds] = {"estimate": t_interval([r["estimate"] for r in live]),
                   "achieved_error": t_interval([r["achieved_error"]
                                                 for r in live]),
                   "consistency_gap": gap,
                   "calibration_warning": bool(
                       gap["ci95"] and (gap["ci95"][0] > 0
                                        or gap["ci95"][1] < 0)),
                   "auprc": t_interval([r["auprc"] for r in live]),
                   "test_fraud_rate": live[0]["test_fraud_rate"]
                   if ds == "ieee" else t_interval(
                       [r["test_fraud_rate"] for r in live])["mean"]}
    if check is None:
        reading = "the shuffled-label check has not run"
    elif check["pass"]:
        reading = ("check passed: each interval is the plug-in ceiling "
                   "estimate, error metric, under the plug-in's calibration "
                   "assumption; not a recall ceiling")
    else:
        reading = ("check failed: the method does not transfer to real "
                   "data; the estimates are plug-in values only, never "
                   "ceilings, and F114 stays open")
    return {"by_dataset": out, "reading": reading,
            "ceilings_reported": bool(check and check["pass"])}


def _doc(state: dict, complete: bool = False) -> dict:
    return {"card": "F114", "sprint": 31, "phase": 2, "evidence_tag": "SIM",
            "metered_seconds": 0,
            "entry": "experiments/phase2/PREREGISTRATION_DRAFT.md section 6, "
                     "F108, amendment 2026-11-05 (F114)",
            "estimator": "f169_plugin_bins.make('lgbm_bins', seed)",
            "margin": {"abs": fc.MARGIN_ABS, "rel": fc.MARGIN_REL},
            "check": state.get("check"), "seed_plan": state.get("plan", {}),
            "ieee_fold": state.get("ieee_fold"),
            "rows": state["rows"],
            "summary": summarize(state.get("check"), state["rows"]),
            "complete": complete}


def main() -> int:
    import provenance
    rid, resume = provenance.start(OUT)
    state = {"rows": [], "plan": {}}
    if resume:
        old = json.loads(OUT.read_text(encoding="utf-8"))
        state = {"rows": old["rows"], "plan": old["seed_plan"],
                 "check": old["check"], "ieee_fold": old.get("ieee_fold")}

    def save():
        provenance.write_result(OUT, _doc(state), __file__,
                                [r["seed"] for r in state["rows"]], rid)

    if state.get("check") is None:
        state["check"] = shuffle_check()
        print(f"  check: {state['check']}", flush=True)
        save()
    for ds in DATASETS:
        done = {r["seed"] for r in state["rows"] if r["dataset"] == ds}
        if CHECK_SEED not in done:
            row = seed_row(ds, CHECK_SEED)
            state["rows"].append(row)
            # A seed's cost: IEEE-CIS builds its fixed fold once, so only
            # the fit repeats; ULB draws a new split every seed.
            t42 = (row["fit_s"] + (row["load_s"] if ds == "ulb" else 0)) / 60
            state["plan"][ds] = {"t42_min": round(t42, 2),
                                 "n_seeds": seed_count(t42)}
            if ds == "ieee":
                state["ieee_fold"] = ieee(CHECK_SEED)["meta"]
            save()
        for seed in SEEDS[:state["plan"][ds]["n_seeds"]]:
            if seed in {r["seed"] for r in state["rows"]
                        if r["dataset"] == ds}:
                continue           # resume: never redo a seed
            state["rows"].append(seed_row(ds, seed))
            save()
    doc = _doc(state, complete=True)
    provenance.write_result(OUT, doc, __file__,
                            [r["seed"] for r in state["rows"]], rid)
    print(json.dumps(doc["summary"], indent=1))
    print("complete", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
