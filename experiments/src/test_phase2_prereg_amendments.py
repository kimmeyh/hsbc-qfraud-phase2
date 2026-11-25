"""The form of the Phase 2 amendments file (Sprint 34 Task C, F102, #137).

`experiments/phase2/PREREGISTRATION_AMENDMENTS.md` holds every change
written after the Phase 2 preregistration was filed (2026-11-18); the
filed text is locked and never edited (Sprint 34 D2 option 1). Each
entry must have:

1. a heading `### P2-A<n>. <date>: <title>`, numbered from 1 with no gap;
2. a real date, not later than today;
3. a date not earlier than the entry above it;
4. a `- **Filed section**:` line with a value;
5. a `- **Kind**:` line, one of the stated kinds.

One test per term, each proven red. The file's content is the team
lead's record; this checks its form only.
"""
from __future__ import annotations

import datetime as dt
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AMENDMENTS = ROOT / "experiments" / "phase2" / "PREREGISTRATION_AMENDMENTS.md"
THIS = Path(__file__).relative_to(ROOT).as_posix()

KINDS = ("procedure", "filing fact", "result note", "amendment", "new entry")
HEADING = re.compile(r"^### (P2-A(\d+))\. (\S+): (.+)$")


def entries(text: str) -> list[dict]:
    """Each entry: its id, number, date text, title and body lines."""
    out = []
    for line in text.splitlines():
        m = HEADING.match(line)
        if m:
            out.append({"id": m.group(1), "n": int(m.group(2)),
                        "date": m.group(3), "title": m.group(4), "body": []})
        elif line.startswith("### "):
            out.append({"id": line, "n": None, "date": "", "title": "",
                        "body": []})
        elif out:
            out[-1]["body"].append(line)
    return out


def field(entry: dict, name: str) -> str | None:
    prefix = f"- **{name}**:"
    for line in entry["body"]:
        if line.startswith(prefix):
            return line[len(prefix):].strip()
    return None


def problems(text: str, today: dt.date | None = None) -> list[str]:
    today = today or dt.date.today()
    bad, before = [], None
    for i, e in enumerate(entries(text), start=1):
        if e["n"] != i:
            bad.append(f"{e['id']}: expected heading ### P2-A{i}. <date>: <title>")
            continue
        try:
            day = dt.date.fromisoformat(e["date"])
        except ValueError:
            bad.append(f"{e['id']}: {e['date']!r} is not a YYYY-MM-DD date")
            continue
        if day > today:
            bad.append(f"{e['id']}: dated {day}, after today")
        if before is not None and day < before:
            bad.append(f"{e['id']}: dated {day}, before the entry above it")
        before = day
        if not field(e, "Filed section"):
            bad.append(f"{e['id']}: no Filed section")
        kind = field(e, "Kind")
        if kind not in KINDS:
            bad.append(f"{e['id']}: kind {kind!r} is not one of {KINDS}")
    return bad


def _entry(n, date, section="7", kind="procedure"):
    lines = [f"### P2-A{n}. {date}: a title"]
    if section is not None:
        lines.append(f"- **Filed section**: {section}")
    if kind is not None:
        lines.append(f"- **Kind**: {kind}")
    return "\n".join(lines + ["", "Text.", ""])


TODAY = dt.date(2026, 11, 22)


# ------------------------------------------------------------ the real file
def test_the_amendments_file_has_the_stated_form():
    text = AMENDMENTS.read_text(encoding="utf-8")
    assert entries(text), "the amendments file holds no entry"
    bad = problems(text)
    assert not bad, bad


# ------------------------------------------------------------ each term
def test_good_entries_pass():
    text = _entry(1, "2026-11-22") + _entry(2, "2026-11-22", kind="filing fact")
    assert problems(text, TODAY) == []


def test_a_gap_in_the_numbering_is_caught():
    text = _entry(1, "2026-11-22") + _entry(3, "2026-11-22")
    assert problems(text, TODAY) == [
        "P2-A3: expected heading ### P2-A2. <date>: <title>"]


def test_a_date_that_is_not_a_date_is_caught():
    assert problems(_entry(1, "2026-13-01"), TODAY) == [
        "P2-A1: '2026-13-01' is not a YYYY-MM-DD date"]


def test_a_future_date_is_caught():
    assert problems(_entry(1, "2026-11-23"), TODAY) == [
        "P2-A1: dated 2026-11-23, after today"]


def test_a_date_before_the_entry_above_is_caught():
    text = _entry(1, "2026-11-22") + _entry(2, "2026-11-21")
    assert problems(text, TODAY) == [
        "P2-A2: dated 2026-11-21, before the entry above it"]


def test_an_entry_with_no_filed_section_is_caught():
    assert problems(_entry(1, "2026-11-22", section=None), TODAY) == [
        "P2-A1: no Filed section"]


def test_an_entry_with_an_unknown_kind_is_caught():
    assert problems(_entry(1, "2026-11-22", kind="note"), TODAY) == [
        f"P2-A1: kind 'note' is not one of {KINDS}"]


# ------------------------------------------------------------ red proofs
def test_each_term_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    src = Path(__file__)
    for old, new, node, label in (
            ('        if e["n"] != i:\n', "        if False:\n",
             "test_a_gap_in_the_numbering_is_caught", "a numbering gap"),
            ("            day = dt.date.fromisoformat(e[\"date\"])\n",
             "            day = TODAY\n",
             "test_a_date_that_is_not_a_date_is_caught", "a date not read"),
            ("        if day > today:\n", "        if False:\n",
             "test_a_future_date_is_caught", "a future date"),
            ("        if before is not None and day < before:\n",
             "        if False:\n",
             "test_a_date_before_the_entry_above_is_caught", "dates out of order"),
            ('        if not field(e, "Filed section"):\n', "        if False:\n",
             "test_an_entry_with_no_filed_section_is_caught", "no filed section"),
            ("        if kind not in KINDS:\n", "        if False:\n",
             "test_an_entry_with_an_unknown_kind_is_caught", "an unknown kind")):
        assert_can_fail([Mutation(src, old, new, expect_occurrences=1)],
                        lambda node=node: run_pytest(f"{THIS}::{node}", ROOT),
                        label)
