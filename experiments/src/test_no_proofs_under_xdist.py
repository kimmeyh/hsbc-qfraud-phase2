"""Red proofs never run inside an xdist worker (Sprint 31 Task N, #106).

A proof mutates a tracked file and restores it from the bytes it read
first. Under `pytest -n 4` two proofs on one learning document interleaved:
the second read the first's mutation as the original and restored it, and
the mutated figure was committed in dfb1694. CI's push job caught it. The
root `conftest.py` now fails a proof at setup in a worker, before its body
runs; a parallel run with `-m "not proof"` is unchanged.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
THIS = Path(__file__).relative_to(ROOT).as_posix()
TARGET = "experiments/src/test_suite_times.py"   # three tests, one proof
sys.path.insert(0, str(Path(__file__).resolve().parent))


def _pytest(*args: str) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items()
           if not k.startswith("PYTEST_XDIST")}
    return subprocess.run([sys.executable, "-m", "pytest", TARGET, "-q",
                           "-p", "no:cacheprovider", *args],
                          cwd=ROOT, env=env, capture_output=True, text=True,
                          timeout=300)


def test_a_proof_in_a_worker_is_refused_and_the_rest_runs():
    out = _pytest("-n", "2")
    assert out.returncode != 0
    assert "red proof refused inside xdist worker" in out.stdout
    assert "3 passed, 1 error" in out.stdout


def test_a_parallel_run_without_proofs_is_unchanged():
    out = _pytest("-n", "2", "-m", "not proof")
    assert out.returncode == 0, out.stdout[-2000:]


def test_the_refusal_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    assert_can_fail(
        [Mutation(ROOT / "conftest.py",
                  "    if worker and item.get_closest_marker(\"proof\"):",
                  "    if False:", expect_occurrences=1)],
        lambda: run_pytest(f"{THIS}::test_a_proof_in_a_worker_is_refused_"
                           "and_the_rest_runs", ROOT),
        "a proof run inside an xdist worker")
