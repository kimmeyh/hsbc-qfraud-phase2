"""F153: Experiment 3's proxy design, the ridge sweep and both resolution checks.

Sprint 28 Task C (#50). Zero metered seconds. The entry is
`experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "Experiment 3",
committed before any Hamiltonian here was built. Reuses F94's instances,
objective and controls (`exp3_controls`), unchanged.

Steps, in the entry's order:
  1. Build F94's six validation-fold instances (seeds 42-44; 60 choose 10
     and 136 choose 25).
  2. Greedy at every ridge weight in the sweep; choose the weight by the
     entry's rule (data term at least 10% of |objective| on all six).
  3. At the chosen weight: the first instance's gap to the floor is checked
     before any comparison; then annealing and SCIP (300 s cap); test
     AUPRC for context, with outcome blocks.
  4. F104's gate and the guide's check on every chosen Hamiltonian.
  5. The device quote, as a bracket.

Run:  <venv python> experiments/phase2/src/f153_exp3_design.py
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
import exp3_controls as ec  # noqa: E402  (Phase 2, F94)
import outcome_record as orec  # noqa: E402  (Phase 2)

OUT = ROOT / "experiments" / "phase2" / "results" / "f153_exp3_design.json"
SEEDS = (42, 43, 44)
INSTANCES = (("free", 60, 10), ("mid", 136, 25))
SWEEP = (2.0, 0.2, 0.02, 0.002)
DATA_SHARE_MIN = 0.10
GAP_MIN = 0.01
SCIP_CAP_S = 300.0
# F139's two integer probes on Dirac-3 (seconds) and F142's Dirac-3S /
# Dirac-3 ratio range on the continuous solver; the bracket is inferred.
PROBES_DIRAC3_S = {"probe_mid_hi": 28, "probe_high": 165}
DIRAC3S_RATIO = (0.4, 1.3)


def floor(lam_mult: float, m: int) -> float:
    return -1.0 + lam_mult / m


def data_term(J, C, w, lam_mult: float) -> float:
    """||H'w - y||^2 / n = objective + 1 - lam_mult ||w||^2."""
    return ec.objective(J, C, w) + 1.0 - lam_mult * float(w @ w)


def _w(res: dict, n: int, J, C) -> np.ndarray:
    return ec.solve_on_support(J, C, res["support"]) if res.get("support") \
        else np.zeros(n)


def choose_ridge(greedy_rows: list[dict]) -> dict:
    """The largest weight whose data share is >= 10% on every instance."""
    # A weight with no rows must not qualify by an empty all().
    ok = [lm for lm in SWEEP
          if any(r["lam_mult"] == lm for r in greedy_rows)
          and all(r["data_share"] >= DATA_SHARE_MIN
                  for r in greedy_rows if r["lam_mult"] == lm)]
    if ok:
        return {"lam_mult": max(ok), "rule_met": True}
    return {"lam_mult": min(SWEEP), "rule_met": False}


def quote() -> dict:
    total = sum(PROBES_DIRAC3_S.values())
    lo, hi = DIRAC3S_RATIO
    return {"probes": PROBES_DIRAC3_S, "dirac3_total_s": total,
            "dirac3s_low_s": round(total * lo), "dirac3s_high_s": round(total * hi),
            "label": "inferred: F142's continuous-solver ratio applied to integer "
                     "probes; no Dirac-3S integer timing exists",
            "approval": "separate, per block (Criterion H)"}


