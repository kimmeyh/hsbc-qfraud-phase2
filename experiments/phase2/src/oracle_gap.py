"""F113: could ANY router between CVQBoost and XGBoost beat the better model?

Sprint 25 Task D (#16). Phase 2 code over STORED Phase 1 predictions
(`experiments/results/predictions/*.npz`); nothing is refitted and no Phase 1
file is edited. Results go to `experiments/phase2/results/f113_oracle_gap.json`.
Zero metered seconds.

WHAT IS MEASURED, per seed on the ULB test fold, at the 0.5% alert budget
(the proposal's router criterion):
  - each model's recall at the budget (its top 0.5% of scores flagged);
  - the ORACLE's recall: each transaction is scored by whichever model ranks
    it better FOR ITS TRUE LABEL (higher percentile for a fraud, lower for a
    legitimate transaction), then the top 0.5% is flagged. No real router can
    beat it, because no real router knows the label;
  - Spearman rank correlation of the two score vectors, over all test rows
    and over the frauds alone.

WHICH CONFIGURATIONS. One CVQBoost proxy family and one XGBoost family, each
chosen by mean VALIDATION AUPRC across the seeds, so the choice never looks at
the test fold. Every other pair is reported as a sensitivity check.

PREMISE FALSIFIER, stated before the run (Sprint 25 plan, Task D): if the
oracle's recall at the 0.5% budget is less than ROUTER_CRITERION (1 point)
above the better single model, no router can meet the proposal's criterion,
and the write-up recommends retiring F121. A larger oracle gap is an upper
bound only: it says a router is not ruled out, not that one would work.

Run:  <venv python> experiments/phase2/src/oracle_gap.py
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PRED = ROOT / "experiments" / "results" / "predictions"
OUT = ROOT / "experiments" / "phase2" / "results" / "f113_oracle_gap.json"

SEEDS = tuple(range(42, 52))
CVQ_FAMILIES = ("cvqboost_proxy_1e6bf03caab3676b", "cvqboost_proxy_47012b1404d5d4de",
                "cvqboost_proxy_640ed4cf9c46ea4b")
XGB_FAMILIES = ("xgboost_03999a57a5107f44", "xgboost_d68789d82137da1d")
ALERT_BUDGET = 0.005
ROUTER_CRITERION = 0.01


def percentile_rank(scores: np.ndarray) -> np.ndarray:
    """Average-tie percentile in (0, 1]; comparable across models."""
    from scipy.stats import rankdata
    return rankdata(scores, method="average") / len(scores)


def recall_at_budget(y: np.ndarray, scores: np.ndarray,
                     budget: float = ALERT_BUDGET) -> float:
    """Recall when the top `budget` fraction of rows is flagged.

    Ties at the cut are broken by row order (stable sort), so the number of
    flagged rows is exactly ceil(budget * n)."""
    y = np.asarray(y)
    k = int(np.ceil(budget * len(y)))
    top = np.argsort(-np.asarray(scores), kind="stable")[:k]
    pos = int(y.sum())
    if pos == 0:
        raise ValueError("recall is undefined with no positives")
    return float(y[top].sum() / pos)


def oracle_scores(y: np.ndarray, a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Per transaction, the better of the two percentile ranks for its label."""
    ra, rb = percentile_rank(a), percentile_rank(b)
    return np.where(np.asarray(y) == 1, np.maximum(ra, rb), np.minimum(ra, rb))


def one_seed(y: np.ndarray, p_cvq: np.ndarray, p_xgb: np.ndarray) -> dict:
    from scipy.stats import spearmanr
    r_cvq = recall_at_budget(y, p_cvq)
    r_xgb = recall_at_budget(y, p_xgb)
    r_orc = recall_at_budget(y, oracle_scores(y, p_cvq, p_xgb))
    best = max(r_cvq, r_xgb)
    pos = np.asarray(y) == 1
    return {"recall_cvq": r_cvq, "recall_xgb": r_xgb, "recall_oracle": r_orc,
            "oracle_gap": r_orc - best, "n_test": int(len(y)),
            "n_positives": int(pos.sum()),
            "n_flagged": int(np.ceil(ALERT_BUDGET * len(y))),
            "spearman_all": float(spearmanr(p_cvq, p_xgb).statistic),
            "spearman_frauds": float(spearmanr(p_cvq[pos], p_xgb[pos]).statistic)}


