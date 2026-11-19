"""The Phase 2 preregistration draft stays consistent while reviews change it.

Sprint 33 Task D (#125), card F102. The team lead, at planning: "Add
gaurding [sic] the draft of the preregistration so that it does not drift in the
future. However, this is a draft that will go through a couple of reviews
before submitting later today."

So this is NOT a byte lock: the reviews may change any word. It fails when
a change leaves the draft inconsistent with itself or with the repository.
The byte lock (a tag, a hash test and the document-of-record hook) is a
filing step, listed in the draft's section 7.

One test per term; each is proven red below by breaking the draft (or the
PoC plan it cites) and watching that test fail.

1. Each of Experiments 1-6 has a section 6 table row and an entry.
2. Table rows and entry headings match one for one.
3. Each row's State is Run, Partly run or To run.
4. A Run or Partly run row names a tracked result file.
5. Each Experiment 1-6 entry states its state at filing, equal to its row.
6. The Filing section carries a filing date and a filing venue ("not set"
   is a value).
7. Every assumption the draft cites exists in the PoC plan's register.
8. Section 7 holds only closed items, decided items and filing steps.
9. The draft's newest revision-log date is not older than its last change.
10. Every decimal figure resolves to a tracked result file the draft names
    (F164's rule, `test_phase2_figures_resolve.py`), or is registered here
    with a reason.
11. `PREREGISTRATION_FINAL.md`, the copy submitted for filing, is
    byte-identical to the draft (PR #122 review, 2026-11-18).

Not a source-scan guard: it reads one document's structure, so Sprint 32
i3's list of forms does not apply.
"""
from __future__ import annotations

import datetime as dt
import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DRAFT = ROOT / "experiments" / "phase2" / "PREREGISTRATION_DRAFT.md"
POC = ROOT / "docs" / "phase2" / "PHASE2_POC_PLAN_DRAFT.md"
FINAL = ROOT / "experiments" / "phase2" / "PREREGISTRATION_FINAL.md"
THIS = Path(__file__).relative_to(ROOT).as_posix()

STATES = ("Run", "Partly run", "To run")
EXPERIMENTS = range(1, 7)

# Figures in the draft that resolve to no tracked result file it names.
# Each was checked when registered (2026-11-16).
# -0.0024 (F64's interval, quoted from docs/F64_LADDER_DECOMPOSITION.md)
# left this list 2026-11-18: the D9 notes name f144_proxy_twin.json and
# f154_confusion.json, which hold values that round to it. The match is
# by coincidence; the figure's source is still F64's document.
REGISTERED = {
    "10.5220": "part of the DOI 10.5220/0014628400004052, not a figure",
    "824.6": "the Experiment 4 pilot's projection in minutes; stored in "
             "f111_loke_protocol.json, which that entry does not name",
    "735.4": "quoted from the hardware plan: one pool build in seconds",
    "1.243": "derived: 1,865 s of training over 1,500 steps",
    "0.70514": "the AUPRC of a refused F107 run, noted before any F107 "
               "result; the refused run was not stored",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def section(text: str, start: str, end: str) -> str:
    """The text from the heading line `start` to the next heading `end`."""
    i = text.index(start)
    j = text.index(end, i + len(start))
    return text[i:j]


def rows(text: str) -> list[dict[str, str]]:
    """Section 6's status table, one dict per data row."""
    sec = section(text, "\n## 6. Experiments", "\n### ")
    lines = [ln for ln in sec.splitlines() if ln.startswith("|")]
    head = [c.strip() for c in lines[0].strip("|").split("|")]
    out = []
    for ln in lines[1:]:
        if set(ln) <= set("|- "):
            continue
        cells = [c.strip() for c in ln.strip("|").split("|")]
        out.append(dict(zip(head, cells)))
    return out


def headings(text: str) -> list[str]:
    sec = section(text, "\n## 6. Experiments", "\n## 7.")
    return [ln[4:] for ln in sec.splitlines() if ln.startswith("### ")]


def row_key(row: dict[str, str]) -> str:
    if row["#"] != "-":
        return f"Experiment {row['#']}"
    return re.sub(r"\s*\(.*?\)", "", row["Card(s)"]).strip()


def heading_key(h: str) -> str:
    m = re.match(r"(Experiment \d+) \(", h)
    return m.group(1) if m else h.split(":", 1)[0].strip()


def entry(text: str, n: int) -> str:
    sec = section(text, "\n## 6. Experiments", "\n## 7.")
    i = sec.index(f"\n### Experiment {n} (")
    j = sec.find("\n### ", i + 1)
    return sec[i:j if j >= 0 else len(sec)]


def _git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], capture_output=True, text=True,
                          cwd=str(ROOT))


