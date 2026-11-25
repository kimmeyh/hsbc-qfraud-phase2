"""F188 (Sprint 32 Task C, #112): do F176's below-greedy gains on
IEEE-CIS survive the device's resolution?

The entry is "F188" in `experiments/phase2/PREREGISTRATION_DRAFT.md`
section 6, committed before this module existed. F176 found selections
below greedy by under 2e-05 on the six IEEE-CIS instances. The device
sees each coefficient only to max |coefficient| / R, with R about 200
(QCi's stated figure, `device_resolution.DYNAMIC_RANGE`; not measured on
Dirac-3S). Here each instance is rounded at R = 100, 200 and 400 and
every support F176 recorded is solved again on the rounded problem. No
search is run again.

1. The check that "lost" can fire, first: F176's check size (20
   learners choosing 4), solved exactly; on each case where greedy is
   above the optimum, the gain must be kept with no rounding, and lost
   at R = 2 on at least one case.
2. Each IEEE-CIS instance, rebuilt with F176's code and its greedy
   checked against F176's record, at each R.

    <venv python> experiments/phase2/src/f188_rounding.py
    <venv python> experiments/phase2/src/f188_rounding.py --delivered
    <venv python> experiments/phase2/src/f188_rounding.py --release-rule

`--release-rule` (F200, Sprint 34 Task E) computes Experiment 3's
release rule as filed on 2026-11-18 (Sprint 33 D6), after filing, as the
filing's first test: at R = 200, the support the rounded problem ranks
best against greedy's own selection solved the same way (both weights
solved on the rounded problem, both scored on the unrounded one). It
passes on an instance when the pick is below greedy by more than TOL,
and the rule is met when it passes on at least one. Before the verdict,
every instance whose pick is greedy's selection must show a gain of
exactly zero. Written to `f188_release_rule.json`.

Zero metered seconds. Writes `experiments/phase2/results/f188_rounding.json`
through `provenance.write_result`, once, at the end (`resumable=False`).
`--delivered` is the entry's amendment (the second reading): the support
each rounded problem ranks best, its weights scored on the unrounded
problem, written to `f188_rounding_delivered.json`.
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
import exp3_controls as ec  # noqa: E402
import f176_below_greedy as f176  # noqa: E402

OUT = ROOT / "experiments" / "phase2" / "results" / "f188_rounding.json"
OUT_DELIVERED = OUT.with_name("f188_rounding_delivered.json")
OUT_RELEASE = OUT.with_name("f188_release_rule.json")
LONG_RUN = False                       # about 10 minutes, one straight run
F176_OUT = f176.OUT
TOL = f176.TOL                         # 1e-6, F176's "below"
RANGES = (100.0, 200.0, 400.0)         # 200 is the reading (the entry)
READING_R = 200.0
CHECK_COARSE_R = 2.0
GREEDY_MATCH = 1e-9


def rounded(J: np.ndarray, C: np.ndarray, R: float):
    """The problem the device can see: every coefficient rounded to the
    nearest multiple of max(|J|, |C|) / R (`device_resolution`'s rule).
    R = inf returns the problem unchanged."""
    if math.isinf(R):
        return J, C, 0.0
    step = float(max(np.abs(J).max(), np.abs(C).max())) / R
    if not step > 0:
        raise ValueError("every coefficient is zero; nothing to round")
    return np.round(J / step) * step, np.round(C / step) * step, step


def support_objective(J, C, support) -> float:
    """Weights solved again on `support` for this problem, and their
    objective on it."""
    return ec.objective(J, C, ec.solve_on_support(J, C, support))


def gain(J, C, R: float, greedy_support, others: dict) -> dict:
    """Best other support's objective minus greedy's, on the problem
    rounded at R. Kept when it is below -TOL."""
    Jq, Cq, step = rounded(J, C, R)
    g = support_objective(Jq, Cq, greedy_support)
    objs = {k: support_objective(Jq, Cq, s) for k, s in others.items()}
    best = min(objs, key=objs.get)
    d = objs[best] - g
    return {"R": None if math.isinf(R) else R, "step": step,
            "greedy": g, "best_other": best, "best_other_objective": objs[best],
            "gain": d, "gain_in_steps": (d / step) if step else None,
            "kept": bool(d < -TOL)}


def delivered(J, C, R: float, greedy_support, others: dict) -> dict:
    """The entry's amendment (second reading): the support the problem
    rounded at R ranks best is the device's pick; its weights, solved on
    the rounded problem, are scored on the unrounded one. It delivers a
    gain when that is below greedy's unrounded objective by more than
    TOL."""
    Jq, Cq, step = rounded(J, C, R)
    supports = {"greedy": greedy_support, **others}
    seen = {k: support_objective(Jq, Cq, s) for k, s in supports.items()}
    pick = min(seen, key=seen.get)
    w = ec.solve_on_support(Jq, Cq, supports[pick])
    true_pick = ec.objective(J, C, w)
    greedy_true = support_objective(J, C, greedy_support)
    d = true_pick - greedy_true
    return {"R": None if math.isinf(R) else R, "step": step, "pick": pick,
            "pick_unrounded_objective": true_pick,
            "greedy_unrounded_objective": greedy_true,
            "delivered_gain": d, "delivers": bool(d < -TOL)}


def release(J, C, R: float, greedy_support, others: dict) -> dict:
    """Experiment 3's release rule as filed (Sprint 33 D6): the support
    the problem rounded at R ranks best, against greedy's selection solved
    the same way. Both weights are solved on the rounded problem and both
    are scored on the unrounded one, so a pick that is greedy's selection
    gains exactly zero. It passes when the pick is below greedy by more
    than TOL."""
    Jq, Cq, step = rounded(J, C, R)
    supports = {"greedy": greedy_support, **others}
    seen = {k: support_objective(Jq, Cq, s) for k, s in supports.items()}
    pick = min(seen, key=seen.get)
    pick_true = ec.objective(J, C, ec.solve_on_support(Jq, Cq, supports[pick]))
    greedy_true = ec.objective(J, C, ec.solve_on_support(Jq, Cq, greedy_support))
    d = pick_true - greedy_true
    return {"R": None if math.isinf(R) else R, "step": step, "pick": pick,
            "pick_objective": pick_true, "greedy_objective": greedy_true,
            "release_gain": d, "passes": bool(d < -TOL)}


def require_zero_where_greedy(rows: list[dict]) -> list[str]:
    """The check fired before the verdict: where the pick is greedy's
    selection, the gain is exactly zero. Returns those instances."""
    at = [r for r in rows if r["release"]["pick"] == "greedy"]
    bad = [f"{r['seed']}/{r['instance']}" for r in at
           if r["release"]["release_gain"] != 0.0]
    if bad:
        raise RuntimeError("the pick is greedy's selection but the gain is "
                           f"not zero on {bad}: greedy is not solved the "
                           "same way as the pick")
    return [f"{r['seed']}/{r['instance']}" for r in at]


def verdict(rows: list[dict]) -> dict:
    """The rule is met when it passes on at least one instance."""
    at = [f"{r['seed']}/{r['instance']}" for r in rows
          if r["release"]["passes"]]
    return {"n_instances": len(rows), "passes_on": at,
            "rule_met": bool(at),
            "finding": ("met: the device arm (F25) may leave HOLD, after the "
                        "dated amendment that commitment 2 requires"
                        if at else
                        "not met on any instance: F25 stays on HOLD")}


def release_doc(rows: list[dict], n_expected: int, check: dict) -> dict:
    """The F200 result, `complete` only with every instance."""
    if n_expected == 0 or len(rows) != n_expected:
        raise RuntimeError(f"{len(rows)} rows for {n_expected} F176 "
                           "instances; not complete")
    return {"card": "F200", "sprint": 34, "phase": 2, "evidence_tag": "SIM",
            "metered_seconds": 0, "dataset": "ieee_cis",
            "entry": "experiments/phase2/PREREGISTRATION_SUBMITTED_2026-11-18.md "
                     "section 6, Experiment 3, the release rule (Sprint 33 D6)",
            "computed_after_filing": "2026-11-18",
            "reading_range": READING_R, "tol": TOL,
            "check": check, "rows": rows, "verdict": verdict(rows),
            "complete": True}


def run_release() -> None:
    import f160_room_ieee as f160
    import provenance
    f176_doc = json.loads(F176_OUT.read_text(encoding="utf-8"))
    require_complete(f176_doc)
    old = {(r["seed"], r["instance"]): r for r in json.loads(
        OUT_DELIVERED.read_text(encoding="utf-8"))["rows"]}
    rid, _ = provenance.start(OUT_RELEASE, resumable=False)
    lam = f176_doc["rows"][0]["lam_mult"]
    t0 = time.perf_counter()
    inst, _ = f160.ieee_instances(f160.ieee_fold())
    print(f"instances rebuilt in {round(time.perf_counter() - t0)} s",
          flush=True)
    rows = []
    for rec in f176_doc["rows"]:
        H, y, m = inst[(rec["seed"], rec["instance"])]
        J, C = ec.problem(H, y, lam)
        require_same_greedy(rec, ec.greedy(J, C, m)["objective"])
        meth = rec["methods"]
        others = {k: v["support"] for k, v in meth.items()
                  if k != "greedy" and v.get("support")}
        r = release(J, C, READING_R, meth["greedy"]["support"], others)
        prior = old[(rec["seed"], rec["instance"])]["rounded"][
            str(int(READING_R))]
        rows.append({"seed": rec["seed"], "instance": rec["instance"],
                     "release": r,
                     "old_comparison_gain": prior["delivered_gain"]})
        print(f"{rec['seed']}/{rec['instance']}: pick {r['pick']}, gain "
              f"{r['release_gain']:.3e}", flush=True)
    greedy_at = require_zero_where_greedy(rows)
    check = {"pick_is_greedy_on": greedy_at,
             "gain_there": 0.0,
             "old_comparison_gain_there": {
                 f"{r['seed']}/{r['instance']}": r["old_comparison_gain"]
                 for r in rows if r["release"]["pick"] == "greedy"},
             "can_fire": bool(greedy_at) and any(
                 r["old_comparison_gain"] != 0.0 for r in rows
                 if r["release"]["pick"] == "greedy")}
    doc = release_doc(rows, len(f176_doc["rows"]), check)
    provenance.write_result(OUT_RELEASE, doc, __file__,
                            sorted({r["seed"] for r in rows}), rid)
    print(json.dumps(doc["verdict"]), flush=True)
    print("complete", flush=True)


# ----------------------------------------------------------- the check
def check_case(H: np.ndarray, y: np.ndarray, lam: float) -> dict | None:
    """One exact-size case; None when greedy is already optimal there."""
    J, C = ec.problem(H[:f176.CHECK_N], y, lam)
    ex = ec.exact_enumeration(J, C, f176.CHECK_M)
    g = ec.greedy(J, C, f176.CHECK_M)
    if not g["objective"] > ex["objective"] + TOL:
        return None
    others = {"exact": ex["support"]}
    return {"exact_minus_greedy": ex["objective"] - g["objective"],
            "unrounded": gain(J, C, math.inf, g["support"], others),
            "coarse": gain(J, C, CHECK_COARSE_R, g["support"], others)}


def can_fire(cases: dict) -> dict:
    """"Lost" can fire if every case keeps its gain unrounded and at least
    one loses it at the coarse R."""
    kept = all(c["unrounded"]["kept"] for c in cases.values())
    lost = [k for k, c in cases.items() if not c["coarse"]["kept"]]
    return {"n_cases": len(cases), "kept_unrounded_on_all": kept,
            "lost_at_coarse_on": lost,
            "can_fire": bool(cases) and kept and bool(lost)}


def random_cases(lam: float) -> dict:
    out = {}
    for s in f176.CHECK_RANDOM_SEEDS:
        rng = np.random.default_rng(5000 + s)        # F176's draws
        y = np.where(rng.random(400) < 0.1, 1, -1)
        H = rng.choice([-1.0, 1.0], size=(f176.CHECK_N, 400))
        c = check_case(H, y, lam)
        if c is not None:
            out[f"random_{s}"] = c
    return out


# ----------------------------------------------------------- the run
def reading(per_r: dict) -> dict:
    r = per_r[str(int(READING_R))]
    return {"kept_at_200": r["kept"], "gain_at_200": r["gain"],
            "gain_in_steps_at_200": r["gain_in_steps"],
            "kept_at": [k for k, v in per_r.items() if v["kept"]]}


def instance_row(J, C, rec: dict) -> dict:
    meth = rec["methods"]
    greedy_support = meth["greedy"]["support"]
    others = {k: v["support"] for k, v in meth.items()
              if k != "greedy" and v.get("support")}
    per_r = {str(int(R)): gain(J, C, R, greedy_support, others)
             for R in RANGES}
    unrounded = gain(J, C, math.inf, greedy_support, others)
    return {"seed": rec["seed"], "instance": rec["instance"], "m": rec["m"],
            "f176_gain": rec["reading"]["gap_best_to_greedy"],
            "unrounded": unrounded, "rounded": per_r,
            "reading": reading(per_r)}


def summary(rows: list[dict]) -> dict:
    kept = [f"{r['seed']}/{r['instance']}" for r in rows
            if r["reading"]["kept_at_200"]]
    return {"n_instances": len(rows), "kept_at_200": kept,
            "all_lost_at_200": not kept,
            "finding": ("lost at R = 200 on every instance: no device run on "
                        "this formulation at this resolution can show the "
                        "gains F176 found" if not kept else
                        "kept at R = 200 on " + ", ".join(kept) +
                        ": the device question stays open there")}


def require_complete(f176_doc: dict) -> None:
    if f176_doc.get("complete") is not True:
        raise RuntimeError("f176_below_greedy.json is not complete")


def require_same_greedy(rec: dict, rebuilt: float) -> None:
    recorded = rec["methods"]["greedy"]["objective"]
    if not abs(rebuilt - recorded) <= GREEDY_MATCH:
        raise RuntimeError(
            f"{rec['seed']}/{rec['instance']}: rebuilt greedy {rebuilt} "
            f"differs from F176's {recorded}; not F176's instance")


def delivered_doc(rows: list[dict], n_expected: int) -> dict:
    """The second reading's result, `complete` only with every instance."""
    if len(rows) != n_expected or n_expected == 0:
        raise RuntimeError(f"{len(rows)} rows for {n_expected} F176 "
                           "instances; not complete")
    at = [f"{r['seed']}/{r['instance']}" for r in rows
          if r["rounded"][str(int(READING_R))]["delivers"]]
    return {"card": "F188", "sprint": 32, "phase": 2, "evidence_tag": "SIM",
            "metered_seconds": 0, "dataset": "ieee_cis",
            "entry": "experiments/phase2/PREREGISTRATION_DRAFT.md section 6, "
                     "F188, amendment of 2026-11-09 (second reading)",
            "first_reading": "experiments/phase2/results/f188_rounding.json",
            "ranges": list(RANGES), "reading_range": READING_R, "tol": TOL,
            "rows": rows,
            "summary": {"n_instances": len(rows), "delivers_at_200": at},
            "complete": True}


def run_delivered() -> None:
    import f160_room_ieee as f160
    import provenance
    f176_doc = json.loads(F176_OUT.read_text(encoding="utf-8"))
    require_complete(f176_doc)
    rid, _ = provenance.start(OUT_DELIVERED, resumable=False)
    lam = f176_doc["rows"][0]["lam_mult"]
    inst, _ = f160.ieee_instances(f160.ieee_fold())
    rows = []
    for rec in f176_doc["rows"]:
        H, y, m = inst[(rec["seed"], rec["instance"])]
        J, C = ec.problem(H, y, lam)
        require_same_greedy(rec, ec.greedy(J, C, m)["objective"])
        meth = rec["methods"]
        others = {k: v["support"] for k, v in meth.items()
                  if k != "greedy" and v.get("support")}
        g = meth["greedy"]["support"]
        rows.append({"seed": rec["seed"], "instance": rec["instance"],
                     "f176_gain": rec["reading"]["gap_best_to_greedy"],
                     "rounded": {str(int(R)): delivered(J, C, R, g, others)
                                 for R in RANGES}})
        print(f"{rec['seed']}/{rec['instance']}: " + json.dumps(
            {k: v["delivered_gain"] for k, v in rows[-1]["rounded"].items()}),
            flush=True)
    doc = delivered_doc(rows, len(f176_doc["rows"]))
    provenance.write_result(OUT_DELIVERED, doc, __file__,
                            sorted({r["seed"] for r in rows}), rid)
    print("complete", flush=True)


def run() -> None:
    import f160_room_ieee as f160
    import provenance
    f176_doc = json.loads(F176_OUT.read_text(encoding="utf-8"))
    require_complete(f176_doc)
    rid, _ = provenance.start(OUT, resumable=False)
    lam = f176_doc["rows"][0]["lam_mult"]
    t0 = time.perf_counter()
    inst, _ = f160.ieee_instances(f160.ieee_fold())
    print(f"instances rebuilt in {round(time.perf_counter() - t0)} s",
          flush=True)

    cases = {}
    for (s, c), (H, y, _m) in sorted(inst.items()):
        got = check_case(H, y, lam)
        if got is not None:
            cases[f"{s}/{c}"] = got
    cases.update(random_cases(lam))
    check = can_fire(cases)
    check["cases"] = cases
    print("check", json.dumps({k: check[k] for k in
                               ("n_cases", "lost_at_coarse_on", "can_fire")}),
          flush=True)

    rows = []
    for rec in f176_doc["rows"]:
        H, y, m = inst[(rec["seed"], rec["instance"])]
        J, C = ec.problem(H, y, lam)
        require_same_greedy(rec, ec.greedy(J, C, m)["objective"])
        rows.append(instance_row(J, C, rec))
        print(f"{rec['seed']}/{rec['instance']}: "
              f"{json.dumps(rows[-1]['reading'])}", flush=True)
    doc = final_doc(check, rows, len(f176_doc["rows"]))
    seeds = sorted({r["seed"] for r in rows})
    provenance.write_result(OUT, doc, __file__, seeds, rid)
    print("complete", flush=True)


def final_doc(check: dict, rows: list[dict], n_expected: int) -> dict:
    """The result, `complete` only when every F176 instance has a row."""
    if len(rows) != n_expected or n_expected == 0:
        raise RuntimeError(f"{len(rows)} rows for {n_expected} F176 "
                           "instances; not complete")
    return {"card": "F188", "sprint": 32, "phase": 2, "evidence_tag": "SIM",
           "metered_seconds": 0, "dataset": "ieee_cis",
           "entry": "experiments/phase2/PREREGISTRATION_DRAFT.md section 6, "
                    "F188 (2026-11-09)",
           "instances_from": "f176_below_greedy.json (rebuilt with F176's "
                             "code; greedy checked against its record)",
           "rounding": "step = max(|J|, |C|) / R; coefficients rounded to "
                       "the nearest step (device_resolution's rule)",
           "ranges": list(RANGES), "reading_range": READING_R, "tol": TOL,
           "check": check, "rows": rows, "summary": summary(rows),
           "complete": True}


if __name__ == "__main__":
    if sys.argv[1:] == ["--delivered"]:
        run_delivered()
    elif sys.argv[1:] == ["--release-rule"]:
        run_release()
    elif sys.argv[1:]:
        raise SystemExit(f"usage: f188_rounding.py [--delivered | "
                         f"--release-rule]; "
                         f"got {sys.argv[1:]}")
    else:
        run()
