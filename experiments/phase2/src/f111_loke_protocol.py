"""F111: Experiment 4, the CVQBoost-KNN lane under the source protocol and ours.

Sprint 28 Task D (#51). Zero metered seconds. The entry is
`experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "Experiment 4",
committed before this module existed (`e07aa84`); every choice is fixed
there and repeated here.

  lane       all 30 ULB columns, MinMaxScaler fit on training rows, KNN
             weak learners (n_neighbors=15), schedule 2 full-pair (465
             learners, `full_pair_pool`), lambda 0, simplex QP; score w.H
  reference  HGB, l2_regularization=1.0 (F151), same rows and features
  protocol A the source's: no dedup, 70/30 stratified, the test fold split
             33/67 validation/evaluation, SMOTETomek on train (ratio 0.02)
  protocol B ours: dedup, 60/20/20 stratified, no resampling

Modes (one is required; there is no default):
  pilot    seed 42, 10% stratified sample of every fold, both protocols,
           KNN lane timed; writes the projection and whether to run.
           Refuses when a pilot is already recorded, so the recorded pilot
           and any approval on it are never overwritten.
  approve <reference>
           records the team lead's approval of a run over the cap, naming
           the decision it came from; only after a pilot, and only once
  run      seeds 42-51 under A and B, then the 0.05 sensitivity (A, 42-44);
           resumable, saved after every row; refuses unless the pilot said
           run or an over-cap approval is recorded. Each invocation's wall
           clock is recorded under `run_sessions`.
  analyze  the paired A - B difference and the rest of the entry's report;
           `complete` says whether every planned row is present

Run:  <venv python> experiments/phase2/src/f111_loke_protocol.py pilot|approve <reference>|run|analyze
"""
from __future__ import annotations

import json
import os
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

OUT = ROOT / "experiments" / "phase2" / "results" / "f111_loke_protocol.json"
SEEDS = tuple(range(42, 52))
SENS_SEEDS = (42, 43, 44)
RATIO, SENS_RATIO = 0.02, 0.05
VAL_EVAL_TEST_SIZE = 0.67
KNN_PARAMS = {"n_neighbors": 15}
SCHEDULE, LAMBDA = 2, 0.0
HGB_L2 = 1.0
PILOT_SEED, PILOT_FRACTION = 42, 0.10
CAP_MIN = 120.0
TARGET, TOLERANCE = 0.8108, 0.03
LEVEL = 0.95


# ------------------------------------------------------------------ protocols

def _xy(df):
    import data
    X = df.drop(columns=[data.LABEL_COL]).to_numpy(np.float64)
    return X, df[data.LABEL_COL].to_numpy().astype(int)


def smote_tomek(X, y01, ratio: float, seed: int):
    """The source code's train-only balancing (`0092a38`, main.py 427-457)."""
    from imblearn.combine import SMOTETomek
    from imblearn.over_sampling import SMOTE
    pos, neg = int(y01.sum()), int(len(y01) - y01.sum())
    target = max(pos / max(neg, 1), min(float(ratio), 0.5))
    if target <= pos / max(neg, 1) + 1e-6:
        return X, y01, {"applied": False}
    k = max(1, min(10, pos - 1))
    st = SMOTETomek(sampling_strategy=target, random_state=seed,
                    smote=SMOTE(sampling_strategy=target, k_neighbors=k,
                                random_state=seed))
    Xr, yr = st.fit_resample(X, y01)
    return Xr, yr, {"applied": True, "ratio": target, "k_neighbors": k,
                    "pos_before": pos, "neg_before": neg,
                    "pos_after": int(yr.sum()), "neg_after": int(len(yr) - yr.sum())}


def duplicates_in_train(X_tr, y_tr, X_q, y_q) -> int:
    """Scored rows with an exact copy (every column and the label) in train."""
    seen = {r.tobytes() for r in np.column_stack([X_tr, y_tr]).astype(np.float64)}
    return int(sum(r.tobytes() in seen
                   for r in np.column_stack([X_q, y_q]).astype(np.float64)))


