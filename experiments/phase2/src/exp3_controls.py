"""F94: Experiment 3's classical controls, built before any device block runs.

Sprint 25 Task F (#18). Phase 2 code: it IMPORTS Phase 1 modules (`qubo_proxy`)
and edits none. Results go to `experiments/phase2/results/f94_controls.json`.
Zero metered seconds.

THE PROBLEM. Cardinality-constrained CVQBoost on the identical Hamiltonian
`qubo_proxy` solves: minimize w'Jw + C'w with J = HH^T + lambda*I, C = -2Hy,
lambda = 2 * n_train (LAMBDA_MULT), subject to sum(w) = 1, w >= 0 and at most
m nonzero weights. The continuous problem is convex and solved exactly in
milliseconds (Sprint 4); the cardinality limit makes it combinatorial, which
is Experiment 3's whole point. J and C are divided by n_train before any
solve. That changes no argmin and keeps every solver's numbers near 1.

THE CONTROLS, each on the same instances:
  - exact enumeration of every support of size m at a small size: the
    certified optimum the others are checked against;
  - greedy forward selection: add the learner that lowers the objective most,
    until m are chosen;
  - simulated annealing over supports of size m (swap one in, one out), with
    its seed recorded;
  - SCIP (Sprint 25 D4) through `ExactSolver`, a thin interface so that a
    commercial solver supplied in Phase 2 can be dropped in and checked on the
    same instances. Each SCIP solve is capped and reports its gap.
Every support's weights are the exact convex optimum ON that support, so the
methods differ only in which support they choose.

INSTANCES (Sprint 25 plan, corrected at plan verification): ULB proxy pools
built sequentially, seeds 42-44: the first 60 learners of the frozen `free`
pool (m = 10) and the whole 136-learner `mid` pool (m = 25). The exact check
uses the first 20 learners of the `free` pool with m = 4. Each instance is
solved twice: on the training fold, as the device runs build it, and on the
validation fold (see SOURCES for why).

PREMISE FALSIFIER FOR THE SOLVER LEG: SCIP and exact enumeration must agree
where both run. If they do not, the SCIP leg is not used and the cause is
recorded.

Run:  <venv python> experiments/phase2/src/exp3_controls.py
"""
from __future__ import annotations

import hashlib
import itertools
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

OUT = ROOT / "experiments" / "phase2" / "results" / "f94_controls.json"
SEEDS = (42, 43, 44)
INSTANCES = (("free", 60, 10), ("mid", 136, 25))
EXACT_CHECK = ("free", 20, 4)
SCIP_TIME_LIMIT_S = 600.0
SA_ITERATIONS = 3000
AGREE_TOL = 1e-6
# Which rows the objective is built on. "train" is the pool's own training
# fold, as `qubo_proxy` and the device runs use it. Added during the run
# (Sprint 25, recorded in SPRINT_25_VALIDATION.md): on "train" the dct
# learners memorize the fold (69 of 78 `free` and 124 of 136 `mid` learners
# classify every row correctly), so every size-m support ties and no control
# can be told apart from another. "validation" builds the same objective on
# the held-out validation fold, where the learners differ. Test is scored
# only, never optimized on.
SOURCES = ("train", "validation")


# ------------------------------------------------------------ the objective

def problem(H: np.ndarray, y_pm1: np.ndarray, lam_mult: float = 2.0):
    """(J, C) of the CVQBoost Hamiltonian, scaled by 1/n_train."""
    n = H.shape[1]
    J = (H @ H.T).astype(np.float64) / n + lam_mult * np.eye(H.shape[0])
    C = (-2.0 * H @ y_pm1).astype(np.float64) / n
    return J, C


def objective(J: np.ndarray, C: np.ndarray, w: np.ndarray) -> float:
    return float(w @ J @ w + C @ w)


def _project_simplex(v: np.ndarray) -> np.ndarray:
    u = np.sort(v)[::-1]
    css = np.cumsum(u)
    rho = np.nonzero(u * np.arange(1, len(v) + 1) > (css - 1))[0][-1]
    return np.maximum(v - (css[rho] - 1.0) / (rho + 1.0), 0.0)


def solve_on_support(J: np.ndarray, C: np.ndarray, support,
                     max_iter: int = 20000, tol: float = 1e-13) -> np.ndarray:
    """Exact convex optimum with weights only on `support` (FISTA on the simplex)."""
    S = np.asarray(sorted(support))
    Js, Cs = J[np.ix_(S, S)], C[S]
    L = 2.0 * float(np.linalg.eigvalsh(Js)[-1]) + 1e-12
    x = np.full(len(S), 1.0 / len(S))
    z, t, prev = x.copy(), 1.0, float(x @ Js @ x + Cs @ x)
    for _ in range(max_iter):
        x_new = _project_simplex(z - (2.0 * Js @ z + Cs) / L)
        t_new = (1.0 + np.sqrt(1.0 + 4.0 * t * t)) / 2.0
        z = x_new + ((t - 1.0) / t_new) * (x_new - x)
        x, t = x_new, t_new
        cur = float(x @ Js @ x + Cs @ x)
        if abs(prev - cur) <= tol * (1.0 + abs(prev)):
            break
        prev = cur
    w = np.zeros(len(C))
    w[S] = x
    return w


