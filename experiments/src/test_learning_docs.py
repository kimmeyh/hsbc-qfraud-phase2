"""The three learning documents link, define and cite as their rules say.

F178 (Sprint 31 Task K, #103). `docs/learning/` holds three versions of
what this project has learned about machine learning, quantum machine
learning and quantum computing: a plain-terms version (Doc 1), one for
machine learning experts (Doc 2) and one for quantum computing experts
(Doc 3). They are updated every sprint, so their links, definitions and
citations drift unless a test holds them.

THE CONVENTIONS THIS TEST ENFORCES (each document states them too).

- Anchors are explicit: `<a id="kind-name"></a>` at the start of an
  appendix entry, `**Label**: text` after it. A link fragment must name
  such an id in a learning document; fragments into other documents are
  refused, because a heading slug is not stable.
- Acronyms: a token of capitals and digits with at least two capitals
  ("AUPRC", "GA2M", "IEEE-CIS"; a trailing plural "s" is allowed). Every
  acronym used in any of the three documents has an `acr-` entry in
  Doc 1's acronym appendix, and only there. Every use, in all three
  documents, is a link whose text is the acronym and whose target is
  that entry. In Doc 1 the first use in the body is spelled out: the
  text before it ends with the entry's expansion and " (". An entry
  whose text starts "Name, not an acronym" is a proper name written in
  capitals (SPECTRA) and is not spelled out. Bracketed evidence tags
  ([HW], [SIM], [PROJ]) are not acronyms. Headings are not uses; an
  acronym in a heading still needs an entry.
- Terms: every other appendix entry. A term's first use in a document's
  body (before its first "## Appendix" heading, headings and code
  excluded) links to its entry. Doc 2 and Doc 3 link to Doc 1's
  entries; each defines only what Doc 1 lacks, and Doc 3 only what Doc 1
  and Doc 2 lack.
- Claims: a section whose heading contains "What our experiments
  showed" holds only claim bullets. Each starts with an evidence tag and
  ends with a parenthesis of backticked repository paths, each a tracked
  file outside `docs/learning/`. Every decimal figure in the bullet must
  be in one of those sources: written in a cited markdown document, or
  resolving in a cited result file under `test_phase2_figures_resolve`'s
  rules.
- Outside claims: a section whose heading contains "What outside
  research says" holds only bullets, each naming an EvidenceBasedDB
  entry with its grade (EvidenceBasedDB `id`, high) or a web source.

WHAT THIS DOES NOT CATCH. Integers in claims are not checked (the
figure rule reads decimals, as F44 and F164 do). A figure that is in a
cited source but quoted for the wrong thing passes. EvidenceBasedDB ids
are checked for form only: the store is outside this repository, so CI
cannot open it; `scripts/edb_query.py show <id>` checks one by hand.
Reading level is not measured. A term used before its entry exists is
not found; only defined terms are checked.
"""
from __future__ import annotations

import functools
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

import pytest

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs" / "learning"
THIS = Path(__file__).relative_to(ROOT).as_posix()
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_phase2_figures_resolve import _values, figures, resolves  # noqa: E402

STEM = "ML QML and QC Understandings about Quantum Advantage - "
DOC1 = STEM + "Laymen terms.md"
DOC2 = STEM + "ML Expert.md"
DOC3 = STEM + "QC Expert.md"
ORDER = (DOC1, DOC2, DOC3)

ANCHOR = re.compile(r'<a id="([a-z0-9-]+)"></a>')
ENTRY = re.compile(r'^- <a id="([a-z0-9-]+)"></a>\*\*([^*]+)\*\*:\s*(.*)$',
                   re.S)
SEGMENT = re.compile(
    r"(?P<code>`[^`]*`)"
    r"|(?P<tag>\[(?:HW|SIM|PROJ)(?:, ?(?:HW|SIM|PROJ))*\](?!\())"
    r"|(?P<link>\[(?P<text>[^\]]*)\]\((?P<target>[^)\s]*)\))"
    r"|(?P<url>https?://\S+)"
    r"|(?P<html><[^>]+>)")
ACRONYM = re.compile(
    r"(?<![\w])([A-Z][A-Z0-9]*[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*)s?(?![\w])")
HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
TAG = re.compile(r"^- \[(?:HW|SIM|PROJ)(?:, ?(?:HW|SIM|PROJ))*\] ")
PATHS = re.compile(r"\((`[^`]+`(?:,\s*`[^`]+`)*)\)\.?$")
OUTSIDE_SOURCE = re.compile(
    r"EvidenceBasedDB `[a-z0-9-]+`, (?:high|moderate|low|very-low)"
    r"|\]\(https?://")
CLAIMS = "what our experiments showed"
OUTSIDE = "what outside research says"
NAME_ONLY = "name, not an acronym"


# ---------------------------------------------------------------- parsing

def slug(token: str) -> str:
    return "acr-" + re.sub(r"[^a-z0-9]+", "-", token.lower()).strip("-")


def segments(line: str) -> list[tuple[str, str, str]]:
    """(kind, visible text, link target) for each part of one line.
    Kinds: plain, link, code, tag, url, html."""
    out, pos = [], 0
    for m in SEGMENT.finditer(line):
        if m.start() > pos:
            out.append(("plain", line[pos:m.start()], ""))
        kind = m.lastgroup if m.lastgroup not in ("text", "target") else "link"
        if m.group("link"):
            out.append(("link", m.group("text"), m.group("target")))
        else:
            out.append((kind, m.group(0), ""))
        pos = m.end()
    if pos < len(line):
        out.append(("plain", line[pos:], ""))
    return out


def lines_of(text: str):
    """(line number, line, is heading, in body) outside fenced code."""
    fenced, body = False, True
    for n, line in enumerate(text.splitlines(), 1):
        if line.startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        h = HEADING.match(line)
        if h and len(h.group(1)) == 2 and h.group(2).startswith("Appendix"):
            body = False
        yield n, line, bool(h), body


def bullets(lines: list[str]) -> list[str]:
    """Join each "- " bullet with its indented continuation lines."""
    out: list[str] = []
    for line in lines:
        if line.startswith("- "):
            out.append(line)
        elif line.startswith("  ") and out and line.strip():
            out[-1] += " " + line.strip()
    return out


def entries(text: str) -> list[tuple[str, str, str]]:
    """(id, label, text) for every anchored appendix entry."""
    app = [ln for _, ln, _, body in lines_of(text) if not body]
    out = []
    for b in bullets(app):
        m = ENTRY.match(b)
        if m:
            out.append((m.group(1), m.group(2).strip(), m.group(3).strip()))
    return out


def sections(text: str, key: str) -> list[tuple[str, list[str]]]:
    """(heading, lines) for each section whose heading contains `key`,
    up to the next heading of the same or a higher level."""
    out, cur, level = [], None, 0
    for _, line, is_h, _ in lines_of(text):
        h = HEADING.match(line) if is_h else None
        if h:
            if cur is not None and len(h.group(1)) <= level:
                cur = None
            if key in h.group(2).lower():
                cur, level = [], len(h.group(1))
                out.append((h.group(2), cur))
                continue
        if cur is not None:
            cur.append(line)
    return out


def _strip_label(line: str) -> str:
    """An acronym entry's own bold label is its definition, not a use."""
    return re.sub(r'(<a id="acr-[^"]+"></a>)\*\*[^*]+\*\*', r"\1", line)


def acronym_entries(docs: dict[str, str]) -> dict[str, tuple[str, str]]:
    """Token -> (expansion, entry text) from Doc 1's acronym appendix."""
    out = {}
    for aid, label, body in entries(docs[DOC1]):
        if aid.startswith("acr-"):
            out[label] = (_visible(body).split(". ")[0].rstrip("."), body)
    return out


def _visible(text: str) -> str:
    return "".join(t for k, t, _ in segments(text)
                   if k in ("plain", "link", "tag")).replace("*", "")


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()


def _split(target: str, doc: str) -> tuple[str, str]:
    """A link target as (learning-doc name or repository path, fragment)."""
    path, _, frag = target.partition("#")
    path = unquote(path)
    if not path:
        return doc, frag
    if path in ORDER:
        return path, frag
    return (Path("docs/learning") / path).as_posix(), frag


def _resolve(p: str) -> str:
    parts: list[str] = []
    for part in p.split("/"):
        if part == "..":
            if parts:
                parts.pop()
        elif part not in ("", "."):
            parts.append(part)
    return "/".join(parts)


