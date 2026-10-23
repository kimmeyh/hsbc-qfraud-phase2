"""Backfill F154 outcome blocks into older Phase 2 result files.

Sprint 28 Manual Validation, decision DV4 (team lead, option 1, "do now"):
the Phase 2 result files written before the F154 rule (2026-10-22) get the
outcome blocks of `outcome_record.py` wherever their per-row test scores can
be rebuilt EXACTLY. A file that cannot be rebuilt exactly stays in the guard's
`EXEMPT_BEFORE_RULE` list and is named in the sprint record instead.

One adapter per file. An adapter rebuilds the per-row scores with the file's
own generator functions (or names the stored per-row file, F154's `source=`
pattern) and returns a `Plan`: the scored lanes, the checks of each stored
test metric against the same scores, and the lanes it cannot cover with the
reason. This module then does the rest, and refuses to write when:

  - the file's bytes do not round-trip through `json.dumps` with one of the
    indent styles below (the format could not be preserved);
  - the file already holds an `outcome_backfill` object (no second run);
  - the plan carries no metric check, or any check differs from the stored
    value by more than that value's stored rounding;
  - any pre-existing leaf value would change, or a new value would land
    anywhere but under a key this module adds;
  - the written bytes, read back from disk, fail either check above.

Every new value goes under a new key: `"outcome"` beside a scored entry, or
the top-level `"outcome_backfill"` object, which also records the date, this
generator, the decision and the covered and uncovered lanes.

Zero metered seconds; nothing here calls a device or a network service.

    python experiments/phase2/src/backfill_outcomes.py f112_intervals --dry-run
    python experiments/phase2/src/backfill_outcomes.py f112_intervals
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "experiments" / "src"))
import outcome_record as orec  # noqa: E402  (Phase 2)

RESULTS = ROOT / "experiments" / "phase2" / "results"
PHASE1_PRED = ROOT / "experiments" / "results" / "predictions"
GENERATOR = "experiments/phase2/src/backfill_outcomes.py"
DATE = "2026-10-23"
DECISION = "Sprint 28 Manual Validation DV4"
META_KEY = "outcome_backfill"
INDENTS = (1, 2, 4, None)
FULL_PRECISION_TOL = 1e-12


class BackfillRefused(RuntimeError):
    """The backfill would not be exact, or would change stored evidence."""


@dataclass
class Lane:
    """One model's per-row test scores on one seed.

    `place` is the path (keys and list indices) of the dict that receives the
    block under `key`; None appends the block to `outcome_backfill.blocks`.
    `source` names a stored per-row file ({"path", "sha256"}) instead of
    saving a new one.
    """
    name: str
    seed: object
    y: np.ndarray
    p: np.ndarray
    place: tuple | None = None
    key: str = "outcome"
    y_val: np.ndarray | None = None
    p_val: np.ndarray | None = None
    threshold: float | None = None
    source: dict | None = None


@dataclass
class Check:
    """A stored test metric and the same metric recomputed from the lanes."""
    label: str
    stored: float
    recomputed: Callable[[], float]
    tol: float | None = None


@dataclass
class Plan:
    lanes: list[Lane]
    checks: list[Check]
    covered: list[str]
    uncovered: dict[str, str] = field(default_factory=dict)
    notes: dict = field(default_factory=dict)


# ------------------------------------------------------------ the core
def rounding_tol(stored: float) -> float:
    """Half a unit in the stored value's last decimal place, or 1e-12 when
    the value carries full float precision (no rounding to undo)."""
    r = repr(float(stored))
    if "e" in r or "E" in r:
        return FULL_PRECISION_TOL
    decimals = len(r.split(".")[1]) if "." in r else 0
    if decimals >= 12:
        return FULL_PRECISION_TOL
    return 0.5 * 10.0 ** -decimals * (1 + 1e-9)


def rounded(decimals: int) -> float:
    """The tolerance of a value the generator stored with round(x, decimals):
    explicit, because repr drops trailing zeros (round(x, 4) can read 0.515)."""
    return 0.5 * 10.0 ** -decimals * (1 + 1e-9)


def read_exact(path: Path) -> str:
    with open(path, encoding="utf-8", newline="") as fh:
        return fh.read()


def dumps(doc, fmt: tuple) -> str:
    """`fmt` is (indent, line ending, trailing line ending). The working
    tree may hold CRLF (core.autocrlf on Windows) while git stores LF."""
    indent, eol, trailing = fmt
    text = json.dumps(doc, indent=indent) + ("\n" if trailing else "")
    return text.replace("\n", eol)


def detect_format(text: str) -> tuple:
    """The format that reproduces `text` byte for byte."""
    doc = json.loads(text)
    for indent in INDENTS:
        for eol in ("\n", "\r\n"):
            for trailing in (True, False):
                if dumps(doc, (indent, eol, trailing)) == text:
                    return indent, eol, trailing
    raise BackfillRefused("the file's bytes do not round-trip through "
                          "json.dumps with any known indent; its format "
                          "could not be preserved")


def leaves(o, path=()) -> dict:
    """Every leaf as {path: (type name, repr)}; floats compare by repr."""
    out = {}
    if isinstance(o, dict):
        if not o:
            out[path] = ("dict", "{}")
        for k, v in o.items():
            out.update(leaves(v, path + (k,)))
    elif isinstance(o, list):
        if not o:
            out[path] = ("list", "[]")
        for i, v in enumerate(o):
            out.update(leaves(v, path + (i,)))
    else:
        out[path] = (type(o).__name__, repr(o))
    return out


def check_leaves(old, new, added: list[tuple]) -> None:
    """Refuse unless every old leaf is unchanged and every new leaf sits
    under one of the `added` key paths."""
    lo, ln = leaves(old), leaves(new)
    changed = [p for p, v in lo.items() if ln.get(p) != v]
    if changed:
        raise BackfillRefused(f"{len(changed)} pre-existing value(s) would "
                              f"change, first {changed[:3]}")
    stray = [p for p in ln if p not in lo
             and not any(p[:len(a)] == a for a in added)]
    if stray:
        raise BackfillRefused(f"{len(stray)} new value(s) outside the added "
                              f"keys, first {stray[:3]}")


def _navigate(doc, path: tuple):
    node = doc
    for k in path:
        node = node[k]
    if not isinstance(node, dict):
        raise BackfillRefused(f"placement {path} is not an object")
    return node


def run_checks(checks: list[Check]) -> list[dict]:
    if not checks:
        raise BackfillRefused("the plan carries no metric check; an "
                              "unverified rebuild is not written")
    out = []
    for c in checks:
        got = float(c.recomputed())
        tol = rounding_tol(c.stored) if c.tol is None else c.tol
        diff = abs(got - float(c.stored))
        if not diff <= tol:
            raise BackfillRefused(f"metric mismatch on {c.label}: stored "
                                  f"{c.stored!r}, recomputed {got!r}, "
                                  f"difference {diff:.3g} > {tol:.3g}")
        out.append({"label": c.label, "stored": c.stored,
                    "recomputed": got, "abs_diff": diff, "tolerance": tol})
    return out


def summarize_checks(checks: list[dict]) -> dict:
    """What the file records: the count, the worst difference, and every
    check that was not bit-identical. A check not listed matched exactly."""
    return {"n_checks": len(checks),
            "all_within_tolerance": True,
            "max_abs_diff": max(c["abs_diff"] for c in checks),
            "not_identical": [c for c in checks if c["abs_diff"] > 0]}


def build(doc, plan: Plan, pred_dir: Path = orec.PRED_DIR) -> tuple:
    """The new document and the key paths added. Checks run first, so a
    refused plan writes no per-row file either."""
    if META_KEY in doc:
        raise BackfillRefused(f"the file already holds {META_KEY!r}; "
                              "a second backfill is refused")
    checks = run_checks(plan.checks)
    if not plan.lanes:
        raise BackfillRefused("the plan covers no lane")
    new = copy.deepcopy(doc)
    added: list[tuple] = [(META_KEY,)]
    listed = []
    for ln in plan.lanes:
        blk = orec.record(ln.name, ln.seed, ln.y, ln.p, y_val=ln.y_val,
                          p_val=ln.p_val, threshold=ln.threshold,
                          pred_dir=pred_dir, source=ln.source)
        if ln.place is None:
            listed.append(blk)
            continue
        parent = _navigate(new, ln.place)
        if ln.key in parent:
            raise BackfillRefused(f"{ln.place + (ln.key,)} already exists")
        parent[ln.key] = blk
        added.append(tuple(ln.place) + (ln.key,))
    meta = {"date": DATE, "generator": GENERATOR, "decision": DECISION,
            "covered_lanes": plan.covered,
            "uncovered_lanes": plan.uncovered,
            "n_blocks": len(plan.lanes),
            "metric_check": summarize_checks(checks), **plan.notes}
    if listed:
        meta["blocks"] = listed
    new[META_KEY] = meta
    check_leaves(doc, new, added)
    return new, added


def apply(path: Path, plan: Plan, *, write: bool = True,
          pred_dir: Path = orec.PRED_DIR) -> dict:
    text = read_exact(path)
    fmt = detect_format(text)
    old = json.loads(text)
    new, added = build(old, plan, pred_dir)
    out = dumps(new, fmt)
    if write:
        fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as fh:
            fh.write(out)
        os.replace(tmp, path)
        back = read_exact(path)
        if back != out or detect_format(back) != fmt:
            raise BackfillRefused(f"{path.name} did not read back as written")
        check_leaves(old, json.loads(back), added)
    return new[META_KEY]


# ------------------------------------------------------------ helpers
def ap(y, p) -> float:
    from sklearn.metrics import average_precision_score
    return float(average_precision_score(y, p))


def auroc(y, p) -> float:
    from sklearn.metrics import roc_auc_score
    return float(roc_auc_score(y, p))


def stored_source(path: Path) -> dict:
    return {"path": path.relative_to(ROOT).as_posix(),
            "sha256": orec.sha256_of(path)}


def phase1_family(fam: str, seed: int) -> tuple[dict, dict]:
    """A Phase 1 stored prediction file (read-only) and its source dict."""
    f = PHASE1_PRED / f"{fam}_stratified_{seed}.npz"
    d = dict(np.load(f))
    return d, stored_source(f)


# ------------------------------------------------------------ adapters
def plan_f112(doc) -> Plan:
    import f112_intervals as g
    lanes, checks, data = [], [], {}
    for s in g.SEEDS:
        for cell, h in g.CELLS.items():
            d, src = phase1_family(f"cvqboost_proxy_{h}", s)
            y, p = d["y_test"].astype(int), d["p_test"].astype(np.float64)
            data[(cell, s)] = (y, p)
            lanes.append(Lane(f"f112_{cell}", s, y, p, y_val=d["y_val"],
                              p_val=d["p_val"], source=src))
    for eff, (a, b) in g.EFFECTS.items():
        for i, row in enumerate(doc[eff]["per_seed"]):
            s = row["seed"]
            (y, pa), (_, pb) = data[(a, s)], data[(b, s)]
            checks.append(Check(f"{eff}.per_seed[{i}].delta_auprc",
                                row["delta_auprc"],
                                lambda y=y, pa=pa, pb=pb: ap(y, pa) - ap(y, pb)))
            checks.append(Check(f"{eff}.per_seed[{i}].delta_auroc",
                                row["delta_auroc"],
                                lambda y=y, pa=pa, pb=pb:
                                auroc(y, pa) - auroc(y, pb)))
    return Plan(lanes, checks,
                covered=[f"{c} ({h}), seeds 42-51, stored Phase 1 predictions"
                         for c, h in g.CELLS.items()],
                uncovered={"interaction_secondary twin term":
                           "F144's twin; its blocks are in "
                           "f144_proxy_twin.json"},
                notes={"placement": "blocks listed here; the file's rows "
                                    "are paired deltas, not single models"})


def plan_f113(doc) -> Plan:
    import oracle_gap as g
    fams = doc["candidate_families"]["cvq"] + doc["candidate_families"]["xgb"]
    lanes, checks, data = [], [], {}
    for fam in fams:
        for s in g.SEEDS:
            d, src = phase1_family(fam, s)
            data[(fam, s)] = d
            lanes.append(Lane(fam, s, d["y_test"], d["p_test"],
                              y_val=d["y_val"], p_val=d["p_val"], source=src))
    for fam, v in doc["validation_auprc_by_family"].items():
        checks.append(Check(f"validation_auprc_by_family.{fam}", v,
                            lambda fam=fam: np.mean(
                                [ap(data[(fam, s)]["y_val"],
                                    data[(fam, s)]["p_val"]) for s in g.SEEDS])))

    def recall(fam, s):
        return g.recall_at_budget(data[(fam, s)]["y_test"],
                                  data[(fam, s)]["p_test"])
    pairs = [("primary", doc["primary"])] + \
        [(f"sensitivity[{i}]", p) for i, p in enumerate(doc["sensitivity"])]
    for label, pr in pairs:
        for side in ("cvq", "xgb"):
            fam = pr[side]
            checks.append(Check(f"{label}.recall_{side}_mean",
                                pr[f"recall_{side}_mean"],
                                lambda fam=fam: np.mean(
                                    [recall(fam, s) for s in g.SEEDS])))
    for i, row in enumerate(doc["primary"]["rows"]):
        for side in ("cvq", "xgb"):
            fam = doc["primary"][side]
            checks.append(Check(f"primary.rows[{i}].recall_{side}",
                                row[f"recall_{side}"],
                                lambda fam=fam, s=row["seed"]: recall(fam, s)))
    return Plan(lanes, checks,
                covered=[f"{f}, seeds 42-51, stored Phase 1 predictions"
                         for f in fams],
                uncovered={
                    "oracle": "not a model: it picks each row's better rank "
                              "using the row's label",
                    "fraud_side_only, legit_side_only": "not models: each "
                              "uses the row's label to pick a rank",
                    "label_free_mean_rank, label_free_max_rank": "derived "
                              "rank combinations of two covered lanes; "
                              "recomputable from their per-row files"},
                notes={"placement": "one block per family and seed, listed "
                                    "here; pairs share families",
                       "tie_handling": "the file's recalls give the tie at "
                                       "the cut fractional credit "
                                       "(oracle_gap.recall_at_budget); a "
                                       "block flags the whole tie "
                                       "(outcome_record), so its n_flagged "
                                       "can exceed n_budget by design"})


def plan_f144(doc) -> Plan:
    import f144_proxy_twin as g
    lanes, checks = [], []
    pools = {"ref_stored": lambda s: g.PHASE1_POOLS / f"h_{s}_free_dct_full.npz",
             "ref_rebuilt": lambda s: g.pool_path("ref", s),
             "twin": lambda s: g.pool_path("twin", s)}
    for i, row in enumerate(doc["rows"]):
        s = row["seed"]
        for arm, where in pools.items():
            npz = np.load(where(s))
            _, p = g.pool_scores(npz)
            y = npz["y_te"].astype(int)
            lanes.append(Lane(f"f144_{arm}", s, y, p, place=("rows", i, arm)))
            for m, fn in (("auprc", ap), ("auroc", auroc)):
                checks.append(Check(f"rows[{i}].{arm}.{m}", row[arm][m],
                                    lambda y=y, p=p, fn=fn: fn(y, p)))
        d, src = phase1_family("cvqboost_hw_None", s)
        lanes.append(Lane("cvqboost_hw_None", s, d["y_test"], d["p_test"],
                          place=("rows", i), key="b2_device_outcome",
                          y_val=d["y_val"], p_val=d["p_val"], source=src))
        checks.append(Check(f"rows[{i}].b2_device_auprc",
                            row["b2_device_auprc"],
                            lambda d=d: ap(d["y_test"], d["p_test"])))
    return Plan(lanes, checks,
                covered=["ref_stored (Phase 1 pools, solved here), seeds 42-51",
                         "ref_rebuilt (F144 pools, solved here), seeds 42-51",
                         "twin (F144 seeded pools, solved here), seeds 42-51",
                         "B2 device (hw_b2_full), seeds 42-51, stored Phase 1 "
                         "predictions cvqboost_hw_None"],
                notes={"pools": "experiments/phase2/results/pools/f144_* are "
                                "gitignored and local to the machine that "
                                "built them; the per-row files carry the "
                                "scores and their SHA-256"})


def plan_f142(doc) -> Plan:
    import f142_readout as g
    rows = {r["seed"]: r for r in json.loads(
        g.ROWS.read_text(encoding="utf-8"))["rows"]
        if r["status"] == "ok" and r["unit"].startswith("b4_")}
    lanes, checks = [], []
    for i, b in enumerate(doc["b4"]):
        s = b["seed"]
        j = next(k for k, x in enumerate(doc["b4_structure"]) if x["seed"] == s)
        pool = g._pool(s, rows[s])          # refuses unless the hash matches
        best = g._best(g._response(rows[s]))
        w = g.f126.exact_weights(g.CELL, s)
        y = np.asarray(pool["y_te"]).astype(int)
        for lane, v, place, key in (
                ("f142_b4_dirac3s", best, ("b4", i, "dirac3s"), "outcome"),
                ("f142_b4_exact", w, ("b4_structure", j),
                 "exact_reference_outcome")):
            p = np.clip((v @ pool["H_te"] + 1.0) / 2.0, 0.0, 1.0)
            lanes.append(Lane(lane, s, y, p, place=place, key=key))
            stored = doc["b4_structure"][j]["test_auprc_scored_from_pool"]
            name = ("device_best_sample" if lane.endswith("dirac3s")
                    else "exact_reference")
            checks.append(Check(f"b4_structure[{j}].test_auprc_scored_from_"
                                f"pool.{name}", stored[name],
                                lambda y=y, p=p: ap(y, p)))
            if lane.endswith("dirac3s"):
                checks.append(Check(f"b4[{i}].dirac3s.test_auprc",
                                    b["dirac3s"]["test_auprc"],
                                    lambda y=y, p=p: ap(y, p)))
    return Plan(lanes, checks,
                covered=["B4 Dirac-3S best sample (seeded pool rebuilt behind "
                         "its Hamiltonian-hash refusal), seeds 42-43",
                         "B4 exact reference solve (F126), seeds 42-43"],
                uncovered={
                    "B4 Dirac-3 (b4[].dirac3)": "per-row scores were never "
                        "stored, and its Phase 1 pool was an unseeded build "
                        "that does not reproduce",
                    "b1, b2 cost rows": "no test score; cost only"},
                notes={"per_row_files": "the Dirac-3S lane's scores are "
                       "rebuilt from stored device samples at zero metered "
                       "seconds, so they are saved under the gitignored "
                       "name f142_*, not hw_*"})


def plan_f130_hgb(doc) -> Plan:
    import f130_levers as g
    scores: dict = {}
    g.run_ulb_hgb_check(scores=scores)
    lanes, checks = [], []
    for i, r in enumerate(doc["rows"]):
        y, p = scores[(r["seed"], r["variant"])]
        y = np.asarray(y).astype(int)
        lanes.append(Lane(f"f130_hgb_{r['variant']}", r["seed"], y, p,
                          place=("rows", i)))
        checks.append(Check(f"rows[{i}].test_auprc", r["test_auprc"],
                            lambda y=y, p=p: ap(y, p)))
    for v, stored in doc["mean_test_auprc"].items():
        checks.append(Check(f"mean_test_auprc.{v}", stored,
                            lambda v=v: np.mean([ap(*scores[(r["seed"], v)])
                                                 for r in doc["rows"]
                                                 if r["variant"] == v]),
                            tol=rounded(4)))
    return Plan(lanes, checks,
                covered=[f"HGB {v}, seeds {doc['seeds'][0]}-{doc['seeds'][-1]}"
                         for v in doc["mean_test_auprc"]],
                notes={"generator_hash": "the file's generator_sha256 matches "
                       "no committed f130_levers.py; every row's test AUPRC "
                       "reproduced at full precision, which is the check "
                       "relied on here"})


def same_leaves(stored, rebuilt, label: str, skip=()) -> list[Check]:
    """One check per leaf of a stored entry against the same entry rebuilt:
    numbers within their rounding, everything else equal."""
    a, b = leaves(stored), leaves(rebuilt)
    out = []
    for path, (typ, rep) in a.items():
        if any(k in path for k in skip):
            continue
        name = f"{label}." + ".".join(map(str, path))
        val = _leaf_value(stored, path)
        if typ in ("float", "int") and not isinstance(val, bool):
            # The rebuilt entry passes through the generator's own rounding,
            # so it must match at full precision whatever the stored digits.
            out.append(Check(name, val, lambda p=path: _leaf_value(rebuilt, p),
                             tol=FULL_PRECISION_TOL))
        else:
            out.append(Check(name, 0.0, lambda p=path, v=(typ, rep):
                             0.0 if b.get(p) == v else 1.0, tol=0.0))
    return out


def _leaf_value(doc, path):
    for k in path:
        doc = doc[k]
    return doc


def plan_f108(doc, stem: str) -> Plan:
    import f108_ceiling as g
    full = g.CURVE[-1]
    lanes, checks = [], []
    for i, row in enumerate(doc["rows"]):
        s = row["seed"]
        scores: dict = {}
        rebuilt = g.seed_run(s, scores)
        checks += same_leaves(row, rebuilt, f"rows[{i}]", skip=("seconds",))
        for arm in row["arms"]:
            for kind, key, (y, p) in (
                    ("hgb_full", "outcome", scores[arm][("hgb", full)]),
                    ("bayes", "bayes_outcome", scores[arm]["bayes"])):
                y = np.asarray(y).astype(int)
                lanes.append(Lane(f"{stem}_{arm}_{kind}", s, y, p,
                                  place=("rows", i, "arms", arm), key=key))
                stored = (row["arms"][arm]["curve"][-1]["auprc"]
                          if kind == "hgb_full"
                          else row["arms"][arm]["bayes_auprc"])
                checks.append(Check(f"rows[{i}].arms.{arm}.{kind} auprc "
                                    "from the block's scores", stored,
                                    lambda y=y, p=p: ap(y, p)))
    seeds = ", ".join(str(r["seed"]) for r in doc["rows"])
    arms = list(doc["rows"][0]["arms"])
    return Plan(lanes, checks,
                covered=[f"{a}: HGB on the full training days (curve "
                         f"fraction 1.0), seeds {seeds}" for a in arms]
                + [f"{a}: the exact Bayes posterior (bayes_auprc), seeds "
                   f"{seeds}" for a in arms],
                uncovered={
                    "learning-curve fits at fractions 1/32 to 1/2":
                        "rebuildable exactly by the same seed_run, but not "
                        "saved: five more 615k-row files per arm and seed "
                        "(about 5 MB each); the full-data fit is the model",
                    "cover_hart": "a 1-NN error on a 100k-row test subsample; "
                                  "no per-row score"},
                notes={"row_check": "every stored leaf of each row except "
                       "'seconds' was rebuilt by f108_ceiling.seed_run and "
                       "compared"})


F103_LANES = ("gam", "gam_2_harmonics", "gam_3_harmonics", "ga2m", "hgb",
              "joint")


def tier1_lanes(lanes, checks, name, place, seed, stored, rebuilt, scores,
                skip=("lane_seconds",)) -> None:
    """One F103-style target row (`f103_tier1.run_target`): every stored
    leaf against the rebuilt row, then one block per scored lane with its
    AUROC (stored rounded to 4 decimals) recomputed from the block's scores."""
    label = ".".join(map(str, place))
    checks += same_leaves(stored, rebuilt, label, skip=skip)
    for lane in F103_LANES:
        if lane not in scores:
            continue
        yt, p = scores[lane]
        yt = np.asarray(yt).astype(int)
        lanes.append(Lane(f"{name}_{lane}", seed, yt, p, place=place,
                          key=f"{lane}_outcome"))
        checks.append(Check(f"{label}.{lane} AUC from the block's scores",
                            stored[lane], lambda yt=yt, p=p: auroc(yt, p),
                            tol=rounded(4)))


