"""The billing rule must keep reproducing the recorded campaign cost.

ceil(sum(runtime)) was a team-lead hypothesis, tested against every retained
job. It matches the recorded total AND the per-job distribution exactly, where
four other candidate rules do not. These tests pin that so a future edit cannot
quietly substitute a rule that merely looks plausible -- which is how the F46
probe came to record a 5.0-second default as if it were a measurement.

Offline: reads the committed ledger, makes no API calls.
"""
from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path

import pytest

import qpu_cost_model as m

LEDGER = Path(__file__).resolve().parents[1] / "results" / "qpu_cost_ledger.json"
RECORDED_TOTAL = 120.0
RECORDED_DISTRIBUTION = {4: 15, 5: 12}


@pytest.fixture(scope="module")
def ledger():
    if not LEDGER.exists():
        pytest.skip("qpu_cost_ledger.json not built yet")
    return json.loads(LEDGER.read_text(encoding="utf-8"))


def _free_tier(ledger):
    """The 27 backfilled free-tier rows the billing rule was validated against.

    Filters on PROVENANCE rather than tier alone: run_metered writes rows with
    the same tier field, so a future free-tier call through it would join this
    set and break the count and the distribution assertions below. Those
    assertions are about the ORIGINAL validation set, not about every row that
    happens to share a tier.
    """
    return [c for c in ledger["calls"]
            if c.get("tier") == "free"
            and c.get("runtime_sum_s") is not None
            and c.get("preprocessing_s") is not None
            and str(c.get("cost_source", "")).startswith("ceil(sum(runtime))")]


def test_the_rule_reproduces_the_recorded_total(ledger):
    calls = _free_tier(ledger)
    assert len(calls) == 27, f"expected the 27 retained free-tier jobs, got {len(calls)}"
    total = sum(m.billed_from_runtime(c["runtime_sum_s"]) for c in calls)
    assert total == RECORDED_TOTAL, (
        f"ceil(sum(runtime)) gives {total}s against the recorded {RECORDED_TOTAL}s. "
        f"The billing rule has drifted or the ledger has.")


def test_the_rule_reproduces_the_per_job_distribution(ledger):
    """The total alone is not enough: two wrong rules can share a total."""
    calls = _free_tier(ledger)
    dist = Counter(int(m.billed_from_runtime(c["runtime_sum_s"])) for c in calls)
    assert dict(dist) == RECORDED_DISTRIBUTION, (
        f"per-job distribution {dict(dist)} against the recorded "
        f"{RECORDED_DISTRIBUTION}")


@pytest.mark.parametrize("name,fn", [
    ("floor(sum)", lambda xs: sum(math.floor(x) for x in xs)),
    ("round(sum)", lambda xs: sum(round(x) for x in xs)),
])
def test_the_rejected_rules_still_fail(ledger, name, fn):
    """Guard the guard: if a rejected rule starts matching, the data changed."""
    rt = [c["runtime_sum_s"] for c in _free_tier(ledger)]
    assert fn(rt) != RECORDED_TOTAL, (
        f"{name} now also reproduces {RECORDED_TOTAL}s, so the validation no "
        f"longer distinguishes the rules")


def test_preprocessing_is_not_billed(ledger):
    """Including preprocessing breaks the match; that is why it is excluded."""
    calls = _free_tier(ledger)
    with_pre = sum(math.ceil(c["runtime_sum_s"] + c["preprocessing_s"]) for c in calls)
    assert with_pre != RECORDED_TOTAL, (
        "including preprocessing_time now matches too, so the claim that it is "
        "unbilled is no longer supported by this evidence")


def test_estimate_declines_to_guess_without_an_anchor(ledger):
    """Criterion H needs an honest 'unknown', not a fabricated number."""
    out = m.estimate_for(n_variables=4000, degree=3, n_samples=8, ledger=ledger)
    assert out["known"] is False, (
        "a degree-3 4000-variable call has no measured anchor; the estimator "
        "must say so rather than extrapolate")


