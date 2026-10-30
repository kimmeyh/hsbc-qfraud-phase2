"""The commit-msg hook refuses an untracked feat or fix commit (Sprint 28 IMP-4).

The rule's cases run on `check_commit_issue.problem`; one test runs the REAL
hook in a scratch git repository, so git's behavior with the hook installed
is what is asserted, as `test_pre_commit_hook.py` does for its gate.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / ".githooks" / "commit-msg"
SCRIPT = ROOT / "scripts" / "check_commit_issue.py"
THIS = Path(__file__).relative_to(ROOT).as_posix()
sys.path.insert(0, str(ROOT / "scripts"))

import check_commit_issue as cci  # noqa: E402

BRANCH = "feature/20261019_Sprint_28"
STATUS = {"current_sprint": {"branch": BRANCH, "pr": 46,
                             "github_issues": [59, 60, 61],
                             "task_started": {"A": "t0", "B": "t1"},
                             "task_actuals": {"A": 5}}}


def test_a_feature_commit_without_its_issue_is_refused():
    # The shape of 39f9943, D4 part 1.
    assert cci.problem("feat: device_store, every device job stored\n",
                       BRANCH, STATUS)


def test_an_issue_or_the_pr_review_admits_it():
    assert cci.problem("feat: provenance (#61)\n", BRANCH, STATUS) is None
    assert cci.problem("fix: x\n\nPart of #60.\n", BRANCH, STATUS) is None
    assert cci.problem("fix: PR 46 review findings\n", BRANCH, STATUS) is None
    assert cci.problem("fix(guard): y (#59)\n", BRANCH, STATUS) is None


def test_an_issue_from_another_sprint_or_pr_does_not():
    assert cci.problem("feat: z (#12)\n", BRANCH, STATUS)
    assert cci.problem("fix: PR 32 review findings\n", BRANCH, STATUS)


def test_other_types_merges_and_other_branches_pass():
    for msg in ("docs: a\n", "chore: b\n", "test: c\n",
                "Merge branch 'develop'\n", "Revert \"feat: d\"\n"):
        assert cci.problem(msg, BRANCH, STATUS) is None, msg
    assert cci.problem("feat: e\n", "develop", STATUS) is None


def test_an_unreadable_status_file_blocks():
    assert cci.problem("feat: f (#61)\n", BRANCH, None)
    assert cci.problem("feat: f (#61)\n", BRANCH, {"current_sprint": []})


def test_a_status_file_for_another_branch_blocks():
    other = {"current_sprint": {**STATUS["current_sprint"],
                                "branch": "feature/x_Sprint_29"}}
    assert cci.problem("feat: f (#61)\n", BRANCH, other)


def test_comment_lines_are_not_the_message():
    assert cci.problem("# feat: (#61)\nfeat: g\n", BRANCH, STATUS)
    assert cci.problem("feat: g\n#\n# Please enter (#61)\n", BRANCH, STATUS)
    assert cci.problem("feat: g\n# ------------------------ >8 -------\n"
                       "#61 in the diff below\n", BRANCH, STATUS)


def _with(**fields):
    return {"current_sprint": {**STATUS["current_sprint"], **fields}}


def test_a_commit_with_no_timer_running_is_refused():
    # Sprint 29 IMP-4: Task C's work was committed with no timer.
    msg = "feat: h (#61)\n"
    assert cci.problem(msg, BRANCH, _with(task_started={})) is not None
    assert cci.problem(msg, BRANCH,
                       _with(task_actuals={"A": 5, "B": 7})) is not None
    assert cci.problem(msg, BRANCH,
                       _with(task_paused={"B": "t2"})) is not None
    assert cci.problem(msg, BRANCH, _with(task_started=[])) is not None
    assert "timer" in cci.problem(msg, BRANCH, _with(task_started={}))


def test_the_timer_rule_holds_for_the_pr_review_too():
    assert cci.problem("fix: PR 46 review\n", BRANCH,
                       _with(task_started={})) is not None


def test_a_running_timer_admits_and_other_types_need_none():
    assert cci.timed(STATUS["current_sprint"]) == ["B"]
    assert cci.problem("feat: h (#61)\n", BRANCH, STATUS) is None
    assert cci.problem("docs: i\n", BRANCH, _with(task_started={})) is None


def test_a_body_line_naming_the_issue_is_kept():
    # git commit -m "feat: x" -m "#61 is the task" keeps that line.
    assert cci.problem("feat: x\n\n#61 is the task\n", BRANCH, STATUS) is None


@pytest.mark.skipif(shutil.which("git") is None, reason="git is not installed")
def test_the_real_hook_refuses_and_admits(tmp_path):
    def git(*a):
        return subprocess.run(["git", *a], cwd=tmp_path, capture_output=True,
                              text=True)
    git("init", "-q", "-b", BRANCH)
    git("config", "user.email", "t@example.invalid")
    git("config", "user.name", "t")
    git("config", "commit.gpgsign", "false")
    (tmp_path / ".githooks").mkdir()
    (tmp_path / "scripts").mkdir()
    (tmp_path / ".claude").mkdir()
    # Bytes, so a CRLF conversion cannot break the sh shebang.
    (tmp_path / ".githooks" / "commit-msg").write_bytes(HOOK.read_bytes())
    (tmp_path / ".githooks" / "commit-msg").chmod(0o755)
    (tmp_path / "scripts" / "check_commit_issue.py").write_bytes(
        SCRIPT.read_bytes())
    (tmp_path / ".claude" / "sprint_status.json").write_text(
        json.dumps(STATUS), encoding="utf-8")
    git("config", "core.hooksPath", ".githooks")
    (tmp_path / "a.txt").write_text("a", encoding="utf-8")
    git("add", "a.txt")
    refused = git("commit", "-q", "-m", "feat: untracked work")
    assert refused.returncode != 0 and "BLOCKED" in refused.stderr
    admitted = git("commit", "-q", "-m", "feat: tracked work (#61)")
    assert admitted.returncode == 0, admitted.stderr


def test_the_rule_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    assert_can_fail([Mutation(SCRIPT,
                              "    if not (named & issues or review):\n",
                              "    if False:\n", expect_occurrences=1)],
                    lambda: run_pytest(
                        f"{THIS}::test_a_feature_commit_without_its_issue_"
                        "is_refused", ROOT),
                    "a feat commit with no issue")
    assert_can_fail([Mutation(SCRIPT,
                              '    if cur.get("branch") != branch:\n',
                              "    if False:\n", expect_occurrences=1)],
                    lambda: run_pytest(
                        f"{THIS}::test_a_status_file_for_another_branch_"
                        "blocks", ROOT),
                    "a status file for another branch")
    assert_can_fail([Mutation(SCRIPT,
                              "        if not COMMENT.match(ln):\n",
                              "        if not ln.startswith('#'):\n",
                              expect_occurrences=1)],
                    lambda: run_pytest(
                        f"{THIS}::test_a_body_line_naming_the_issue_is_kept",
                        ROOT),
                    "an issue line dropped as a comment")
    assert_can_fail([Mutation(SCRIPT, "    if not timed(cur):\n",
                              "    if False:\n", expect_occurrences=1)],
                    lambda: run_pytest(
                        f"{THIS}::test_a_commit_with_no_timer_running_is_"
                        "refused", ROOT),
                    "a commit with no timer running")
    assert_can_fail([Mutation(SCRIPT,
                              '                  and t not in part("task_paused"))\n',
                              "                  )\n", expect_occurrences=1)],
                    lambda: run_pytest(
                        f"{THIS}::test_a_commit_with_no_timer_running_is_"
                        "refused", ROOT),
                    "a paused timer counted as running")
