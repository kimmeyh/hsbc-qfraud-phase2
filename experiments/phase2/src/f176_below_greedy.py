"""F176 (Sprint 30 Task E, #79): Experiment 3 on IEEE-CIS, can a classical
solver get below greedy?

The entry is the 2026-10-31 amendment to "Experiment 3" in
`experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, committed before
this module existed. F160 measured the room only to the floor: greedy
ended about 0.097 above it on all six IEEE-CIS instances, and SCIP stopped
at its 300 s cap without beating greedy. Here, on the same six instances,
rebuilt from F160's seeded pools (F160 stored rows, not Hamiltonians):

1. The check that "below greedy" can fire, first: small instances
   (n = 20 learners, m = 4) solved exactly by enumeration; on one where
   greedy is not optimal, the local search must reach the optimum.
2. Each IEEE-CIS instance at F160's chosen weight: greedy (checked against
   F160's recorded objective before any solver runs), a best-improvement
   swap search from greedy's support, simulated annealing from greedy's
   support (3 seeds), and SCIP with a 1,200 s cap (4 x F160's).

    <venv python> experiments/phase2/src/f176_below_greedy.py

Zero metered seconds. Writes `experiments/phase2/results/f176_below_greedy.json`
through `provenance.write_result` after the check and after each
instance; resumable by instance, `complete` true at the end and a final
`complete` line on stdout.
"""
from __future__ import annotations

import itertools
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "experiments" / "src"))
import exp3_controls as ec  # noqa: E402
import f153_exp3_design as fd  # noqa: E402

OUT = ROOT / "experiments" / "phase2" / "results" / "f176_below_greedy.json"
F160 = ROOT / "experiments" / "phase2" / "results" / "f160_room_ieee.json"
# F168 part 7: a long run resumes through provenance.start.
LONG_RUN = True
TOL = ec.AGREE_TOL                     # 1e-6: "below" means by more than this
SCIP_CAP_S = 1200.0                    # 4 x F160's 300 s
SA_SEEDS = (42, 43, 44)
MAX_PASSES = 100
CHECK_N, CHECK_M = 20, 4               # F94's exact-check size
CHECK_RANDOM_SEEDS = tuple(range(20))
GREEDY_MATCH = 1e-9                    # rebuilt greedy vs F160's record


def swap_search(J, C, m: int, start) -> dict:
    """Best-improvement 1-swap local search over size-m supports, from
    `start`, until no swap improves by more than TOL or MAX_PASSES."""
    t0 = time.perf_counter()
    n = len(C)
    cache: dict[tuple, float] = {}

    def energy(sup):
        key = tuple(sorted(int(i) for i in sup))
        if key not in cache:
            cache[key] = ec.objective(J, C, ec.solve_on_support(J, C, key))
        return cache[key]

    S = sorted(int(i) for i in start)
    cur, passes = energy(S), 0
    while passes < MAX_PASSES:
        passes += 1
        best_T, best_e = None, cur
        for out_i, in_j in itertools.product(S, range(n)):
            if in_j in S:
                continue
            T = sorted([i for i in S if i != out_i] + [in_j])
            e = energy(T)
            if e < best_e - TOL:
                best_T, best_e = T, e
        if best_T is None:
            break
        S, cur = best_T, best_e
    w = ec.solve_on_support(J, C, S)
    return ec._result(J, C, w, "swap_search", time.perf_counter() - t0, m,
                      passes=passes, supports_checked=len(cache))


def methods(J, C, m: int, scip_cap_s: float | None = SCIP_CAP_S) -> dict:
    g = ec.greedy(J, C, m)
    out = {"greedy": g, "swap_search": swap_search(J, C, m, g["support"])}
    for s in SA_SEEDS:
        out[f"sa_from_greedy_{s}"] = ec.simulated_annealing(
            J, C, m, s, start=g["support"])
    if scip_cap_s:
        out["scip"] = ec.exact_solver_control(J, C, m, ec.ScipSolver(),
                                              scip_cap_s)
    return out


def reading(res: dict, greedy_obj: float, floor: float) -> dict:
    """Best found, its gap to greedy and to the floor, and whether any
    method got below greedy by more than TOL."""
    found = {k: v["objective"] for k, v in res.items()
             if v.get("objective") is not None}
    best_m = min(found, key=found.get)
    best = found[best_m]
    out = {"best_method": best_m, "best_objective": best,
           "gap_best_to_greedy": best - greedy_obj,
           "gap_best_to_floor": best - floor,
           "gap_greedy_to_floor": greedy_obj - floor,
           "below_greedy": bool(best < greedy_obj - TOL)}
    dual = (res.get("scip") or {}).get("dual_bound")
    if dual is not None:
        # No selection can be below SCIP's dual bound.
        out["scip_dual_bound"] = dual
        out["room_bound"] = greedy_obj - max(dual, floor)
    return out