def _sample(y01, frac, seed):
    from sklearn.model_selection import train_test_split
    if frac is None or frac >= 1.0:
        return np.arange(len(y01))
    idx, _ = train_test_split(np.arange(len(y01)), train_size=frac,
                              stratify=y01, random_state=seed)
    return np.sort(idx)


def protocol_a(seed: int, ratio: float = RATIO, frac: float | None = None) -> dict:
    import data
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import MinMaxScaler
    X, y = _xy(data.load_ulb().dropna())
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3,
                                          random_state=seed, stratify=y)
    Xva, Xev, yva, yev = train_test_split(Xte, yte, test_size=VAL_EVAL_TEST_SIZE,
                                          random_state=seed, stratify=yte)
    i_tr, i_va, i_ev = (_sample(ytr, frac, seed), _sample(yva, frac, seed),
                        _sample(yev, frac, seed))
    Xtr, ytr, Xva, yva, Xev, yev = (Xtr[i_tr], ytr[i_tr], Xva[i_va], yva[i_va],
                                    Xev[i_ev], yev[i_ev])
    dups = duplicates_in_train(Xtr, ytr, Xev, yev)
    sc = MinMaxScaler().fit(Xtr)
    Xtr_s, ytr_r, bal = smote_tomek(sc.transform(Xtr), ytr, ratio, seed)
    return {"protocol": "A", "ratio": ratio, "Xtr": Xtr_s, "ytr": ytr_r,
            "Xva": sc.transform(Xva), "yva": yva, "Xte": sc.transform(Xev),
            "yte": yev, "balance": bal, "eval_duplicates_in_train": dups}


def protocol_b(seed: int, frac: float | None = None) -> dict:
    import data
    from sklearn.preprocessing import MinMaxScaler
    s = data.stratified_split(data.load_ulb().drop_duplicates().reset_index(drop=True), seed)
    Xtr, ytr = s.X_train.to_numpy(np.float64), s.y_train.to_numpy().astype(int)
    Xva, yva = s.X_val.to_numpy(np.float64), s.y_val.to_numpy().astype(int)
    Xte, yte = s.X_test.to_numpy(np.float64), s.y_test.to_numpy().astype(int)
    i_tr, i_va, i_te = _sample(ytr, frac, seed), _sample(yva, frac, seed), _sample(yte, frac, seed)
    Xtr, ytr, Xva, yva, Xte, yte = (Xtr[i_tr], ytr[i_tr], Xva[i_va], yva[i_va],
                                    Xte[i_te], yte[i_te])
    sc = MinMaxScaler().fit(Xtr)
    return {"protocol": "B", "ratio": None, "Xtr": sc.transform(Xtr), "ytr": ytr,
            "Xva": sc.transform(Xva), "yva": yva, "Xte": sc.transform(Xte),
            "yte": yte, "balance": {"applied": False},
            "eval_duplicates_in_train": duplicates_in_train(Xtr, ytr, Xte, yte)}


# ---------------------------------------------------------------------- lanes

def score(w: np.ndarray, H: np.ndarray) -> np.ndarray:
    """w . H mapped to [0, 1]; on the simplex w . H is already in [-1, 1],
    so the map is monotone and AUC-PR equals that of `predict_raw`."""
    return np.clip((w @ H + 1.0) / 2.0, 0.0, 1.0)