# ----------------------------------------------------------------- checks

def link_problems(docs: dict[str, str], tracked: set[str]) -> list[str]:
    """Each problem is "kind: where: what"; kinds are anchor (a fragment
    in the same document), file (a missing target) and cross-anchor (a
    fragment in another document)."""
    ids = {d: set(ANCHOR.findall(t)) for d, t in docs.items()}
    out = []
    for doc, text in docs.items():
        for n, line, _, _ in lines_of(text):
            for kind, _, target in segments(line):
                if kind != "link" or target.startswith(("http://",
                                                        "https://")):
                    continue
                path, frag = _split(target, doc)
                where = f"{doc}:{n}"
                if path in ORDER:
                    if frag and frag not in ids[path]:
                        k = "anchor" if path == doc else "cross-anchor"
                        out.append(f"{k}: {where}: no id {frag!r} in {path}")
                elif _resolve(path) not in tracked:
                    out.append(f"file: {where}: {target} is not a tracked "
                               "file or a learning document")
                elif frag:
                    out.append(f"anchor: {where}: fragment into {path}; "
                               "only learning-document ids are stable")
    return out


def duplicate_id_problems(docs: dict[str, str]) -> list[str]:
    out = []
    for doc, text in docs.items():
        seen: set[str] = set()
        for i in ANCHOR.findall(text):
            if i in seen:
                out.append(f"{doc}: id {i!r} defined twice")
            seen.add(i)
    return out


def _uses(doc: str, text: str):
    """(line, is heading, in body, segment kind, token, target)."""
    for n, line, is_h, body in lines_of(text):
        for kind, vis, target in segments(_strip_label(line)):
            if kind not in ("plain", "link"):
                continue
            for m in ACRONYM.finditer(vis):
                yield n, is_h, body, kind, m.group(1), target, vis


def acronym_entry_problems(docs: dict[str, str]) -> list[str]:
    known = acronym_entries(docs)
    out = []
    for doc, text in docs.items():
        if doc != DOC1:
            out += [f"{doc}: acronym entry {aid!r}; acronyms live in Doc 1"
                    for aid, _, _ in entries(text) if aid.startswith("acr-")]
        for n, _, _, _, token, _, _ in _uses(doc, text):
            if token not in known:
                out.append(f"{doc}:{n}: {token} has no entry in Doc 1's "
                           "acronym appendix")
    return out


def acronym_link_problems(docs: dict[str, str]) -> list[str]:
    known = acronym_entries(docs)
    out = []
    for doc, text in docs.items():
        for n, is_h, _, kind, token, target, vis in _uses(doc, text):
            if is_h or token not in known:
                continue
            path, frag = _split(target, doc) if kind == "link" else ("", "")
            ok = (kind == "link" and vis.strip() in (token, token + "s")
                  and path == DOC1 and frag == slug(token))
            if not ok:
                out.append(f"{doc}:{n}: {token} is not a link to its entry")
    return out


def spelled_out_problems(docs: dict[str, str]) -> list[str]:
    """Doc 1: the body's first use of each acronym follows its expansion."""
    known = acronym_entries(docs)
    seen: set[str] = set()
    out = []
    before = ""
    for n, line, is_h, body in lines_of(docs[DOC1]):
        if not body or is_h:
            continue
        for kind, vis, _ in segments(line):
            if kind not in ("plain", "link", "tag"):
                continue
            vis = vis.replace("*", "")
            for m in ACRONYM.finditer(vis):
                token = m.group(1)
                if token in seen or token not in known:
                    continue
                seen.add(token)
                exp, entry = known[token]
                if _norm(entry).startswith(NAME_ONLY):
                    continue
                prior = _norm(before + vis[:m.start()])
                if not prior.endswith(_norm(exp) + " ("):
                    out.append(f"{DOC1}:{n}: first use of {token} is not "
                               f"spelled out as {exp!r}")
            before += vis
        before += " "
    return out


def _terms(docs: dict[str, str], doc: str) -> dict[str, tuple[str, str]]:
    """Label -> (defining document, id) for the terms `doc` may link."""
    chain = {DOC1: (DOC1,), DOC2: (DOC1, DOC2), DOC3: (DOC1, DOC2, DOC3)}
    out = {}
    for d in chain[doc]:
        for aid, label, _ in entries(docs[d]):
            if not aid.startswith("acr-"):
                out.setdefault(label.lower(), (d, aid))
    return out


