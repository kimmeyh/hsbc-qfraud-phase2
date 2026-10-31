"""F172 (Sprint 30 Task I, #83): each seeded module's resume loop skips
the units its result already records, at module level.

`provenance.start` decides whether a run resumes; these tests check the
loop that acts on that decision. Each module runs against a recorded
result in tmp_path with its unit of work replaced by a recorder, so
nothing is fitted and nothing under `experiments/` is written.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
PHASE2 = ROOT / "experiments" / "phase2" / "src"
THIS = Path(__file__).relative_to(ROOT).as_posix()
sys.path.insert(0, str(PHASE2))


class _Done(Exception):
    """Raised by the first call after the loop: the loop has finished."""


def _done(*a, **k):
    raise _Done


def _resume(monkeypatch, mod, tmp_path, doc: dict) -> None:
    import provenance
    out = tmp_path / "result.json"
    out.write_text(json.dumps(doc), encoding="utf-8")
    monkeypatch.setattr(mod, "OUT", out)
    monkeypatch.setattr(provenance, "start", lambda *a, **k: ("rid", True))
    monkeypatch.setattr(provenance, "write_result", lambda *a, **k: None)


def test_f156_resumes_at_its_first_unrecorded_seed(monkeypatch, tmp_path):
    import f156_hp_bound as m
    seeds = list(m.fc.SEEDS)
    _resume(monkeypatch, m, tmp_path, {"rows": [{"seed": s} for s in seeds[:2]]})
    pilot = tmp_path / "pilot.json"
    pilot.write_text(json.dumps({"size_for_run": 100}), encoding="utf-8")
    monkeypatch.setattr(m, "OUT_PILOT", pilot)
    ran = []
    monkeypatch.setattr(m, "seed_run", lambda s, size: ran.append(s) or {"seed": s})
    monkeypatch.setattr(m, "_doc", lambda *a, **k: {"summary": {}})
    m.main(["run"])
    assert ran == seeds[2:]


def test_f158_resumes_at_its_first_unrecorded_seed(monkeypatch, tmp_path):
    import f158_fraud_types as m
    seeds = list(m.SEEDS)
    _resume(monkeypatch, m, tmp_path, {"rows": [{"seed": s} for s in seeds[:2]]})
    ran = []
    monkeypatch.setattr(m, "seed_run", lambda s: ran.append(s) or {"seed": s})
    monkeypatch.setattr(m, "_doc", lambda *a, **k: {})
    monkeypatch.setattr(m, "step3", _done)
    with pytest.raises(_Done):
        m.main()
    assert ran == seeds[2:]


def test_f159_resumes_at_its_first_untimed_unit(monkeypatch, tmp_path):
    import f159_parallel_pool as m
    units = [(f, b) for f in m.FRACTIONS for b in ("serial", *map(str, m.WORKERS))]
    _resume(monkeypatch, m, tmp_path, {"units": [
        {"fraction": f, "build": b} for f, b in units[:2]]})
    ran = []

    def unit(frac, build, budget):
        ran.append((frac, build))
        return {"fraction": frac, "build": build}
    monkeypatch.setattr(m, "time_unit", unit)
    monkeypatch.setattr(m, "budget_for", lambda *a: None)
    monkeypatch.setattr(m, "_doc", lambda units: {})
    monkeypatch.setattr(m, "leave_if_abandoned", lambda failed: None)
    m.main(["run"])
    assert ran == units[2:]


def test_f166_resumes_at_its_first_unrecorded_seed(monkeypatch, tmp_path):
    import f166_ulb_algorithms as m
    seeds = list(range(42, 47))
    _resume(monkeypatch, m, tmp_path, {
        "rows": [{"seed": s} for s in seeds[:2]],
        "seed_plan": {"seeds": seeds}, "proxy_build": {"use": False}})
    ran = []
    monkeypatch.setattr(m, "seed_run",
                        lambda s, par: (ran.append(s) or {"seed": s}, {}))
    monkeypatch.setattr(m, "_doc", lambda *a, **k: {})
    monkeypatch.setattr(m, "load_scores", _done)
    with pytest.raises(_Done):
        m.run()
    assert ran == seeds[2:]


def test_f169_resumes_at_its_first_unrecorded_seed(monkeypatch, tmp_path):
    import f169_plugin_bins as m
    seeds = list(m.fc.SEEDS)
    _resume(monkeypatch, m, tmp_path, {"rows": [{"seed": s} for s in seeds[:2]]})
    ran = []
    monkeypatch.setattr(m, "seed_run", lambda s: ran.append(s) or {"seed": s})
    monkeypatch.setattr(m, "_doc", lambda *a, **k: {"summary": {}})
    m.main()
    assert ran == seeds[2:]


def test_f174_resumes_at_its_first_unrecorded_seed(monkeypatch, tmp_path):
    import f174_ieee_algorithms as m
    seeds = list(m.SEEDS)
    _resume(monkeypatch, m, tmp_path, {"rows": [{"seed": s} for s in seeds[:2]]})
    monkeypatch.setattr(m, "data", lambda: {
        "val": {"meta": {}}, "test": {"meta": {}}, "rows_after_dedupe": 0,
        "exact_duplicates_removed": 0})
    ran = []
    monkeypatch.setattr(m, "seed_run",
                        lambda s, d: ran.append(s) or {"seed": s, "minutes": 0})
    monkeypatch.setattr(m, "_doc", lambda *a, **k: {})
    monkeypatch.setattr(m.f166, "load_scores", _done)
    with pytest.raises(_Done):
        m.run()
    assert ran == seeds[2:]


LOOPS = {
    "f156_hp_bound.py": ("                continue           # resume: never redo a seed\n",
                         "f156"),
    "f158_fraud_types.py": ("            continue           # resume: never redo a seed\n",
                            "f158"),
    "f159_parallel_pool.py": ("                        continue       # resume: never time "
                              "a unit twice\n", "f159"),
    "f166_ulb_algorithms.py": ("            continue           # resume: never refit a seed\n",
                               "f166"),
    "f169_plugin_bins.py": ("            continue           # resume: never redo a seed\n",
                            "f169"),
    "f174_ieee_algorithms.py": ("            continue           # resume: never refit a seed\n",
                                "f174"),
}


@pytest.mark.parametrize("name", sorted(LOOPS))
def test_each_resume_loop_can_fail(name):
    from injection import Mutation, assert_can_fail, run_pytest
    old, card = LOOPS[name]
    node = next(n for n in globals() if n.startswith(f"test_{card}_resumes"))
    assert_can_fail([Mutation(PHASE2 / name, old, old.replace("continue", "pass    "),
                              expect_occurrences=1)],
                    lambda: run_pytest(f"{THIS}::{node}", ROOT),
                    f"{card}'s loop redoes a recorded unit")
