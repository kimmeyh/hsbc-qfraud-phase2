"""CI's two jobs keep their selections (Sprint 30 Task L, team lead D9).

The push job runs every test except the red proofs and the `slow` test;
the full job, on ready for review and on demand, runs the proofs too. The
proofs left the push job only because the full job is their replacement,
so each half is checked here: a push job that drops more than the proofs,
or a full job that drops them, or loses its trigger, fails.

`conftest.py` marks a proof from its source, following the module's own
helpers (`_proof(...)` in `test_outcome_record_required.py`), so a proof
that reaches `assert_can_fail` through a helper is marked too.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"
CONFTEST = ROOT / "conftest.py"
THIS = Path(__file__).relative_to(ROOT).as_posix()
sys.path.insert(0, str(Path(__file__).resolve().parent))


def _jobs() -> dict[str, str]:
    text = WORKFLOW.read_text(encoding="utf-8").replace("\r\n", "\n")
    body = text.split("\njobs:", 1)[1]
    head, full = body.split("\n  full:\n", 1)
    return {"test": head.split("\n  test:\n", 1)[1], "full": full}


def _pytest_lines(job: str) -> list[str]:
    return [ln.strip() for ln in job.splitlines()
            if ln.strip().startswith("run: pytest")]


def test_the_push_job_leaves_out_only_the_proofs_and_slow():
    assert _pytest_lines(_jobs()["test"]) == [
        'run: pytest -m "not proof and not slow" -q --durations=25']


def test_the_full_job_runs_the_proofs_on_ready_for_review():
    jobs = _jobs()
    assert _pytest_lines(jobs["full"]) == [
        'run: pytest -m "not slow" -q --durations=25']
    assert ("if: github.event.action == 'ready_for_review' || "
            "github.event_name == 'workflow_dispatch'" in jobs["full"])
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "types: [opened, synchronize, reopened, ready_for_review]" in text
    assert "Test run must leave the tree clean" in jobs["full"]


def _conftest():
    spec = importlib.util.spec_from_file_location("_root_conftest", CONFTEST)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_a_proof_is_marked_directly_and_through_a_helper():
    import test_f166_docs
    import test_outcome_record_required as orr
    is_proof = _conftest().is_proof
    item = lambda f: SimpleNamespace(function=f)  # noqa: E731
    assert is_proof(item(test_f166_docs.test_the_page_check_can_fail))
    assert is_proof(item(
        orr.test_a_new_exempt_name_is_caught_even_with_the_count_raised))
    assert not is_proof(item(
        test_f166_docs.test_the_committed_pages_are_what_the_generator_renders))
    assert not is_proof(item(orr.test_the_exempt_list_only_shrinks))


def test_the_selection_and_marking_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    node = f"{THIS}::test_a_proof_is_marked_directly_and_through_a_helper"
    for path, old, new, label in (
            (CONFTEST, '                if f"{n}(" not in calls and any(c in src for c in calls):\n',
             '                if False:\n',
             "a proof behind a helper left unmarked"),
            (CONFTEST, 'PROOF_CALLS = ("assert_can_fail(", "run_pytest(")\n',
             'PROOF_CALLS = ()\n',
             "no direct call marks a proof"),
            (CONFTEST, "    return any(call in src\n",
             "    return True or any(call in src\n",
             "every test marked a proof")):
        assert_can_fail([Mutation(path, old, new, expect_occurrences=1)],
                        lambda: run_pytest(node, ROOT), label)
    for old, new, test, label in (
            ('pytest -m "not proof and not slow" -q',
             'pytest -m "not proof and not slow and not hook" -q',
             "test_the_push_job_leaves_out_only_the_proofs_and_slow",
             "the push job leaves out more than the proofs"),
            ('pytest -m "not slow" -q', 'pytest -m "not proof and not slow" -q',
             "test_the_full_job_runs_the_proofs_on_ready_for_review",
             "the full job leaves out the proofs")):
        assert_can_fail([Mutation(WORKFLOW, old, new, expect_occurrences=1)],
                        lambda test=test: run_pytest(f"{THIS}::{test}", ROOT),
                        label)
