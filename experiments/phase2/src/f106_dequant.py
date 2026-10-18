"""F106 (Sprint 27 Task I): dequantization check of a sandwich-encoded
circuit on ULB.

The entry is `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6,
"F106", written before this module existed; every choice is fixed there
and repeated here. The design is `docs/phase2/F6_GATE_BASED_ARM.md`
section 5.

Circuit: 8 qubits, exact NumPy statevector, three layers of
    RY(phi_q / 2) on every qubit
    exp(-i lambda_l sum_q Z_q Z_{q+1})   (ring)
    RY(phi_q / 2) on every qubit
    trainable RY, RZ on every qubit
read out as logit b + sum_q w_q <Z_q>, trained by binary cross-entropy
with Adam; gradients by the adjoint method (exact, one backward sweep).

Twins on the same 8 phases and the same training rows: logistic
regression on cos/sin, F103's trained-frequency GAM and GA2M, HGB,
F103's k-way JOINT, and an RFF surrogate.

Primary (m = 6, Bonferroni): for each twin, the paired stratified
bootstrap interval on the across-seed mean of (twin - circuit) test
AUPRC. Dequantized if any lower bound exceeds -MARGIN.

    <venv python> experiments/phase2/src/f106_dequant.py pilot
    <venv python> experiments/phase2/src/f106_dequant.py run

Zero metered seconds; no Braket service is called. Writes
`experiments/phase2/results/f106_dequant.json` (the pilot writes
`f106_dequant_pilot.json`).
"""
from __future__ import annotations

import itertools
import json
import sys
import time
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "experiments" / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import f103_tier1 as t1                              # noqa: E402  (Phase 2)

OUT = ROOT / "experiments" / "phase2" / "results" / "f106_dequant.json"
OUT_PILOT = OUT.with_name("f106_dequant_pilot.json")
SEEDS = tuple(range(42, 50))
N_QUBITS, N_LAYERS = 8, 3
N_NEG_TRAIN = 6000
STEPS, BATCH, LR = 1500, 512, 0.05
LAMBDA_START, INIT_HALF = 0.5, 0.1
RFF_GAMMAS, RFF_COMPONENTS = (0.05, 0.2, 0.8), 1000
TWINS = ("lr", "gam", "ga2m", "hgb", "joint", "rff")
ALPHA = 0.05 / len(TWINS)
MARGIN = 0.005
N_BOOT, BOOT_CHUNK = 2000, 200
C_FLOOR = 0.01
DIAG_ROWS, DIAG_STEP = 100, 1e-4
PILOT_LIMIT_S = 3 * 3600

DIM = 2 ** N_QUBITS
_BITS = (np.arange(DIM)[:, None] >> (N_QUBITS - 1 - np.arange(N_QUBITS))) & 1
Z = (1 - 2 * _BITS).T.astype(np.float64)          # Z[q, i]: eigenvalue of Z_q
RING = Z * np.roll(Z, -1, axis=0)
ZZ_DIAG = RING.sum(axis=0)                         # sum_q Z_q Z_{q+1}
Y = np.array([[0, -1j], [1j, 0]])
ZM = np.array([[1, 0], [0, -1]], dtype=complex)


# ------------------------------------------------------------------ phases

def ecdf_phase(v_tr: np.ndarray, v: np.ndarray) -> np.ndarray:
    """2 pi F(v) - pi, F the training rows' mid-rank empirical CDF. On a
    training row this is the paper's rank phase; other rows fall on the
    same step function."""
    s = np.sort(v_tr)
    mid = (np.searchsorted(s, v, "left") + np.searchsorted(s, v, "right")) / 2
    return 2 * np.pi * mid / len(s) - np.pi


