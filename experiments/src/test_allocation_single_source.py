"""The Dirac-3 balance has one owner, and no live document restates it.

Sprint 24 IMP-1 (team lead, 2026-10-10: "hoping only one single source of
truth"). The balance read 8,522 s on 2026-10-10, after QCi loaded the
account, while six live documents still stated an older figure as current:
two master plan cards, two `CHECKLIST-Phase2.md` items,
`SPECTRA_IMPROVEMENT_RESEARCH.md` and `QPU_RECONCILIATION.md` (1,961 s, two
reads stale). A restated balance is right on the day it is written and wrong
from the next metered call or grant onwards, and a stale one can size a
metered run.

The owner is `experiments/results/allocation_reads.json`, written only by
`check_allocation.py --record`; its last read is the balance. Documents cite
it. The scan below fails on a present-tense balance claim in any tracked
markdown outside the record files, whose job is to say what was true on
their date.
"""
from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from check_allocation import READS, record_read

ROOT = Path(__file__).resolve().parents[2]

# Present-tense balance claims: "the balance is 1,022 s", "1,681 s remain",
# "Remaining: 1,961 seconds". Matched on whitespace-collapsed text, because a
# wrapped line splits the claim across two lines.
CLAIM = re.compile(
    r"\bbalance\s+(?:is|stays|remains|of|now)\s+(?:about\s+|now\s+)?\**"
    r"\d[\d,]*\s*(?:s|sec|seconds)\b"
    r"|\b\d[\d,]*\**\s*(?:s|sec|seconds)\s+(?:remain|remains|left)\b"
    r"|\bremaining\W{0,4}\s*\**\d[\d,]*\**\s*(?:s|sec|seconds)\b",
    re.IGNORECASE)

# Records: each says what was true on its own date, and is not rewritten.
RECORD_PREFIXES = ("docs/sprints/", "docs/paper/", "docs/submission/")
RECORD_FILES = {
    "CHANGELOG.md",
    "experiments/PREREGISTRATION.md",       # FROZEN, amendments only
    "docs/HARDWARE_PLAN_PHASE_2.md",        # sent to QCi
    "docs/HARDWARE_REQUEST_B1_G0b.md",      # a dated request
}


def _tracked_markdown() -> list[str]:
    out = subprocess.run(["git", "ls-files", "-z", "*.md"], cwd=str(ROOT),
                         capture_output=True, check=True).stdout
    files = [p for p in out.decode("utf-8").split("\0") if p]
    assert files, "git ls-files returned nothing; this test would check nothing"
    return files


def _is_record(rel: str) -> bool:
    return rel in RECORD_FILES or rel.startswith(RECORD_PREFIXES)


def balance_claims(root: Path, files: list[str]) -> list[tuple[str, str]]:
    """(file, claim) for every present-tense balance claim outside the records."""
    found = []
    for rel in files:
        if _is_record(rel):
            continue
        p = root / rel
        if not p.is_file():
            continue
        text = " ".join(p.read_text(encoding="utf-8").split())
        found += [(rel, m.group(0)) for m in CLAIM.finditer(text)]
    return found


# ---- the scan ------------------------------------------------------------

def test_no_live_document_states_the_balance():
    claims = balance_claims(ROOT, _tracked_markdown())
    assert not claims, (
        "these documents state a Dirac-3 balance. Cite "
        "experiments/results/allocation_reads.json instead, or write the "
        f"figure as dated history ('fell to', 'remained'): {claims}")


def test_the_scan_reports_injected_claims_and_only_them(tmp_path):
    """Proves the scan can fail: the real tree has no claims, so the test
    above passes whether or not the scan detects anything."""
    (tmp_path / "docs" / "sprints").mkdir(parents=True)
    docs = {
        "docs/a.md": "Note.\nThe balance is\n1,022 s today.\n",
        "docs/b.md": "- **Remaining**: **1,961 seconds**\n",
        "docs/c.md": "after B4, 446 s remain for the rest\n",
        "docs/sprints/SPRINT_99_PLAN.md": "the balance stays 1,022 s\n",
        "CHANGELOG.md": "- the balance is 1,022 s\n",
        "docs/d.md": "it fell to 1,022 s; see allocation_reads.json\n",
    }
    for rel, text in docs.items():
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_text(text, encoding="utf-8")
    hits = sorted({rel for rel, _ in balance_claims(tmp_path, list(docs))})
    assert hits == ["docs/a.md", "docs/b.md", "docs/c.md"]


def test_every_record_file_still_exists():
    """A stale entry is a hole a new file could fill."""
    tracked = set(_tracked_markdown())
    missing = sorted(f for f in RECORD_FILES if f not in tracked)
    assert not missing, f"listed as records but not tracked: {missing}"


def test_the_documents_that_need_the_balance_cite_the_owner():
    for rel in ("docs/QPU_RECONCILIATION.md", "CHECKLIST-Phase2.md",
                "docs/ALL_SPRINTS_MASTER_PLAN.md",
                "docs/phase2/SPECTRA_IMPROVEMENT_RESEARCH.md"):
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert "allocation_reads.json" in text, f"{rel} does not cite the owner"


# ---- the owner -----------------------------------------------------------

def test_the_reads_file_is_well_formed():
    doc = json.loads(READS.read_text(encoding="utf-8"))
    assert doc["evidence_tag"] == "HW"
    reads = doc["reads"]
    assert reads, "no read recorded; the balance has no source"
    stamps = [r["checked_utc"] for r in reads]
    assert stamps == sorted(stamps) and len(set(stamps)) == len(stamps)
    for r in reads:
        assert isinstance(r["dirac_seconds"], int) and r["dirac_seconds"] >= 0
        assert r["metered_seconds"] == 0.0
        assert r["allocations"]["dirac"]["seconds"] == r["dirac_seconds"]


T0 = datetime(2026, 10, 10, 13, 0, tzinfo=timezone.utc)
LIVE = {"allocations": {"csample": {"metered": True, "seconds": 0,
                                    "paid": False},
                        "dirac": {"metered": True, "seconds": 8522,
                                  "paid": True}}}


def test_record_read_creates_the_file_and_appends(tmp_path):
    path = tmp_path / "reads.json"
    record_read(LIVE, path, now=T0)
    inner = {"dirac": {"metered": True, "seconds": 8440, "paid": True}}
    record_read(inner, path, now=T0 + timedelta(hours=1))
    doc = json.loads(path.read_text(encoding="utf-8"))
    assert [r["dirac_seconds"] for r in doc["reads"]] == [8522, 8440]
    assert doc["reads"][0]["checked_utc"] == T0.isoformat()
    assert doc["evidence_tag"] == "HW"
    assert not (tmp_path / "reads.json.tmp").exists()


@pytest.mark.parametrize("bad", [
    {"allocations": {"csample": {"seconds": 0}}},
    {"allocations": {"dirac": {"seconds": "8522"}}},
    {},
])
def test_record_read_refuses_a_response_without_dirac_seconds(tmp_path, bad):
    path = tmp_path / "reads.json"
    with pytest.raises(ValueError):
        record_read(bad, path, now=T0)
    assert not path.exists()


def test_record_read_refuses_a_read_older_than_the_last(tmp_path):
    path = tmp_path / "reads.json"
    record_read(LIVE, path, now=T0)
    before = path.read_bytes()
    with pytest.raises(ValueError):
        record_read(LIVE, path, now=T0)
    assert path.read_bytes() == before
