"""F144 (Sprint 26 Task C): the proxy twin of B2's configuration.

Entry: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F144",
written before any twin pool was built.

Two steps, each a command:

    # WSL (the full-pair build needs fork), one pool per call:
    python experiments/phase2/src/f144_proxy_twin.py build --arm twin --seed 42
    python experiments/phase2/src/f144_proxy_twin.py build --arm ref --seed 42

    # either platform, after all 20 pools exist:
    python experiments/phase2/src/f144_proxy_twin.py score

Arms:
- `twin`: the `full` config (k=17, schedule 3, full pair, 833 variables),
  built with F145's seeded weak learners.
- `ref`: the `free` config (91 variables, full pair), rebuilt UNSEEDED, to
  compare with the stored Phase 1 `h_*_free_dct_full` pools. The true
  difference is zero, so this measures the build's run-to-run drift.

Phase 1 files are read, never written: the stored pools and B2's rows in
`experiments/results/`. Pools go to `experiments/phase2/results/pools/`
(ignored); the result goes to `experiments/phase2/results/f144_proxy_twin.json`.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

SRC = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC))
import metrics  # noqa: E402
import qubo_proxy as qp  # noqa: E402

PHASE2_RESULTS = Path(__file__).resolve().parents[1] / "results"
POOLS = PHASE2_RESULTS / "pools"
OUT = PHASE2_RESULTS / "f144_proxy_twin.json"
PHASE1_RESULTS = qp.RESULTS
PHASE1_POOLS = qp.POOLS_DIR
SEEDS = qp.SEEDS
ARMS = {"twin": {"config": "full", "seeded": True},
        "ref": {"config": "free", "seeded": False}}
ALPHA = 0.05


def pool_path(arm: str, seed: int) -> Path:
    return POOLS / f"f144_{arm}_{ARMS[arm]['config']}_dct_full_{seed}.npz"


def cmd_build(args) -> None:
    spec = ARMS[args.arm]
    out = pool_path(args.arm, args.seed)
    if out.exists():
        # Reused only if it was built the same way (code review finding 15).
        meta = json.loads(out.with_suffix(".meta.json").read_text())
        same = (meta.get("arm"), meta.get("config"),
                meta.get("seeded_learners")) == (args.arm, spec["config"],
                                                 spec["seeded"])
        if not same:
            raise SystemExit(f"{out.name} exists but was built differently "
                             f"({meta}); remove it to rebuild")
        print(f"[skip] {out.name} exists")
        return
    t0 = time.time()
    split, cols, Xtr, Xva, Xte, y_pm1 = qp._prep(
        args.seed, qp.CONFIGS[spec["config"]]["k"])
    params = qp.seeded_weak_params(args.seed) if spec["seeded"] else None
    clf = qp.build_pool(Xtr, y_pm1, qp.CONFIGS[spec["config"]]["schedule"],
                        "dct", "full", weak_params=params)
    H_tr, H_va, H_te = (qp.h_matrix(clf, X) for X in (Xtr, Xva, Xte))
    out.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(out, H_tr=H_tr, H_va=H_va, H_te=H_te,
                        y_tr01=split.y_train.to_numpy(),
                        y_te=split.y_test.to_numpy())
    meta = {"arm": args.arm, "seed": args.seed, "config": spec["config"],
            "seeded_learners": spec["seeded"], "features": cols,
            "n_pool": len(clf.h_list), "build_seconds": round(time.time() - t0, 1)}
    out.with_suffix(".meta.json").write_text(json.dumps(meta, indent=1))
    print(f"[built] {out.name} pool={len(clf.h_list)} "
          f"{meta['build_seconds']}s")


def test_auprc(npz) -> dict:
    """Score a saved pool exactly as qubo_proxy.cmd_solve does."""
    y_pm1 = np.where(npz["y_tr01"] == 1, 1, -1)
    w = qp.solve_simplex_qp(npz["H_tr"], y_pm1, qp.LAMBDA_MULT * len(y_pm1))
    p = np.clip((w @ npz["H_te"] + 1.0) / 2.0, 0.0, 1.0)
    y = npz["y_te"]
    from sklearn.metrics import average_precision_score, roc_auc_score
    ap = float(average_precision_score(y, p))
    prev = float(np.mean(y))
    return {"auprc": ap, "auprc_norm": (ap - prev) / (1 - prev),
            "auroc": float(roc_auc_score(y, p)), "n_pool": int(len(w))}


def paired(a: list[float], b: list[float], seed: int = 42) -> dict:
    """a minus b, per seed: exact Wilcoxon (primary), bootstrap and t."""
    from scipy.stats import wilcoxon
    d = np.asarray(a) - np.asarray(b)
    p = float(wilcoxon(d, alternative="two-sided", method="exact").pvalue)
    rng = np.random.default_rng(seed)
    boot = rng.choice(d, size=(10000, len(d)), replace=True).mean(axis=1)
    lo, hi = np.percentile(boot, [2.5, 97.5])
    return {"diffs": d.tolist(), "mean": float(d.mean()),
            "wilcoxon_p": p, "rejects": bool(p < ALPHA),
            "bootstrap_ci95": [float(lo), float(hi)],
            "t_interval": metrics.seed_mean_t_interval(d.tolist())}


def b2_device_auprc() -> dict[int, float]:
    rows = json.loads(PHASE1_RESULTS.read_text(encoding="utf-8"))["rows"]
    out = {r["seed"]: float(r["metrics"]["auprc"]) for r in rows
           if r.get("config") == "hw_b2_full" and r.get("status") == "ok"
           and r.get("seed") in SEEDS}
    assert sorted(out) == list(SEEDS), f"B2 seeds found: {sorted(out)}"
    return out


def stored_proxy_auprc() -> dict[int, float]:
    """Phase 1's own rows for the stored free pools: a check that this
    script scores a pool the way Phase 1 did."""
    rows = json.loads(PHASE1_RESULTS.read_text(encoding="utf-8"))["rows"]
    return {r["seed"]: float(r["metrics"]["auprc"]) for r in rows
            if r.get("arm") == "cvqboost_proxy" and r.get("config") == "free"
            and r.get("pool_variant") == "dct"
            and r.get("pair_build") == "full"}


def cmd_score(args) -> None:
    missing = [pool_path(a, s).name for a in ARMS for s in SEEDS
               if not pool_path(a, s).exists()]
    if missing:
        raise SystemExit(f"pools missing: {missing}")
    stored_rows = stored_proxy_auprc()
    rows, ref_stored, ref_rebuilt, twin, device = [], [], [], [], []
    b2 = b2_device_auprc()
    for s in SEEDS:
        st = test_auprc(np.load(PHASE1_POOLS / f"h_{s}_free_dct_full.npz"))
        rb = test_auprc(np.load(pool_path("ref", s)))
        tw = test_auprc(np.load(pool_path("twin", s)))
        ref_stored.append(st["auprc"])
        ref_rebuilt.append(rb["auprc"])
        twin.append(tw["auprc"])
        device.append(b2[s])
        rows.append({"seed": s, "evidence_tag": "SIM",
                     "ref_stored": st, "ref_rebuilt": rb, "twin": tw,
                     "b2_device_auprc": b2[s],
                     "stored_row_auprc": stored_rows.get(s)})
    missing_rows = [r["seed"] for r in rows if r["stored_row_auprc"] is None]
    if missing_rows:
        raise SystemExit(f"no Phase 1 free proxy row for seeds {missing_rows}")
    scoring_check = max(abs(r["ref_stored"]["auprc"] - r["stored_row_auprc"])
                        for r in rows)
    # Enforced, not only reported (code review finding 9): if this script
    # scored a pool differently from Phase 1, nothing below is comparable.
    if scoring_check > 1e-9:
        raise SystemExit(f"scoring differs from Phase 1's rows by "
                         f"{scoring_check}; refusing to write a result")
    ref = paired(ref_rebuilt, ref_stored)
    dev = paired(device, twin)
    doc = {
        "generator": "experiments/phase2/src/f144_proxy_twin.py",
        "card": "F144", "sprint": 26, "evidence_tag": "SIM",
        "metered_seconds": 0,
        "entry": "experiments/phase2/PREREGISTRATION_DRAFT.md section 6, F144",
        "written": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "scoring_check_max_abs_diff_vs_phase1_rows": scoring_check,
        "drift_reference": ref,
        "device_vs_twin": dev,
        "device_comparison_readable": not ref["rejects"],
        "note": "Twins B2's configuration, not its pools, which were "
                "never stored. Device AUPRC read from Phase 1 hw_b2_full "
                "rows; nothing in experiments/results/ is written.",
        "rows": rows,
    }
    OUT.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: doc[k] for k in (
        "scoring_check_max_abs_diff_vs_phase1_rows",
        "device_comparison_readable")}, indent=1))
    print("reference:", {k: ref[k] for k in ("mean", "wilcoxon_p",
                                              "bootstrap_ci95")})
    print("device-twin:", {k: dev[k] for k in ("mean", "wilcoxon_p",
                                                "bootstrap_ci95")})


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--arm", choices=list(ARMS), required=True)
    b.add_argument("--seed", type=int, required=True)
    sub.add_parser("score")
    args = ap.parse_args()
    {"build": cmd_build, "score": cmd_score}[args.cmd](args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
