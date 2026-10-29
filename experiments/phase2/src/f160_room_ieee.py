"""F160 (Sprint 29 Task E, #68): Experiment 3's room check on IEEE-CIS.

The entry is the 2026-10-26 amendment to "Experiment 3" in
`experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, committed before
this module existed (52454e2). F153's sweep, ridge rule, floor, falsifier
and resolution checks are imported from `f153_exp3_design`, unchanged;
F94's objective and controls from `exp3_controls`.

Order: the positive control (random-sign learners on each instance's own
labels) first. The control uses the IEEE-CIS fold's evaluation labels, so
the fold is loaded first; the IEEE-CIS pools are built and read only if
the control shows room on some instance (`gate`).

    <venv python> experiments/phase2/src/f160_room_ieee.py

Zero metered seconds. Writes `experiments/phase2/results/f160_room_ieee.json`
through `provenance.write_result`: once after the control, and again,
with `complete` true, at the end. Not resumable; a rerun over the recorded
result is refused before any work (`provenance.start`).
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "experiments" / "src"))
import exp3_controls as ec  # noqa: E402  (Phase 2, F94; not edited)
import f153_exp3_design as fd  # noqa: E402  (Phase 2, F153; not edited)

OUT = ROOT / "experiments" / "phase2" / "results" / "f160_room_ieee.json"
SEEDS = (42, 43, 44)
CONFIG_K = {"free": 13, "mid": 17}
MI_ROWS = 50_000


def room(H: np.ndarray, y: np.ndarray, m: int) -> dict:
    """F153's sweep on one instance: greedy at every swept weight."""
    sweep = []
    for lm in fd.SWEEP:
        J, C = ec.problem(H, y, lm)
        g = ec.greedy(J, C, m)
        w = fd._w(g, len(C), J, C)
        obj = g["objective"]
        sweep.append({"lam_mult": lm, "objective": obj,
                      "floor": fd.floor(lm, m),
                      "gap_to_floor": obj - fd.floor(lm, m),
                      "data_share": fd.data_term(J, C, w, lm) / abs(obj)
                      if obj else float("nan")})
    return {"sweep": sweep, "m": m, "n_learners": int(H.shape[0]),
            "fraud_rate": float(np.mean(y == 1))}


def chosen(m: int, H, y, lam_mult: float, scip: bool) -> dict:
    """Greedy, SCIP (if asked) and both resolution checks at one weight."""
    import device_resolution as dr
    J, C = ec.problem(H, y, lam_mult)
    g = ec.greedy(J, C, m)
    row = {"lam_mult": lam_mult, "floor": fd.floor(lam_mult, m),
           "greedy": {k: v for k, v in g.items() if k != "support"},
           "gap_greedy_to_floor": g["objective"] - fd.floor(lam_mult, m),
           "f104_gate": dr.resolution_gate(J, C),
           "guide_check": dr.resolution_check_guide(J, C)}
    best = g["objective"]
    if scip:
        sc = ec.exact_solver_control(J, C, m, ec.ScipSolver(), fd.SCIP_CAP_S)
        row["scip"] = {k: v for k, v in sc.items() if k != "support"}
        if sc.get("objective") is not None:
            best = min(best, sc["objective"])
    row["best_found"] = best
    row["gap_best_to_floor"] = best - fd.floor(lam_mult, m)
    return row


def falsifier_rows(rows: list[dict]) -> list[dict]:
    """The rows in the shape `f153_exp3_design.design_fails` reads."""
    return [{"methods": {"greedy": {"objective": r["chosen"]["greedy"]["objective"]}},
             "floor": r["chosen"]["floor"], "f104_gate": r["chosen"]["f104_gate"],
             "guide_check": r["chosen"]["guide_check"]} for r in rows]


def no_room(res: dict) -> bool:
    """The control's gate as the entry sets it: no room on every instance.
    Not `design_fails`, which also fires when both resolution checks fail
    on every instance; that term must not stop the IEEE-CIS reading
    (PR 63 review)."""
    return all(r["methods"]["greedy"]["objective"] - r["floor"] < fd.GAP_MIN
               for r in falsifier_rows(res["rows"]))


def gate(doc: dict, control: dict, read_ieee) -> None:
    """IEEE-CIS is built and read only after a control with room."""
    if no_room(control):
        doc["stopped"] = ("the positive control shows no room on every "
                          "instance; no IEEE-CIS pool built")
    else:
        doc["ieee"] = read_ieee()


def evaluate(instances: dict, scip: bool) -> dict:
    """instances: {(seed, cfg): (H, y, m)}. F153's ridge rule over all of
    them, then each at the chosen weight, and the falsifier."""
    sweeps = {key: room(H, y, m) for key, (H, y, m) in instances.items()}
    greedy_rows = [{"lam_mult": s["lam_mult"], "data_share": s["data_share"]}
                   for r in sweeps.values() for s in r["sweep"]]
    choice = fd.choose_ridge(greedy_rows)
    rows = []
    for key, (H, y, m) in instances.items():
        r = sweeps[key]
        r["chosen"] = chosen(m, H, y, choice["lam_mult"], scip)
        rows.append({"seed": key[0], "instance": key[1], **r})
    return {"ridge_choice": choice, "rows": rows,
            "design_fails": fd.design_fails(falsifier_rows(rows))}


