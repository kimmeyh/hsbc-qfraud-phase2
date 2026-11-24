"""F198 (Sprint 34 Task F, #140): F188 at other ridge weights and finer
resolutions.

The entry is amendment P2-A4 in
`experiments/phase2/PREREGISTRATION_AMENDMENTS.md`, committed before this
module existed. On F176's six IEEE-CIS instances, with F176's ridge
weight (`lam_mult` 2.0) times 0.1, 1 and 10, and R = 100, 200, 400, 800
and 1,600, it reports three readings for each instance, weight and R:

- F188's registered reading (`f188_rounding.gain`): kept when the best
  other support is below greedy on the rounded problem by more than 1e-6;
- F188's delivered reading (`f188_rounding.delivered`);
- the filed release rule's comparison (`f188_rounding.release`).

F188's check that "lost" can fire runs first at each weight. F176's
supports are reused; no search is run again. Descriptive, no test, no
device: a passing setting does not open the device arm (P2-A4).

    <venv python> experiments/phase2/src/f198_extended.py

Zero metered seconds. Writes `experiments/phase2/results/f198_extended.json`.
"""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "experiments" / "src"))
import exp3_controls as ec  # noqa: E402
import f188_rounding as fr  # noqa: E402

OUT = ROOT / "experiments" / "phase2" / "results" / "f198_extended.json"
LONG_RUN = False                 # one straight run; see the plan's runtime
WEIGHT_FACTORS = (0.1, 1.0, 10.0)
RANGES = (100.0, 200.0, 400.0, 800.0, 1600.0)


def setting_row(J, C, greedy_support, others: dict, R: float) -> dict:
    g = fr.gain(J, C, R, greedy_support, others)
    d = fr.delivered(J, C, R, greedy_support, others)
    r = fr.release(J, C, R, greedy_support, others)
    return {"R": R, "kept": g["kept"], "gain": g["gain"],
            "delivered_gain": d["delivered_gain"], "delivers": d["delivers"],
            "release_pick": r["pick"], "release_gain": r["release_gain"],
            "release_passes": r["passes"]}


def summary(rows: list[dict]) -> dict:
    """Where each reading holds, as `<weight factor>/<R>/<instance>`."""
    def where(key):
        return [f"{r['weight_factor']}/{int(s['R'])}/{r['seed']}/{r['instance']}"
                for r in rows for s in r["settings"] if s[key]]
    return {"kept_at": where("kept"), "delivers_at": where("delivers"),
            "release_passes_at": where("release_passes")}


def extended_doc(rows: list[dict], checks: dict, n_instances: int) -> dict:
    want = n_instances * len(WEIGHT_FACTORS)
    if n_instances == 0 or len(rows) != want or any(
            len(r["settings"]) != len(RANGES) for r in rows):
        raise RuntimeError(f"{len(rows)} rows for {want} (instance, weight) "
                           "pairs, or a missing R; not complete")
    return {"card": "F198", "sprint": 34, "phase": 2, "evidence_tag": "SIM",
            "metered_seconds": 0, "dataset": "ieee_cis",
            "entry": "experiments/phase2/PREREGISTRATION_AMENDMENTS.md P2-A4",
            "weight_factors": list(WEIGHT_FACTORS), "ranges": list(RANGES),
            "tol": fr.TOL, "checks": checks, "rows": rows,
            "summary": summary(rows), "complete": True}


def main(argv: list[str]) -> None:
    if argv:
        raise SystemExit(f"usage: f198_extended.py; got {argv}")
    run()


def run() -> None:
    import f160_room_ieee as f160
    import provenance
    f176_doc = json.loads(fr.F176_OUT.read_text(encoding="utf-8"))
    fr.require_complete(f176_doc)
    rid, _ = provenance.start(OUT, resumable=False)
    lam0 = f176_doc["rows"][0]["lam_mult"]
    t0 = time.perf_counter()
    inst, _ = f160.ieee_instances(f160.ieee_fold())
    print(f"instances rebuilt in {round(time.perf_counter() - t0)} s",
          flush=True)
    rows, checks = [], {}
    for factor in WEIGHT_FACTORS:
        lam = lam0 * factor
        cases = {}
        for (s, c), (H, y, _m) in sorted(inst.items()):
            got = fr.check_case(H, y, lam)
            if got is not None:
                cases[f"{s}/{c}"] = got
        cases.update(fr.random_cases(lam))
        chk = fr.can_fire(cases)
        checks[str(factor)] = {k: chk[k] for k in
                               ("n_cases", "kept_unrounded_on_all",
                                "lost_at_coarse_on", "can_fire")}
        print(f"weight x{factor}: check {json.dumps(checks[str(factor)])}",
              flush=True)
        for rec in f176_doc["rows"]:
            H, y, m = inst[(rec["seed"], rec["instance"])]
            J, C = ec.problem(H, y, lam)
            if factor == 1.0:
                fr.require_same_greedy(rec, ec.greedy(J, C, m)["objective"])
            meth = rec["methods"]
            greedy_support = ec.greedy(J, C, m)["support"]
            others = {k: v["support"] for k, v in meth.items()
                      if k != "greedy" and v.get("support")}
            rows.append({"seed": rec["seed"], "instance": rec["instance"],
                         "weight_factor": factor, "lam_mult": lam,
                         "settings": [setting_row(J, C, greedy_support,
                                                  others, R)
                                      for R in RANGES]})
            print(f"x{factor} {rec['seed']}/{rec['instance']} done "
                  f"({round(time.perf_counter() - t0)} s)", flush=True)
    doc = extended_doc(rows, checks, len(f176_doc["rows"]))
    provenance.write_result(OUT, doc, __file__,
                            sorted({r["seed"] for r in rows}), rid)
    print(json.dumps(doc["summary"]), flush=True)
    print("complete", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