def _result(J, C, w, method, seconds, m: int | None = None, **extra) -> dict:
    """One method's answer. With `m` given, a support over m is refused: an
    infeasible answer would otherwise win on objective (Sprint 25 review)."""
    support = [int(i) for i in np.flatnonzero(w > 1e-12)]
    if m is not None and len(support) > m:
        raise ValueError(f"{method} returned {len(support)} learners, limit {m}")
    return {"method": method, "objective": objective(J, C, w),
            "support": support, "support_size": len(support),
            "weight_sum": float(w.sum()), "min_weight": float(w.min()),
            "seconds": round(seconds, 3), **extra}


# --------------------------------------------------------------- the controls

def exact_enumeration(J, C, m: int) -> dict:
    t0 = time.perf_counter()
    best_w, best = None, np.inf
    for S in itertools.combinations(range(len(C)), m):
        w = solve_on_support(J, C, S)
        f = objective(J, C, w)
        if f < best:
            best, best_w = f, w
    return _result(J, C, best_w, "exact_enumeration", time.perf_counter() - t0, m,
                   supports_checked=math.comb(len(C), m))


def greedy(J, C, m: int) -> dict:
    t0 = time.perf_counter()
    chosen: list[int] = []
    w = None
    for _ in range(m):
        best_j, best_f, best_w = None, np.inf, None
        for j in range(len(C)):
            if j in chosen:
                continue
            cand = solve_on_support(J, C, chosen + [j])
            f = objective(J, C, cand)
            if f < best_f:
                best_j, best_f, best_w = j, f, cand
        chosen.append(best_j)
        w = best_w
    return _result(J, C, w, "greedy", time.perf_counter() - t0, m)


def simulated_annealing(J, C, m: int, seed: int,
                        iterations: int = SA_ITERATIONS,
                        start: list[int] | None = None) -> dict:
    """Swap moves over size-m supports; geometric cooling from the initial
    spread of move costs. `start` defaults to a random support."""
    t0 = time.perf_counter()
    rng = np.random.default_rng(seed)
    n = len(C)
    S = list(start) if start is not None else list(rng.choice(n, size=m, replace=False))
    cache: dict[tuple, float] = {}

    def energy(sup):
        key = tuple(sorted(int(i) for i in sup))
        if key not in cache:
            cache[key] = objective(J, C, solve_on_support(J, C, key))
        return cache[key]

    cur = energy(S)
    best_S, best = list(S), cur
    probe = []
    for _ in range(20):
        T = list(S)
        T[rng.integers(m)] = int(rng.choice([j for j in range(n) if j not in S]))
        probe.append(abs(energy(T) - cur))
    temp0 = max(float(np.mean(probe)), 1e-12)
    for it in range(iterations):
        temp = temp0 * (1e-3 ** (it / max(iterations - 1, 1)))
        T = list(S)
        T[rng.integers(m)] = int(rng.choice([j for j in range(n) if j not in S]))
        e = energy(T)
        if e <= cur or rng.random() < np.exp(-(e - cur) / temp):
            S, cur = T, e
            if cur < best:
                best_S, best = list(S), cur
    w = solve_on_support(J, C, best_S)
    return _result(J, C, w, "simulated_annealing", time.perf_counter() - t0, m,
                   sa_seed=seed, iterations=iterations,
                   supports_evaluated=len(cache))


class ExactSolver:
    """Interface for an exact mixed-integer solver of the cardinality problem.

    `solve` returns the support it found, its status, and its best bound. The
    weights are then re-solved exactly on that support, so every method is
    scored by the same objective code."""

    name = "abstract"

    def solve(self, J, C, m: int, time_limit_s: float) -> dict:
        raise NotImplementedError