def plan_f103(doc, stem: str) -> Plan:
    import f103_tier1 as g
    d = g.load_raw()
    P_real, _ = g.real_phases(d)
    y_real = d["target_real"].to_numpy().astype(int)
    entries = [(("permuted_reference",), "permuted", 42,
                lambda s: (P_real, np.random.default_rng(42).permutation(
                    y_real)), False)]
    for i, s in enumerate(doc["seeds"]):
        entries += [(("real", i), "real", s, lambda s: (P_real, y_real), True),
                    (("sparse", i), "sparse", s,
                     lambda s: g.sparse_pocket(d, s), False),
                    (("dense", i), "dense", s,
                     lambda s: g.dense_substrate(d, s), False)]
    lanes, checks = [], []
    for place, target, s, data, secondary in entries:
        stored = _leaf_value(doc, place)
        P, y = data(s)
        scores: dict = {}
        rebuilt = g.run_target(target, P, y, s, secondary=secondary,
                               scores=scores)
        if "frequency_recovery" in stored:
            rebuilt["frequency_recovery"] = g.freq_recovery(
                rebuilt["joint_terms"])
        tier1_lanes(lanes, checks, f"{stem}_{target}", place, s, stored,
                    rebuilt, scores)
    seeds = ", ".join(map(str, doc["seeds"]))
    return Plan(lanes, checks,
                covered=["permuted reference (seed 42): gam, ga2m, hgb, joint"]
                + [f"real (seeds {seeds}): gam, gam_2_harmonics, "
                   "gam_3_harmonics, ga2m, hgb, joint",
                   f"sparse (seeds {seeds}): gam, ga2m, hgb, joint",
                   f"dense (seeds {seeds}): gam, ga2m, hgb, joint"],
                notes={"row_check": "every stored leaf of each target row "
                       "except 'lane_seconds' was rebuilt by "
                       "f103_tier1.run_target and compared",
                       "metric": "the file's lane scores are test AUROC, "
                                 "stored rounded to 4 decimals"})


