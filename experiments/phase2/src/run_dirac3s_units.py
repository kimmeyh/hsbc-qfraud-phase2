"""F155 and F95 (Sprint 31 Tasks I and J, #101 #102): Dirac-3S units, each
stop approved on its own (Criterion H).

The entries are "F155" and "F95" in `experiments/phase2/PREREGISTRATION_DRAFT.md`
section 6, committed before this module existed. Device: Dirac-3S
(`eqc_submit.PHASE2_DEVICE`; Sprint 31 D5's standing rule).

    F155 stop 1: one CVQBoost pool of 1,350 variables, one sample,
                 schedule 2: does the queue accept it?           1 call
    F95  stop 1: b1_dct_42 at relaxation schedule 4               1 call
    F95  stop 2: b1_dct_43, g0b_3_42, b1_lg_42 at schedule 4      3 calls

    <venv python> experiments/phase2/src/run_dirac3s_units.py --card F155 --stop 1 --dry-run
    <venv python> experiments/phase2/src/run_dirac3s_units.py --card F155 --stop 1   # metered

The send path is F142's, proven on Dirac-3S (`run_dirac3s_verify`: the
classifier, the screen, the ledger redirect, the client), with the Sprint 28
D4 store in place of F142's own save: `device_store.saving` checks the
Hamiltonian's hash before the send, writes an intent before it, stores the
full response and the pool declaration, and refuses a problem already sent.

PAID CALLS ARE NEVER REPEATED: one attempt per unit (`max_attempts=1`); a
unit with any row, any ledger entry or any stored intent is never sent
again; a lock refuses a second run; a stop ends at its cap (between units)
or at a failed unit. No test score is computed: neither entry reads
accuracy. Zero metered seconds in a dry run.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from contextlib import contextmanager
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "src"))
sys.path.insert(0, str(HERE))

import eqc_submit  # noqa: E402
import qubo_proxy as qp  # noqa: E402
import device_store  # noqa: E402
import provenance  # noqa: E402
import run_dirac3s_verify as v  # noqa: E402

# A stop is one to three device calls and their offline builds; it is never
# resumed mid-call, so it is not a long run (F168).
LONG_RUN = False
RESULTS = ROOT / "experiments" / "phase2" / "results"
DEVICE = eqc_submit.PHASE2_DEVICE

# B1 and G0b configurations as `run_hardware.py` ran them on Dirac-3
# (B1_VARIANTS; proxy_ranking.json's g0b_configs), rebuilt seeded (F145).
LG = {"max_iter": 300, "class_weight": "balanced"}
CARDS = {
    "F155": {
        "result": RESULTS / "f155_variable_ceiling.json",
        "cap_s": 60.0,
        "units": [
            {"unit": "pool_1350", "stop": 1, "k": 20, "order": 3,
             "wt": "dct", "wp": {}, "alpha": 2.0, "seed": 42,
             "relaxation_schedule": 2, "num_samples": 1},
        ],
    },
    "F95": {
        "result": RESULTS / "f95_schedule4.json",
        "cap_s": 120.0,
        "units": [
            {"unit": "b1_dct_42", "stop": 1, "k": 13, "order": 2,
             "wt": "dct", "wp": {}, "alpha": 2.0, "seed": 42,
             "relaxation_schedule": 4, "num_samples": 8,
             "twin": "f142:b1_42"},
            {"unit": "b1_dct_43", "stop": 2, "k": 13, "order": 2,
             "wt": "dct", "wp": {}, "alpha": 2.0, "seed": 43,
             "relaxation_schedule": 4, "num_samples": 8,
             "twin": "f142:b1_43"},
            {"unit": "g0b_3_42", "stop": 2, "k": 9, "order": 2,
             "wt": "lg", "wp": LG, "alpha": 4.0, "seed": 42,
             "relaxation_schedule": 4, "num_samples": 8,
             "twin": "dirac-3:hw_g0b_3_stratified_42"},
            {"unit": "b1_lg_42", "stop": 2, "k": 9, "order": 2,
             "wt": "lg", "wp": LG, "alpha": 0.5, "seed": 42,
             "relaxation_schedule": 4, "num_samples": 8,
             "twin": "dirac-3:hw_b1_lg_stratified_42"},
        ],
    },
}
SEEDS = {c: sorted({u["seed"] for u in spec["units"]})
         for c, spec in CARDS.items()}


def n_variables(k: int, order: int) -> int:
    """A CVQBoost pool's size: k singles, C(k,2) pairs, C(k,3) triples."""
    n = k
    if order >= 2:
        n += k * (k - 1) // 2
    if order >= 3:
        n += k * (k - 1) * (k - 2) // 6
    return n