class Phases:
    """Rank phase, PCA-whiten, rank phase again; fit on training rows."""

    def __init__(self, Xtr: np.ndarray):
        self.Xtr = Xtr
        P = self._first(Xtr)
        self.mu = P.mean(axis=0)
        vals, vecs = np.linalg.eigh(np.cov(P - self.mu, rowvar=False))
        self.W = vecs / np.sqrt(np.maximum(vals, 1e-12))
        self.Ztr = (P - self.mu) @ self.W

    def _first(self, X):
        return np.column_stack([ecdf_phase(self.Xtr[:, j], X[:, j])
                                for j in range(X.shape[1])])

    def __call__(self, X: np.ndarray) -> np.ndarray:
        Zx = (self._first(X) - self.mu) @ self.W
        return np.column_stack([ecdf_phase(self.Ztr[:, j], Zx[:, j])
                                for j in range(Zx.shape[1])])


# ----------------------------------------------------------------- circuit

def _ry(a):
    """RY(a) for an array of angles: shape (..., 2, 2)."""
    c, s = np.cos(a / 2), np.sin(a / 2)
    return np.stack([np.stack([c, -s], -1), np.stack([s, c], -1)], -2)


def _rz(a):
    e = np.exp(-0.5j * a)
    return np.array([[e, 0], [0, np.conj(e)]])


def apply_1q(psi: np.ndarray, M: np.ndarray, q: int) -> np.ndarray:
    """Apply a 2x2 gate on qubit q; M is (2, 2) or per row (n, 2, 2)."""
    n = psi.shape[0]
    v = psi.reshape(n, 2 ** q, 2, 2 ** (N_QUBITS - 1 - q))
    spec = "nab,nibj->niaj" if M.ndim == 3 else "ab,nibj->niaj"
    return np.einsum(spec, M, v).reshape(n, DIM)


class Params:
    """Flat parameter vector: lambdas (L), rotations (L, Q, 2), w (Q), b."""

    def __init__(self, base_rate: float, seed: int):
        rng = np.random.default_rng(seed)
        L, Q = N_LAYERS, N_QUBITS
        self.lam = np.full(L, LAMBDA_START)
        self.rot = rng.uniform(-INIT_HALF, INIT_HALF, (L, Q, 2))
        self.w = rng.uniform(-INIT_HALF, INIT_HALF, Q)
        self.b = float(np.log(base_rate / (1 - base_rate)))

    def flat(self) -> np.ndarray:
        return np.concatenate([self.lam, self.rot.ravel(), self.w, [self.b]])

    def set_flat(self, x: np.ndarray) -> None:
        L, Q = N_LAYERS, N_QUBITS
        self.lam = x[:L].copy()
        self.rot = x[L:L + 2 * L * Q].reshape(L, Q, 2).copy()
        self.w = x[L + 2 * L * Q:L + 2 * L * Q + Q].copy()
        self.b = float(x[-1])


def ops(params: Params, Phi: np.ndarray, encoding_only: bool = False) -> list:
    """The gate sequence as (kind, qubit, matrix-or-diag, generator id).
    encoding_only: the first layer's sandwich alone, no trainable
    rotations (the IBR diagnostics are taken on the encoded state)."""
    data = _ry(Phi / 2)                            # (n, Q, 2, 2)
    seq = []
    for l in range(1 if encoding_only else N_LAYERS):
        for q in range(N_QUBITS):
            seq.append(("1q", q, data[:, q], None))
        seq.append(("zz", None, np.exp(-1j * params.lam[l] * ZZ_DIAG),
                    ("lam", l)))
        for q in range(N_QUBITS):
            seq.append(("1q", q, data[:, q], None))
        if not encoding_only:
            for q in range(N_QUBITS):
                seq.append(("1q", q, _ry(params.rot[l, q, 0]),
                            ("ry", l, q)))
                seq.append(("1q", q, _rz(params.rot[l, q, 1]),
                            ("rz", l, q)))
    return seq


def _apply(psi, op, adjoint=False):
    kind, q, M, _ = op
    if kind == "zz":
        return psi * (np.conj(M) if adjoint else M)[None, :]
    if adjoint:
        M = np.conj(np.swapaxes(M, -1, -2))
    return apply_1q(psi, M, q)


