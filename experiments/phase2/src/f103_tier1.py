"""F103 (Sprint 27 Task F): SPECTRA Tier 1, reimplemented, on UCI Steel.

The entry is `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6,
"F103", written before this module first ran; every choice the Fourier
Wall paper (arXiv:2607.15815) leaves open is fixed there and repeated
here. SPECTRA's own code is proprietary; this is a reimplementation from
the paper's text (Algorithm 1, sections 3 and 6.4).

Lanes, on identical phases and splits:
  GAM    one trained frequency per phase (periodogram of the centered
         label on training rows), cos and sin, logistic regression
  GA2M   GAM basis plus all pairwise products of the per-feature terms
  HGB    scikit-learn defaults
  JOINT  GA2M basis plus up to 6 greedy 3-way joint terms cos/sin(u),
         u = sum_j f_j phi_j, the subset and frequency vector found by a
         coarse-to-fine periodogram scan of the current residual

Gates: g1 off-grid mass (exploratory estimator), g2 GAM > chance, g3 HGB -
GAM > 0, g4 JOINT - GA2M > 0, g5 d x q <= 14.

Targets: the real target (`target_real`, five native phases), the sparse
pocket (Eq. 6) and the dense substrate (a 7-site Heisenberg chain), each
rebuilt from the raw fields by the paper's section 6.4. A permuted-label
reference runs first.

    <venv python> experiments/phase2/src/f103_tier1.py pilot
    <venv python> experiments/phase2/src/f103_tier1.py run

Zero metered seconds. Writes `experiments/phase2/results/f103_tier1.json`.
"""
from __future__ import annotations

import itertools
import json
import sys
import time
from pathlib import Path

import numpy as np
from scipy.stats import rankdata

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "experiments" / "data" / "spectra" / "spectra_energy_steel.csv"
OUT = ROOT / "experiments" / "phase2" / "results" / "f103_tier1.json"
SEEDS = (42, 43, 44, 45, 46)
TEST_SIZE = 0.30

COARSE_1D = np.arange(0.25, 8.0 + 1e-9, 0.05)
FINE_STEP_1D, FINE_HALF_1D = 0.005, 0.05
JOINT_TERMS, JOINT_ORDER = 6, 3
COARSE_AXIS = np.arange(0.5, 8.0 + 1e-9, 0.5)
FINE_STEP_J, FINE_HALF_J = 0.05, 0.5
G1_GRID = np.arange(0.05, 8.0 + 1e-9, 0.05)
G1_OFF, G1_THRESHOLD = 0.1, 0.3
QUBIT_BUDGET = 14

SPARSE_W, SPARSE_F, SPARSE_G, SPARSE_NOISE = 0.25, (3.7, 5.1, 6.8), 6.0, 0.01
DENSE_N, DENSE_T, DENSE_STEPS = 6000, 3.0, 3

KNOWN = {"real_g2_gam_auc": (0.94, 0.03),
         "sparse_joint_minus_ga2m": (0.37, 0.05),
         "dense_hgb_minus_gam": (0.15, 0.05),
         "dense_joint_minus_ga2m": (0.00, 0.05)}
PAPER_FREQS = (3.67, 5.13, 6.83)
FREQ_TOL = 0.05


# ------------------------------------------------------------------ phases

def rank_phase(v: np.ndarray) -> np.ndarray:
    """The paper's rank phase, 2 pi (rank - 1/2) / n - pi, on all rows."""
    return 2 * np.pi * (rankdata(v) - 0.5) / len(v) - np.pi


def whiten_rerank(P: np.ndarray) -> np.ndarray:
    """PCA-whiten a phase block, then re-rank each component to a uniform
    phase (section 6.4; covariates only)."""
    X = P - P.mean(axis=0)
    vals, vecs = np.linalg.eigh(np.cov(X, rowvar=False))
    Z = X @ vecs / np.sqrt(np.maximum(vals, 1e-12))
    return np.column_stack([rank_phase(Z[:, j]) for j in range(Z.shape[1])])


def load_raw():
    import pandas as pd
    return pd.read_csv(DATA)


def real_phases(d) -> tuple[np.ndarray, list[str]]:
    phi = np.column_stack([
        2 * np.pi * d["NSM"].to_numpy() / 86400 - np.pi,
        rank_phase(np.log1p(d["Usage_kWh"].to_numpy())),
        rank_phase(np.log1p(
            d["Lagging_Current_Reactive.Power_kVarh"].to_numpy())),
        2 * np.pi * d["day_of_year"].to_numpy() / 365 - np.pi,
        2 * np.pi * d["dow_num"].to_numpy() / 7 - np.pi])
    return phi, ["tod", "load", "reactive", "season", "dow"]