def config(u: dict, n_train: int) -> dict:
    return dict(lambda_coef=u["alpha"] * n_train,
                weak_cls_schedule=u["order"], weak_cls_type=u["wt"],
                weak_cls_params=qp.seeded_weak_params(u["seed"], u["wp"]),
                weak_cls_strategy="multi_processing",
                relaxation_schedule=u["relaxation_schedule"],
                num_samples=u["num_samples"])


def declaration(u: dict, cfg: dict, features: list) -> dict:
    """What `device_store` keeps to rebuild the pool."""
    return {"kind": "cvqboost_pool", "weak_cls_type": u["wt"],
            "weak_cls_params": cfg["weak_cls_params"], "seed": u["seed"],
            "data": "ULB, data.stratified_split(seed), "
                    "data.top_k_features(k, seed)",
            "k": u["k"], "weak_cls_schedule": u["order"],
            "lambda_coef": cfg["lambda_coef"], "features": list(features)}


def _data(u: dict):
    split, cols, Xtr, _, _, y_pm1 = qp._prep(u["seed"], u["k"])
    return Xtr, y_pm1, config(u, len(y_pm1)), list(cols)


def offline(u: dict) -> dict:
    """The dry run of one unit: every line but the network, on Dirac-3S."""
    from qpu_cost_model import quote
    Xtr, y_pm1, cfg, cols = _data(u)
    sent: list = []
    with eqc_submit.offline_solver(sent, device_type=DEVICE):
        clf = v._make_clf(cfg, {})
        clf.fit(Xtr, y_pm1)
    s = sent[0]
    scr = v.resolution_screen(clf._J, clf._C)
    q = quote(s["n_variables"], cfg["num_samples"],
              relaxation_schedule=cfg["relaxation_schedule"])
    return {"unit": u["unit"], "n_variables": s["n_variables"],
            "n_variables_expected": n_variables(u["k"], u["order"]),
            "device_type": s["device_type"], "num_samples": s["num_samples"],
            "relaxation_schedule": cfg["relaxation_schedule"],
            "dynamic_range_db": s["dynamic_range_db"],
            "off_diagonal_spread_over_resolvable":
                scr["off_diagonal_spread_over_resolvable"],
            "linear_spread_over_resolvable":
                scr["linear_spread_over_resolvable"],
            "screen_pass": scr["pass"],
            "quote": q,
            "hamiltonian_sha256": device_store.problem_sha256(
                device_store.problem_arrays(clf))}


def _rows(card: str) -> list[dict]:
    path = CARDS[card]["result"]
    if not path.exists():
        return []
    try:
        return json.loads(path.read_text(encoding="utf-8"))["rows"]
    except Exception as exc:                              # noqa: BLE001
        raise SystemExit(
            f"REFUSING: {path.name} is unreadable ({exc}). A runner that "
            "cannot read its own record cannot know what it has paid for.")


def _ledger_units(card: str) -> set[str]:
    """Units with any entry in the Phase 2 ledger, whatever its status."""
    if not v.LEDGER.exists():
        return set()
    try:
        calls = json.loads(v.LEDGER.read_text(encoding="utf-8"))["calls"]
    except Exception as exc:                              # noqa: BLE001
        raise SystemExit(
            f"REFUSING: {v.LEDGER.name} is unreadable ({exc}). A runner "
            "that cannot read its ledger cannot know what it has paid for.")
    prefix = f"{card.lower()}_"
    out = set()
    for c in calls:
        label = str(c.get("label") or "")
        if label.startswith(prefix) and "_a" in label:
            out.add(label[len(prefix):label.rindex("_a")])
    return out


def _intent_units(card: str) -> set[str]:
    """Units with a stored intent: a send that may have happened."""
    out = set()
    tag = f"_{card.lower()}_"
    for p in (device_store.STORE_DIR / device_store.INTENTS).glob("*.json"):
        if tag in p.stem:
            out.add(p.stem.split(tag, 1)[1])
    return out