def random_sign_instances(labels: dict) -> dict:
    out = {}
    for (seed, cfg), (y, n, m) in labels.items():
        rng = np.random.default_rng(1000 + seed)
        H = rng.choice([-1.0, 1.0], size=(n, len(y)))
        out[(seed, cfg)] = (H, y, m)
    return out


def ieee_fold():
    import data
    import ieee_harness as ih
    import ieee_loader
    df, _ = ieee_loader.dedupe_ieee(data.load_ieee_cis_train())
    fold = ih.folds_for(df)[0]
    b = ih.build_fold(df, fold)
    Xtr, Xev = b["X_train"], b["X_eval"]
    med = Xtr.median()
    Xtr, Xev = Xtr.fillna(med).fillna(0.0), Xev.fillna(med).fillna(0.0)
    ytr = b["parts"]["y_train"].to_numpy().astype(int)
    yev = b["parts"]["y_eval"].to_numpy().astype(int)
    return int(fold.eval_month), Xtr, ytr, Xev, yev


def ieee_instances(fold, seeds=SEEDS) -> tuple[dict, dict]:
    import data
    import pandas as pd
    import qubo_proxy as qp
    em, Xtr, ytr, Xev, yev = fold
    y_ev = np.where(yev == 1, 1, -1)
    y_tr = np.where(ytr == 1, 1, -1)
    out, meta = {}, {}
    for seed in seeds:
        rng = np.random.default_rng(seed)
        keep = []
        for c in (0, 1):
            idx = np.nonzero(ytr == c)[0]
            k = max(1, int(round(MI_ROWS * len(idx) / len(ytr))))
            keep.append(rng.choice(idx, k, replace=False))
        sub = np.sort(np.concatenate(keep))
        for cfg, (_, n, m) in zip(("free", "mid"), fd.INSTANCES):
            k = CONFIG_K[cfg]
            cols = data.top_k_features(Xtr.iloc[sub], pd.Series(ytr[sub]), k,
                                       seed=seed)
            t0 = time.perf_counter()
            # Schedule 2 for both sizes, as F94's free and mid pools.
            clf = qp.build_pool(Xtr[cols].to_numpy(np.float32), y_tr, 2,
                                "dct", "sequential",
                                weak_params=qp.seeded_weak_params(seed))
            H = qp.h_matrix(clf, Xev[cols].to_numpy(np.float32))
            meta[(seed, cfg)] = {"eval_month": em, "features": list(cols),
                                 "pool_size": int(H.shape[0]),
                                 "build_s": round(time.perf_counter() - t0, 1)}
            if H.shape[0] < n:
                # The entry: a smaller pool is refused and recorded.
                meta[(seed, cfg)]["refused"] = (
                    f"pool has {H.shape[0]} learners, instance needs {n}")
                continue
            out[(seed, cfg)] = (ec._first(H, n), y_ev, m)
    return out, meta


def read_instances(inst: dict, meta: dict) -> dict:
    """The IEEE-CIS reading: the instances that were built, with each
    refused pool recorded beside them."""
    refused = {f"{s}/{c}": m for (s, c), m in meta.items() if "refused" in m}
    if not inst:
        return {"rows": [], "refused": refused, "design_fails": None,
                "note": "every pool was refused; no reading"}
    res = evaluate(inst, scip=True)
    for r in res["rows"]:
        r.update(meta[(r["seed"], r["instance"])])
    return {**res, "rows": _rows(res), "refused": refused}


def _rows(res: dict) -> list:
    return [{k: v for k, v in r.items()} for r in res["rows"]]


def main(argv=None) -> int:
    import json
    import provenance
    rid, _ = provenance.start(OUT, resumable=False)
    t0 = time.time()
    fold = ieee_fold()
    em, _, ytr, _, yev = fold
    labels = {(s, cfg): (np.where(yev == 1, 1, -1), n, m)
              for s in SEEDS for cfg, n, m in fd.INSTANCES}
    control = evaluate(random_sign_instances(labels), scip=False)
    doc = {"card": "F160", "sprint": 29, "phase": 2, "evidence_tag": "SIM",
           "metered_seconds": 0,
           "entry": "experiments/phase2/PREREGISTRATION_DRAFT.md section 6, "
                    "Experiment 3, amendment 2026-10-26 (52454e2)",
           "dataset": "ieee-cis", "eval_month": em,
           "fraud_rate_train": float(ytr.mean()),
           "fraud_rate_eval": float(yev.mean()),
           "rule": {"gap_min": fd.GAP_MIN, "sweep": list(fd.SWEEP),
                    "scip_cap_s": fd.SCIP_CAP_S},
           "control": {"kind": "random-sign learners, seed 1000 + seed",
                       **control, "rows": _rows(control)},
           "complete": False}
    provenance.write_result(OUT, doc, __file__, list(SEEDS), rid)
    print("control no room", no_room(control), flush=True)
    gate(doc, control, lambda: read_instances(*ieee_instances(fold)))
    if "ieee" in doc:
        print("ieee design_fails", doc["ieee"]["design_fails"], flush=True)
    doc["wall_seconds"] = round(time.time() - t0, 1)
    doc["complete"] = True
    provenance.write_result(OUT, doc, __file__, list(SEEDS), rid)
    print("complete", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
