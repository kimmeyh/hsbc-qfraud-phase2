"""The full-pair weak-learner pool, built without `fork`.

Sprint 28 (Tasks D and E). eqc-models' full-pair builder,
`QBoostClassifier._build_weak_classifiers_mp`, calls
`set_start_method("fork", force=True)`, which raises ValueError on
Windows (Phase 1 feedback item 3; `docs/phase2/DIRAC_UNDERSTANDINGS.md`
section 3, item 2). This module builds the same learners in the same
order, one after another, with the library's own `WeakClassifier`:
every single feature, then every pair i < j, then (schedule 3) every
triple i < j < k. Each learner is trained exactly as the library's worker
trains it (`WeakClassifier(X[:, idx], y, type, params).train()`).

`qubo_proxy.build_pool` (Phase 1, shared) is not edited. The classifier is
constructed with the same arguments and the same attribute check, so
`qubo_proxy.h_matrix` and the library's own `get_hamiltonian` read it as
they read a library-built pool.
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "experiments" / "src"))


def learner_indices(n_dims: int, schedule: int) -> list[list[int]]:
    """The library's full-pair order: singles, pairs i < j, triples."""
    out = [[i] for i in range(n_dims)]
    if schedule >= 2:
        out += [list(p) for p in itertools.combinations(range(n_dims), 2)]
    if schedule >= 3:
        out += [list(t) for t in itertools.combinations(range(n_dims), 3)]
    return out


def build_full(X_tr: np.ndarray, y_pm1: np.ndarray, schedule: int,
               weak_type: str, weak_params: dict | None = None,
               lambda_coef: float | None = None, indices=None):
    """`qubo_proxy.build_pool(..., pair_build="full")`, without `fork`.
    `indices` (default: the full-pair order) lets F159's parallel build
    take the classifier from here with no learners (`indices=[]`)."""
    from eqc_models.ml.classifierqboost import QBoostClassifier, WeakClassifier
    import qubo_proxy as qp
    n = X_tr.shape[1]
    if schedule >= 2 and n < 4:
        raise ValueError(f"schedule {schedule} impossible for n={n} features "
                         "(pair cap n(n-3)/2 <= 0); use schedule 1")
    cfg = dict(lambda_coef=(qp.LAMBDA_MULT * len(y_pm1) if lambda_coef is None
                            else lambda_coef),
               weak_cls_schedule=schedule, weak_cls_type=weak_type,
               weak_cls_params=dict(weak_params or {}),
               weak_cls_strategy="multi_processing", **qp.FIXED)
    clf = QBoostClassifier(**cfg)
    for k, v in cfg.items():   # qubo_proxy's F18 silent-kwarg-drop guard
        assert getattr(clf, k) == v, f"constructed attr mismatch: {k}"
    clf.h_list, clf.ind_list = [], []
    for idx in (learner_indices(n, schedule) if indices is None else indices):
        wc = WeakClassifier(X_tr[:, idx], y_pm1, weak_type, cfg["weak_cls_params"])
        wc.train()
        clf.ind_list.append(idx)
        clf.h_list.append(wc)
    return clf
