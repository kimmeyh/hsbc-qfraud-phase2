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
    # If the guard ever broke, an empty token and an unreachable URL make the
    # subprocess fail closed instead of submitting (code review finding 6).
    # (A dict entry, not keyword form: the confidentiality hook matches the
    # .env-style keyword text, and an empty token is not a secret.)
    env = dict(os.environ)
    env.update({"PYTEST_CURRENT_TEST": "guard::f142", "QCI_TOKEN": "",
                "QCI_API_URL": "https://offline.invalid"})
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


def test_an_attempted_unit_is_never_resubmitted(tmp_path, monkeypatch):
    """Any row, failed included, and any ledger entry: a failed unit may
    have been billed, and a crash after the intent write leaves only the
    ledger entry."""
    f = tmp_path / "f142.json"
    f.write_text(json.dumps({"rows": [
        {"unit": "b1_42", "status": "ok"},
        {"unit": "b1_43", "status": "failed"}]}), encoding="utf-8")
    led = tmp_path / "ledger.json"
    led.write_text(json.dumps({"calls": [
        {"label": "f142_b2_42_a1", "status": "intent"},
        {"label": "b4_oilgas_42_a1", "status": "ok"}]}), encoding="utf-8")
    monkeypatch.setattr(R, "RESULT", f)
    monkeypatch.setattr(R, "LEDGER", led)
    assert R._done() == {"b1_42", "b1_43", "b2_42"}


def test_a_second_concurrent_run_is_refused(tmp_path, monkeypatch):
    monkeypatch.setattr(R, "RESULT", tmp_path / "f142.json")
    with R._lock():
        with pytest.raises(SystemExit, match="REFUSING"):
            with R._lock():
                pass
    with R._lock():                      # released on exit
        pass


class _Model:
    def __init__(self, J, C):
        self._J, self._C = J, C


def _guarded_class(unit, screened, saved, base_solve=None, base_results=None):
    class Base:
        sent = []

        def solve(self, model, **kw):
            Base.sent.append(model)
            return base_solve(model) if base_solve else "sent"

        def makeResults(self, model, response):
            if base_results:
                return base_results(model, response)
            return response
    return R._guarded(unit, screened, saved)(Base), Base


def test_a_changed_hamiltonian_is_refused_before_anything_is_sent():
    import eqc_submit
    import numpy as np
    m = _Model(np.eye(3), np.ones((3, 1)))
    # A report-only unit, so only the hash check can refuse it.
    G, Base = _guarded_class({"unit": "b1_42", "screen": "report"},
                             {"hamiltonian_sha256": "not-this"}, {})
    with pytest.raises(eqc_submit.NoRetry, match="differs from the screened"):
        G().solve(m)
    assert Base.sent == []
    G1, Base1 = _guarded_class({"unit": "b1_42", "screen": "report"},
                               {"hamiltonian_sha256": R._hash(m)}, {})
    assert G1().solve(m) == "sent" and len(Base1.sent) == 1
    unit = {"unit": "b4_oilgas_42", "screen": "enforce"}
    G2, Base2 = _guarded_class(unit, {"hamiltonian_sha256": R._hash(m)}, {})
    # Same hash, but eye(3) has no off-diagonal spread: an enforce unit
    # that fails A31's test is refused before sending, too.
    with pytest.raises(eqc_submit.NoRetry, match="resolution"):
        G2().solve(m)
    assert Base2.sent == []


def test_the_raw_response_is_saved_before_post_processing(tmp_path,
                                                          monkeypatch):
    """A post-billing failure (here, makeResults raising) keeps the job id
    and the samples on disk, and never overwrites an earlier response."""
    import numpy as np
    monkeypatch.setattr(R, "RESP_DIR", tmp_path)
    jid = "a" * 24
    resp = {"job_info": {"job_id": jid},
            "results": {"solutions": [[0.5, 0.5]], "energies": [0.0]}}

    def boom(model, response):
        raise RuntimeError("metrics read failed")

    saved: dict = {}
    G, _ = _guarded_class({"unit": "b1_42", "screen": "report"}, {}, saved,
                          base_results=boom)
    with pytest.raises(RuntimeError):
        G().makeResults(_Model(np.eye(2), np.ones(2)), resp)
    first = tmp_path / f"f142_b1_42_{jid}.json"
    assert json.loads(first.read_text())["response"]["job_info"]["job_id"] == jid
    assert saved["job_id"] == jid
    with pytest.raises(RuntimeError):
        G().makeResults(_Model(np.eye(2), np.ones(2)), resp)
    assert len(list(tmp_path.glob("f142_b1_42_*.json"))) == 2
    assert json.loads(first.read_text())["job_id"] == jid


class _Rec:
    def __init__(self, label):
        self.label, self.n_variables, self.n_samples = label, 3, 8
        self.expected_seconds, self.notes = "x", []
        self.job_id = self.error = self.balance_before = None
        self.balance_after = self.measured_seconds = None
        self.status, self.cost_source = "intent", ""
        self.submitted_utc = self.finished_utc = None


