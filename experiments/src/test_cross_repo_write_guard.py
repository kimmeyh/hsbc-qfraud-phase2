"""The cross-repository write boundary must be enforced, not merely documented.

Team lead, 2026-09-15: sessions in this repository never write to the sibling
repositories. Reading is fine: the evidence library freely (team lead,
2026-10-14), the others on request.

Why a test and not only a CLAUDE.md line: in Sprint 14 a session reviewing
PR #97 examined a sibling repository, found real defects, and fixed, committed
and pushed them there directly. Every finding was genuine; the boundary was
still wrong, because the changes reached that repository with no review, no
tests as gatekeeper and no sprint record.

Half of these cases assert the guard ALLOWS something. That half is not filler.
The first version of this hook blocked two legitimate read-only commands within
minutes of shipping, because it tested "is this mutating anywhere?" and "does it
name a sibling anywhere?" independently and ANDed the answers. A grep whose
PATTERN contained `New-Item|Remove-Item` was refused, and so was a heredoc
writing a file in THIS repository whose text quoted the sibling names. A guard
that blocks correct work trains people to bypass it, which is worse than no
guard.

The cases run through the hook itself, so a hook that stops firing fails here
rather than going quietly inert. That is exactly how two hooks in this
repository stayed dead for their entire life.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
# F78 (Sprint 16) converted this hook to Python. The cases below are
# unchanged; only the implementation under test moved.
HOOK = ROOT / ".claude" / "hooks" / "block_cross_repo_write.py"

# Assembled at runtime so this file's own text is not a literal match for the
# guard it tests. Writing the names out would make the file unwritable through
# a shell heredoc, which is how this test was first blocked.
SIBLING = "Evidence" + "BasedDB"
OTHER = "spamfilter" + "-multi"
# F132 (Sprint 24): the Phase 1 repository is forbidden too. Assembled for the
# same reason, and so this file needs no place on the boundary allowlist.
PHASE1 = "hsbc-quantum-fraud" + "-2026"
THIS = "hsbc-qfraud-phase2"
HERE = "D:/Data/Harold/github"
PROJECTS = "C:/Users/kimme/.claude/projects"

BLOCK, ALLOW = 2, 0

CASES = [
    # --- must BLOCK: the sibling is the target of a write -------------------
    ("Write tool into a sibling", BLOCK,
     {"tool_name": "Write",
      "tool_input": {"file_path": f"{HERE}/{SIBLING}/CLAUDE.md"}}),
    ("Edit tool into the other sibling", BLOCK,
     {"tool_name": "Edit",
      "tool_input": {"file_path": f"{HERE}/{OTHER}/lib/main.dart"}}),
    ("git push after cd into a sibling", BLOCK,
     {"tool_name": "Bash",
      "tool_input": {"command": f"cd {HERE}/{SIBLING} && git " + "push origin HEAD"}}),
    ("git -C pointed at a sibling", BLOCK,
     {"tool_name": "Bash",
      "tool_input": {"command": f"git -C {HERE}/{SIBLING} commit -m x"}}),
    ("shell redirect into a sibling", BLOCK,
     {"tool_name": "Bash",
      "tool_input": {"command": f"echo hi > {HERE}/{SIBLING}/x.md"}}),
    ("rm inside a sibling", BLOCK,
     {"tool_name": "Bash",
      "tool_input": {"command": f"rm -f {HERE}/{SIBLING}/docs/old.md"}}),
    ("sed -i against a sibling", BLOCK,
     {"tool_name": "Bash",
      "tool_input": {"command": f"sed -i s/a/b/ {HERE}/{SIBLING}/README.md"}}),

    # --- F132: the Phase 1 repository, in both directions --------------------
    ("Write tool into the Phase 1 repository", BLOCK,
     {"tool_name": "Write",
      "tool_input": {"file_path": f"{HERE}/{PHASE1}/docs/x.md"}}),
    ("shell redirect into the Phase 1 repository", BLOCK,
     {"tool_name": "Bash",
      "tool_input": {"command": f"echo hi > {HERE}/{PHASE1}/README.md"}}),
    ("shell write into the Phase 1 repository by its WSL path", BLOCK,
     {"tool_name": "Bash",
      "tool_input": {"command": f"cp x.md /mnt/d/Data/Harold/github/{PHASE1}/x.md"}}),
    ("git push after cd into the Phase 1 repository", BLOCK,
     {"tool_name": "Bash",
      "tool_input": {"command": f"cd {HERE}/{PHASE1} && git " + "push origin HEAD"}}),
    ("Write tool into this repository by its full path", ALLOW,
     {"tool_name": "Write",
      "tool_input": {"file_path": f"{HERE}/{THIS}/docs/x.md"}}),
    ("shell redirect into this repository by its full path", ALLOW,
     {"tool_name": "Bash",
      "tool_input": {"command": f"echo hi > {HERE}/{THIS}/docs/x.md"}}),
    ("git commit after cd into this repository", ALLOW,
     {"tool_name": "Bash",
      "tool_input": {"command": f"cd {HERE}/{THIS} && git commit -m x"}}),
    ("reading the Phase 1 repository", ALLOW,
     {"tool_name": "Bash",
      "tool_input": {"command": f"git -C {HERE}/{PHASE1} log --oneline -5"}}),

    # --- must ALLOW: reading a sibling --------------------------------------
    ("cat a sibling file", ALLOW,
     {"tool_name": "Bash",
      "tool_input": {"command": f"cat {HERE}/{SIBLING}/CLAUDE.md"}}),
    ("grep a sibling", ALLOW,
     {"tool_name": "Bash",
      "tool_input": {"command": f"grep -n rule {HERE}/{SIBLING}/CLAUDE.md"}}),
    ("git log in a sibling", ALLOW,
     {"tool_name": "Bash",
      "tool_input": {"command": f"git -C {HERE}/{SIBLING} log --oneline -5"}}),
    ("ls a sibling directory", ALLOW,
     {"tool_name": "Bash",
      "tool_input": {"command": f"ls {HERE}/{SIBLING}/.claude/hooks/"}}),

    # --- must ALLOW: the regressions the first version caused ---------------
    ("grep whose PATTERN names cmdlets, run against a sibling", ALLOW,
     {"tool_name": "Bash",
      "tool_input": {"command":
                     f"grep -cE 'New-Item|Remove-Item|Set-Content' {HERE}/{SIBLING}/x.ps1"}}),
    ("writing in THIS repo a file whose text mentions the siblings", ALLOW,
     {"tool_name": "Bash",
      "tool_input": {"command":
                     f"echo 'never write to {OTHER} or {SIBLING}' > "
                     f"{HERE}/{THIS}/docs/rule.md"}}),

    # --- Sprint 25 IMP-3: a FOLDER named for a sibling, not a file name ------
    ("Write tool into the evidence library's data folder", BLOCK,
     {"tool_name": "Write",
      "tool_input": {"file_path": f"D:/Data/Harold/{SIBLING}/store/x.db"}}),
    # Under a root that does not exist, so `realpath` cannot restore the
    # folder's true case on Windows and the case fold itself is what is tested.
    ("Write tool into a sibling spelled in lower case", BLOCK,
     {"tool_name": "Write",
      "tool_input": {"file_path": f"Z:/no-such-root/{SIBLING.lower()}/x.md"}}),
    # Windows opens "name.", "name " and "name:stream" as the folder "name";
    # an exact match without canonicalizing would let each one through
    # (security review of 2af9045).
    ("Write tool into a sibling with a trailing dot", BLOCK,
     {"tool_name": "Write",
      "tool_input": {"file_path": f"{HERE}/{SIBLING}./x.md"}}),
    ("Write tool into a sibling with a trailing space", BLOCK,
     {"tool_name": "Write",
      "tool_input": {"file_path": f"{HERE}/{SIBLING} /x.md"}}),
    ("Write tool into a sibling through a stream suffix", BLOCK,
     {"tool_name": "Write",
      "tool_input": {"file_path": f"{HERE}/{SIBLING}::$INDEX_ALLOCATION/x.md"}}),
    ("Write tool in this repository, file named after a sibling", ALLOW,
     {"tool_name": "Write",
      "tool_input": {"file_path":
                     f"{HERE}/{THIS}/docs/phase2/{SIBLING.upper()}_PROPOSALS.md"}}),
    ("Edit tool in this repository, file named after the Phase 1 repo", ALLOW,
     {"tool_name": "Edit",
      "tool_input": {"file_path": f"{HERE}/{THIS}/docs/{PHASE1}_notes.md"}}),

    # --- Sprint 26 Task I: a sibling's Claude Code project directory --------
    ("Write tool into a sibling's Claude Code memory", BLOCK,
     {"tool_name": "Write",
      "tool_input": {"file_path": f"{PROJECTS}/D--Data-Harold-github-"
                                  f"{SIBLING}/memory/x.md"}}),
    ("Edit tool into the project directory of a session in a sibling's "
     "subfolder", BLOCK,
     {"tool_name": "Edit",
      "tool_input": {"file_path": f"{PROJECTS}/D--Data-Harold-github-"
                                  f"{OTHER}-docs/memory/x.md"}}),
    ("Write tool into the Phase 1 repository's Claude Code memory", BLOCK,
     {"tool_name": "Write",
      "tool_input": {"file_path": f"{PROJECTS}/D--Data-Harold-github-"
                                  f"{PHASE1}/memory/x.md"}}),
    ("Write tool into this repository's own Claude Code memory", ALLOW,
     {"tool_name": "Write",
      "tool_input": {"file_path": f"{PROJECTS}/D--Data-Harold-github-"
                                  f"{THIS}/memory/x.md"}}),
    ("Write tool into a folder outside .claude/projects ending in a "
     "sibling's name", ALLOW,
     {"tool_name": "Write",
      "tool_input": {"file_path": f"{HERE}/{THIS}/docs/notes-{SIBLING}/x.md"}}),

    # --- must ALLOW: ordinary work in this repository -----------------------
    ("Write tool in this repository", ALLOW,
     {"tool_name": "Write",
      "tool_input": {"file_path": str(ROOT / "docs" / "scratch.md")}}),
    ("git commit in this repository", ALLOW,
     {"tool_name": "Bash", "tool_input": {"command": "git commit -m x"}}),
]


def test_the_hook_file_exists():
    assert HOOK.exists(), f"{HOOK} is missing; the boundary would be unenforced"


# NO skipif. This test ran only where PowerShell was on PATH until Sprint 17
# Task H measured the suite on both platforms and found 15 cases skipping on
# Linux. The gate was a leftover from the PowerShell era: the hook under test
# is block_cross_repo_write.py, a PYTHON file invoked through sys.executable,
# so PowerShell has nothing to do with it.
#
# The cost of the leftover was precise. CI is ubuntu-latest, so the guard
# enforcing the team lead's cross-repo boundary -- the rule added after a
# session wrote into EvidenceBasedDB -- was never actually exercised there.
# It passed by being skipped.
@pytest.mark.parametrize("name,expected,payload", CASES, ids=[c[0] for c in CASES])
def test_guard_decides_correctly(name, expected, payload, tmp_path):
    f = tmp_path / "payload.json"
    f.write_text(json.dumps(payload), encoding="utf-8")
    with f.open("rb") as stdin:
        r = subprocess.run([sys.executable, str(HOOK)],
                           stdin=stdin, capture_output=True)
    verb = "BLOCK" if expected == BLOCK else "ALLOW"
    assert r.returncode == expected, (
        f"expected the guard to {verb} ({expected}) for {name!r}, got "
        f"{r.returncode}. stderr: {r.stderr.decode(errors='replace')[:300]}")


def test_the_folder_match_cases_can_fail():
    """Sprint 25 IMP-3: each new case must go red when the rule it pins breaks.

    Reverting to the old substring match must turn the file-name ALLOW cases
    red; dropping the case fold must turn the lower-case BLOCK case red;
    dropping the Windows canonicalization must turn the trailing-dot,
    trailing-space and stream-suffix BLOCK cases red.
    """
    from injection import Mutation, assert_can_fail

    new_cases = [c for c in CASES if c[0] in {
        "Write tool into a sibling spelled in lower case",
        "Write tool into a sibling with a trailing dot",
        "Write tool into a sibling with a trailing space",
        "Write tool into a sibling through a stream suffix",
        "Write tool in this repository, file named after a sibling",
        "Edit tool in this repository, file named after the Phase 1 repo"}]
    assert len(new_cases) == 6

    def run() -> bool:
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            for name, expected, payload in new_cases:
                f = Path(d) / "payload.json"
                f.write_text(json.dumps(payload), encoding="utf-8")
                with f.open("rb") as stdin:
                    r = subprocess.run([sys.executable, str(HOOK)],
                                       stdin=stdin, capture_output=True)
                if r.returncode != expected:
                    return False
        return True

    # The pre-IMP-3 behavior: the forbidden name anywhere in the path.
    substring = [
        Mutation(HOOK, "            if folder in forbidden:",
                 "            if any(k in candidate.lower() for k in forbidden):",
                 expect_occurrences=1),
    ]
    assert_can_fail(substring, run, "substring match blocks file names")

    # Both sides of the comparison are folded, so both folds must go: removing
    # one alone still compares lower case with lower case and stays green.
    no_fold = [
        Mutation(HOOK, '    return part.rstrip(". ").lower()',
                 '    return part.rstrip(". ")', expect_occurrences=1),
        Mutation(HOOK, "    forbidden = {repo.lower(): repo for",
                 "    forbidden = {repo: repo for", expect_occurrences=1),
    ]
    assert_can_fail(no_fold, run, "case-sensitive match misses lower case")

    # Exact match with no Windows canonicalization (the 2af9045 regression).
    # On Windows `realpath` also strips trailing dots and spaces, so the two
    # defenses cover each other there; both go, or the proof stays green.
    # On Linux (CI) `_canonical_folder` is the only one that applies.
    no_canon = [
        Mutation(HOOK, "        candidates.append(os.path.realpath(path))",
                 "        pass", expect_occurrences=1),
        Mutation(HOOK, '    return part.rstrip(". ").lower()',
                 "    return part.lower()", expect_occurrences=1),
        Mutation(HOOK, '        part = part.split(":", 1)[0]',
                 "        part = part", expect_occurrences=1),
    ]
    assert_can_fail(no_canon, run, "uncanonicalized names slip past")


def test_the_project_directory_cases_can_fail():
    """Sprint 26 Task I: each project-directory case goes red when its rule
    breaks. Without the check, the three BLOCK cases pass through; matching
    only at the end misses the subfolder session; dropping the
    `.claude/projects` anchor blocks the folder elsewhere; blocking every
    project directory blocks this repository's own memory."""
    from injection import Mutation, assert_can_fail

    names = {
        "Write tool into a sibling's Claude Code memory",
        "Edit tool into the project directory of a session in a sibling's "
        "subfolder",
        "Write tool into the Phase 1 repository's Claude Code memory",
        "Write tool into this repository's own Claude Code memory",
        "Write tool into a folder outside .claude/projects ending in a "
        "sibling's name"}
    new_cases = [c for c in CASES if c[0] in names]
    assert len(new_cases) == 5

    def run() -> bool:
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            for name, expected, payload in new_cases:
                f = Path(d) / "payload.json"
                f.write_text(json.dumps(payload), encoding="utf-8")
                with f.open("rb") as stdin:
                    r = subprocess.run([sys.executable, str(HOOK)],
                                       stdin=stdin, capture_output=True)
                if r.returncode != expected:
                    return False
        return True

    anchor = ('            if i >= 2 and folders[i - 2:i] == '
              '[".claude", "projects"]:')
    match = ('                    if folder.endswith("-" + key) or '
             'f"-{key}-" in folder:')
    assert_can_fail([Mutation(HOOK, anchor, "            if False:",
                              expect_occurrences=1)],
                    run, "no project-directory check")
    assert_can_fail([Mutation(HOOK, match,
                              '                    if folder.endswith('
                              '"-" + key):', expect_occurrences=1)],
                    run, "end-only match misses a subfolder session")
    assert_can_fail([Mutation(HOOK, anchor, "            if True:",
                              expect_occurrences=1)],
                    run, "unanchored match blocks folders elsewhere")
    assert_can_fail([Mutation(HOOK, match, "                    if True:",
                              expect_occurrences=1)],
                    run, "blocking every project directory")


