"""F154: confusion counts for every stored result, and where each model wins.

Sprint 28 Task F (#47). Phase 2 code over STORED Phase 1 results and
predictions; nothing is refitted and no Phase 1 file is written. The entry
is in `experiments/phase2/PREREGISTRATION_DRAFT.md`, section 6, "F154",
written before any pairwise or subset count. Zero metered seconds.

Three parts:
  1. The table: TN, FP, FN and TP at both validation-chosen operating points
     for every row of `experiments/results/results.json` and of
     `experiments/phase2/results/f142_dirac3s_verify.json`.
  2. Per pair of stored prediction families and per seed, at the 0.5% alert
     budget on the test rows: frauds A flags that B misses, the reverse, and
     those both flag.
  3. The subset interaction (amount, day) with a Bonferroni t interval over
     seeds, the entry's primary test.

Run:  <venv python> experiments/phase2/src/f154_confusion.py
"""
from __future__ import annotations

import itertools
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "experiments" / "src"))
import outcome_record as orec  # noqa: E402  (Phase 2)

PRED = ROOT / "experiments" / "results" / "predictions"
RESULTS = ROOT / "experiments" / "results" / "results.json"
F142 = ROOT / "experiments" / "phase2" / "results" / "f142_dirac3s_verify.json"
OUT = ROOT / "experiments" / "phase2" / "results" / "f154_confusion.json"
SEEDS = tuple(range(42, 52))
ALERT_BUDGET = orec.ALERT_BUDGET
DAY_S = 86_400
ALPHA = 0.05


# ---------------------------------------------------------------- part 1
def table_rows(rows: list[dict], source: str) -> list[dict]:
    out = []
    for r in rows:
        ops = (r.get("metrics") or {}).get("operating_points") or []
        for op in ops:
            if "confusion" not in op:
                continue
            out.append({"source": source, "arm": r.get("arm"),
                        "dataset": r.get("dataset"), "protocol": r.get("protocol"),
                        "config_hash": r.get("config_hash"), "seed": r.get("seed"),
                        "evidence_tag": r.get("evidence_tag"),
                        "operating_point": op["operating_point"],
                        **op["confusion"]})
    return out


# ---------------------------------------------------------------- part 2
def families(pred_dir: Path = PRED) -> list[str]:
    """Every stored stratified family with all ten seeds."""
    found: dict[str, set] = {}
    for f in pred_dir.glob("*_stratified_*.npz"):
        fam, seed = f.stem.rsplit("_stratified_", 1)
        if seed.isdigit():
            found.setdefault(fam, set()).add(int(seed))
    return sorted(f for f, s in found.items() if set(SEEDS) <= s)


def load(fam: str, seed: int, pred_dir: Path = PRED) -> dict:
    return dict(np.load(pred_dir / f"{fam}_stratified_{seed}.npz"))


def catch_and_miss(y, flag_a, flag_b) -> dict:
    y = np.asarray(y).astype(bool)
    a, b = np.asarray(flag_a, bool), np.asarray(flag_b, bool)
    return {"a_only": int((y & a & ~b).sum()), "b_only": int((y & b & ~a).sum()),
            "both": int((y & a & b).sum()), "neither": int((y & ~a & ~b).sum())}


def budget_weights(scores, budget: float = ALERT_BUDGET) -> np.ndarray:
    """Expected flag per row with exactly the budget flagged: 1 above the
    cut, a random tie-break's share for rows tied at it (F113's rule).
    The sensitivity check for the entry's tied-together flags, which flag
    more rows than the budget when scores tie at the cut."""
    s = np.asarray(scores, dtype=float)
    k = int(np.ceil(budget * len(s)))
    cut = np.sort(s)[::-1][k - 1]
    above, tied = s > cut, s == cut
    w = above.astype(float)
    w[tied] = (k - int(above.sum())) / int(tied.sum())
    return w


def subset_recall(y, flag, mask) -> float:
    """Share of the subset's frauds flagged; `flag` may be 0/1 or weights."""
    y = np.asarray(y).astype(bool)
    m = np.asarray(mask, bool)
    pos = int((y & m).sum())
    if pos == 0:
        return float("nan")
    return float(np.asarray(flag, float)[y & m].sum() / pos)