def plan_f106(doc, stem: str) -> Plan:
    import data
    import f106_dequant as g
    from sklearn.metrics import average_precision_score as aps
    df = data.load_ulb()
    lanes, checks, trained = [], [], False
    for i, row in enumerate(doc["rows"]):
        s = row["seed"]
        d = g.prepare(df, s)
        checks.append(Check(f"rows[{i}].features", 0.0,
                            lambda f=d["feats"], r=row: 0.0
                            if list(f) == r["features"] else 1.0, tol=0.0))
        if "params_flat" in row:
            params = g.Params(float(d["ytr"].mean()), s)
            params.set_flat(np.asarray(row["params_flat"], dtype=np.float64))
        else:
            # The pilot stored no parameters: retrain at its own step count.
            trained = True
            params, trace = g.train_circuit(d["Ptr"], d["ytr"], s,
                                            doc["steps"])
            checks.append(Check(f"rows[{i}].loss_trace", 0.0,
                                lambda t=trace, r=row: 0.0
                                if t == r["loss_trace"] else 1.0, tol=0.0))
        scores = {"circuit": g.predict(params, d["Pte"])}
        twins, sec = g.twin_scores(d["Ptr"], d["ytr"], d["Pva"], d["yva"],
                                   d["Pte"], s)
        scores.update(twins)
        checks += same_leaves(row["twin_detail"],
                              {k: v for k, v in sec.items()
                               if not k.startswith("seconds")},
                              f"rows[{i}].twin_detail")
        y = d["yte"]
        base = float(y.mean())
        for lane, p in scores.items():
            lanes.append(Lane(f"{stem}_{lane}", s, y, p,
                              place=("rows", i, "lanes", lane)))
            st = row["lanes"][lane]
            checks += [
                Check(f"rows[{i}].lanes.{lane}.auprc", st["auprc"],
                      lambda p=p, y=y: ap(y, p)),
                Check(f"rows[{i}].lanes.{lane}.auroc", st["auroc"],
                      lambda p=p, y=y: auroc(y, p)),
                Check(f"rows[{i}].lanes.{lane}.norm_auprc", st["norm_auprc"],
                      lambda p=p, y=y, base=base:
                      (aps(y, p) - base) / (1 - base))]
    seeds = ", ".join(str(r["seed"]) for r in doc["rows"])
    how = (f"retrained at the file's {doc['steps']} steps (the pilot stored "
           "no parameters)" if trained else "predicted from the stored "
           "params_flat")
    return Plan(lanes, checks,
                covered=[f"circuit ({how}), seeds {seeds}"]
                + [f"{t} twin, seeds {seeds}" for t in g.TWINS])