def done(card: str) -> set[str]:
    """Units ever attempted: never sent again by this runner."""
    return ({r["unit"] for r in _rows(card)} | _ledger_units(card)
            | _intent_units(card))


@contextmanager
def _lock(card: str):
    lock = CARDS[card]["result"].with_suffix(".lock")
    lock.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        raise SystemExit(f"REFUSING: {lock.name} exists; another {card} run "
                         "may be in progress. Remove it only if none is.")
    try:
        os.write(fd, str(os.getpid()).encode())
        os.close(fd)
        yield
    finally:
        lock.unlink(missing_ok=True)


def gaps(J, C, w_ref, samples) -> dict:
    """Relative objective gap of each sample to the reference optimum, in
    float64: (obj(w) - obj(w_ref)) / |obj(w_ref)|."""
    J = np.asarray(J, dtype=np.float64)
    C = np.asarray(C, dtype=np.float64)

    def obj(w):
        w = np.asarray(w, dtype=np.float64)
        return float(w @ J @ w + C @ w)

    ref = obj(w_ref)
    per = [(obj(s) - ref) / abs(ref) for s in samples]
    return {"objective_reference": ref, "per_sample_gap": per,
            "gap_min": min(per) if per else None,
            "gap_range": (max(per) - min(per)) if per else None}


def metered(card: str, u: dict, screened: dict, client, on_submitted) -> dict:
    """One metered Dirac-3S fit, ONE attempt, stored through device_store.
    `on_submitted(row)` is called as soon as the fit returns, before any
    reading, so the paid call is on disk whatever follows."""
    Xtr, y_pm1, cfg, cols = _data(u)
    wrap, saved = device_store.saving(
        card, u["unit"], DEVICE, screened["hamiltonian_sha256"],
        declaration(u, cfg, cols))
    api = dict(api_url=os.environ.get("QCI_API_URL"),
               api_token=os.environ.get("QCI_TOKEN"))

    def make_record(attempt):
        return v.mc.CallRecord(
            label=f"{card.lower()}_{u['unit']}_a{attempt + 1}", degree=2,
            n_variables=screened["n_variables"],
            n_samples=cfg["num_samples"],
            expected_seconds=screened["quote"].get("high_s") or 10.0)

    t_submit = time.strftime("%Y-%m-%dT%H:%M:%S")
    t0 = time.perf_counter()
    with v._phase2_ledger(), eqc_submit.device(DEVICE, wrap=wrap):
        fit = eqc_submit.metered_fit(lambda: v._make_clf(cfg, api), Xtr,
                                     y_pm1, make_record, client,
                                     max_attempts=1,
                                     zero_cost_is_unparsed=True)
    row = {"card": card, "unit": u["unit"], "stop": u["stop"],
           "seed": u["seed"], "device_type": DEVICE, "evidence_tag": "HW",
           "job_id": fit["job_id"] or saved.get("job_id"),
           "metered_seconds": fit["metered_seconds"],
           "metered_seconds_parsed": fit["parsed"],
           "attempts": fit["attempts"],
           "wall_seconds_including_queue": round(time.perf_counter() - t0, 1),
           "submitted": t_submit,
           "finished": time.strftime("%Y-%m-%dT%H:%M:%S"),
           "stored": (str(Path(saved["path"]).relative_to(RESULTS))
                      if saved.get("path") else None),
           "hw_config": {k: (dict(x) if isinstance(x, dict) else x)
                         for k, x in cfg.items()},
           "screen": {k: screened[k] for k in (
               "off_diagonal_spread_over_resolvable",
               "linear_spread_over_resolvable", "screen_pass",
               "dynamic_range_db", "n_variables", "hamiltonian_sha256")},
           "twin": u.get("twin")}
    if fit["clf"] is None:
        row.update({"status": "failed", "error": fit["error"]})
        row.update(_returned_length(saved, screened["n_variables"]))
        on_submitted(row)
        return row
    device_store.require_saved(saved)
    row["status"] = "submitted_reading"
    on_submitted(row)
    try:
        read(card, row, fit, cfg, Xtr, y_pm1, screened["n_variables"])
    except Exception as exc:                               # noqa: BLE001
        import traceback
        row.update({"status": "ok_reading_failed",
                    "reading_error": f"{type(exc).__name__}: {exc}"[:400],
                    "reading_traceback": traceback.format_exc()[-4000:]})
    return row


