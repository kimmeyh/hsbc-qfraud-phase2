"""Every figure quoted in docs/phase2 resolves to evidence or is registered.

F164 (Sprint 29 Task C, #66; team lead Decision 1 option 1). F44
(`test_document_figures_resolve.py`) checks only the submitted papers.
Seven PR #46 findings were figures or labels in docs/phase2 and the
validation document that the result files do not support.

WHY PER-DOCUMENT POOLS. F44 resolves a figure against ONE pool of every
stored value. The tracked result files hold about 145,000 numbers; rounded
to the quoted places they cover all of the 2-place grid and 99.4% of the
3-place grid in [0, 1) (Sprint 29 planning probe). One pool therefore
accepts almost any figure quoted to 1-3 places, and the wrong endpoint
0.829 from the PR #46 review resolved in it. Here a figure resolves only
against the tracked result files its OWN document names (by file name,
anywhere in its text), plus any listed in SOURCES with a reason. In
F111_LOKE_PROTOCOL.md's pool 0.829 does not resolve and 0.828 does.

RULES.
- A figure is a decimal outside code (F44's extraction), with a thousands
  comma kept ("2,553.5" is 2553.5). Not figures: dotted versions
  ("0.21.0"), arXiv identifiers, and section or table numbers
  ("section 5.3"). Wall-clock keys are not evidence (F44's timing rule).
- A figure resolves when a pool value rounds to it at its quoted places,
  half up or as Python formats it. A figure written with "%" also resolves
  when figure / 100 does.
- Anything else is REGISTERED once per document with a reason: a quote
  from an outside source, a figure derived from stored values (the reason
  says how, and the derived ones were recomputed when registered,
  2026-10-26), or a projection or setting.

WHAT THIS DOES NOT CATCH. F44's limit stands: a figure that exists in the
cited files but is quoted in the wrong place passes; that needs per-claim
provenance (F39). A registered figure is not checked for correctness. Of
the seven PR #46 findings that motivated F164, only 0.829 is a decimal.
The other six are out of this check's reach: F111's unrecorded 95-minute
wall clock and the "776 of 950" label are integers, and F110's clamp cause,
F151's second failing reason, F114's scope and F146 P1 listed open are
prose.
"""
from __future__ import annotations

import functools
import json
import re
import subprocess
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs" / "phase2"
THIS = Path(__file__).relative_to(ROOT).as_posix()
TIMING_KEYS = {"elapsed_s", "elapsed_sec"}
NAME = re.compile(r"[\w.-]+\.json")
NUMBER = re.compile(r"(?<![\d.,])(\d{1,3}(?:,\d{3})+|\d+)\.(\d+)(?![\d])")
NOT_FIGURES = (
    re.compile(r"\d+\.\d+\.\d+"),                          # versions
    re.compile(r"arXiv:\s*\d+\.\d+(?:v\d+)?", re.I),        # identifiers
    re.compile(r"\b(?:sections?|tables?)\s+\d+\.\d+", re.I),
)

from phase2_figure_registry import REGISTERED, SOURCES  # noqa: E402


@functools.lru_cache(maxsize=1)
def _tracked() -> dict[str, list[Path]]:
    out = subprocess.run(["git", "ls-files", "experiments/results",
                          "experiments/phase2/results"],
                         capture_output=True, text=True, cwd=str(ROOT))
    if out.returncode != 0:
        pytest.skip(f"cannot enumerate tracked files (git exited "
                    f"{out.returncode}): {out.stderr.strip()[:200]}")
    files: dict[str, list[Path]] = {}
    for line in out.stdout.splitlines():
        if line.endswith(".json"):
            files.setdefault(Path(line).name, []).append(ROOT / line)
    return files


@functools.lru_cache(maxsize=None)
def _values(path: Path) -> tuple[float, ...]:
    vals: list[float] = []

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k not in TIMING_KEYS:
                    walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
        elif isinstance(o, (int, float)) and not isinstance(o, bool):
            if abs(float(o)) < 1e12:
                vals.append(abs(float(o)))
    try:
        walk(json.loads(path.read_text(encoding="utf-8")))
    except ValueError:
        pass
    return tuple(vals)


def _prose(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " ", text)
    for rule in NOT_FIGURES:
        text = rule.sub(" ", text)
    return text


def figures(text: str) -> dict[str, bool]:
    """Each figure, as written without its comma, and whether it is ever
    written with "%"."""
    out: dict[str, bool] = {}
    prose = _prose(text)
    for m in NUMBER.finditer(prose):
        fig = f"{m.group(1).replace(',', '')}.{m.group(2)}"
        pct = prose[m.end():m.end() + 2].lstrip().startswith("%")
        out[fig] = out.get(fig, False) or pct
    return out


def _rounds_to(v: float, fig: str) -> bool:
    places = len(fig.split(".")[1])
    return (Decimal(repr(v)).quantize(Decimal(1).scaleb(-places),
                                      ROUND_HALF_UP) == Decimal(fig)
            or f"{v:.{places}f}" == fig)


