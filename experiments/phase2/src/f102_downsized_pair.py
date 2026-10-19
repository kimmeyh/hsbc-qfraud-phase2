"""F102 (Sprint 27 Task C): section 5's downsized matched pair, from code.

The Phase 2 draft's section 5 gave the energy_steel figures from the F102
card (2026-10-05) and asked for them to be recomputed by code before
filing. This computes, on each frozen SPECTRA cell and each of the five
seeds, the test fold's in-segment and complement counts and the largest
size-and-rate-matched pair both sides can supply:

    positives per side = min(segment positives, complement positives)
    negatives per side = round(positives per side x segment negatives /
                               segment positives)

so each side keeps the segment's own positive rate; it is feasible when the
complement also holds that many negatives. The AUC interval widening is the
ratio of sqrt(1/P + 1/N) after and before downsizing, the leading term of
the Hanley-McNeil standard error. It is an approximation, labeled so.

Zero metered seconds; reads the SPECTRA splits only. Writes
`experiments/phase2/results/f102_downsized_pair.json`.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import soft_votes as sv                              # noqa: E402  (Phase 2)
import spectra_segment as ss                         # noqa: E402  (Phase 1, read-only)

OUT = sv.OUT_DIR / "f102_downsized_pair.json"


def pair(seg_pos: int, seg_neg: int, comp_pos: int, comp_neg: int) -> dict:
    p = min(seg_pos, comp_pos)
    n = int(round(p * seg_neg / seg_pos)) if seg_pos else 0
    feasible = bool(p > 0 and n <= comp_neg and n <= seg_neg)
    widen = (float(np.sqrt((1 / p + 1 / n) / (1 / seg_pos + 1 / seg_neg)))
             if feasible and n > 0 else None)
    return {"positives_per_side": p, "negatives_per_side": n,
            "feasible": feasible,
            "segment_positives_kept": round(p / seg_pos, 4) if seg_pos else None,
            "already_matchable_without_downsizing": bool(seg_pos <= comp_pos),
            "auc_interval_width_ratio_approx": (round(widen, 4)
                                                if widen else None)}


def main() -> int:
    rows = []
    for cell in ss.FROZEN_CELLS:
        name = cell["dataset"].replace("spectra_", "")
        for seed in sv.SEEDS:
            split, _ = ss._prep_spectra(name, seed)
            seg = split.X_test[ss.SEGMENT_FLAG].to_numpy().astype(bool)
            y = split.y_test.to_numpy().astype(int)
            counts = {"segment_positives": int(y[seg].sum()),
                      "segment_negatives": int((1 - y[seg]).sum()),
                      "complement_positives": int(y[~seg].sum()),
                      "complement_negatives": int((1 - y[~seg]).sum())}
            r = {"dataset": cell["dataset"], "seed": seed, **counts,
                 **pair(counts["segment_positives"],
                        counts["segment_negatives"],
                        counts["complement_positives"],
                        counts["complement_negatives"])}
            rows.append(r)
            print(json.dumps(r), flush=True)
    OUT.write_text(json.dumps({
        "generator": "experiments/phase2/src/f102_downsized_pair.py",
        "card": "F102", "sprint": 27, "phase": 2, "evidence_tag": "SIM",
        "metered_seconds": 0, "date": time.strftime("%Y-%m-%d"),
        "rule": "positives per side = min(segment, complement positives); "
                "negatives per side at the segment's own rate",
        "widening": "sqrt(1/P + 1/N) after over before; Hanley-McNeil "
                    "leading term, an approximation",
        "rows": rows}, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
