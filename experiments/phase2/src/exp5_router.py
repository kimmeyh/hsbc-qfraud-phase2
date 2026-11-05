"""Experiment 5 (F121, Sprint 31 Task H, #100): segment transfer and router
acceptance, on the proxy, from F174's stored month-4 scores.

The entry is "Experiment 5" in `experiments/phase2/PREREGISTRATION_DRAFT.md`
section 6, committed before this module existed. The hold of record was
set aside by the team lead (Sprint 31 D3 option 2).

No model is fit. The scores are F174's (`experiments/phase2/predictions/
f174_{lane}_{seed}.npz`): every lane fitted on months 0-3 and scored on
month 4, its configuration chosen on month 3. Segments: the five values
of `ProductCD`. For segment S and lane L, the edge is L's recall at the
0.5% alert budget applied within S, minus the champion's (LightGBM's).
The control is section 5's matched random segment from outside S, 20
draws per seed. S is accepted for L when the mean edge is at least 0.01
and the 99% t interval (1 - 0.05 / 5) of (edge minus control edge) over
the 10 seeds lies wholly above 0.

Order: the alignment check; the classical reference (HGB in the proxy's
place); the proxy only if HGB is accepted on no segment.

    <venv python> experiments/phase2/src/exp5_router.py

Zero metered seconds. Writes `experiments/phase2/results/exp5_router.json`.
"""
from __future__ import annotations

import hashlib
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "experiments" / "src"))

OUT = ROOT / "experiments" / "phase2" / "results" / "exp5_router.json"
PRED = ROOT / "experiments" / "phase2" / "predictions"
SEEDS = tuple(range(42, 52))
CHAMPION, REFERENCE, PROXY = "lightgbm", "hgb", "proxy"
SEGMENTS = ("W", "C", "R", "H", "S")
BUDGET = 0.005
MIN_EDGE = 0.01
ALPHA = 0.05 / len(SEGMENTS)
DRAWS = 20


# ------------------------------------------------------------------ data
def month4_segments() -> tuple[np.ndarray, np.ndarray]:
    """Labels and ProductCD of the month-4 rows, in fold order."""
    import data as dmod
    import f174_ieee_algorithms as f174
    import ieee_loader
    import ieee_splits
    df, _ = ieee_loader.dedupe_ieee(dmod.load_ieee_cis_train())
    folds = ieee_splits.rolling_origin_folds(df, n_folds=4)
    ieee_splits.assert_no_temporal_leakage(df, folds)
    fold = {int(f.eval_month): f for f in folds}[f174.TEST_MONTH]
    rows = df.loc[fold.eval_idx]
    return (rows["isFraud"].to_numpy().astype(int),
            rows["ProductCD"].astype(str).to_numpy())


def scores(lane: str, seed: int) -> tuple[np.ndarray, np.ndarray, dict]:
    f = PRED / f"f174_{lane}_{seed}.npz"
    z = np.load(f, allow_pickle=False)
    src = {"path": f.relative_to(ROOT).as_posix(),
           "sha256": hashlib.sha256(f.read_bytes()).hexdigest()}
    return z["y_test"].astype(int), z["p_test"].astype(float), src


def aligned(y: np.ndarray, lanes=(CHAMPION, REFERENCE, PROXY)) -> dict:
    """Every stored label vector must equal the rebuilt one."""
    bad = [f"{lane}/{seed}" for lane in lanes for seed in SEEDS
           if not np.array_equal(scores(lane, seed)[0], y)]
    return {"pass": not bad, "mismatched": bad}


# ------------------------------------------------------------- the rules
def recall_at_budget(y: np.ndarray, s: np.ndarray, idx: np.ndarray) -> float:
    """Recall within the rows `idx` when the top ceil(0.005 x |idx|) of
    them by score are flagged. Ties keep row order."""
    k = math.ceil(BUDGET * len(idx))
    top = idx[np.argsort(-s[idx], kind="stable")[:k]]
    pos = int(y[idx].sum())
    return float(y[top].sum() / pos) if pos else float("nan")


def matched_pair(seg_pos: int, seg_neg: int, comp_pos: int,
                 comp_neg: int) -> dict:
    """Section 5's downsized pair: positives per side the smaller of the
    two, negatives at the segment's own rate."""
    p = min(seg_pos, comp_pos)
    n = int(round(p * seg_neg / seg_pos)) if seg_pos else 0
    return {"positives": p, "negatives": n,
            "feasible": p > 0 and n <= comp_neg and n <= seg_neg,
            "downsized": p < seg_pos}


def draw(rng, y: np.ndarray, pool: np.ndarray, p: int, n: int) -> np.ndarray:
    pos, neg = pool[y[pool] == 1], pool[y[pool] == 0]
    return np.sort(np.concatenate([rng.choice(pos, p, replace=False),
                                   rng.choice(neg, n, replace=False)]))