def _returned_length(saved: dict, n: int) -> dict:
    """For a failed fit: the returned solution's length, if a response was
    stored (the library asserts the length after the response is saved)."""
    path = saved.get("path")
    if not path or not Path(path).exists():
        return {"returned_length": None, "accepted": False}
    doc = json.loads(Path(path).read_text(encoding="utf-8"))
    sols = eqc_submit.samples_of(doc.get("response") or {})
    length = len(sols[0]) if sols else None
    return {"returned_length": length, "accepted": length == n}


def read(card, row, fit, cfg, Xtr, y_pm1, n) -> None:
    """Everything after the paid call; no test score. Updates `row`."""
    clf, resp = fit["clf"], fit["resp"]
    samples = eqc_submit.samples_of(resp)
    row["n_samples_returned"] = len(samples)
    row["returned_length"] = len(samples[0]) if samples else None
    row["device_timing"] = v.device_timing(resp)
    if card == "F155":
        row["accepted"] = row["returned_length"] == n
        row["status"] = "ok" if fit["parsed"] else "ok_unmetered"
        return
    H = qp.h_matrix(clf, Xtr)
    w_ref = qp.solve_simplex_qp(H, y_pm1, cfg["lambda_coef"])
    J, C = qp.hamiltonian(H.astype(np.float64), y_pm1, cfg["lambda_coef"])
    g = gaps(J, C, w_ref, samples)
    row.update({"gap_device_weights": gaps(J, C, w_ref, [clf.params])
                ["per_sample_gap"][0], **g,
                "status": "ok" if fit["parsed"] else "ok_unmetered"})


F142_DRY_RUN = RESULTS / "f142_dry_run.json"
F142_RESULT = RESULTS / "f142_dirac3s_verify.json"


def twin_gaps(f142_unit: str) -> dict:
    """The schedule-2 twin's per-sample gaps, from F142's stored samples:
    the pool rebuilt seeded, its hash checked against F142's dry run, the
    reference optimum solved, each stored sample's objective computed.
    No device call."""
    rows = {r["unit"]: r for r in json.loads(
        F142_RESULT.read_text(encoding="utf-8"))["rows"]}
    row = rows[f142_unit]
    hashes = {u["unit"]: u["hamiltonian_sha256"]
              for s in json.loads(F142_DRY_RUN.read_text(
                  encoding="utf-8"))["stops"].values() for u in s["units"]}
    u = next(x for x in v.UNITS if x["unit"] == f142_unit)
    Xtr, _, _, y_pm1, _, _, cfg, _ = v._data(u)
    sent: list = []
    with eqc_submit.offline_solver(sent, device_type=DEVICE):
        clf = v._make_clf(cfg, {})
        clf.fit(Xtr, y_pm1)
    sha = device_store.problem_sha256(device_store.problem_arrays(clf))
    if sha != hashes[f142_unit]:
        raise RuntimeError(f"{f142_unit}: the rebuilt pool's hash differs "
                           "from F142's dry run; its samples cannot be read "
                           "against it")
    doc = json.loads((RESULTS / row["all_samples"]).read_text(
        encoding="utf-8"))
    samples = eqc_submit.samples_of(doc["response"])
    H = qp.h_matrix(clf, Xtr)
    w_ref = qp.solve_simplex_qp(H, y_pm1, cfg["lambda_coef"])
    J, C = qp.hamiltonian(H.astype(np.float64), y_pm1, cfg["lambda_coef"])
    return {"f142_unit": f142_unit, "hamiltonian_sha256": sha,
            "relaxation_schedule": row["hw_config"]["relaxation_schedule"],
            "samples": row["all_samples"], **gaps(J, C, w_ref, samples)}


TWINS_RESULT = RESULTS / "f95_schedule4_twins.json"
HW_DISPERSION = ROOT / "experiments" / "results" / "hw_dispersion.json"


def twin_reading(row: dict, twin: dict) -> dict:
    """The F95 entry's reading for a unit with a same-device twin:
    schedule 4 changes the reading only if its gap differs from the
    twin's by more than the range of the twin's per-sample gaps. The gap
    compared is each side's best sample (`gap_min`)."""
    for side, d in (("schedule-4 row", row), ("twin", twin)):
        if d.get("gap_min") is None or d.get("gap_range") is None:
            raise ValueError(f"{row['unit']}: the {side} has no per-sample "
                             "gaps, so the entry's comparison cannot be made")
    diff = row["gap_min"] - twin["gap_min"]
    return {"gap_difference": diff, "twin_gap_range": twin["gap_range"],
            "changes_reading": abs(diff) > twin["gap_range"]}


