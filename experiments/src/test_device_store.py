"""device_store: refusals before sending, and the save before scoring.

Offline only: the "solver" here is a local class with the eqc-models
`solve` / `makeResults` shape. Nothing reaches a device.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "src"))
import device_store as ds  # noqa: E402
import eqc_submit  # noqa: E402

J = np.array([[2.0, 0.5], [0.5, 1.0]])
C = np.array([-1.0, -0.5])
HASH = ds.problem_sha256((J, C))
POOL = {"kind": "cvqboost_pool", "weak_cls_type": "dct",
        "weak_cls_params": {"max_depth": 1, "random_state": 42},
        "seed": 42, "data": "spectra_oilgas_gasturbine target, house split"}


class Model:
    def __init__(self, J, C):
        self._J, self._C = J, C


class FakeSolver:
    sent = 0

    def solve(self, model, **kw):
        FakeSolver.sent += 1
        return self.makeResults(model, {"job_info": {"job_id": "abc123"},
                                        "results": {"solutions": [[0.5, 0.5]]}})

    def makeResults(self, model, response):
        return {"made": True}


def test_refuses_a_malformed_hash():
    with pytest.raises(ValueError, match="SHA-256"):
        ds.saving("F999", "u1", "dirac-3s", "not-a-hash", POOL)


def test_refuses_an_unseeded_tree_pool():
    pool = {**POOL, "weak_cls_params": {"max_depth": 1}}
    with pytest.raises(ValueError, match="unseeded pool"):
        ds.saving("F999", "u1", "dirac-3s", HASH, pool)


def test_knn_pool_needs_no_random_state():
    pool = {**POOL, "weak_cls_type": "knn", "weak_cls_params": {"n_neighbors": 15}}
    ds.saving("F999", "u1", "dirac-3s", HASH, pool)


def test_pool_needs_its_seed_and_data():
    for key in ("seed", "data"):
        with pytest.raises(ValueError, match=key):
            ds.saving("F999", "u1", "dirac-3s", HASH, {**POOL, key: None})


def test_hamiltonian_needs_its_arrays_and_they_must_match():
    with pytest.raises(ValueError, match="arrays"):
        ds.saving("F999", "u1", "dirac-3s", HASH, {"kind": "hamiltonian"})
    with pytest.raises(ValueError, match="do not hash"):
        ds.saving("F999", "u1", "dirac-3s", HASH,
                  {"kind": "hamiltonian", "arrays": (J * 2, C)})


def test_a_different_model_is_refused_before_sending(tmp_path):
    wrap, saved = ds.saving("F999", "u1", "dirac-3s", HASH, POOL, tmp_path)
    before = FakeSolver.sent
    with pytest.raises(eqc_submit.NoRetry, match="nothing sent"):
        wrap(FakeSolver)().solve(Model(J * 2, C))
    assert FakeSolver.sent == before and not saved
    with pytest.raises(RuntimeError, match="not stored"):
        ds.require_saved(saved)


def test_the_full_response_is_stored_before_it_is_returned(tmp_path):
    wrap, saved = ds.saving("F999", "u1", "dirac-3s", HASH, POOL, tmp_path)
    out = wrap(FakeSolver)().solve(Model(J, C))
    assert out == {"made": True}
    path = ds.require_saved(saved)
    doc = json.loads(path.read_text(encoding="utf-8"))
    assert doc["job_id"] == "abc123" and doc["problem_sha256"] == HASH
    assert doc["problem"]["weak_cls_params"]["random_state"] == 42
    assert doc["response"]["results"]["solutions"] == [[0.5, 0.5]]


def test_a_hamiltonian_job_stores_its_arrays(tmp_path):
    prob = {"kind": "hamiltonian", "arrays": (J, C)}
    wrap, saved = ds.saving("F999", "u2", "dirac-3s", HASH, prob, tmp_path)
    wrap(FakeSolver)().solve(Model(J, C))
    doc = json.loads(ds.require_saved(saved).read_text(encoding="utf-8"))
    back = np.load(tmp_path / doc["arrays_file"])
    assert ds.problem_sha256((back["arr_0"], back["arr_1"])) == HASH
    assert "arrays" not in doc["problem"]


# F168 part 3 (Sprint 30): a resume never repeats a metered call.

class StoppedSolver(FakeSolver):
    """Sends, then the process stops before the job returns."""

    def solve(self, model, **kw):
        FakeSolver.sent += 1
        raise KeyboardInterrupt("stopped before the response returned")


def test_a_job_whose_process_stopped_is_not_sent_again(tmp_path):
    wrap, saved = ds.saving("F999", "u1", "dirac-3s", HASH, POOL, tmp_path)
    with pytest.raises(KeyboardInterrupt):
        wrap(StoppedSolver)().solve(Model(J, C))
    assert not saved, "no response was saved"
    found = ds.lookup(HASH, tmp_path)
    assert found["responses"] == [] and len(found["intents"]) == 1
    with pytest.raises(ValueError, match="already sent"):
        ds.saving("F999", "u1", "dirac-3s", HASH, POOL, tmp_path)


def test_a_job_with_a_saved_response_is_not_sent_again(tmp_path):
    wrap, _ = ds.saving("F999", "u1", "dirac-3s", HASH, POOL, tmp_path)
    wrap(FakeSolver)().solve(Model(J, C))
    for p in (tmp_path / ds.INTENTS).glob("*.json"):
        p.unlink()                      # the response alone must refuse
    assert len(ds.lookup(HASH, tmp_path)["responses"]) == 1
    with pytest.raises(ValueError, match="already sent"):
        ds.saving("F999", "u2", "dirac-3s", HASH, POOL, tmp_path)


def test_a_new_problem_is_not_refused(tmp_path):
    wrap, _ = ds.saving("F999", "u1", "dirac-3s", HASH, POOL, tmp_path)
    wrap(FakeSolver)().solve(Model(J, C))
    other = ds.problem_sha256((J * 3, C))
    ds.saving("F999", "u3", "dirac-3s", other, POOL, tmp_path)


def test_files_without_a_hash_are_listed_not_matched(tmp_path):
    (tmp_path / "b4_backfill_42.json").write_text(
        json.dumps({"job_id": "x", "response": {}}), encoding="utf-8")
    assert ds.lookup(HASH, tmp_path) == {"responses": [], "intents": [],
                                         "unreadable": []}
    assert [p.name for p in ds.unhashed(tmp_path)] == ["b4_backfill_42.json"]


def test_an_unreadable_response_file_refuses_the_send(tmp_path):
    # PR 74 review: lookup skipped a corrupt file that may be this
    # problem's response, so the send passed.
    (tmp_path / "f999_u1_job.json").write_text("{trunc", encoding="utf-8")
    with pytest.raises(ValueError, match="unreadable response files"):
        ds.saving("F999", "u1", "dirac-3s", HASH, POOL, tmp_path)


def test_the_resend_refusal_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    src = ROOT / "experiments" / "phase2" / "src" / "device_store.py"
    this = Path(__file__).relative_to(ROOT).as_posix()

    def test(name):
        return lambda: run_pytest(f"{this}::{name}", ROOT)
    assert_can_fail([Mutation(src, '    if found["responses"] or '
                              'found["intents"]:\n', "    if False:\n",
                              expect_occurrences=1)],
                    test("test_a_job_with_a_saved_response_is_not_sent_"
                         "again"),
                    "a saved response sent again")
    assert_can_fail([Mutation(src, '    if found["responses"] or '
                              'found["intents"]:\n',
                              '    if found["responses"]:\n',
                              expect_occurrences=1)],
                    test("test_a_job_whose_process_stopped_is_not_sent_"
                         "again"),
                    "an intent with no response ignored")
    assert_can_fail([Mutation(src, "                _store(intent, {",
                              "                (intent, {",
                              expect_occurrences=1)],
                    test("test_a_job_whose_process_stopped_is_not_sent_"
                         "again"),
                    "no intent written before the send")
    assert_can_fail([Mutation(src, '    if found["unreadable"]:\n',
                              "    if False:\n", expect_occurrences=1)],
                    test("test_an_unreadable_response_file_refuses_the_"
                         "send"),
                    "an unreadable response file skipped")
