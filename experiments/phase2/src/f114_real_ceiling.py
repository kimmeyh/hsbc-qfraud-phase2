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
    <venv python> experiments/phase2/src/f114_real_ceiling.py --lr05

`--lr05` is stage 2 of the 2026-11-05 F114 re-run amendment, run only if
stage 1 (`f169_plugin_bins.py lr05`) passes: `lgbm_lr05` in place of
`lgbm_bins`, each seed's training AUPRC recorded, written to
`f114_real_ceiling_lr05.json`. The default run is unchanged.

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
# The F114 re-run amendment (2026-11-05, Sprint 31 D11 option 1), stage 2:
# `--lr05` uses `lgbm_lr05`, writes `OUT_LR05` and records each seed's
# training AUPRC. The default run is unchanged.
ESTIMATOR = "lgbm_bins"
TRAIN_AUPRC = False
# The score files' name stem. The re-run has its own (Sprint 31 D13): with
# the first run's stem it replaced that run's nine recorded ULB files.
RECORD = "f114"
OUT_LR05 = OUT.with_name("f114_real_ceiling_lr05.json")
# Stage 1's result (`f169_plugin_bins.OUT_LR05`). Stage 2 runs only when it
# is complete and passed (Sprint 31 i2 b; the PR 92 review found `--lr05`
# never read it).
STAGE1 = OUT.with_name("f169_plugin_bins_lr05.json")
ENTRY = ("experiments/phase2/PREREGISTRATION_DRAFT.md section 6, F108, "
         "amendment 2026-11-05 (F114)")
ENTRY_LR05 = ("experiments/phase2/PREREGISTRATION_DRAFT.md section 6, F108, "
              "amendment 2026-11-05 (F114 re-run)")
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
def fit_plugin(Xtr, ytr, seed: int):
    import f169_plugin_bins as f169
    return f169.make(ESTIMATOR, seed).fit(Xtr, ytr)


def plugin_scores(Xtr, ytr, Xte, seed: int) -> np.ndarray:
    return fit_plugin(Xtr, ytr, seed).predict_proba(Xte)[:, 1]


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
    model = fit_plugin(d["Xtr"], d["ytr"], seed)
    p = model.predict_proba(d["Xte"])[:, 1]
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
           "outcome": orec.record(f"{RECORD}_{dataset}", seed, y, p)}
    if TRAIN_AUPRC:
        # Reported, not decisive: a fit that collapses shows here.
        row["train_auprc"] = float(average_precision_score(
            d["ytr"], model.predict_proba(d["Xtr"])[:, 1]))
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
            "entry": ENTRY_LR05 if ESTIMATOR == "lgbm_lr05" else ENTRY,
            "estimator": f"f169_plugin_bins.make('{ESTIMATOR}', seed)",
            "margin": {"abs": fc.MARGIN_ABS, "rel": fc.MARGIN_REL},
            "check": state.get("check"), "seed_plan": state.get("plan", {}),
            "ieee_fold": state.get("ieee_fold"),
            "rows": state["rows"],
            "summary": summarize(state.get("check"), state["rows"]),
            "complete": complete}


def seeds_used(state: dict) -> list[int]:
    """The seeds a save records. Before any seed row exists, the result
    holds only the shuffled-label check, which ran on CHECK_SEED; an empty
    list is refused by `provenance.record` (the first save of 2026-11-05
    crashed on it after the check had run)."""
    seeds = sorted({r["seed"] for r in state["rows"]})
    if state.get("check") is not None and CHECK_SEED not in seeds:
        seeds = sorted(seeds + [CHECK_SEED])
    return seeds


def select(argv: list[str]) -> bool:
    """`--lr05`: stage 2 of the F114 re-run amendment. Returns False for an
    argument this module does not take."""
    global OUT, ESTIMATOR, TRAIN_AUPRC, RECORD
    if argv == ["--lr05"]:
        OUT, ESTIMATOR, TRAIN_AUPRC = OUT_LR05, "lgbm_lr05", True
        RECORD = "f114lr05"
        return True
    return not argv


def stage1_refusal() -> str | None:
    """Why stage 2 may not run, or None: stage 1's result must be readable,
    complete and passed."""
    try:
        s = json.loads(STAGE1.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return f"stage 1's result {STAGE1.name} cannot be read ({exc})"
    if s.get("complete") is not True:
        return f"stage 1's result {STAGE1.name} is not complete"
    if (s.get("summary") or {}).get("passes") is not True:
        return f"stage 1's result {STAGE1.name} did not pass"
    return None


def main(argv: list[str] | None = None) -> int:
    argv = [] if argv is None else argv
    if not select(argv):
        print(f"usage: f114_real_ceiling.py [--lr05]; got {argv}")
        return 2
    if ESTIMATOR == "lgbm_lr05":
        why = stage1_refusal()
        if why:
            print(f"REFUSING: {why}; stage 2 runs only after stage 1 passes")
            return 2
    import provenance
    rid, resume = provenance.start(OUT)
    state = {"rows": [], "plan": {}}
    if resume:
        old = json.loads(OUT.read_text(encoding="utf-8"))
        state = {"rows": old["rows"], "plan": old["seed_plan"],
                 "check": old["check"], "ieee_fold": old.get("ieee_fold")}

    def save():
        provenance.write_result(OUT, _doc(state), __file__,
                                seeds_used(state), rid)

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
    provenance.write_result(OUT, doc, __file__, seeds_used(state), rid)
    print(json.dumps(doc["summary"], indent=1))
    print("complete", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