def _start(n: int) -> np.ndarray:
    psi = np.zeros((n, DIM), dtype=complex)
    psi[:, 0] = 1.0
    return psi


def state(params: Params, Phi: np.ndarray, encoding_only: bool = False):
    psi = _start(len(Phi))
    for op in ops(params, Phi, encoding_only):
        psi = _apply(psi, op)
    return psi


def expectations(psi: np.ndarray) -> np.ndarray:
    """<Z_q> per row: (n, Q)."""
    return (np.abs(psi) ** 2) @ Z.T


def logits(params: Params, Phi: np.ndarray) -> np.ndarray:
    return params.b + expectations(state(params, Phi)) @ params.w


def loss_and_grad(params: Params, Phi: np.ndarray, y: np.ndarray):
    """Mean binary cross-entropy and its exact gradient (adjoint method)."""
    seq = ops(params, Phi)
    psi = _start(len(Phi))
    for op in seq:
        psi = _apply(psi, op)
    m = expectations(psi)
    s = params.b + m @ params.w
    p = 1 / (1 + np.exp(-s))
    eps = 1e-12
    loss = float(-np.mean(y * np.log(p + eps) + (1 - y) * np.log(1 - p + eps)))
    gs = (p - y) / len(y)                          # dL/ds per row
    g = Params.__new__(Params)
    g.lam = np.zeros(N_LAYERS)
    g.rot = np.zeros((N_LAYERS, N_QUBITS, 2))
    g.w = gs @ m
    g.b = float(gs.sum())
    lam = gs[:, None] * (params.w @ Z)[None, :] * psi
    phi = psi
    for op in reversed(seq):
        kind, q, _, gen = op
        if gen is not None:
            if kind == "zz":
                Gphi, c = ZZ_DIAG[None, :] * phi, 1.0
            else:
                Gphi, c = apply_1q(phi, Y if gen[0] == "ry" else ZM, q), 0.5
            d = 2 * c * float(np.imag(np.vdot(lam, Gphi)))
            if gen[0] == "lam":
                g.lam[gen[1]] = d
            else:
                g.rot[gen[1], gen[2], 0 if gen[0] == "ry" else 1] = d
        phi = _apply(phi, op, adjoint=True)
        lam = _apply(lam, op, adjoint=True)
    return loss, g.flat()


def train_circuit(Phi: np.ndarray, y: np.ndarray, seed: int,
                  steps: int = STEPS) -> tuple[Params, list]:
    params = Params(float(y.mean()), seed)
    rng = np.random.default_rng(seed)
    x = params.flat()
    m1, m2 = np.zeros_like(x), np.zeros_like(x)
    b1, b2 = 0.9, 0.999
    trace = []
    for t in range(1, steps + 1):
        idx = rng.choice(len(y), size=min(BATCH, len(y)), replace=False)
        params.set_flat(x)
        loss, g = loss_and_grad(params, Phi[idx], y[idx])
        m1 = b1 * m1 + (1 - b1) * g
        m2 = b2 * m2 + (1 - b2) * g * g
        x = x - LR * (m1 / (1 - b1 ** t)) / (np.sqrt(m2 / (1 - b2 ** t)) + 1e-8)
        if t % 100 == 0:
            trace.append([t, round(loss, 5)])
    params.set_flat(x)
    return params, trace


def predict(params: Params, Phi: np.ndarray, chunk: int = 8192) -> np.ndarray:
    s = np.concatenate([logits(params, Phi[i:i + chunk])
                        for i in range(0, len(Phi), chunk)])
    return 1 / (1 + np.exp(-s))


# ------------------------------------------------------------- diagnostics