def test_the_guard_is_registered_and_its_path_resolves():
    """A hook registered at a path that does not resolve cannot fire.

    Not hypothetical: two hooks here were registered with a single backslash
    before `block-`, which JSON parses as U+0008, and never ran. The same bug
    was reproduced while writing THIS guard and caught by this check.
    """
    settings = json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))
    commands = [h.get("command", "")
                for matchers in settings.get("hooks", {}).values()
                for m in matchers for h in m.get("hooks", [])]

    # Match the STEM, not the extension: asserting on ".ps1" is what made this
    # test fail on the very conversion it should have survived.
    mine = [c for c in commands
            if "cross-repo-write" in c or "cross_repo_write" in c]
    assert mine, ("the cross-repository guard is not registered in "
                  ".claude/settings.json")

    for c in mine:
        ctrl = [hex(ord(ch)) for ch in c if ord(ch) < 32]
        assert not ctrl, f"control characters {ctrl} in the registered command: {c!r}"
        # Commands now use forward slashes (F78: they work on both OSes and
        # cannot be eaten as an escape), so split on either separator.
        name = c.rstrip('"').replace("\\", "/").split("/")[-1]
        assert (ROOT / ".claude" / "hooks" / name).exists(), \
            f"registered hook {name!r} does not resolve to a file"
