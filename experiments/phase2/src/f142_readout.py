"""F142 readout (Sprint 26 Task D): what the five Dirac-3S fits show.

Zero metered seconds. Reads the F142 rows and saved responses, Dirac-3's B4
rows (`experiments/results/b4_hardware.json`) and samples
(`experiments/phase2/results/device_samples/b4_*`), and F126's exact
optimum of each seeded B4 pool. Writes
`experiments/phase2/results/f142_readout.json`.

Written after the fits. The F142 entry's falsifier (the cosine band) was
fixed before any call; everything else here is descriptive, and the
uniform-vector baseline was added after the result, because B4's exact
optimum is itself near-uniform (`docs/phase2/F126_SPARSITY_RULE.md`).
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
import f126_sparsity_rule as f126  # noqa: E402

RES = ROOT / "experiments" / "phase2" / "results"
ROWS = RES / "f142_dirac3s_verify.json"
OUT = RES / "f142_readout.json"
B4_D3 = ROOT / "experiments" / "results" / "b4_hardware.json"
BAND = (0.8832, 0.9095)          # the F142 entry's falsifier, set before any call
CELL = "oilgas_gasturbine"


def cos(a, b) -> float:
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))


def _response(row: dict) -> dict:
    return json.loads((RES / row["all_samples"]).read_text(
        encoding="utf-8"))["response"]


def _best(resp: dict) -> np.ndarray:
    r = resp["results"]
    return np.asarray(r["solutions"][int(np.argmin(r["energies"]))],
                      dtype=np.float64)


def cost(row: dict) -> dict:
    resp = _response(row)
    t = row.get("device_timing") or {}
    st = resp["job_info"]["job_status"]

    def ts(k):
        from datetime import datetime
        return datetime.fromisoformat(st[k].replace("Z", "+00:00"))
    rt = t.get("runtime_sum_s")
    S = np.asarray(resp["results"]["solutions"], dtype=np.float64)
    return {
        "max_spread_between_samples_per_weight": float(
            (S.max(axis=0) - S.min(axis=0)).max()),
        "all_values_on_1e-7_grid": bool(
            np.abs(S * 1e7 - np.round(S * 1e7)).max() < 1e-6),
        "unit": row["unit"], "n_variables": row["screen"]["n_variables"],
        "n_samples": row["hw_config"]["num_samples"],
        "metered_seconds": row["metered_seconds"],
        "device_usage_s": resp["job_info"]["job_result"].get(
            "device_usage_s"),
        "runtime_sum_s": rt,
        "ceil_runtime_sum_s": math.ceil(rt) if rt is not None else None,
        "per_sample_s": rt / row["hw_config"]["num_samples"] if rt else None,
        "queued_to_running_s": round(
            (ts("running_at_rfc3339nano") - ts("queued_at_rfc3339nano"))
            .total_seconds(), 3),
        "running_to_completed_s": round(
            (ts("completed_at_rfc3339nano") - ts("running_at_rfc3339nano"))
            .total_seconds(), 3),
    }


def b4(row: dict, d3_rows: dict) -> dict:
    seed = row["seed"]
    w = f126.exact_weights(CELL, seed)
    dev = _best(_response(row))
    n = w.size
    u = np.full(n, 1.0 / n)
    c_dev = cos(dev, w)
    # The exact optimum is F126's seeded rebuild; the row's own cosine was
    # computed against the solve of the Hamiltonian actually sent. They must
    # agree, or the two pools differ and nothing below is readable.
    if abs(c_dev - row["weight_cosine_vs_classical"]) > 1e-6:
        raise SystemExit(f"REFUSING: seed {seed}: F126's exact optimum is "
                         "not the pool F142 sent")
    zero_dev, zero_ex = set(np.flatnonzero(dev == 0)), set(
        np.flatnonzero(w <= 1e-12))
    d3 = d3_rows[seed]
    d3_dev = f126.device_best(CELL, seed)
    return {
        "seed": seed,
        "dirac3s": {
            "weight_cosine_vs_exact": c_dev,
            "in_band": BAND[0] <= c_dev <= BAND[1],
            "deviation_correlation_vs_exact": float(
                np.corrcoef(dev - u, w - u)[0, 1]),
            "zero_count": len(zero_dev),
            "zeros_shared_with_exact": len(zero_dev & zero_ex),
            "objective_device": row["objective_device"],
            "objective_exact": row["objective_proxy_optimum"],
            "test_auprc": row["metrics"]["auprc"],
            "in_segment_auprc": row["in_segment"]["in_segment"]["auprc"],
            "random_control_auprc":
                row["in_segment"]["random_control"]["auprc"],
        },
        "uniform_vector_cosine_vs_exact": cos(u, w),
        # How fine the structure is that a device must reproduce: the
        # optimum's typical departure from uniform, against A31's weight
        # step (1/200 of the sum constraint of 1).
        "exact_median_abs_departure_from_uniform": float(
            np.median(np.abs(w - u))),
        "a31_weight_step": 1 / 200,
        "exact_zero_count": len(zero_ex),
        "n_variables": n,
        "dirac3": {
            "weight_cosine_vs_exact": d3["weight_cosine_vs_classical"],
            "zero_fraction_lowest_energy_sample": float(np.mean(d3_dev == 0)),
            "test_auprc": d3["metrics"]["auprc"],
            "in_segment_auprc": d3["in_segment"]["in_segment"]["auprc"],
            "note": "Phase 1 row, an unseeded build of the same cell and "
                    "seed: a different pool from the Dirac-3S fit's",
        },
    }


DRY_RUN = RES / "f142_dry_run.json"


def _pool(seed: int, row: dict | None = None) -> dict:
    """Rebuild the seeded B4 pool F142 sent: J, C, the test-fold H and the
    exact weights. Refuses unless its Hamiltonian hashes to the one the
    runner sent: the row's own `screen.hamiltonian_sha256` when present,
    else the hash the dry run recorded for that unit, else neither and it
    refuses."""
    import hashlib

    import qubo_proxy as qp
    import spectra_segment as ss
    c = ss.frozen_cell_by_name(CELL)["config"]
    split, cols = ss._prep_spectra(CELL, seed)

    def X(df):
        return ss.coerce_features_to_numeric(df[cols]).to_numpy("float32")
    y = np.where(split.y_train.to_numpy() == 1, 1, -1)
    lam = c["lambda_coef_alpha"] * len(y)
    clf = qp.build_pool(X(split.X_train), y, c["weak_cls_schedule"], "dct",
                        "sequential",
                        weak_params=qp.seeded_weak_params(
                            seed, c["weak_cls_params"]),
                        lambda_coef=lam)
    H_tr = qp.h_matrix(clf, X(split.X_train)).astype(np.float64)
    J, C = qp.hamiltonian(H_tr, y, lam)
    h = hashlib.sha256()
    for a in (J, C):
        h.update(np.ascontiguousarray(a, dtype=np.float64).tobytes())
    # The row records what was sent from PR #21's review on; the five rows
    # written before then carry it only in the dry-run file.
    unit = f"b4_oilgas_{seed}"
    want = (row or {}).get("screen", {}).get("hamiltonian_sha256")
    if want is None:
        sent = {u["unit"]: u.get("hamiltonian_sha256") for u in json.loads(
            DRY_RUN.read_text(encoding="utf-8"))["stops"]["3"]["units"]}
        want = sent.get(unit)
    if want is None:
        raise SystemExit(f"REFUSING: seed {seed}: no record of the "
                         "Hamiltonian F142 sent for this unit")
    if h.hexdigest() != want:
        raise SystemExit(f"REFUSING: seed {seed}: the rebuilt Hamiltonian "
                         "is not the one F142 screened and sent")
    return {"J": J, "C": C, "H_te": qp.h_matrix(clf, X(split.X_test)),
            "y_te": split.y_test.to_numpy()}


def structure(row: dict, pool: dict, w: np.ndarray) -> dict:
    """The fresh-eyes review's checks (2026-10-15), all written after the
    result: every sample, a baseline with the optimum's zeros, the error in
    weight units, the returned values' grid, and the reference solve's
    convergence."""
    from sklearn.metrics import average_precision_score
    J, C = pool["J"], pool["C"]
    resp = _response(row)["results"]
    S = np.asarray(resp["solutions"], dtype=np.float64)
    n = w.size
    u = np.full(n, 1.0 / n)
    zero_ex = w <= 1e-12
    u0 = np.where(zero_ex, 0.0, 1.0 / (n - zero_ex.sum()))

    def obj(v):
        return float(v @ J @ v + C @ v)

    def auprc(v):
        p = np.clip((v @ pool["H_te"] + 1.0) / 2.0, 0.0, 1.0)
        return float(average_precision_score(pool["y_te"], p))
    g = 2.0 * J @ w + C
    support = w > 1e-12
    grid = np.abs(S * 1e7 - np.round(S * 1e7)).max()
    best = S[int(np.argmin(resp["energies"]))]
    plateau_value, plateau_count = np.unique(np.round(w, 9),
                                             return_counts=True)
    return {
        "seed": row["seed"],
        "pool_hash_matches_dry_run": True,
        "per_sample": [{
            "reported_energy": float(e),
            "objective_minus_reference": obj(s) - obj(w),
            "cosine_vs_exact": cos(s, w),
            "deviation_correlation_vs_exact": float(
                np.corrcoef(s - u, w - u)[0, 1]),
            "max_abs_error_vs_exact": float(np.abs(s - w).max()),
            "zeros_shared_with_exact": int(((s == 0) & zero_ex).sum()),
            "sum": float(s.sum())} for s, e in zip(S, resp["energies"])],
        "max_abs_error_in_a31_steps": float(np.abs(S - w).max() / (1 / 200)),
        "max_spread_between_samples_per_weight": float(
            (S.max(axis=0) - S.min(axis=0)).max()),
        "all_values_on_1e-7_grid": bool(grid < 1e-6),
        "distinct_values_in_best_sample": int(np.unique(best).size),
        "exact_largest_plateau": {
            "value": float(plateau_value[np.argmax(plateau_count)]),
            "count": int(plateau_count.max())},
        "exact_weights_below_plateau": int(
            (w < plateau_value[np.argmax(plateau_count)] - 1e-9).sum()),
        "uniform_plus_exact_zeros": {
            "cosine_vs_exact": cos(u0, w),
            "deviation_correlation_vs_exact": float(
                np.corrcoef(u0 - u, w - u)[0, 1])},
        "reference_solve_kkt_gradient_spread_on_support": float(
            g[support].max() - g[support].min()),
        "test_auprc_scored_from_pool": {
            "exact_reference": auprc(w), "device_best_sample": auprc(best),
            "device_row_metrics": row["metrics"]["auprc"]},
    }


def main() -> int:
    record = json.loads(ROWS.read_text(encoding="utf-8"))
    rows = record["rows"]
    d3 = {r["seed"]: r for r in json.loads(B4_D3.read_text(
        encoding="utf-8"))["rows"] if CELL in r["dataset"]}
    ok = [r for r in rows if r["status"] == "ok"]
    out = {
        "generator": "experiments/phase2/src/f142_readout.py",
        "card": "F142", "sprint": 26,
        "evidence_tag": "HW (Dirac-3S samples) with SIM (exact solves)",
        "metered_seconds": 0,
        "falsifier_band": list(BAND),
        "falsifier_fixed": "experiments/phase2/PREREGISTRATION_DRAFT.md "
                           "section 6, F142, before any call",
        "baseline_added_after_result": "uniform_vector_cosine_vs_exact",
        # The runner's own total, over every row it wrote, so a billed row
        # that is not "ok" is never dropped from spend (PR #21 review).
        "total_metered_seconds": record["metered_seconds"],
        "units_not_scored": [r["unit"] for r in rows
                             if r["status"] != "ok"],
        "cost": [cost(r) for r in ok],
        "b4": [b4(r, d3) for r in ok if r["unit"].startswith("b4_")],
    }
    out["falsifier_fires"] = any(not b["dirac3s"]["in_band"]
                                 for b in out["b4"])
    out["b4_structure"] = [
        structure(r, _pool(r["seed"], r), f126.exact_weights(CELL, r["seed"]))
        for r in ok if r["unit"].startswith("b4_")]
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
