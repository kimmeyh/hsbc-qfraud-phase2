"""F185 (Sprint 32 Task D, #113): a cost-weighted alert budget on the
stored champion scores.

The entry is "F185" in `experiments/phase2/PREREGISTRATION_DRAFT.md`
section 6, committed before this module existed. At the same review
count as today's 0.5% budget, k = ceil(0.005 x n_test), two rankings:
(1) by score, today's; (2) by expected loss, score x amount (Hoppner et
al., EvidenceBasedDB `hoppner-instance-threshold`: flag when
s_i > c_f / A_i). Both read the champions' stored per-row test scores,
ten seeds each: ULB CatBoost (F166) and IEEE-CIS LightGBM (F174). The
amounts are joined by rebuilding each test part; a score file whose
SHA-256 differs from its outcome block, or whose labels differ from the
rebuilt ones, is refused, not joined.

    <venv python> experiments/phase2/src/f185_cost_budget.py

Zero metered seconds. Writes `experiments/phase2/results/f185_cost_budget.json`
through `provenance.write_result`, once, at the end (`resumable=False`).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "experiments" / "src"))
import outcome_record as orec  # noqa: E402

OUT = ROOT / "experiments" / "phase2" / "results" / "f185_cost_budget.json"
LONG_RUN = False                       # minutes, one straight run
RESULTS = ROOT / "experiments" / "phase2" / "results"
SOURCES = {
    "ulb": {"result": RESULTS / "f166_ulb_algorithms.json",
            "lane": "catboost", "amount": "Amount",
            "unit": "the dataset's Amount unit (not stated in its source)"},
    "ieee_cis": {"result": RESULTS / "f174_ieee_algorithms.json",
                 "lane": "lightgbm", "amount": "TransactionAmt",
                 "unit": "US dollars"},
}
REVIEW_COSTS = (5.0, 10.0, 25.0)       # c_f per alert, fixed by the entry
BUDGET = orec.ALERT_BUDGET             # 0.005


class Refused(RuntimeError):
    """A score file that cannot be joined to its amounts."""


# ----------------------------------------------------------- the join
def joined(y_stored, p_stored, y_rebuilt, amounts) -> tuple:
    """(y, scores, amounts) once the stored labels equal the rebuilt ones
    row for row; refused otherwise."""
    y_s = np.asarray(y_stored).astype(int)
    y_r = np.asarray(y_rebuilt).astype(int)
    a = np.asarray(amounts, dtype=float)
    if y_s.shape != y_r.shape or a.shape != y_s.shape \
            or np.asarray(p_stored).shape != y_s.shape:
        raise Refused(f"shapes differ: stored {y_s.shape}, rebuilt "
                      f"{y_r.shape}, amounts {a.shape}")
    if not np.array_equal(y_s, y_r):
        raise Refused(f"{int((y_s != y_r).sum())} labels differ from the "
                      "rebuilt test part; the rows are not aligned")
    if not np.all(np.isfinite(a)) or (a < 0).any():
        raise Refused("an amount is missing, infinite or negative")
    return y_s, np.asarray(p_stored, dtype=float), a


def checked_scores(block: dict) -> tuple:
    """(y_test, p_test) from a stored outcome block's file, refused when
    its SHA-256 is not the block's."""
    src = block["test_scores"]
    path = ROOT / src["path"]
    if not path.exists():
        raise Refused(f"{src['path']} is not on disk")
    if orec.sha256_of(path) != src["sha256"]:
        raise Refused(f"{src['path']}: SHA-256 differs from its outcome "
                      "block")
    with np.load(path) as z:            # closes the file (Windows cleanup)
        return z["y_test"], z["p_test"]


# ----------------------------------------------------------- the reading
def ranking(y, scores, amounts, costs=REVIEW_COSTS) -> dict:
    """Dollars caught and the confusion counts at the 0.5% budget for one
    ranking's scores; net savings per review cost."""
    flagged = orec.flagged_at_budget(scores, BUDGET)
    fraud = y == 1
    caught = float(amounts[flagged & fraud].sum())
    total = float(amounts[fraud].sum())
    n = int(flagged.sum())
    return {"n_flagged": n, "confusion": orec.confusion(y, flagged),
            "dollars_caught": caught, "dollars_missed": total - caught,
            "fraud_dollars": total,
            "net_savings": {str(c): caught - n * c for c in costs}}


def hoppner_alerts(scores, amounts, costs=REVIEW_COSTS) -> dict:
    """Alerts Hoppner's rule s_i > c_f / A_i would raise, per c_f
    (scores used as given, not recalibrated)."""
    loss = np.asarray(scores, float) * np.asarray(amounts, float)
    # s > c / A is s x A > c for A > 0; an amount of 0 is never flagged.
    return {str(c): int((loss > c).sum()) for c in costs}


def compare(y, scores, amounts) -> dict:
    by_score = ranking(y, scores, amounts)
    by_loss = ranking(y, scores * amounts, amounts)
    return {"by_score": by_score, "by_expected_loss": by_loss,
            "dollars_gain": by_loss["dollars_caught"]
            - by_score["dollars_caught"],
            "hoppner_alerts": hoppner_alerts(scores, amounts)}


def can_fire() -> dict:
    """A built case where ranking by expected loss must catch more
    dollars: 400 rows, k = 2; two small frauds score 0.9, two large frauds
    0.8, the rest 0.1."""
    y = np.zeros(400, int)
    y[:4] = 1
    s = np.full(400, 0.1)
    s[:2], s[2:4] = 0.9, 0.8
    a = np.full(400, 10.0)
    a[:2], a[2:4] = 5.0, 500.0
    c = compare(y, s, a)
    return {"by_score_caught": c["by_score"]["dollars_caught"],
            "by_loss_caught": c["by_expected_loss"]["dollars_caught"],
            "can_fire": bool(c["dollars_gain"] > 0)}