def test_dirac3s_quote_brackets_what_f142_spent():
    """Sprint 26 IMP-5: a quote from measured Dirac-3S per-sample times. At
    B4's 560 variables the range must contain both B4 fits' billed seconds,
    read from the rows, not restated here."""
    a = m.dirac3s_anchors()
    b4 = [x["metered_seconds"] for x in a if x["unit"].startswith("b4_")]
    assert len(b4) >= 2          # a live smoke check; later rows may add more
    q = m.quote(560, 8)
    assert q["known"] and q["device"] == "dirac-3s"
    assert all(q["low_s"] <= s <= q["high_s"] for s in b4), (q, b4)


def _fixture_rows(path: Path) -> Path:
    """Fixed Dirac-3S rows, all at schedule 2, sizes 560 and 833, so the
    tests below do not change when a later run adds rows (PR #21 review)."""
    def row(unit, n, runtime, status="ok"):
        return {"unit": unit, "status": status, "device_type": "dirac-3s",
                "metered_seconds": math.ceil(runtime),
                "hw_config": {"num_samples": 8, "relaxation_schedule": 2},
                "screen": {"n_variables": n},
                "device_timing": {"runtime_sum_s": runtime}}
    path.write_text(json.dumps({"rows": [
        row("x_560", 560, 20.8), row("y_833", 833, 30.6),
        row("z_failed", 560, 99.0, status="failed")]}), encoding="utf-8")
    return path


def test_dirac3s_quote_is_honest_off_its_anchors(tmp_path):
    rows = _fixture_rows(tmp_path / "rows.json")
    assert [a["unit"] for a in m.dirac3s_anchors(rows)] == ["x_560", "y_833"]
    assert m.quote(560, 8, rows_path=rows)["known"] is True
    assert m.quote(3000, 8, rows_path=rows)["known"] is False   # beyond 2x
    assert m.quote(560, 8, relaxation_schedule=4,
                   rows_path=rows)["known"] is False
    above = m.quote(987, 8, rows_path=rows)                     # F143's size
    assert above["above_largest_anchor"] == 833
    assert "floor" in above["note"]
    with pytest.raises(ValueError):
        m.quote(560, 8, device="dirac-4")


def test_an_anchor_beyond_2x_does_not_hide_the_warning(monkeypatch):
    """PR #21 review: the in-range anchors (500, 600) are all smaller than
    a 700-variable job, so the range's high end is a floor. A 2,000-variable
    anchor, outside the range, must not suppress the flag."""
    fake = [{"unit": u, "degree": 2, "n_variables": n,
             "relaxation_schedule": 2, "per_sample_s": s,
             "metered_seconds": 0}
            for u, n, s in (("a", 500, 2.0), ("b", 600, 2.5),
                            ("c", 2000, 9.0))]
    monkeypatch.setattr(m, "dirac3s_anchors", lambda *a, **k: fake)
    q = m.quote(700, 8)
    assert q["known"] and q["above_largest_anchor"] == 600


def test_the_quote_guards_can_fail(tmp_path):
    import importlib

    from injection import Mutation, assert_can_fail
    src = Path(m.__file__)
    rows = _fixture_rows(tmp_path / "rows.json")

    def run() -> bool:
        mod = importlib.reload(m)
        return (mod.quote(560, 8, relaxation_schedule=4,
                          rows_path=rows)["known"] is False
                and "above_largest_anchor" in mod.quote(987, 8,
                                                        rows_path=rows))

    try:
        assert_can_fail([Mutation(src, "               if a[\"relaxation_"
                                  "schedule\"] == relaxation_schedule]",
                                  "               ]", expect_occurrences=1)],
                        run, "schedule ignored")
        assert_can_fail([Mutation(src, "    if q[\"known\"] and n_variables "
                                  "> max(sizes):", "    if False:",
                                  expect_occurrences=1)],
                        run, "no flag above the largest anchor")
    finally:
        importlib.reload(m)


def test_estimate_uses_an_anchor_when_one_exists(ledger):
    out = m.estimate_for(n_variables=100, degree=2, n_samples=8, ledger=ledger)
    assert out["known"] is True
    assert out["low_s"] <= out["high_s"]
    assert out["high_s"] > 0