def tracked(path: str) -> bool:
    """A tracked FILE: ls-files also accepts a directory or a glob that
    holds tracked files (PR #122 review), so the path must be a file."""
    return ((ROOT / path).is_file()
            and _git("ls-files", "--error-unmatch", path).returncode == 0)


def test_each_of_the_six_experiments_has_a_row_and_an_entry():
    text = _read(DRAFT)
    numbered = {r["#"] for r in rows(text)}
    keys = {heading_key(h) for h in headings(text)}
    missing = [n for n in EXPERIMENTS
               if str(n) not in numbered or f"Experiment {n}" not in keys]
    assert not missing, (f"Experiments {missing} lack a section 6 row or an "
                         "entry; the filing commits to all six")


def test_rows_and_entries_match_one_for_one():
    text = _read(DRAFT)
    r = [row_key(x) for x in rows(text)]
    h = [heading_key(x) for x in headings(text)]
    assert sorted(r) == sorted(h), (
        f"rows without an entry: {sorted(set(r) - set(h))}; "
        f"entries without a row: {sorted(set(h) - set(r))}")
    assert len(set(r)) == len(r), "a row key appears twice"


def test_each_state_is_one_of_the_stated_values():
    bad = [(row_key(r), r.get("State")) for r in rows(_read(DRAFT))
           if r.get("State") not in STATES]
    assert not bad, f"states outside {STATES}: {bad}"


def test_a_run_row_names_a_tracked_result():
    bad = []
    for r in rows(_read(DRAFT)):
        if r.get("State") in ("Run", "Partly run"):
            m = re.fullmatch(r"`([^`]+)`", r.get("Result", ""))
            if not m or not tracked(m.group(1)):
                bad.append((row_key(r), r.get("Result")))
    assert not bad, f"run rows whose result is not a tracked file: {bad}"


def test_each_experiment_states_its_state_at_filing():
    text = _read(DRAFT)
    by_n = {r["#"]: r.get("State") for r in rows(text)}
    bad = []
    for n in EXPERIMENTS:
        m = re.search(r"\*\*State at filing \(\d{4}-\d{2}-\d{2}\): "
                      r"(Run|Partly run|To run)\.\*\*", entry(text, n))
        if not m or m.group(1) != by_n.get(str(n)):
            bad.append((n, m.group(1) if m else None, by_n.get(str(n))))
    assert not bad, f"(experiment, entry state, row state) differ: {bad}"


def test_the_filing_section_has_a_date_and_a_venue():
    sec = section(_read(DRAFT), "\n## Filing\n", "\n## ")
    for field in ("Filing date", "Filing venue"):
        m = re.search(rf"^- \*\*{field}\*\*: *(\S.*)$", sec, re.M)
        assert m and m.group(1).strip(" ."), (
            f"the Filing section has no '{field}' value; write 'not set' "
            "until it is set")


