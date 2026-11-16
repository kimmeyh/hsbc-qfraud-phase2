"""The pre-push gate refuses a tree no passing `--tests` run tested (Sprint 32 i2).

Each rule term has its own test on a scratch repository: the tree, the
merge base, a run narrowed by `--`, an uncommitted change, the status file
exception and a delete. One test runs the REAL hook through `git push` to a
scratch bare remote, as `test_commit_msg_hook.py` does for its gate. No test
pushes to a real remote.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / ".githooks" / "pre-push"
SP = ROOT / "scripts" / "select_proofs.py"
CPP = ROOT / "scripts" / "check_pre_push.py"
THIS = Path(__file__).relative_to(ROOT).as_posix()
sys.path.insert(0, str(ROOT / "scripts"))

import check_pre_push as cpp  # noqa: E402
import select_proofs as sp  # noqa: E402

pytestmark = pytest.mark.skipif(shutil.which("git") is None,
                                reason="git is not installed")
ZERO = "0" * 40


def _git(cwd: Path, *a: str) -> str:
    r = subprocess.run(["git", *a], cwd=cwd, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return r.stdout.strip()


def _commit(cwd: Path, name: str, text: str) -> str:
    (cwd / name).parent.mkdir(parents=True, exist_ok=True)
    (cwd / name).write_text(text, encoding="utf-8")
    _git(cwd, "add", name)
    _git(cwd, "commit", "-q", "-m", f"change {name}")
    return _git(cwd, "rev-parse", "HEAD")


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """develop at A (also origin/develop), branch feat at B."""
    w = tmp_path / "work"
    w.mkdir()
    _git(w, "init", "-q", "-b", "develop")
    _git(w, "config", "user.email", "t@example.invalid")
    _git(w, "config", "user.name", "t")
    _git(w, "config", "commit.gpgsign", "false")
    (w / "scripts").mkdir()
    (w / ".githooks").mkdir()
    # Bytes, so a CRLF conversion cannot break the sh shebang.
    (w / ".githooks" / "pre-push").write_bytes(HOOK.read_bytes())
    (w / "scripts" / "select_proofs.py").write_bytes(SP.read_bytes())
    (w / "scripts" / "check_pre_push.py").write_bytes(CPP.read_bytes())
    # As in this repository: the hook's import writes a bytecode cache.
    (w / ".gitignore").write_text("__pycache__/\n", encoding="utf-8")
    _git(w, "add", ".")
    a = _commit(w, ".claude/sprint_status.json", "{}\n")
    _git(w, "update-ref", "refs/remotes/origin/develop", a)
    _git(w, "checkout", "-q", "-b", "feat")
    b = _commit(w, "mod.py", "x = 1\n")
    monkeypatch.setattr(sp, "ROOT", w)
    return w, a, b


def _push(sha: str, remote: str) -> list[str]:
    return [f"refs/heads/feat {sha} refs/heads/feat {remote}"]


def test_a_tested_tree_is_admitted(repo):
    w, a, b = repo
    assert sp.note_pass(sp.fingerprint("HEAD"), a, []).startswith("recorded")
    assert cpp.main(_push(b, a)) == 0
    assert cpp.main(_push(b, ZERO)) == 0          # a new remote branch


def test_an_untested_tree_is_refused(repo):
    w, a, b = repo
    sp.note_pass(sp.fingerprint("HEAD"), a, [])
    c = _commit(w, "mod.py", "x = 2\n")
    assert cpp.problem(_push(c, a)[0], sp.passed_runs()) is not None
    assert cpp.main(_push(c, a)) == 1


def test_a_run_from_a_later_base_is_refused(repo):
    # `--base HEAD` on a committed tree selects almost nothing; its base,
    # B, is not an ancestor of the remote's A, so it covers no push.
    w, a, b = repo
    sp.note_pass(sp.fingerprint("HEAD"), b, [])
    why = cpp.problem(_push(b, a)[0], sp.passed_runs())
    assert why is not None and "did not cover" in why
    assert cpp.main(_push(b, ZERO)) == 1           # B is not on develop


def test_a_narrowed_run_records_nothing(repo):
    w, a, b = repo
    why = sp.note_pass(sp.fingerprint("HEAD"), a, ["-k", "one_test"])
    assert why.startswith("not recorded") and sp.passed_runs() == []


def test_an_uncommitted_change_records_nothing(repo):
    w, a, b = repo
    (w / "new.py").write_text("y = 1\n", encoding="utf-8")      # untracked
    assert sp.note_pass(sp.fingerprint("HEAD"), a, []).startswith(
        "not recorded")
    (w / "new.py").unlink()
    (w / "mod.py").write_text("x = 9\n", encoding="utf-8")      # modified
    assert sp.note_pass(sp.fingerprint("HEAD"), a, []).startswith(
        "not recorded")
    assert sp.passed_runs() == []


def test_the_status_file_may_differ(repo):
    # The timer changes it all sprint; a run with it dirty still records,
    # and a commit of it alone does not need a new run.
    w, a, b = repo
    (w / ".claude" / "sprint_status.json").write_text('{"t": 1}\n',
                                                      encoding="utf-8")
    assert sp.note_pass(sp.fingerprint("HEAD"), a, []).startswith("recorded")
    _git(w, "add", ".claude/sprint_status.json")
    _git(w, "commit", "-q", "-m", "status")
    assert cpp.main(_push(_git(w, "rev-parse", "HEAD"), a)) == 0


def test_a_delete_is_admitted(repo):
    w, a, b = repo
    assert cpp.main([f"(delete) {ZERO} refs/heads/feat {b}"]) == 0


def test_the_real_hook_refuses_and_admits(repo, tmp_path):
    w, a, b = repo
    remote = tmp_path / "remote.git"
    _git(tmp_path, "init", "-q", "--bare", str(remote))
    _git(w, "remote", "add", "origin", str(remote))
    _git(w, "config", "core.hooksPath", ".githooks")

    def push():
        return subprocess.run(["git", "push", "-q", "origin", "feat"],
                              cwd=w, capture_output=True, text=True)
    refused = push()
    assert refused.returncode != 0 and "BLOCKED push" in refused.stderr
    noted = sp.note_pass(sp.fingerprint("HEAD"), a, [])
    assert noted.startswith("recorded"), noted
    admitted = push()
    assert admitted.returncode == 0, admitted.stderr


def test_the_hook_is_tracked_with_lf_endings():
    assert b"\r\n" not in HOOK.read_bytes(), "CRLF breaks the sh shebang"
    tracked = subprocess.run(["git", "ls-files", "--error-unmatch",
                              ".githooks/pre-push"], cwd=ROOT,
                             capture_output=True)
    assert tracked.returncode == 0, "the hook must be tracked by git"


def test_the_push_check_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest

    def test(name):
        return lambda: run_pytest(f"{THIS}::{name}", ROOT)
    for path, old, new, name, label in (
            (CPP, "    same_tree = [m for f, m in runs if f == fp]\n",
             "    same_tree = [m for f, m in runs]\n",
             "test_an_untested_tree_is_refused", "an untested tree admitted"),
            (CPP, "    if not any(is_ancestor(m, anchor) for m in "
                  "same_tree):\n", "    if False:\n",
             "test_a_run_from_a_later_base_is_refused",
             "a run from a later base admitted"),
            (CPP, '    if set(local_sha) == {"0"}:                      '
                  "# a delete\n", "    if False:\n",
             "test_a_delete_is_admitted", "a delete refused"),
            (SP, "    if extra:\n", "    if False:\n",
             "test_a_narrowed_run_records_nothing",
             "a narrowed run recorded"),
            (SP, "    if before is None or other_changes():\n",
             "    if before is None:\n",
             "test_an_uncommitted_change_records_nothing",
             "an uncommitted change recorded"),
            (SP, '             if ln.split("\\t", 1)[1] not in '
                 "UNTESTED_OK]\n", "             if True]\n",
             "test_the_status_file_may_differ",
             "the status file read as code")):
        assert_can_fail([Mutation(path, old, new, expect_occurrences=1)],
                        test(name), label)
