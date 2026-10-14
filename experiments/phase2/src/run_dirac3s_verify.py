"""F142 (Sprint 26 Task D): the first Dirac-3S fits, in three approval stops.

Entry: `experiments/phase2/PREREGISTRATION_DRAFT.md` section 6, "F142",
written before any call. Every stop needs the team lead's own approval with
its call count and seconds (Criterion H); plan approval approved none.

    stop 1: B1 (91 variables, ULB) seed 42                1 call, cap  60 s
    stop 2: B1 seed 43; B2 (833 variables, ULB) seed 42   2 calls, cap 150 s
    stop 3: B4 oilgas_gasturbine seeds 42 and 43           2 calls, cap 150 s

    python experiments/phase2/src/run_dirac3s_verify.py --stop 1 --dry-run
    python experiments/phase2/src/run_dirac3s_verify.py --stop 1   # metered

B1 and B2 run under the draft's section 4 exception: their purpose is cost
and queue time, and their failed resolution screen is reported beside them.
B4 is the fidelity twin: each B4 job must pass A31's resolution test, or it
is not submitted (`resolution_screen`). The test is A31's, not the
library's `get_dynamic_range`: that ratio passes B1 at 4.8 dB, although A31
shows no coefficient difference in B1 is resolvable. Both are recorded.

THE SCREEN READS THE HAMILTONIAN THAT IS SENT. Every pool here is built with
F145's seeded weak learners, so the offline build that is screened and the
metered build are byte-identical. The runner checks that: it
hashes J and C from both builds and refuses to submit a B4 unit whose
metered-run Hamiltonian differs from the one it screened. (Unseeded, the
two builds drift, and the screen would be of a different matrix.)

PHASE 1 FILES ARE NEVER WRITTEN (CLAUDE.md, the Phase 1 boundary, rule 3).
`metered_call` writes its ledger and call logs under `experiments/results/`;
this runner points both at `experiments/phase2/results/` for the duration of
the run (`_phase2_ledger`). Rows, responses and the ledger all live there.

The full-pair B1 and B2 builds need fork, so run this under WSL.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from contextlib import contextmanager
from pathlib import Path

import numpy as np

SRC = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC))
import eqc_submit  # noqa: E402
import metered_call as mc  # noqa: E402
import metrics  # noqa: E402
import qubo_proxy as qp  # noqa: E402

PHASE2_RESULTS = Path(__file__).resolve().parents[1] / "results"
RESULT = PHASE2_RESULTS / "f142_dirac3s_verify.json"
LEDGER = PHASE2_RESULTS / "qpu_cost_ledger_phase2.json"
LOG_DIR = PHASE2_RESULTS / "call_logs"
RESP_DIR = PHASE2_RESULTS / "device_samples"
DEVICE = eqc_submit.DIRAC_3S
ARM = "cvqboost_dirac3s"

# B1 and B2 are qubo_proxy's `free` and `full` configs, as run_hardware.py
# ran them on Dirac-3 (hw_b1_dct, hw_b2_full).
UNITS = [
    {"unit": "b1_42", "stop": 1, "kind": "ulb", "config": "free", "seed": 42,
     "screen": "report"},
    {"unit": "b1_43", "stop": 2, "kind": "ulb", "config": "free", "seed": 43,
     "screen": "report"},
    {"unit": "b2_42", "stop": 2, "kind": "ulb", "config": "full", "seed": 42,
     "screen": "report"},
    {"unit": "b4_oilgas_42", "stop": 3, "kind": "spectra",
     "cell": "oilgas_gasturbine", "seed": 42, "screen": "enforce"},
    {"unit": "b4_oilgas_43", "stop": 3, "kind": "spectra",
     "cell": "oilgas_gasturbine", "seed": 43, "screen": "enforce"},
]
STOP_CAP_S = {1: 60.0, 2: 150.0, 3: 150.0}
EXPECTED = {1: "about 5 s (B1 cost 4-5 s per fit on Dirac-3)",
            2: "re-quoted from stop 1's measured cost",
            3: "re-quoted from stops 1 and 2"}


@contextmanager
def _phase2_ledger():
    """Point metered_call's ledger and call logs at Phase 2 paths."""
    saved = (mc.LEDGER, mc.LOG_DIR)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    mc.LEDGER, mc.LOG_DIR = LEDGER, LOG_DIR
    try:
        yield
    finally:
        mc.LEDGER, mc.LOG_DIR = saved