def release_jitter(d) -> dict:
    """How far the release's phase columns sit from the paper's recipe."""
    phi, _ = real_phases(d)
    out = {}
    for j, col in enumerate(["tod_phase", "usage_phase", "reactive_phase",
                             "season_phase", "dow_phase"]):
        e = np.angle(np.exp(1j * (d[col].to_numpy() - phi[:, j])))
        out[col] = {"mean": round(float(e.mean()), 5),
                    "sd": round(float(e.std()), 5),
                    "max_abs": round(float(np.abs(e).max()), 4)}
    return out


def sparse_pocket(d, seed: int):
    phi, _ = real_phases(d)
    P = whiten_rerank(phi[:, :3])
    rng = np.random.default_rng(seed)
    off = rng.uniform(0, 2 * np.pi, size=4)
    f = np.asarray(SPARSE_F)
    z = (SPARSE_W * sum(np.cos(f[j] * P[:, j] + off[j]) for j in range(3))
         + np.cos(P @ f + off[3]))
    tau = float(np.median(z))
    p = 1.0 / (1.0 + np.exp(-SPARSE_G * (z - tau)))
    y = (rng.uniform(size=len(z)) < p).astype(int)
    flip = rng.uniform(size=len(y)) < SPARSE_NOISE
    y[flip] = 1 - y[flip]
    return P, y


DENSE_FIELDS = ["NSM", "Usage_kWh", "Lagging_Current_Reactive.Power_kVarh",
                "day_of_year", "Leading_Current_Reactive_Power_kVarh",
                "Lagging_Current_Power_Factor", "Leading_Current_Power_Factor"]


def _bond_unitary(n: int, k: int, theta: float) -> np.ndarray:
    """exp(-i theta (XX + YY + ZZ)) on qubits k, k+1 of n, as 2^n x 2^n."""
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.diag([1.0, -1.0]).astype(complex)
    S = sum(np.kron(A, A) for A in (X, Y, Z))
    vals, vecs = np.linalg.eigh(S)
    U2 = vecs @ np.diag(np.exp(-1j * theta * vals)) @ vecs.conj().T
    return np.kron(np.kron(np.eye(2 ** k), U2), np.eye(2 ** (n - k - 2)))


def chain_observable(P: np.ndarray, J: np.ndarray, t: float = DENSE_T,
                     steps: int = DENSE_STEPS) -> np.ndarray:
    """<sum_i Z_i Z_{i+1}> after first-order Trotter evolution of |+>^n
    under H = sum_k J_k (XX+YY+ZZ)_{k,k+1} + sum_i phi_i Z_i."""
    rows, n = P.shape
    dim = 2 ** n
    dt = t / steps
    bonds = np.eye(dim, dtype=complex)
    for k in range(n - 1):                     # bond order k = 1..n-1
        bonds = _bond_unitary(n, k, J[k] * dt) @ bonds
    bits = ((np.arange(dim)[:, None] >> (n - 1 - np.arange(n))) & 1)
    zval = 1.0 - 2.0 * bits                    # (dim, n): +1 for |0>
    field = P @ zval.T                         # (rows, dim): sum_i phi_i z_i
    psi = np.full((rows, dim), 1.0 / np.sqrt(dim), dtype=complex)
    for _ in range(steps):
        psi = psi @ bonds.T                    # bonds, then the field
        psi = psi * np.exp(-1j * dt * field)
    zz = sum(zval[:, i] * zval[:, i + 1] for i in range(n - 1))
    return (np.abs(psi) ** 2) @ zz


def dense_substrate(d, seed: int):
    rng = np.random.default_rng(seed)
    cols = []
    for c in DENSE_FIELDS:
        v = d[c].to_numpy().astype(float)
        if c in ("Usage_kWh", "Lagging_Current_Reactive.Power_kVarh"):
            v = np.log1p(v)
        cols.append(rank_phase(v))
    P_all = whiten_rerank(np.column_stack(cols))
    idx = rng.choice(len(P_all), size=DENSE_N, replace=False)
    P = P_all[idx]
    J = rng.uniform(0.5, 1.5, size=P.shape[1] - 1)
    o = chain_observable(P, J)
    return P, (o > np.median(o)).astype(int)


