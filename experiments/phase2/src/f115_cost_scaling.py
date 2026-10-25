"""F115: the integer-probe cost fit, computed from the probe's own rows.

Sprint 28 Task I (#55). Zero metered seconds. Reads
`experiments/results/integer_probe.json` (Phase 1 evidence, read only) and
writes `experiments/phase2/results/f115_cost_scaling.json`.

The hardware plan says integer cost is "superlinear in variables" and quotes
the fit `vars^0.75 x levels^0.52`. That fit is sublinear in variables at
fixed levels; it is superlinear only when levels grow with variables. This
script reproduces the fit and adds what the plan does not say: four of the
five probes have levels = 4 x variables, so they identify only the SUM of
the two exponents, and the split between them rests on the fifth probe
(`probe_deep`) alone.

Run:  <venv python> experiments/phase2/src/f115_cost_scaling.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PROBE = ROOT / "experiments" / "results" / "integer_probe.json"
OUT = ROOT / "experiments" / "phase2" / "results" / "f115_cost_scaling.json"


def distinct_points(calls: list[dict]) -> list[dict]:
    """One row per probe label, first occurrence (probe_small ran twice at
    the same cost); only successful calls."""
    seen: dict[str, dict] = {}
    for c in calls:
        if c.get("status") == "ok" and c["label"] not in seen:
            seen[c["label"]] = c
    return list(seen.values())


def log_fit(vars_, levels, seconds) -> dict:
    """log s = a + b log vars + c log levels, least squares."""
    X = np.c_[np.ones(len(vars_)), np.log(vars_), np.log(levels)]
    y = np.log(seconds)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    r2 = 1 - float(resid @ resid) / float(((y - y.mean()) ** 2).sum())
    miss = np.exp(X @ beta) / np.asarray(seconds, float) - 1
    return {"intercept": float(beta[0]), "vars_exponent": float(beta[1]),
            "levels_exponent": float(beta[2]), "exponent_sum": float(beta[1] + beta[2]),
            "r2": r2, "relative_miss": [float(m) for m in miss],
            "max_abs_miss": float(np.max(np.abs(miss)))}


def sum_only_fit(vars_, seconds) -> dict:
    """On points with levels proportional to vars, only the sum is defined."""
    X = np.c_[np.ones(len(vars_)), np.log(vars_)]
    beta, *_ = np.linalg.lstsq(X, np.log(seconds), rcond=None)
    return {"exponent_sum": float(beta[1])}


def run() -> dict:
    pts = distinct_points(json.loads(PROBE.read_text(encoding="utf-8"))["calls"])
    v = np.array([p["n_variables"] for p in pts], float)
    lv = np.array([p["level_budget"] for p in pts], float)
    s = np.array([p["metered_seconds"] for p in pts], float)
    ratio = lv / v
    prop = np.isclose(ratio, np.median(ratio))
    full = log_fit(v, lv, s)
    return {"generator": "experiments/phase2/src/f115_cost_scaling.py",
            "card": "F115", "sprint": 28, "evidence_tag": "HW (re-analysis, no new call)",
            "metered_seconds": 0,
            "source": "experiments/results/integer_probe.json",
            "points": [{"label": p["label"], "n_variables": p["n_variables"],
                        "level_budget": p["level_budget"],
                        "metered_seconds": p["metered_seconds"]} for p in pts],
            "two_factor_fit": full,
            "levels_per_variable": [float(r) for r in ratio],
            "points_with_levels_proportional": [p["label"] for p, k in zip(pts, prop) if k],
            "points_off_the_line": [p["label"] for p, k in zip(pts, prop) if not k],
            "sum_only_fit_on_proportional_points": sum_only_fit(v[prop], s[prop]),
            "reading": {
                "fixed_levels": "cost ~ vars^b with b < 1: sublinear in variables",
                "levels_grow_with_variables": "cost ~ vars^(b+c) with b+c > 1: superlinear",
                "identification": ("the split between b and c rests on the points "
                                   "off the levels = k x vars line; here one point"),
            }}


def main() -> None:
    res = run()
    OUT.write_text(json.dumps(res, indent=1), encoding="utf-8")
    f = res["two_factor_fit"]
    print(f"vars^{f['vars_exponent']:.2f} x levels^{f['levels_exponent']:.2f}, "
          f"R^2 {f['r2']:.3f}, max miss {f['max_abs_miss']:.0%}; off-line points "
          f"{res['points_off_the_line']}; sum-only "
          f"{res['sum_only_fit_on_proportional_points']['exponent_sum']:.2f}")


if __name__ == "__main__":
    main()