def term_first_use_problems(docs: dict[str, str]) -> list[str]:
    out = []
    for doc, text in docs.items():
        terms = _terms(docs, doc)
        anchored = {d: set(ANCHOR.findall(t)) for d, t in docs.items()}
        pending = dict(terms)
        for n, line, is_h, body in lines_of(text):
            if not body or is_h or not pending:
                continue
            for kind, vis, target in segments(line):
                if kind not in ("plain", "link"):
                    continue
                path, frag = _split(target, doc) if kind == "link" \
                    else ("", "")
                other_entry = (kind == "link" and path in ORDER
                               and frag in anchored[path])
                for label, (d, aid) in list(pending.items()):
                    pat = (r"(?<![\w-])" + r"\s+".join(map(re.escape,
                           label.split())) + r"(?-i:s|es)?(?![\w-])")
                    if not re.search(pat, vis, re.I):
                        continue
                    if kind == "link" and path == d and frag == aid:
                        del pending[label]
                    elif other_entry:
                        continue        # inside a link to another entry
                    else:
                        out.append(f"{doc}:{n}: first use of {label!r} "
                                   f"does not link to {d}#{aid}")
                        del pending[label]
    return out


def duplicate_term_problems(docs: dict[str, str]) -> list[str]:
    out = []
    seen: dict[str, str] = {}
    for doc in ORDER:
        for aid, label, _ in entries(docs[doc]):
            key = label.lower()
            if key in seen and seen[key] != doc:
                out.append(f"{doc}: {label!r} is already defined in "
                           f"{seen[key]}")
            seen.setdefault(key, doc)
    return out


def claim_bullets(docs: dict[str, str]):
    for doc, text in docs.items():
        for heading, lines in sections(text, CLAIMS):
            yield doc, heading, lines, bullets(lines)


def claim_shape_problems(docs: dict[str, str]) -> list[str]:
    out = []
    for doc, heading, lines, _ in claim_bullets(docs):
        for line in lines:
            if line.strip() and not line.startswith(("- ", "  ")):
                out.append(f"{doc}: {heading!r} holds a line that is not "
                           f"a claim bullet: {line[:60]!r}")
    return out


def claim_tag_problems(docs: dict[str, str]) -> list[str]:
    return [f"{doc}: claim without an evidence tag: {b[:70]!r}"
            for doc, _, _, bs in claim_bullets(docs) for b in bs
            if not TAG.match(b)]


def _cited(bullet: str) -> list[str]:
    m = PATHS.search(bullet.rstrip())
    return re.findall(r"`([^`]+)`", m.group(1)) if m else []


def claim_path_problems(docs: dict[str, str], tracked: set[str]) -> list[str]:
    out = []
    for doc, _, _, bs in claim_bullets(docs):
        for b in bs:
            paths = _cited(b)
            if not paths:
                out.append(f"{doc}: claim names no file: {b[:70]!r}")
            for p in paths:
                if p not in tracked or p.startswith("docs/learning/"):
                    out.append(f"{doc}: claim cites {p}, not a tracked "
                               "source file")
    return out


@functools.lru_cache(maxsize=None)
def _md_figures(path: Path) -> frozenset[str]:
    text = path.read_text(encoding="utf-8")
    return frozenset(f.lstrip("-") for f in figures(text))


def claim_figure_problems(docs: dict[str, str], tracked: set[str],
                          root: Path) -> list[str]:
    out = []
    for doc, _, _, bs in claim_bullets(docs):
        for b in bs:
            sources = [p for p in _cited(b) if p in tracked]
            if not sources:
                continue
            for fig, pct in figures(b).items():
                found = False
                for p in sources:
                    full = root / p
                    if p.endswith(".json"):
                        found = resolves(fig, pct, _values(full))
                    else:
                        found = fig.lstrip("-") in _md_figures(full)
                    if found:
                        break
                if not found:
                    out.append(f"{doc}: figure {fig} is in none of "
                               f"{sources}: {b[:60]!r}")
    return out


