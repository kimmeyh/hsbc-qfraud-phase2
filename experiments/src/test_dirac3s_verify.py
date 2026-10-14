"""F142 (Sprint 26 Task D): the Dirac-3S verify runner, without a device.

No test here submits anything. The one subprocess run carries the pytest
marker, so the runner must refuse before touching data or a client
(`test_metered_runners_refuse_in_tests.py`, Sprint 21).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "experiments" / "phase2" / "src" / "run_dirac3s_verify.py"
sys.path.insert(0, str(RUNNER.parent))
import run_dirac3s_verify as R  # noqa: E402

PHASE2 = ROOT / "experiments" / "phase2" / "results"


def test_the_runner_refuses_when_invoked_from_a_test():
    env = dict(os.environ, PYTEST_CURRENT_TEST="guard::f142")
    r = subprocess.run([sys.executable, str(RUNNER), "--stop", "1"],
                       capture_output=True, text=True, cwd=str(ROOT),
                       env=env, timeout=600)
    assert "REFUSING" in r.stdout and "test process" in r.stdout, r.stdout
    assert r.returncode == 5


def test_every_output_path_is_phase_2():
    for p in (R.RESULT, R.LEDGER, R.LOG_DIR, R.RESP_DIR):
        assert PHASE2 in p.resolve().parents or p.resolve() == PHASE2, p


def test_the_ledger_is_redirected_and_restored():
    import metered_call as mc
    before = (mc.LEDGER, mc.LOG_DIR)
    with R._phase2_ledger():
        assert (mc.LEDGER, mc.LOG_DIR) == (R.LEDGER, R.LOG_DIR)
    assert (mc.LEDGER, mc.LOG_DIR) == before


def test_the_stops_match_the_plan():
    by_stop = {s: [u["unit"] for u in R.UNITS if u["stop"] == s]
               for s in R.STOP_CAP_S}
    assert by_stop == {1: ["b1_42"], 2: ["b1_43", "b2_42"],
                       3: ["b4_oilgas_42", "b4_oilgas_43"]}
    assert R.STOP_CAP_S == {1: 60.0, 2: 150.0, 3: 150.0}
    assert {u["unit"] for u in R.UNITS if u["screen"] == "enforce"} == {
        "b4_oilgas_42", "b4_oilgas_43"}
    assert R.DEVICE == "dirac-3s"


def test_the_screen_is_a31s_spread_test_not_the_dynamic_range():
    """A CVQBoost-shaped Hamiltonian: large, nearly equal off-diagonals. Its
    max/min ratio is tiny (well under 23 dB), yet no difference is visible
    at 1/200 of the largest term -- B1's case under A31. The screen must
    fail it, and pass the same matrix with a real spread."""
    import numpy as np
    n = 20
    rng = np.random.default_rng(0)
    off = 1000.0 + rng.uniform(0, 1.0, size=(n, n))
    J = (off + off.T) / 2
    np.fill_diagonal(J, 3000.0)
    C = -2.0 * (100.0 + rng.uniform(0, 1.0, size=n))
    assert 10 * np.log10(np.abs(J).max() / np.abs(C).min()) < 23.0
    assert not R.resolution_screen(J, C)["pass"]

    spread = J + np.triu(rng.uniform(0, 500, size=(n, n)), 1)
    spread = np.triu(spread, 1) + np.triu(spread, 1).T
    np.fill_diagonal(spread, 3000.0)
    C2 = -2.0 * rng.uniform(0, 500, size=n)
    assert R.resolution_screen(spread, C2)["pass"]


def test_a_done_unit_is_never_resubmitted(tmp_path, monkeypatch):
    f = tmp_path / "f142.json"
    f.write_text(json.dumps({"rows": [
        {"unit": "b1_42", "status": "ok"},
        {"unit": "b1_43", "status": "failed"}]}), encoding="utf-8")
    monkeypatch.setattr(R, "RESULT", f)
    assert R._done() == {"b1_42"}


def test_an_unreadable_record_refuses(tmp_path, monkeypatch):
    f = tmp_path / "f142.json"
    f.write_text("{not json", encoding="utf-8")
    monkeypatch.setattr(R, "RESULT", f)
    with pytest.raises(SystemExit, match="REFUSING"):
        R._done()
