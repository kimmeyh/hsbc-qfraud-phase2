"""F155 and F95's Dirac-3S runner sends only what its entries name, and
never pays twice (Sprint 31 Tasks I and J, #101 #102).

Nothing here sends: the stop loop runs with a stub fit, a stub client and
a stub balance (the F149 pattern), and the record, the ledger and the
store live in tmp_path.
"""
from __future__ import annotations

import importlib
import json
import shutil
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "experiments" / "phase2" / "src" / "run_dirac3s_units.py"
sys.path.insert(0, str(RUNNER.parent))
import run_dirac3s_units as R  # noqa: E402
import device_store  # noqa: E402
import eqc_submit  # noqa: E402


def _unit(card, name):
    return next(u for u in R.CARDS[card]["units"] if u["unit"] == name)


def test_the_units_are_the_entries():
    f155 = R.CARDS["F155"]["units"]
    assert [u["unit"] for u in f155] == ["pool_1350"]
    u = f155[0]
    assert R.n_variables(u["k"], u["order"]) == 1350
    assert (u["relaxation_schedule"], u["num_samples"]) == (2, 1)
    f95 = R.CARDS["F95"]["units"]
    assert [(u["unit"], u["stop"]) for u in f95] == [
        ("b1_dct_42", 1), ("b1_dct_43", 2), ("g0b_3_42", 2),
        ("b1_lg_42", 2)]
    assert {R.n_variables(u["k"], u["order"]) for u in f95[:2]} == {91}
    assert {R.n_variables(u["k"], u["order"]) for u in f95[2:]} == {45}
    assert all(u["relaxation_schedule"] == 4 for u in f95)
    assert [u["alpha"] for u in f95] == [2.0, 2.0, 4.0, 0.5]
    assert R.CARDS["F95"]["cap_s"] == 120.0


def test_a_pool_size_is_singles_pairs_and_triples():
    assert R.n_variables(19, 3) == 1159
    assert R.n_variables(17, 3) == 833
    assert R.n_variables(13, 1) == 13


def test_every_unit_goes_to_dirac3s():
    assert R.DEVICE == eqc_submit.PHASE2_DEVICE == eqc_submit.DIRAC_3S


def test_the_pool_is_seeded_and_lambda_scales_with_the_rows():
    u = _unit("F95", "g0b_3_42")
    cfg = R.config(u, 1000)
    assert cfg["lambda_coef"] == 4000.0
    assert cfg["weak_cls_params"] == {**R.LG, "random_state": 42}
    assert cfg["relaxation_schedule"] == 4
    decl = R.declaration(u, cfg, ["V1"])
    device_store.check_problem(decl)            # the store accepts it


def test_the_gap_is_relative_to_the_reference_optimum():
    J = np.eye(2)
    C = np.array([-1.0, -1.0])
    ref = [0.5, 0.5]                              # obj = 0.5 - 1 = -0.5
    g = R.gaps(J, C, ref, [[0.5, 0.5], [1.0, 0.0]])
    assert g["objective_reference"] == -0.5
    assert g["per_sample_gap"] == [0.0, 1.0]     # (0 - -0.5) / 0.5
    assert g["gap_min"] == 0.0 and g["gap_range"] == 1.0


def test_the_runner_refuses_when_invoked_from_a_test():
    assert R.main(["--card", "F155", "--stop", "1"]) == 5


def test_an_unknown_stop_is_refused():
    assert R.main(["--card", "F155", "--stop", "2", "--dry-run"]) == 2


def _paths(tmp_path, monkeypatch):
    for card in R.CARDS:
        monkeypatch.setitem(R.CARDS[card], "result",
                            tmp_path / f"{card.lower()}.json")
    monkeypatch.setattr(R.v, "LEDGER", tmp_path / "ledger.json")
    monkeypatch.setattr(device_store, "STORE_DIR", tmp_path / "store")


def test_a_unit_with_any_record_is_done(tmp_path, monkeypatch):
    _paths(tmp_path, monkeypatch)
    assert R.done("F95") == set()
    R.v.LEDGER.write_text(json.dumps({"calls": [
        {"label": "f95_b1_dct_42_a1", "status": "intent"},
        {"label": "f142_b1_42_a1", "status": "ok"}]}), encoding="utf-8")
    intents = device_store.STORE_DIR / device_store.INTENTS
    intents.mkdir(parents=True)
    (intents / f"{'a' * 64}_f95_g0b_3_42.json").write_text("{}",
                                                           encoding="utf-8")
    assert R.done("F95") == {"b1_dct_42", "g0b_3_42"}
    assert R.done("F155") == set()