def interaction(y, flag_a, flag_b, mask) -> float:
    """[rA(S) - rB(S)] - [rA(not S) - rB(not S)]."""
    m = np.asarray(mask, bool)
    return ((subset_recall(y, flag_a, m) - subset_recall(y, flag_b, m))
            - (subset_recall(y, flag_a, ~m) - subset_recall(y, flag_b, ~m)))


def t_interval(values, level: float) -> dict:
    from scipy import stats
    v = np.asarray(values, dtype=float)
    n = len(v)
    mean = float(v.mean())
    sd = float(v.std(ddof=1))
    half = float(stats.t.ppf(1 - (1 - level) / 2, n - 1) * sd / np.sqrt(n))
    return {"mean": mean, "sd": sd, "n": n, "level": level,
            "low": mean - half, "high": mean + half,
            "excludes_zero": bool(mean - half > 0 or mean + half < 0)}


# ---------------------------------------------------------------- the split
def test_features(seed: int, df) -> "object":
    """ULB test rows for `seed`, recovered as the stored files were made."""
    import data
    return data.stratified_split(df, seed).X_test


def raw_split_matches(fam: str, df_raw) -> str:
    """Why a family is off the deduplicated split: is it on the raw one?"""
    import data
    same = [np.array_equal(data.stratified_split(df_raw, s).y_test.to_numpy(),
                           np.asarray(load(fam, s)["y_test"]).astype(int))
            for s in SEEDS]
    if all(same):
        return ("its test labels match the split WITHOUT deduplication on every "
                "seed, so its rows are not the other families' rows")
    return f"test labels match neither split (raw split matches on {sum(same)} seeds)"


def subsets(x_test) -> dict:
    amt = x_test["Amount"].to_numpy()
    return {"amount_above_median": amt > np.median(amt),
            "day_1": x_test["Time"].to_numpy() < DAY_S}