# ------------------------------------------------------------------- lanes

def _periodogram_1d(phi, r, freqs):
    return np.abs(np.exp(1j * np.outer(freqs, phi)) @ r) ** 2


def _ls_power(phi, r, freqs):
    """Least-squares (Lomb-Scargle) periodogram: the variance of r that
    cos(f phi) and sin(f phi), centered, explain together. On a bounded
    phase interval cos and sin of a non-integer f are not orthogonal, so
    the plain periodogram's peak is biased; this one is not."""
    A = np.outer(freqs, phi)
    C, S = np.cos(A), np.sin(A)
    C -= C.mean(axis=1, keepdims=True)
    S -= S.mean(axis=1, keepdims=True)
    cc, ss, cs = (C * C).sum(1), (S * S).sum(1), (C * S).sum(1)
    rc, rs = C @ r, S @ r
    det = np.maximum(cc * ss - cs * cs, 1e-12)
    return (ss * rc * rc - 2 * cs * rc * rs + cc * rs * rs) / det


def trained_frequency(phi: np.ndarray, y: np.ndarray) -> float:
    r = y - y.mean()
    f0 = COARSE_1D[int(np.argmax(_ls_power(phi, r, COARSE_1D)))]
    fine = np.arange(max(0.01, f0 - FINE_HALF_1D), f0 + FINE_HALF_1D + 1e-9,
                     FINE_STEP_1D)
    return float(fine[int(np.argmax(_ls_power(phi, r, fine)))])


def gam_basis(P, freqs, harmonics=1):
    cols = []
    for j, f in enumerate(freqs):
        for h in range(1, harmonics + 1):
            cols += [np.cos(h * f * P[:, j]), np.sin(h * f * P[:, j])]
    return np.column_stack(cols)


def ga2m_basis(P, freqs):
    B = gam_basis(P, freqs)
    d = P.shape[1]
    prods = []
    for a, b in itertools.combinations(range(d), 2):
        for ca in (2 * a, 2 * a + 1):
            for cb in (2 * b, 2 * b + 1):
                prods.append(B[:, ca] * B[:, cb])
    return np.column_stack([B] + prods) if prods else B


def _lr(Btr, ytr):
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import make_pipeline
    return make_pipeline(StandardScaler(), LogisticRegression(
        C=1.0, max_iter=2000)).fit(Btr, ytr)


def _auc(y, p):
    from sklearn.metrics import roc_auc_score
    return float(roc_auc_score(y, p))


def joint_scan(P: np.ndarray, r: np.ndarray, subset: tuple) -> tuple:
    """(power, frequency vector) maximizing |sum r e^{i <f, phi_S>}|^2 over
    the coarse grid with signs, then a fine grid around the maximum."""
    A = [P[:, j] for j in subset]

    def best(axes):
        E = [np.exp(1j * np.outer(ax, a)) for ax, a in zip(axes, A)]
        T = np.einsum("n,an,bn,cn->abc", r, E[0], E[1], E[2], optimize=True)
        pw = np.abs(T) ** 2
        i = np.unravel_index(int(np.argmax(pw)), pw.shape)
        return float(pw[i]), np.array([axes[k][i[k]] for k in range(3)])
    signed = np.concatenate([-COARSE_AXIS[::-1], COARSE_AXIS])
    _, f0 = best([COARSE_AXIS, signed, signed])
    fine = [np.arange(f - FINE_HALF_J, f + FINE_HALF_J + 1e-9, FINE_STEP_J)
            for f in f0]
    return best(fine)


