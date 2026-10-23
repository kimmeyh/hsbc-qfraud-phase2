"""F130 (Sprint 27 Task E): proxy screens of F124's ranks 3, 5 and 6.

Phase 2 code. It imports Phase 1 modules (`qubo_proxy`, `spectra_segment`)
and edits none; `qubo_proxy.build_pool` gained one opt-in argument,
`pair_count`, whose default keeps Phase 1's build. Results go to
`experiments/phase2/results/f130_levers.json`. Zero metered seconds.

Every SPECTRA cell is the frozen B4 configuration (sequential pairs, hard
votes, exact simplex QP), on the five seeds of `soft_votes.SEEDS`, with two
references on the same split: HGB, and the baseline `dct` pool. dct pools
are seeded (`qubo_proxy.seeded_weak_params`) so a rerun rebuilds them; a KNN
pool is not, because `KNeighborsClassifier` takes no `random_state` and is
deterministic without one (`weak_params`).

    rank 3  knn       KNN weak learners, oilgas and telecom (F124's confirm
                      already ran energy_steel)
    rank 5  phase     each `*_phase` column replaced by its cos and sin, the
                      10-column block whitened on the training rows only
    rank 6  pairs_N   `weak_cls_pair_count` N: 30, 60, 90 and 119 on
                      energy_steel and telecom (17 features, cap 119), 30,
                      60 and 90 on oilgas (15 features, cap 90). The cap is
                      eqc-models' `topNPairs` assert, d(d-3)/2. The count
                      limits PAIRS only; schedule 3's triples are unchanged
    ulb     ulb_pilot KNN on ULB's B1 configuration (`free`), one seed, a
                      10% stratified sample of train and test, timed. The
                      KNN build's cost is train rows x query rows, so the
                      full run is projected at 100 times the pilot

Decision rule (Sprint 27 plan, set before any run): a lever "moves AUPRC"
only with a mean change of at least 0.005 against the baseline AND a
paired 95% bootstrap CI over the seed deltas that excludes zero; it "beats
HGB" only with a CI against HGB that lies above zero. A lever that does
neither is recorded as rejected. The rank 5 `in_pocket` caveat is written
on its rows: `in_pocket` is predictable from the phase features at AUC
0.93-0.99 (`docs/F101_IN_POCKET_PROVENANCE.md`).

Run:  <venv python> experiments/phase2/src/f130_levers.py [knn|phase|pairs|ulb|all]
      <venv python> experiments/phase2/src/f130_levers.py ulb_full
            (only after the pilot projected it within budget)
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import soft_votes as sv                              # noqa: E402  (Phase 2)
import qubo_proxy as qp                              # noqa: E402  (Phase 1, read-only)
import spectra_segment as ss                         # noqa: E402  (Phase 1, read-only)

OUT = sv.OUT_DIR / "f130_levers.json"
DATASETS = ("energy_steel", "oilgas_gasturbine", "telecom_churn")
KNN_DATASETS = ("oilgas_gasturbine", "telecom_churn")
PAIR_COUNTS = {"energy_steel": (30, 60, 90, 119),
               "oilgas_gasturbine": (30, 60, 90),
               "telecom_churn": (30, 60, 90, 119)}
MOVE_MIN = 0.005
ULB_FRACTION = 0.10
ULB_FULL_BUDGET_MIN = 60.0
IN_POCKET_CAVEAT = ("in_pocket is predictable from the phase features at "
                    "AUC 0.93-0.99 (docs/F101_IN_POCKET_PROVENANCE.md); a "
                    "rank 5 gain may be a gain on the segment flag")


def weak_params(weak_type: str, seed: int, params: dict | None = None) -> dict:
    """Seeded params for a tree learner; KNN skips the seed, because
    `KNeighborsClassifier(random_state=...)` raises TypeError."""
    if weak_type == "knn":
        return dict(params or {})
    return qp.seeded_weak_params(seed, params)


def pair_cap(n_features: int) -> int:
    """eqc-models' `topNPairs` limit, d(d-3)/2."""
    return n_features * (n_features - 3) // 2


