"""F157 SPECTRA part (Sprint 31 Task F, #98): best achievable result per
algorithm on SPECTRA's four datasets, classical and proxy lanes.

The entry is "F157 SPECTRA part" in `experiments/phase2/PREREGISTRATION_DRAFT.md`
section 6, committed before this module existed. F166's seven algorithms
and grids (`f166_ulb_algorithms`, imported, unchanged), F174's median fill
for the linear models and its proxy fit (`f174_ieee_algorithms.proxy_fit`,
whose top-k keeps every feature when a dataset has fewer than k). Each
dataset uses the seeded 60/20/20 split of `spectra_segment`, label
`target`: every configuration is fitted on the training fold and chosen on
the validation fold; the chosen one is scored once on the test fold.

Seeds per dataset: seed 42 first, timed; n = min(10, floor(60 / t42)),
at least 3.

    <venv python> experiments/phase2/src/f157_spectra_algorithms.py run
    <venv python> experiments/phase2/src/f157_spectra_algorithms.py analyze

Zero metered seconds. Writes `experiments/phase2/results/f157_spectra_algorithms.json`
through `provenance.write_result` after every (dataset, seed); resumable,
`complete` true at the end and a final `complete` line on stdout.
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
import f166_ulb_algorithms as f166  # noqa: E402
import f174_ieee_algorithms as f174  # noqa: E402

OUT = ROOT / "experiments" / "phase2" / "results" / "f157_spectra_algorithms.json"
# F168 part 7: a long run resumes through provenance.start.
LONG_RUN = True
DATASETS = ("energy_steel", "oilgas_gasturbine", "telecom_churn",
            "maintenance_ai4i")
ALGOS, GRIDS = f166.ALGOS, f166.GRIDS
FIRST_SEED = 42
CAP_MIN = 60.0
MAX_SEEDS, MIN_SEEDS = 10, 3


# ------------------------------------------------------------------ data
def data(name: str, seed: int) -> dict:
    """The split every Phase 2 SPECTRA result uses, in F174's fold shape:
    `val` fits on the training fold and scores the validation fold;
    `test` fits on the training fold and scores the test fold."""
    import pandas as pd
    import spectra_segment as ss
    split, cols = ss._prep_spectra(name, seed)

    def X(df):
        return ss.coerce_features_to_numeric(df[cols]).astype(float)
    Xtr = pd.DataFrame(X(split.X_train)).reset_index(drop=True)
    ytr = split.y_train.to_numpy().astype(int)
    return {"features": list(cols),
            "val": {"Xtr": Xtr, "ytr": ytr,
                    "Xev": X(split.X_val).reset_index(drop=True),
                    "yev": split.y_val.to_numpy().astype(int)},
            "test": {"Xtr": Xtr, "ytr": ytr,
                     "Xev": X(split.X_test).reset_index(drop=True),
                     "yev": split.y_test.to_numpy().astype(int)},
            "pocket": split.X_test[ss.SEGMENT_FLAG].to_numpy().astype(bool)}


# ---------------------------------------------------------------- lanes
def pocket_auprc(y, p, mask) -> dict:
    from sklearn.metrics import average_precision_score
    out = {}
    for name, m in (("in_pocket", mask), ("out_of_pocket", ~mask)):
        out[name] = (float(average_precision_score(y[m], p[m]))
                     if m.any() and 0 < y[m].sum() < m.sum() else None)
    return out


def lane(name: str, algo: str, seed: int, d: dict) -> tuple[dict, np.ndarray]:
    """F174's lane on one SPECTRA split, recorded under this card's name."""
    import outcome_record as orec
    from sklearn.metrics import average_precision_score
    V, T = d["val"], d["test"]
    tried, p_vas, fits = [], [], []
    for params in GRIDS[algo]:
        if algo == "proxy":
            f = f174.proxy_fit(params["config"], seed, V["Xtr"], V["ytr"])
            p_va, fit_s = f["score"](V["Xev"]), f["fit_s"]
        else:
            f, fit_s = f174.fit_classical(algo, params, seed, V["Xtr"],
                                          V["ytr"])
            p_va = f166.scores(f, V["Xev"].to_numpy(np.float64))
        tried.append({"params": params, "fit_s": fit_s,
                      "val_auprc": float(average_precision_score(V["yev"],
                                                                 p_va))})
        p_vas.append(p_va)
        fits.append(f)
    i = f166.choose(tried)
    f = fits[i]
    # The training fold is the same for both views, so the chosen fit is
    # scored on the test fold as fitted: no second fit.
    if algo == "proxy":
        p_te, p_tr = f["score"](T["Xev"]), f["p_tr"]
        extra = {k: f[k] for k in ("features", "n_learners")}
        extra["build"] = "serial"
    else:
        p_te = f166.scores(f, T["Xev"].to_numpy(np.float64))
        p_tr = f166.scores(f, T["Xtr"].to_numpy(np.float64))
        extra = {}
    row = {"algorithm": algo, "seed": seed, "tried": tried, "chosen": i,
           "chosen_params": tried[i]["params"], **extra,
           "test": f166.fold_metrics(T["yev"], V["yev"], p_vas[i], p_te,
                                     T["ytr"], p_tr, seed),
           "pocket": pocket_auprc(T["yev"], p_te, d["pocket"]),
           "outcome": orec.record(f"f157_{name}_{algo}", seed, T["yev"], p_te,
                                  y_val=V["yev"], p_val=p_vas[i])}
    return row, p_te


def rbf_alternative(seed: int, d: dict) -> dict:
    from sklearn.metrics import average_precision_score
    V = d["val"]
    rows = f166.stratified_rows(V["ytr"], f166.RBF_ROWS, seed)
    tried = []
    for params in f166.RBF_GRID:
        m, fit_s = f174.fit_classical("rbf", params, seed, V["Xtr"].iloc[rows],
                                      V["ytr"][rows])
        p_va = f166.scores(m, V["Xev"].to_numpy(np.float64))
        tried.append({"params": params, "fit_s": fit_s,
                      "val_auprc": float(average_precision_score(V["yev"],
                                                                 p_va))})
    return {"rows": int(len(rows)), "tried": tried,
            "best_val_auprc": max(t["val_auprc"] for t in tried)}


def rbf_lane(name: str, seed: int, d: dict, recorded: dict) -> dict:
    """The D14 amendment: the kept RBF form, the validation-chosen `C` of
    the recorded subsample fits, scored once on the test fold. Refuses a
    refit whose validation AUPRC differs from the recorded one."""
    import outcome_record as orec
    from sklearn.metrics import average_precision_score
    V, T = d["val"], d["test"]
    sub = f166.stratified_rows(V["ytr"], f166.RBF_ROWS, seed)
    if len(sub) != recorded["rows"]:
        raise RuntimeError(f"{name} s{seed}: subsample of {len(sub)} rows, "
                           f"recorded {recorded['rows']}")
    tried, p_vas, fits = [], [], []
    for params in f166.RBF_GRID:
        m, fit_s = f174.fit_classical("rbf", params, seed, V["Xtr"].iloc[sub],
                                      V["ytr"][sub])
        p_va = f166.scores(m, V["Xev"].to_numpy(np.float64))
        tried.append({"params": params, "fit_s": fit_s,
                      "val_auprc": float(average_precision_score(V["yev"],
                                                                 p_va))})
        p_vas.append(p_va)
        fits.append(m)
    got = [t["val_auprc"] for t in tried]
    want = [t["val_auprc"] for t in recorded["tried"]]
    if not np.allclose(got, want, rtol=0, atol=1e-12):
        raise RuntimeError(f"{name} s{seed}: the RBF refit gives validation "
                           f"AUPRC {got}, recorded {want}; nothing scored")
    i = f166.choose(tried)
    p_te = f166.scores(fits[i], T["Xev"].to_numpy(np.float64))
    # Training AUPRC on the subsample the form was fitted on (the amendment).
    p_tr = f166.scores(fits[i], T["Xtr"].iloc[sub].to_numpy(np.float64))
    return {"algorithm": "svm", "form": "rbf", "seed": seed, "tried": tried,
            "chosen": i, "chosen_params": tried[i]["params"],
            "subsample_rows": int(len(sub)),
            "test": f166.fold_metrics(T["yev"], V["yev"], p_vas[i], p_te,
                                      T["ytr"][sub], p_tr, seed),
            "pocket": pocket_auprc(T["yev"], p_te, d["pocket"]),
            "outcome": orec.record(f"f157_{name}_svm_rbf", seed, T["yev"], p_te,
                                   y_val=V["yev"], p_val=p_vas[i])}


def seed_run(name: str, seed: int) -> dict:
    t0 = time.perf_counter()
    d = data(name, seed)
    lanes = {}
    for algo in ALGOS:
        t1 = time.perf_counter()
        lanes[algo], _ = lane(name, algo, seed, d)
        lanes[algo]["lane_s"] = round(time.perf_counter() - t1, 1)
        print(f"  {name} s{seed} {algo:9s} test auprc "
              f"{lanes[algo]['test']['auprc']:.4f} {lanes[algo]['lane_s']} s",
              flush=True)
    rbf = rbf_alternative(seed, d)
    linear_best = max(t["val_auprc"] for t in lanes["svm"]["tried"])
    rbf["beats_linear_on_validation"] = bool(rbf["best_val_auprc"] > linear_best)
    return {"dataset": name, "seed": seed, "features": d["features"],
            "lanes": lanes, "svm_rbf_alternative": rbf,
            "minutes": round((time.perf_counter() - t0) / 60, 2)}


def choose_seeds(t42_min: float) -> dict:
    """F166's rule with 60 minutes in place of 120 (the entry)."""
    n = min(MAX_SEEDS, math.floor(CAP_MIN / t42_min)) if t42_min > 0 \
        else MAX_SEEDS
    n = max(MIN_SEEDS, n)
    return {"t42_minutes": t42_min, "n_seeds": n,
            "seeds": list(range(FIRST_SEED, FIRST_SEED + n)),
            "projected_minutes": round(n * t42_min, 1),
            "over_cap": n * t42_min > CAP_MIN,
            "below_section2_five_seeds": n < 5}


