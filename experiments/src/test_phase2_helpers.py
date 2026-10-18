"""Functions PR #21's review found untested (Sprint 26 test-coverage review).

- `f126_sparsity_rule.fit_and_test`: picks the parameter on the training
  fits only and judges the rule on the held-out ones.
- `f144_proxy_twin.paired`: the exact Wilcoxon decides, at ALPHA. Five
  same-sign differences give p = 0.0625 (not rejected), six give 0.03125.
- `eqc_submit.device(wrap=)`: installs the wrapped class, then restores the
  real one.
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))


def _const(w, p):
    return p


def _fit_and_test_holds(f126) -> bool:
    grid = np.array([0.0, 0.2, 0.5])
    train = [(None, 0.2), (None, 0.2)]
    near = f126.fit_and_test(train, [(None, 0.22), (None, 0.18)], _const,
                             grid)
    far = f126.fit_and_test(train, [(None, 0.5)], _const, grid)
    return (near["param"] == 0.2 and near["train_mae"] == 0.0
            and abs(near["test_mae"] - 0.02) < 1e-12 and near["passes"]
            and far["param"] == 0.2 and not far["passes"]
            and abs(far["test_max_abs_error"] - 0.3) < 1e-12)


def test_fit_and_test_fits_on_train_and_judges_on_test():
    import f126_sparsity_rule as f126
    assert _fit_and_test_holds(f126)


def test_fit_and_test_can_fail():
    import f126_sparsity_rule as f126
    from injection import Mutation, assert_can_fail
    src = Path(f126.__file__)

    def run() -> bool:
        return _fit_and_test_holds(importlib.reload(f126))

    try:
        assert_can_fail([Mutation(src, "grid[int(np.argmin(errs))]",
                                  "grid[int(np.argmax(errs))]",
                                  expect_occurrences=1)],
                        run, "the parameter chosen by the worst fit")
        assert_can_fail([Mutation(src, '"passes": bool(np.mean(np.abs(held))'
                                  ' <= TOLERANCE)',
                                  '"passes": bool(min(errs) <= TOLERANCE)',
                                  expect_occurrences=1)],
                        run, "the rule judged on its training fits")
    finally:
        importlib.reload(f126)


def _paired_holds(f144) -> bool:
    five = f144.paired([0.1, 0.2, 0.3, 0.4, 0.5], [0.0] * 5)
    six = f144.paired([0.1, 0.2, 0.3, 0.4, 0.5, 0.6], [0.0] * 6)
    zero = f144.paired([0.3] * 5, [0.3] * 5)
    return (five["wilcoxon_p"] == 0.0625 and not five["rejects"]
            and six["wilcoxon_p"] == 0.03125 and six["rejects"]
            and not zero["rejects"] and zero["mean"] == 0.0)


def test_paired_rejects_on_the_exact_wilcoxon_only():
    import f144_proxy_twin as f144
    assert _paired_holds(f144)


def test_paired_can_fail():
    import f144_proxy_twin as f144
    from injection import Mutation, assert_can_fail
    src = Path(f144.__file__)

    def run() -> bool:
        return _paired_holds(importlib.reload(f144))

    try:
        assert_can_fail([Mutation(src, 'method="exact"',
                                  'method="asymptotic"',
                                  expect_occurrences=1)],
                        run, "the normal approximation at five seeds")
        assert_can_fail([Mutation(src, '"rejects": bool(p < ALPHA)',
                                  '"rejects": bool(p < 2 * ALPHA)',
                                  expect_occurrences=1)],
                        run, "a looser threshold than ALPHA")
    finally:
        importlib.reload(f144)


def _wrap_installs_and_restores(eqc_submit) -> bool:
    import eqc_models.ml.classifierbase as cb
    real = cb.Dirac3CloudSolver
    seen = []

    def wrap(cls):
        seen.append(cls)
        return type("Wrapped", (cls,), {})

    with eqc_submit.device(eqc_submit.DIRAC_3, wrap=wrap):
        inside = cb.Dirac3CloudSolver
    return (seen == [real] and inside.__name__ == "Wrapped"
            and issubclass(inside, real) and cb.Dirac3CloudSolver is real)


def test_device_installs_the_wrapped_class_and_restores():
    import eqc_submit
    assert _wrap_installs_and_restores(eqc_submit)


def test_the_wrap_install_can_fail():
    import eqc_submit
    from injection import Mutation, assert_can_fail
    src = Path(eqc_submit.__file__)

    def run() -> bool:
        return _wrap_installs_and_restores(importlib.reload(eqc_submit))

    try:
        assert_can_fail([Mutation(src, "= wrap(cls) if wrap else cls",
                                  "= cls", expect_occurrences=1)],
                        run, "the wrap ignored")
    finally:
        importlib.reload(eqc_submit)