def outside_problems(docs: dict[str, str]) -> list[str]:
    out = []
    for doc, text in docs.items():
        for heading, lines in sections(text, OUTSIDE):
            for line in lines:
                if line.strip() and not line.startswith(("- ", "  ")):
                    out.append(f"{doc}: {heading!r} holds a line that is "
                               f"not a bullet: {line[:60]!r}")
            for b in bullets(lines):
                if not OUTSIDE_SOURCE.search(b):
                    out.append(f"{doc}: outside claim names no source: "
                               f"{b[:70]!r}")
    return out


# ------------------------------------------------------------------ tests

@functools.lru_cache(maxsize=1)
def _tracked() -> frozenset[str]:
    out = subprocess.run(["git", "ls-files"], capture_output=True,
                         text=True, cwd=str(ROOT))
    if out.returncode != 0:
        # Fail, not skip: a skip reads as green with the check gone.
        pytest.fail(f"cannot enumerate tracked files (git exited "
                    f"{out.returncode}): {out.stderr.strip()[:200]}")
    return frozenset(out.stdout.splitlines())


def _docs() -> dict[str, str]:
    return {d: (DOCS / d).read_text(encoding="utf-8") for d in ORDER}


def _none(problems: list[str], what: str) -> None:
    assert not problems, f"{len(problems)} {what}:\n" + "\n".join(
        problems[:15])


def test_the_documents_are_there_and_not_empty():
    """A guard over empty documents passes trivially."""
    docs = _docs()
    acr = acronym_entries(docs)
    assert len(acr) >= 20, f"Doc 1 has {len(acr)} acronym entries"
    assert len(_terms(docs, DOC1)) >= 20, "Doc 1 has too few term entries"
    for doc in ORDER:
        claims = [b for d, _, _, bs in claim_bullets({doc: docs[doc]})
                  for b in bs]
        assert len(claims) >= 10, f"{doc}: {len(claims)} claim bullets"
        assert sections(docs[doc], OUTSIDE), f"{doc}: no outside section"
        assert re.search(r"^\*\*Version \d+\.\d+\*\*, \d{4}-\d\d-\d\d",
                         docs[doc], re.M), f"{doc}: no version line"
        assert "## Change list" in docs[doc], f"{doc}: no change list"


def test_the_acronym_pattern():
    found = [m.group(1) for m in ACRONYM.finditer(
        "AUPRC, GA2M, IEEE-CIS, QUBOs and CVQBoost-KNN; not F108, A31, "
        "CVQBoost, Dirac-3S, QCi, LightGBM, S2 or H1b")]
    assert found == ["AUPRC", "GA2M", "IEEE-CIS", "QUBO", "KNN"]
    assert slug("IEEE-CIS") == "acr-ieee-cis"
    kinds = [k for k, _, _ in segments(
        "a [SIM] b `x` [y](#z) <a id=\"q\"></a> https://e.org/p")]
    assert kinds == ["plain", "tag", "plain", "code", "plain", "link",
                     "plain", "html", "html", "plain", "url"]


def test_same_document_anchors_resolve():
    _none([p for p in link_problems(_docs(), set(_tracked()))
           if p.startswith("anchor:")], "broken same-document anchor(s)")


def test_cross_document_files_resolve():
    _none([p for p in link_problems(_docs(), set(_tracked()))
           if p.startswith("file:")], "link(s) to a missing file")


def test_cross_document_anchors_resolve():
    _none([p for p in link_problems(_docs(), set(_tracked()))
           if p.startswith("cross-anchor:")],
          "broken cross-document anchor(s)")


def test_no_anchor_id_is_repeated():
    _none(duplicate_id_problems(_docs()), "repeated anchor id(s)")


def test_every_acronym_has_an_entry_in_doc1():
    _none(acronym_entry_problems(_docs()), "acronym(s) with no entry")


def test_doc1_spells_out_each_acronym_at_first_use():
    _none(spelled_out_problems(_docs()), "acronym(s) used before spelled out")


def test_every_acronym_use_links_its_entry():
    _none(acronym_link_problems(_docs()), "unlinked acronym use(s)")


def test_a_terms_first_use_links_its_entry():
    _none(term_first_use_problems(_docs()), "unlinked first use(s)")


def test_no_term_is_defined_twice():
    _none(duplicate_term_problems(_docs()), "term(s) defined twice")