def phase_block(Xtr, Xte, cols):
    """Rank 5: each `*_phase` column (radians) replaced by cos and sin, and
    the cos/sin block whitened (ZCA) with the TRAINING rows' mean and
    covariance only. Returns (Xtr, Xte, new column names)."""
    ph = [i for i, c in enumerate(cols) if c.endswith("_phase")]
    keep = [i for i in range(len(cols)) if i not in ph]

    def enc(X):
        a = X[:, ph].astype(np.float64)
        return np.hstack([np.cos(a), np.sin(a)])
    Btr, Bte = enc(Xtr), enc(Xte)
    mu = Btr.mean(axis=0)
    cov = np.cov(Btr - mu, rowvar=False)
    vals, vecs = np.linalg.eigh(cov)
    W = vecs @ np.diag(1.0 / np.sqrt(np.maximum(vals, 1e-12))) @ vecs.T
    out_tr = np.hstack([Xtr[:, keep], (Btr - mu) @ W]).astype(np.float32)
    out_te = np.hstack([Xte[:, keep], (Bte - mu) @ W]).astype(np.float32)
    names = ([cols[i] for i in keep] + [f"cos_{cols[i]}" for i in ph]
             + [f"sin_{cols[i]}" for i in ph])
    return out_tr, out_te, names


def _cell(Xtr, Xte, ytr01, yte, pocket, cfg, weak_type, seed,
          pair_count=None):
    """One pool built, solved and scored. Never raises: an error is a row
    field, because a lever that cannot be built is a finding."""
    y_pm1 = np.where(ytr01 == 1, 1, -1)
    lam = cfg["lambda_coef_alpha"] * len(y_pm1)
    t0 = time.perf_counter()
    row: dict = {}
    try:
        clf = qp.build_pool(Xtr, y_pm1, cfg["weak_cls_schedule"],
                            weak_type=weak_type, pair_build="sequential",
                            # The frozen tree params (empty for B4) apply to
                            # dct only; a KNN learner takes none of them.
                            weak_params=weak_params(
                                weak_type, seed,
                                cfg.get("weak_cls_params")
                                if weak_type == "dct" else None),
                            lambda_coef=lam, pair_count=pair_count)
        H_tr, H_te = qp.h_matrix(clf, Xtr), qp.h_matrix(clf, Xte)
        w = qp.solve_simplex_qp(H_tr, y_pm1, lam)
        p_te, p_tr = sv._score(w, H_te), sv._score(w, H_tr)
        row.update(test_auprc=sv._ap(yte, p_te),
                   train_auprc=sv._ap(ytr01, p_tr),
                   in_pocket_auprc=(sv._in_pocket_ap(yte, p_te, pocket)
                                    if pocket is not None else None),
                   n_learners=int(H_tr.shape[0]),
                   n_nonzero_weights=int((w > 1e-6).sum()))
    except Exception as e:                              # noqa: BLE001
        row["error"] = f"{type(e).__name__}: {str(e)[:300]}"
    row["elapsed_s"] = round(time.perf_counter() - t0, 1)
    return row


def _variants(part: str, name: str) -> list[tuple[str, dict]]:
    """(variant, how) for one dataset. `how` keys: weak_type, pair_count,
    phase."""
    if part == "knn":
        return [("knn", {"weak_type": "knn"})] if name in KNN_DATASETS else []
    if part == "phase":
        return [("phase", {"weak_type": "dct", "phase": True})]
    if part == "pairs":
        return [(f"pairs_{n}", {"weak_type": "dct", "pair_count": n})
                for n in PAIR_COUNTS[name]]
    raise ValueError(part)


def run_spectra(parts: list[str], save) -> list[dict]:
    """Every SPECTRA row for `parts`, with HGB and the seeded dct baseline
    on the same split. `save(rows)` is called after each row (heartbeat)."""
    from sklearn.ensemble import HistGradientBoostingClassifier
    rows: list[dict] = []
    for name in DATASETS:
        todo = [v for p in parts for v in _variants(p, name)]
        if not todo:
            continue
        cell = ss.frozen_cell_by_name(name)
        cfg = cell["config"]
        for seed in sv.SEEDS:
            c, Xtr, Xte, ytr01, yte, pocket = sv._prep(name, seed)
            _, cols = ss._prep_spectra(name, seed)
            hgb = HistGradientBoostingClassifier(random_state=seed).fit(
                Xtr, ytr01)
            hgb_ap = sv._ap(yte, hgb.predict_proba(Xte)[:, 1])
            base = {"dataset": f"spectra_{name}", "seed": seed,
                    "hgb_test_auprc": hgb_ap, "n_features": len(cols)}
            b = _cell(Xtr, Xte, ytr01, yte, pocket, cfg, "dct", seed)
            rows.append({**base, "variant": "baseline_dct", **b})
            _log(rows[-1])
            save(rows)
            for vname, how in todo:
                if how.get("phase"):
                    Ptr, Pte, pcols = phase_block(Xtr, Xte, list(cols))
                    r = _cell(Ptr, Pte, ytr01, yte, pocket, cfg, "dct", seed)
                    h2 = HistGradientBoostingClassifier(
                        random_state=seed).fit(Ptr, ytr01)
                    r.update(n_features=len(pcols),
                             hgb_on_phase_features_test_auprc=sv._ap(
                                 yte, h2.predict_proba(Pte)[:, 1]),
                             caveat=IN_POCKET_CAVEAT)
                else:
                    r = _cell(Xtr, Xte, ytr01, yte, pocket, cfg,
                              how["weak_type"], seed, how.get("pair_count"))
                    if how.get("pair_count"):
                        r.update(pair_count=how["pair_count"],
                                 pair_cap=pair_cap(len(cols)))
                rows.append({**base, "variant": vname, **r})
                _log(rows[-1])
                save(rows)
    return rows


