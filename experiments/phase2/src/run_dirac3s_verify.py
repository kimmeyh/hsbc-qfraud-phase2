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
metered build are byte-identical. The runner enforces that BEFORE the
network call: its solver subclass (`_guarded`) hashes J and C inside
`solve`, before the library uploads anything, and raises
`eqc_submit.NoRetry` if they differ from the screened hash, or if an
`enforce` unit fails the screen. (Unseeded, the two builds drift, and the
screen would be of a different matrix.)

PAID CALLS ARE NEVER REPEATED BY THE RUNNER (Sprint 26 code review):
- One attempt per unit (`max_attempts=1`): a fit can fail AFTER the device
  billed it (the metrics read, the size check), and a retry would pay again.
  So the call count approved for a stop is the most it can spend.
- The raw response is saved in `makeResults`, before any post-processing,
  under a name carrying the job id, and never overwritten.
- A "submitted" row is written as soon as the fit returns, before scoring.
- A unit with ANY row, or ANY Phase 2 ledger entry, is never submitted
  again; a crash between the intent write and the outcome leaves a ledger
  entry, and that unit was possibly billed. Clearing one is a human act.
- A zero or negative balance change on a successful call is charged the
  conservative estimate (Dirac-3S's billing source is unverified, question
  A3), so the stop cap still counts it. The cap applies between units: a
  running call cannot be stopped.
- A lock file refuses a second concurrent run.

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
DRY_RUN = PHASE2_RESULTS / "f142_dry_run.json"
LEDGER = PHASE2_RESULTS / "qpu_cost_ledger_phase2.json"
LOG_DIR = PHASE2_RESULTS / "call_logs"
RESP_DIR = PHASE2_RESULTS / "device_samples"
DEVICE = eqc_submit.DIRAC_3S  # device named: F142 verifies Dirac-3S itself
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


def _ledger_units() -> set[str]:
    """Units with any entry in the Phase 2 ledger, whatever its status."""
    if not LEDGER.exists():
        return set()
    try:
        calls = json.loads(LEDGER.read_text(encoding="utf-8"))["calls"]
    except Exception as exc:                              # noqa: BLE001
        raise SystemExit(
            f"REFUSING: {LEDGER.name} is unreadable ({exc}). A runner that "
            "cannot read its ledger cannot know what it has paid for.")
    out = set()
    for c in calls:
        label = str(c.get("label") or "")
        if label.startswith("f142_") and "_a" in label:
            out.add(label[len("f142_"):label.rindex("_a")])
    return out


def _done() -> set[str]:
    """Units ever attempted: any row, any status, or any ledger entry. Never
    submitted again by this runner (a failed unit may have been billed)."""
    return {r["unit"] for r in _rows()} | _ledger_units()


@contextmanager
def _lock():
    """One metered run at a time: a second one would see the same units as
    not done and submit them too."""
    lock = RESULT.with_suffix(".lock")
    lock.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        raise SystemExit(f"REFUSING: {lock.name} exists; another F142 run "
                         "may be in progress. Remove it only if none is.")
    try:
        os.write(fd, str(os.getpid()).encode())
        os.close(fd)
        yield
    finally:
        lock.unlink(missing_ok=True)


