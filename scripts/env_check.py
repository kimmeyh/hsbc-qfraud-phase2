"""Time this workstation's process costs before a long run (F177 change f,
Sprint 31 D8).

    <venv python> scripts/env_check.py          print the timings
    <venv python> scripts/env_check.py --json   the same as JSON

Each measurement runs in a fresh Python process, as a test's subprocess
does, and is printed beside the idle range F180 measured on 2026-11-05
(`docs/testing/F180_TESTING_ANALYSIS.md`, "How this was measured"). A
measurement above its range's top is marked SLOW, so a slow machine is
seen before a run, not during it. Exit 0 always: this reports, it does
not gate.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# name: (code run in a fresh interpreter, idle range in seconds, 2026-11-05)
CHECKS = {
    "python start": ("pass", (0.6, 0.7)),
    "import numpy, pandas, sklearn": ("import numpy, pandas, sklearn",
                                      (18.0, 22.0)),
}
STAT_FILES = 200
STAT_IDLE_MS = (3.0, 9.0)


def fresh(code: str) -> float:
    t0 = time.perf_counter()
    subprocess.run([sys.executable, "-c", code], check=True,
                   capture_output=True)
    return time.perf_counter() - t0


def stat_ms(n: int = STAT_FILES) -> float:
    files = sorted(ROOT.glob("experiments/**/*.py"))[:n]
    if not files:
        raise SystemExit(f"no .py files under {ROOT / 'experiments'}")
    t0 = time.perf_counter()
    for f in files:
        f.stat()
    return (time.perf_counter() - t0) * 1000 / len(files)


def verdict(value: float, idle: tuple[float, float]) -> str:
    return "SLOW" if value > idle[1] else "ok"


def measure() -> list[dict]:
    rows = []
    for name, (code, idle) in CHECKS.items():
        v = fresh(code)
        rows.append({"check": name, "seconds": round(v, 2), "idle": idle,
                     "verdict": verdict(v, idle)})
    v = stat_ms()
    rows.append({"check": f"os.stat per file ({STAT_FILES} files), ms",
                 "seconds": round(v, 2), "idle": STAT_IDLE_MS,
                 "verdict": verdict(v, STAT_IDLE_MS)})
    return rows


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", action="store_true")
    as_json = ap.parse_args(argv).json
    rows = measure()
    if as_json:
        print(json.dumps(rows, indent=1))
        return 0
    for r in rows:
        lo, hi = r["idle"]
        print(f"{r['verdict']:4s}  {r['check']}: {r['seconds']} "
              f"(idle {lo}-{hi} on 2026-11-05)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