def test_an_unreadable_ledger_refuses(tmp_path, monkeypatch):
    _paths(tmp_path, monkeypatch)
    R.v.LEDGER.write_text("{not json", encoding="utf-8")
    try:
        R.done("F95")
    except SystemExit as exc:
        assert "unreadable" in str(exc)
    else:
        raise AssertionError("an unreadable ledger was read as empty")


def _stop(tmp_path, monkeypatch, card, stop, results=None, balance=100.0,
          ledger=()):
    """`run_stop` with a stub fit returning `results[unit]` (status,
    seconds). Returns (exit code, units fitted, clients made)."""
    _paths(tmp_path, monkeypatch)
    if ledger:
        R.v.LEDGER.write_text(json.dumps({"calls": list(ledger)}),
                              encoding="utf-8")
    todo = [u for u in R.CARDS[card]["units"] if u["stop"] == stop]
    screened = {u["unit"]: {} for u in todo}
    fitted, clients = [], []

    def fit(c, u, s, client, on_submitted):
        fitted.append(u["unit"])
        status, secs = (results or {}).get(u["unit"], ("ok", 5.0))
        row = {"unit": u["unit"], "stop": stop, "status": status,
               "metered_seconds": secs}
        on_submitted(row)
        return row
    rc = R.run_stop(card, stop, todo, screened,
                    make_client=lambda: clients.append(1) or "client",
                    fit=fit, balance=lambda client: balance)
    return rc, fitted, len(clients)


def test_the_stop_fits_each_unit_once_and_records_it(tmp_path, monkeypatch):
    rc, fitted, _ = _stop(tmp_path, monkeypatch, "F95", 2)
    assert rc == 0 and fitted == ["b1_dct_43", "g0b_3_42", "b1_lg_42"]
    doc = json.loads(R.CARDS["F95"]["result"].read_text(encoding="utf-8"))
    assert [r["unit"] for r in doc["rows"]] == fitted
    assert doc["provenance"]["run_id"] and doc["complete"] is False


def test_an_unreadable_balance_sends_nothing(tmp_path, monkeypatch):
    rc, fitted, _ = _stop(tmp_path, monkeypatch, "F155", 1, balance=None)
    assert (rc, fitted) == (4, [])


def _ledger_skips(tmp_path, monkeypatch) -> bool:
    """A unit that gained a ledger entry after the todo list was made is
    never sent."""
    rc, fitted, _ = _stop(tmp_path, monkeypatch, "F95", 2, ledger=[
        {"label": "f95_g0b_3_42_a1", "status": "intent"}])
    return rc == 0 and fitted == ["b1_dct_43", "b1_lg_42"]


def test_a_unit_with_a_ledger_entry_is_not_sent(tmp_path, monkeypatch):
    assert _ledger_skips(tmp_path, monkeypatch)


def _cap_stops(tmp_path, monkeypatch) -> bool:
    rc, fitted, _ = _stop(tmp_path, monkeypatch, "F95", 2,
                          results={"b1_dct_43": ("ok", 120.0)})
    return fitted == ["b1_dct_43"]


def test_the_cap_ends_the_stop(tmp_path, monkeypatch):
    assert _cap_stops(tmp_path, monkeypatch)


def _failed_stops(tmp_path, monkeypatch) -> bool:
    rc, fitted, _ = _stop(tmp_path, monkeypatch, "F95", 2,
                          results={"b1_dct_43": ("failed", 3.0)})
    return rc == 1 and fitted == ["b1_dct_43"]


def test_a_failed_unit_ends_the_stop_and_exits_nonzero(tmp_path,
                                                       monkeypatch):
    assert _failed_stops(tmp_path, monkeypatch)


def test_a_rejected_job_reads_its_stored_length(tmp_path):
    p = tmp_path / "r.json"
    p.write_text(json.dumps({"response": {"results": {
        "solutions": [[0.1] * 949]}}}), encoding="utf-8")
    assert R._returned_length({"path": p}, 1350) == {
        "returned_length": 949, "accepted": False}
    assert R._returned_length({}, 1350) == {"returned_length": None,
                                            "accepted": False}


def test_the_runner_can_fail(tmp_path, monkeypatch):
    from injection import Mutation, assert_can_fail
    src = Path(R.__file__)

    def run(check):
        def go() -> bool:
            importlib.reload(R)
            for f in tmp_path.iterdir():
                shutil.rmtree(f) if f.is_dir() else f.unlink()
            return check(tmp_path, monkeypatch)
        return go

    try:
        assert_can_fail([Mutation(src, 'if u["unit"] in done(card):',
                                  "if False:", expect_occurrences=1)],
                        run(_ledger_skips),
                        "a unit sent despite a ledger entry")
        assert_can_fail([Mutation(src, "            if spent >= cap:\n",
                                  "            if False:\n",
                                  expect_occurrences=1)],
                        run(_cap_stops), "the cap not applied")
        assert_can_fail([Mutation(src, '            if row["status"] == '
                                  '"failed":\n',
                                  "            if False:\n",
                                  expect_occurrences=1)],
                        run(_failed_stops), "a failed unit not ending the stop")
    finally:
        importlib.reload(R)