def knn_lane(d: dict) -> dict:
    import full_pair_pool as fpp
    import qubo_proxy as qp
    y_pm1 = np.where(d["ytr"] == 1, 1, -1)
    t0 = time.perf_counter()
    clf = fpp.build_full(d["Xtr"], y_pm1, SCHEDULE, "knn", KNN_PARAMS,
                         lambda_coef=LAMBDA)
    t_build = time.perf_counter() - t0
    t0 = time.perf_counter()
    H_tr = qp.h_matrix(clf, d["Xtr"])
    t_htr = time.perf_counter() - t0
    w = qp.solve_simplex_qp(H_tr, y_pm1, LAMBDA)
    del H_tr
    t0 = time.perf_counter()
    p_va, p_te = (score(w, qp.h_matrix(clf, d["Xva"])),
                  score(w, qp.h_matrix(clf, d["Xte"])))
    t_q = time.perf_counter() - t0
    return {"p_va": p_va, "p_te": p_te, "n_learners": len(clf.h_list),
            "n_nonzero_weights": int((w > 1e-6).sum()),
            "seconds": {"build": round(t_build, 1), "h_train": round(t_htr, 1),
                        "h_scored": round(t_q, 1)}}


def hgb_lane(d: dict, seed: int) -> dict:
    from sklearn.ensemble import HistGradientBoostingClassifier
    t0 = time.perf_counter()
    m = HistGradientBoostingClassifier(l2_regularization=HGB_L2,
                                       random_state=seed).fit(d["Xtr"], d["ytr"])
    return {"p_va": m.predict_proba(d["Xva"])[:, 1],
            "p_te": m.predict_proba(d["Xte"])[:, 1],
            "seconds": {"fit": round(time.perf_counter() - t0, 1)}}


def _row(d: dict, lane: str, seed: int, out: dict) -> dict:
    from sklearn.metrics import average_precision_score, roc_auc_score
    tag = d["protocol"] + ("" if d["ratio"] is None else
                           f"_r{int(round(d['ratio'] * 100)):03d}")
    return {"protocol": d["protocol"], "ratio": d["ratio"], "lane": lane,
            "seed": seed, "n_train": int(len(d["ytr"])),
            "n_scored": int(len(d["yte"])), "n_positives_scored": int(d["yte"].sum()),
            "balance": d["balance"],
            "eval_duplicates_in_train": d["eval_duplicates_in_train"],
            "test_auprc": float(average_precision_score(d["yte"], out["p_te"])),
            "test_roc_auc": float(roc_auc_score(d["yte"], out["p_te"])),
            **{k: v for k, v in out.items() if k not in ("p_va", "p_te")},
            "outcome": orec.record(f"f111_{tag}_{lane}", seed, d["yte"], out["p_te"],
                                   y_val=d["yva"], p_val=out["p_va"])}


# --------------------------------------------------------------- bookkeeping

def _load() -> dict:
    if OUT.exists():
        return json.loads(OUT.read_text(encoding="utf-8"))
    return {"generator": "experiments/phase2/src/f111_loke_protocol.py",
            "card": "F111", "sprint": 28, "phase": 2, "evidence_tag": "SIM",
            "metered_seconds": 0, "cpu_count": os.cpu_count(),
            "entry": "experiments/phase2/PREREGISTRATION_DRAFT.md section 6, Experiment 4",
            "lane": {"features": "all 30 ULB columns", "scaler": "MinMaxScaler, train",
                     "weak": "knn", "weak_params": KNN_PARAMS, "schedule": SCHEDULE,
                     "pair_build": "full (full_pair_pool)", "lambda": LAMBDA},
            "reference": {"hgb_l2_regularization": HGB_L2},
            "rows": []}


def _save(doc: dict) -> None:
    tmp = OUT.with_suffix(".tmp.json")
    tmp.write_text(json.dumps(doc, indent=1, default=strict_json.numpy_scalar), encoding="utf-8")
    tmp.replace(OUT)


def _key(r: dict) -> tuple:
    return (r["protocol"], r["ratio"], r["lane"], r["seed"])


