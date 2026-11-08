"""No two red proofs make the same break (Sprint 31 D17 option 1 d, V13).

A proof shows that one check can fail by making one mutation; a second
proof with the same mutation (same old text, same new text) shows
nothing new and costs a run. More than one proof per test file stays
allowed: a file with five refusals needs five.

The scan reads each test file's syntax tree and collects the (old, new)
pairs of every `Mutation(target, old, new, ...)` whose old and new are
string literals, directly or through the names of a `for` loop over a
literal table of tuples. A mutation built from computed strings is not
seen; that is the gap, stated here so it is not mistaken for coverage.
Pairs are compared by text and by the target's source text, so the same
edit to two different files is not a duplicate.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
THIS = Path(__file__).relative_to(ROOT).as_posix()
sys.path.insert(0, str(HERE))


def _const(node):
    return node.value if isinstance(node, ast.Constant) and \
        isinstance(node.value, str) else None


def _is_mutation(call: ast.Call) -> bool:
    f = call.func
    return (isinstance(f, ast.Name) and f.id == "Mutation") or \
        (isinstance(f, ast.Attribute) and f.attr == "Mutation")


def _in_proof(node, parents) -> bool:
    """The mutation is made inside an `assert_can_fail(...)` call: a red
    proof, not a test of the mutation machinery itself."""
    p = parents.get(node)
    while p is not None:
        if isinstance(p, ast.Call) and ast.unparse(p.func).endswith(
                "assert_can_fail"):
            return True
        p = parents.get(p)
    return False


def _loop_rows(loop: ast.For):
    """[{name: node}] for `for a, b, ... in ((...), (...)):`."""
    if not isinstance(loop.target, ast.Tuple) or not isinstance(
            loop.iter, (ast.Tuple, ast.List)):
        return []
    names = [t.id if isinstance(t, ast.Name) else None
             for t in loop.target.elts]
    rows = []
    for row in loop.iter.elts:
        if isinstance(row, ast.Tuple) and len(row.elts) == len(names):
            rows.append({n: v for n, v in zip(names, row.elts) if n})
    return rows


def mutations(source: str) -> list[tuple[str, str, str, int]]:
    """(target text, old, new, line) for each literal mutation."""
    tree = ast.parse(source)
    # `SRC = ROOT / "scripts" / "x.py"` (module level or in the test)
    # stands for its value, so `SRC` or `page` in two files compares by
    # the file it names.
    named = {t.id: ast.unparse(n.value) for n in ast.walk(tree)
             if isinstance(n, ast.Assign) for t in n.targets
             if isinstance(t, ast.Name)}

    def resolve(text: str) -> str:
        return named.get(text, text)
    parents = {}
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            parents[child] = node
    out = []
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and _is_mutation(node)
                and len(node.args) >= 3 and _in_proof(node, parents)):
            continue
        target = ast.unparse(node.args[0])
        old, new = node.args[1], node.args[2]
        if _const(old) is not None and _const(new) is not None:
            out.append((resolve(target), _const(old), _const(new),
                        node.lineno))
            continue
        p = parents.get(node)
        while p is not None and not isinstance(p, ast.For):
            p = parents.get(p)
        if p is None:
            continue
        for row in _loop_rows(p):
            t = row.get(target) if isinstance(node.args[0], ast.Name) else None
            o = row.get(old.id) if isinstance(old, ast.Name) else old
            n = row.get(new.id) if isinstance(new, ast.Name) else new
            if _const(o) is not None and _const(n) is not None:
                tt = ast.unparse(t) if t is not None else target
                out.append((resolve(tt), _const(o), _const(n),
                            getattr(o, "lineno", node.lineno)))
    return out


def duplicates(sources: dict[str, str]) -> list[str]:
    seen: dict[tuple, str] = {}
    out = []
    for name, src in sorted(sources.items()):
        for target, old, new, line in mutations(src):
            key = (target, old, new)
            where = f"{name}:{line}"
            if key in seen:
                out.append(f"{where} repeats the mutation at {seen[key]}: "
                           f"{old[:50]!r} -> {new[:50]!r}")
            else:
                seen[key] = where
    return out


# The tests of `assert_can_fail` itself, which mutate a pytest fixture
# file on purpose many times; they are not proofs of repository files.
EXEMPT = frozenset({"experiments/src/test_injection.py"})


def _sources() -> dict[str, str]:
    return {name: p.read_text(encoding="utf-8")
            for p in sorted(HERE.glob("test_*.py"))
            if (name := p.relative_to(ROOT).as_posix()) not in EXEMPT}


def test_the_exempt_files_exist():
    assert all((ROOT / f).is_file() for f in EXEMPT)


def test_the_scan_reads_both_forms():
    src = ('def t():\n'
           '    assert_can_fail([Mutation(SRC, "a\\n", "b\\n")], run, "l")\n'
           '    for old, new, label in (("c", "d", "x"), ("e", "f", "y")):\n'
           '        assert_can_fail([Mutation(SRC, old, new,\n'
           '                                  expect_occurrences=1)], run, label)\n'
           '    Mutation(SRC, "g", "h").apply()  # machinery test, not a proof\n')
    got = [(t, o, n) for t, o, n, _ in mutations(src)]
    assert got == [("SRC", "a\n", "b\n"), ("SRC", "c", "d"), ("SRC", "e", "f")]


def test_a_repeated_mutation_is_found():
    one = 'assert_can_fail([Mutation(SRC, "old", "new")], run, "l")\n'
    assert duplicates({"a.py": one, "b.py": "x = 1\n"}) == []
    assert len(duplicates({"a.py": one, "b.py": one})) == 1
    other = 'assert_can_fail([Mutation(OTHER, "old", "new")], run, "l")\n'
    assert duplicates({"a.py": one, "b.py": other}) == []
    # The same name for two different files is not a repeat.
    a = 'SRC = ROOT / "a.py"\n' + one
    b = 'SRC = ROOT / "b.py"\n' + one
    assert duplicates({"a.py": a, "b.py": b}) == []


def test_no_two_proofs_make_the_same_break():
    found = duplicates(_sources())
    assert not found, (f"{len(found)} repeated proof mutation(s):\n"
                       + "\n".join(found))


def test_the_duplicate_rule_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    me = Path(__file__)
    for old, new, test, label in (
            ("            if key in seen:\n", "            if False:\n",
             "test_a_repeated_mutation_is_found", "a repeat not found"),
            ("            key = (target, old, new)\n",
             "            key = (old, new)\n",
             "test_a_repeated_mutation_is_found",
             "the same edit to two files read as a repeat"),
            ('            if (name := p.relative_to(ROOT).as_posix()) not in EXEMPT}\n',
             '            if (name := p.relative_to(ROOT).as_posix()) or EXEMPT}\n',
             "test_no_two_proofs_make_the_same_break",
             "the scan reading every file, exempt or not"),
            ("        for row in _loop_rows(p):\n",
             "        for row in []:\n",
             "test_the_scan_reads_both_forms", "a loop table not read"),
            ("                and len(node.args) >= 3 and _in_proof(node, parents)):\n",
             "                and len(node.args) >= 3):\n",
             "test_the_scan_reads_both_forms",
             "a machinery test counted as a proof")):
        assert_can_fail([Mutation(me, old, new, expect_occurrences=1)],
                        lambda test=test: run_pytest(f"{THIS}::{test}", ROOT),
                        label)