class ScipSolver(ExactSolver):
    """SCIP through PySCIPOpt: binaries z, w <= z, sum z <= m, sum w = 1, and
    the quadratic objective entered as a constraint on an epigraph variable."""

    name = "scip"

    def solve(self, J, C, m: int, time_limit_s: float) -> dict:
        from pyscipopt import Model, quicksum
        n = len(C)
        md = Model()
        md.hideOutput()
        md.setParam("limits/time", float(time_limit_s))
        w = [md.addVar(lb=0.0, ub=1.0, name=f"w{i}") for i in range(n)]
        z = [md.addVar(vtype="B", name=f"z{i}") for i in range(n)]
        t = md.addVar(lb=None, name="t")
        md.addCons(quicksum(w) == 1.0)
        for i in range(n):
            md.addCons(w[i] <= z[i])
        md.addCons(quicksum(z) <= m)
        md.addCons(t >= quicksum(J[i, j] * w[i] * w[j] for i in range(n) for j in range(n))
                   + quicksum(C[i] * w[i] for i in range(n)))
        md.setObjective(t, "minimize")
        md.optimize()
        status = md.getStatus()
        if md.getNSols() == 0:
            return {"status": status, "support": None, "dual_bound": md.getDualbound()}
        # The support comes from the binaries, not from w: SCIP's feasibility
        # tolerance (1e-6) admits a tiny w_i with z_i = 0 (Sprint 25 review).
        zv = np.array([md.getVal(v) for v in z])
        return {"status": status, "support": [int(i) for i in np.flatnonzero(zv > 0.5)],
                "dual_bound": float(md.getDualbound()), "gap": float(md.getGap()),
                "solver_objective": float(md.getObjVal())}


def exact_solver_control(J, C, m: int, solver: ExactSolver,
                         time_limit_s: float = SCIP_TIME_LIMIT_S) -> dict:
    t0 = time.perf_counter()
    out = solver.solve(J, C, m, time_limit_s)
    secs = time.perf_counter() - t0
    if out["support"] is None:
        return {"method": solver.name, "objective": None, "status": out["status"],
                "seconds": round(secs, 3), "dual_bound": out["dual_bound"]}
    w = solve_on_support(J, C, out["support"])
    return _result(J, C, w, solver.name, secs, m, status=out["status"],
                   gap=out["gap"], dual_bound=out["dual_bound"],
                   solver_objective=out["solver_objective"])


# ----------------------------------------------------------------- the run

def _pool(seed: int, config: str) -> dict:
    """{source: (H, labels)}: train and validation labels in {-1, +1} for the
    objective; test labels in {0, 1} for scoring."""
    import qubo_proxy as qp
    split, cols, Xtr, Xva, Xte, y_pm1 = qp._prep(seed, qp.CONFIGS[config]["k"])
    clf = qp.build_pool(Xtr, y_pm1, qp.CONFIGS[config]["schedule"], "dct", "sequential")
    y_va = np.where(split.y_val.to_numpy() == 1, 1, -1)
    return {"train": (qp.h_matrix(clf, Xtr), y_pm1),
            "validation": (qp.h_matrix(clf, Xva), y_va),
            "test": (qp.h_matrix(clf, Xte), split.y_test.to_numpy())}


def _test_auprc(w, H_te, y_te) -> float:
    from sklearn.metrics import average_precision_score
    return float(average_precision_score(y_te, np.clip((w @ H_te + 1) / 2, 0, 1)))


def _first(H: np.ndarray, n: int) -> np.ndarray:
    """The first n learners; a smaller pool is refused, not silently used
    under the larger label (Sprint 25 review)."""
    if H.shape[0] < n:
        raise ValueError(f"pool has {H.shape[0]} learners, instance needs {n}")
    return H[:n]


def agrees(exact: dict, solver: dict, tol: float = AGREE_TOL) -> bool:
    """The exact leg's falsifier: the solver CERTIFIED optimality and matches
    enumeration. A time-limited incumbent that happens to match does not
    count (Sprint 25 review)."""
    return (solver.get("objective") is not None
            and solver.get("status") == "optimal"
            and abs(solver["objective"] - exact["objective"])
            <= tol * (1 + abs(exact["objective"])))


def pool_diagnostics(H: np.ndarray, y_pm1: np.ndarray) -> dict:
    """How distinguishable the learners are on the rows the objective sees."""
    agree = (H @ y_pm1) / H.shape[1]
    G = (H @ H.T) / H.shape[1]
    off = G[~np.eye(len(G), dtype=bool)]
    return {"learners_perfect_on_these_rows": int((agree == 1.0).sum()),
            "agreement_with_label_min": float(agree.min()),
            "agreement_with_label_max": float(agree.max()),
            "pairwise_agreement_min": float(off.min()) if off.size else None}