# ---------------------------------------------------------------- analysis
class FormNotScored(RuntimeError):
    """The rule keeps a form the SVM lane did not score (F166's `rbf_kept`;
    Sprint 31 D14: this module had recorded it and carried on)."""


def lane_form(rows: list[dict]) -> str:
    forms = {r["lanes"]["svm"].get("form", "linear") for r in rows}
    if len(forms) != 1:
        raise FormNotScored(f"the SVM lane mixes forms across seeds: {forms}")
    return forms.pop()


def analyze_dataset(rows: list[dict]) -> dict:
    """F166's analysis for one dataset. Refuses, before any figure, a
    dataset whose kept SVM form is not the form its lane scored."""
    kept = f166.analyze(rows, {})["svm_form"]["kept"]
    scored = lane_form(rows)
    if kept != scored:
        raise FormNotScored(
            f"{rows[0]['dataset']}: the rule keeps the {kept} SVM and the "
            f"lane scored the {scored} form; run the rbf mode (D14)")
    a = f166.analyze(rows, f166.load_scores(rows))
    a["svm_lane_is_kept_form"] = True
    a["svm_lane_form"] = scored
    def side_summary(alg, side):
        v = [r["lanes"][alg]["pocket"][side] for r in rows
             if r["lanes"][alg]["pocket"][side] is not None]
        return f166.t_summary(v) if v else None
    a["pocket"] = {alg: {side: side_summary(alg, side)
                         for side in ("in_pocket", "out_of_pocket")}
                   for alg in ALGOS}
    return a