def cited(text: str) -> set[int]:
    out: set[int] = set()
    # \s+ so a citation wrapped across lines is still read (PR review).
    for m in re.finditer(r"\bassumptions?\s+A(\d+)(?:\s*(?:-|to)\s*A(\d+))?",
                         text):
        lo = int(m.group(1))
        out |= set(range(lo, int(m.group(2) or lo) + 1))
    return out


def test_a_wrapped_or_ranged_citation_is_read():
    assert cited("per assumption\n  A13, and assumptions A1-A3") == {
        1, 2, 3, 13}


def test_every_cited_assumption_is_in_the_register():
    register = {int(n) for n in re.findall(r"^- \*\*\[A(\d+)\]",
                                           _read(POC), re.M)}
    missing = sorted(cited(_read(DRAFT)) - register)
    assert cited(_read(DRAFT)), "the draft cites no assumption"
    assert not missing, (f"the draft cites assumptions {missing}, absent "
                         f"from the register in {POC.relative_to(ROOT)}")


def test_section_7_holds_only_closed_decided_or_filing_steps():
    sec = section(_read(DRAFT), "\n## 7.", "\n## Revision log")
    items = [ln for ln in sec.splitlines() if ln.startswith("- ")]
    bad = [ln[:80] for ln in items
           if not ln.startswith(("- ~~", "- **Decided", "- **Open, filing step"))]
    assert items and not bad, f"section 7 items still open: {bad}"


def last_change() -> dt.date:
    """The day the draft last changed: today if it differs from HEAD,
    else its last commit's author date."""
    if _git("rev-parse", "--is-shallow-repository").stdout.strip() == "true":
        pytest.fail("shallow clone: the draft's last commit cannot be read")
    rel = DRAFT.relative_to(ROOT).as_posix()
    if _git("diff", "--quiet", "HEAD", "--", rel).returncode != 0:
        return dt.date.today()
    out = _git("log", "-1", "--format=%as", "--", rel)
    if out.returncode != 0 or not out.stdout.strip():
        pytest.fail(f"cannot read the draft's last commit: {out.stderr[:200]}")
    return dt.date.fromisoformat(out.stdout.strip())


def test_a_change_adds_a_revision_log_row():
    log = _read(DRAFT).split("\n## Revision log", 1)[1]
    dates = [dt.date.fromisoformat(d)
             for d in re.findall(r"^- (\d{4}-\d{2}-\d{2}):", log, re.M)]
    changed = last_change()
    assert dates and max(dates) >= changed, (
        f"the draft changed on {changed}, and its newest revision-log row "
        f"is {max(dates) if dates else None}; add a dated row")
    # A future date would satisfy the check for good (PR review).
    assert max(dates) <= dt.date.today(), (
        f"a revision-log row is dated in the future: {max(dates)}")


def test_every_figure_resolves_or_is_registered():
    from test_phase2_figures_resolve import unresolved
    live = set(unresolved("PREREGISTRATION_DRAFT.md", _read(DRAFT)))
    bad = sorted(live - set(REGISTERED), key=lambda f: float(f))
    stale = sorted(set(REGISTERED) - live)
    assert not bad, (f"figures that resolve to no result file the draft "
                     f"names and are not registered: {bad}")
    assert not stale, f"registered figures no longer unresolved: {stale}"
    assert all(len(why) >= 10 for why in REGISTERED.values())


def test_the_final_copy_matches_the_draft():
    assert FINAL.read_bytes() == DRAFT.read_bytes(), (
        "PREREGISTRATION_FINAL.md differs from PREREGISTRATION_DRAFT.md; "
        "the two copies of the filed text must stay byte-identical")


# --- Each term proven red -------------------------------------------------

def _fails(path: Path, old: str, new: str, node: str, label: str) -> None:
    from injection import Mutation, assert_can_fail, run_pytest
    assert_can_fail([Mutation(path, old, new, expect_occurrences=1)],
                    lambda: run_pytest(f"{THIS}::{node}", ROOT), label)


