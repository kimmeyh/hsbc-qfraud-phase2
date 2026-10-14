"""F145 (Sprint 26): a pool build is repeatable from its seed, when asked.

Two seed-42 `free` builds of the same pool, with today's code, gave identical
training rows and different validation and test rows: 61 of 78 learners and
327 of 4,426,188 test cells differed. eqc-models builds each
`DecisionTreeClassifier` with no `random_state`, so ties between equally good
splits are broken at random. The trees agree on the rows they were fitted to
and disagree elsewhere.

The fix is OPT-IN (`qubo_proxy.seeded_weak_params`, `build --seeded-learners`)
so Phase 1 builds keep their filed behavior (CLAUDE.md, the Phase 1
boundary, rule 4).

The fixture forces the tie: two training columns are identical, so either
gives the same split, and they differ off the training rows, so a tree that
picked the other column predicts differently there.
"""
from __future__ import annotations

import numpy as np

import qubo_proxy


def _tied_data():
    rng = np.random.default_rng(3)
    n = 400
    a = rng.normal(size=n)
    X_tr = np.column_stack([a, a, rng.normal(size=(n, 3))]).astype(np.float32)
    y = np.where(a + 0.3 * rng.normal(size=n) > 0, 1, -1)
    X_other = X_tr.copy()
    X_other[:, 1] = rng.normal(size=n)          # the twin column diverges
    return X_tr, y, X_other


def _build(weak_params):
    X_tr, y, X_other = _tied_data()
    clf = qubo_proxy.build_pool(X_tr, y, schedule=2, weak_type="dct",
                                pair_build="sequential",
                                weak_params=weak_params)
    return (qubo_proxy.h_matrix(clf, X_tr), qubo_proxy.h_matrix(clf, X_other))


def test_seeded_builds_are_byte_identical():
    params = qubo_proxy.seeded_weak_params(42)
    a_tr, a_other = _build(params)
    b_tr, b_other = _build(params)
    assert a_tr.tobytes() == b_tr.tobytes()
    assert a_other.tobytes() == b_other.tobytes(), (
        "two seeded builds disagree off the training rows (F145)")


def test_seeding_is_opt_in_and_keeps_the_callers_params():
    assert qubo_proxy.seeded_weak_params(7) == {"random_state": 7}
    assert qubo_proxy.seeded_weak_params(7, {"max_depth": 2}) == {
        "max_depth": 2, "random_state": 7}
    # The Phase 1 default passes no random_state.
    import inspect
    src = inspect.getsource(qubo_proxy.cmd_build)
    assert "seeded_learners" in src


def test_unseeded_builds_differ_on_this_fixture():
    """The reference: without the seed, this fixture DOES drift, so the
    identical-build test above is not passing for lack of a tie."""
    outs = [_build(None)[1].tobytes() for _ in range(4)]
    assert len(set(outs)) > 1