def _guarded(unit: dict, screened: dict, saved: dict):
    """A `wrap` for `eqc_submit.device`: the pre-submit check and the raw
    response save, on the device's own solver class."""
    def wrap(cls):
        class Guarded(cls):
            def solve(self, model, **kw):
                if _hash(model) != screened["hamiltonian_sha256"]:
                    raise eqc_submit.NoRetry(
                        "pre-submit: Hamiltonian differs from the screened "
                        "one; nothing sent")
                if unit["screen"] == "enforce" and not resolution_screen(
                        model._J, model._C)["pass"]:
                    raise eqc_submit.NoRetry(
                        "pre-submit: fails A31's resolution test; nothing "
                        "sent")
                return super().solve(model, **kw)

            def makeResults(self, model, response):
                job_id = str((response.get("job_info") or {}).get("job_id"))
                RESP_DIR.mkdir(parents=True, exist_ok=True)
                path = RESP_DIR / f"f142_{unit['unit']}_{job_id}.json"
                if path.exists():
                    path = path.with_name(
                        f"{path.stem}_{time.strftime('%Y%m%dT%H%M%S')}.json")
                path.write_text(json.dumps(
                    {"job_id": job_id, "device_type": DEVICE, "card": "F142",
                     "unit": unit["unit"],
                     "response": eqc_submit.to_jsonable(response)},
                    indent=1), encoding="utf-8")
                saved["path"], saved["job_id"] = path, job_id
                return super().makeResults(model, response)
        return Guarded
    return wrap


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
    reach max |coefficient| / 200? The test is F104's shared gate,
    `device_resolution.resolution_gate` (Sprint 27).
    """
    import device_resolution as dres
    g = dres.resolution_gate(J, C)
    return {k: g[k] for k in ("off_diagonal_spread_over_resolvable",
                              "linear_spread_over_resolvable", "pass")}


def offline(u: dict) -> dict:
    """The dry run of one unit: every line but the network, on Dirac-3S."""
    Xtr, _, _, y_pm1, _, _, cfg, _ = _data(u)
    sent: list = []
    with eqc_submit.offline_solver(sent, device_type=DEVICE):
        clf = _make_clf(cfg, {})
        clf.fit(Xtr, y_pm1)
    s = sent[0]
    scr = resolution_screen(clf._J, clf._C)
    # A31's second half, REPORTED, not enforced: an optimum whose weights sit
    # below about 1/200 of the sum constraint cannot be represented, so the
    # device returns a sparser vector (fresh-eyes review, finding 13).
    w = qp.solve_simplex_qp(qp.h_matrix(clf, Xtr), y_pm1, cfg["lambda_coef"])
    nz = w[w > 0]
    return {"unit": u["unit"], "n_variables": s["n_variables"],
            "exact_optimum_median_nonzero_weight": float(np.median(nz)),
            "weight_step": 1.0 / 200.0,
            "weights_resolvable": bool(np.median(nz) >= 1.0 / 200.0),
            "device_type": s["device_type"], "num_samples": s["num_samples"],
            "dynamic_range_db": s["dynamic_range_db"],
            "off_diagonal_spread_over_resolvable":
                scr["off_diagonal_spread_over_resolvable"],
            "linear_spread_over_resolvable":
                scr["linear_spread_over_resolvable"],
            "screen_pass": scr["pass"],
            "hamiltonian_sha256": _hash(clf)}


def metered(u: dict, screened: dict, client, on_submitted) -> dict:
    """One metered Dirac-3S fit, ONE attempt. Caller has checked the screen;
    the solver checks it again before the network call. `on_submitted(row)`
    is called as soon as the fit returns, before scoring, so the paid call
    is on disk even if scoring fails."""
    Xtr, Xva, Xte, y_pm1, y_va01, y_te01, cfg, extra = _data(u)
    api = dict(api_url=os.environ.get("QCI_API_URL"),
               api_token=os.environ.get("QCI_TOKEN"))
    saved: dict = {}

    def make_clf():
        return _make_clf(cfg, api)

    def make_record(attempt):
        return mc.CallRecord(label=f"f142_{u['unit']}_a{attempt + 1}",
                             degree=2, n_variables=screened["n_variables"],
                             n_samples=cfg["num_samples"],
                             expected_seconds=EXPECTED[u["stop"]])

    t_submit = time.strftime("%Y-%m-%dT%H:%M:%S")
    t0 = time.perf_counter()
    with _phase2_ledger(), eqc_submit.device(
            DEVICE, wrap=_guarded(u, screened, saved)):
        fit = eqc_submit.metered_fit(make_clf, Xtr, y_pm1, make_record,
                                     client, max_attempts=1,
                                     zero_cost_is_unparsed=True)
    wall = round(time.perf_counter() - t0, 1)

    row = {"arm": ARM, "card": "F142", "unit": u["unit"], "stop": u["stop"],
           "seed": u["seed"], "device_type": DEVICE,
           "evidence_tag": "HW",
           "job_id": fit["job_id"] or saved.get("job_id"),
           "metered_seconds": fit["metered_seconds"],
           "metered_seconds_parsed": fit["parsed"],
           "attempts": fit["attempts"],
           "wall_seconds_including_queue": wall,
           "submitted": t_submit,
           "finished": time.strftime("%Y-%m-%dT%H:%M:%S"),
           "all_samples": (f"device_samples/{saved['path'].name}"
                           if saved.get("path") else None),
           "hw_config": {k: (dict(v) if isinstance(v, dict) else v)
                         for k, v in cfg.items()},
           "screen": {**{k: screened[k] for k in (
               "off_diagonal_spread_over_resolvable",
               "linear_spread_over_resolvable", "screen_pass",
               "dynamic_range_db", "n_variables",
               "exact_optimum_median_nonzero_weight", "weights_resolvable",
               # What was sent, on the row itself, so no later command can
               # erase the record the readout checks against (PR #21 review).
               "hamiltonian_sha256")},
                      "test": "A31: spreads >= max |coefficient| / 200",
                      "rule": u["screen"]},
           "features_used": list(extra["features"])}
    if fit["clf"] is None:
        row.update({"status": "failed", "error": fit["error"]})
        on_submitted(row)
        return row
    row["status"] = "submitted_scoring"
    on_submitted(row)
    try:
        _score(row, u, fit, cfg, Xtr, Xva, Xte, y_pm1, y_va01, y_te01, extra)
    except Exception as exc:                               # noqa: BLE001
        import traceback
        row.update({"status": "ok_scoring_failed",
                    "scoring_error": f"{type(exc).__name__}: {exc}"[:400],
                    # The paid call is kept; the traceback says what to fix
                    # before it is rescored (PR #21 review).
                    "scoring_traceback": traceback.format_exc()[-4000:]})
    return row


def _merge_dry_run(prior_stop: dict | None, screened: dict, units: list,
                   now: str) -> dict:
    """A stop's dry-run entry, per unit: the units rebuilt now replace their
    old entries, and every other unit's entry is KEPT.

    PR #21 review: the entry used to be replaced whole by the units still to
    do, so a dry run of a finished stop wrote `units: []` and erased the
    Hamiltonian hashes of calls already paid for, which the readout checks
    its rebuilt pools against."""
    kept = {u["unit"]: u for u in (prior_stop or {}).get("units", [])}
    for name, s in screened.items():
        kept[name] = {**s, "unit": name, "written": now}
    order = [u["unit"] for u in units]
    return {"written": now,
            "units": sorted(kept.values(),
                            key=lambda u: (order.index(u["unit"])
                                           if u["unit"] in order
                                           else len(order)))}


# A paid unit that was not scored is not a success: the exit code says so
# (PR #21 review: `ok_scoring_failed` exited 0).
NONZERO_STATUSES = ("failed", "ok_scoring_failed")


def device_timing(resp) -> dict | None:
    """Per-sample run times from the library's result, in seconds. eqc-models
    reads them from the job metrics under the submitted device name, so their
    presence shows the `dirac-3s` metrics key works. Stop 1's row predates
    this field (its billed figure is the response's `device_usage_s`)."""
    rt = list(getattr(resp, "run_time", None) or [])
    unit = getattr(resp, "time_units", None)
    if not rt or unit != "ns":
        return None
    pre = getattr(resp, "preprocessing_time", None)
    return {"run_time_per_sample_s": [float(t) / 1e9 for t in rt],
            "runtime_sum_s": float(sum(rt)) / 1e9,
            "preprocessing_s": float(pre) / 1e9 if pre is not None else None,
            "source": "eqc-models SolutionResults.run_time (ns)"}


def _score(row, u, fit, cfg, Xtr, Xva, Xte, y_pm1, y_va01, y_te01, extra):
    """Everything after the paid call. Updates `row` in place."""
    clf, resp = fit["clf"], fit["resp"]
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
        "n_weak_classifiers": len(clf.h_list),
        "n_samples_returned": len(eqc_submit.samples_of(resp)),
        "weight_cosine_vs_classical": (float(w_hw @ w_px / denom)
                                       if denom > 0 else None),
        "objective_device": obj(w_hw), "objective_proxy_optimum": obj(w_px),
        "exact_zero_fraction": float(np.mean(w_hw == 0.0)),
        "device_timing": device_timing(resp),
        "metrics": m,
    })
    if u["kind"] == "spectra":
        import spectra_segment as ss
        row["in_segment"] = ss.evaluate_in_segment(
            y_te01, p_test, extra["in_pocket_test"], u["seed"],
            label="target")