def _doc(rows, plans, complete=False):
    return {"card": "F157", "part": "SPECTRA", "sprint": 31, "phase": 2,
            "evidence_tag": "SIM", "metered_seconds": 0,
            "datasets": list(DATASETS), "label": "target",
            "entry": "experiments/phase2/PREREGISTRATION_DRAFT.md section 6, "
                     "F157 SPECTRA part (2026-11-05)",
            "protocol": {"split": "spectra_segment.spectra_split 60/20/20, "
                                  "seeded",
                         "tune": "fit on training, choose on validation",
                         "test": "the chosen fit scored once on test",
                         "thresholds": "from the chosen fit's validation "
                                       "scores"},
            "grids": GRIDS, "svm_rbf_grid": f166.RBF_GRID,
            "rbf_rows": f166.RBF_ROWS, "seed_plans": plans,
            "seeds": sorted({r["seed"] for r in rows}), "rows": rows,
            "complete": complete}


def run() -> None:
    import provenance
    rid, resume = provenance.start(OUT)
    prior = json.loads(OUT.read_text(encoding="utf-8")) if resume else {}
    rows, plans = prior.get("rows", []), prior.get("seed_plans", {})

    def save():
        provenance.write_result(OUT, _doc(rows, plans), __file__,
                                sorted({r["seed"] for r in rows}), rid)

    def done(name):
        return {r["seed"] for r in rows if r["dataset"] == name}
    for name in DATASETS:
        if FIRST_SEED not in done(name):
            row = seed_run(name, FIRST_SEED)
            rows.append(row)
            plans[name] = choose_seeds(row["minutes"])
            save()
            print(f"{name} seed plan", json.dumps(plans[name]), flush=True)
        for seed in plans[name]["seeds"]:
            if seed in done(name):
                continue           # resume: never refit a seed
            rows.append(seed_run(name, seed))
            save()
    doc = _doc(rows, plans, complete=True)
    doc["analysis"] = {name: analyze_dataset([r for r in rows
                                              if r["dataset"] == name])
                       for name in DATASETS}
    provenance.write_result(OUT, doc, __file__,
                            sorted({r["seed"] for r in rows}), rid)
    print("complete", flush=True)


