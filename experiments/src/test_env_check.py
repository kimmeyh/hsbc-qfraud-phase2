"""F177 change f: `scripts/env_check.py` marks a measurement above its
idle range SLOW and reports without gating. Each rule is proven red."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
THIS = Path(__file__).relative_to(ROOT).as_posix()
SRC = ROOT / "scripts" / "env_check.py"
sys.path.insert(0, str(ROOT / "scripts"))

import env_check as ec  # noqa: E402


def test_a_value_above_the_idle_range_is_slow():
    assert ec.verdict(0.7, (0.6, 0.7)) == "ok"
    assert ec.verdict(0.71, (0.6, 0.7)) == "SLOW"
    assert ec.verdict(0.1, (0.6, 0.7)) == "ok"


def test_the_report_never_gates(monkeypatch, capsys):
    monkeypatch.setattr(ec, "fresh", lambda code: 99.0)
    monkeypatch.setattr(ec, "stat_ms", lambda n=0: 99.0)
    assert ec.main([]) == 0
    out = capsys.readouterr().out
    assert out.count("SLOW") == 3 and "idle 18.0-22.0 on 2026-11-05" in out
    assert ec.main(["--json"]) == 0


def test_the_idle_ranges_are_f180s():
    assert ec.CHECKS["python start"][1] == (0.6, 0.7)
    assert ec.CHECKS["import numpy, pandas, sklearn"][1] == (18.0, 22.0)
    assert ec.STAT_IDLE_MS == (3.0, 9.0)


def test_the_rules_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    assert_can_fail([Mutation(SRC, '    return "SLOW" if value > idle[1] else "ok"\n',
                              '    return "ok"\n', expect_occurrences=1)],
                    lambda: run_pytest(f"{THIS}::test_a_value_above_the_idle_"
                                       "range_is_slow", ROOT),
                    "a slow machine reported as ok")