def dirac3_history(file: str) -> dict:
    """A Dirac-3 schedule-2 fit's recorded gap, reported beside a unit
    with no same-device twin (not compared as a test)."""
    fits = json.loads(HW_DISPERSION.read_text(encoding="utf-8"))["per_fit"]
    hit = [p for p in fits if p.get("file") == file]
    if len(hit) != 1:
        raise ValueError(f"{file}: {len(hit)} rows in hw_dispersion.json")
    p = hit[0]
    return {"source": "experiments/results/hw_dispersion.json",
            "file": file, "device": "dirac-3",
            "relaxation_schedule": p["relaxation_schedule"],
            "gap_to_exact_pct": p["gap_to_exact_pct"]}


def twins(read_twin=None) -> Path:
    """F95's preregistered reading, offline, from stored samples only
    (no device call): each unit's schedule-4 gap against its twin. Written
    to its own file; `f95_schedule4.json` is read, never written."""
    read_twin = read_twin or twin_gaps
    rows = json.loads(CARDS["F95"]["result"].read_text(
        encoding="utf-8"))["rows"]
    run_id, _ = provenance.start(TWINS_RESULT, resumable=False)
    out = []
    for r in rows:
        kind, name = r["twin"].split(":", 1)
        rec = {"unit": r["unit"], "twin": r["twin"],
               "gap_min": r["gap_min"], "gap_range": r["gap_range"],
               "screen_pass": r["screen"]["screen_pass"]}
        if kind == "f142":
            t = read_twin(name)
            rec["twin_gaps"] = t
            rec["reading"] = twin_reading(r, t)
        else:
            rec["dirac3_history"] = dirac3_history(f"{name}.json")
            rec["reading"] = "reported beside, not a test: the device differs"
        out.append(rec)
    doc = {"generator": "experiments/phase2/src/run_dirac3s_units.py "
                        "--card F95 --twins",
           "card": "F95", "sprint": 31, "evidence_tag": "HW",
           "metered_seconds": 0, "complete": True,
           "entry": "experiments/phase2/PREREGISTRATION_DRAFT.md section 6, "
                    "F95, Reading",
           "note": "computed from stored device samples; no device call",
           "rows": out}
    provenance.write_result(TWINS_RESULT, doc, __file__, SEEDS["F95"],
                            run_id)
    return TWINS_RESULT


def write(card: str, rows: list, run_id: str) -> None:
    spec = CARDS[card]
    good = {r["unit"] for r in rows if r.get("status") in ("ok",
                                                           "ok_unmetered")}
    doc = {"generator": "experiments/phase2/src/run_dirac3s_units.py",
           "card": card, "sprint": 31, "evidence_tag": "HW",
           "device_type": DEVICE,
           "metered_seconds": round(sum(float(r.get("metered_seconds") or 0)
                                        for r in rows), 2),
           "entry": f"experiments/phase2/PREREGISTRATION_DRAFT.md section 6, "
                    f"{card}",
           "complete": all(u["unit"] in good for u in spec["units"]),
           "rows": rows}
    provenance.write_result(spec["result"], doc, __file__, SEEDS[card],
                            run_id)


NONZERO = ("failed", "ok_reading_failed")


