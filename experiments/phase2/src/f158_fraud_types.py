"""F158 (Sprint 29 Task G, #70): per-type detectors against one model, on
F108's simulator.

The entry is "F158" in `experiments/phase2/PREREGISTRATION_DRAFT.md`
section 6, committed before this module existed (43eb2bb). F108's
generator, splits and day ranges are imported from `f108_ceiling`,
unchanged; F154's stored-prediction readers from `f154_confusion`.

  1. Per seed (42-49): the single model, the cascade (an S2 detector and an
     S3 detector, a row's score the larger probability) and the shuffled
     reference, each scored by recall of all test fraud in the top 0.5% of
     test rows. Primary test: cascade minus single, exact two-sided
     Wilcoxon at 0.05 with a 95% t interval.
  2. Step 2 (ULB and IEEE-CIS clustering) runs only if the primary test
     reads "cascade above" and the shuffled reference does not; this
     module records whether the condition holds and does not run it.
  3. Descriptive: the ULB test frauds every on-split F154 family misses at
     the budget, against the caught ones, feature by feature.

    <venv python> experiments/phase2/src/f158_fraud_types.py

Zero metered seconds. Writes `experiments/phase2/results/f158_fraud_types.json`
through `provenance.write_result`, after each seed, with `complete` true at
the end; resumable by seed (`provenance.run_id_for`).
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import f108_ceiling as fc  # noqa: E402  (Phase 2, F108; not edited)

ROOT = fc.ROOT
sys.path.insert(0, str(ROOT / "experiments" / "src"))
OUT = ROOT / "experiments" / "phase2" / "results" / "f158_fraud_types.json"
SEEDS = tuple(range(42, 50))
DELAY = 7                      # a label is known 7 days after its day
ALPHA = 0.05
FEATURES = ("amount", "mu", "time", "amount_over_mu", "cust_txn_prev_day",
            "term_fraud_d14_d8", "term_txn_d14_d8", "term_fraud_d35_d8",
            "term_txn_d35_d8", "cust_fraud_d35_d8")
MODELS = ("single", "cascade", "shuffled")


# ---------------------------------------------------------------- features
def _per_day(ent: np.ndarray, day: np.ndarray, w: np.ndarray, n_ent: int,
             n_days: int) -> np.ndarray:
    """Cumulative sums: C[e, k] is the total of w for entity e before day k."""
    a = np.zeros((n_ent, n_days), dtype=float)
    np.add.at(a, (ent, day), w)
    c = np.zeros((n_ent, n_days + 1), dtype=float)
    np.cumsum(a, axis=1, out=c[:, 1:])
    return c


def _window(c: np.ndarray, ent: np.ndarray, day: np.ndarray, lo: int,
            hi: int) -> np.ndarray:
    """Per row, the entity's total over days day-lo .. day-hi, inclusive,
    clipped at day 0 (lo > hi >= 1)."""
    a = np.clip(day - lo, 0, None)
    b = np.clip(day - hi + 1, 0, None)
    return c[ent, b] - c[ent, a]


def features(d: dict) -> np.ndarray:
    """The entry's features, one column each, in FEATURES order. Every
    label-based window ends DELAY + 1 days before the row's day."""
    cust, term, day = d["customer"], d["terminal"], d["day"]
    nd = int(day.max()) + 1
    ones = np.ones(len(day))
    y = d["y_main"].astype(float)
    ct = _per_day(cust, day, ones, d["n_customers"], nd)
    tt = _per_day(term, day, ones, d["n_terminals"], nd)
    tf = _per_day(term, day, y, d["n_terminals"], nd)
    cf = _per_day(cust, day, y, d["n_customers"], nd)
    gap = DELAY + 1
    cols = [d["amount"], d["mu"], d["time"], d["amount"] / d["mu"],
            _window(ct, cust, day, 1, 1),
            _window(tf, term, day, 14, gap), _window(tt, term, day, 14, gap),
            _window(tf, term, day, 35, gap), _window(tt, term, day, 35, gap),
            _window(cf, cust, day, 35, gap)]
    return np.column_stack(cols)


