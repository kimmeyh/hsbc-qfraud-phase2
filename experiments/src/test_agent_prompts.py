"""Every kept agent launch prompt keeps its restart section (F168 part 7).

F168 part 1 (Sprint 30): a usage limit stops an agent mid-task, so each
prompt in `docs/agent_prompts/` tells the agent to read its progress file
first, skip finished units, save each unit when checked, mark the end and
say what it resumed. A prompt that loses any of these loses work at the
next limit, silently, because the agent still runs.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROMPTS = ROOT / "docs" / "agent_prompts"
THIS = Path(__file__).relative_to(ROOT).as_posix()
KINDS = ("ci_fix.md", "review.md", "fresh_eyes.md", "research.md")

# Each term of the section, as a phrase the agent must be given.
TERMS = {
    "progress folder": ".claude/agent_progress/<name>/",
    "read first": "progress.md` there FIRST",
    "skip finished units": "Skip every",
    "save each unit": "append one line",
    "no device call": "Never send a device call",
    "end marker": "write `DONE` as the last line",
    "say what resumed": "say what you resumed",
}


def section(text: str) -> str:
    """The body of the "Progress and restart" section, or ""."""
    m = re.search(r"^## Progress and restart\n(.*?)(?=^## |\Z)", text,
                  re.S | re.M)
    return m.group(1) if m else ""


def problems(text: str) -> list[str]:
    body = section(text)
    if not body:
        return ["no '## Progress and restart' section"]
    flat = " ".join(body.split())
    return [f"restart section lacks: {name}" for name, phrase in TERMS.items()
            if " ".join(phrase.split()) not in flat]


def test_each_agent_kind_has_a_kept_prompt():
    assert sorted(p.name for p in PROMPTS.glob("*.md")
                  if p.name != "README.md") == sorted(KINDS)


def test_every_kept_prompt_has_its_restart_section():
    bad = {p.name: problems(p.read_text(encoding="utf-8"))
           for p in sorted(PROMPTS.glob("*.md")) if p.name != "README.md"}
    assert not {k: v for k, v in bad.items() if v}, bad


def test_a_prompt_without_the_section_or_a_term_is_refused():
    good = (PROMPTS / "review.md").read_text(encoding="utf-8")
    assert problems(good) == []
    assert problems(good.replace("## Progress and restart", "## Notes")) == [
        "no '## Progress and restart' section"]
    assert problems(good.replace("Never send a device call", "Avoid")) == [
        "restart section lacks: no device call"]


def test_the_process_doc_points_to_the_prompts():
    wf = (ROOT / "docs" / "SPRINT_EXECUTION_WORKFLOW.md").read_text(
        encoding="utf-8")
    assert "docs/agent_prompts/" in wf


def test_the_restart_rule_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    target = PROMPTS / "ci_fix.md"
    assert_can_fail([Mutation(target, "## Progress and restart\n",
                              "## Notes\n", expect_occurrences=1)],
                    lambda: run_pytest(f"{THIS}::test_every_kept_prompt_has_"
                                       "its_restart_section", ROOT),
                    "a kept prompt losing its restart section")
    assert_can_fail([Mutation(target, "- When you finish, write `DONE` as "
                              "the last line of `progress.md`.\n", "",
                              expect_occurrences=1)],
                    lambda: run_pytest(f"{THIS}::test_every_kept_prompt_has_"
                                       "its_restart_section", ROOT),
                    "a kept prompt losing its end marker")
