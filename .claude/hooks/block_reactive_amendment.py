"""PREREGISTRATION.md is FROZEN: amendments only, and only after verification.

Converted from PowerShell 2026-09-17 (F78, Sprint 16).

Why this is a hook rather than a rule: in Sprint 12 a correction was written in
response to a review finding and published within hours. The correction was
false. Two external reviews caught it the same day, and A27 records the
withdrawal. The verification that would have prevented it took four minutes when
it was finally done.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hooklib  # noqa: E402

EDIT_TOOLS = {"Edit", "Write", "NotebookEdit"}
GUARDED_SUFFIX = "experiments/PREREGISTRATION.md"
APPROVAL_TOKEN = ".claude/.amendment-verified"
# The Phase 2 preregistration as filed (Sprint 34 Task D, F102, D3 option
# 1). No token opens these: the team lead, 2026-11-22, "neither as filed
# copy (phase 1 and phase 2) should ever be changed". Amendments go in
# experiments/phase2/PREREGISTRATION_AMENDMENTS.md (D2 option 1).
LOCKED_PHASE2 = (
    "experiments/phase2/PREREGISTRATION_SUBMITTED_2026-11-18.md",
    "experiments/phase2/PREREGISTRATION_FINAL.md",
    "experiments/phase2/PREREGISTRATION_DRAFT.md",
)
PHASE2_MESSAGE = """[BLOCKED] This is the Phase 2 preregistration as filed on 2026-11-18.
It is locked and is never edited, with no exception (team lead, 2026-11-22).

Write the change as a dated entry in
experiments/phase2/PREREGISTRATION_AMENDMENTS.md instead. That file's
header gives the form. experiments/src/test_phase2_prereg_filed.py also
fails on any change to the locked files."""

MESSAGE = """[BLOCKED] PREREGISTRATION.md is FROZEN. Amendments only, and only after the
finding behind them has been independently verified (workflow: VERIFY BEFORE
AMENDING, team lead 2026-09-11).

Before amending:

  1. Verify the finding against the CODE or the ARTIFACT it describes.
     Not against the reviewer's description of it.
  2. If a review is still arriving, WAIT and batch. Do not amend per finding.
  3. Record what you checked:

     .claude/.amendment-verified  <- write what was checked, and how

Do NOT create that file to unblock yourself.

Why this is a hook: in Sprint 12 a correction was written in response to a
review finding and published within hours. The correction was false. Two
external reviews caught it the same day, and A27 records the withdrawal. The
verification that would have prevented it took four minutes when it was finally
done."""


def main() -> int:
    payload = hooklib.read_payload()
    if hooklib.tool_name(payload) not in EDIT_TOOLS:
        return hooklib.ALLOW

    path = hooklib.file_path_of(payload)
    if not path:
        return hooklib.ALLOW

    # normalize() so a Windows-separator path still matches. A check that
    # matches only one separator style silently never fires on the other OS.
    if hooklib.normalize(path).endswith(LOCKED_PHASE2):
        return hooklib.block(PHASE2_MESSAGE)
    if not hooklib.normalize(path).endswith(GUARDED_SUFFIX):
        return hooklib.ALLOW

    token = hooklib.repo_file(*APPROVAL_TOKEN.split("/"))
    if token.exists():
        # THE TOKEN IS SINGLE-USE AND IS CONSUMED HERE (Sprint 17 improvement
        # 5). While it exists this guard is disabled, so a token left behind
        # after the amendment it authorized turns the guard off for every
        # later edit -- silently, because a disabled guard looks exactly like
        # a passing one.
        #
        # That happened in Sprint 17: the token written for A33 stayed on disk
        # after the amendment was made, and three hook-parity tests went red
        # because the hook could no longer block anything. Deleting it was a
        # remembered step, and a remembered step is the thing this repository
        # keeps replacing with a mechanical one.
        #
        # Consuming it also makes the approval mean what it says: ONE verified
        # amendment, not "amendments are allowed from now on".
        try:
            token.unlink()
        except OSError as exc:
            # Never fail the edit over cleanup -- but never do it SILENTLY
            # either. If the unlink fails the guard is now disabled for every
            # later edit, which is precisely the harm the comment above
            # describes, and a silent handler leaves no trace of it.
            #
            # Routine causes on Windows: the file held open by an editor, an
            # antivirus scanner, or a sync client. Stderr from a hook that
            # returns ALLOW blocks nothing, so the warning is free.
            # (PR #122 review.)
            sys.stderr.write(
                f"[WARNING] Could not consume the amendment token {token}: "
                f"{exc}. block_reactive_amendment is now DISABLED until that "
                "file is deleted by hand. This edit is allowed; so is the "
                "next one.\n")
        return hooklib.ALLOW

    return hooklib.block(MESSAGE)


if __name__ == "__main__":
    sys.exit(main())
