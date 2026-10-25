"""The fork-free full-pair pool equals the library's own full-pair pool.

Sprint 28 (Tasks D and E). The direct comparison needs `fork`, so it runs
on Linux (CI) and skips visibly on Windows; the order and the learner
outputs are checked everywhere.
"""
from __future__ import annotations

import multiprocessing
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "src"))

import full_pair_pool as fpp  # noqa: E402
import qubo_proxy as qp  # noqa: E402

HAS_FORK = "fork" in multiprocessing.get_all_start_methods()


def _data(n=400, d=6, seed=0):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, d)).astype(np.float32)
    y = np.where(X[:, 0] + X[:, 1] * X[:, 2] + rng.normal(0, 0.5, n) > 0, 1, -1)
    return X, y


def test_learner_counts_match_the_variable_counts_on_record():
    assert len(fpp.learner_indices(13, 2)) == 91       # free
    assert len(fpp.learner_indices(17, 2)) == 153      # mid
    assert len(fpp.learner_indices(13, 3)) == 377      # deep
    assert len(fpp.learner_indices(17, 3)) == 833      # full
    assert len(fpp.learner_indices(30, 2)) == 465      # all ULB columns


def test_order_is_singles_then_pairs_then_triples():
    idx = fpp.learner_indices(4, 3)
    assert idx[:4] == [[0], [1], [2], [3]]
    assert idx[4:10] == [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]
    assert idx[10] == [0, 1, 2] and idx[-1] == [1, 2, 3]


def test_each_learner_sees_only_its_own_columns():
    from sklearn.neighbors import KNeighborsClassifier
    X, y = _data()
    clf = fpp.build_full(X, y, 2, "knn", {"n_neighbors": 15}, lambda_coef=0.0)
    H = qp.h_matrix(clf, X)
    for row, idx in ((0, [0]), (6, [0, 1]), (len(clf.ind_list) - 1, [4, 5])):
        assert clf.ind_list[row] == idx
        k = KNeighborsClassifier(n_neighbors=15).fit(X[:, idx], (y == 1).astype(int))
        assert np.array_equal(np.sign(H[row]), np.where(k.predict(X[:, idx]) == 1, 1, -1))


def test_the_constructor_carries_lambda_zero():
    X, y = _data()
    clf = fpp.build_full(X, y, 2, "knn", {"n_neighbors": 5}, lambda_coef=0.0)
    assert clf.lambda_coef == 0.0 and clf.weak_cls_schedule == 2


@pytest.mark.skipif(not HAS_FORK, reason="NOT COMPARED: the library's full-pair "
                    "builder needs fork, absent on this OS; CI (Linux) runs it")
def test_equals_the_library_full_pair_builder():
    X, y = _data()
    ours = fpp.build_full(X, y, 3, "dct", qp.seeded_weak_params(42))
    lib = qp.build_pool(X, y, 3, "dct", "full", weak_params=qp.seeded_weak_params(42))
    assert ours.ind_list == lib.ind_list
    assert np.array_equal(qp.h_matrix(ours, X), qp.h_matrix(lib, X))