def diagnostics(params: Params, Phi: np.ndarray) -> dict:
    """IBR section 6.4 on the first encoding layer alone, at lambda_1."""
    psi = state(params, Phi, encoding_only=True)
    norm = (np.abs(psi) ** 2).sum(1)
    C = float(np.mean((np.imag(psi) ** 2).sum(1) / norm))
    A = []
    for mu in range(Phi.shape[1]):
        e = np.zeros(Phi.shape[1])
        e[mu] = DIAG_STEP
        dpsi = (state(params, Phi + e, True) - state(params, Phi - e, True)) \
            / (2 * DIAG_STEP)
        A.append(np.abs(np.einsum("ni,ni->n", np.conj(psi), dpsi)))
    S = 0.0
    for q in range(N_QUBITS):
        v = psi.reshape(len(psi), 2 ** q, 2, 2 ** (N_QUBITS - 1 - q))
        rho = np.einsum("niaj,nibj->nab", v, np.conj(v))
        ev = np.clip(np.linalg.eigvalsh(rho), 1e-15, 1)
        S += float(np.mean(-(ev * np.log2(ev)).sum(1)))
    return {"C": round(C, 4), "berry_abs": round(float(np.mean(A)), 4),
            "sum_single_qubit_entropy_bits": round(S, 4)}


# ------------------------------------------------------------------- twins

def _cs(P):
    return np.column_stack([np.cos(P), np.sin(P)])


def _joint(Ptr, ytr, Pte, Gtr, Gte, p_tr):
    """F103's greedy JOINT loop, returning test probabilities."""
    Jtr, Jte = Gtr, Gte
    subsets = list(itertools.combinations(range(Ptr.shape[1]), t1.JOINT_ORDER))
    for _ in range(t1.JOINT_TERMS):
        r = ytr - p_tr
        (pw, f), S = max(((t1.joint_scan(Ptr, r, S), S) for S in subsets),
                         key=lambda x: x[0][0])
        u_tr, u_te = Ptr[:, S] @ f, Pte[:, S] @ f
        Jtr = np.column_stack([Jtr, np.cos(u_tr), np.sin(u_tr)])
        Jte = np.column_stack([Jte, np.cos(u_te), np.sin(u_te)])
        m = t1._lr(Jtr, ytr)
        p_tr = m.predict_proba(Jtr)[:, 1]
    return m.predict_proba(Jte)[:, 1]


def twin_scores(Ptr, ytr, Pva, yva, Pte, seed: int) -> tuple[dict, dict]:
    from sklearn.ensemble import HistGradientBoostingClassifier
    from sklearn.kernel_approximation import RBFSampler
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import average_precision_score
    from sklearn.pipeline import make_pipeline
    out, sec = {}, {}
    t0 = time.perf_counter()
    out["lr"] = t1._lr(_cs(Ptr), ytr).predict_proba(_cs(Pte))[:, 1]
    freqs = [t1.trained_frequency(Ptr[:, j], ytr) for j in range(Ptr.shape[1])]
    sec["trained_frequencies"] = [round(f, 3) for f in freqs]
    out["gam"] = t1._lr(t1.gam_basis(Ptr, freqs), ytr).predict_proba(
        t1.gam_basis(Pte, freqs))[:, 1]
    Gtr, Gte = t1.ga2m_basis(Ptr, freqs), t1.ga2m_basis(Pte, freqs)
    ga2m = t1._lr(Gtr, ytr)
    out["ga2m"] = ga2m.predict_proba(Gte)[:, 1]
    out["hgb"] = HistGradientBoostingClassifier(random_state=seed).fit(
        Ptr, ytr).predict_proba(Pte)[:, 1]
    sec["seconds_lr_gam_ga2m_hgb"] = round(time.perf_counter() - t0, 1)
    t0 = time.perf_counter()
    out["joint"] = _joint(Ptr, ytr, Pte, Gtr, Gte, ga2m.predict_proba(Gtr)[:, 1])
    sec["seconds_joint"] = round(time.perf_counter() - t0, 1)
    t0 = time.perf_counter()

    def rff(gamma):
        return make_pipeline(
            RBFSampler(gamma=gamma, n_components=RFF_COMPONENTS,
                       random_state=seed),
            LogisticRegression(C=1.0, max_iter=2000)).fit(_cs(Ptr), ytr)
    val = {g: float(average_precision_score(
        yva, rff(g).predict_proba(_cs(Pva))[:, 1])) for g in RFF_GAMMAS}
    best = max(val, key=val.get)
    out["rff"] = rff(best).predict_proba(_cs(Pte))[:, 1]
    sec["rff_val_auprc"] = {str(g): round(v, 4) for g, v in val.items()}
    sec["rff_gamma"] = best
    sec["seconds_rff"] = round(time.perf_counter() - t0, 1)
    return out, sec


