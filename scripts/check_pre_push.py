"""Refuse a push whose tree no passing `select_proofs.py --tests` run tested
(Sprint 32 i2).

Run by `.githooks/pre-push`, which git gives one line per ref on stdin:
`<local ref> <local sha> <remote ref> <remote sha>`. A ref is admitted
when a recorded passing run (`select_proofs.passed_runs`) has:
  - the same tree as the pushed commit, less `select_proofs.UNTESTED_OK`;
  - a merge base that is an ancestor of the remote's current commit, so
    the run's diff covered every commit being pushed. For a new remote
    branch, the base must be an ancestor of `origin/develop`.
A deleted ref is admitted, and so is a ref whose commit is already in the
remote commit's (or `origin/develop`'s) history: it pushes nothing new to
test. No override flag.

Why: Sprint 32 had two CI failures (5027f4f, c692eac) and Sprint 31 one
(dfb1694), each a change pushed before its own tests ran locally.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import select_proofs as sp  # noqa: E402

NEW_BRANCH_ANCHOR = "origin/develop"
# The base to name depends on the case: for a new remote branch,
# origin/<branch> does not exist yet (PR 116 short review).
FIX = ("Run `<venv python> scripts/select_proofs.py --tests --base {base}` "
       "on the committed tree, then push again.")
NEW_BRANCH_BASE = "origin/develop"
BRANCH_BASE = "origin/<branch>"


def is_ancestor(a: str, b: str) -> bool:
    return subprocess.run(["git", "merge-base", "--is-ancestor", a, b],
                          cwd=sp.ROOT, capture_output=True).returncode == 0


def problem(line: str, runs: list[tuple[str, str]]) -> str | None:
    """Why one pushed ref is refused, or None."""
    parts = line.split()
    if len(parts) != 4:
        return None
    local_ref, local_sha, _remote_ref, remote_sha = parts
    if set(local_sha) == {"0"}:                      # a delete
        return None
    anchor = NEW_BRANCH_ANCHOR if set(remote_sha) == {"0"} else remote_sha
    # Nothing new to cover: the commit is already in the anchor's history
    # (a tag on develop, a new branch made at a develop commit).
    if is_ancestor(f"{local_sha}^{{commit}}", anchor):
        return None
    fp = sp.fingerprint(local_sha)
    same_tree = [m for f, m in runs if f == fp]
    if not same_tree:
        return (f"{local_ref} ({local_sha[:9]}): no passing --tests run "
                "tested this tree")
    if not any(is_ancestor(m, anchor) for m in same_tree):
        return (f"{local_ref} ({local_sha[:9]}): the run that tested this "
                f"tree started after {anchor[:14]}, so it did not cover "
                "every pushed commit (or the remote commit is not fetched)")
    return None


def main(lines: list[str]) -> int:
    runs = sp.passed_runs()
    why = [(ln, w) for ln, w in ((ln, problem(ln, runs)) for ln in lines)
           if w]
    for _ln, w in why:
        print(f"BLOCKED push: {w}.", file=sys.stderr)
    if why:
        print(fix_hint([ln for ln, _w in why]), file=sys.stderr)
        return 1
    return 0


def fix_hint(lines: list[str]) -> str:
    """The command to run: a new remote branch has no origin/<branch>."""
    new = any(len(ln.split()) == 4 and set(ln.split()[3]) == {"0"}
              for ln in lines)
    return FIX.format(base=NEW_BRANCH_BASE if new else BRANCH_BASE)


if __name__ == "__main__":
    sys.exit(main(sys.stdin.read().splitlines()))
