"""F197 (Sprint 34 Task G, #141): does the re-entry's measure saturate?

Experiment 5's re-entry is entry P2-A3 in
`experiments/phase2/PREREGISTRATION_AMENDMENTS.md`, committed before this
module ran. Its measure is the average precision (AUPRC) of a lane within
a ProductCD segment. Experiment 5's first measure, recall at the 0.5%
budget within the segment, saturated: on C, R, H and S the champion's
alerts were all frauds, so no lane could beat it.

This check reads the champion's stored month-4 scores only (F174's
LightGBM lane, seeds 42-51). No lane is compared, no edge is computed and
no proxy or HGB score is read: those are the run, which waits for the
team lead's approval of the entry.

1. The reference, first: on the same scores, the old measure must show
   saturation on at least one segment (the champion's recall equals the
   most its budget allows, min(k, positives) / positives, on every
   seed). If it does not, this check cannot tell the two measures apart,
   and the result says so.
2. The new measure: on each segment that can be scored, the champion's
   in-segment AUPRC must leave room for the entry's minimum edge, 0.01,
   on every seed (AUPRC at most 1 - 0.01). A segment without that room
   is reported as saturated under the new measure too.

    <venv python> experiments/phase2/src/f197_saturation.py

Zero metered seconds. Writes `experiments/phase2/results/f197_saturation.json`.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "experiments" / "src"))
import exp5_router as e5  # noqa: E402

OUT = ROOT / "experiments" / "phase2" / "results" / "f197_saturation.json"
LONG_RUN = False                 # reads stored scores; under a minute
MIN_EDGE = e5.MIN_EDGE           # 0.01, the entry's minimum edge
SEGMENTS = e5.SEGMENTS


def most_recall(y: np.ndarray, idx: np.ndarray) -> float:
    """The most recall a 0.5% budget within `idx` allows."""
    k = math.ceil(e5.BUDGET * len(idx))
    pos = int(y[idx].sum())
    return min(k, pos) / pos if pos else float("nan")


def old_saturated(y, s, idx) -> bool:
    return e5.recall_at_budget(y, s, idx) >= most_recall(y, idx)


def segment_auprc(y, s, idx) -> float:
    from sklearn.metrics import average_precision_score
    if int(y[idx].sum()) == 0:
        return float("nan")
    return float(average_precision_score(y[idx], s[idx]))


def has_room(auprc: float) -> bool:
    """Room for the minimum edge above the champion."""
    return auprc <= 1.0 - MIN_EDGE


def segment_reading(per_seed: list[dict]) -> dict:
    """A segment saturates under a measure when it does on every seed."""
    return {"old_saturated_on_every_seed": all(r["old_saturated"]
                                               for r in per_seed),
            "new_room_on_every_seed": all(r["new_room"] for r in per_seed),
            "min_champion_auprc": min(r["champion_auprc"] for r in per_seed),
            "max_champion_auprc": max(r["champion_auprc"] for r in per_seed)}


def summary(segments: dict) -> dict:
    old = [k for k, v in segments.items() if v["old_saturated_on_every_seed"]]
    room = [k for k, v in segments.items() if v["new_room_on_every_seed"]]
    can_fire = bool(old)
    return {"reference_can_fire": can_fire,
            "old_measure_saturated_on": old,
            "new_measure_has_room_on": room,
            "new_measure_saturated_on": [k for k in segments if k not in room],
            "finding": (
                "the reference did not fire: on these scores the old "
                "measure never saturates, so this check cannot tell the "
                "measures apart" if not can_fire else
                "the new measure leaves room for the minimum edge on "
                + (", ".join(room) if room else "no segment")
                + "; the old measure saturates on " + ", ".join(old))}


def require_same_labels(stored: np.ndarray, rebuilt: np.ndarray,
                        where: str) -> None:
    """The stopping rule: a stored label vector that differs from the
    rebuilt month 4 stops the check."""
    if not np.array_equal(stored, rebuilt):
        raise RuntimeError(f"{where}: stored labels differ from the "
                           "rebuilt month 4")


def saturation_doc(segments: dict, blocks: list, n_seeds: int) -> dict:
    """The result, marked complete only when every scored segment has
    every seed and there is an outcome block per seed."""
    if (not segments or n_seeds == 0 or len(blocks) != n_seeds
            or any(len(v["per_seed"]) != n_seeds for v in segments.values())):
        raise RuntimeError(f"{len(segments)} segments, {len(blocks)} "
                           f"outcome blocks for {n_seeds} seeds; not complete")
    return {"card": "F197", "sprint": 34, "phase": 2, "evidence_tag": "SIM",
            "metered_seconds": 0, "dataset": "ieee_cis",
            "entry": "experiments/phase2/PREREGISTRATION_AMENDMENTS.md P2-A3",
            "lane": e5.CHAMPION, "min_edge": MIN_EDGE,
            "segments": segments, "summary": summary(segments),
            "outcomes": blocks, "complete": True}


def main(argv: list[str]) -> None:
    if argv:
        raise SystemExit(f"usage: f197_saturation.py; got {argv}")
    run()


def run() -> None:
    import outcome_record as orec
    import provenance
    rid, _ = provenance.start(OUT, resumable=False)
    y, seg = e5.month4_segments()
    segments, blocks = {}, []
    for lab in SEGMENTS:
        idx = np.flatnonzero(seg == lab)
        if int(y[idx].sum()) == 0:
            continue
        per_seed = []
        for seed in e5.SEEDS:
            ys, s, src = e5.scores(e5.CHAMPION, seed)
            require_same_labels(ys, y, f"{e5.CHAMPION}/{seed}")
            a = segment_auprc(y, s, idx)
            per_seed.append({"seed": seed, "rows": int(len(idx)),
                             "positives": int(y[idx].sum()),
                             "old_saturated": old_saturated(y, s, idx),
                             "champion_auprc": a, "new_room": has_room(a)})
        segments[lab] = {"per_seed": per_seed, **segment_reading(per_seed)}
        print(lab, segments[lab]["old_saturated_on_every_seed"],
              segments[lab]["new_room_on_every_seed"],
              round(segments[lab]["max_champion_auprc"], 4), flush=True)
    for seed in e5.SEEDS:
        ys, s, src = e5.scores(e5.CHAMPION, seed)
        blocks.append(orec.record(f"f197_{e5.CHAMPION}", seed, ys, s,
                                  source=src))
    doc = saturation_doc(segments, blocks, len(e5.SEEDS))
    provenance.write_result(OUT, doc, __file__, list(e5.SEEDS), rid)
    print(doc["summary"]["finding"], flush=True)
    print("complete", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