def fit_lanes(Ptr, ytr, Pte, yte, seed: int, joint: bool = True,
              secondary: bool = False) -> dict:
    from sklearn.ensemble import HistGradientBoostingClassifier
    t0 = time.perf_counter()
    freqs = [trained_frequency(Ptr[:, j], ytr) for j in range(Ptr.shape[1])]
    out = {"trained_frequencies": [round(f, 3) for f in freqs]}
    gam = _lr(gam_basis(Ptr, freqs), ytr)
    out["gam"] = _auc(yte, gam.predict_proba(gam_basis(Pte, freqs))[:, 1])
    if secondary:
        for h in (2, 3):
            m = _lr(gam_basis(Ptr, freqs, h), ytr)
            out[f"gam_{h}_harmonics"] = _auc(
                yte, m.predict_proba(gam_basis(Pte, freqs, h))[:, 1])
    Gtr, Gte = ga2m_basis(Ptr, freqs), ga2m_basis(Pte, freqs)
    ga2m = _lr(Gtr, ytr)
    p_tr = ga2m.predict_proba(Gtr)[:, 1]
    out["ga2m"] = _auc(yte, ga2m.predict_proba(Gte)[:, 1])
    hgb = HistGradientBoostingClassifier(random_state=seed).fit(Ptr, ytr)
    out["hgb"] = _auc(yte, hgb.predict_proba(Pte)[:, 1])
    out["lane_seconds"] = {"gam_ga2m_hgb": round(time.perf_counter() - t0, 1)}
    if joint:
        t1 = time.perf_counter()
        Jtr, Jte, terms = Gtr, Gte, []
        subsets = list(itertools.combinations(range(Ptr.shape[1]),
                                              JOINT_ORDER))
        for _ in range(JOINT_TERMS):
            r = ytr - p_tr
            scans = [(joint_scan(Ptr, r, S), S) for S in subsets]
            (pw, f), S = max(scans, key=lambda x: x[0][0])
            u_tr, u_te = Ptr[:, S] @ f, Pte[:, S] @ f
            Jtr = np.column_stack([Jtr, np.cos(u_tr), np.sin(u_tr)])
            Jte = np.column_stack([Jte, np.cos(u_te), np.sin(u_te)])
            m = _lr(Jtr, ytr)
            p_tr = m.predict_proba(Jtr)[:, 1]
            terms.append({"subset": list(S),
                          "freqs": [round(float(x), 3) for x in f]})
        out["joint"] = _auc(yte, m.predict_proba(Jte)[:, 1])
        out["joint_terms"] = terms
        out["lane_seconds"]["joint"] = round(time.perf_counter() - t1, 1)
    return out


def g1_off_grid(Ptr, ytr) -> float:
    """Exploratory g1 estimator (no published value): the fraction of 1-D
    periodogram mass, over every phase, at frequencies farther than 0.1
    from an integer."""
    r = ytr - ytr.mean()
    off = np.abs(G1_GRID - np.round(G1_GRID)) > G1_OFF
    tot = offm = 0.0
    for j in range(Ptr.shape[1]):
        pw = _periodogram_1d(Ptr[:, j], r, G1_GRID)
        tot += pw.sum()
        offm += pw[off].sum()
    return float(offm / tot) if tot > 0 else float("nan")


def gates(lanes: dict, rho_off: float, d: int) -> dict:
    g = {"g1_rho_off": round(rho_off, 4),
         "g1_pass": bool(rho_off > G1_THRESHOLD),
         "g2_gam_auc": round(lanes["gam"], 4),
         "g2_pass": bool(lanes["gam"] > 0.5),
         "g3_hgb_minus_gam": round(lanes["hgb"] - lanes["gam"], 4),
         "g3_pass": bool(lanes["hgb"] > lanes["gam"]),
         "g5_qubits_q1": d, "g5_qubits_q2": 2 * d,
         "g5_pass": bool(d <= QUBIT_BUDGET)}
    if "joint" in lanes:
        g["g4_joint_minus_ga2m"] = round(lanes["joint"] - lanes["ga2m"], 4)
        g["g4_pass"] = bool(lanes["joint"] > lanes["ga2m"])
    g["tier1"] = ("refuse" if not all(v for k, v in g.items()
                                      if k.endswith("_pass")) else "candidate")
    return g


# -------------------------------------------------------------------- runs

def _split(n, y, seed):
    from sklearn.model_selection import train_test_split
    return train_test_split(np.arange(n), test_size=TEST_SIZE, stratify=y,
                            random_state=seed)


def run_target(name: str, P: np.ndarray, y: np.ndarray, seed: int,
               secondary: bool = False) -> dict:
    tr, te = _split(len(y), y, seed)
    lanes = fit_lanes(P[tr], y[tr], P[te], y[te], seed, secondary=secondary)
    row = {"target": name, "seed": seed, "n": int(len(y)),
           "base_rate": round(float(y.mean()), 4), "d": int(P.shape[1]),
           **{k: (round(v, 4) if isinstance(v, float) else v)
              for k, v in lanes.items()}}
    row["gates"] = gates(lanes, g1_off_grid(P[tr], y[tr]), P.shape[1])
    print(f"  {name:10s} s{seed} gam {lanes['gam']:.4f} ga2m "
          f"{lanes['ga2m']:.4f} hgb {lanes['hgb']:.4f} joint "
          f"{lanes.get('joint', float('nan')):.4f} {lanes['lane_seconds']}",
          flush=True)
    return row