def edges(y, s_lane, s_champ, seg_mask, seed: int, seg_i: int) -> dict:
    seg = np.flatnonzero(seg_mask)
    comp = np.flatnonzero(~seg_mask)
    pair = matched_pair(int(y[seg].sum()), int((y[seg] == 0).sum()),
                        int(y[comp].sum()), int((y[comp] == 0).sum()))
    if not pair["feasible"]:
        return {"pair": pair, "edge": None, "control_edge": None}
    rng = np.random.default_rng(1000 * seed + seg_i)

    def edge(idx):
        return (recall_at_budget(y, s_lane, idx)
                - recall_at_budget(y, s_champ, idx))
    if pair["downsized"]:
        e = float(np.mean([edge(draw(rng, y, seg, pair["positives"],
                                     pair["negatives"]))
                           for _ in range(DRAWS)]))
    else:
        e = edge(seg)
    c = float(np.mean([edge(draw(rng, y, comp, pair["positives"],
                                 pair["negatives"]))
                       for _ in range(DRAWS)]))
    return {"pair": pair, "rows": int(len(seg)),
            "positives": int(y[seg].sum()),
            "lane_recall": recall_at_budget(y, s_lane, seg),
            "champion_recall": recall_at_budget(y, s_champ, seg),
            "edge": e, "control_edge": c}


def accept(per_seed: list[dict]) -> dict:
    """The router criterion over seeds."""
    from scipy import stats
    live = [r for r in per_seed if r["edge"] is not None]
    if len(live) < 2:
        return {"accepted": False, "reason": "fewer than 2 feasible seeds",
                "n": len(live)}
    e = np.array([r["edge"] for r in live])
    d = e - np.array([r["control_edge"] for r in live])
    n = len(d)
    mean_d, sd = float(d.mean()), float(d.std(ddof=1))
    h = float(stats.t.ppf(1 - ALPHA / 2, n - 1)) * sd / math.sqrt(n)
    lo, hi = mean_d - h, mean_d + h
    if np.all(d == 0):
        p = 1.0
    else:
        # Reported beside the interval, not decisive; zero differences
        # are dropped (scipy's "wilcox" rule) and the exact method used.
        p = float(stats.wilcoxon(d, method="exact").pvalue)
    ok = bool(e.mean() >= MIN_EDGE and lo > 0)
    return {"accepted": ok, "n": n, "mean_edge": float(e.mean()),
            "mean_edge_minus_control": mean_d,
            "interval": [lo, hi], "level": 1 - ALPHA, "wilcoxon_p": p}


def lane_result(lane: str, y: np.ndarray, seg_col: np.ndarray) -> dict:
    per_seg = {}
    for i, seg in enumerate(SEGMENTS):
        mask = seg_col == seg
        rows = []
        for seed in SEEDS:
            _, s_lane, _ = scores(lane, seed)
            _, s_champ, _ = scores(CHAMPION, seed)
            rows.append({"seed": seed,
                         **edges(y, s_lane, s_champ, mask, seed, i)})
        per_seg[seg] = {"per_seed": rows, "criterion": accept(rows)}
    return per_seg


def blocked_by_reference(reference: dict) -> list[str]:
    """Segments where the classical reference is accepted: there the
    criterion cannot separate a model difference from a routing effect."""
    return [s for s, v in reference.items() if v["criterion"]["accepted"]]


def outcomes(lanes) -> dict:
    import outcome_record as orec
    out = {}
    for lane in lanes:
        for seed in SEEDS:
            y, p, src = scores(lane, seed)
            out[f"{lane}/{seed}"] = orec.record(f"exp5_{lane}", seed, y, p,
                                                source=src)
    return out


def run() -> dict:
    import json as _json
    y, seg_col = month4_segments()
    doc = {"card": "F121", "experiment": 5, "sprint": 31, "phase": 2,
           "evidence_tag": "SIM", "metered_seconds": 0,
           "entry": "experiments/phase2/PREREGISTRATION_DRAFT.md section 6, "
                    "Experiment 5 (2026-11-05)",
           "scores": "experiments/phase2/predictions/f174_{lane}_{seed}.npz",
           "segments": {s: int((seg_col == s).sum()) for s in SEGMENTS},
           "champion": CHAMPION, "seeds": list(SEEDS), "budget": BUDGET,
           "min_edge": MIN_EDGE, "alpha_each": ALPHA, "draws": DRAWS}
    top = _json.loads((ROOT / "experiments" / "phase2" / "results" /
                       "f174_ieee_algorithms.json").read_text(
        encoding="utf-8"))["analysis"]["order_by_mean_test_auprc"][0]
    doc["f174_top_lane"] = top
    doc["alignment"] = aligned(y)
    if not doc["alignment"]["pass"]:
        doc["stopped"] = "stored labels do not match the rebuilt month 4"
        return doc
    doc["reference"] = lane_result(REFERENCE, y, seg_col)
    hit = blocked_by_reference(doc["reference"])
    if hit:
        doc["stopped"] = (f"HGB is accepted on {hit}: the criterion cannot "
                          "tell a model difference from a routing effect "
                          "there; a redesign is written as a decision "
                          "before the proxy's figures are computed")
        doc["outcomes"] = outcomes((CHAMPION, REFERENCE))
        return doc
    doc["proxy"] = lane_result(PROXY, y, seg_col)
    doc["accepted_segments"] = [s for s, v in doc["proxy"].items()
                                if v["criterion"]["accepted"]]
    doc["outcomes"] = outcomes((CHAMPION, REFERENCE, PROXY))
    return doc


def main() -> int:
    import provenance
    rid, _ = provenance.start(OUT, resumable=False)
    doc = run()
    doc["complete"] = True
    provenance.write_result(OUT, doc, __file__, list(SEEDS), rid)
    print({k: doc.get(k) for k in ("alignment", "stopped",
                                   "accepted_segments")})
    print("complete", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
