"""F114 gate (Sprint 28 Task G, #53): an isotonic-calibrated plug-in on
F108's simulator.

The entry is the dated amendment to "F108" in
`experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, committed before
this module existed. F108's generator, posterior, splits, seeds, arms and
margin are imported from `f108_ceiling`, unchanged. Only the plug-in's
model changes: F151's stable HGB, fit on 75% of train, with isotonic
calibration on the held-out 25%.

    <venv python> experiments/phase2/src/f114_calibrated_plugin.py pilot
    <venv python> experiments/phase2/src/f114_calibrated_plugin.py run

Zero metered seconds. Writes `experiments/phase2/results/f114_calibrated_plugin.json`
(the pilot writes `f114_calibrated_plugin_pilot.json`).
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

OUT = fc.ROOT / "experiments" / "phase2" / "results" / "f114_calibrated_plugin.json"
OUT_PILOT = OUT.with_name("f114_calibrated_plugin_pilot.json")
HOLDOUT = 0.25
L2 = 1.0                       # F151's REFERENCE_VARIANT, "l2_1p0"
DECIDING_ARM = "none"


def split_train(y: np.ndarray, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """75/25 of the training rows, stratified on the label, once per seed."""
    from sklearn.model_selection import train_test_split
    idx = np.arange(len(y))
    fit, hold = train_test_split(idx, test_size=HOLDOUT, stratify=y,
                                 random_state=seed)
    return np.sort(fit), np.sort(hold)


def plugin(p: np.ndarray) -> float:
    return float(np.mean(np.minimum(p, 1 - p)))


def calibrate(p_hold: np.ndarray, y_hold: np.ndarray,
              p_test: np.ndarray) -> np.ndarray:
    """Isotonic map from held-out probabilities to held-out labels."""
    from sklearn.isotonic import IsotonicRegression
    iso = IsotonicRegression(out_of_bounds="clip", y_min=0.0, y_max=1.0)
    return iso.fit(p_hold, y_hold).predict(p_test)


def calibrated_plugins(Xtr, ytr, Xte, seed) -> dict:
    """Uncalibrated and isotonic-calibrated plug-ins from one 75% model."""
    from sklearn.ensemble import HistGradientBoostingClassifier
    fit, hold = split_train(ytr, seed)
    m = HistGradientBoostingClassifier(l2_regularization=L2,
                                       random_state=seed).fit(Xtr[fit], ytr[fit])
    p_raw = m.predict_proba(Xte)[:, 1]
    p_cal = calibrate(m.predict_proba(Xtr[hold])[:, 1], ytr[hold], p_raw)
    return {"uncalibrated": plugin(p_raw), "calibrated": plugin(p_cal),
            "n_fit": int(len(fit)), "n_holdout": int(len(hold))}


def score_arm(Xtr, ytr, Xte, eta_te, seed, rng) -> dict:
    bayes = float(np.mean(np.minimum(eta_te, 1 - eta_te)))
    # F108's score_arm draws its Cover-Hart subsample from the shared
    # stream; drawing it here too keeps the next arm's noisy labels F108's.
    rng.choice(len(eta_te), min(fc.NN_TEST_ROWS, len(eta_te)), replace=False)
    est = calibrated_plugins(Xtr, ytr, Xte, seed)
    return {"bayes_error": bayes, **est,
            "calibrated_recovered": fc.recovered(est["calibrated"], bayes),
            "uncalibrated_recovered": fc.recovered(est["uncalibrated"], bayes)}


def seed_run(seed: int) -> dict:
    """F108's seed_run, with only the plug-in replaced."""
    t0 = time.perf_counter()
    d = fc.generate(seed)
    tr = (d["day"] >= fc.TRAIN_DAYS[0]) & (d["day"] <= fc.TRAIN_DAYS[1])
    te = (d["day"] >= fc.TEST_DAYS[0]) & (d["day"] <= fc.TEST_DAYS[1])
    X = np.column_stack([d["amount"], d["mu"], d["time"]])
    pi_t, q = fc.world_rates(d, te)
    eta = fc.posterior(d["amount"], d["mu"], pi_t, q)
    check = fc.generator_check(d["y_main"][te], eta[te])
    row = {"seed": seed, "n_train": int(tr.sum()), "n_test": int(te.sum()),
           "generator_check": check, "arms": {}}
    if not check["pass"]:
        row["stopped"] = "generator check failed"
        return row
    rng = np.random.default_rng(seed + 7)          # F108's noise stream
    for name, rates in fc.NOISE.items():
        y, e = fc.add_noise(d["y_main"], eta, rates, rng)
        row["arms"][name] = score_arm(X[tr], y[tr], X[te], e[te], seed, rng)
    ref_eta = (d["base_amount"] > fc.S1_AMOUNT).astype(float)
    Xref = np.column_stack([d["base_amount"], d["mu"], d["time"]])
    row["arms"]["reference"] = score_arm(Xref[tr], d["y_ref"][tr], Xref[te],
                                         ref_eta[te], seed, rng)
    row["seconds"] = round(time.perf_counter() - t0, 1)
    print(f"  s{seed} " + " | ".join(
        f"{a}: bayes {v['bayes_error']:.5f} cal {v['calibrated']:.5f} "
        f"raw {v['uncalibrated']:.5f}" for a, v in row["arms"].items())
        + f" {row['seconds']} s", flush=True)
    return row