# -------------------------------------------------------------------- runs

def seed_run(df, seed: int, steps: int = STEPS) -> tuple[dict, np.ndarray, dict]:
    import data
    from sklearn.metrics import average_precision_score, roc_auc_score
    sp = data.stratified_split(df, seed)
    feats = data.top_k_features(sp.X_train, sp.y_train, N_QUBITS, seed)
    ytr_all = sp.y_train.to_numpy().astype(int)
    rng = np.random.default_rng(seed)
    pos = np.flatnonzero(ytr_all == 1)
    neg = rng.choice(np.flatnonzero(ytr_all == 0), N_NEG_TRAIN, replace=False)
    rows = np.sort(np.concatenate([pos, neg]))
    Xtr = sp.X_train[feats].to_numpy(dtype=np.float64)[rows]
    ytr = ytr_all[rows]
    ph = Phases(Xtr)
    Ptr = ph(Xtr)
    Pva = ph(sp.X_val[feats].to_numpy(dtype=np.float64))
    Pte = ph(sp.X_test[feats].to_numpy(dtype=np.float64))
    yva = sp.y_val.to_numpy().astype(int)
    yte = sp.y_test.to_numpy().astype(int)

    t0 = time.perf_counter()
    params, trace = train_circuit(Ptr, ytr, seed, steps)
    train_s = time.perf_counter() - t0
    t0 = time.perf_counter()
    scores = {"circuit": predict(params, Pte)}
    predict_s = time.perf_counter() - t0
    twins, sec = twin_scores(Ptr, ytr, Pva, yva, Pte, seed)
    scores.update(twins)
    base = float(yte.mean())
    lanes = {k: {"auprc": float(average_precision_score(yte, p)),
                 "auroc": float(roc_auc_score(yte, p)),
                 "norm_auprc": float((average_precision_score(yte, p) - base)
                                     / (1 - base))}
             for k, p in scores.items()}
    diag_rows = np.random.default_rng(seed).choice(len(Ptr), DIAG_ROWS,
                                                    replace=False)
    row = {"seed": seed, "features": feats, "n_train": int(len(rows)),
           "n_train_pos": int(ytr.sum()), "n_test": int(len(yte)),
           "n_test_pos": int(yte.sum()), "lanes": lanes,
           "lambdas": [round(float(v), 4) for v in params.lam],
           "loss_trace": trace,
           "diagnostics": diagnostics(params, Ptr[diag_rows]),
           "seconds": {"circuit_train": round(train_s, 1),
                       "circuit_predict": round(predict_s, 1),
                       **{k: v for k, v in sec.items()
                          if k.startswith("seconds")}},
           "twin_detail": {k: v for k, v in sec.items()
                           if not k.startswith("seconds")}}
    print(f"  s{seed} " + " ".join(f"{k} {v['auprc']:.4f}"
                                   for k, v in lanes.items())
          + f" C {row['diagnostics']['C']} {row['seconds']}", flush=True)
    return row, yte, scores


