"""The one reader of the repository's `.env` for QCi credentials.

Sprint 26 IMP-1. This repository had at least five `.env` readers, and they
did not accept the same key names: `run_hardware.py` took `QCI_API_KEY` as
the token, while the F142 runner, copied from `run_hardware_b4.py`, required
`QCI_TOKEN`. The repository's `.env` uses `QCI_API_KEY`, so the first
approved F142 stop exited before submitting. It spent nothing, and it cost
an approval round.

A module of its own, with no imports beyond the standard library, so a
small tool can use it without loading eqc-models. Never prints a value.

The Phase 1 hardware runners keep their own readers: they are the code that
produced Phase 1 evidence, and they never run for Phase 2
(`test_qci_env_single_loader.py` lists them).
"""
from __future__ import annotations

import os
from pathlib import Path

ENV = Path(__file__).resolve().parents[2] / ".env"
TOKEN, URL = "QCI_TOKEN", "QCI_API_URL"
TOKEN_ALIAS = "QCI_API" + "_KEY"     # run_hardware.py's convention


def load(env: Path | None = None, require: bool = True) -> None:
    """Load `.env` into the environment without overriding what is set.

    Quotes around a value are stripped. The alias is accepted as the token.
    With `require`, a missing token or URL exits naming the key, never its
    value.
    """
    env = env or ENV
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(),
                                      v.strip().strip('"').strip("'"))
    if not os.environ.get(TOKEN) and os.environ.get(TOKEN_ALIAS):
        os.environ[TOKEN] = os.environ[TOKEN_ALIAS]
    if require:
        for k in (TOKEN, URL):
            if not os.environ.get(k):
                raise SystemExit(f"{k} is not set (in the environment or "
                                 f"{env}); {TOKEN_ALIAS} is accepted as "
                                 "the token.")