def projection_min(pilot: dict) -> float:
    """F130's formula on the lane, per protocol, plus the full-size data
    preparation (SMOTETomek's neighbor search is not free), summed over
    the run's seed counts."""
    total = 0.0
    for p in ("A", "B"):
        r = pilot[p]
        scale = (r["full_train"] / r["pilot_train"]) * (r["full_query"] / r["pilot_query"])
        n = len(SEEDS) + (len(SENS_SEEDS) if p == "A" else 0)
        total += (r["seconds"] * scale + r["prep_seconds_full"]) * n / 60.0
    return total


def pilot() -> dict:
    # Before any work: a second pilot would replace the recorded one and the
    # approval recorded on it. No override flag (CLAUDE.md: a guard does not
    # ship with its escape hatch).
    if _load().get("pilot"):
        raise SystemExit("a pilot is already recorded; it is not re-run")
    out = {}
    for p, fn in (("A", protocol_a), ("B", protocol_b)):
        t0 = time.perf_counter()
        full = fn(PILOT_SEED)
        prep = time.perf_counter() - t0
        small = fn(PILOT_SEED, frac=PILOT_FRACTION)
        t0 = time.perf_counter()
        r = knn_lane(small)
        out[p] = {"seconds": round(time.perf_counter() - t0, 1), "lane": r["seconds"],
                  "prep_seconds_full": round(prep, 1), "balance_full": full["balance"],
                  "eval_duplicates_in_train_full": full["eval_duplicates_in_train"],
                  "pilot_train": len(small["ytr"]),
                  "pilot_query": len(small["ytr"]) + len(small["yva"]) + len(small["yte"]),
                  "full_train": len(full["ytr"]),
                  "full_query": len(full["ytr"]) + len(full["yva"]) + len(full["yte"])}
        print(f"  pilot {p}: {out[p]}", flush=True)
    proj = projection_min(out)
    doc = _load()
    doc["pilot"] = {"seed": PILOT_SEED, "fraction": PILOT_FRACTION, **out,
                    "projected_minutes": round(proj, 1), "cap_minutes": CAP_MIN,
                    "run": proj <= CAP_MIN}
    _save(doc)
    return doc["pilot"]


def approve(reference: str) -> dict:
    """Record the team lead's approval of a run over the cap, with the
    decision it came from. Only after a pilot, and only once."""
    if not reference.strip():
        raise SystemExit("an approval names the decision it came from")
    doc = _load()
    pilot_ = doc.get("pilot")
    if not pilot_:
        raise SystemExit("no pilot recorded; nothing to approve")
    if "over_cap_approval" in pilot_:
        raise SystemExit("an approval is already recorded")
    pilot_["over_cap_approval"] = {"reference": reference,
                                   "date": time.strftime("%Y-%m-%d"),
                                   "projected_minutes": pilot_["projected_minutes"]}
    _save(doc)
    return pilot_["over_cap_approval"]


def run() -> None:
    doc = _load()
    pilot_ = doc.get("pilot", {})
    if not (pilot_.get("run") or pilot_.get("over_cap_approval")):
        raise SystemExit("the pilot did not project the run within the cap; "
                         "the seed count goes to Manual Validation")
    t_start, started = time.perf_counter(), time.strftime("%Y-%m-%dT%H:%M:%S")
    done = {_key(r) for r in doc["rows"]}
    n_before = len(doc["rows"])
    for seed, p, ratio in _plan():
        if all((p, ratio, lane, seed) in done for lane in ("knn", "hgb")):
            continue
        d = protocol_a(seed, ratio) if p == "A" else protocol_b(seed)
        for lane in ("knn", "hgb"):
            if (p, ratio, lane, seed) in done:
                continue
            out = knn_lane(d) if lane == "knn" else hgb_lane(d, seed)
            doc["rows"].append(_row(d, lane, seed, out))
            _save(doc)
            r = doc["rows"][-1]
            print(f"  {p} r={ratio} {lane} s{seed}: auprc {r['test_auprc']:.4f} "
                  f"dups {r['eval_duplicates_in_train']} {r.get('seconds')}", flush=True)
    # Additive: this invocation's wall clock, start to last write.
    doc.setdefault("run_sessions", []).append(
        {"started": started, "run_wall_s": round(time.perf_counter() - t_start, 1),
         "rows_added": len(doc["rows"]) - n_before})
    _save(doc)