# F95's preregistered reading against each twin (Sprint 31 Phase 5,
# fresh-eyes finding 1.1: `twin_gaps` existed and nothing called it).

def _row(gmin, grange, unit="u"):
    return {"unit": unit, "gap_min": gmin, "gap_range": grange}


def test_the_reading_changes_only_beyond_the_twin_range():
    twin = _row(1.0e-8, 5.0e-8)
    assert R.twin_reading(_row(3.0e-8, 1e-8), twin)["changes_reading"] is False
    assert R.twin_reading(_row(5.0e-8, 1e-8), twin)["changes_reading"] is False
    assert R.twin_reading(_row(7.0e-8, 1e-8), twin)["changes_reading"] is True
    assert R.twin_reading(_row(-5.0e-8, 1e-8), twin)["changes_reading"] is True


def test_a_twin_without_per_sample_gaps_is_refused():
    import pytest
    with pytest.raises(ValueError, match="twin has no per-sample gaps"):
        R.twin_reading(_row(1e-8, 1e-8), _row(None, None))
    with pytest.raises(ValueError, match="schedule-4 row has no"):
        R.twin_reading(_row(1e-8, None), _row(1e-8, 1e-8))


def test_the_dirac3_history_needs_exactly_one_row(tmp_path, monkeypatch):
    import pytest
    hw = tmp_path / "hw_dispersion.json"
    hw.write_text(json.dumps({"per_fit": [
        {"file": "a.json", "relaxation_schedule": 2, "gap_to_exact_pct": 0.4},
        {"file": "b.json", "relaxation_schedule": 2, "gap_to_exact_pct": 0.1},
        {"file": "b.json", "relaxation_schedule": 2, "gap_to_exact_pct": 0.2}]}),
        encoding="utf-8")
    monkeypatch.setattr(R, "HW_DISPERSION", hw)
    assert R.dirac3_history("a.json")["gap_to_exact_pct"] == 0.4
    for name in ("b.json", "c.json"):
        with pytest.raises(ValueError, match="rows in hw_dispersion"):
            R.dirac3_history(name)


def test_twins_is_f95_only_and_stop_is_needed_otherwise():
    import pytest
    assert R.main(["--card", "F155", "--twins"]) == 2
    with pytest.raises(SystemExit):
        R.main(["--card", "F95"])


def test_twins_writes_its_own_file_and_reads_the_result(tmp_path, monkeypatch):
    rows = [{"unit": "x", "twin": "f142:t", "gap_min": 2e-8, "gap_range": 1e-8,
             "screen": {"screen_pass": False}, "job_id": "jx",
             "device_type": "dirac-3s"},
            {"unit": "y", "twin": "dirac-3:hist", "gap_min": 1e-8,
             "gap_range": 1e-8, "screen": {"screen_pass": True},
             "job_id": "jy", "device_type": "dirac-3s"}]
    first = tmp_path / "f95_schedule4.json"
    first.write_text(json.dumps({"rows": rows}), encoding="utf-8")
    before = first.read_bytes()
    hw = tmp_path / "hw.json"
    hw.write_text(json.dumps({"per_fit": [{"file": "hist.json",
                  "relaxation_schedule": 2, "gap_to_exact_pct": 0.4}]}),
                  encoding="utf-8")
    monkeypatch.setitem(R.CARDS["F95"], "result", first)
    monkeypatch.setattr(R, "TWINS_RESULT", tmp_path / "twins.json")
    monkeypatch.setattr(R, "HW_DISPERSION", hw)
    path = R.twins(read_twin=lambda name: _row(1e-8, 5e-8))
    doc = json.loads(path.read_text(encoding="utf-8"))
    assert first.read_bytes() == before
    assert doc["metered_seconds"] == 0 and "provenance" in doc
    x, y = doc["rows"]
    assert x["reading"]["changes_reading"] is False
    assert y["dirac3_history"]["gap_to_exact_pct"] == 0.4
    assert isinstance(y["reading"], str)
    # Task N: each row names its job and device (B2, F141).
    assert [(r["job_id"], r["device_type"]) for r in doc["rows"]] == [
        ("jx", "dirac-3s"), ("jy", "dirac-3s")]
    # A recorded file is replaced only with a stated reason, recorded.
    with pytest.raises(FileExistsError):
        R.twins(read_twin=lambda name: _row(1e-8, 5e-8))
    R.twins(read_twin=lambda name: _row(1e-8, 5e-8), replace="test reason")
    again = json.loads(path.read_text(encoding="utf-8"))
    assert again["provenance"]["replaces"]["reason"] == "test reason"


