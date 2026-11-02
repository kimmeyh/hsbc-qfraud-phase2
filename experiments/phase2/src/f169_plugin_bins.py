"""F169 (Sprint 30 Task F, #80): the F108 plug-in with two estimators set
for extreme imbalance.

The entry is the 2026-10-31 amendment to "F108" in
`experiments/phase2/PREREGISTRATION_DRAFT.md` section 6 (Sprint 30 D3,
option 1), committed before this module existed. F108's generator,
seeds, arms, margin and pass rule are imported from `f108_ceiling`,
unchanged. F108's inferred cause of HGB's failure on its reference arm:
255 quantile bins put a top-0.05% threshold inside one bin, possibly
with early stopping on few positives. HGB cannot take more than 255
bins (scikit-learn 1.9.0 refuses 256), so the two arms are:

- `hgb_no_es`: HGB, F108's settings, early stopping off;
- `lgbm_bins`: LightGBM with HGB's shape (100 trees, learning rate 0.1,
  31 leaves, 20 rows per leaf), `max_bin` 4095, no early stopping.

Each is scored as F108's plug-in (the mean of min(p, 1 - p) on the test
window, against the Bayes error) on the full training window. The pass
rule is F108's: recovered on 4 of 5 seeds on the main, no-noise arm.

    <venv python> experiments/phase2/src/f169_plugin_bins.py

Zero metered seconds. Writes `experiments/phase2/results/f169_plugin_bins.json`
through `provenance.write_result` after each seed; resumable by seed,
`complete` true at the end and a final `complete` line on stdout.
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
import f108_ceiling as fc  # noqa: E402  (Phase 2, F108; not edited)

OUT = ROOT / "experiments" / "phase2" / "results" / "f169_plugin_bins.json"
# F168 part 7: a long run resumes through provenance.start.
LONG_RUN = True
ESTIMATORS = ("hgb_no_es", "lgbm_bins")
LGBM_MAX_BIN = 4095
DECIDING_ARM = "none"                  # F108's main, no-noise arm


def make(name: str, seed: int):
    if name == "hgb_no_es":
        from sklearn.ensemble import HistGradientBoostingClassifier
        return HistGradientBoostingClassifier(random_state=seed,
                                              early_stopping=False)
    if name == "lgbm_bins":
        from lightgbm import LGBMClassifier
        return LGBMClassifier(n_estimators=100, learning_rate=0.1,
                              num_leaves=31, min_child_samples=20,
                              max_bin=LGBM_MAX_BIN, random_state=seed,
                              verbose=-1)
    raise ValueError(f"unknown estimator {name!r}")


def plugin(arm: str, name: str, seed: int, Xtr, ytr, Xte, yte, eta_te) -> dict:
    import outcome_record as orec
    from sklearn.metrics import average_precision_score
    t0 = time.perf_counter()
    p = make(name, seed).fit(Xtr, ytr).predict_proba(Xte)[:, 1]
    bayes = float(np.mean(np.minimum(eta_te, 1 - eta_te)))
    est = float(np.mean(np.minimum(p, 1 - p)))
    return {"estimate": est, "bayes_error": bayes,
            "ratio": est / bayes if bayes else None,
            "recovered": fc.recovered(est, bayes),
            "auprc": float(average_precision_score(yte, p)),
            "bayes_auprc": float(average_precision_score(yte, eta_te)),
            "fit_s": round(time.perf_counter() - t0, 1),
            "outcome": orec.record(f"f169_{arm}_{name}", seed, yte, p)}


def labels(d: dict, eta: np.ndarray) -> dict:
    """F108's three arms at F108's noise rates, from F108's noise stream
    (seed + 7). The flip arm's labels are a new draw, not F108's: F108's
    `seed_run` takes a Cover-Hart subsample from the same stream between
    the two noise arms, and this does not (PR 74 review). The `none` arm,
    which decides the reading, has no noise, and the Bayes errors are
    exact, so the reading does not depend on it."""
    X = np.column_stack([d["amount"], d["mu"], d["time"]])
    rng = np.random.default_rng(d["seed"] + 7)
    out = {}
    for name, rates in fc.NOISE.items():
        y, e = fc.add_noise(d["y_main"], eta, rates, rng)
        out[name] = (X, y, e)
    ref_eta = (d["base_amount"] > fc.S1_AMOUNT).astype(float)
    out["reference"] = (np.column_stack([d["base_amount"], d["mu"],
                                         d["time"]]), d["y_ref"], ref_eta)
    return out


def seed_run(seed: int) -> dict:
    t0 = time.perf_counter()
    d = fc.generate(seed)
    d["seed"] = seed
    tr = (d["day"] >= fc.TRAIN_DAYS[0]) & (d["day"] <= fc.TRAIN_DAYS[1])
    te = (d["day"] >= fc.TEST_DAYS[0]) & (d["day"] <= fc.TEST_DAYS[1])
    pi_t, q = fc.world_rates(d, te)
    eta = fc.posterior(d["amount"], d["mu"], pi_t, q)
    check = fc.generator_check(d["y_main"][te], eta[te])
    row = {"seed": seed, "n_train": int(tr.sum()), "n_test": int(te.sum()),
           "generator_check": check, "arms": {}}
    if not check["pass"]:
        row["stopped"] = "generator check failed"
        return row
    for arm, (X, y, e) in labels(d, eta).items():
        row["arms"][arm] = {name: plugin(arm, name, seed, X[tr], y[tr], X[te],
                                         y[te], e[te]) for name in ESTIMATORS}
    row["seconds"] = round(time.perf_counter() - t0, 1)
    print(f"  s{seed} " + " | ".join(
        f"{a}/{n}: est {v[n]['estimate']:.5f} bayes {v[n]['bayes_error']:.5f}"
        f" rec {v[n]['recovered']} "
        f"auprc {v[n]['auprc']:.3f}" for a, v in row["arms"].items()
        for n in ESTIMATORS) + f" {row['seconds']} s", flush=True)
    return row


def summarize(rows: list) -> dict:
    """Recovered seeds per arm and estimator, out of every seed run (a
    stopped seed is a miss, as F108 counts), the pass on the deciding
    arm, and the attribution D3 names."""
    out = {}
    for arm in list(fc.NOISE) + ["reference"]:
        live = [r for r in rows if arm in r["arms"]]
        out[arm] = {n: {"seeds_recovered": sum(r["arms"][arm][n]["recovered"]
                                               for r in live),
                        "n_seeds": len(rows),
                        "recovers": bool(live) and sum(
                            r["arms"][arm][n]["recovered"] for r in live)
                        >= min(fc.PASS_SEEDS, len(rows))}
                    for n in ESTIMATORS}
    passes = {n: out[DECIDING_ARM][n]["recovers"] for n in ESTIMATORS}
    if passes["hgb_no_es"] and passes["lgbm_bins"]:
        reading = "both pass: early stopping, not bins, was the cause"
    elif passes["lgbm_bins"]:
        reading = "only LightGBM passes: the bins mattered"
    elif passes["hgb_no_es"]:
        reading = "only HGB without early stopping passes"
    else:
        reading = "neither passes: no plug-in is validated; F114 stays blocked"
    return {"by_arm": out, "deciding_arm": DECIDING_ARM, "passes": passes,
            "reading": reading}


def _doc(rows, complete=False):
    return {"card": "F169", "sprint": 30, "phase": 2, "evidence_tag": "SIM",
            "metered_seconds": 0,
            "entry": "experiments/phase2/PREREGISTRATION_DRAFT.md section 6, "
                     "F108, amendment 2026-10-31 (F169)",
            "estimators": {"hgb_no_es": "HistGradientBoostingClassifier("
                                        "early_stopping=False)",
                           "lgbm_bins": f"LGBMClassifier(n_estimators=100, "
                                        f"learning_rate=0.1, num_leaves=31, "
                                        f"min_child_samples=20, "
                                        f"max_bin={LGBM_MAX_BIN})"},
            "margin": {"abs": fc.MARGIN_ABS, "rel": fc.MARGIN_REL},
            "pass_seeds": fc.PASS_SEEDS, "seeds": [r["seed"] for r in rows],
            "rows": rows, "summary": summarize(rows), "complete": complete}


def main() -> int:
    import provenance
    rid, resume = provenance.start(OUT)
    rows = json.loads(OUT.read_text(encoding="utf-8"))["rows"] if resume else []
    for seed in fc.SEEDS:
        if seed in {r["seed"] for r in rows}:
            continue           # resume: never redo a seed
        rows.append(seed_run(seed))
        provenance.write_result(OUT, _doc(rows), __file__,
                                [r["seed"] for r in rows], rid)
    doc = _doc(rows, complete=True)
    provenance.write_result(OUT, doc, __file__, [r["seed"] for r in rows], rid)
    print(json.dumps(doc["summary"], indent=1))
    print("complete", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