def _rows() -> list[dict]:
    if not RESULT.exists():
        return []
    try:
        return json.loads(RESULT.read_text(encoding="utf-8"))["rows"]
    except Exception as exc:                              # noqa: BLE001
        raise SystemExit(
            f"REFUSING: {RESULT.name} is unreadable ({exc}). A runner that "
            "cannot read its own record cannot know what it has paid for.")


def _done() -> set[str]:
    """Units already submitted and not failed: never submitted again."""
    return {r["unit"] for r in _rows() if r.get("status") != "failed"}


def _data(u: dict):
    """(X_tr, X_va, X_te, y_pm1, y_va01, y_te01, cfg, extras)."""
    if u["kind"] == "ulb":
        c = qp.CONFIGS[u["config"]]
        split, cols, Xtr, Xva, Xte, y_pm1 = qp._prep(u["seed"], c["k"])
        cfg = dict(lambda_coef=qp.LAMBDA_MULT * len(y_pm1),
                   weak_cls_schedule=c["schedule"], weak_cls_type="dct",
                   weak_cls_params=qp.seeded_weak_params(u["seed"]),
                   weak_cls_strategy="multi_processing", **qp.FIXED)
        return (Xtr, Xva, Xte, y_pm1, split.y_val.to_numpy(),
                split.y_test.to_numpy(), cfg, {"features": cols})
    import spectra_segment as ss
    cell = ss.frozen_cell_by_name(u["cell"])
    split, cols = ss._prep_spectra(u["cell"], u["seed"])

    def X(df):
        return ss.coerce_features_to_numeric(df[cols]).to_numpy(
            dtype="float32")

    y_pm1 = np.where(split.y_train.to_numpy() == 1, 1, -1)
    c = cell["config"]
    cfg = dict(lambda_coef=c["lambda_coef_alpha"] * len(y_pm1),
               weak_cls_schedule=c["weak_cls_schedule"], weak_cls_type="dct",
               weak_cls_params={**c["weak_cls_params"],
                                **qp.seeded_weak_params(u["seed"])},
               weak_cls_strategy=c["weak_cls_strategy"],
               relaxation_schedule=c["relaxation_schedule"],
               num_samples=c["num_samples"])
    pocket = split.X_test[ss.SEGMENT_FLAG].to_numpy().astype(bool)
    return (X(split.X_train), X(split.X_val), X(split.X_test), y_pm1,
            split.y_val.to_numpy(), split.y_test.to_numpy(), cfg,
            {"features": cols, "in_pocket_test": pocket})


def _hash(clf) -> str:
    h = hashlib.sha256()
    for a in (clf._J, clf._C):
        h.update(np.ascontiguousarray(np.asarray(a, dtype=np.float64)).tobytes())
    return h.hexdigest()


def _make_clf(cfg, api):
    from eqc_models.ml.classifierqboost import QBoostClassifier
    clf = QBoostClassifier(**api, **cfg)
    for k, v in cfg.items():
        assert getattr(clf, k) == v, f"constructed attr mismatch: {k}"
    return clf


def resolution_screen(J, C) -> dict:
    """A31's test, not the library's dynamic range.

    `get_dynamic_range` is 10 log10(max |coefficient| / min |coefficient|).
    On a CVQBoost Hamiltonian the off-diagonals are large and nearly equal,
    so that ratio stays small (B1: 4.8 dB) while their DIFFERENCES fall
    below what the device resolves -- the failure A31 found on B1's pools.
    The screen asks A31's question: do the off-diagonal and linear spreads
    reach max |coefficient| / 200 (`device_resolution._coefficient_spread`)?
    """
    import device_resolution as dres
    s = dres._coefficient_spread(np.asarray(J, dtype=np.float64),
                                 np.asarray(C, dtype=np.float64).reshape(-1))
    return {"off_diagonal_spread_over_resolvable":
                s["off_diagonal_spread_over_resolvable"],
            "linear_spread_over_resolvable":
                s["linear_spread_over_resolvable"],
            "pass": bool(s["off_diagonal_resolvable"]
                         and s["linear_resolvable"])}


def offline(u: dict) -> dict:
    """The dry run of one unit: every line but the network, on Dirac-3S."""
    Xtr, _, _, y_pm1, _, _, cfg, _ = _data(u)
    sent: list = []
    with eqc_submit.offline_solver(sent, device_type=DEVICE):
        clf = _make_clf(cfg, {})
        clf.fit(Xtr, y_pm1)
    s = sent[0]
    scr = resolution_screen(clf._J, clf._C)
    return {"unit": u["unit"], "n_variables": s["n_variables"],
            "device_type": s["device_type"], "num_samples": s["num_samples"],
            "dynamic_range_db": s["dynamic_range_db"],
            "off_diagonal_spread_over_resolvable":
                scr["off_diagonal_spread_over_resolvable"],
            "linear_spread_over_resolvable":
                scr["linear_spread_over_resolvable"],
            "screen_pass": scr["pass"],
            "hamiltonian_sha256": _hash(clf)}


