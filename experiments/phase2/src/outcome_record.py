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
  - from filing on (2026-11-18), the same counts and the recall at the
    0.1% budget, `at_low_budget_on_test` (the filed preregistration,
    section 2; Sprint 33 D10; card F201). Each budget's entry also gives
    its recall, TP / (TP + FN). Blocks recorded before filing are not
    recomputed; `test_outcome_record_required.py` lists their files;
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
LOW_BUDGET = 0.001            # reported beside 0.5% from filing on (F201)
LOW_BUDGET_KEY = "at_low_budget_on_test"
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


def recall(c: dict) -> float:
    """TP / (TP + FN); refuses a fold with no positive."""
    pos = c["tp"] + c["fn"]
    if pos == 0:
        raise ValueError("no positive row; recall is undefined")
    return c["tp"] / pos


def at_budget_on_test(y, scores, budget: float = ALERT_BUDGET) -> dict:
    f = flagged_at_budget(scores, budget)
    c = confusion(y, f)
    return {"budget": budget, "n_budget": int(np.ceil(budget * len(f))),
            "n_flagged": int(f.sum()), "confusion": c, "recall": recall(c)}


def save_test_scores(name: str, seed, y_test, p_test,
                     pred_dir: Path = PRED_DIR) -> dict:
    """Write the per-row test labels and scores; return path and SHA-256.

    Never replaces a file (Sprint 31 D13, team lead: check that the name
    does not exist first and alter it as needed). If `<name>_<seed>.npz`
    holds the same bytes, it is reused (a resumed or repeated run). If it
    holds different bytes, the next free name `<name>_<seed>_v2.npz`,
    `_v3`, ... is written, and the returned path is that one. The F114
    re-run replaced nine recorded score files because this function
    overwrote whatever held the name."""
    if not name or any(c in name for c in "/\\ ."):
        raise ValueError(f"name {name!r} must be a plain file stem")
    pred_dir.mkdir(parents=True, exist_ok=True)
    first = pred_dir / f"{name}_{seed}.npz"
    tmp = first.with_suffix(f".{os.getpid()}.tmp.npz")
    np.savez_compressed(tmp, y_test=np.asarray(y_test), p_test=np.asarray(p_test))
    data = tmp.read_bytes()
    f, n = first, 1
    while True:
        try:
            os.link(tmp, f)        # fails if the name exists: never replaces
            break
        except FileExistsError:
            if f.read_bytes() == data:
                break              # the same scores are already there
            n += 1
            f = pred_dir / f"{name}_{seed}_v{n}.npz"
    tmp.unlink()
    return {"path": shown_path(f),
            "sha256": hashlib.sha256(data).hexdigest(),
            "n_rows": int(len(p_test))}


def shown_path(f: Path) -> str:
    """The path a block records: relative to the repository when inside it,
    so `stale_hashes` resolves it on any clone."""
    try:
        return Path(f).relative_to(ROOT).as_posix()
    except ValueError:
        return Path(f).as_posix()


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
           "at_budget_on_test": at_budget_on_test(y, p, budget),
           LOW_BUDGET_KEY: at_budget_on_test(y, p, LOW_BUDGET)}
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