def _log(r):
    print(f"  {r['dataset']:26s} s{r['seed']} {r['variant']:13s} "
          f"{r.get('test_auprc', float('nan')):.4f} "
          f"hgb {r['hgb_test_auprc']:.4f} {r['elapsed_s']:.0f}s "
          f"{r.get('error', '')}", flush=True)


def verdict(d_base: list[float], d_hgb: list[float]) -> dict:
    """The plan's rule on one lever's paired seed deltas."""
    ci_b = sv._bootstrap_ci(d_base)
    ci_h = sv._bootstrap_ci(d_hgb)
    mean_b = float(np.mean(d_base))
    moves = abs(mean_b) >= MOVE_MIN and (ci_b[0] > 0 or ci_b[1] < 0)
    beats = ci_h[0] > 0
    return {"mean_delta_vs_baseline": round(mean_b, 4),
            "delta_vs_baseline_ci95": ci_b,
            "mean_delta_vs_hgb": round(float(np.mean(d_hgb)), 4),
            "delta_vs_hgb_ci95": ci_h,
            "moves_auprc": bool(moves),
            "direction": ("up" if mean_b > 0 else "down") if moves else None,
            "beats_hgb": bool(beats),
            "rejected": not (moves or beats)}


def summarize(rows: list[dict]) -> dict:
    """Per dataset and variant. A variant is judged only when it and the
    baseline completed on every seed; otherwise it is reported unjudged."""
    out: dict = {}
    full = len(sv.SEEDS)
    for ds in sorted({r["dataset"] for r in rows}):
        base = {r["seed"]: r for r in rows if r["dataset"] == ds
                and r["variant"] == "baseline_dct" and "test_auprc" in r}
        out[ds] = {"baseline_dct_mean_test_auprc": (round(float(np.mean(
            [r["test_auprc"] for r in base.values()])), 4) if base else None),
            "hgb_mean_test_auprc": round(float(np.mean(
                [r["hgb_test_auprc"] for r in rows if r["dataset"] == ds
                 and r["variant"] == "baseline_dct"])), 4)}
        for v in sorted({r["variant"] for r in rows if r["dataset"] == ds}
                        - {"baseline_dct"}):
            sub = [r for r in rows if r["dataset"] == ds
                   and r["variant"] == v]
            ok = [r for r in sub if "test_auprc" in r and r["seed"] in base]
            entry = {"n_seeds": len(ok),
                     "errors": sorted({r["error"] for r in sub
                                       if "error" in r})}
            if ok:
                entry.update(
                    mean_test_auprc=round(float(np.mean(
                        [r["test_auprc"] for r in ok])), 4),
                    mean_train_test_gap=round(float(np.mean(
                        [r["train_auprc"] - r["test_auprc"] for r in ok])), 4),
                    mean_n_learners=round(float(np.mean(
                        [r["n_learners"] for r in ok])), 1))
            if len(ok) == full and len(base) == full:
                entry.update(verdict(
                    [r["test_auprc"] - base[r["seed"]]["test_auprc"]
                     for r in ok],
                    [r["test_auprc"] - r["hgb_test_auprc"] for r in ok]))
            else:
                entry["verdict"] = "not judged: not every seed completed"
            if v == "phase":
                entry["caveat"] = IN_POCKET_CAVEAT
            out[ds][v] = entry
    return out


