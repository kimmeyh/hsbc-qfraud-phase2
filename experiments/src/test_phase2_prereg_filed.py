"""The Phase 2 preregistration as filed is locked (Sprint 34 Task D, F102).

The team lead sent the Phase 2 preregistration on 2026-11-18 at 9:01am
EST, and on 2026-11-22: "neither as filed copy (phase 1 and phase 2)
should ever be changed. Keep track of amendments for what we do later."
(Sprint 34 Q2, D2 option 1, D3 option 1.)

Three files are locked, each by the SHA-256 of its text with line endings
read as LF (a Windows checkout may write CRLF; the text is the same):

- `PREREGISTRATION_SUBMITTED_2026-11-18.md`: the text as sent, restored
  byte for byte from commit b8e2c0e, the last commit before 9:01. The
  tag `phase2-prereg-filed` points at that commit.
- `PREREGISTRATION_FINAL.md` and `PREREGISTRATION_DRAFT.md`: the two
  copies as they stood when the lock was added (c3d3c00). They differ
  from the sent text only in section 7 and the revision log.

The filed section 7 said this test would hash the text above an
"## Amendments" heading. The heading is not added, because adding it
would change the files; amendments go in
`experiments/phase2/PREREGISTRATION_AMENDMENTS.md` (entry P2-A1). So
each file is hashed whole.

`.claude/hooks/block_reactive_amendment.py` blocks an Edit or Write to
the three files, with no token that opens them; this test is the check
that also catches a change made any other way. There is no flag or
list that switches it off.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
P2 = ROOT / "experiments" / "phase2"
THIS = Path(__file__).relative_to(ROOT).as_posix()

SENT = "3d09845dbffae163d6819a9bdd3970843c8dafeee987034cb42aa2a1286019d6"
AT_LOCK = "636ce90c49079d4c546a14cbb3e1523be0131a75eb280c479a54e8bd0689466b"
LOCKED = {
    "PREREGISTRATION_SUBMITTED_2026-11-18.md": SENT,
    "PREREGISTRATION_FINAL.md": AT_LOCK,
    "PREREGISTRATION_DRAFT.md": AT_LOCK,
}


def text_sha256(path: Path) -> str:
    return hashlib.sha256(
        path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


@pytest.mark.parametrize("name", sorted(LOCKED))
def test_the_filed_text_is_unchanged(name):
    got = text_sha256(P2 / name)
    assert got == LOCKED[name], (
        f"{name} changed (SHA-256 {got}). The Phase 2 preregistration as "
        "filed is never edited; write the change as a dated entry in "
        "experiments/phase2/PREREGISTRATION_AMENDMENTS.md instead.")


def test_three_files_are_locked():
    assert len(LOCKED) == 3
    assert all(len(h) == 64 for h in LOCKED.values())


def test_the_sent_text_names_its_filing_date():
    """A cross-check that the SUBMITTED file is the sent text, not a later
    copy: the date was set at 08:54 and the venue never was."""
    text = (P2 / "PREREGISTRATION_SUBMITTED_2026-11-18.md").read_text(
        encoding="utf-8")
    assert "- **Filing date**: 2026-11-18." in text
    assert "- **Filing venue**: not set." in text
    assert "The lock step runs after the venue is" not in text  # 09:18 text


def test_line_endings_do_not_change_the_hash(tmp_path):
    lf, crlf = tmp_path / "lf.md", tmp_path / "crlf.md"
    lf.write_bytes(b"a\nb\n")
    crlf.write_bytes(b"a\r\nb\r\n")
    assert text_sha256(lf) == text_sha256(crlf)
    (tmp_path / "x.md").write_bytes(b"a\nc\n")
    assert text_sha256(tmp_path / "x.md") != text_sha256(lf)


# ------------------------------------------------------------ red proofs
# Each proof changes one locked file by one character and runs that file's
# check; the injection helper restores it and verifies the restore.
@pytest.mark.parametrize("name,old,new", [
    ("PREREGISTRATION_SUBMITTED_2026-11-18.md",
     "- **Filing venue**: not set.", "- **Filing venue**: not sat."),
    ("PREREGISTRATION_FINAL.md",
     "- **Filing venue**: not set.", "- **Filing venue**: not sat."),
    ("PREREGISTRATION_DRAFT.md",
     "- **Filing venue**: not set.", "- **Filing venue**: not sat."),
])
def test_each_locked_file_check_can_fail(name, old, new):
    from injection import Mutation, assert_can_fail, run_pytest
    assert_can_fail(
        [Mutation(P2 / name, old, new, expect_occurrences=1)],
        lambda: run_pytest(f"{THIS}::test_the_filed_text_is_unchanged[{name}]",
                           ROOT),
        f"{name} edited")


def test_the_hook_lock_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    hook = ROOT / ".claude" / "hooks" / "block_reactive_amendment.py"
    node = ("experiments/src/test_hook_parity.py::"
            "test_python_hook_matches_expectation["
            "block_reactive_amendment:editing the Phase 2 text as sent]")
    assert_can_fail(
        [Mutation(hook, "    if hooklib.normalize(path).endswith(LOCKED_PHASE2):\n",
                  "    if False:\n", expect_occurrences=1)],
        lambda: run_pytest(node, ROOT), "the hook lets the filed text be edited")
