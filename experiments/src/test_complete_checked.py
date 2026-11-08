"""A Phase 2 result is marked complete only by a check that it is.

Sprint 31 i2 b (team lead, 2026-11-07). The PR 92 review found four places
that wrote `"complete": True` without checking (review class 2): `twins`
and Experiment 5's alignment stop (fixed in 961e564), F114 `--lr05` and
`f157_spectra_algorithms.run_rbf` (fixed with this test). A function in
`experiments/phase2/src/` that sets `complete` to a literal True must
refuse something earlier in the same function (`raise`, `sys.exit`,
`SystemExit`, `print("REFUSING ...")`), or be one of the places reviewed
on 2026-11-07 as complete by construction, listed below with the reason.
That list only shrinks (`frozen_list.check`).

The rule is a proxy: a refusal about something else also passes. Its job
is to make a new literal True a decision that is seen, not a default.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import frozen_list as fl  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
PHASE2 = ROOT / "experiments" / "phase2" / "src"

# Reviewed 2026-11-07 (Sprint 31 i2 b): each writes "complete" only after
# its whole plan ran, and any failure raises before. Never add to this.
COMPLETE_BY_CONSTRUCTION = {
    "f157_spectra_algorithms.py:run": "every dataset's seed-42 run and "
        "every seed of its plan, resumed seeds skipped, never dropped",
    "f158_fraud_types.py:main": "every seed in SEEDS",
    "f160_room_ieee.py:main": "one straight run, not resumable",
    "f166_ulb_algorithms.py:run": "seed 42 and every seed of its plan",
    "f169_plugin_bins.py:main": "every seed in fc.SEEDS",
    "f169_plugin_bins.py:main_lr05": "every seed in fc.SEEDS",
    "f170_missed_neighbors.py:main": "one straight run; ULB runs only when "
        "the simulator check fires, by the entry's rule",
    "f171_budgets.py:main": "one straight run, not resumable; "
        "check_recorded raises on a mismatch",
    "f171_missed_ieee.py:main": "one straight run, not resumable",
    "f174_ieee_algorithms.py:run": "every seed in SEEDS",
    "run_dirac3s_units.py:dry_run": "a dry-run file written once, after "
        "every request was built offline",
}
COMPLETE_BY_CONSTRUCTION_SHA256 = (
    "bdcb090140fbf5fc64732a41cfdf9b1b35a7f36ba1f89f18377b9a86fc80d08b")


def literal_true_lines(fn: ast.AST) -> list[int]:
    """Lines in `fn` that set `complete` to the literal True: a dict entry
    `"complete": True`, a keyword `complete=True`, or `x["complete"] = True`."""
    out = []
    for node in ast.walk(fn):
        if isinstance(node, ast.Dict):
            out += [v.lineno for k, v in zip(node.keys, node.values)
                    if isinstance(k, ast.Constant) and k.value == "complete"
                    and isinstance(v, ast.Constant) and v.value is True]
        elif isinstance(node, ast.keyword):
            if node.arg == "complete" and isinstance(node.value, ast.Constant) \
                    and node.value.value is True:
                out.append(node.value.lineno)
        elif isinstance(node, ast.Assign):
            if isinstance(node.value, ast.Constant) and node.value.value is True \
                    and any(isinstance(t, ast.Subscript)
                            and isinstance(t.slice, ast.Constant)
                            and t.slice.value == "complete"
                            for t in node.targets):
                out.append(node.lineno)
    return sorted(out)


def refusal_lines(fn: ast.AST) -> list[int]:
    """Lines in `fn` that refuse: `raise`, `sys.exit(...)`,
    `SystemExit(...)`, or a print or write whose text starts `REFUSING`."""
    out = []
    for node in ast.walk(fn):
        if isinstance(node, ast.Raise):
            out.append(node.lineno)
        elif isinstance(node, ast.Call):
            f = node.func
            name = f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", None)
            if name in ("exit", "SystemExit"):
                out.append(node.lineno)
            elif name in ("print", "write") and node.args:
                first = node.args[0]
                text = (first.value if isinstance(first, ast.Constant) else
                        first.values[0].value if isinstance(first, ast.JoinedStr)
                        and first.values and isinstance(first.values[0], ast.Constant)
                        else "")
                if isinstance(text, str) and text.startswith("REFUSING"):
                    out.append(node.lineno)
    return sorted(out)


def unchecked(src: str, module: str) -> list[str]:
    """`module:function` for each function that sets a literal True
    complete with no refusal on an earlier line."""
    out = []
    for fn in ast.walk(ast.parse(src)):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        sites, refs = literal_true_lines(fn), refusal_lines(fn)
        if any(not any(r < s for r in refs) for s in sites):
            out.append(f"{module}:{fn.name}")
    return out


def _all_unchecked() -> set[str]:
    return {name for p in sorted(PHASE2.glob("*.py"))
            if not p.name.startswith("test_")
            for name in unchecked(p.read_text(encoding="utf-8"), p.name)}


def test_every_literal_complete_is_checked_or_reviewed():
    new = sorted(_all_unchecked() - set(COMPLETE_BY_CONSTRUCTION))
    assert not new, (f"{new} mark a result complete with no refusal before "
                     "it: check that the run is complete first (Sprint 31 i2)")


def test_the_reviewed_list_only_shrinks():
    bad = fl.check(frozenset(COMPLETE_BY_CONSTRUCTION),
                   frozenset(COMPLETE_BY_CONSTRUCTION),
                   COMPLETE_BY_CONSTRUCTION_SHA256)
    assert not bad, bad
    stale = sorted(set(COMPLETE_BY_CONSTRUCTION) - _all_unchecked())
    assert not stale, (f"{stale} now check before they mark complete, or are "
                       "gone: remove them from the list")


SAMPLE = '''
def dict_form(rows):
    return {"rows": rows, "complete": True}

def keyword_form(rows):
    return _doc(rows, complete=True)

def subscript_form(doc):
    doc["complete"] = True

def checked_by_raise(rows):
    if len(rows) != 3:
        raise ValueError("short")
    return {"complete": True}

def checked_by_exit(rows):
    if len(rows) != 3:
        sys.exit("short")
    return {"complete": True}

def checked_by_print(rows):
    if not rows:
        print(f"REFUSING: {len(rows)} rows")
        return 2
    return _doc(rows, complete=True)

def refusal_after(rows):
    doc = {"complete": True}
    raise ValueError("too late")

def computed(rows):
    return {"complete": len(rows) == 3}

def other_print(rows):
    print("REFUSED nothing")
    return {"complete": True}
'''


def test_the_scan_sees_each_form():
    assert sorted(unchecked(SAMPLE, "m.py")) == [
        "m.py:dict_form", "m.py:keyword_form", "m.py:other_print",
        "m.py:refusal_after", "m.py:subscript_form"]


# ------------------------------------------------------------- red proofs
SELF = Path(__file__)
THIS = SELF.relative_to(ROOT).as_posix()


def test_each_rule_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    scan = f"{THIS}::test_the_scan_sees_each_form"
    shrink = f"{THIS}::test_the_reviewed_list_only_shrinks"
    real = f"{THIS}::test_every_literal_complete_is_checked_or_reviewed"
    for old, new, test, label in (
            ('if isinstance(k, ast.Constant) and k.value == "complete"\n',
             'if isinstance(k, ast.Constant) and k.value == "completed"\n',
             scan, "the dict form not seen"),
            ('if node.arg == "complete" and isinstance(node.value, ast.Constant) \\\n',
             'if node.arg == "completed" and isinstance(node.value, ast.Constant) \\\n',
             scan, "the keyword form not seen"),
            ('                            and t.slice.value == "complete"\n',
             '                            and t.slice.value == "completed"\n',
             scan, "the subscript form not seen"),
            ("        if isinstance(node, ast.Raise):\n            out.append",
             "        if False:\n            out.append",
             scan, "a raise not counted as a refusal"),
            ('if isinstance(text, str) and text.startswith("REFUSING"):\n',
             'if isinstance(text, str):\n',
             scan, "any print counted as a refusal"),
            ("        if any(not any(r < s for r in refs) for s in sites):\n",
             "        if any(not refs for s in sites):\n",
             scan, "a refusal after the site counted"),
            ('    "f158_fraud_types.py:main": "every seed in SEEDS",\n',
             '    "f158_fraud_types.py:main": "every seed in SEEDS", '
             '"f999_new.py:main": "x",\n',
             shrink, "a name added to the reviewed list"),
            ('    "f158_fraud_types.py:main": "every seed in SEEDS",\n', "",
             real, "a real unchecked place not caught")):
        assert_can_fail([Mutation(SELF, old, new, expect_occurrences=1)],
                        lambda test=test: run_pytest(test, ROOT), label)