def run_ulb_pilot(seed: int = 42) -> dict:
    """KNN on ULB's B1 configuration, timed on a 10% stratified sample, with
    the seeded dct pool on the same sample as its reference."""
    from sklearn.model_selection import train_test_split
    c = qp.CONFIGS["free"]
    split, cols, Xtr, _, Xte, y_pm1 = qp._prep(seed, c["k"])
    ytr01, yte = split.y_train.to_numpy(), split.y_test.to_numpy()
    tr, _ = train_test_split(np.arange(len(ytr01)), train_size=ULB_FRACTION,
                             stratify=ytr01, random_state=seed)
    te, _ = train_test_split(np.arange(len(yte)), train_size=ULB_FRACTION,
                             stratify=yte, random_state=seed)
    cfg = {"lambda_coef_alpha": qp.LAMBDA_MULT,
           "weak_cls_schedule": c["schedule"]}
    out = {"seed": seed, "config": "free", "k": c["k"],
           "schedule": c["schedule"], "fraction": ULB_FRACTION,
           "n_train": int(len(tr)), "n_test": int(len(te)),
           "n_train_full": int(len(ytr01)), "n_test_full": int(len(yte))}
    for wt in ("dct", "knn"):
        r = _cell(Xtr[tr], Xte[te], ytr01[tr], yte[te], None, cfg, wt, seed)
        out[wt] = r
        print(f"  ulb pilot {wt}: {r}", flush=True)
    t = out["knn"]["elapsed_s"]
    scale = (out["n_train_full"] / out["n_train"]) * (
        (out["n_train_full"] + out["n_test_full"])
        / (out["n_train"] + out["n_test"]))
    out["knn_projected_full_seed_min"] = round(t * scale / 60.0, 1)
    out["knn_projected_5_seeds_min"] = round(5 * t * scale / 60.0, 1)
    out["projection"] = ("pilot seconds x (full train / pilot train) x "
                         "(full query / pilot query); query = train + test "
                         "rows, since the H matrix is evaluated on both")
    out["full_run"] = ("run" if out["knn_projected_5_seeds_min"]
                       <= ULB_FULL_BUDGET_MIN else
                       f"not run: projected above {ULB_FULL_BUDGET_MIN:.0f} "
                       "minutes; the pilot's timing is the result")
    out["note"] = ("a 10% sample is not the record's setup (SMOTE, 70/30, "
                   "10 seeds); its AUPRC is not a test of the 0.8108 claim")
    return out


def run_ulb_full() -> dict:
    """Rank 3 on ULB, run only when the pilot projects it within budget:
    KNN and the seeded dct pool on the B1 configuration (`free`, k=13,
    schedule 2, sequential pairs: 78 learners), the full split, 5 seeds,
    with HGB on the same features and split. Not the EvidenceBasedDB
    record's setup (SMOTE, 70/30, 10 seeds), so not a replication."""
    from sklearn.ensemble import HistGradientBoostingClassifier
    c = qp.CONFIGS["free"]
    cfg = {"lambda_coef_alpha": qp.LAMBDA_MULT,
           "weak_cls_schedule": c["schedule"]}
    rows = []
    for seed in sv.SEEDS:
        split, cols, Xtr, _, Xte, _ = qp._prep(seed, c["k"])
        ytr01, yte = split.y_train.to_numpy(), split.y_test.to_numpy()
        hgb = HistGradientBoostingClassifier(random_state=seed).fit(Xtr, ytr01)
        hgb_ap = sv._ap(yte, hgb.predict_proba(Xte)[:, 1])
        for wt in ("dct", "knn"):
            r = _cell(Xtr, Xte, ytr01, yte, None, cfg, wt, seed)
            rows.append({"dataset": "ulb", "seed": seed,
                         "variant": "baseline_dct" if wt == "dct" else "knn",
                         "hgb_test_auprc": hgb_ap, "n_features": len(cols),
                         **r})
            _log(rows[-1])
    return {"config": "free", "k": c["k"], "schedule": c["schedule"],
            "pair_build": "sequential", "rows": rows,
            "summary": summarize(rows)}


HGB_CHECK_OUT = OUT.with_name("f130_ulb_hgb_check.json")
HGB_CHECK_VARIANTS = {
    "default": {},
    "no_early_stopping": {"early_stopping": False},
    "lr005_iter300": {"learning_rate": 0.05, "max_iter": 300},
    "lr005_iter300_no_early_stopping": {"learning_rate": 0.05, "max_iter": 300,
                                        "early_stopping": False},
}


