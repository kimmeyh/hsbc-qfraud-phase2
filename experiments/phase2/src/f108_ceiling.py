"""F108 (Sprint 27 Task K): ceiling validation on a simulator with hidden
state.

The entry is `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6,
"F108", written before this module existed; every choice is fixed there
and repeated here.

The generator is written clean-room from the prose of the Fraud
Detection Handbook (Le Borgne et al., chapter 3, "Simulated dataset",
CC BY-SA 4.0). The handbook's code is GPL-3.0 and was not read or copied.
Two deliberate departures, both stated in the entry: amounts are not
rounded, and scenario 3 selects each transaction with probability 1/3
rather than a third of them, so the posterior below is exact.

Known ceiling: with observed features (amount, customer mean amount,
time of day) and the compromise state hidden, the posterior is
    eta = 1 - (1 - pi_T)(1 - s)
    s   = q g(a/5)/5 / (q g(a/5)/5 + (1 - q) g(a))
on days where both compromise windows are full.

    <venv python> experiments/phase2/src/f108_ceiling.py pilot
    <venv python> experiments/phase2/src/f108_ceiling.py run

Zero metered seconds. Writes `experiments/phase2/results/f108_ceiling.json`
(the pilot writes `f108_ceiling_pilot.json`).
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "experiments" / "phase2" / "results" / "f108_ceiling.json"
OUT_PILOT = OUT.with_name("f108_ceiling_pilot.json")
SEEDS = (42, 43, 44, 45, 46)

N_CUSTOMERS, N_TERMINALS, N_DAYS, RADIUS, GRID = 5000, 10000, 183, 5.0, 100.0
DAY_S, TIME_MU, TIME_SD = 86400, 43200, 20000
S1_AMOUNT = 220.0
S2_PER_DAY, S2_DAYS = 2, 28
S3_PER_DAY, S3_DAYS, S3_FRACTION, S3_MULT = 3, 14, 1 / 3, 5.0
TRAIN_DAYS, TEST_DAYS = (28, 119), (120, 182)
NOISE = {"none": (0.0, 0.0), "flip": (0.05, 0.0005)}   # (pos->neg, neg->pos)
CURVE = (1 / 32, 1 / 16, 1 / 8, 1 / 4, 1 / 2, 1.0)
NN_TEST_ROWS = 100_000
MARGIN_ABS, MARGIN_REL, MARGIN_AUPRC = 0.0005, 0.10, 0.01
PASS_SEEDS = 4
CHECK_SD = 3.0


# --------------------------------------------------------------- generator

def generate(seed: int, n_customers: int = N_CUSTOMERS,
             n_terminals: int = N_TERMINALS, n_days: int = N_DAYS) -> dict:
    """Transactions with their hidden state, as column arrays."""
    from scipy.spatial import cKDTree
    rng = np.random.default_rng(seed)
    cxy = rng.uniform(0, GRID, (n_customers, 2))
    mu = rng.uniform(5, 100, n_customers)
    sd = mu / 2
    rate = rng.uniform(0, 4, n_customers)
    txy = rng.uniform(0, GRID, (n_terminals, 2))
    avail = cKDTree(txy).query_ball_point(cxy, RADIUS - 1e-12)
    has = np.array([len(a) > 0 for a in avail])

    counts = rng.poisson(rate[:, None] * has[:, None], (n_customers, n_days))
    cust = np.repeat(np.arange(n_customers), counts.sum(axis=1))
    day = np.concatenate([np.repeat(np.arange(n_days), c) for c in counts])
    n = len(cust)
    t = rng.normal(TIME_MU, TIME_SD, n)
    keep = (t >= 0) & (t < DAY_S)
    cust, day, t = cust[keep], day[keep], t[keep]
    n = len(cust)
    a0 = rng.normal(mu[cust], sd[cust])
    neg = a0 < 0
    a0[neg] = rng.uniform(0, 2 * mu[cust[neg]])
    sizes = np.array([len(avail[c]) for c in cust])
    pick = np.floor(rng.uniform(0, 1, n) * sizes).astype(int)
    term = np.array([avail[c][k] for c, k in zip(cust, pick)])

    compT = np.zeros((n_terminals, n_days), dtype=bool)
    compC = np.zeros((n_customers, n_days), dtype=bool)
    for k in range(n_days):
        for j in rng.choice(n_terminals, S2_PER_DAY, replace=False):
            compT[j, k:k + S2_DAYS] = True
        for j in rng.choice(n_customers, S3_PER_DAY, replace=False):
            compC[j, k:k + S3_DAYS] = True
    s2 = compT[term, day]
    s3 = compC[cust, day] & (rng.uniform(0, 1, n) < S3_FRACTION)
    amount = np.where(s3, a0 * S3_MULT, a0)
    return {"customer": cust, "day": day, "time": t, "amount": amount,
            "base_amount": a0, "mu": mu[cust], "terminal": term,
            "y_main": (s2 | s3).astype(int),
            "y_ref": (a0 > S1_AMOUNT).astype(int),
            "hidden_s2": s2, "hidden_s3": s3,
            "n_customers": n_customers, "n_terminals": n_terminals}


def amount_density(a: np.ndarray, mu: np.ndarray) -> np.ndarray:
    """g(a): N(mu, mu/2) on [0, inf) plus the negative draws' U[0, 2 mu]."""
    sd = mu / 2
    g = np.where(a >= 0, stats.norm.pdf(a, mu, sd), 0.0)
    return g + stats.norm.cdf(-mu / sd) * ((a >= 0) & (a <= 2 * mu)) / (2 * mu)