def test_the_six_experiment_check_can_fail():
    _fails(DRAFT, "### Experiment 6 (F110)", "### Experiment 7 (F110)",
           "test_each_of_the_six_experiments_has_a_row_and_an_entry",
           "Experiment 6's entry gone")


def test_the_row_entry_match_can_fail():
    _fails(DRAFT, "### F185: a cost-weighted", "### F186: a cost-weighted",
           "test_rows_and_entries_match_one_for_one", "an entry with no row")


def test_the_state_values_can_fail():
    _fails(DRAFT, "| Run | `docs/phase2/F185_COST_BUDGET.md` |",
           "| Done | `docs/phase2/F185_COST_BUDGET.md` |",
           "test_each_state_is_one_of_the_stated_values", "state 'Done'")


def test_the_tracked_result_check_can_fail():
    _fails(DRAFT, "| Run | `docs/phase2/F188_ROUNDING.md` |",
           "| Run | `docs/phase2/F188_ROUNDING_GONE.md` |",
           "test_a_run_row_names_a_tracked_result", "an untracked result")


def test_a_directory_is_not_a_tracked_result():
    _fails(DRAFT, "| Run | `docs/phase2/F188_ROUNDING.md` |",
           "| Run | `docs/phase2` |",
           "test_a_run_row_names_a_tracked_result",
           "a directory as the result")


def test_the_final_copy_check_can_fail():
    _fails(FINAL, "### Experiment 6 (F110)", "### Experiment 6 (F111)",
           "test_the_final_copy_matches_the_draft",
           "the FINAL copy edited alone")


def test_the_state_at_filing_check_can_fail():
    _fails(DRAFT, "**State at filing (2026-11-16): Run.** The intervals",
           "**State at filing (2026-11-16): Partly run.** The intervals",
           "test_each_experiment_states_its_state_at_filing",
           "an entry state that differs from its row")


def test_the_filing_fields_check_can_fail():
    _fails(DRAFT, "- **Filing venue**: not set.", "- **Venue**: not set.",
           "test_the_filing_section_has_a_date_and_a_venue",
           "the filing venue field gone")


def test_the_assumption_check_can_fail():
    _fails(POC, "- **[A12] The reader", "- **[A21] The reader",
           "test_every_cited_assumption_is_in_the_register",
           "a cited assumption missing from the register")


def test_the_section_7_check_can_fail():
    _fails(DRAFT, "- **Decided: pool build drift", "- Pool build drift",
           "test_section_7_holds_only_closed_decided_or_filing_steps",
           "an open item in section 7")


def test_the_revision_log_check_can_fail():
    # Moves the change one day past the newest row. Back-dating one row
    # went vacuous as soon as a second row shared its date.
    _fails(Path(__file__), "    changed = last_change()\n",
           "    changed = max(dt.date.fromisoformat(d) for d in re.findall("
           "r\"^- (\\d{4}-\\d{2}-\\d{2}):\", log, re.M)) "
           "+ dt.timedelta(days=1)\n",
           "test_a_change_adds_a_revision_log_row",
           "a change with no newer revision-log row")


def test_the_wrapped_citation_reading_can_fail():
    _fails(Path(__file__),
           "finditer(r\"\\bassumptions?\\s+A(\\d+)",
           "finditer(r\"\\bassumptions? A(\\d+)",
           "test_a_wrapped_or_ranged_citation_is_read",
           "a wrapped citation missed")


def test_the_future_date_check_can_fail():
    _fails(DRAFT, "- 2026-11-16: prepared for filing",
           "- 2099-11-16: prepared for filing",
           "test_a_change_adds_a_revision_log_row",
           "a revision-log row dated in the future")


def test_the_figure_check_can_fail():
    _fails(DRAFT, "- **Filing date**: 2026-11-18.",
           "- **Filing date**: 0.123457, 2026-11-18.",
           "test_every_figure_resolves_or_is_registered",
           "an unresolved figure")
