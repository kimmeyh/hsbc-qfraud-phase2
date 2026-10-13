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
    legitimate transaction), then the top 0.5% is flagged. No router that
    chooses or averages the two models' percentile ranks per transaction can
    beat it, because none knows the label. It does not bound a stacker that
    uses features or the raw scores on their own scales;
  - Spearman rank correlation of the two score vectors, over all test rows
    and over the frauds alone.

WHICH CONFIGURATIONS. Every stored CVQBoost proxy family and XGBoost family
with predictions on all ten seeds is a candidate, found in the predictions
directory (the plan said "from results.json by config hash"; the directory is
the complete list of what can be scored, and each family's hash is checked
against a results.json row). One of each is chosen by mean VALIDATION AUPRC,
so the choice never looks at the test fold. Every other pair is reported as a
sensitivity check.

THE BASELINE is one fixed model, the chosen pair's better model by mean
validation recall at the budget, because a deployed router competes against
one model, not against whichever wins each seed. The gap against the
per-seed better model is reported beside it.

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

RESULTS = ROOT / "experiments" / "results" / "results.json"
SEEDS = tuple(range(42, 52))
ARMS = ("cvqboost_proxy", "xgboost")
ALERT_BUDGET = 0.005
ROUTER_CRITERION = 0.01


def percentile_rank(scores: np.ndarray) -> np.ndarray:
    """Average-tie percentile in (0, 1]; comparable across models."""
    from scipy.stats import rankdata
    return rankdata(scores, method="average") / len(scores)


def recall_at_budget(y: np.ndarray, scores: np.ndarray,
                     budget: float = ALERT_BUDGET) -> float:
    """Expected recall when the top `budget` fraction of rows is flagged.

    Exactly ceil(budget * n) rows are flagged. Rows strictly above the cut
    score are all flagged; the rest come from the group tied AT the cut, and
    that group gets fractional credit (the expected recall under a random
    tie-break), so the result does not depend on row order (Sprint 25 code
    review: the oracle's tied group at the cut held a fraud on two seeds)."""
    y = np.asarray(y)
    s = np.asarray(scores)
    pos = int(y.sum())
    if pos == 0:
        raise ValueError("recall is undefined with no positives")
    k = int(np.ceil(budget * len(y)))
    cut = np.sort(s)[::-1][k - 1]
    above = s > cut
    tied = s == cut
    n_above = int(above.sum())
    credit = (k - n_above) / int(tied.sum())
    return float((y[above].sum() + credit * y[tied].sum()) / pos)