def refusal_fires() -> dict:
    """A copy of a label vector with one label flipped must be refused."""
    y = np.array([0, 1, 0, 0])
    flipped = y.copy()
    flipped[0] = 1
    try:
        joined(y, np.zeros(4), flipped, np.ones(4))
    except Refused:
        return {"label_flip_refused": True}
    return {"label_flip_refused": False}


def t_interval(x) -> dict:
    from scipy import stats
    x = np.asarray(x, float)
    n, m = len(x), float(np.mean(x))
    if n < 2:
        return {"n": n, "mean": m, "t95": None}
    h = float(stats.t.ppf(0.975, n - 1) * np.std(x, ddof=1) / np.sqrt(n))
    return {"n": n, "mean": m, "t95": [m - h, m + h]}


def over_seeds(rows: list[dict]) -> dict:
    key = lambda r, k: r["compare"][k]["dollars_caught"]  # noqa: E731
    return {"by_score_caught": t_interval([key(r, "by_score") for r in rows]),
            "by_loss_caught": t_interval([key(r, "by_expected_loss")
                                          for r in rows]),
            "paired_gain": t_interval([r["compare"]["dollars_gain"]
                                       for r in rows]),
            "fraud_dollars": t_interval([r["compare"]["by_score"]
                                         ["fraud_dollars"] for r in rows])}


# ----------------------------------------------------------- the data
def ulb_parts():
    """{seed: (y_test, amounts)} from F166's rebuilt split."""
    import data as dmod
    df = dmod.load_ulb().drop_duplicates().reset_index(drop=True)

    def one(seed):
        s = dmod.stratified_split(df, seed)
        return s.y_test.to_numpy().astype(int), \
            s.X_test["Amount"].to_numpy(float)
    return one


def ieee_parts():
    """Month 4's eval part, the same rows for every seed (F174)."""
    import data as dmod
    import ieee_loader
    import ieee_splits
    df, _ = ieee_loader.dedupe_ieee(dmod.load_ieee_cis_train())
    folds = {int(f.eval_month): f for f in
             ieee_splits.rolling_origin_folds(df, n_folds=4)}
    parts = ieee_splits.split_xy(df, folds[4])
    y = parts["y_eval"].to_numpy().astype(int)
    a = parts["X_eval"]["TransactionAmt"].to_numpy(float)
    return lambda seed: (y, a)


def dataset_rows(name: str, parts) -> list[dict]:
    spec = SOURCES[name]
    doc = json.loads(spec["result"].read_text(encoding="utf-8"))
    out = []
    for r in doc["rows"]:
        seed = r["seed"]
        block = r["lanes"][spec["lane"]]["outcome"]
        y_s, p_s = checked_scores(block)
        y_r, a = parts(seed)
        y, s, a = joined(y_s, p_s, y_r, a)
        c = compare(y, s, a)
        loss_block = orec.record(f"f185_{name}_expected_loss", seed, y, s * a)
        score_block = orec.record(f"f185_{name}_score", seed, y, s,
                                  source=block["test_scores"])
        out.append({"seed": seed, "n_test": int(len(y)),
                    "n_positives": int(y.sum()), "compare": c,
                    "outcome_by_score": score_block,
                    "outcome_by_expected_loss": loss_block})
        print(f"{name} {seed}: gain {c['dollars_gain']:.2f}", flush=True)
    return out


def require_fired(check: dict) -> None:
    """The entry's check, before any amount is joined."""
    if not (check["can_fire"] and check["label_flip_refused"]):
        raise RuntimeError(f"the check did not fire: {check}")


def final_doc(check: dict, datasets: dict) -> dict:
    """The result, `complete` only when every dataset has ten seeds."""
    short = {k: len(v["rows"]) for k, v in datasets.items()
             if len(v["rows"]) != 10}
    if short or set(datasets) != set(SOURCES):
        raise RuntimeError(f"datasets incomplete: {short or sorted(datasets)}")
    return {"card": "F185", "sprint": 32, "phase": 2, "evidence_tag": "SIM",
            "metered_seconds": 0,
            "entry": "experiments/phase2/PREREGISTRATION_DRAFT.md section 6, "
                     "F185 (2026-11-09)",
            "budget": BUDGET, "review_costs": list(REVIEW_COSTS),
            "scores": "stored champion scores used as given, not "
                      "recalibrated",
            "check": check, "datasets": datasets, "complete": True}


def run() -> None:
    import provenance
    rid, _ = provenance.start(OUT, resumable=False)
    check = {**can_fire(), **refusal_fires()}
    print("check", json.dumps(check), flush=True)
    require_fired(check)
    datasets = {}
    for name, parts in (("ulb", ulb_parts), ("ieee_cis", ieee_parts)):
        rows = dataset_rows(name, parts())
        datasets[name] = {"source": SOURCES[name]["result"].relative_to(
                              ROOT).as_posix(),
                          "lane": SOURCES[name]["lane"],
                          "amount_column": SOURCES[name]["amount"],
                          "unit": SOURCES[name]["unit"],
                          "rows": rows, "over_seeds": over_seeds(rows)}
    doc = final_doc(check, datasets)
    seeds = sorted({r["seed"] for d in datasets.values() for r in d["rows"]})
    provenance.write_result(OUT, doc, __file__, seeds, rid)
    print("complete", flush=True)


if __name__ == "__main__":
    run()
