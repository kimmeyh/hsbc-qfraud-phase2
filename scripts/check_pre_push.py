"""Refuse a push whose tree no passing `select_proofs.py --tests` run tested
(Sprint 32 i2).

Run by `.githooks/pre-push`, which git gives one line per ref on stdin:
`<local ref> <local sha> <remote ref> <remote sha>`. A ref is admitted
when a recorded passing run (`select_proofs.passed_runs`) has:
  - the same tree as the pushed commit, less `select_proofs.UNTESTED_OK`;
  - a merge base that is an ancestor of the remote's current commit, so
    the run's diff covered every commit being pushed. For a new remote
    branch, the base must be an ancestor of `origin/develop`.
A deleted ref is admitted. No override flag.

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
FIX = ("Run `<venv python> scripts/select_proofs.py --tests --base "
       "origin/<branch>` on the committed tree, then push again.")


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
    why = [w for w in (problem(ln, runs) for ln in lines) if w]
    for w in why:
        print(f"BLOCKED push: {w}.", file=sys.stderr)
    if why:
        print(FIX, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.stdin.read().splitlines()))