def run_ulb_hgb_check(scores: dict | None = None) -> dict:
    """Why `ulb_full`'s "beats HGB" is not a finding: the HGB comparator,
    refit on the same features and split under the variants above, with the
    iterations it ran. Added after the run (Sprint 27), so a check of the
    comparator, not a lever screen; it changes no recorded row.

    `scores`, opt-in (Sprint 28 DV4 outcome backfill): a dict that receives
    (test labels, per-row test scores) under (seed, variant). The rows
    returned are the same with or without it."""
    from sklearn.ensemble import HistGradientBoostingClassifier
    c = qp.CONFIGS["free"]
    rows = []
    for seed in sv.SEEDS:
        split, cols, Xtr, _, Xte, _ = qp._prep(seed, c["k"])
        ytr01, yte = split.y_train.to_numpy(), split.y_test.to_numpy()
        for name, kw in HGB_CHECK_VARIANTS.items():
            t0 = time.time()
            m = HistGradientBoostingClassifier(random_state=seed, **kw).fit(
                Xtr, ytr01)
            p_te = m.predict_proba(Xte)[:, 1]
            if scores is not None:
                scores[(seed, name)] = (yte, p_te)
            rows.append({"seed": seed, "variant": name, "params": kw,
                         "n_iter": int(m.n_iter_),
                         "test_auprc": float(sv._ap(yte, p_te)),
                         "test_positive_rate": float(np.mean(yte)),
                         "elapsed_s": round(time.time() - t0, 1)})
            print(f"  s{seed} {name:34s} iter {rows[-1]['n_iter']:4d} "
                  f"auprc {rows[-1]['test_auprc']:.4f}", flush=True)
    means = {n: round(float(np.mean([r["test_auprc"] for r in rows
                                     if r["variant"] == n])), 4)
             for n in HGB_CHECK_VARIANTS}
    return {**_header(), "mode": "ulb_hgb_check",
            "for": "experiments/phase2/results/f130_levers.json ulb_full",
            "config": "free", "k": c["k"], "rows": rows,
            "mean_test_auprc": means}


def _header() -> dict:
    import hashlib
    return {"generator": "experiments/phase2/src/f130_levers.py",
            "card": "F130", "sprint": 27, "phase": 2, "evidence_tag": "SIM",
            "metered_seconds": 0, "eqc_models_version": sv._eqc_version(),
            "seeds": list(sv.SEEDS), "date": time.strftime("%Y-%m-%d"),
            "decision_rule": {"moves_auprc_min_mean": MOVE_MIN,
                              "ci": "paired percentile bootstrap over the "
                                    "seed deltas, 95%",
                              "beats_hgb": "CI against HGB above zero"},
            "pair_counts": {k: list(v) for k, v in PAIR_COUNTS.items()},
            "generator_sha256": hashlib.sha256(
                Path(__file__).read_bytes()).hexdigest()}


def _load() -> dict:
    if OUT.exists():
        return json.loads(OUT.read_text(encoding="utf-8"))
    return {}


def _write(doc: dict) -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    tmp = OUT.with_suffix(".tmp")
    tmp.write_text(json.dumps(doc, indent=1), encoding="utf-8")
    tmp.replace(OUT)


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    part = argv[0] if argv else "all"
    parts = {"all": ["knn", "phase", "pairs"], "knn": ["knn"],
             "phase": ["phase"], "pairs": ["pairs"], "ulb": [],
             "ulb_full": [], "ulb_hgb_check": []}[part]
    if part == "ulb_hgb_check":
        res = run_ulb_hgb_check()
        HGB_CHECK_OUT.write_text(json.dumps(res, indent=1), encoding="utf-8")
        print(json.dumps(res["mean_test_auprc"], indent=1))
        return 0
    doc = {**_load(), **_header()}
    if part in ("all", "ulb"):
        doc["ulb_pilot"] = run_ulb_pilot()
        _write(doc)
    if part == "ulb_full":
        pilot = doc.get("ulb_pilot") or {}
        if pilot.get("full_run") != "run":
            raise SystemExit("REFUSING: the ULB pilot did not project the "
                             "full run within budget (or has not run)")
        doc["ulb_full"] = run_ulb_full()
        _write(doc)
        print(json.dumps(doc["ulb_full"]["summary"], indent=1))
    if parts:
        # A baseline is rebuilt only for datasets this part touches, so only
        # those datasets' baselines are dropped (a partial rerun otherwise
        # deletes baselines it does not rebuild; Sprint 27 code review).
        touched = {f"spectra_{n}" for n in DATASETS
                   if any(_variants(p, n) for p in parts)}
        kept = [r for r in doc.get("rows", [])
                if not (r["variant"] == "baseline_dct"
                        and r["dataset"] in touched)
                and not any(r["variant"] == v
                            for p in parts
                            for v, _ in _variants(p, r["dataset"]
                                                  .replace("spectra_", "")))]

        def save(new):
            doc["rows"] = kept + new
            doc["status"] = "running"
            _write(doc)
        new = run_spectra(parts, save)
        doc["rows"] = kept + new
        doc["summary"] = summarize(doc["rows"])
        doc["status"] = "complete"
        _write(doc)
        print(json.dumps(doc["summary"], indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