def _write(rows: list[dict]) -> None:
    """`complete` is true only when every unit of every stop has a scored
    row; a stop ended by its cap or a failure is not complete."""
    spent = sum(float(r.get("metered_seconds") or 0) for r in rows)
    scored = {r["unit"] for r in rows if r.get("status") in ("ok",
                                                             "ok_unmetered")}
    complete = all(u["unit"] in scored for u in UNITS)
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
    print(f"  CALL COUNT now : {len(todo)} (one attempt per unit, no retry)")
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
              f"median-weight={s['exact_optimum_median_nonzero_weight']:.4f}"
              f"{'' if s['weights_resolvable'] else ' (below 0.005)'} "
              f"({u['screen']})")
    if args.dry_run:
        # The figures a Criterion H statement quotes come from a file, not
        # a console (fresh-eyes review, finding 14).
        DRY_RUN.parent.mkdir(parents=True, exist_ok=True)
        prior = (json.loads(DRY_RUN.read_text(encoding="utf-8"))["stops"]
                 if DRY_RUN.exists() else {})
        prior[str(args.stop)] = _merge_dry_run(
            prior.get(str(args.stop)), screened, units,
            time.strftime("%Y-%m-%dT%H:%M:%S"))
        DRY_RUN.write_text(json.dumps({
            "generator": "experiments/phase2/src/run_dirac3s_verify.py "
                         "--dry-run",
            "card": "F142", "evidence_tag": "SIM", "metered_seconds": 0,
            "note": "offline builds of the requests each stop would send; "
                    "no device call",
            "stops": prior}, indent=1) + "\n", encoding="utf-8")
        print(f"Dry run: requests built offline; nothing submitted. "
              f"Written: {DRY_RUN.name}")
        return 0
    return _run_stop(args.stop, todo, screened)


