"""F108 (Sprint 27 Task K): the ceiling harness's building blocks.

A small simulated world only; nothing written. The ceiling results are
evidence (`f108_ceiling.json`), not a test. These pin the claim the
harness rests on: the generator's labels follow the exact posterior that
defines the known Bayes error.
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "src"))

import f108_ceiling as fc        # noqa: E402

# Few terminals and many customer-days, so both scenarios are frequent.
SMALL = {"n_customers": 2000, "n_terminals": 500, "n_days": 80}


def _check(seed=1) -> dict:
    d = fc.generate(seed, **SMALL)
    full = d["day"] >= fc.S2_DAYS - 1
    eta = fc.posterior(d["amount"], d["mu"], *fc.world_rates(d, full))
    return fc.generator_check(d["y_main"][full], eta[full])


def test_closed_form_priors_match_a_world_on_average():
    """Over many small worlds the realized rates center on the priors."""
    pt, pq = fc.priors(SMALL["n_customers"], SMALL["n_terminals"])
    rates = []
    for s in range(12):
        d = fc.generate(100 + s, **SMALL)
        rates.append(fc.world_rates(d, d["day"] >= fc.S2_DAYS - 1))
    rt, rq = np.array(rates).T
    assert abs(rt.mean() - pt) < 3 * rt.std(ddof=1) / np.sqrt(len(rt))
    assert abs(rq.mean() - pq) < 3 * rq.std(ddof=1) / np.sqrt(len(rq))


def test_generator_follows_the_exact_posterior():
    c = _check()
    assert c["pass"], c
    assert 0.05 < c["fraud_rate"] < 0.3


def test_generator_check_can_fail():
    from injection import Mutation, assert_can_fail
    src = Path(fc.__file__)

    def run() -> bool:
        importlib.reload(fc)
        return _check()["pass"]

    try:
        assert_can_fail([Mutation(
            src, "f = q * amount_density(amount / S3_MULT, mu) / S3_MULT",
            "f = q * amount_density(amount / S3_MULT, mu) * 1.0",
            expect_occurrences=1)], run, "the multiplier's Jacobian dropped")
    finally:
        importlib.reload(fc)


def test_amount_density_integrates_to_one():
    a = np.linspace(0, 400, 400001)
    for mu in (5.0, 40.0, 100.0):
        g = fc.amount_density(a, np.full_like(a, mu))
        assert abs(np.trapz(g, a) - 1) < 1e-3


def test_hidden_state_is_not_a_feature():
    d = fc.generate(2, **SMALL)
    X = np.column_stack([d["amount"], d["mu"], d["time"]])
    for hidden in ("hidden_s2", "hidden_s3", "terminal"):
        assert not any(np.array_equal(X[:, j], d[hidden])
                       for j in range(X.shape[1]))


def test_reference_labels_are_deterministic_in_amount():
    d = fc.generate(3, **SMALL)
    assert np.array_equal(d["y_ref"], (d["base_amount"] > 220).astype(int))


def test_noise_posterior_matches_flip_rates():
    rng = np.random.default_rng(0)
    y = (rng.uniform(size=400000) < 0.2).astype(int)
    eta = np.full(len(y), 0.2)
    yn, en = fc.add_noise(y, eta, (0.05, 0.01), rng)
    assert abs(yn.mean() - en.mean()) < 3 * np.sqrt(en[0] * (1 - en[0]) / len(y))
    np.testing.assert_allclose(en, 0.95 * 0.2 + 0.01 * 0.8)


def test_floor_fit_recovers_a_planted_floor():
    n = np.array([30, 60, 120, 240, 480, 960])
    f = fc.fit_floor(n, 0.4 * n ** -0.6 + 0.007)
    assert f["fit"] and abs(f["c"] - 0.007) < 1e-4


def test_floor_fit_survives_a_rising_curve():
    """The pilot's reference arm: 1 - AUPRC that does not fall."""
    n = np.array([10, 20, 40, 80, 160, 320])
    f = fc.fit_floor(n, np.array([0.0, 0.001, 0.0, 0.002, 0.001, 0.003]))
    assert f["fit"] and 0 <= f["c"] <= 0.003


def test_recovered_margin():
    assert fc.recovered(0.0104, 0.0100)
    assert not fc.recovered(0.0120, 0.0100)
    assert fc.recovered(0.0004, 0.0)
    assert not fc.recovered(None, 0.01)
