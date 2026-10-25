"""Every shrink-only list in a test module is pinned by `frozen_list.check`.

Sprint 28 IMP-1. The outcome guard's exempt list could grow while its test
stayed green (four PR #46 reviewers), and three lists in
`test_device_store_required.py` had the same hole. Each was pinned by a
count or by nothing. This guard fails a test module that keeps a list named
like a shrink-only list and never passes it to `frozen_list.check`.

A shrink-only list is a module-level collection (a set, frozenset, dict,
list, tuple, or an expression building one) whose name ends `_BEFORE_RULE`,
`_FROZEN`, `_NOT_SUBMITTING` or `_EXEMPT`, or starts `EXEMPT_`. Allowlists
gated by a stated reason use other names (`ALLOWED`, `EXEMPT`) and are not
in scope.
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "experiments" / "src"
THIS = Path(__file__).relative_to(ROOT).as_posix()
NAME = re.compile(r"(_BEFORE_RULE|_FROZEN|_NOT_SUBMITTING|_EXEMPT)$|^EXEMPT_")
COLLECTION = (ast.Set, ast.Dict, ast.List, ast.Tuple, ast.BinOp,
              ast.SetComp, ast.DictComp, ast.ListComp)


def _is_collection(v) -> bool:
    if isinstance(v, COLLECTION):
        return True
    return (isinstance(v, ast.Call) and isinstance(v.func, ast.Name)
            and v.func.id in ("frozenset", "set", "dict", "tuple", "list"))


def _checked_names(tree) -> set[str]:
    out = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        f = node.func
        if not (isinstance(f, ast.Attribute) and f.attr == "check"
                and isinstance(f.value, ast.Name)
                and f.value.id in ("fl", "frozen_list")):
            continue
        for arg in node.args:
            out |= {n.id for n in ast.walk(arg) if isinstance(n, ast.Name)}
    return out


def unpinned(src: str) -> list[str]:
    tree = ast.parse(src)
    lists = []
    for node in tree.body:
        if isinstance(node, ast.Assign):
            targets, value = node.targets, node.value
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            targets, value = [node.target], node.value
        else:
            continue
        for t in targets:
            if isinstance(t, ast.Name) and NAME.search(t.id) \
                    and _is_collection(value):
                lists.append(t.id)
    checked = _checked_names(tree)
    return [n for n in lists if n not in checked]


def violations(src_dir: Path = SRC) -> dict[str, list[str]]:
    found = {p.name: unpinned(p.read_text(encoding="utf-8"))
             for p in sorted(src_dir.glob("test_*.py"))}
    return {k: v for k, v in found.items() if v}


def test_every_shrink_only_list_is_pinned():
    bad = violations()
    assert not bad, ("shrink-only lists not passed to frozen_list.check "
                     f"(Sprint 28 IMP-1): {bad}")


def test_the_guard_sees_the_real_lists():
    # A floor, so a scan that finds nothing cannot pass vacuously.
    seen = set()
    for p in SRC.glob("test_*.py"):
        tree = ast.parse(p.read_text(encoding="utf-8"))
        seen |= _checked_names(tree)
    assert {"EXEMPT_BEFORE_RULE", "PROVENANCE_EXEMPT", "PHASE1_FROZEN",
            "PHASE2_NOT_SUBMITTING", "PHASE2_SUBMIT_BEFORE_RULE",
            "UNSEEDED_BEFORE_RULE"} <= seen


def test_an_unpinned_list_is_caught():
    assert unpinned("X_BEFORE_RULE = {'a.py': 'why'}\n") == ["X_BEFORE_RULE"]
    assert unpinned("EXEMPT_NEW = frozenset({'a'})\n") == ["EXEMPT_NEW"]
    assert unpinned("Y_EXEMPT = BASE - DONE\n") == ["Y_EXEMPT"]


def test_a_pinned_list_passes_and_constants_are_out_of_scope():
    src = ("X_BEFORE_RULE = {'a.py': 'why'}\n"
           "X_COUNT_FROZEN = 3\n"            # a constant, not a list
           "EXEMPT = {'pkg'}\n"              # a reasoned allowlist
           "def test():\n"
           "    assert not fl.check(frozenset(X_BEFORE_RULE), O, SHA)\n")
    assert unpinned(src) == []


def test_the_pin_rule_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    assert_can_fail([Mutation(Path(__file__),
                              "    return [n for n in lists if n not in "
                              "checked]\n",
                              "    return []\n", expect_occurrences=1)],
                    lambda: run_pytest(
                        f"{THIS}::test_an_unpinned_list_is_caught", ROOT),
                    "an unpinned list")


def test_a_real_unpinned_list_is_caught():
    from injection import Mutation, assert_can_fail, run_pytest
    target = ROOT / "experiments" / "src" / "test_device_store_required.py"
    assert_can_fail([Mutation(target,
                              "           + fl.check(PHASE1_FROZEN, "
                              "PHASE1_FROZEN, PHASE1_FROZEN_SHA256)\n",
                              "", expect_occurrences=1)],
                    lambda: run_pytest(
                        f"{THIS}::test_every_shrink_only_list_is_pinned",
                        ROOT),
                    "the Phase 1 list unpinned")