def _client():
    """The live QCi client, with the credentials from `.env`."""
    _load_env()
    from qci_client import QciClient
    return QciClient(api_token=os.environ["QCI_TOKEN"],
                     url=os.environ["QCI_API_URL"])


def _run_stop(stop: int, todo: list[dict], screened: dict,
              make_client=None, fit=None, balance=None) -> int:
    """A metered stop after its offline builds: the refusals, then each
    unit's one paid fit. Returns main()'s exit code.

    F149 (Sprint 27): extracted from main() so the per-unit skip, the cap,
    the save and the exit code can be tested with a stub `fit` (signature of
    `metered`), a stub `make_client` and a stub `balance` reader. main()
    passes none of them, so a real run uses `_client`, `metered` and
    `eqc_submit._balance_or_none`.
    """
    make_client = make_client or _client
    fit = fit or metered
    balance = balance or eqc_submit._balance_or_none
    if not todo:
        print("Nothing to do: every unit of this stop is already done.")
        return 0

    blocked = [u["unit"] for u in todo if u["screen"] == "enforce"
               and not screened[u["unit"]]["screen_pass"]]
    if blocked:
        print(f"REFUSING: {blocked} fail A31's resolution test and are "
              "accuracy runs.")
        return 6

    client = make_client()
    if balance(client) is None:
        print("REFUSING: the allocation balance cannot be read, so the cost "
              "of each call cannot be measured.")
        return 4

    with _lock():
        rows = _rows()
        # Spend already recorded on this stop counts against its cap.
        spent = sum(float(r.get("metered_seconds") or 0) for r in rows
                    if r.get("stop") == stop)
        for u in todo:
            if spent >= STOP_CAP_S[stop]:
                print(f"  stop cap {STOP_CAP_S[stop]} s reached "
                      f"({spent:.1f} s); stopping")
                break
            if u["unit"] in _done():          # re-read: never pay twice
                continue
            print(f"  [submit] {u['unit']} ...", flush=True)

            def on_submitted(row):
                if row not in rows:
                    rows.append(row)
                _write(rows)

            row = fit(u, screened[u["unit"]], client, on_submitted)
            spent += float(row.get("metered_seconds") or 0)
            _write(rows)
            print(f"      {row['status']}  {row.get('metered_seconds')} s  "
                  f"wall {row.get('wall_seconds_including_queue')} s  "
                  f"job {row.get('job_id')}", flush=True)
            if row["status"] == "failed":
                print("STOPPING: a failed unit is not retried and ends the "
                      "stop; it needs a human decision.")
                break
        _write(rows)
    return 1 if any(r["status"] in NONZERO_STATUSES for r in rows) else 0


def _load_env(env: Path | None = None) -> None:
    # The one `.env` reader (Sprint 26 IMP-1). It accepts the repository's
    # key name as the token; this runner's own copy once did not, and the
    # first stop exited before submitting.
    import qci_env
    qci_env.load(env)


if __name__ == "__main__":
    raise SystemExit(main())