def freq_recovery(terms: list[dict]) -> dict:
    """The first joint term against the planted (3.7, 5.1, 6.8), up to a
    global sign, on the subset (0, 1, 2)."""
    t = terms[0]
    f = np.asarray(t["freqs"])
    if f[0] < 0:
        f = -f
    err = np.abs(f - np.asarray(SPARSE_F))
    return {"first_term_subset": t["subset"], "recovered": f.round(3).tolist(),
            "planted": list(SPARSE_F), "paper_recovered": list(PAPER_FREQS),
            "max_abs_error": round(float(err.max()), 3),
            "within_tolerance": bool(t["subset"] == [0, 1, 2]
                                     and err.max() <= FREQ_TOL)}


def _mean_sd(rows, key):
    v = np.array([key(r) for r in rows], dtype=float)
    return {"mean": round(float(v.mean()), 4),
            "sd": round(float(v.std(ddof=1)), 4) if len(v) > 1 else None}


def check(rows: dict) -> dict:
    """Each known answer against its tolerance, on the seed means."""
    vals = {
        "real_g2_gam_auc": _mean_sd(rows["real"], lambda r: r["gam"]),
        "sparse_joint_minus_ga2m": _mean_sd(
            rows["sparse"], lambda r: r["joint"] - r["ga2m"]),
        "dense_hgb_minus_gam": _mean_sd(
            rows["dense"], lambda r: r["hgb"] - r["gam"]),
        "dense_joint_minus_ga2m": _mean_sd(
            rows["dense"], lambda r: r["joint"] - r["ga2m"])}
    out = {}
    for k, (target, tol) in KNOWN.items():
        m = vals[k]["mean"]
        out[k] = {**vals[k], "published": target, "tolerance": tol,
                  # Inclusive, with a float allowance: 0.97 - 0.94 is
                  # 0.030000000000000027 in binary floating point.
                  "within": bool(abs(m - target) <= tol + 1e-9)}
    out["task_g_runs"] = out["real_g2_gam_auc"]["within"]
    return out


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    mode = argv[0] if argv else "run"
    seeds = SEEDS[:1] if mode == "pilot" else SEEDS
    d = load_raw()
    P_real, names = real_phases(d)
    y_real = d["target_real"].to_numpy().astype(int)
    t0 = time.perf_counter()
    doc = {"generator": "experiments/phase2/src/f103_tier1.py", "card": "F103",
           "sprint": 27, "phase": 2, "evidence_tag": "SIM",
           "metered_seconds": 0, "date": time.strftime("%Y-%m-%d"),
           "mode": mode, "seeds": list(seeds),
           "entry": "experiments/phase2/PREREGISTRATION_DRAFT.md section 6, "
                    "F103",
           "release_phase_jitter": release_jitter(d), "real_phases": names}
    perm = np.random.default_rng(42).permutation(y_real)
    doc["permuted_reference"] = run_target("permuted", P_real, perm, 42)
    rows = {"real": [], "sparse": [], "dense": []}
    for s in seeds:
        rows["real"].append(run_target("real", P_real, y_real, s,
                                       secondary=True))
        P, y = sparse_pocket(d, s)
        r = run_target("sparse", P, y, s)
        r["frequency_recovery"] = freq_recovery(r["joint_terms"])
        rows["sparse"].append(r)
        P, y = dense_substrate(d, s)
        rows["dense"].append(run_target("dense", P, y, s))
    doc.update(rows)
    doc["frequency_recovery_all_seeds"] = all(
        r["frequency_recovery"]["within_tolerance"] for r in rows["sparse"])
    doc["check"] = check(rows)
    if not doc["frequency_recovery_all_seeds"]:
        doc["check"]["note"] = ("JOINT did not recover the planted "
                                "frequencies on every seed; per the entry "
                                "no JOINT value is reported as a check")
        for k in ("sparse_joint_minus_ga2m", "dense_joint_minus_ga2m"):
            doc["check"][k]["within"] = None
    doc["elapsed_s"] = round(time.perf_counter() - t0, 1)
    out = OUT.with_name("f103_tier1_pilot.json") if mode == "pilot" else OUT
    out.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(doc["check"], indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