def resolves(fig: str, pct: bool, pool) -> bool:
    if any(_rounds_to(v, fig) for v in pool):
        return True
    if pct:
        places = len(fig.split(".")[1]) + 2
        frac = f"{Decimal(fig) / 100:.{places}f}"
        return any(_rounds_to(v, frac) for v in pool)
    return False


def pool_for(doc: str, text: str) -> list[float]:
    files = _tracked()
    names = {n for n in NAME.findall(text) if n in files}
    names |= set(SOURCES.get(doc, {}))
    return [v for n in sorted(names) for p in files.get(n, ())
            for v in _values(p)]


def unresolved(doc: str, text: str) -> list[str]:
    pool = pool_for(doc, text)
    return sorted((f for f, pct in figures(text).items()
                   if not resolves(f, pct, pool)), key=float)


def _docs() -> list[str]:
    return sorted(p.name for p in DOCS.glob("*.md"))


@pytest.mark.parametrize("doc", _docs())
def test_every_figure_resolves_or_is_registered(doc):
    text = (DOCS / doc).read_text(encoding="utf-8")
    reg = REGISTERED.get(doc, {})
    bad = [f for f in unresolved(doc, text) if f not in reg]
    assert not bad, (
        f"{doc} quotes {len(bad)} figure(s) that resolve to no value in the "
        f"result files it names and are not registered: {bad}. Either the "
        "figure is wrong, or the document should name its result file, or "
        "it belongs in phase2_figure_registry.py with a reason.")


def stale_entries(registered: dict, texts: dict[str, str]) -> list[str]:
    """Registered figures no longer quoted, or that now resolve."""
    stale = []
    for doc, reg in registered.items():
        if doc not in texts:
            stale.append(f"{doc}: no such document")
            continue
        live = set(unresolved(doc, texts[doc]))
        stale += [f"{doc}: {f}" for f in reg if f not in live]
    return stale


def test_the_registry_holds_only_live_unresolved_figures():
    texts = {d: (DOCS / d).read_text(encoding="utf-8") for d in _docs()}
    stale = stale_entries(REGISTERED, texts)
    assert not stale, ("registered figures that are no longer quoted, or "
                       f"that now resolve; remove them: {stale}")


def test_a_registered_figure_that_resolves_is_stale():
    doc = "F111_LOKE_PROTOCOL.md"
    texts = {doc: (DOCS / doc).read_text(encoding="utf-8")}
    assert stale_entries({doc: {"0.828": "resolves in its own pool"}},
                         texts) == [f"{doc}: 0.828"]
    assert stale_entries({"NOPE.md": {}}, texts) == ["NOPE.md: no such document"]


def test_every_entry_has_a_reason():
    for table in (REGISTERED, SOURCES):
        for doc, entries in table.items():
            for key, why in entries.items():
                assert isinstance(why, str) and len(why.strip()) >= 10, (
                    doc, key)
    files = _tracked()
    for doc, srcs in SOURCES.items():
        for name in srcs:
            assert name in files, f"{doc}: SOURCES names {name}, not tracked"


def test_the_wrong_endpoint_fails():
    """F164's motivating finding, put back. 0.828 resolves in F111's own
    pool; 0.829 does not, though it resolves in a pool of every file."""
    doc = "F111_LOKE_PROTOCOL.md"
    text = (DOCS / doc).read_text(encoding="utf-8")
    assert "0.683-0.828" in text
    assert "0.828" not in unresolved(doc, text)
    broken = text.replace("0.683-0.828", "0.683-0.829", 1)
    assert "0.829" in unresolved(doc, broken)
    everything = [v for ps in _tracked().values() for p in ps
                  for v in _values(p)]
    assert resolves("0.829", False, everything), (
        "0.829 no longer resolves globally, so this test no longer shows "
        "why the pool is per document")


def test_extraction_rules():
    f = figures("seen 2,553.5 and 7.56% then 0.21.0, arXiv:2306.03481, "
                "section 5.3, `0.9` and 0.42")
    assert f == {"2553.5": False, "7.56": True, "0.42": False}
    assert resolves("7.56", True, [0.0756])
    assert not resolves("7.56", False, [0.0756])
    assert resolves("0.828", False, [0.82849])
    assert not resolves("0.829", False, [0.82849])


def _fails(path, old, new, node, label):
    from injection import Mutation, assert_can_fail, run_pytest
    assert_can_fail([Mutation(path, old, new, expect_occurrences=1)],
                    lambda: run_pytest(f"{THIS}::{node}", ROOT), label)


def test_the_per_document_pool_can_fail():
    _fails(Path(__file__),
           "    names = {n for n in NAME.findall(text) if n in files}\n",
           "    names = set(files)\n",
           "test_the_wrong_endpoint_fails", "a global pool")


def test_the_stale_registry_check_can_fail():
    _fails(Path(__file__),
           "        stale += [f\"{doc}: {f}\" for f in reg if f not in live]\n",
           "        stale += []\n",
           "test_a_registered_figure_that_resolves_is_stale",
           "a registered figure that resolves")
