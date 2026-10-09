"""No tracked file names the Phase 1 repository, except the approved list.

F132 (Sprint 24). Team lead, 2026-10-09: "nothing in this p2 repo should
reference anything in the p1 repo ... update all references as needed in this
sprint". The defect that made it urgent: `scripts/us_english_fix.py` held the
Phase 1 clone's absolute path, so running it from here rewrote that
repository's markdown, and the cross-repo hook could not see it because the
path was inside the script, not the command.

The name is matched case-insensitively as a substring, so one rule covers the
Windows path, the backslash form, the `/mnt/d` WSL form and the GitHub URL.
It is assembled at runtime so this file needs no place on its own allowlist.

The allowlist was approved at Sprint 24 planning:
  - D2 (team lead, 2026-10-09): the submitted proposal and appendix (FROZEN,
    they cite the public URL as filed), the B5/B4 launcher log (generated
    evidence) and four history records.
  - The files that must name the repository in order to block it: the
    cross-repo hook and CLAUDE.md's boundary rule.
  - D6 option 1: the record files, CHANGELOG.md, the master plan and
    everything under docs/sprints/, which record F127, the rename and
    Sprint 23 and cannot do so without the name.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NAME = ("hsbc-quantum-fraud" + "-2026").encode()

ALLOWED_FILES = {
    # D2: submitted documents, FROZEN
    "docs/paper/proposal.md",
    "docs/paper/appendix.md",
    # D2: generated evidence
    "experiments/results/call_logs/b5_then_b4_launcher.log",
    # D2: history records outside docs/sprints/
    "docs/reviews/f36-float-tables-outcome.md",
    # The boundary must name the repository to block it
    ".claude/hooks/block_cross_repo_write.py",
    "CLAUDE.md",
    # D6 option 1: records
    "CHANGELOG.md",
    "docs/ALL_SPRINTS_MASTER_PLAN.md",
}
# D6 option 1. D2's three history records under it (SPRINT_1_SUMMARY.md,
# SPRINT_14_RETROSPECTIVE.md, SPRINT_16_RETROSPECTIVE.md) are covered here.
ALLOWED_PREFIXES = ("docs/sprints/",)


def _tracked() -> list[str]:
    out = subprocess.run(["git", "ls-files", "-z"], cwd=str(ROOT),
                         capture_output=True, check=True).stdout
    files = [p for p in out.decode("utf-8").split("\0") if p]
    assert files, "git ls-files returned nothing; this test would check nothing"
    return files


def _allowed(path: str) -> bool:
    return path in ALLOWED_FILES or path.startswith(ALLOWED_PREFIXES)


def test_no_tracked_file_outside_the_allowlist_names_the_phase1_repository():
    offenders = []
    for rel in _tracked():
        if _allowed(rel):
            continue
        p = ROOT / rel
        if not p.is_file():
            continue
        if NAME in p.read_bytes().lower():
            offenders.append(rel)
    assert not offenders, (
        "these tracked files name the Phase 1 repository. Point them at this "
        "repository, say 'the Phase 1 repository', or (only with the team "
        f"lead's approval) add them to the allowlist: {offenders}")


def test_every_allowlisted_file_still_exists():
    """A stale allowlist entry is a hole waiting for a new file to fill it."""
    tracked = set(_tracked())
    missing = sorted(f for f in ALLOWED_FILES if f not in tracked)
    assert not missing, f"allowlisted but not tracked: {missing}"


def test_the_scan_reads_this_repository():
    """The companion: a scan that reads no files passes vacuously."""
    tracked = _tracked()
    assert "CLAUDE.md" in tracked
    assert NAME in (ROOT / "CLAUDE.md").read_bytes().lower(), (
        "CLAUDE.md's boundary rule no longer names the Phase 1 repository, so "
        "either the rule changed or this scan cannot see the name")