def run() -> dict:
    import device_resolution as dr
    t_start = time.time()
    built = {}
    for seed in SEEDS:
        pools = {cfg: ec._pool(seed, cfg) for cfg in {c for c, _, _ in INSTANCES}}
        for cfg, n, m in INSTANCES:
            H_va, y_va = pools[cfg]["validation"]
            H_te, y_te = pools[cfg]["test"]
            built[(seed, cfg)] = {"H": ec._first(H_va, n), "y": y_va,
                                  "H_te": ec._first(H_te, n), "y_te": y_te, "m": m}
    greedy_rows = []
    for lm in SWEEP:
        for (seed, cfg), b in built.items():
            J, C = ec.problem(b["H"], b["y"], lm)
            g = ec.greedy(J, C, b["m"])
            w = _w(g, len(C), J, C)
            obj = g["objective"]
            greedy_rows.append({
                "lam_mult": lm, "seed": seed, "instance": cfg, "m": b["m"],
                "objective": obj, "floor": floor(lm, b["m"]),
                "gap_to_floor": obj - floor(lm, b["m"]),
                "data_term": data_term(J, C, w, lm),
                "data_share": data_term(J, C, w, lm) / abs(obj) if obj else float("nan"),
                "seconds": g["seconds"]})
            print(f"  lam {lm:<6} s{seed} {cfg:4s} obj {obj:.5f} gap "
                  f"{greedy_rows[-1]['gap_to_floor']:.4f} share "
                  f"{greedy_rows[-1]['data_share']:.3f}", flush=True)
    choice = choose_ridge(greedy_rows)
    lm = choice["lam_mult"]

    first = next(r for r in greedy_rows if r["lam_mult"] == lm)
    first_check = {"instance": f"s{first['seed']} {first['instance']}",
                   "gap_to_floor": first["gap_to_floor"],
                   "room_left": first["gap_to_floor"] >= GAP_MIN}

    rows = []
    for (seed, cfg), b in built.items():
        J, C = ec.problem(b["H"], b["y"], lm)
        m = b["m"]
        g = ec.greedy(J, C, m)
        sa = ec.simulated_annealing(J, C, m, seed)
        sc = ec.exact_solver_control(J, C, m, ec.ScipSolver(), SCIP_CAP_S)
        methods = {"greedy": g, "simulated_annealing": sa, "scip": sc}
        best = min(v["objective"] for v in methods.values() if v["objective"] is not None)
        aup = {}
        for name, res in methods.items():
            if res.get("support"):
                w = ec.solve_on_support(J, C, res["support"])
                p = np.clip((w @ b["H_te"] + 1) / 2, 0, 1)
                from sklearn.metrics import average_precision_score
                aup[name] = {"test_auprc": float(average_precision_score(b["y_te"], p)),
                             "outcome": orec.record(
                                 f"f153_{cfg}_lam{str(lm).replace('.', 'p')}_{name}",
                                 seed, b["y_te"], p)}
        rows.append({
            "seed": seed, "instance": cfg, "m": m, "lam_mult": lm,
            "floor": floor(lm, m), "best_found": best,
            "gap_best_to_floor": best - floor(lm, m),
            "greedy_minus_best": g["objective"] - best,
            "methods": {k: {kk: vv for kk, vv in v.items() if kk != "support"}
                        | {"support_size": v.get("support_size")}
                        for k, v in methods.items()},
            "context_test": aup,
            "f104_gate": dr.resolution_gate(J, C),
            "guide_check": dr.resolution_check_guide(J, C)})
        print(f"  chosen s{seed} {cfg}: best {best:.5f} gap {rows[-1]['gap_best_to_floor']:.4f} "
              f"scip {sc.get('status')} gate {rows[-1]['f104_gate']['pass']} "
              f"guide {rows[-1]['guide_check']['pass']}", flush=True)

    design_fails = (all(r["gap_best_to_floor"] < GAP_MIN for r in rows)
                    or all(not r["f104_gate"]["pass"] and not r["guide_check"]["pass"]
                           for r in rows))
    return {"generator": "experiments/phase2/src/f153_exp3_design.py",
            "card": "F153", "sprint": 28, "evidence_tag": "SIM",
            "metered_seconds": 0,
            "entry": "experiments/phase2/PREREGISTRATION_DRAFT.md section 6, Experiment 3",
            "seeds": list(SEEDS), "sweep": list(SWEEP),
            "rule": {"data_share_min": DATA_SHARE_MIN, "gap_min": GAP_MIN,
                     "scip_cap_s": SCIP_CAP_S},
            "greedy_sweep": greedy_rows, "ridge_choice": choice,
            "first_instance_check": first_check,
            "chosen": rows, "design_fails": design_fails,
            "quote": quote(), "wall_seconds": round(time.time() - t_start, 1)}


def main() -> None:
    res = run()
    OUT.write_text(json.dumps(res, indent=1, default=str), encoding="utf-8")
    print("chosen", res["ridge_choice"], "first", res["first_instance_check"],
          "design_fails", res["design_fails"], "quote", res["quote"]["dirac3s_low_s"],
          res["quote"]["dirac3s_high_s"])


if __name__ == "__main__":
    main()