def verdict(gaps: list[float], criterion: float = ROUTER_CRITERION) -> dict:
    g = np.asarray(gaps, dtype=float)
    mean = float(g.mean())
    return {"oracle_gap_mean": mean, "oracle_gap_min": float(g.min()),
            "oracle_gap_max": float(g.max()), "router_criterion": criterion,
            "router_ruled_out": mean < criterion}


def _load(family: str, seed: int) -> dict:
    return dict(np.load(PRED / f"{family}_stratified_{seed}.npz"))


def _val_auprc(family: str) -> float:
    from sklearn.metrics import average_precision_score
    return float(np.mean([average_precision_score(d["y_val"], d["p_val"])
                          for d in (_load(family, s) for s in SEEDS)]))


def run_pair(cvq: str, xgb: str) -> dict:
    rows = []
    for seed in SEEDS:
        a, b = _load(cvq, seed), _load(xgb, seed)
        if not np.array_equal(a["y_test"], b["y_test"]):
            raise ValueError(f"seed {seed}: {cvq} and {xgb} are not on the same split")
        rows.append({"seed": seed, **one_seed(a["y_test"], a["p_test"], b["p_test"])})
    return {"cvq": cvq, "xgb": xgb, "rows": rows,
            "verdict": verdict([r["oracle_gap"] for r in rows]),
            "recall_cvq_mean": float(np.mean([r["recall_cvq"] for r in rows])),
            "recall_xgb_mean": float(np.mean([r["recall_xgb"] for r in rows])),
            "recall_oracle_mean": float(np.mean([r["recall_oracle"] for r in rows])),
            "spearman_all_mean": float(np.mean([r["spearman_all"] for r in rows])),
            "spearman_frauds_mean": float(np.mean([r["spearman_frauds"] for r in rows]))}


def run() -> dict:
    val = {f: _val_auprc(f) for f in CVQ_FAMILIES + XGB_FAMILIES}
    cvq = max(CVQ_FAMILIES, key=val.get)
    xgb = max(XGB_FAMILIES, key=val.get)
    primary = run_pair(cvq, xgb)
    sensitivity = [run_pair(c, x) for c in CVQ_FAMILIES for x in XGB_FAMILIES
                   if (c, x) != (cvq, xgb)]
    return {"validation_auprc_by_family": val, "primary": primary,
            "sensitivity": [{k: p[k] for k in p if k != "rows"} for p in sensitivity]}


def main() -> int:
    res = run()
    header = {
        "generator": "experiments/phase2/src/oracle_gap.py", "card": "F113",
        "sprint": 25, "phase": 2, "evidence_tag": "SIM", "metered_seconds": 0,
        "date": time.strftime("%Y-%m-%d"), "dataset": "ulb",
        "protocol": "stratified", "seeds": list(SEEDS),
        "alert_budget": ALERT_BUDGET, "router_criterion": ROUTER_CRITERION,
        "selection": "each family by mean validation AUPRC; test fold unseen",
        "generator_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    OUT.write_text(json.dumps({**header, **res}, indent=2), encoding="utf-8")
    p = res["primary"]
    print(json.dumps({"cvq": p["cvq"], "xgb": p["xgb"], **p["verdict"],
                      "recall_cvq_mean": p["recall_cvq_mean"],
                      "recall_xgb_mean": p["recall_xgb_mean"],
                      "recall_oracle_mean": p["recall_oracle_mean"],
                      "spearman_all_mean": p["spearman_all_mean"],
                      "spearman_frauds_mean": p["spearman_frauds_mean"]}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