OUT_RBF = OUT.with_name("f157_spectra_algorithms_rbf.json")
AMENDMENT = ("experiments/phase2/PREREGISTRATION_DRAFT.md section 6, F157 "
             "SPECTRA part, amendment 2026-11-05 (Sprint 31 D14 option 1)")


def source_refusal(src: dict) -> str | None:
    """Why the recorded result cannot be the amendment's source, or None:
    it must be complete, and each dataset must hold exactly its seed plan's
    seeds (Sprint 31 i2 b; the PR 92 review found `run_rbf` checked
    neither)."""
    if src.get("complete") is not True:
        return f"{OUT.name} is not complete"
    for name in DATASETS:
        want = {FIRST_SEED} | set(src["seed_plans"][name]["seeds"])
        got = {r["seed"] for r in src["rows"] if r["dataset"] == name}
        if got != want:
            return (f"{OUT.name}: {name} holds seeds {sorted(got)}, its plan "
                    f"{sorted(want)}")
    return None


def run_rbf() -> None:
    """The D14 amendment: every row of the recorded result, with the kept
    RBF form scored into the SVM lane where the rule keeps it, written to
    `OUT_RBF`; the recorded result is read, never written. Resumable by
    (dataset, seed)."""
    import provenance
    src = json.loads(OUT.read_text(encoding="utf-8"))
    why = source_refusal(src)
    if why:
        raise SystemExit(f"REFUSING: {why}; the amendment rescores a "
                         "complete result only")
    rid, resume = provenance.start(OUT_RBF)
    rows = (json.loads(OUT_RBF.read_text(encoding="utf-8"))["rows"]
            if resume else [dict(r, lanes=dict(r["lanes"])) for r in src["rows"]])
    plans = src["seed_plans"]

    def doc(complete=False):
        d = _doc(rows, plans, complete)
        d["amendment"], d["source_result"] = AMENDMENT, OUT.name
        return d
    for name in DATASETS:
        rs = [r for r in rows if r["dataset"] == name]
        if f166.analyze(rs, {})["svm_form"]["kept"] != "rbf":
            continue
        for r in rs:
            if r["lanes"]["svm"].get("form") == "rbf":
                continue           # resume (rbf): never rescore a seed
            d = data(name, r["seed"])
            r["lanes"]["svm_linear"] = r["lanes"]["svm"]
            r["lanes"]["svm"] = rbf_lane(name, r["seed"], d,
                                         r["svm_rbf_alternative"])
            print(f"  {name} s{r['seed']} svm rbf test auprc "
                  f"{r['lanes']['svm']['test']['auprc']:.4f}", flush=True)
            provenance.write_result(OUT_RBF, doc(), __file__,
                                    sorted({x["seed"] for x in rows}), rid)
    final = doc(complete=True)
    final["analysis"] = {n: analyze_dataset([r for r in rows
                                             if r["dataset"] == n])
                         for n in DATASETS}
    provenance.write_result(OUT_RBF, final, __file__,
                            sorted({r["seed"] for r in rows}), rid)
    print("complete", flush=True)


def main(argv=None) -> int:
    mode = (argv or sys.argv[1:] or [""])[0]
    if mode == "run":
        run()
    elif mode == "rbf":
        run_rbf()
    elif mode == "analyze":
        doc = json.loads(OUT.read_text(encoding="utf-8"))
        print(json.dumps({n: analyze_dataset([r for r in doc["rows"]
                                              if r["dataset"] == n])
                          for n in DATASETS}, indent=1, default=str))
    else:
        raise SystemExit("mode required: run | rbf | analyze")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