def plan_f107(doc) -> Plan:
    import data
    import f107_shots as g
    src = {r["seed"]: r for r in json.loads(
        g.F106.read_text(encoding="utf-8"))["rows"]}
    df = data.load_ulb()
    lanes, checks = [], []
    for i, row in enumerate(doc["rows"]):
        s = row["seed"]
        scores: dict = {}
        rebuilt = g.seed_shots(df, src[s], scores)
        checks += same_leaves(row, rebuilt, f"rows[{i}]")
        for m, key, stored in [("exact", "exact_outcome", row["exact_auprc"])] + [
                (m, f"shots_{m}_outcome", row["auprc_at_shots"][str(m)])
                for m in g.SHOTS]:
            y, p = scores[m]
            y = np.asarray(y).astype(int)
            lanes.append(Lane(f"f107_{m if m == 'exact' else f'shots_{m}'}",
                              s, y, p, place=("rows", i), key=key))
            checks.append(Check(f"rows[{i}].{key} AUPRC from the block's "
                                "scores", stored, lambda y=y, p=p: ap(y, p)))
    seeds = ", ".join(str(r["seed"]) for r in doc["rows"])
    return Plan(lanes, checks,
                covered=[f"exact circuit (F106 stored params), seeds {seeds}"]
                + [f"{m} shots, seeds {seeds}" for m in g.SHOTS],
                notes={"row_check": "every stored leaf of each row was "
                       "rebuilt by f107_shots.seed_shots and compared",
                       "score_scale": "the per-row score is the circuit "
                       "logit b + <Z> w, as the file's AUPRC used it"})