def test_the_twin_reading_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    src = Path(R.__file__)
    me = "experiments/src/test_run_dirac3s_units.py::"
    for old, new, test, label in (
            ('"changes_reading": abs(diff) > twin["gap_range"]}',
             '"changes_reading": abs(diff) >= 0}',
             "test_the_reading_changes_only_beyond_the_twin_range",
             "a change read inside the twin's range"),
            ('        if d.get("gap_min") is None or d.get("gap_range") is None:\n',
             "        if False:\n",
             "test_a_twin_without_per_sample_gaps_is_refused",
             "a comparison made with no per-sample gaps"),
            ("    if len(hit) != 1:\n", "    if not hit:\n",
             "test_the_dirac3_history_needs_exactly_one_row",
             "an ambiguous Dirac-3 history row used"),
            ('        rec = {"unit": r["unit"], "job_id": r["job_id"],\n'
             '               "device_type": r["device_type"], "twin":',
             '        rec = {"unit": r["unit"], "twin":',
             "test_twins_writes_its_own_file_and_reads_the_result",
             "a twins row with no job id or device"),
            ("                            run_id, replace=replace)",
             "                            run_id)",
             "test_twins_writes_its_own_file_and_reads_the_result",
             "the stated replacement not passed to the writer"),
            ('        if args.card != "F95":\n', "        if False:\n",
             "test_twins_is_f95_only_and_stop_is_needed_otherwise",
             "--twins run for a card with no twins")):
        assert_can_fail([Mutation(src, old, new, expect_occurrences=1)],
                        lambda test=test: run_pytest(me + test, ROOT), label)


# Sprint 31 D16 option 1: each changed refusal has a test and a proof.

def test_an_unreadable_result_refuses(tmp_path, monkeypatch):
    import pytest
    _paths(tmp_path, monkeypatch)
    R.CARDS["F95"]["result"].write_text("{not json", encoding="utf-8")
    with pytest.raises(SystemExit, match="is unreadable"):
        R.done("F95")


def test_a_held_lock_refuses_and_is_left_alone(tmp_path, monkeypatch):
    import pytest
    _paths(tmp_path, monkeypatch)
    lock = R.CARDS["F95"]["result"].with_suffix(".lock")
    lock.write_text("1", encoding="utf-8")
    with pytest.raises(SystemExit, match="exists; another F95 run"):
        with R._lock("F95"):
            pass
    assert lock.read_text(encoding="utf-8") == "1"


def test_a_rebuilt_pool_with_another_hash_is_refused(tmp_path, monkeypatch):
    import contextlib
    import pytest
    res = tmp_path / "f142.json"
    res.write_text(json.dumps({"rows": [{"unit": "t", "all_samples": "x"}]}),
                   encoding="utf-8")
    dry = tmp_path / "dry.json"
    dry.write_text(json.dumps({"stops": {"1": {"units": [
        {"unit": "t", "hamiltonian_sha256": "a" * 64}]}}}), encoding="utf-8")
    monkeypatch.setattr(R, "F142_RESULT", res)
    monkeypatch.setattr(R, "F142_DRY_RUN", dry)
    monkeypatch.setattr(R.v, "UNITS", [{"unit": "t"}])
    monkeypatch.setattr(R.v, "_data", lambda u: (None,) * 8)

    class Clf:
        def fit(self, X, y):
            pass
    monkeypatch.setattr(R.v, "_make_clf", lambda cfg, extra: Clf())
    monkeypatch.setattr(R.eqc_submit, "offline_solver",
                        lambda sent, device_type=None: contextlib.nullcontext())
    monkeypatch.setattr(R.device_store, "problem_arrays", lambda clf: None)
    monkeypatch.setattr(R.device_store, "problem_sha256", lambda a: "b" * 64)
    with pytest.raises(RuntimeError, match="hash differs"):
        R.twin_gaps("t")


def test_the_d16_refusals_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    src = Path(R.__file__)
    me = "experiments/src/test_run_dirac3s_units.py::"
    for old, new, test, label in (
            ('        return json.loads(path.read_text(encoding="utf-8"))["rows"]\n',
             "        return []\n",
             "test_an_unreadable_result_refuses",
             "an unreadable result read as empty"),
            ("os.O_CREAT | os.O_EXCL | os.O_WRONLY", "os.O_CREAT | os.O_WRONLY",
             "test_a_held_lock_refuses_and_is_left_alone",
             "a held lock taken over"),
            ("    if sha != hashes[f142_unit]:\n", "    if False:\n",
             "test_a_rebuilt_pool_with_another_hash_is_refused",
             "samples read against a different pool")):
        assert_can_fail([Mutation(src, old, new, expect_occurrences=1)],
                        lambda test=test: run_pytest(me + test, ROOT), label)