def priors(n_customers: int, n_terminals: int) -> tuple[float, float]:
    """(pi_T, q) on days where both windows are full."""
    pi_t = 1 - (1 - S2_PER_DAY / n_terminals) ** S2_DAYS
    q = S3_FRACTION * (1 - (1 - S3_PER_DAY / n_customers) ** S3_DAYS)
    return pi_t, q


def world_rates(d: dict, mask: np.ndarray) -> tuple[float, float]:
    """(pi_T, q) as realized on the masked rows. The compromise schedule is
    drawn once per world (2 terminals and 3 customers a day), so a world's
    rates scatter around `priors` far more than a row-level binomial
    allows; the known ceiling is the posterior at the realized rates."""
    return float(d["hidden_s2"][mask].mean()), float(d["hidden_s3"][mask].mean())


def posterior(amount, mu, pi_t: float, q: float) -> np.ndarray:
    f = q * amount_density(amount / S3_MULT, mu) / S3_MULT
    c = (1 - q) * amount_density(amount, mu)
    s = np.divide(f, f + c, out=np.ones_like(f), where=(f + c) > 0)
    return 1 - (1 - pi_t) * (1 - s)


def add_noise(y: np.ndarray, eta: np.ndarray, rates: tuple, rng) -> tuple:
    p2n, n2p = rates
    u = rng.uniform(0, 1, len(y))
    yn = np.where(y == 1, (u >= p2n).astype(int), (u < n2p).astype(int))
    return yn, (1 - p2n) * eta + n2p * (1 - eta)


def generator_check(y: np.ndarray, eta: np.ndarray) -> dict:
    """The realized labels against the exact posterior (the entry's stop)."""
    bayes = float(np.mean(np.minimum(eta, 1 - eta)))
    realized = float(np.mean((eta > 0.5).astype(int) != y))
    sd_err = float(np.sqrt(np.sum(np.minimum(eta, 1 - eta)
                                  * np.maximum(eta, 1 - eta))) / len(y))
    sd_rate = float(np.sqrt(np.sum(eta * (1 - eta))) / len(y))
    rate, mean_eta = float(y.mean()), float(eta.mean())
    ok_err = abs(realized - bayes) <= CHECK_SD * max(sd_err, 1e-12)
    ok_rate = abs(rate - mean_eta) <= CHECK_SD * max(sd_rate, 1e-12)
    return {"bayes_error": bayes, "bayes_classifier_error": realized,
            "sd_error": sd_err, "fraud_rate": rate, "mean_eta": mean_eta,
            "sd_rate": sd_rate, "pass": bool(ok_err and ok_rate)}


# ----------------------------------------------------------------- methods

def _hgb(X, y, seed):
    from sklearn.ensemble import HistGradientBoostingClassifier
    return HistGradientBoostingClassifier(random_state=seed).fit(X, y)