# ----------------------------------------------------------- the check
def check_instance(H: np.ndarray, y: np.ndarray, lam_mult: float) -> dict:
    J, C = ec.problem(H[:CHECK_N], y, lam_mult)
    ex = ec.exact_enumeration(J, C, CHECK_M)
    g = ec.greedy(J, C, CHECK_M)
    ls = swap_search(J, C, CHECK_M, g["support"])
    return {"exact": ex["objective"], "greedy": g["objective"],
            "swap_search": ls["objective"],
            "greedy_not_optimal": bool(g["objective"] > ex["objective"] + TOL),
            "search_reaches_exact": bool(abs(ls["objective"] - ex["objective"])
                                         <= TOL)}


def can_fire(cases: dict) -> dict:
    """"Below greedy" can fire if some case has greedy above the exact
    optimum and the swap search reaches it there."""
    fired = [k for k, c in cases.items()
             if c["greedy_not_optimal"] and c["search_reaches_exact"]]
    missed = [k for k, c in cases.items()
              if c["greedy_not_optimal"] and not c["search_reaches_exact"]]
    return {"cases": cases, "fires_on": fired, "search_missed": missed,
            "can_fire": bool(fired)}


def random_check_cases(lam_mult: float, n_rows: int = 400) -> dict:
    out = {}
    for s in CHECK_RANDOM_SEEDS:
        rng = np.random.default_rng(5000 + s)
        y = np.where(rng.random(n_rows) < 0.1, 1, -1)
        H = rng.choice([-1.0, 1.0], size=(CHECK_N, n_rows))
        out[f"random_{s}"] = check_instance(H, y, lam_mult)
    return out


# ----------------------------------------------------------- the run
def f160_record() -> dict:
    doc = json.loads(F160.read_text(encoding="utf-8"))
    rows = {(r["seed"], r["instance"]): r for r in doc["ieee"]["rows"]}
    return {"lam_mult": doc["ieee"]["ridge_choice"]["lam_mult"], "rows": rows}


def _doc(check, rows, complete=False):
    return {"card": "F176", "sprint": 30, "phase": 2, "evidence_tag": "SIM",
            "metered_seconds": 0, "dataset": "ieee_cis",
            "entry": "experiments/phase2/PREREGISTRATION_DRAFT.md section 6, "
                     "Experiment 3, 2026-10-31 amendment (F176)",
            "instances_from": "f160_room_ieee.json (rebuilt from its seeded "
                              "pools; greedy checked against its record)",
            "tol": TOL, "scip_cap_s": SCIP_CAP_S, "sa_seeds": list(SA_SEEDS),
            "max_passes": MAX_PASSES, "check": check, "rows": rows,
            "complete": complete}


def run() -> None:
    import f160_room_ieee as f160
    import provenance
    rid, resume = provenance.start(OUT)
    prior = json.loads(OUT.read_text(encoding="utf-8")) if resume else {}
    rec = f160_record()
    lam = rec["lam_mult"]
    t0 = time.perf_counter()
    fold = f160.ieee_fold()
    inst, meta = f160.ieee_instances(fold)
    print(f"instances rebuilt in {round(time.perf_counter() - t0)} s",
          flush=True)
    seeds = sorted({s for s, _ in rec["rows"]})
    check = prior.get("check")
    if check is None:
        cases = {f"{s}/{c}": check_instance(H, y, lam)
                 for (s, c), (H, y, _) in inst.items()}
        cases.update(random_check_cases(lam))
        check = can_fire(cases)
        provenance.write_result(OUT, _doc(check, []), __file__, seeds, rid)
        print("check", json.dumps({k: check[k] for k in
                                   ("fires_on", "can_fire")}), flush=True)
    rows = prior.get("rows", [])
    for (s, c), (H, y, m) in sorted(inst.items()):
        if any(r["seed"] == s and r["instance"] == c for r in rows):
            continue           # resume: never resolve an instance
        J, C = ec.problem(H, y, lam)
        g = ec.greedy(J, C, m)
        recorded = rec["rows"][(s, c)]["chosen"]["greedy"]["objective"]
        if abs(g["objective"] - recorded) > GREEDY_MATCH:
            raise RuntimeError(
                f"{s}/{c}: rebuilt greedy {g['objective']} differs from "
                f"F160's {recorded}; the instance is not F160's")
        res = methods(J, C, m)
        floor = fd.floor(lam, m)
        rows.append({"seed": s, "instance": c, "m": m,
                     "n_learners": int(H.shape[0]), "lam_mult": lam,
                     "floor": floor, "f160_greedy": recorded,
                     "methods": res,
                     "reading": reading(res, g["objective"], floor),
                     "features": meta[(s, c)]["features"]})
        provenance.write_result(OUT, _doc(check, rows), __file__, seeds, rid)
        print(f"{s}/{c}: {json.dumps(rows[-1]['reading'])}", flush=True)
    doc = _doc(check, rows, complete=True)
    doc["summary"] = {
        "below_greedy_instances": [f"{r['seed']}/{r['instance']}" for r in rows
                                   if r["reading"]["below_greedy"]],
        "n_instances": len(rows),
        "check_can_fire": check["can_fire"]}
    provenance.write_result(OUT, doc, __file__, seeds, rid)
    print("complete", flush=True)


if __name__ == "__main__":
    run()