def metered(u: dict, screened: dict, client) -> dict:
    """One metered Dirac-3S fit. Caller has checked the screen."""
    Xtr, Xva, Xte, y_pm1, y_va01, y_te01, cfg, extra = _data(u)
    api = dict(api_url=os.environ.get("QCI_API_URL"),
               api_token=os.environ.get("QCI_TOKEN"))
    built: dict = {}

    def make_clf():
        clf = _make_clf(cfg, api)
        built["clf"] = clf
        return clf

    def make_record(attempt):
        return mc.CallRecord(label=f"f142_{u['unit']}_a{attempt + 1}",
                             degree=2, n_variables=screened["n_variables"],
                             n_samples=cfg["num_samples"],
                             expected_seconds=EXPECTED[u["stop"]])

    t_submit = time.strftime("%Y-%m-%dT%H:%M:%S")
    t0 = time.perf_counter()
    with _phase2_ledger(), eqc_submit.device(DEVICE):
        fit = eqc_submit.metered_fit(make_clf, Xtr, y_pm1, make_record,
                                     client)
    wall = round(time.perf_counter() - t0, 1)

    row = {"arm": ARM, "card": "F142", "unit": u["unit"], "stop": u["stop"],
           "seed": u["seed"], "device_type": DEVICE,
           "evidence_tag": "HW", "job_id": fit["job_id"],
           "metered_seconds": fit["metered_seconds"],
           "metered_seconds_parsed": fit["parsed"],
           "retry_count": max(0, fit["attempts"] - 1),
           "wall_seconds_including_queue": wall,
           "submitted": t_submit,
           "finished": time.strftime("%Y-%m-%dT%H:%M:%S"),
           "hw_config": {k: (dict(v) if isinstance(v, dict) else v)
                         for k, v in cfg.items()},
           "screen": {**{k: screened[k] for k in (
               "off_diagonal_spread_over_resolvable",
               "linear_spread_over_resolvable", "screen_pass",
               "dynamic_range_db", "n_variables")},
                      "test": "A31: spreads >= max |coefficient| / 200",
                      "rule": u["screen"]},
           "features_used": list(extra["features"])}
    if fit["clf"] is None:
        row.update({"status": "failed", "error": fit["error"]})
        return row

    clf, resp = fit["clf"], fit["resp"]
    RESP_DIR.mkdir(parents=True, exist_ok=True)
    resp_file = RESP_DIR / f"f142_{u['unit']}.json"
    resp_file.write_text(json.dumps(
        {"job_id": fit["job_id"], "device_type": DEVICE, "card": "F142",
         "unit": u["unit"], "response": eqc_submit.to_jsonable(resp)},
        indent=1), encoding="utf-8")

    w_hw = np.asarray(clf.params, dtype=np.float64)
    H_tr = qp.h_matrix(clf, Xtr)
    w_px = qp.solve_simplex_qp(H_tr, y_pm1, cfg["lambda_coef"])
    J, C = qp.hamiltonian(H_tr.astype(np.float64), y_pm1, cfg["lambda_coef"])
    denom = float(np.linalg.norm(w_hw) * np.linalg.norm(w_px))

    def obj(w):
        return float(w @ J @ w + C @ w)

    def score(Xm):
        return np.clip((clf.predict_raw(Xm) + 1.0) / 2.0, 0.0, 1.0)

    p_val, p_test = score(Xva), score(Xte)
    m = metrics.summarize(y_te01, y_va01, p_val, p_test, seed=u["seed"])
    row.update({
        "status": "ok" if fit["parsed"] else "ok_unmetered",
        "hamiltonian_matches_screened": _hash(clf) == screened[
            "hamiltonian_sha256"],
        "n_weak_classifiers": len(clf.h_list),
        "n_samples_returned": len(eqc_submit.samples_of(resp)),
        "all_samples": f"device_samples/{resp_file.name}",
        "weight_cosine_vs_classical": (float(w_hw @ w_px / denom)
                                       if denom > 0 else None),
        "objective_device": obj(w_hw), "objective_proxy_optimum": obj(w_px),
        "exact_zero_fraction": float(np.mean(w_hw == 0.0)),
        "metrics": m,
    })
    if u["kind"] == "spectra":
        import spectra_segment as ss
        row["in_segment"] = ss.evaluate_in_segment(
            y_te01, p_test, extra["in_pocket_test"], u["seed"],
            label="target")
    return row


