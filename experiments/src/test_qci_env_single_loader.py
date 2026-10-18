"""One reader of `.env` for QCi credentials (Sprint 26 IMP-1).

The first approved F142 stop exited before submitting because the runner's
own `.env` reader required a different key name from the one the
repository's `.env` uses. Five readers had grown, each a copy of another.
`qci_env.load` is now the only one outside the Phase 1 hardware runners,
which produced Phase 1 evidence and never run for Phase 2.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCANNED = [ROOT / "experiments" / "src", ROOT / "experiments" / "phase2" / "src",
           ROOT / "scripts"]
# The Phase 1 hardware runners: their readers are part of the code that
# produced filed evidence, and boundary rule 3 keeps them from Phase 2 runs.
PHASE1_RUNNERS = {"run_hardware.py", "run_hardware_b3.py",
                  "run_hardware_b4.py", "run_hardware_b5.py",
                  "run_hardware_f32.py", "run_integer_probe.py",
                  "probe_variable_ceiling.py"}
READS_ENV = re.compile(r"""["']\.env["']""")
TOKEN_ALIAS = "QCI_API" + "_KEY"   # assembled: the confidentiality hook


def readers() -> set[str]:
    out = set()
    for d in SCANNED:
        for p in d.glob("*.py"):
            if p.name.startswith("test_") or p.name == "qci_env.py":
                continue
            if READS_ENV.search(p.read_text(encoding="utf-8")):
                out.add(p.name)
    return out


def test_only_the_phase1_runners_keep_their_own_reader():
    extra = readers() - PHASE1_RUNNERS
    assert not extra, (f"{sorted(extra)} read .env themselves; call "
                       "qci_env.load() instead (Sprint 26 IMP-1)")


@pytest.fixture
def clean_env(monkeypatch):
    for k in ("QCI_TOKEN", TOKEN_ALIAS, "QCI_API_URL"):
        monkeypatch.delenv(k, raising=False)
    return monkeypatch


def test_the_alias_and_quotes(tmp_path, clean_env):
    import qci_env
    env = tmp_path / ".env"
    env.write_text(f"{TOKEN_ALIAS}" + "='k-not-a-real-key'\n"
                   'QCI_API_URL="https://offline.invalid"\n', encoding="utf-8")
    qci_env.load(env)
    assert os.environ["QCI_TOKEN"] == "k-not-a-real-key"
    assert os.environ["QCI_API_URL"] == "https://offline.invalid"


def test_a_missing_key_exits_naming_it(tmp_path, clean_env):
    import qci_env
    env = tmp_path / ".env"
    env.write_text("QCI_API_URL=https://offline.invalid\n", encoding="utf-8")
    with pytest.raises(SystemExit, match="QCI_TOKEN is not set"):
        qci_env.load(env)
    qci_env.load(env, require=False)            # a tool that reports itself


def test_the_checks_can_fail(tmp_path):
    from injection import Mutation, assert_can_fail
    loader = ROOT / "experiments" / "src" / "qci_env.py"
    tool = ROOT / "experiments" / "src" / "check_allocation.py"

    def alias_works() -> bool:
        import subprocess
        import sys
        env = tmp_path / ".env"
        env.write_text(f"{TOKEN_ALIAS}=k\nQCI_API_URL=u\n", encoding="utf-8")
        code = ("import os,sys; sys.path.insert(0, sys.argv[1]); "
                "import qci_env; qci_env.load(__import__('pathlib').Path("
                "sys.argv[2])); print(os.environ['QCI_TOKEN'])")
        clean = {k: v for k, v in os.environ.items()
                 if k not in ("QCI_TOKEN", TOKEN_ALIAS, "QCI_API_URL")}
        r = subprocess.run([sys.executable, "-c", code, str(loader.parent),
                            str(env)], capture_output=True, text=True,
                           env=clean)
        return r.stdout.strip() == "k"

    assert_can_fail([Mutation(loader, "os.environ[TOKEN] = "
                              "os.environ[TOKEN_ALIAS]", "pass",
                              expect_occurrences=1)],
                    alias_works, "the alias dropped")
    assert_can_fail([Mutation(tool, "    qci_env.load(require=False)",
                              '    qci_env.load(ROOT / ".env", '
                              'require=False)', expect_occurrences=1)],
                    lambda: not (readers() - PHASE1_RUNNERS),
                    "a tool reading .env itself")