def run() -> dict:
    rows, checks, diagnostics = [], [], []
    pools = {}
    for seed in SEEDS:
        for config in sorted({c for c, _, _ in INSTANCES} | {EXACT_CHECK[0]}):
            print(f"[F94] building {config} pool, seed {seed}", flush=True)
            pools[(seed, config)] = _pool(seed, config)
    scip = ScipSolver()
    for source in SOURCES:
        for seed in SEEDS:
            config, n, m = EXACT_CHECK
            p = pools[(seed, config)]
            J, C = problem(_first(p[source][0], n), p[source][1])
            ex = exact_enumeration(J, C, m)
            sc = exact_solver_control(J, C, m, scip)
            agree = agrees(ex, sc)
            checks.append({"source": source, "seed": seed, "config": config, "n": n,
                           "m": m, "exact": ex, "scip": sc, "agree": bool(agree)})
            print(f"[F94] exact check {source} seed {seed}: exact {ex['objective']:.10f} "
                  f"scip {sc['objective']} agree={agree}", flush=True)
    for source in SOURCES:
        for seed in SEEDS:
            for config, n, m in INSTANCES:
                p = pools[(seed, config)]
                H, y = _first(p[source][0], n), p[source][1]
                H_te, y_te = _first(p["test"][0], n), p["test"][1]
                diagnostics.append({"source": source, "seed": seed, "config": config,
                                    "n": n, "n_pool": int(p[source][0].shape[0]),
                                    **pool_diagnostics(H, y)})
                J, C = problem(H, y)
                relaxed = solve_on_support(J, C, range(n))
                inst = {"source": source, "seed": seed, "config": config, "n": n, "m": m,
                        "relaxed_objective": objective(J, C, relaxed),
                        "relaxed_support_size": int((relaxed > 1e-12).sum()),
                        "relaxed_test_auprc": _test_auprc(relaxed, H_te, y_te)}
                for res in (greedy(J, C, m),
                            simulated_annealing(J, C, m, seed=seed),
                            exact_solver_control(J, C, m, scip)):
                    if res.get("objective") is not None:
                        res["test_auprc"] = _test_auprc(
                            solve_on_support(J, C, res["support"]), H_te, y_te)
                    rows.append({**inst, **res})
                    print(f"[F94] {source} seed {seed} {config} n={n} m={m} "
                          f"{res['method']}: {res.get('objective')} ({res['seconds']} s)",
                          flush=True)
    return {"pool_diagnostics": diagnostics, "exact_checks": checks, "rows": rows,
            "summary": summarize(checks, rows)}


def summarize(checks: list[dict], rows: list[dict]) -> dict:
    """Per-instance comparison. If SCIP failed any certified exact check, its
    rows are kept but it is not ranked (the plan's premise falsifier)."""
    scip_ok = bool(checks) and all(c["agree"] for c in checks)
    out = {"scip_agrees_with_enumeration": scip_ok,
           "exact_checks": len(checks), "per_instance": []}
    if not scip_ok:
        out["scip_excluded_reason"] = ("no exact check ran" if not checks else
                                       "SCIP did not certify a match with enumeration")
    by = {}
    for r in rows:
        by.setdefault((r.get("source", "train"), r["seed"], r["config"]), []).append(r)
    for (source, seed, config), rs in sorted(by.items()):
        objs = {r["method"]: r.get("objective") for r in rs}
        valid = [v for k, v in objs.items()
                 if v is not None and (scip_ok or k != "scip")]
        best = min(valid) if valid else None
        out["per_instance"].append({
            "source": source, "seed": seed, "config": config, "objectives": objs,
            "test_auprc": {r["method"]: r.get("test_auprc") for r in rs},
            "best_method": [k for k, v in objs.items()
                            if v is not None and v == best and (scip_ok or k != "scip")],
            "gap_to_best": {k: (None if v is None or best is None else v - best)
                            for k, v in objs.items()},
            "scip_status": next((r.get("status") for r in rs if r["method"] == "scip"), None),
            "scip_gap": next((r.get("gap") for r in rs if r["method"] == "scip"), None)})
    return out


def main() -> int:
    res = run()
    header = {
        "generator": "experiments/phase2/src/exp3_controls.py", "card": "F94",
        "sprint": 25, "phase": 2, "evidence_tag": "SIM", "metered_seconds": 0,
        "date": time.strftime("%Y-%m-%d"), "dataset": "ulb",
        "seeds": list(SEEDS), "instances": [list(i) for i in INSTANCES],
        "exact_check": list(EXACT_CHECK), "scip_time_limit_s": SCIP_TIME_LIMIT_S,
        "sa_iterations": SA_ITERATIONS, "sources": list(SOURCES),
        "objective_scale": "J and C divided by the number of rows the objective is built on",
        "solver_versions": _versions(),
        "generator_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    OUT.write_text(json.dumps({**header, **res}, indent=2), encoding="utf-8")
    print(json.dumps(res["summary"], indent=1))
    return 0


def _versions() -> dict:
    from importlib import metadata
    import pyscipopt
    return {"pyscipopt": metadata.version("pyscipopt"),
            "scip": str(pyscipopt.Model().version())}


if __name__ == "__main__":
    raise SystemExit(main())