def test_claim_sections_hold_only_claims():
    _none(claim_shape_problems(_docs()), "non-claim line(s)")


def test_every_claim_has_an_evidence_tag():
    _none(claim_tag_problems(_docs()), "claim(s) without a tag")


def test_every_claim_names_a_tracked_file():
    _none(claim_path_problems(_docs(), set(_tracked())),
          "claim(s) without a tracked source")


def test_every_claim_figure_is_in_a_cited_source():
    _none(claim_figure_problems(_docs(), set(_tracked()), ROOT),
          "claim figure(s) not in their sources")


def test_every_outside_claim_names_its_source():
    _none(outside_problems(_docs()), "outside claim(s) without a source")


# ------------------------------------------------------------- red proofs
# Each target occurs exactly once in its document (expect_occurrences=1),
# so a moved or repeated target refuses instead of proving nothing.

def _fails(doc, old, new, node, label):
    from injection import Mutation, assert_can_fail, run_pytest
    assert_can_fail([Mutation(DOCS / doc, old, new, expect_occurrences=1)],
                    lambda: run_pytest(f"{THIS}::{node}", ROOT), label)


_D1 = "ML%20QML%20and%20QC%20Understandings%20about%20Quantum%20Advantage"

PROOFS = [
    # (document, old, new, test, label)
    (DOC1, '<a id="ml-alert-budget"></a>', '<a id="ml-alert-budgetx"></a>',
     "test_same_document_anchors_resolve", "a same-document anchor"),
    (DOC2, "Laymen%20terms.md)", "Laymen%20term.md)",
     "test_cross_document_files_resolve", "a cross-document file"),
    (DOC3, "ML%20Expert.md#ml2-wilcoxon-test)",
     "ML%20Expert.md#ml2-wilcoxon-testx)",
     "test_cross_document_anchors_resolve", "a cross-document anchor"),
    (DOC3, '<a id="qc3-room"></a>', '<a id="qc3-dual-bound"></a>',
     "test_no_anchor_id_is_repeated", "a repeated anchor id"),
    (DOC1, "**SCIP**:", "**SCIPX**:",
     "test_every_acronym_has_an_entry_in_doc1", "an acronym with no entry"),
    (DOC1, "card-not-present ([CNP]", "([CNP]",
     "test_doc1_spells_out_each_acronym_at_first_use",
     "an acronym not spelled out"),
    (DOC3, f"[QSVM]({_D1}%20-%20Laymen%20terms.md#acr-qsvm)", "QSVM",
     "test_every_acronym_use_links_its_entry", "an unlinked acronym"),
    (DOC1, "[Bayes error](#ml-bayes-error)", "Bayes error",
     "test_a_terms_first_use_links_its_entry", "an unlinked first use"),
    (DOC2, "**Equivalence margin**:", "**Alert budget**:",
     "test_no_term_is_defined_twice", "a term defined twice"),
    (DOC3, "- [SIM] On the training fold, as every device run built it",
     "Untagged prose.\n\n- [SIM] On the training fold, as each device "
     "run built it",
     "test_claim_sections_hold_only_claims", "prose in a claim section"),
    (DOC1, "- [HW] A quantum support vector machine",
     "- A quantum support vector machine",
     "test_every_claim_has_an_evidence_tag", "a claim without a tag"),
    (DOC3, "`docs/sprints/SPRINT_26_SUMMARY.md`",
     "`docs/sprints/SPRINT_26_SUMMARX.md`",
     "test_every_claim_names_a_tracked_file", "a claim citing no file"),
    (DOC2, "LightGBM 0.5785", "LightGBM 0.5786",
     "test_every_claim_figure_is_in_a_cited_source",
     "a figure not in its source"),
    (DOC2, "mean -0.069, 95% interval", "mean -0.079, 95% interval",
     "test_every_claim_figure_is_in_a_cited_source",
     "a figure not in its cited JSON"),
    (DOC1, "`tang-no-exponential-speedup`, high",
     "`tang-no-exponential-speedup`",
     "test_every_outside_claim_names_its_source",
     "an outside claim without a grade"),
]


@pytest.mark.parametrize("doc,old,new,node,label", PROOFS,
                         ids=[p[4] for p in PROOFS])
def test_each_rule_can_fail(doc, old, new, node, label):
    _fails(doc, old, new, node, label)