def oracle_scores(y: np.ndarray, a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Per transaction, the better of the two percentile ranks for its label."""
    ra, rb = percentile_rank(a), percentile_rank(b)
    return np.where(np.asarray(y) == 1, np.maximum(ra, rb), np.minimum(ra, rb))


def one_seed(y: np.ndarray, p_cvq: np.ndarray, p_xgb: np.ndarray,
             baseline: str = "xgb") -> dict:
    """`baseline` names the fixed model the gap is measured against."""
    from scipy.stats import spearmanr
    r_cvq = recall_at_budget(y, p_cvq)
    r_xgb = recall_at_budget(y, p_xgb)
    r_orc = recall_at_budget(y, oracle_scores(y, p_cvq, p_xgb))
    fixed = {"cvq": r_cvq, "xgb": r_xgb}[baseline]
    pos = np.asarray(y) == 1
    ra, rb = percentile_rank(p_cvq), percentile_rank(p_xgb)
    r_base = rb if baseline == "xgb" else ra
    # Fresh-eyes review, Sprint 25: split the oracle into its halves, and
    # add label-free combinations as the floor beside the oracle's ceiling.
    fraud_side = np.where(pos, np.maximum(ra, rb), r_base)
    legit_side = np.where(pos, r_base, np.minimum(ra, rb))
    _, counts = np.unique(p_cvq, return_counts=True)
    return {"recall_cvq": r_cvq, "recall_xgb": r_xgb, "recall_oracle": r_orc,
            "oracle_gap": r_orc - fixed,
            "oracle_gap_vs_per_seed_best": r_orc - max(r_cvq, r_xgb),
            "recall_oracle_fraud_side_only": recall_at_budget(y, fraud_side),
            "recall_oracle_legit_side_only": recall_at_budget(y, legit_side),
            "recall_label_free_mean_rank": recall_at_budget(y, (ra + rb) / 2),
            "recall_label_free_max_rank": recall_at_budget(y, np.maximum(ra, rb)),
            "cvq_distinct_scores": int(len(counts)),
            "cvq_modal_score_share": float(counts.max() / len(p_cvq)),
            "n_test": int(len(y)),
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


def _val_recall(family: str) -> float:
    return float(np.mean([recall_at_budget(d["y_val"], d["p_val"])
                          for d in (_load(family, s) for s in SEEDS)]))


def families(arm: str, pred_dir: Path = PRED) -> list[str]:
    """Every stored family of `arm` with stratified predictions on all seeds."""
    found = {}
    for f in pred_dir.glob(f"{arm}_*_stratified_*.npz"):
        fam = f.name.rsplit("_stratified_", 1)[0]
        if fam[len(arm) + 1:].count("_") == 0:            # arm_<hash> only
            found.setdefault(fam, set()).add(int(f.stem.rsplit("_", 1)[1]))
    return sorted(f for f, s in found.items() if set(SEEDS) <= s)


def _check_in_results(fams: list[str]) -> None:
    hashes = {r.get("config_hash") for r in json.loads(RESULTS.read_text())["rows"]}
    missing = [f for f in fams if f.rsplit("_", 1)[1] not in hashes]
    if missing:
        raise ValueError(f"prediction families with no results.json row: {missing}")


def run_pair(cvq: str, xgb: str) -> dict:
    baseline = "xgb" if _val_recall(xgb) >= _val_recall(cvq) else "cvq"
    rows = []
    for seed in SEEDS:
        a, b = _load(cvq, seed), _load(xgb, seed)
        if not np.array_equal(a["y_test"], b["y_test"]):
            raise ValueError(f"seed {seed}: {cvq} and {xgb} are not on the same split")
        rows.append({"seed": seed,
                     **one_seed(a["y_test"], a["p_test"], b["p_test"], baseline)})
    return {"cvq": cvq, "xgb": xgb, "baseline": baseline,
            "baseline_rule": "the pair's better model by mean validation recall at the budget",
            "rows": rows,
            "verdict": verdict([r["oracle_gap"] for r in rows]),
            "oracle_gap_vs_per_seed_best_mean": float(np.mean(
                [r["oracle_gap_vs_per_seed_best"] for r in rows])),
            "recall_cvq_mean": float(np.mean([r["recall_cvq"] for r in rows])),
            "recall_xgb_mean": float(np.mean([r["recall_xgb"] for r in rows])),
            "recall_oracle_mean": float(np.mean([r["recall_oracle"] for r in rows])),
            **{f"{k}_mean": float(np.mean([r[k] for r in rows]))
               for k in ("recall_oracle_fraud_side_only", "recall_oracle_legit_side_only",
                         "recall_label_free_mean_rank", "recall_label_free_max_rank",
                         "cvq_modal_score_share")},
            "spearman_all_mean": float(np.mean([r["spearman_all"] for r in rows])),
            "spearman_frauds_mean": float(np.mean([r["spearman_frauds"] for r in rows]))}


def run() -> dict:
    cvq_fams, xgb_fams = families(ARMS[0]), families(ARMS[1])
    if not cvq_fams or not xgb_fams:
        raise ValueError("no stored prediction family for one of the arms")
    _check_in_results(cvq_fams + xgb_fams)
    val = {f: _val_auprc(f) for f in cvq_fams + xgb_fams}
    cvq = max(cvq_fams, key=val.get)
    xgb = max(xgb_fams, key=val.get)
    primary = run_pair(cvq, xgb)
    sensitivity = [run_pair(c, x) for c in cvq_fams for x in xgb_fams
                   if (c, x) != (cvq, xgb)]
    # Within-family reference (fresh-eyes review): the same oracle between
    # the other XGBoost family and the chosen one. If it also clears the
    # criterion, the criterion does not single out CVQBoost.
    others = [x for x in xgb_fams if x != xgb]
    reference = ({k: v for k, v in run_pair(others[0], xgb).items() if k != "rows"}
                 if others else None)
    return {"candidate_families": {"cvq": cvq_fams, "xgb": xgb_fams},
            "within_family_reference": reference,
            "validation_auprc_by_family": val, "primary": primary,
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
        "recall_ties": "the group tied at the cut gets fractional credit",
        "generator_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    OUT.write_text(json.dumps({**header, **res}, indent=2), encoding="utf-8")
    p = res["primary"]
    print(json.dumps({"cvq": p["cvq"], "xgb": p["xgb"], "baseline": p["baseline"],
                      **p["verdict"],
                      "gap_vs_per_seed_best_mean": p["oracle_gap_vs_per_seed_best_mean"],
                      "recall_cvq_mean": p["recall_cvq_mean"],
                      "recall_xgb_mean": p["recall_xgb_mean"],
                      "recall_oracle_mean": p["recall_oracle_mean"],
                      "spearman_all_mean": p["spearman_all_mean"],
                      "spearman_frauds_mean": p["spearman_frauds_mean"]}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
