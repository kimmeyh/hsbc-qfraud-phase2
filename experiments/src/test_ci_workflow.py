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
        'run: pytest -m "not slow" -q --durations=25 --junitxml=${{ runner.temp }}/ci-full.xml']
    # Every non-draft event, so a push after ready for review runs the
    # proofs too (PR 74 review); the push job only on a draft.
    assert ("if: github.event_name == 'workflow_dispatch' || "
            "!github.event.pull_request.draft" in jobs["full"])
    assert ("if: github.event_name == 'pull_request' && "
            "github.event.pull_request.draft" in jobs["test"])
    text = WORKFLOW.read_text(encoding="utf-8").replace("\r\n", "\n")
    assert "types: [opened, synchronize, reopened, ready_for_review]" in text
    assert "\n  workflow_dispatch:\n" in text.split("\njobs:", 1)[0]
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


def test_a_test_named_like_a_helper_is_not_a_proof():
    # PR 74 review: a substring match found the helper `_fails(` in
    # `def test_the_wrong_endpoint_fails():` and dropped a regular guard
    # from the push job.
    import test_phase2_figures_resolve as pfr
    is_proof = _conftest().is_proof
    assert not is_proof(SimpleNamespace(
        function=pfr.test_the_wrong_endpoint_fails))
    assert is_proof(SimpleNamespace(
        function=pfr.test_the_per_document_pool_can_fail))


def test_the_selection_and_marking_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    node = f"{THIS}::test_a_proof_is_marked_directly_and_through_a_helper"
    named = f"{THIS}::test_a_test_named_like_a_helper_is_not_a_proof"
    for path, old, new, label, target in (
            (CONFTEST, "                if n not in calls and called & calls:\n",
             "                if False:\n",
             "a proof behind a helper left unmarked", node),
            (CONFTEST, 'PROOF_CALLS = frozenset({"assert_can_fail", "run_pytest"})\n',
             "PROOF_CALLS = frozenset()\n",
             "no direct call marks a proof", node),
            (CONFTEST, "    return bool(_called(fn) & _proof_calls(inspect.getmodule(fn)))\n",
             "    return True\n",
             "every test marked a proof", node),
            (CONFTEST, "    return bool(_called(fn) & _proof_calls(inspect.getmodule(fn)))\n",
             "    return any(c + '(' in inspect.getsource(fn)\n"
             "               for c in _proof_calls(inspect.getmodule(fn)))\n",
             "a test named like a helper marked by substring", named)):
        assert_can_fail([Mutation(path, old, new, expect_occurrences=1)],
                        lambda target=target: run_pytest(target, ROOT), label)
    for old, new, test, label in (
            ('pytest -m "not proof and not slow" -q',
             'pytest -m "not proof and not slow and not hook" -q',
             "test_the_push_job_leaves_out_only_the_proofs_and_slow",
             "the push job leaves out more than the proofs"),
            ('pytest -m "not slow" -q', 'pytest -m "not proof and not slow" -q',
             "test_the_full_job_runs_the_proofs_on_ready_for_review",
             "the full job leaves out the proofs"),
            ("    if: github.event_name == 'workflow_dispatch' || "
             "!github.event.pull_request.draft\n",
             "    if: github.event.action == 'ready_for_review'\n",
             "test_the_full_job_runs_the_proofs_on_ready_for_review",
             "a push after ready for review skips the proofs")):
        assert_can_fail([Mutation(WORKFLOW, old, new, expect_occurrences=1)],
                        lambda test=test: run_pytest(f"{THIS}::{test}", ROOT),
                        label)