def fit_floor(n_pos: np.ndarray, err: np.ndarray) -> dict:
    """a N^(-b) + c by least squares; c is the floor."""
    from scipy.optimize import curve_fit

    def f(n, a, b, c):
        return a * n ** (-b) + c
    try:
        # A curve that does not fall (the zero-ceiling reference can be flat
        # or noisy) still needs a start inside the bounds.
        p0 = (max(float(err[0] - err[-1]), 1e-6), 0.5,
              float(np.clip(err.min(), 0, 1)))
        (a, b, c), _ = curve_fit(f, n_pos.astype(float), err, p0=p0,
                                 bounds=([0, 0, 0], [np.inf, 5, 1]),
                                 maxfev=20000)
        return {"a": float(a), "b": float(b), "c": float(c), "fit": True}
    except (RuntimeError, ValueError) as e:
        return {"a": None, "b": None, "c": None, "fit": False,
                "error": str(e)}


def cover_hart(Xtr, ytr, Xte, yte) -> dict:
    from sklearn.neighbors import KNeighborsClassifier
    m, s = Xtr.mean(axis=0), Xtr.std(axis=0)
    knn = KNeighborsClassifier(n_neighbors=1).fit((Xtr - m) / s, ytr)
    e = float(np.mean(knn.predict((Xte - m) / s) != yte))
    return {"nn_error": e, "lower": (1 - np.sqrt(max(0.0, 1 - 2 * e))) / 2,
            "upper": e}


def recovered(est, true) -> bool:
    return bool(est is not None
                and abs(est - true) <= max(MARGIN_ABS, MARGIN_REL * true))


def score_arm(Xtr, ytr, Xte, yte, eta_te, seed, rng) -> dict:
    from sklearn.metrics import average_precision_score
    bayes_err = float(np.mean(np.minimum(eta_te, 1 - eta_te)))
    bayes_ap = float(average_precision_score(yte, eta_te))
    order = np.random.default_rng(seed).permutation(len(ytr))
    curve = []
    for frac in CURVE:
        idx = order[:max(1, int(round(frac * len(ytr))))]
        p = _hgb(Xtr[idx], ytr[idx], seed).predict_proba(Xte)[:, 1]
        curve.append({"fraction": frac, "n_pos": int(ytr[idx].sum()),
                      "error": float(np.mean((p > 0.5) != yte)),
                      "auprc": float(average_precision_score(yte, p)),
                      "plugin": float(np.mean(np.minimum(p, 1 - p)))})
    n_pos = np.array([c["n_pos"] for c in curve])
    floor_err = fit_floor(n_pos, np.array([c["error"] for c in curve]))
    floor_ap = fit_floor(n_pos, 1 - np.array([c["auprc"] for c in curve]))
    sub = rng.choice(len(yte), min(NN_TEST_ROWS, len(yte)), replace=False)
    ch = cover_hart(Xtr, ytr, Xte[sub], yte[sub])
    plugin = curve[-1]["plugin"]
    ap_ceiling = None if floor_ap["c"] is None else 1 - floor_ap["c"]
    return {
        "fraud_rate_test": float(yte.mean()), "bayes_error": bayes_err,
        "bayes_auprc": bayes_ap, "curve": curve,
        "plugin": {"estimate": plugin,
                   "recovered": recovered(plugin, bayes_err)},
        "floor_error": {**floor_err,
                        "recovered": recovered(floor_err["c"], bayes_err)},
        "floor_auprc": {**floor_ap, "ceiling": ap_ceiling,
                        "recovered": bool(ap_ceiling is not None and abs(
                            ap_ceiling - bayes_ap) <= MARGIN_AUPRC)},
        "cover_hart": {**ch, "recovered": bool(
            ch["lower"] <= bayes_err <= ch["upper"])}}


METHODS = ("plugin", "floor_error", "floor_auprc", "cover_hart")