def plan_f109(doc, stem: str) -> Plan:
    import data
    import f103_tier1 as t1
    import f109_ladder as g
    seeds = doc["seeds"]
    lanes, checks = [], []
    skip = ("lane_seconds", "pipeline_seconds")
    for name in g.SPECTRA:
        P, y, cols = g.spectra_phases(name)
        for i, s in enumerate(seeds):
            sc: dict = {}
            rebuilt = dict(t1.run_target(name, P, y, s, scores=sc),
                           features=cols)
            tier1_lanes(lanes, checks, f"{stem}_{name}", ("datasets", name, i),
                        s, doc["datasets"][name][i], rebuilt, sc, skip)
    for i, s in enumerate(seeds):
        sc = {}
        rebuilt = g.ulb_run(s, sc)
        tier1_lanes(lanes, checks, f"{stem}_ulb", ("datasets", "ulb", i), s,
                    doc["datasets"]["ulb"][i], rebuilt, sc, skip)
    cis = data.load_ieee_cis_train()
    if doc["mode"] == "pilot":
        import ieee_harness
        cis = ieee_harness.time_sample(cis, g.PILOT_FRAC)
    checks.append(Check("ieee_rows_available", doc["ieee_rows_available"],
                        lambda n=len(cis): n, tol=0.0))
    for i, s in enumerate(seeds):
        sc = {}
        pair = g.ieee_runs(cis, s, sc)
        for side in ("before", "after"):
            tier1_lanes(lanes, checks, f"{stem}_ieee_{side}",
                        ("datasets", f"ieee_{side}", i), s,
                        doc["datasets"][f"ieee_{side}"][i], pair[side],
                        sc[side], skip)
    sl = ", ".join(map(str, seeds))
    return Plan(lanes, checks,
                covered=[f"{n} (seeds {sl}): gam, ga2m, hgb, joint"
                         for n in (*g.SPECTRA, "ulb", "ieee_before",
                                   "ieee_after")],
                uncovered={"energy_steel": "rows copied from "
                           "f103_tier1.json (cited); their blocks are there"},
                notes={"row_check": "every stored leaf of each target row "
                       "except the seconds was rebuilt by the generator's "
                       "own functions and compared",
                       "metric": "the file's lane scores are test AUROC, "
                                 "stored rounded to 4 decimals"})


