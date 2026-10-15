"""Blocks writes to sibling repositories from this repository's sessions.

Converted from PowerShell 2026-09-17 (F78, Sprint 16). Written 2026-09-15.

Team lead: work in this repository never writes to spamfilter-multi,
EvidenceBasedDB or the Phase 1 repository. EvidenceBasedDB is read freely
(team lead, 2026-10-14); the other two are read on request.

THE PHASE 1 REPOSITORY IS FORBIDDEN TOO (F132, Sprint 24). Phase 2 work moved
here, and the Phase 1 repository is about to be restored as filed and
archived. A write there would change the filed record. Its name is a prefix
of nothing in this repository's path since the 2026-10-09 rename, so a
substring match cannot block this repository. It does also match the
planning folder outside every repository whose name starts with the Phase 1
name; blocking writes there is accepted (F132 card).

The failure this guards: a Sprint 14 session reviewing PR #97 also examined
EvidenceBasedDB, found real defects, and fixed, committed and pushed them there
directly. Every finding was genuine and the boundary was still wrong. The
changes arrived in that repository with no review, no tests as gatekeeper and no
sprint record.

THE SIBLING MUST BE THE TARGET OF THE MUTATION, not merely mentioned. The first
version tested "is this mutating anywhere?" and "does it name a sibling
anywhere?" independently and ANDed the answers. That blocked two legitimate
read-only commands within minutes of shipping: a grep whose PATTERN contained
`New-Item|Remove-Item`, and a heredoc writing a file in THIS repository whose
text quoted both sibling names. A guard that blocks correct work trains bypass.

Cmdlets are anchored to a command position for the same reason, so a quoted grep
pattern cannot match.

Reads are deliberately NOT blocked: cat, grep, git log, git show, Read.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hooklib  # noqa: E402

EDIT_TOOLS = {"Edit", "Write", "NotebookEdit"}
SHELL_TOOLS = {"Bash", "PowerShell"}

FORBIDDEN = ("spamfilter-multi", "EvidenceBasedDB", "hsbc-quantum-fraud-2026")

GIT_WRITE = re.compile(
    r"git\s+(-C\s+\S*\s+)?(add|commit|push|mv|rm|checkout|switch|apply|restore|"
    r"reset|merge|rebase|tag|branch\s+-[dDmM])", re.IGNORECASE)


def message(what: str) -> str:
    return f"""BLOCKED: cross-repository write.

{what}

This repository's sessions never write to spamfilter-multi, EvidenceBasedDB or
the Phase 1 repository (CLAUDE.md standing rules; SPRINT_EXECUTION_WORKFLOW.md
invariant 9). EvidenceBasedDB is read freely, its store read-only; the
other two are read on request. A change wanted in EvidenceBasedDB goes as a
prompt the team lead pastes into a session there.

If a finding belongs to that repository, REPORT it -- file, line and fix -- and
hand it to a session running there, so it lands through that repository's own
review and tests."""


def check_path(path: str) -> str | None:
    # A path is inside a forbidden repository when one of its FOLDERS is that
    # repository's name. Matching the name anywhere in the path (the version
    # before Sprint 25 IMP-3) also blocked files in THIS repository whose
    # names merely contained it, such as a proposals file named after the
    # evidence library. Case-insensitive, because Windows paths are.
    #
    # Each folder is canonicalized the way Windows resolves it, because an
    # exact name match is otherwise easy to step around: Windows drops
    # trailing dots and spaces ("name." and "name " open "name"), and a
    # ":stream" suffix names a stream of the same folder. The path is also
    # resolved, which expands 8.3 short names ("NAME~1") and follows
    # junctions to the real folder. Both the written and the resolved forms
    # are checked; either one matching blocks.
    candidates = [path]
    try:
        candidates.append(os.path.realpath(path))
    except (OSError, ValueError):
        pass
    forbidden = {repo.lower(): repo for repo in FORBIDDEN}
    for candidate in candidates:
        folders = [_canonical_folder(p)
                   for p in hooklib.normalize(candidate).split("/")[:-1]]
        for i, folder in enumerate(folders):
            if folder in forbidden:
                return (f"Tool targets a path inside '{forbidden[folder]}':"
                        f"\n  {path}")
            # A forbidden repository's Claude Code project directory, where
            # that repository's sessions keep their memory. Claude Code names
            # it after the session's working directory with every separator
            # turned into "-" ("D--Data-Harold-github-<name>"), so the name is
            # a "-"-bounded part of it, at the end or, for a session started
            # in a subfolder, followed by "-". (Sprint 26 Task I, from
            # EvidenceBasedDB's F79: an exact folder match missed it.)
            if i >= 2 and folders[i - 2:i] == [".claude", "projects"]:
                for key, repo in forbidden.items():
                    if folder.endswith("-" + key) or f"-{key}-" in folder:
                        return (f"Tool targets the Claude Code project "
                                f"directory of '{repo}':\n  {path}")
    return None


def _canonical_folder(part: str) -> str:
    """A folder name as Windows would open it, lower-cased."""
    if ":" in part and not re.fullmatch(r"[A-Za-z]:", part):
        part = part.split(":", 1)[0]
    return part.rstrip(". ").lower()


def check_command(cmd: str) -> str | None:
    for repo in FORBIDDEN:
        r = re.escape(repo)

        targets = [
            rf">>?\s*[\"']?[^\"'|;&]*{r}",
            rf"\b(cp|mv|rm|tee|touch|mkdir|rmdir)\b[^;&|]*{r}",
            rf"\bsed\s+-i[^;&|]*{r}",
            # Anchored to a command position, so a quoted grep PATTERN
            # containing these words cannot match.
            rf"(^|[;&|]\s*|\|\s*)(Set-Content|Out-File|Add-Content|New-Item|"
            rf"Remove-Item|Copy-Item|Move-Item)\s[^;&|]*{r}",
        ]
        for t in targets:
            if re.search(t, cmd, re.IGNORECASE | re.MULTILINE):
                return f"A write targets '{repo}':\n  {cmd}"

        # Git writes are scoped by the working directory, so a cd into the
        # sibling, or -C pointing at it, is the shape that matters.
        if GIT_WRITE.search(cmd):
            if (re.search(rf"cd\s+[\"']?[^\"';&|]*{r}", cmd, re.IGNORECASE) or
                    re.search(rf"git\s+-C\s+[\"']?[^\"';&|]*{r}", cmd, re.IGNORECASE)):
                return f"A git write runs inside '{repo}':\n  {cmd}"
    return None


def main() -> int:
    payload = hooklib.read_payload()
    tool = hooklib.tool_name(payload)

    if tool in EDIT_TOOLS:
        path = hooklib.file_path_of(payload)
        if path:
            found = check_path(path)
            if found:
                return hooklib.block(message(found))
        return hooklib.ALLOW

    if tool in SHELL_TOOLS:
        cmd = hooklib.command_of(payload)
        if cmd:
            found = check_command(cmd)
            if found:
                return hooklib.block(message(found))

    return hooklib.ALLOW


if __name__ == "__main__":
    sys.exit(main())
