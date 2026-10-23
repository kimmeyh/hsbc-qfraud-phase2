"""Every device job is stored in full, and every Phase 2 pool can be rebuilt.

Sprint 28 D4 (team lead, 2026-10-23): F142's Dirac-3 B4 lane lost its
per-row scores, and its unseeded pool means they can never be rebuilt. Two
static guards, each with a frozen list of what predates the rule:

1. A Phase 2 module that submits to a device goes through
   `device_store.saving` and `device_store.require_saved`. No new module
   under `experiments/src` may submit: Phase 1's runners are frozen, and new
   device runners live under `experiments/phase2/src`.
2. A Phase 2 pool build (`build_pool`, `build_full`, `QBoostClassifier`)
   passes `qubo_proxy.seeded_weak_params`. Modules from before the rule keep
   their counted exemption; a count can fall, never rise.

The runtime half (hash check before sending, refusal of an unseeded pool,
the save itself) is `test_device_store.py`.
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PHASE2 = ROOT / "experiments" / "phase2" / "src"
PHASE1 = ROOT / "experiments" / "src"

SUBMIT = re.compile(r"metered_fit\(|CloudSolver|process_job\(|"
                    r"eqc_submit\.device\(|QciClient\(")

# Phase 2 modules that match SUBMIT without submitting a stored job.
PHASE2_NOT_SUBMITTING = {
    "device_store.py": "the store itself",
    "dirac3_emulator.py": "a local stand-in for the cloud solver; sends nothing",
    "recover_device_samples.py": "reads finished jobs (get_job_results) only",
}
# Phase 2 device runners from before the rule. Never add to this.
PHASE2_SUBMIT_BEFORE_RULE = {
    "run_dirac3s_verify.py": "F142, complete; saves its raw response in "
                             "its own makeResults, the code device_store lifts",
}
# Phase 1 modules that match SUBMIT (runners, the wrapper, read-only tools).
# Frozen at 10 on 2026-10-23. Never add to this.
PHASE1_FROZEN = frozenset({
    "check_allocation.py", "eqc_submit.py", "integer_path.py", "job_query.py",
    "probe_variable_ceiling.py", "run_hardware.py", "run_hardware_b3.py",
    "run_hardware_b4.py", "run_hardware_b5.py", "run_integer_probe.py",
})
PHASE1_FROZEN_COUNT = 10

POOL_CALLS = {"build_pool", "build_full", "QBoostClassifier"}
# Unseeded pool builds per module on 2026-10-23, before the rule. A count
# may fall, never rise; a module not listed must have none.
UNSEEDED_BEFORE_RULE = {
    "emulator_sparsity.py": (1, "F17 emulator study; pools from Phase 1 configs"),
    "exp3_controls.py": (1, "F94 controls; must be seeded before any Experiment 3 device run"),
    "f111_loke_protocol.py": (1, "KNN learners; no random state to seed"),
    "f130_levers.py": (1, "its weak_params helper returns seeded params for tree learners"),
    "f144_proxy_twin.py": (1, "unseeded by design on the arm that measures Phase 1 drift"),
    "full_pair_pool.py": (1, "a builder; passes its caller's params through"),
    "lever_screen.py": (4, "F124 screens, before F145"),
    "run_dirac3s_verify.py": (1, "cfg from _data, which uses seeded_weak_params"),
    "sample_size.py": (1, "F29, before F145"),
    "soft_votes.py": (3, "F20, before F145"),
    "validate_emulator.py": (1, "F17 emulator study; pools from Phase 1 configs"),
}
UNSEEDED_FROZEN_TOTAL = 16


def _modules(d: Path):
    return sorted(p for p in d.glob("*.py") if not p.name.startswith("test_"))


def _unseeded_pool_calls(src: str) -> int:
    n = 0
    for node in ast.walk(ast.parse(src)):
        if not isinstance(node, ast.Call):
            continue
        f = node.func
        name = f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", None)
        if name not in POOL_CALLS:
            continue
        kw = [k for k in node.keywords if k.arg in ("weak_params", "weak_cls_params")]
        seg = ast.get_source_segment(src, kw[0].value) if kw else ""
        if "seeded_weak_params" not in (seg or ""):
            n += 1
    return n


def test_phase2_device_runners_store_every_job():
    bad = []
    for p in _modules(PHASE2):
        src = p.read_text(encoding="utf-8")
        if not SUBMIT.search(src) or p.name in PHASE2_NOT_SUBMITTING \
                or p.name in PHASE2_SUBMIT_BEFORE_RULE:
            continue
        if "device_store.saving(" not in src or "device_store.require_saved(" not in src:
            bad.append(p.name)
    assert not bad, (f"{bad} submit to a device without device_store.saving "
                     "and device_store.require_saved")


def test_no_new_phase1_module_submits():
    found = {p.name for p in _modules(PHASE1)
             if SUBMIT.search(p.read_text(encoding="utf-8"))}
    new = found - PHASE1_FROZEN
    assert not new, (f"{sorted(new)} submit from experiments/src; new device "
                     "runners go in experiments/phase2/src, through device_store")
    assert len(PHASE1_FROZEN) == PHASE1_FROZEN_COUNT


def test_frozen_lists_only_shrink():
    assert len(PHASE2_SUBMIT_BEFORE_RULE) <= 1
    assert sum(n for n, _ in UNSEEDED_BEFORE_RULE.values()) <= UNSEEDED_FROZEN_TOTAL
    for name in list(PHASE2_NOT_SUBMITTING) + list(PHASE2_SUBMIT_BEFORE_RULE) \
            + list(UNSEEDED_BEFORE_RULE):
        assert (PHASE2 / name).exists(), f"{name} is gone; remove it from the list"


def test_phase2_pool_builds_are_seeded():
    bad = []
    for p in _modules(PHASE2):
        n = _unseeded_pool_calls(p.read_text(encoding="utf-8"))
        allowed = UNSEEDED_BEFORE_RULE.get(p.name, (0, ""))[0]
        if n > allowed:
            bad.append(f"{p.name}: {n} unseeded, {allowed} allowed")
    assert not bad, ("pool builds without qubo_proxy.seeded_weak_params "
                     f"cannot be rebuilt: {bad}")


def test_the_scan_sees_an_unseeded_build():
    src = ("clf = qp.build_pool(X, y, 2, 'dct', 'sequential')\n"
           "c2 = fpp.build_full(X, y, 2, 'dct', weak_params={'max_depth': 1})\n"
           "c3 = qp.build_pool(X, y, 2, 'dct', 'full', "
           "weak_params=qp.seeded_weak_params(42))\n")
    assert _unseeded_pool_calls(src) == 2