# ---------------------------------------------------------------- models
def _hgb(X, y, seed):
    from sklearn.ensemble import HistGradientBoostingClassifier
    return HistGradientBoostingClassifier(l2_regularization=1.0,
                                          random_state=seed).fit(X, y)


def shuffled_types(s2: np.ndarray, s3: np.ndarray, seed: int):
    """The (S2, S3) pairs permuted among the frauds; non-frauds unchanged,
    so every fraud stays a fraud and keeps at least one type."""
    fraud = np.nonzero(s2 | s3)[0]
    perm = np.random.default_rng(seed + 11).permutation(len(fraud))
    a, b = s2.copy(), s3.copy()
    a[fraud], b[fraud] = s2[fraud][perm], s3[fraud][perm]
    return a, b


def cascade_scores(Xtr, s2, s3, Xte, seed) -> np.ndarray:
    p2 = _hgb(Xtr, s2.astype(int), seed).predict_proba(Xte)[:, 1]
    p3 = _hgb(Xtr, s3.astype(int), seed).predict_proba(Xte)[:, 1]
    return np.maximum(p2, p3)


def recall_at_budget(y, scores, mask=None) -> float:
    import outcome_record as orec
    f = orec.flagged_at_budget(scores, orec.ALERT_BUDGET)
    y = np.asarray(y).astype(bool)
    m = y if mask is None else (y & np.asarray(mask, bool))
    return float(f[m].sum() / m.sum()) if m.sum() else float("nan")


def seed_run(seed: int) -> dict:
    import outcome_record as orec
    from sklearn.metrics import average_precision_score
    t0 = time.perf_counter()
    d = fc.generate(seed)
    tr = (d["day"] >= fc.TRAIN_DAYS[0]) & (d["day"] <= fc.TRAIN_DAYS[1])
    te = (d["day"] >= fc.TEST_DAYS[0]) & (d["day"] <= fc.TEST_DAYS[1])
    X = features(d)
    y, s2, s3 = d["y_main"], d["hidden_s2"], d["hidden_s3"]
    sh2, sh3 = shuffled_types(s2[tr], s3[tr], seed)
    scores = {
        "single": _hgb(X[tr], y[tr], seed).predict_proba(X[te])[:, 1],
        "cascade": cascade_scores(X[tr], s2[tr], s3[tr], X[te], seed),
        "shuffled": cascade_scores(X[tr], sh2, sh3, X[te], seed)}
    yte = y[te]
    row = {"seed": seed, "n_train": int(tr.sum()), "n_test": int(te.sum()),
           "test_fraud": int(yte.sum()), "test_s2": int(s2[te].sum()),
           "test_s3": int(s3[te].sum()), "models": {}, "outcomes": []}
    for name, p in scores.items():
        row["models"][name] = {
            "recall_at_budget": recall_at_budget(yte, p),
            "recall_s2": recall_at_budget(yte, p, s2[te]),
            "recall_s3": recall_at_budget(yte, p, s3[te]),
            "auprc": float(average_precision_score(yte, p))}
        row["outcomes"].append(orec.record(f"f158_{name}", seed, yte, p))
    row["seconds"] = round(time.perf_counter() - t0, 1)
    print(f"  s{seed} " + " | ".join(
        f"{k} {v['recall_at_budget']:.4f}" for k, v in row["models"].items())
        + f" {row['seconds']} s", flush=True)
    return row


# ---------------------------------------------------------------- tests
def paired_test(diffs) -> dict:
    """Exact two-sided Wilcoxon and a 95% t interval on per-seed diffs."""
    from scipy import stats
    import f154_confusion as fcf
    v = np.asarray(diffs, dtype=float)
    ci = fcf.t_interval(v, 1 - ALPHA)
    if np.all(v == 0):
        w = {"statistic": None, "p": 1.0, "note": "every difference is zero"}
    else:
        r = stats.wilcoxon(v, alternative="two-sided", method="exact")
        w = {"statistic": float(r.statistic), "p": float(r.pvalue)}
    rejects = w["p"] < ALPHA
    if rejects and ci["low"] > 0:
        reading = "above"
    elif rejects and ci["high"] < 0:
        reading = "below"
    else:
        reading = "no reliable difference"
    return {"n": int(len(v)), "wilcoxon": w, "t_interval": ci,
            "reading": reading}


