"""F170 (Sprint 30 Task G, #81): ULB frauds missed by every model, are
their nearest neighbors legitimate?

The entry is "F170" in `experiments/phase2/PREREGISTRATION_DRAFT.md`
section 6, committed before this module existed. F158 step 3 compared
group means only. Here, row by row: for each ULB test fraud, the share of
legitimate rows among its k = 10 nearest training rows (Euclidean, on the
30 features standardized on the training rows), missed by every family
against caught by some, on F158's families and split, seeds 42-51.

The simulator check runs first: on F108's world (seed 42, main arm),
frauds the Bayes classifier calls legitimate (posterior below 0.5)
against the rest. There the answer is known, so the comparison has a
case where it must differ; if it does not, the ULB reading is not made.

    <venv python> experiments/phase2/src/f170_missed_neighbors.py

Zero metered seconds. Reads the stored predictions in
`experiments/results/predictions/` (Phase 1 evidence, read only). Writes
`experiments/phase2/results/f170_missed_neighbors.json` through
`provenance.write_result`, after the check and at the end.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "experiments" / "src"))

OUT = ROOT / "experiments" / "phase2" / "results" / "f170_missed_neighbors.json"
# F168 part 7: a long run resumes through provenance.start.
LONG_RUN = True
K = 10
ALPHA = 0.05
CHECK_SEED = 42


def legit_share(Xtr, ytr, Xq, k: int = K) -> np.ndarray:
    """For each query row, the share of legitimate rows (label 0) among its
    k nearest training rows, after standardizing on the training rows."""
    from scipy.spatial import cKDTree
    mu, sd = Xtr.mean(axis=0), Xtr.std(axis=0)
    sd = np.where(sd > 0, sd, 1.0)
    tree = cKDTree((Xtr - mu) / sd)
    _, idx = tree.query((Xq - mu) / sd, k=k)
    return (np.asarray(ytr)[idx] == 0).mean(axis=1)


def compare(missed: np.ndarray, caught: np.ndarray) -> dict:
    """Two-sided Mann-Whitney U on the legitimate shares (two independent
    groups, no pairing). "Higher" means missed frauds sit among more
    legitimate rows than caught ones."""
    from scipy import stats
    missed, caught = np.asarray(missed, float), np.asarray(caught, float)
    if len(missed) == 0 or len(caught) == 0:
        return {"n_missed": len(missed), "n_caught": len(caught),
                "p": None, "rejects": False, "direction": "no test"}
    u = stats.mannwhitneyu(missed, caught, alternative="two-sided")
    rejects = bool(u.pvalue < ALPHA)
    return {"n_missed": int(len(missed)), "n_caught": int(len(caught)),
            "missed_median": float(np.median(missed)),
            "caught_median": float(np.median(caught)),
            "missed_mean": float(missed.mean()),
            "caught_mean": float(caught.mean()),
            "missed_share_majority_legit": float(np.mean(missed > 0.5)),
            "caught_share_majority_legit": float(np.mean(caught > 0.5)),
            "u": float(u.statistic), "p": float(u.pvalue), "rejects": rejects,
            "direction": ("higher" if rejects and np.median(missed) >
                          np.median(caught) else
                          "lower" if rejects else "no difference")}


def simulator_check(seed: int = CHECK_SEED) -> dict:
    """F108's world: frauds below the Bayes boundary must sit among more
    legitimate rows than frauds above it."""
    import f108_ceiling as fc
    d = fc.generate(seed)
    tr = (d["day"] >= fc.TRAIN_DAYS[0]) & (d["day"] <= fc.TRAIN_DAYS[1])
    te = (d["day"] >= fc.TEST_DAYS[0]) & (d["day"] <= fc.TEST_DAYS[1])
    pi_t, q = fc.world_rates(d, te)
    eta = fc.posterior(d["amount"], d["mu"], pi_t, q)
    X = np.column_stack([d["amount"], d["mu"], d["time"]])
    y = d["y_main"]
    fr = te & (y == 1)
    share = legit_share(X[tr], y[tr], X[fr])
    below = eta[fr] < 0.5
    res = compare(share[below], share[~below])
    return {"seed": seed, "frauds": int(fr.sum()),
            "below_bayes_boundary": int(below.sum()), **res,
            "fires": bool(res["direction"] == "higher")}


def ulb() -> dict:
    import data
    import f154_confusion as fcf
    import f158_fraud_types as f158
    import outcome_record as orec
    df = data.load_ulb().drop_duplicates().reset_index(drop=True)
    fams = fcf.families()
    shares, missed_ids, per_seed, off = [], [], [], {}
    for seed in fcf.SEEDS:
        s = data.stratified_split(df, seed)
        y = s.y_test.to_numpy().astype(int)
        flags = []
        for fam in fams:
            st = fcf.load(fam, seed)
            if not f158.on_split(st["y_test"], y):
                off.setdefault(fam, []).append(seed)
                continue
            flags.append(orec.flagged_at_budget(st["p_test"], orec.ALERT_BUDGET))
        miss = f158.missed_by_all(y, flags)
        fr = y == 1
        share = legit_share(s.X_train.to_numpy(np.float64),
                            s.y_train.to_numpy().astype(int),
                            s.X_test.to_numpy(np.float64)[fr])
        ids = s.X_test.index.to_numpy()[fr]
        for i, sh, m in zip(ids, share, miss[fr]):
            shares.append({"row": int(i), "seed": seed, "share": float(sh),
                           "missed": bool(m)})
        missed_ids += [int(i) for i, m in zip(ids, miss[fr]) if m]
        per_seed.append({"seed": seed, "families": len(flags),
                         "frauds": int(fr.sum()), "missed_by_all": int(miss.sum())})
    # Distinct frauds: a row is in several seeds' test folds. Its share is
    # the mean over its appearances; it is "missed" if missed in every one,
    # "caught" if caught in every one, "mixed" otherwise.
    by_row: dict[int, list] = {}
    for r in shares:
        by_row.setdefault(r["row"], []).append(r)
    groups = {"missed": [], "caught": [], "mixed": []}
    for row, rs in by_row.items():
        m = [r["missed"] for r in rs]
        g = "missed" if all(m) else "caught" if not any(m) else "mixed"
        groups[g].append(float(np.mean([r["share"] for r in rs])))
    pairs = compare([r["share"] for r in shares if r["missed"]],
                    [r["share"] for r in shares if not r["missed"]])
    return {"families": [f for f in fams if f not in off],
            "off_split_families": off, "per_seed": per_seed,
            "pairs_missed": int(sum(r["missed"] for r in shares)),
            "pairs_total": len(shares),
            "distinct_missed_rows": sorted(set(missed_ids)),
            "distinct": {"missed": len(groups["missed"]),
                         "caught": len(groups["caught"]),
                         "mixed": len(groups["mixed"])},
            "primary": compare(groups["missed"], groups["caught"]),
            "secondary_pairs": pairs}


def reading(check: dict, res: dict | None) -> str:
    if not check["fires"]:
        return ("the simulator check did not separate the groups; the "
                "comparison cannot show the reading, and no ULB reading is "
                "made")
    p = res["primary"]
    if p["direction"] == "higher" and p["missed_median"] > 0.5:
        return ("missed frauds sit among mostly legitimate rows, more than "
                "caught frauds: consistent with ULB's information limit")
    return ("missed frauds do not sit among more legitimate rows than "
            "caught frauds, or not mostly legitimate: a model weakness "
            "remains open")


def _doc(check, res=None, complete=False):
    return {"card": "F170", "sprint": 30, "phase": 2, "evidence_tag": "SIM",
            "metered_seconds": 0,
            "entry": "experiments/phase2/PREREGISTRATION_DRAFT.md section 6, "
                     "F170",
            "k": K, "distance": "Euclidean on features standardized on the "
                                "training rows", "alpha": ALPHA,
            "test": "two-sided Mann-Whitney U, distinct frauds",
            "simulator_check": check, "ulb": res,
            "reading": reading(check, res) if res or not check["fires"]
            else None, "complete": complete}


def main() -> int:
    import provenance
    import f154_confusion as fcf
    rid, resume = provenance.start(OUT)
    prior = json.loads(OUT.read_text(encoding="utf-8")) if resume else {}
    t0 = time.perf_counter()
    check = prior.get("simulator_check") or simulator_check()
    provenance.write_result(OUT, _doc(check), __file__, [CHECK_SEED], rid)
    print("check", json.dumps({k: check[k] for k in
                               ("direction", "p", "fires")}), flush=True)
    res = ulb() if check["fires"] else None
    doc = _doc(check, res, complete=True)
    doc["seconds"] = round(time.perf_counter() - t0, 1)
    provenance.write_result(OUT, doc, __file__, list(fcf.SEEDS), rid)
    print(doc["reading"])
    print("complete", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