def seed_run(seed: int) -> dict:
    t0 = time.perf_counter()
    d = generate(seed)
    gen_s = time.perf_counter() - t0
    tr = (d["day"] >= TRAIN_DAYS[0]) & (d["day"] <= TRAIN_DAYS[1])
    te = (d["day"] >= TEST_DAYS[0]) & (d["day"] <= TEST_DAYS[1])
    X = np.column_stack([d["amount"], d["mu"], d["time"]])
    pi_t, q = world_rates(d, te)
    eta = posterior(d["amount"], d["mu"], pi_t, q)
    check = {"main": generator_check(d["y_main"][te], eta[te])}
    prior_t, prior_q = priors(d["n_customers"], d["n_terminals"])
    row = {"seed": seed, "n_transactions": int(len(eta)),
           "n_train": int(tr.sum()), "n_test": int(te.sum()),
           "test_rates": {"pi_T": pi_t, "q": q},
           "closed_form_priors": {"pi_T": prior_t, "q": prior_q},
           "train_rates": dict(zip(("pi_T", "q"), world_rates(d, tr))),
           "generator_check": check, "arms": {}}
    if not check["main"]["pass"]:
        row["stopped"] = "generator check failed"
        return row
    rng = np.random.default_rng(seed + 7)
    for name, rates in NOISE.items():
        y, e = add_noise(d["y_main"], eta, rates, rng)
        row["arms"][name] = score_arm(X[tr], y[tr], X[te], y[te], e[te],
                                      seed, rng)
    ref_eta = (d["base_amount"] > S1_AMOUNT).astype(float)
    Xref = np.column_stack([d["base_amount"], d["mu"], d["time"]])
    row["arms"]["reference"] = score_arm(
        Xref[tr], d["y_ref"][tr], Xref[te], d["y_ref"][te], ref_eta[te],
        seed, rng)
    row["seconds"] = {"generate": round(gen_s, 1),
                      "total": round(time.perf_counter() - t0, 1)}
    print(f"  s{seed} " + " | ".join(
        f"{a}: bayes {v['bayes_error']:.5f} plugin {v['plugin']['estimate']:.5f}"
        f" floor {v['floor_error']['c']} ch [{v['cover_hart']['lower']:.5f},"
        f" {v['cover_hart']['upper']:.5f}]" for a, v in row["arms"].items())
        + f" {row['seconds']}", flush=True)
    return row


def summarize(rows: list) -> dict:
    # The pass count is out of every seed run, so a stopped seed counts as
    # a miss rather than shrinking the denominator (Sprint 27 code review).
    out = {}
    for arm in list(NOISE) + ["reference"]:
        live = [r for r in rows if arm in r["arms"]]
        out[arm] = {m: {"seeds_recovered": sum(r["arms"][arm][m]["recovered"]
                                               for r in live),
                        "n_seeds": len(live),
                        "recovers": bool(len(live) > 0 and sum(
                            r["arms"][arm][m]["recovered"] for r in live)
                            >= min(PASS_SEEDS, len(rows)))}
                    for m in METHODS}
    return out


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    mode = argv[0] if argv else "pilot"
    if mode not in ("pilot", "run"):
        raise SystemExit("usage: f108_ceiling.py pilot|run")
    seeds = SEEDS[:1] if mode == "pilot" else SEEDS
    t0 = time.perf_counter()
    rows = [seed_run(s) for s in seeds]
    res = {"generator": "experiments/phase2/src/f108_ceiling.py",
           "card": "F108", "sprint": 27, "phase": 2, "evidence_tag": "SIM",
           "metered_seconds": 0, "date": time.strftime("%Y-%m-%d"),
           "entry": "experiments/phase2/PREREGISTRATION_DRAFT.md section 6, "
                    "F108",
           "source": "Fraud Detection Handbook, chapter 3 'Simulated "
                     "dataset' (prose, CC BY-SA 4.0); clean-room",
           "mode": mode, "seeds": list(seeds),
           "margin": {"abs": MARGIN_ABS, "rel": MARGIN_REL,
                      "auprc": MARGIN_AUPRC},
           "rows": rows, "summary": summarize(rows),
           "elapsed_s": round(time.perf_counter() - t0, 1)}
    (OUT_PILOT if mode == "pilot" else OUT).write_text(
        json.dumps(res, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(res["summary"], indent=1))
    stopped = [r["seed"] for r in rows if "stopped" in r]
    if stopped:
        print(f"STOPPED: the generator check failed on seeds {stopped}; "
              "the entry's stop applies", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