def summarize(rows: list) -> dict:
    def diff(a, b):
        return [r["models"][a]["recall_at_budget"]
                - r["models"][b]["recall_at_budget"] for r in rows]
    primary = paired_test(diff("cascade", "single"))
    shuffled = paired_test(diff("shuffled", "single"))
    go = primary["reading"] == "above" and shuffled["reading"] != "above"
    return {"primary_cascade_minus_single": primary,
            "secondary_shuffled_minus_single": shuffled,
            "step2_condition_met": go,
            "step2": ("condition met; not run in this module, see the entry"
                      if go else "not run: the primary test does not read "
                      "'cascade above' with the shuffled reference not above")}


# ---------------------------------------------------------------- step 3
def missed_by_all(y, flags: list) -> np.ndarray:
    """True for each fraud that no flag array catches."""
    y = np.asarray(y).astype(bool)
    caught = np.zeros_like(y)
    for f in flags:
        caught |= np.asarray(f, bool)
    return y & ~caught


def step3() -> dict:
    import data
    import f154_confusion as fcf
    import outcome_record as orec
    df = data.load_ulb().drop_duplicates().reset_index(drop=True)
    fams = fcf.families()
    per_seed, missed_rows, caught_rows, off_split = [], [], [], {}
    for seed in fcf.SEEDS:
        x_te = fcf.test_features(seed, df)
        y = df.loc[x_te.index, data.LABEL_COL].to_numpy().astype(int)
        flags = []
        for fam in fams:
            st = fcf.load(fam, seed)
            ys = np.asarray(st["y_test"]).astype(int)
            if len(ys) != len(y) or not np.array_equal(ys, y):
                off_split.setdefault(fam, []).append(seed)
                continue
            flags.append(orec.flagged_at_budget(st["p_test"], orec.ALERT_BUDGET))
        miss = missed_by_all(y, flags)
        per_seed.append({"seed": seed, "families": len(flags),
                         "frauds": int(y.sum()), "missed_by_all": int(miss.sum())})
        missed_rows.append(x_te[miss])
        caught_rows.append(x_te[(y == 1) & ~miss])
    import pandas as pd
    m, c = pd.concat(missed_rows), pd.concat(caught_rows)
    cols = {k: {"missed_mean": float(m[k].mean()), "missed_sd": float(m[k].std()),
                "caught_mean": float(c[k].mean()), "caught_sd": float(c[k].std())}
            for k in m.columns}
    return {"families": [f for f in fams if f not in off_split],
            "off_split_families": off_split, "per_seed": per_seed,
            "rows_missed": int(len(m)), "rows_caught": int(len(c)),
            "features": cols, "test": "none (descriptive)"}


# ---------------------------------------------------------------- run
def _doc(rows, extra=None):
    doc = {"card": "F158", "sprint": 29, "phase": 2, "evidence_tag": "SIM",
           "metered_seconds": 0,
           "entry": "experiments/phase2/PREREGISTRATION_DRAFT.md section 6, "
                    "F158 (43eb2bb)",
           "features": list(FEATURES), "label_delay_days": DELAY,
           "alert_budget": 0.005, "seeds": [r["seed"] for r in rows],
           "rows": rows, "complete": False}
    if len(rows) == len(SEEDS):
        doc["summary"] = summarize(rows)
    doc.update(extra or {})
    return doc


def main(argv=None) -> int:
    import provenance
    resume = provenance.sidecar(OUT).exists() and OUT.exists()
    rid = provenance.run_id_for(OUT, resume=resume)
    rows = json.loads(OUT.read_text(encoding="utf-8"))["rows"] if resume else []
    done = {r["seed"] for r in rows}
    for seed in SEEDS:
        if seed in done:
            continue           # resume: never redo a seed
        rows.append(seed_run(seed))
        provenance.write_result(OUT, _doc(rows), __file__,
                                [r["seed"] for r in rows], rid)
    doc = _doc(rows, {"step3_ulb_missed_by_all": step3(), "complete": True})
    provenance.write_result(OUT, doc, __file__, [r["seed"] for r in rows], rid)
    print(json.dumps(doc["summary"]["primary_cascade_minus_single"]["reading"]))
    print("complete", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
