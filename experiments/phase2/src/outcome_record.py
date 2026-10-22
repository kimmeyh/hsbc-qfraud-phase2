"""F154's standing rule: every Phase 2 test result records its outcomes.

Sprint 28 Task F (#47). The team lead, 2026-10-22: every experiment, ML or
QML, this sprint and later, computes and records the confusion counts and
enough to see where each model wins. This module is the one way to do it, and
`experiments/src/test_outcome_record_required.py` fails any new result file
that holds a test score without a block from here.

A block holds:
  - the confusion counts (TN, FP, FN, TP) at the 0.5% alert budget on the
    test rows: every row scoring at or above the score of the ceil(0.5% * n)th
    highest row is flagged, so tied rows are flagged together and the count
    never depends on row order (`n_flagged` can exceed `n_budget` by the tie);
  - when validation scores are given, the counts at the two Phase 1
    operating points chosen on validation (`metrics.summarize`'s max-F1 and
    alert-budget thresholds), through `metrics.evaluate_at`, not a copy;
  - when the experiment has its own threshold, the counts there;
  - the per-row test scores, saved to `experiments/phase2/predictions/`
    (gitignored, except hardware files named `hw_*`, which cost metered
    seconds to regenerate), with the file's SHA-256, so any two models can be
    compared case by case later.

Zero metered seconds; nothing here calls a device.
"""
from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "src"))
import metrics  # noqa: E402  (Phase 1, read-only)

PRED_DIR = ROOT / "experiments" / "phase2" / "predictions"
ALERT_BUDGET = 0.005
REQUIRED_KEYS = ("name", "seed", "n_test", "n_positives",
                 "at_budget_on_test", "test_scores")


def confusion(y, flagged) -> dict:
    """TN, FP, FN and TP for 0/1 labels and a boolean flag per row."""
    y = np.asarray(y).astype(int)
    f = np.asarray(flagged).astype(bool)
    if y.shape != f.shape:
        raise ValueError(f"labels {y.shape} and flags {f.shape} differ in shape")
    return {"tn": int(((~f) & (y == 0)).sum()), "fp": int((f & (y == 0)).sum()),
            "fn": int(((~f) & (y == 1)).sum()), "tp": int((f & (y == 1)).sum())}


def flagged_at_budget(scores, budget: float = ALERT_BUDGET) -> np.ndarray:
    """True for every row at or above the ceil(budget * n)th highest score."""
    s = np.asarray(scores, dtype=float)
    if not np.all(np.isfinite(s)):
        raise ValueError("scores hold a NaN or infinity")
    k = int(np.ceil(budget * len(s)))
    if k < 1:
        raise ValueError(f"budget {budget} flags no row of {len(s)}")
    cut = np.sort(s)[::-1][k - 1]
    return s >= cut


def at_budget_on_test(y, scores, budget: float = ALERT_BUDGET) -> dict:
    f = flagged_at_budget(scores, budget)
    return {"budget": budget, "n_budget": int(np.ceil(budget * len(f))),
            "n_flagged": int(f.sum()), "confusion": confusion(y, f)}


def save_test_scores(name: str, seed, y_test, p_test,
                     pred_dir: Path = PRED_DIR) -> dict:
    """Write the per-row test labels and scores; return path and SHA-256."""
    if not name or any(c in name for c in "/\\ ."):
        raise ValueError(f"name {name!r} must be a plain file stem")
    pred_dir.mkdir(parents=True, exist_ok=True)
    f = pred_dir / f"{name}_{seed}.npz"
    tmp = f.with_suffix(f".{os.getpid()}.tmp.npz")
    np.savez_compressed(tmp, y_test=np.asarray(y_test), p_test=np.asarray(p_test))
    os.replace(tmp, f)
    try:
        shown = f.relative_to(ROOT).as_posix()
    except ValueError:
        shown = f.as_posix()
    return {"path": shown, "sha256": hashlib.sha256(f.read_bytes()).hexdigest(),
            "n_rows": int(len(p_test))}


def record(name: str, seed, y_test, p_test, *, y_val=None, p_val=None,
           threshold: float | None = None, budget: float = ALERT_BUDGET,
           pred_dir: Path = PRED_DIR, save: bool = True,
           source: dict | None = None) -> dict:
    """The block a result row carries. `source` replaces `save` when the
    scores already live in a file (F154 reading stored predictions): pass
    {"path": ..., "sha256": ...} and nothing is written."""
    y = np.asarray(y_test).astype(int)
    p = np.asarray(p_test, dtype=float)
    if len(y) != len(p):
        raise ValueError(f"{len(y)} labels and {len(p)} scores")
    if int(y.sum()) == 0:
        raise ValueError("the test rows hold no positive")
    out = {"name": name, "seed": seed, "n_test": int(len(y)),
           "n_positives": int(y.sum()),
           "at_budget_on_test": at_budget_on_test(y, p, budget)}
    if (y_val is None) != (p_val is None):
        raise ValueError("pass both y_val and p_val, or neither")
    if p_val is not None:
        out["operating_points_from_validation"] = [
            {"operating_point": op["operating_point"], "threshold": op["threshold"],
             "confusion": op["confusion"]}
            for op in (metrics.evaluate_at(y, p, metrics.threshold_max_f1(y_val, p_val),
                                           "max_f1_on_val"),
                       metrics.evaluate_at(y, p, metrics.threshold_alert_budget(p_val, budget),
                                           f"alert_budget_{budget}"))]
    if threshold is not None:
        out["at_own_threshold"] = {"threshold": float(threshold),
                                   "confusion": confusion(y, p >= threshold)}
    if source is not None:
        if not {"path", "sha256"} <= set(source):
            raise ValueError("source needs path and sha256")
        out["test_scores"] = dict(source)
    elif save:
        out["test_scores"] = save_test_scores(name, seed, y, p, pred_dir)
    else:
        raise ValueError("a block needs its per-row scores: save=True or a source")
    return out


def sha256_of(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def is_block(d) -> bool:
    return isinstance(d, dict) and all(k in d for k in REQUIRED_KEYS) \
        and "confusion" in d["at_budget_on_test"] \
        and {"path", "sha256"} <= set(d["test_scores"])