def run_stop(card: str, stop: int, todo: list, screened: dict,
             make_client=None, fit=None, balance=None) -> int:
    """A metered stop after its offline builds. Stubs for `make_client`,
    `fit` (signature of `metered`) and `balance` let the refusals, the
    skip, the cap and the exit code be tested with nothing sent."""
    make_client = make_client or v._client
    fit = fit or metered
    balance = balance or eqc_submit._balance_or_none
    if not todo:
        print("Nothing to do: every unit of this stop is already done.")
        return 0
    client = make_client()
    if balance(client) is None:
        print("REFUSING: the allocation balance cannot be read, so the cost "
              "of each call cannot be measured.")
        return 4
    cap = CARDS[card]["cap_s"]
    with _lock(card):
        run_id, _ = provenance.start(CARDS[card]["result"])
        rows = _rows(card)
        spent = sum(float(r.get("metered_seconds") or 0) for r in rows)
        for u in todo:
            if spent >= cap:
                print(f"  cap {cap} s reached ({spent:.1f} s); stopping")
                break
            if u["unit"] in done(card):        # re-read: never pay twice
                continue
            print(f"  [submit] {u['unit']} ...", flush=True)

            def on_submitted(row):
                if row not in rows:
                    rows.append(row)
                write(card, rows, run_id)

            row = fit(card, u, screened[u["unit"]], client, on_submitted)
            spent += float(row.get("metered_seconds") or 0)
            write(card, rows, run_id)
            print(f"      {row['status']}  {row.get('metered_seconds')} s  "
                  f"wall {row.get('wall_seconds_including_queue')} s  "
                  f"job {row.get('job_id')}", flush=True)
            if row["status"] == "failed":
                print("STOPPING: a failed unit is not retried and ends the "
                      "stop; it needs a human decision.")
                break
    return 1 if any(r["status"] in NONZERO for r in rows) else 0


def dry_run(card: str, stop: int, screened: dict) -> Path:
    """The figures a Criterion H statement quotes, in a file."""
    path = RESULTS / f"{card.lower()}_dry_run_stop{stop}.json"
    run_id, _ = provenance.start(path, resumable=False)
    doc = {"generator": "experiments/phase2/src/run_dirac3s_units.py "
                        "--dry-run",
           "card": card, "stop": stop, "evidence_tag": "SIM",
           "metered_seconds": 0, "complete": True,
           "note": "offline builds of the requests the stop would send; no "
                   "device call",
           "written": time.strftime("%Y-%m-%dT%H:%M:%S"),
           "units": list(screened.values())}
    provenance.write_result(path, doc, __file__, SEEDS[card], run_id)
    return path


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--card", choices=sorted(CARDS), required=True)
    ap.add_argument("--stop", type=int)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--twins", action="store_true",
                    help="F95 only: the entry's reading against each twin, "
                         "from stored samples; no device call")
    args = ap.parse_args(argv)
    if args.twins:
        if args.card != "F95":
            print("REFUSING: --twins is F95's reading only.")
            return 2
        print(f"Written: {twins().name}")
        return 0
    if args.stop is None:
        ap.error("--stop is required unless --twins is given")
    units = [u for u in CARDS[args.card]["units"] if u["stop"] == args.stop]
    if not units:
        print(f"REFUSING: {args.card} has no stop {args.stop}.")
        return 2
    # Refusals FIRST, before any data is touched (run_hardware_b4.py).
    if not args.dry_run and ("PYTEST_CURRENT_TEST" in os.environ
                             or "pytest" in sys.modules):
        print("REFUSING: a metered run was invoked from a test process. "
              "Spending device seconds requires a human-invoked run.")
        return 5
    finished = done(args.card)
    todo = [u for u in units if u["unit"] not in finished]
    print(f"{args.card} stop {args.stop} on {DEVICE}: units "
          f"{[u['unit'] for u in units]}; already done "
          f"{sorted(finished & {u['unit'] for u in units})}")
    print(f"  CALL COUNT now : {len(todo)} (one attempt per unit, no retry)")
    print(f"  CAP            : {CARDS[args.card]['cap_s']} s over the card")
    screened = {}
    for u in (units if args.dry_run else todo):
        s = offline(u)
        screened[u["unit"]] = s
        if s["n_variables"] != s["n_variables_expected"]:
            print(f"REFUSING: {u['unit']} built {s['n_variables']} variables, "
                  f"not the entry's {s['n_variables_expected']}.")
            return 3
        print(f"  [offline] {u['unit']:10s} vars={s['n_variables']} "
              f"device={s['device_type']} samples={s['num_samples']} "
              f"schedule={s['relaxation_schedule']} "
              f"screen={'pass' if s['screen_pass'] else 'FAIL'} "
              f"quote={s['quote']}")
    if args.dry_run:
        path = dry_run(args.card, args.stop, screened)
        print(f"Dry run: requests built offline; nothing submitted. "
              f"Written: {path.name}")
        return 0
    return run_stop(args.card, args.stop, todo, screened)


if __name__ == "__main__":
    raise SystemExit(main())