ADAPTERS: dict[str, Callable] = {
    "f107_shots": plan_f107,
    "f109_ladder_pilot": lambda doc: plan_f109(doc, "f109_pilot"),
    "f109_ladder": lambda doc: plan_f109(doc, "f109"),
    "f106_dequant_pilot": lambda doc: plan_f106(doc, "f106_pilot"),
    "f106_dequant": lambda doc: plan_f106(doc, "f106"),
    "f103_tier1_pilot": lambda doc: plan_f103(doc, "f103_pilot"),
    "f103_tier1": lambda doc: plan_f103(doc, "f103"),
    "f108_ceiling": lambda doc: plan_f108(doc, "f108"),
    "f108_ceiling_pilot": lambda doc: plan_f108(doc, "f108_pilot"),
    "f130_ulb_hgb_check": plan_f130_hgb,
    "f142_readout": plan_f142,
    "f144_proxy_twin": plan_f144,
    "f112_intervals": plan_f112,
    "f113_oracle_gap": plan_f113,
}


def run_one(name: str, write: bool) -> dict:
    path = RESULTS / f"{name}.json"
    doc = json.loads(read_exact(path))
    plan = ADAPTERS[name](doc)
    if write:
        return apply(path, plan)
    with tempfile.TemporaryDirectory() as tmp:
        return apply(path, plan, write=False, pred_dir=Path(tmp))


def main(argv=None) -> int:
    ap_ = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap_.add_argument("name", choices=sorted(ADAPTERS))
    ap_.add_argument("--dry-run", action="store_true",
                     help="rebuild and check; write nothing to the result")
    a = ap_.parse_args(argv)
    meta = run_one(a.name, write=not a.dry_run)
    mc = meta["metric_check"]
    print(json.dumps({"file": a.name, "written": not a.dry_run,
                      "n_blocks": meta["n_blocks"],
                      "n_checks": mc["n_checks"],
                      "max_abs_diff": mc["max_abs_diff"],
                      "nonzero_diffs": {c["label"]: [c["stored"],
                                                     c["recomputed"],
                                                     c["tolerance"]]
                                        for c in mc["not_identical"]},
                      "covered": meta["covered_lanes"],
                      "uncovered": meta["uncovered_lanes"]}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