def compare(seeds, ys, scores) -> dict:
    """Primary: paired stratified bootstrap of mean (twin - circuit)."""
    from sklearn.metrics import average_precision_score
    import metrics
    boot = {t: np.zeros((len(seeds), N_BOOT)) for t in TWINS}
    for i, s in enumerate(seeds):
        y = ys[s]
        rng = np.random.default_rng(1000 + s)
        j = 0
        while j < N_BOOT:
            idx = metrics.stratified_indices(y, rng, min(BOOT_CHUNK, N_BOOT - j))
            for b in idx:
                c = average_precision_score(y[b], scores[s]["circuit"][b])
                for t in TWINS:
                    boot[t][i, j] = average_precision_score(
                        y[b], scores[s][t][b]) - c
                j += 1
    out = {}
    for t in TWINS:
        d = np.array([average_precision_score(ys[s], scores[s][t])
                      - average_precision_score(ys[s], scores[s]["circuit"])
                      for s in seeds])
        lo, hi = np.percentile(boot[t].mean(axis=0),
                               [100 * ALPHA / 2, 100 * (1 - ALPHA / 2)])
        w = (stats.wilcoxon(d, alternative="two-sided", method="exact").pvalue
             if len(seeds) >= 2 and np.any(d != 0) else float("nan"))
        out[t] = {"mean_delta_auprc": float(d.mean()),
                  "interval": [float(lo), float(hi)],
                  "wilcoxon_p_exact": float(w),
                  "seeds_twin_ahead": int((d > 0).sum()),
                  "per_seed_delta": [round(float(x), 5) for x in d],
                  "no_worse_within_margin": bool(lo > -MARGIN),
                  "circuit_ahead": bool(hi < 0)}
    return out


def outcome(cmp: dict) -> str:
    if any(c["no_worse_within_margin"] for c in cmp.values()):
        return "dequantized"
    if all(c["circuit_ahead"] for c in cmp.values()):
        return "circuit ahead"
    return "inconclusive"


def main(argv=None) -> int:
    import data
    argv = sys.argv[1:] if argv is None else argv
    mode = argv[0] if argv else "pilot"
    if mode not in ("pilot", "run"):
        raise SystemExit("usage: f106_dequant.py pilot|run")
    seeds = SEEDS[:1] if mode == "pilot" else SEEDS
    t_all = time.perf_counter()
    df = data.load_ulb()
    rows, ys, scores = [], {}, {}
    for s in seeds:
        row, ys[s], scores[s] = seed_run(df, s)
        rows.append(row)
    cmp = compare(seeds, ys, scores)
    res = {"generator": "experiments/phase2/src/f106_dequant.py",
           "card": "F106", "sprint": 27, "phase": 2, "evidence_tag": "SIM",
           "metered_seconds": 0, "date": time.strftime("%Y-%m-%d"),
           "entry": "experiments/phase2/PREREGISTRATION_DRAFT.md section 6, "
                    "F106",
           "mode": mode, "seeds": list(seeds), "alpha_each": ALPHA,
           "margin": MARGIN, "n_boot": N_BOOT, "steps": STEPS,
           "rows": rows, "compare": cmp, "outcome": outcome(cmp),
           "encoding_built_wrong": bool(np.mean(
               [r["diagnostics"]["C"] for r in rows]) < C_FLOOR)}
    res["elapsed_s"] = round(time.perf_counter() - t_all, 1)
    if mode == "pilot":
        res["projected_run_s"] = round(res["elapsed_s"] * len(SEEDS), 1)
        res["run_within_limit"] = bool(res["projected_run_s"] <= PILOT_LIMIT_S)
    (OUT_PILOT if mode == "pilot" else OUT).write_text(
        json.dumps(res, indent=1) + "\n", encoding="utf-8")
    for t, c in cmp.items():
        print(f"  {t:6s} {c['mean_delta_auprc']:+.4f} "
              f"[{c['interval'][0]:+.4f}, {c['interval'][1]:+.4f}]")
    print("outcome:", res["outcome"], "| built wrong:",
          res["encoding_built_wrong"], "| elapsed", res["elapsed_s"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