def _plan() -> list[tuple]:
    """(seed, protocol, ratio) in run order: the main seeds, then the
    sensitivity seeds."""
    plan = [x for seed in SEEDS for x in ((seed, "A", RATIO), (seed, "B", None))]
    return plan + [(seed, "A", SENS_RATIO) for seed in SENS_SEEDS]


def planned_keys() -> set:
    return {(p, ratio, lane, seed) for seed, p, ratio in _plan()
            for lane in ("knn", "hgb")}


# ------------------------------------------------------------------ analysis

def paired(a: list[float], b: list[float], level: float = LEVEL) -> dict:
    from scipy import stats
    d = np.asarray(a, float) - np.asarray(b, float)
    n = len(d)
    half = float(stats.t.ppf(1 - (1 - level) / 2, n - 1) * d.std(ddof=1) / np.sqrt(n))
    return {"mean": float(d.mean()), "low": float(d.mean() - half),
            "high": float(d.mean() + half), "level": level, "n": n,
            "excludes_zero": bool(d.mean() - half > 0 or d.mean() + half < 0)}


def analyze(doc: dict) -> dict:
    def by(p, ratio, lane):
        return {r["seed"]: r["test_auprc"] for r in doc["rows"]
                if (r["protocol"], r["ratio"], r["lane"]) == (p, ratio, lane)}
    out = {}
    for lane in ("knn", "hgb"):
        a, b = by("A", RATIO, lane), by("B", None, lane)
        seeds = sorted(set(a) & set(b))
        if len(seeds) >= 2:
            out[f"{lane}_A_minus_B"] = paired([a[s] for s in seeds], [b[s] for s in seeds])
            out[f"{lane}_A_mean"] = float(np.mean([a[s] for s in seeds]))
            out[f"{lane}_B_mean"] = float(np.mean([b[s] for s in seeds]))
    for p, ratio in (("A", RATIO), ("B", None)):
        k, h = by(p, ratio, "knn"), by(p, ratio, "hgb")
        seeds = sorted(set(k) & set(h))
        if len(seeds) >= 2:
            out[f"knn_minus_hgb_{p}"] = paired([k[s] for s in seeds], [h[s] for s in seeds])
    if "knn_A_mean" in out:
        out["consistent_with_0_8108"] = bool(abs(out["knn_A_mean"] - TARGET) <= TOLERANCE)
    sens = {lane: by("A", SENS_RATIO, lane) for lane in ("knn", "hgb")}
    out["sensitivity_r005"] = {
        lane: {"mean": float(np.mean(list(v.values()))) if v else None,
               "n": len(v), "seeds": sorted(v)}
        for lane, v in sens.items()}
    present = {_key(r) for r in doc["rows"]}
    missing = planned_keys() - present
    out["complete"] = not missing
    out["n_missing_rows"] = len(missing)
    out["eval_duplicates_in_train_A"] = sorted(
        {r["seed"]: r["eval_duplicates_in_train"] for r in doc["rows"]
         if r["protocol"] == "A" and r["ratio"] == RATIO}.items())
    return out


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        raise SystemExit("usage: f111_loke_protocol.py "
                         "pilot|approve <reference>|run|analyze (no default)")
    mode = argv[0]
    if mode == "pilot":
        print(json.dumps(pilot(), indent=1))
    elif mode == "approve":
        print(json.dumps(approve(" ".join(argv[1:]))))
    elif mode == "run":
        run()
    elif mode == "analyze":
        doc = _load()
        doc["analysis"] = analyze(doc)
        _save(doc)
        print(json.dumps(doc["analysis"], indent=1))
    else:
        raise SystemExit(f"unknown mode {mode!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
