"""Device responses are saved IN FULL, and dry runs return the real type.

Sprint 22. The B4 and B5 runners saved each response with
`json.dumps(resp, default=str)`. A real solve returns a `SolutionResults`
dataclass, so `default=str` stored its printed form -- numpy truncates long
arrays when printing, and every 560- and 816-value sample was saved as its
first and last three values. The B4 rows also recorded n_samples_returned = 0,
because the runner looked for a dict. The full samples were recovered by job
id (experiments/phase2/src/recover_device_samples.py).

It reached the device unseen because `eqc_submit.offline_solver` returned a
plain dict, so every dry run exercised a shape no real run produces. Both are
pinned here.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "src"))

import eqc_submit  # noqa: E402


def _model(n):
    """A REAL eqc model, so from_cloud_response sees the attributes a real
    solve has (machine_slacks, upper_bound)."""
    from eqc_models.ml.classifierqsvm import QSVMClassifier
    m = QSVMClassifier()
    m.set_model(np.eye(n), np.zeros((n, 1)), 1.0)
    return m


def _real_shaped(n=816, ns=8):
    from eqc_models.base.results import SolutionResults

    rng = np.random.default_rng(0)
    raw = {"results": {"solutions": [list(rng.dirichlet(np.ones(n)))
                                     for _ in range(ns)],
                       "energies": list(rng.normal(size=ns)),
                       "counts": [1] * ns},
           "job_info": {"job_id": "a" * 24, "job_submission": {
               "device_config": {"dirac-3": {"num_samples": ns}}}}}
    class _Solver:
        class client:                                   # noqa: N801
            @staticmethod
            def get_job_metrics(job_id=None):
                return {}

    return SolutionResults.from_cloud_response(_model(n), raw, _Solver())


def test_a_solution_results_round_trips_every_value():
    resp = _real_shaped()
    data = json.loads(json.dumps(eqc_submit.to_jsonable(resp)))
    sols = data["solutions"]
    assert len(sols) == 8 and all(len(s) == 816 for s in sols), (
        "a full 816-value sample must survive serialization")


def test_default_str_is_the_defect_this_replaces():
    """The original call, kept as a measurement: it does not round-trip."""
    text = json.dumps(_real_shaped(), default=str)
    assert "..." in text, (
        "numpy's print truncates; if this ever stops truncating, the reason "
        "for to_jsonable should be re-checked")


def test_samples_of_reads_the_real_object():
    assert len(eqc_submit.samples_of(_real_shaped())) == 8


def test_the_offline_solver_returns_the_real_response_type():
    """Dry runs must hand the runners what a real solve hands them."""
    from eqc_models.base.results import SolutionResults

    sent: list = []
    with eqc_submit.offline_solver(sent):
        import eqc_models.ml.classifierbase as cb
        resp = cb.Dirac3CloudSolver().solve(_model(4), num_samples=3,
                                           sum_constraint=1.0,
                                           relaxation_schedule=2)
    assert isinstance(resp, SolutionResults), (
        f"offline_solver returned {type(resp).__name__}; a real solve returns "
        "SolutionResults, so the dry run would test a shape no run produces")
    # The library sends the model's own num_samples, not the argument (F141
    # found this once the real job body was built offline), so the count
    # returned is the count the body asked for.
    assert len(eqc_submit.samples_of(resp)) == sent[0]["num_samples"]


def _offline_body_device(device_type):
    import eqc_models.ml.classifierbase as cb

    sent: list = []
    with eqc_submit.offline_solver(sent, device_type=device_type):
        cb.Dirac3CloudSolver().solve(_model(4), num_samples=3,
                                     sum_constraint=1.0,
                                     relaxation_schedule=2)
    return sent[0]["device_type"]


def test_the_offline_dry_run_builds_a_dirac_3s_request_body():
    """F141: the job body is built by qci-client's own build_job_body, so the
    device it names is what a real submit would send."""
    assert _offline_body_device("dirac-3s") == "dirac-3s"


def test_a_dirac_3_dry_run_is_unchanged():
    # qci-client maps the "dirac-3" alias to its device-specific name.
    assert _offline_body_device("dirac-3") == "dirac-3_normalized_qudit"


def test_the_device_block_selects_dirac_3s_and_restores():
    import eqc_models.ml.classifierbase as cb

    real = cb.Dirac3CloudSolver
    with eqc_submit.device("dirac-3s"):
        assert cb.Dirac3CloudSolver().sampler_type == "dirac-3s"
    assert cb.Dirac3CloudSolver is real
    assert real().sampler_type == "dirac-3"
    with eqc_submit.device("dirac-3"):
        assert cb.Dirac3CloudSolver is real


def test_an_unknown_device_is_refused():
    import pytest

    with pytest.raises(ValueError):
        with eqc_submit.device("dirac-4"):
            pass


def test_neither_runner_uses_default_str_on_a_response():
    for name in ("run_hardware_b4.py", "run_hardware_b5.py"):
        src = (ROOT / "experiments" / "src" / name).read_text(encoding="utf-8")
        assert "json.dumps(resp, default=str" not in src, (
            f"{name} saves a response with default=str again")
