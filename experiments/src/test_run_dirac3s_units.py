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