# ---------------------------------------------------------------- run
def run() -> dict:
    t0 = time.time()
    rows = json.loads(RESULTS.read_text(encoding="utf-8"))["rows"]
    f142 = json.loads(F142.read_text(encoding="utf-8"))["rows"]
    table = table_rows(rows, "experiments/results/results.json") + \
        table_rows(f142, "experiments/phase2/results/f142_dirac3s_verify.json")

    fams = families()
    if len(fams) < 2:
        raise ValueError("fewer than two stored families; nothing to pair")

    import data
    df = data.load_ulb().drop_duplicates().reset_index(drop=True)

    flags: dict[tuple, np.ndarray] = {}
    weights: dict[tuple, np.ndarray] = {}
    ys: dict[int, np.ndarray] = {}
    masks: dict[int, dict] = {}
    blocks, excluded = [], {}
    for seed in SEEDS:
        x_te = test_features(seed, df)
        y_split = df.loc[x_te.index, data.LABEL_COL].to_numpy().astype(int)
        masks[seed] = subsets(x_te)
        for fam in fams:
            d = load(fam, seed)
            y = np.asarray(d["y_test"]).astype(int)
            path = PRED / f"{fam}_stratified_{seed}.npz"
            # Every family gets its block, paired or not: the block needs
            # only the stored labels and scores, not the recovered split.
            blocks.append(orec.record(
                fam, seed, y, d["p_test"], y_val=d["y_val"], p_val=d["p_val"],
                budget=ALERT_BUDGET,
                source={"path": path.relative_to(ROOT).as_posix(),
                        "sha256": orec.sha256_of(path)}))
            if len(y) != len(y_split) or not np.array_equal(y, y_split):
                excluded.setdefault(fam, []).append(seed)
                continue
            ys[seed] = y_split
            flags[(fam, seed)] = orec.flagged_at_budget(d["p_test"], ALERT_BUDGET)
            weights[(fam, seed)] = budget_weights(d["p_test"], ALERT_BUDGET)
    # A family excluded on some seeds only would leave holes in the pairs;
    # the entry leaves the whole family out.
    paired = [f for f in fams if f not in excluded]
    excluded_why = {f: raw_split_matches(f, data.load_ulb()) for f in excluded}
    pairs = list(itertools.combinations(paired, 2))
    subset_names = ("amount_above_median", "day_1")
    m = len(pairs) * len(subset_names)
    level = 1 - ALPHA / m

    pair_rows = []
    for a, b in pairs:
        per_seed, inter = [], {s: [] for s in subset_names}
        inter_w = {s: [] for s in subset_names}
        for seed in SEEDS:
            y, fa, fb = ys[seed], flags[(a, seed)], flags[(b, seed)]
            wa, wb = weights[(a, seed)], weights[(b, seed)]
            for s in subset_names:
                inter_w[s].append(interaction(y, wa, wb, masks[seed][s]))
            rec = {"seed": seed, **catch_and_miss(y, fa, fb),
                   "recall_a": subset_recall(y, fa, np.ones_like(y, bool)),
                   "recall_b": subset_recall(y, fb, np.ones_like(y, bool))}
            for s in subset_names:
                mk = masks[seed][s]
                rec[f"{s}_in_diff"] = subset_recall(y, fa, mk) - subset_recall(y, fb, mk)
                rec[f"{s}_interaction"] = interaction(y, fa, fb, mk)
                inter[s].append(rec[f"{s}_interaction"])
            per_seed.append(rec)
        pair_rows.append({
            "a": a, "b": b, "per_seed": per_seed,
            "a_only_total": sum(r["a_only"] for r in per_seed),
            "b_only_total": sum(r["b_only"] for r in per_seed),
            "both_total": sum(r["both"] for r in per_seed),
            "overall_recall_diff": t_interval(
                [r["recall_a"] - r["recall_b"] for r in per_seed], 0.95),
            "interaction": {s: t_interval(inter[s], level) for s in subset_names},
            "interaction_tie_neutral_sensitivity": {
                s: t_interval(inter_w[s], level) for s in subset_names},
            "in_subset_diff_secondary": {
                s: t_interval([r[f"{s}_in_diff"] for r in per_seed], 0.95)
                for s in subset_names}})

    fired = [{"a": p["a"], "b": p["b"], "subset": s, **p["interaction"][s]}
             for p in pair_rows for s in subset_names
             if p["interaction"][s]["excludes_zero"]]
    fired_w = [{"a": p["a"], "b": p["b"], "subset": s,
                **p["interaction_tie_neutral_sensitivity"][s]}
               for p in pair_rows for s in subset_names
               if p["interaction_tie_neutral_sensitivity"][s]["excludes_zero"]]
    extra = {}
    for blk in blocks:
        ab = blk["at_budget_on_test"]
        extra.setdefault(blk["name"], []).append(ab["n_flagged"] - ab["n_budget"])
    return {
        "generator": "experiments/phase2/src/f154_confusion.py",
        "card": "F154", "sprint": 28, "evidence_tag": "SIM",
        "entry": "experiments/phase2/PREREGISTRATION_DRAFT.md section 6, F154",
        "metered_seconds": 0,
        "alert_budget": ALERT_BUDGET, "seeds": list(SEEDS),
        "subsets": {"amount_above_median": "Amount above the test fold's median Amount",
                    "day_1": f"Time below {DAY_S} s"},
        "families": fams, "excluded_families": excluded,
        "excluded_reason": excluded_why,
        "family_m": m, "interval_level": level,
        "table": table,
        "pairs": pair_rows,
        "interactions_excluding_zero": fired,
        "tie_neutral_interactions_excluding_zero": fired_w,
        "extra_rows_flagged_by_ties": {k: {"max": max(v), "mean": float(np.mean(v))}
                                       for k, v in extra.items()},
        "verdict": ("some pair is reliably different on a subset" if fired else
                    "null: no interaction interval excludes zero"),
        "outcome_records": blocks,
        "wall_seconds": round(time.time() - t0, 1),
    }


def main() -> None:
    res = run()
    tmp = OUT.with_suffix(".tmp.json")
    tmp.write_text(json.dumps(res, indent=1), encoding="utf-8")
    tmp.replace(OUT)
    print(f"{len(res['table'])} table rows; {len(res['families'])} families; "
          f"{len(res['pairs'])} pairs; m = {res['family_m']}; "
          f"excluded {res['excluded_families']}; {res['verdict']}; "
          f"{res['wall_seconds']} s")


if __name__ == "__main__":
    main()