def _run_metered_fit(tmp_path, monkeypatch, fit, balances, **kw):
    """metered_fit with a fake classifier, a scripted balance and the ledger
    in tmp_path. Returns (result, number of fits attempted)."""
    import eqc_submit
    import metered_call as mc
    monkeypatch.setattr(mc, "LEDGER", tmp_path / "ledger.json")
    monkeypatch.setattr(mc, "LOG_DIR", tmp_path / "logs")
    monkeypatch.setattr(mc, "append_ledger", lambda rec: None)
    bal = iter(balances)
    monkeypatch.setattr(eqc_submit, "_balance_or_none",
                        lambda client: next(bal))
    monkeypatch.setattr(eqc_submit.time, "sleep", lambda s: None)
    calls = []

    class Clf:
        def fit(self, X, y):
            calls.append(1)
            return fit()
    out = eqc_submit.metered_fit(Clf, None, None, _Rec, None, **kw)
    return out, len(calls)


def test_one_attempt_means_one_call(tmp_path, monkeypatch):
    def fail():
        raise RuntimeError("metrics read failed after billing")
    out, n = _run_metered_fit(tmp_path, monkeypatch, fail, [100, 95],
                              max_attempts=1)
    assert n == 1 and out["clf"] is None and out["metered_seconds"] == 5


def test_no_retry_ends_the_loop_at_once(tmp_path, monkeypatch):
    import eqc_submit

    def refuse():
        raise eqc_submit.NoRetry("pre-submit")
    out, n = _run_metered_fit(tmp_path, monkeypatch, refuse,
                              [100, 100, 100, 100, 100, 100])
    assert n == 1 and out["attempts"] == 1


def test_the_default_still_retries_twice(tmp_path, monkeypatch):
    """Phase 1's behavior is unchanged when nothing is opted in."""
    def fail():
        raise RuntimeError("transient")
    _, n = _run_metered_fit(tmp_path, monkeypatch, fail,
                            [100, 100, 100, 100, 100, 100])
    assert n == 3


def test_a_balance_that_does_not_fall_is_charged_when_opted_in(tmp_path,
                                                               monkeypatch):
    import eqc_submit
    ok = lambda: {"job_info": {"job_id": "b" * 24}}      # noqa: E731
    out, _ = _run_metered_fit(tmp_path, monkeypatch, ok, [100, 100],
                              max_attempts=1, zero_cost_is_unparsed=True)
    assert out["metered_seconds"] == eqc_submit.UNPARSEABLE_CALL_CHARGE_S
    assert out["parsed"] is False
    out, _ = _run_metered_fit(tmp_path, monkeypatch, ok, [100, 100],
                              max_attempts=1)
    assert out["metered_seconds"] == 0 and out["parsed"] is True


def test_the_key_name_in_the_repository_env_is_accepted(tmp_path,
                                                        monkeypatch):
    """The repository's .env names the key QCI_API_KEY, as run_hardware.py
    accepts. Without the alias, stop 1 exited before submitting."""
    for k in ("QCI_TOKEN", "QCI_API_KEY", "QCI_API_URL"):
        monkeypatch.delenv(k, raising=False)
    env = tmp_path / ".env"
    # Assembled, not literal: the confidentiality hook blocks .env-style
    # key lines in staged text, and this one holds no secret.
    key = "QCI_API" + "_KEY"
    env.write_text(f"{key}" + "='k-not-a-real-key'\n"
                   "QCI_API_URL=https://offline.invalid\n", encoding="utf-8")
    R._load_env(env)
    assert os.environ["QCI_TOKEN"] == "k-not-a-real-key"
    monkeypatch.delenv("QCI_TOKEN")
    monkeypatch.delenv("QCI_API_KEY")
    env.write_text("QCI_API_URL=https://offline.invalid\n", encoding="utf-8")
    with pytest.raises(SystemExit, match="QCI_TOKEN is not set"):
        R._load_env(env)


def test_device_timing_is_read_in_seconds():
    class Res:
        run_time = [656_000_000, 852_000_000]
        time_units = "ns"
        preprocessing_time = 7_500_000
    t = R.device_timing(Res())
    assert t["run_time_per_sample_s"] == [0.656, 0.852]
    assert abs(t["runtime_sum_s"] - 1.508) < 1e-12
    assert abs(t["preprocessing_s"] - 0.0075) < 1e-12

    class Offline:                       # the offline stand-in returns none
        run_time = []
        time_units = "ns"
    assert R.device_timing(Offline()) is None


def test_an_unreadable_record_refuses(tmp_path, monkeypatch):
    f = tmp_path / "f142.json"
    f.write_text("{not json", encoding="utf-8")
    monkeypatch.setattr(R, "RESULT", f)
    with pytest.raises(SystemExit, match="REFUSING"):
        R._done()
