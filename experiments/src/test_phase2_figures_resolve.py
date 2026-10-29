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
  when figure / 100 does. A figure written with a minus sign resolves only
  to a negative value; an unsigned one to either sign (prose states
  magnitudes).
- A document whose result file holds other documents' numbers draws only
  on its own part of it (SCOPES in the registry; F166's eight documents).
- From Sprint 29, each sprint's validation document is checked too
  (key "sprints/<name>"). (Last three rules: PR 63 review.)
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

from phase2_figure_registry import REGISTERED, SCOPES, SOURCES  # noqa: E402


@functools.lru_cache(maxsize=1)
def _tracked() -> dict[str, list[Path]]:
    out = subprocess.run(["git", "ls-files", "experiments/results",
                          "experiments/phase2/results"],
                         capture_output=True, text=True, cwd=str(ROOT))
    if out.returncode != 0:
        # Fail, not skip: a skip reads as green with the check gone
        # (PR 63 review).
        pytest.fail(f"cannot enumerate tracked files (git exited "
                    f"{out.returncode}): {out.stderr.strip()[:200]}")
    files: dict[str, list[Path]] = {}
    for line in out.stdout.splitlines():
        if line.endswith(".json"):
            files.setdefault(Path(line).name, []).append(ROOT / line)
    return files


def _select(o, spec: tuple):
    """The parts of `o` at the key path `spec`; "*" is any list item or
    dict key."""
    if not spec:
        yield o
        return
    head, rest = spec[0], spec[1:]
    if head == "*":
        items = o if isinstance(o, list) else \
            o.values() if isinstance(o, dict) else ()
        for v in items:
            yield from _select(v, rest)
    elif isinstance(o, dict) and head in o:
        yield from _select(o[head], rest)


@functools.lru_cache(maxsize=None)
def _values(path: Path, scope: tuple | None = None) -> tuple[float, ...]:
    """Every number in the file, or only under the key paths in `scope`."""
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
                vals.append(float(o))
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        # Name the file: an empty pool would blame the figures instead.
        raise AssertionError(f"{path} is not valid JSON: {exc}") from exc
    for spec in (scope or ((),)):
        for part in _select(doc, spec):
            walk(part)
    return tuple(vals)


def _prose(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " ", text)
    for rule in NOT_FIGURES:
        text = rule.sub(" ", text)
    return text


def _negative(prose: str, start: int) -> bool:
    """A minus sign right before the figure, itself after a space, the
    start or an opening mark. A hyphen after anything else joins words or
    a range ("0.683-0.828", "2.3x-5.3x", "dirac-3.2")."""
    return (start > 0 and prose[start - 1] in "-−"
            and (start == 1 or prose[start - 2].isspace()
                 or prose[start - 2] in "([=:,/"))


def figures(text: str) -> dict[str, bool]:
    """Each figure, as written without its comma, and whether it is ever
    written with "%". A figure written with a minus sign keeps it: "-0.07"
    resolves only to a negative value, while an unsigned figure resolves to
    a value of either sign, since prose states magnitudes ("below by 0.07")
    (PR 63 review: the sign had been dropped on both sides)."""
    out: dict[str, bool] = {}
    prose = _prose(text)
    for m in NUMBER.finditer(prose):
        sign = "-" if _negative(prose, m.start()) else ""
        fig = f"{sign}{m.group(1).replace(',', '')}.{m.group(2)}"
        pct = prose[m.end():m.end() + 2].lstrip().startswith("%")
        out[fig] = out.get(fig, False) or pct
    return out


def _rounds_to(v: float, fig: str) -> bool:
    places = len(fig.split(".")[1])
    return (Decimal(repr(v)).quantize(Decimal(1).scaleb(-places),
                                      ROUND_HALF_UP) == Decimal(fig)
            or f"{v:.{places}f}" == fig)


def resolves(fig: str, pct: bool, pool) -> bool:
    neg = fig.startswith("-")
    mag = fig.lstrip("-")
    # A signed figure needs a negative value; an unsigned one either sign.
    vals = [-v for v in pool if v < 0] if neg else [abs(v) for v in pool]
    if any(_rounds_to(v, mag) for v in vals):
        return True
    if pct:
        places = len(mag.split(".")[1]) + 2
        frac = f"{Decimal(mag) / 100:.{places}f}"
        return any(_rounds_to(v, frac) for v in vals)
    return False


def pool_for(doc: str, text: str) -> list[float]:
    files = _tracked()
    names = {n for n in NAME.findall(text) if n in files}
    names |= set(SOURCES.get(doc, {}))
    scopes = SCOPES.get(doc, {})
    return [v for n in sorted(names) for p in files.get(n, ())
            for v in _values(p, scopes.get(n))]


def unresolved(doc: str, text: str) -> list[str]:
    pool = pool_for(doc, text)
    return sorted((f for f, pct in figures(text).items()
                   if not resolves(f, pct, pool)), key=float)


# Sprint validation documents quote Phase 2 figures too; from Sprint 29 on
# they are checked (PR 63 review: F156's, F158's and F160's figures sat
# there unchecked). Keyed "sprints/<name>".
FIRST_CHECKED_VALIDATION = 29
VALIDATION = re.compile(r"SPRINT_(\d+)_VALIDATION\.md")


def _path(doc: str) -> Path:
    return ROOT / "docs" / doc if doc.startswith("sprints/") else DOCS / doc


def _docs() -> list[str]:
    # Subfolders too (F166's docs/phase2/algorithms/), keyed by the path
    # under docs/phase2, so a top-level document keeps its bare name.
    out = [p.relative_to(DOCS).as_posix() for p in DOCS.rglob("*.md")]
    for p in (ROOT / "docs" / "sprints").glob("SPRINT_*_VALIDATION.md"):
        m = VALIDATION.fullmatch(p.name)
        if m and int(m.group(1)) >= FIRST_CHECKED_VALIDATION:
            out.append(f"sprints/{p.name}")
    return sorted(out)


@pytest.mark.parametrize("doc", _docs())
def test_every_figure_resolves_or_is_registered(doc):
    text = _path(doc).read_text(encoding="utf-8")
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
    texts = {d: _path(d).read_text(encoding="utf-8") for d in _docs()}
    stale = stale_entries(REGISTERED, texts)
    assert not stale, ("registered figures that are no longer quoted, or "
                       f"that now resolve; remove them: {stale}")


def test_a_registered_figure_that_resolves_is_stale():
    doc = "F111_LOKE_PROTOCOL.md"
    texts = {doc: _path(doc).read_text(encoding="utf-8")}
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
    text = _path(doc).read_text(encoding="utf-8")
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


def test_a_minus_sign_is_kept():
    f = figures("mean -0.07 (0.683-0.828, 2.3x-5.3x, dirac-3.2, [-0.04, 0.1])")
    assert f == {"-0.07": False, "0.683": False, "0.828": False, "2.3": False,
                 "5.3": False, "3.2": False, "-0.04": False, "0.1": False}
    assert not resolves("-0.07", False, [0.07])     # the wrong sign
    assert resolves("-0.07", False, [-0.0701])
    assert resolves("0.07", False, [-0.0701])       # a stated magnitude


def test_an_algorithm_document_draws_on_its_own_part():
    # XGBoost's ten-seed mean is in the file, not in HGB's part of it.
    doc = "algorithms/ULB_HGB.md"
    text = _path(doc).read_text(encoding="utf-8") + "\nXGBoost 0.8229\n"
    assert "0.8229" in unresolved(doc, text)
    whole = _values(_tracked()["f166_ulb_algorithms.json"][0])
    assert resolves("0.8229", False, whole)


def test_a_corrupt_result_file_is_named(tmp_path):
    bad = tmp_path / "broken.json"
    bad.write_text("{not json", encoding="utf-8")
    with pytest.raises(AssertionError, match="broken.json is not valid JSON"):
        _values(bad)


def test_sprint_validation_documents_are_checked_from_29():
    docs = _docs()
    assert "sprints/SPRINT_29_VALIDATION.md" in docs
    assert "sprints/SPRINT_28_VALIDATION.md" not in docs


def _fails(path, old, new, node, label):
    from injection import Mutation, assert_can_fail, run_pytest
    assert_can_fail([Mutation(path, old, new, expect_occurrences=1)],
                    lambda: run_pytest(f"{THIS}::{node}", ROOT), label)


def test_the_per_document_pool_can_fail():
    _fails(Path(__file__),
           "    names = {n for n in NAME.findall(text) if n in files}\n",
           "    names = set(files)\n",
           "test_the_wrong_endpoint_fails", "a global pool")


def test_the_sign_check_can_fail():
    _fails(Path(__file__),
           "    vals = [-v for v in pool if v < 0] if neg else "
           "[abs(v) for v in pool]\n",
           "    vals = [abs(v) for v in pool]\n",
           "test_a_minus_sign_is_kept", "a wrong sign resolved")


def test_the_scope_can_fail():
    _fails(Path(__file__),
           "            for v in _values(p, scopes.get(n))]\n",
           "            for v in _values(p)]\n",
           "test_an_algorithm_document_draws_on_its_own_part",
           "another algorithm's figure resolved")


def test_the_corrupt_file_check_can_fail():
    _fails(Path(__file__),
           "        raise AssertionError(f\"{path} is not valid JSON: {exc}\") "
           "from exc\n",
           "        return ()\n",
           "test_a_corrupt_result_file_is_named", "a corrupt file read as empty")


def test_the_validation_scope_can_fail():
    _fails(Path(__file__),
           "        if m and int(m.group(1)) >= FIRST_CHECKED_VALIDATION:\n",
           "        if False:\n",
           "test_sprint_validation_documents_are_checked_from_29",
           "the validation document unchecked")


def test_the_stale_registry_check_can_fail():
    _fails(Path(__file__),
           "        stale += [f\"{doc}: {f}\" for f in reg if f not in live]\n",
           "        stale += []\n",
           "test_a_registered_figure_that_resolves_is_stale",
           "a registered figure that resolves")
