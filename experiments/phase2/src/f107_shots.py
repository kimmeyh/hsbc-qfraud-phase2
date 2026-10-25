"""F107 (Sprint 27 Task J): shot budget of the F106 circuit.

The entry is `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6,
"F107", written before this module existed. It records why the card's
Schmidt-rank threshold (Wang et al., arXiv:2306.03481) does not transfer
to a classical-input classifier, and what is measured instead:

  per seed, test AUPRC with each row's <Z_q> estimated from m shots, each
  shot one 8-bit outcome drawn from |psi|^2 (multinomial over 256
  outcomes), for m in SHOTS, against the exact statevector; the critical
  shot budget is the smallest m within MARGIN of exact.

Beside it: the effective Schmidt rank of the output state across the
qubits 0-3 | 4-7 cut, and the |<Z_q>| distribution.

    <venv python> experiments/phase2/src/f107_shots.py

Reads the trained parameters in `f106_dequant.json` and rebuilds each
seed's test phases with F106's own code. Zero metered seconds. Writes
`experiments/phase2/results/f107_shots.json`.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "experiments" / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import f106_dequant as fd                            # noqa: E402  (Phase 2)

F106 = ROOT / "experiments" / "phase2" / "results" / "f106_dequant.json"
OUT = ROOT / "experiments" / "phase2" / "results" / "f107_shots.json"
SHOTS = (10, 100, 1000, 10000)
MARGIN = 0.005
SCHMIDT_ROWS = 500
CUT = 4                                              # qubits 0-3 | 4-7
# F106's `predict` chunk. The summation order differs by chunk size, scores
# move by ~1e-14, near-tied rows reorder and AUPRC moves by ~1e-4, so any
# other size fails the exact-AUPRC refusal below (seed 42: 0.70514 at 4096).
CHUNK = 8192


def probabilities(psi: np.ndarray) -> np.ndarray:
    p = np.abs(psi) ** 2
    return p / p.sum(axis=1, keepdims=True)


def shot_expectations(p: np.ndarray, m: int, rng: np.random.Generator):
    """<Z_q> per row from m joint shots: (n, Q)."""
    counts = rng.multinomial(m, p)
    return (counts / m) @ fd.Z.T


def effective_schmidt_rank(psi: np.ndarray, cut: int = CUT) -> np.ndarray:
    """exp(entanglement entropy) across the cut, per row."""
    A = psi.reshape(len(psi), 2 ** cut, 2 ** (fd.N_QUBITS - cut))
    s2 = np.linalg.svd(A, compute_uv=False) ** 2
    s2 = s2 / s2.sum(axis=1, keepdims=True)
    S = -(s2 * np.log(np.clip(s2, 1e-300, 1))).sum(axis=1)
    return np.exp(S)


def critical_budget(auprc: dict, exact: float) -> str | int:
    for m in SHOTS:
        if abs(auprc[m] - exact) <= MARGIN:
            return m
    return f"above {SHOTS[-1]}"


def seed_shots(df, row: dict, scores: dict | None = None) -> dict:
    """`scores`, opt-in (Sprint 28 DV4 outcome backfill): a dict that
    receives (test labels, per-row test scores) under "exact" and each shot
    budget. The row returned is the same with or without it."""
    from sklearn.metrics import average_precision_score
    seed = row["seed"]
    d = fd.prepare(df, seed)
    if d["feats"] != row["features"]:
        raise SystemExit(f"REFUSING: seed {seed} rebuilt features "
                         f"{d['feats']}, F106 recorded {row['features']}")
    params = fd.Params(0.5, seed)
    params.set_flat(np.array(row["params_flat"]))
    Pte, yte = d["Pte"], d["yte"]
    rng = np.random.default_rng(2000 + seed)
    exact_m, shot_m = [], {m: [] for m in SHOTS}
    for i in range(0, len(Pte), CHUNK):
        p = probabilities(fd.state(params, Pte[i:i + CHUNK]))
        exact_m.append(p @ fd.Z.T)
        for m in SHOTS:
            shot_m[m].append(shot_expectations(p, m, rng))
    exact_m = np.vstack(exact_m)

    def ap(mz):
        return float(average_precision_score(yte, params.b + mz @ params.w))
    exact = ap(exact_m)
    if abs(exact - row["lanes"]["circuit"]["auprc"]) > 1e-9:
        raise SystemExit(f"REFUSING: seed {seed} exact AUPRC {exact} differs "
                         f"from F106's {row['lanes']['circuit']['auprc']}")
    if scores is not None:
        scores["exact"] = (yte, params.b + exact_m @ params.w)
        for m in SHOTS:
            scores[m] = (yte, params.b + np.vstack(shot_m[m]) @ params.w)
    auprc = {m: ap(np.vstack(shot_m[m])) for m in SHOTS}
    pick = np.random.default_rng(seed).choice(len(Pte), SCHMIDT_ROWS,
                                               replace=False)
    r_eff = effective_schmidt_rank(fd.state(params, Pte[pick]))
    az = np.abs(exact_m)
    out = {"seed": seed, "exact_auprc": exact,
           "auprc_at_shots": {str(m): v for m, v in auprc.items()},
           "critical_shot_budget": critical_budget(auprc, exact),
           "effective_schmidt_rank": {
               "mean": round(float(r_eff.mean()), 3),
               "quantiles_10_50_90": [round(float(x), 3) for x in
                                      np.percentile(r_eff, [10, 50, 90])],
               "max_possible": 2 ** CUT},
           "abs_z": {"mean": round(float(az.mean()), 4),
                     "quantiles_10_50_90": [round(float(x), 4) for x in
                                            np.percentile(az, [10, 50, 90])]}}
    print(f"  s{seed} exact {exact:.4f} " + " ".join(
        f"m{m} {v:.4f}" for m, v in auprc.items())
        + f" critical {out['critical_shot_budget']}"
        f" r_eff {out['effective_schmidt_rank']['mean']}", flush=True)
    return out


def main() -> int:
    import data
    src = json.loads(F106.read_text(encoding="utf-8"))
    if src.get("mode") != "run":
        raise SystemExit("REFUSING: f106_dequant.json is not the full run")
    t0 = time.perf_counter()
    df = data.load_ulb()
    rows = [seed_shots(df, r) for r in src["rows"]]
    OUT.write_text(json.dumps({
        "generator": "experiments/phase2/src/f107_shots.py",
        "card": "F107", "sprint": 27, "phase": 2, "evidence_tag": "SIM",
        "metered_seconds": 0, "date": time.strftime("%Y-%m-%d"),
        "entry": "experiments/phase2/PREREGISTRATION_DRAFT.md section 6, F107",
        "source_circuits": "experiments/phase2/results/f106_dequant.json",
        "f106_outcome": src["outcome"], "shots": list(SHOTS),
        "margin": MARGIN, "rows": rows,
        "elapsed_s": round(time.perf_counter() - t0, 1)}, indent=1) + "\n",
        encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