def summarize(rows: list) -> dict:
    # Out of every seed run: a stopped seed is a miss (F108's convention).
    out = {}
    for arm in list(fc.NOISE) + ["reference"]:
        live = [r for r in rows if arm in r["arms"]]
        out[arm] = {}
        for k in ("calibrated", "uncalibrated"):
            n = sum(r["arms"][arm][f"{k}_recovered"] for r in live)
            # Always the preregistered count: a one-seed pilot cannot reach
            # it, so it can never read as "recovers".
            out[arm][k] = {"seeds_recovered": int(n), "n_seeds": len(rows),
                           "recovers": bool(live and n >= fc.PASS_SEEDS)}
    return out


def verdict(summary: dict, mode: str) -> dict:
    """The gate verdict, for `run` only. A pilot gets no gate verdict."""
    if mode == "pilot":
        return {"deciding_arm": DECIDING_ARM, "f114": "pilot only, not a gate",
                "pass_seeds": fc.PASS_SEEDS}
    if mode != "run":
        raise ValueError(f"unknown mode {mode!r}")
    ok = summary[DECIDING_ARM]["calibrated"]["recovers"]
    return {"deciding_arm": DECIDING_ARM, "calibrated_plugin_recovers": ok,
            "f114": "eligible: real-data run with this plug-in" if ok
                    else "stays blocked: the calibrated plug-in does not recover"}


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    mode = argv[0] if argv else "pilot"
    if mode not in ("pilot", "run"):
        raise SystemExit("usage: f114_calibrated_plugin.py pilot|run")
    seeds = fc.SEEDS[:1] if mode == "pilot" else fc.SEEDS
    t0 = time.perf_counter()
    rows = [seed_run(s) for s in seeds]
    summary = summarize(rows)
    res = {"generator": "experiments/phase2/src/f114_calibrated_plugin.py",
           "card": "F114", "sprint": 28, "phase": 2, "evidence_tag": "SIM",
           "metered_seconds": 0, "date": time.strftime("%Y-%m-%d"),
           "entry": "experiments/phase2/PREREGISTRATION_DRAFT.md section 6, "
                    "F108, amendment 2026-10-22",
           "model": {"hgb_l2_regularization": L2, "holdout": HOLDOUT,
                     "calibration": "isotonic"},
           "margin": {"abs": fc.MARGIN_ABS, "rel": fc.MARGIN_REL},
           "mode": mode, "seeds": list(seeds), "rows": rows,
           "summary": summary, "verdict": verdict(summary, mode),
           "elapsed_s": round(time.perf_counter() - t0, 1)}
    (OUT_PILOT if mode == "pilot" else OUT).write_text(
        json.dumps(res, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"summary": summary, "verdict": res["verdict"]}, indent=1))
    return 1 if any("stopped" in r for r in rows) else 0


if __name__ == "__main__":
    raise SystemExit(main())
