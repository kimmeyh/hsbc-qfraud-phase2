"""F104 (Sprint 27 Task B): the resolution gate on the real B2 and B4 pools.

The card's acceptance: the gate flags B2 and passes a pool built to be
resolvable. B2's frozen pools were never stored, so B2 is the F142 seeded
rebuild of `b2_42` (833 variables, ULB `full`, full-pair); B4 is
`b4_oilgas_42`, the pool F142 screened and sent. Each is built offline by
`run_dirac3s_verify.offline`, gated by `device_resolution.resolution_gate`,
and its Hamiltonian hash compared with the one F142 recorded on its paid
row, so the matrix gated here is shown to be the matrix that was sent.

Zero metered seconds: offline builds only. The full-pair build needs fork,
so run under WSL:

    /root/eqc-venv/bin/python experiments/phase2/src/f104_gate_check.py

Writes `experiments/phase2/results/f104_gate_check.json`.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_dirac3s_verify as R                       # noqa: E402

OUT = R.PHASE2_RESULTS / "f104_gate_check.json"
UNITS = ("b2_42", "b4_oilgas_42")
EXPECT = {"b2_42": False, "b4_oilgas_42": True}


def _paid_hashes() -> dict:
    """{unit: (sha256, source)}. A paid row carries its hash from the PR #21
    review on; the five F142 rows predate that, so their hash is the dry-run
    entry the runner screened before the call (`f142_dry_run.json`, which
    the F142 readout checks its rebuilds against)."""
    out = {}
    for stop in json.loads(R.DRY_RUN.read_text(
            encoding="utf-8"))["stops"].values():
        for u in stop["units"]:
            out[u["unit"]] = (u["hamiltonian_sha256"], R.DRY_RUN.name)
    for r in json.loads(R.RESULT.read_text(encoding="utf-8"))["rows"]:
        h = (r.get("screen") or {}).get("hamiltonian_sha256")
        if h:
            out[r["unit"]] = (h, f"{R.RESULT.name} row")
    return out


def main() -> int:
    paid = _paid_hashes()
    out = []
    for name in UNITS:
        u = next(x for x in R.UNITS if x["unit"] == name)
        t0 = time.perf_counter()
        s = R.offline(u)
        row = {"unit": name, "n_variables": s["n_variables"],
               "off_diagonal_spread_over_resolvable":
                   s["off_diagonal_spread_over_resolvable"],
               "linear_spread_over_resolvable":
                   s["linear_spread_over_resolvable"],
               "dynamic_range_db": s["dynamic_range_db"],
               "gate_pass": s["screen_pass"],
               "expected_pass": EXPECT[name],
               "as_expected": s["screen_pass"] is EXPECT[name],
               "hamiltonian_sha256": s["hamiltonian_sha256"],
               "sent_sha256": (paid.get(name) or (None, None))[0],
               "sent_sha256_source": (paid.get(name) or (None, None))[1],
               "same_matrix_as_sent": ((paid.get(name) or (None,))[0]
                                       == s["hamiltonian_sha256"]),
               "elapsed_s": round(time.perf_counter() - t0, 1)}
        out.append(row)
        print(json.dumps(row), flush=True)
    OUT.write_text(json.dumps({
        "generator": "experiments/phase2/src/f104_gate_check.py",
        "card": "F104", "sprint": 27, "phase": 2, "evidence_tag": "SIM",
        "metered_seconds": 0, "date": time.strftime("%Y-%m-%d"),
        "gate": "device_resolution.resolution_gate (A31: both spreads >= "
                "max |coefficient| / 200)",
        "python": sys.version.split()[0], "rows": out}, indent=1) + "\n",
        encoding="utf-8")
    return 0 if all(r["as_expected"] for r in out) else 1


if __name__ == "__main__":
    raise SystemExit(main())