def _write(rows: list[dict], complete: bool) -> None:
    spent = sum(float(r.get("metered_seconds") or 0) for r in rows)
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps({
        "generator": "experiments/phase2/src/run_dirac3s_verify.py",
        "card": "F142", "sprint": 26, "evidence_tag": "HW",
        "device_type": DEVICE, "metered_seconds": round(spent, 2),
        "entry": "experiments/phase2/PREREGISTRATION_DRAFT.md section 6, F142",
        "complete": complete, "rows": rows}, indent=1, default=str) + "\n",
        encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--stop", type=int, choices=sorted(STOP_CAP_S),
                    required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    # Refusals FIRST, before any data is touched (run_hardware_b4.py).
    if not args.dry_run and ("PYTEST_CURRENT_TEST" in os.environ
                             or "pytest" in sys.modules):
        print("REFUSING: a metered run was invoked from a test process. "
              "Spending device seconds requires a human-invoked run.")
        return 5

    units = [u for u in UNITS if u["stop"] == args.stop]
    done = _done()
    todo = [u for u in units if u["unit"] not in done]
    print(f"F142 stop {args.stop} on {DEVICE}: units "
          f"{[u['unit'] for u in units]}; already done "
          f"{sorted(done & {u['unit'] for u in units})}")
    print(f"  CALL COUNT now : {len(todo)}")
    print(f"  EXPECTED       : {EXPECTED[args.stop]}")
    print(f"  STOP CAP       : {STOP_CAP_S[args.stop]} s")

    screened = {}
    for u in todo:
        s = offline(u)
        screened[u["unit"]] = s
        verdict = "pass" if s["screen_pass"] else "FAIL"
        print(f"  [offline] {u['unit']:14s} vars={s['n_variables']} "
              f"device={s['device_type']} samples={s['num_samples']} "
              f"off-spread/step="
              f"{s['off_diagonal_spread_over_resolvable']:.3f} "
              f"linear/step={s['linear_spread_over_resolvable']:.3f} "
              f"(dB {s['dynamic_range_db']:.1f}) screen={verdict} "
              f"({u['screen']})")
    if args.dry_run:
        print("Dry run: requests built offline; nothing submitted.")
        return 0
    if not todo:
        print("Nothing to do: every unit of this stop is already done.")
        return 0

    blocked = [u["unit"] for u in todo if u["screen"] == "enforce"
               and not screened[u["unit"]]["screen_pass"]]
    if blocked:
        print(f"REFUSING: {blocked} fail A31's resolution test and are "
              "accuracy runs.")
        return 6

    _load_env()
    from qci_client import QciClient
    client = QciClient(api_token=os.environ["QCI_TOKEN"],
                       url=os.environ["QCI_API_URL"])
    if eqc_submit._balance_or_none(client) is None:
        print("REFUSING: the allocation balance cannot be read, so the cost "
              "of each call cannot be measured.")
        return 4

    rows = _rows()
    spent = 0.0
    for u in todo:
        if spent >= STOP_CAP_S[args.stop]:
            print(f"  stop cap {STOP_CAP_S[args.stop]} s reached; stopping")
            break
        print(f"  [submit] {u['unit']} ...", flush=True)
        row = metered(u, screened[u["unit"]], client)
        rows.append(row)
        spent += float(row.get("metered_seconds") or 0)
        _write(rows, complete=False)
        print(f"      {row['status']}  {row.get('metered_seconds')} s  "
              f"wall {row.get('wall_seconds_including_queue')} s  "
              f"job {row.get('job_id')}", flush=True)
        if (u["screen"] == "enforce"
                and not row.get("hamiltonian_matches_screened", True)):
            print("STOPPING: the submitted Hamiltonian differs from the "
                  "screened one.")
            break
    _write(rows, complete=True)
    return 1 if any(r["status"] == "failed" for r in rows) else 0


def _load_env() -> None:
    env = Path(__file__).resolve().parents[3] / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())
    for k in ("QCI_TOKEN", "QCI_API_URL"):
        if not os.environ.get(k):
            raise SystemExit(f"{k} is not set; F142 cannot submit.")


if __name__ == "__main__":
    raise SystemExit(main())
