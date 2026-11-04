"""A long run resumes, keeps its finished units and marks its end (F168).

F168 part 2 (Sprint 30 D2, team lead 2026-10-31): a long run keeps its
finished units in its own result file, marked `complete: false`, and a
rerun resumes it through `provenance.start`, which accepts only an
unfinished result whose run id matches the gitignored sidecar. Part 4: a
status check reads the run's completion marker, `complete: true` in the
file and a final `complete` line on stdout, never the file's presence.

"Long run" is declared, not guessed: every Phase 2 module that calls
`provenance.start` states `LONG_RUN = True` or `LONG_RUN = False` at module
level, so a new module has to choose. A `LONG_RUN = True` module must:
  - call `provenance.start` at least once without `resumable=False`;
  - write a `"complete"` field;
  - print the `complete` marker.
The resume itself, a run stopped mid-way that skips its finished units,
is exercised end to end in `test_a_stopped_run_resumes_and_skips_its_
finished_units` with a small module built the same way.
"""
from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "experiments" / "phase2" / "src"
THIS = Path(__file__).relative_to(ROOT).as_posix()


def _starts(tree: ast.AST) -> list[ast.Call]:
    return [n for n in ast.walk(tree) if isinstance(n, ast.Call)
            and isinstance(n.func, ast.Attribute) and n.func.attr == "start"
            and isinstance(n.func.value, ast.Name)
            and n.func.value.id == "provenance"]


def _declared(tree: ast.Module):
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "LONG_RUN"
                for t in node.targets):
            if isinstance(node.value, ast.Constant) and \
                    isinstance(node.value.value, bool):
                return node.value.value
            return "not a bool"
    return None


def problems(text: str) -> list[str]:
    """Why a module's source breaks the long-run rule; empty when it holds."""
    tree = ast.parse(text)
    starts = _starts(tree)
    if not starts:
        return []
    long_run = _declared(tree)
    if long_run is None:
        return ["calls provenance.start but declares no LONG_RUN"]
    if long_run == "not a bool":
        return ["LONG_RUN is not True or False"]
    if not long_run:
        return []
    out = []
    resumable = [c for c in starts if not any(
        k.arg == "resumable" and isinstance(k.value, ast.Constant)
        and k.value.value is False for k in c.keywords)]
    if not resumable:
        out.append("LONG_RUN = True with no resumable provenance.start")
    keys = [k for n in ast.walk(tree) if isinstance(n, ast.Dict)
            for k in n.keys if isinstance(k, ast.Constant)
            and k.value == "complete"]
    keys += [n for n in ast.walk(tree) if isinstance(n, ast.Subscript)
             and isinstance(n.slice, ast.Constant)
             and n.slice.value == "complete"]
    if not keys:
        out.append('LONG_RUN = True and no "complete" field')
    prints = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
              and isinstance(n.func, ast.Name) and n.func.id == "print"
              and n.args and isinstance(n.args[0], ast.Constant)
              and n.args[0].value == "complete"]
    if not prints:
        out.append("LONG_RUN = True and no print('complete') marker")
    return out


def test_every_module_that_starts_a_run_follows_the_rule():
    bad = {p.name: problems(p.read_text(encoding="utf-8"))
           for p in sorted(SRC.glob("*.py"))
           if not p.name.startswith("test_")}
    bad = {k: v for k, v in bad.items() if v}
    assert not bad, bad


def test_the_known_long_runs_are_declared():
    # Guards against the rule passing because nothing is declared.
    for name in ("f156_hp_bound", "f158_fraud_types", "f159_parallel_pool",
                 "f166_ulb_algorithms"):
        tree = ast.parse((SRC / f"{name}.py").read_text(encoding="utf-8"))
        assert _declared(tree) is True, name


GOOD = '''
import provenance
LONG_RUN = True
def main():
    rid, resume = provenance.start(OUT)
    provenance.write_result(OUT, {"complete": True}, __file__, [42], rid)
    print("complete", flush=True)
'''


def test_a_module_with_no_declaration_is_refused():
    text = GOOD.replace("LONG_RUN = True\n", "")
    assert problems(text) == ["calls provenance.start but declares no "
                              "LONG_RUN"]


def test_a_long_run_that_cannot_resume_is_refused():
    assert problems(GOOD) == []
    text = GOOD.replace("provenance.start(OUT)",
                        "provenance.start(OUT, resumable=False)")
    assert problems(text) == ["LONG_RUN = True with no resumable "
                              "provenance.start"]


def test_a_long_run_with_no_completion_marker_is_refused():
    text = GOOD.replace('{"complete": True}', "{}")
    assert problems(text) == ['LONG_RUN = True and no "complete" field']
    text = GOOD.replace('    print("complete", flush=True)\n', "")
    assert problems(text) == ["LONG_RUN = True and no print('complete') "
                              "marker"]


# The resume, end to end, in a scratch module built the way the rule says.
TOY = '''
import json, sys
from pathlib import Path
sys.path.insert(0, {src!r})
import provenance
LONG_RUN = True
OUT = Path({out!r})
GEN = {gen!r}   # a generator inside the repository
UNITS = [42, 43, 44, 45]

def main(stop_after=None):
    rid, resume = provenance.start(OUT)
    done = json.loads(OUT.read_text())["rows"] if resume else []
    for seed in UNITS:
        if any(r["seed"] == seed for r in done):
            continue
        done.append({{"seed": seed, "pid": __import__("os").getpid()}})
        provenance.write_result(OUT, {{"rows": done, "complete": False}},
                                GEN, [r["seed"] for r in done], rid)
        if stop_after and len(done) == stop_after:
            raise SystemExit(3)          # the usage limit, mid-run
    provenance.write_result(OUT, {{"rows": done, "complete": True}},
                            GEN, UNITS, rid)
    print("complete", flush=True)

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else None)
'''


def test_a_stopped_run_resumes_and_skips_its_finished_units(tmp_path):
    out = tmp_path / "toy.json"
    mod = tmp_path / "toy_run.py"
    mod.write_text(TOY.format(src=str(SRC), out=str(out),
                              gen=str(Path(__file__))), encoding="utf-8")
    assert problems(mod.read_text(encoding="utf-8")) == []

    first = subprocess.run([sys.executable, str(mod), "2"],
                           capture_output=True, text=True)
    assert first.returncode == 3, first.stderr
    doc = json.loads(out.read_text(encoding="utf-8"))
    assert doc["complete"] is False and len(doc["rows"]) == 2
    pid1 = {r["pid"] for r in doc["rows"]}

    second = subprocess.run([sys.executable, str(mod)], capture_output=True,
                            text=True)
    assert second.returncode == 0, second.stderr
    assert second.stdout.strip().splitlines()[-1] == "complete"
    doc = json.loads(out.read_text(encoding="utf-8"))
    assert doc["complete"] is True
    assert [r["seed"] for r in doc["rows"]] == [42, 43, 44, 45]
    # The first two units were kept, not recomputed.
    assert {r["pid"] for r in doc["rows"][:2]} == pid1
    assert doc["provenance"]["resumed"] == 1
    run_id = doc["provenance"]["run_id"]

    # A third run over a complete result is refused before any work.
    third = subprocess.run([sys.executable, str(mod)], capture_output=True,
                           text=True)
    assert third.returncode != 0 and "FileExistsError" in third.stderr
    assert json.loads(out.read_text(encoding="utf-8"))["provenance"][
        "run_id"] == run_id


def test_the_long_run_rule_can_fail():
    from injection import Mutation, assert_can_fail, run_pytest
    me = Path(__file__)

    def test(name):
        return lambda: run_pytest(f"{THIS}::{name}", ROOT)
    assert_can_fail([Mutation(me, '        return ["calls provenance.start '
                              'but declares no LONG_RUN"]\n',
                              "        return []\n", expect_occurrences=1)],
                    test("test_a_module_with_no_declaration_is_refused"),
                    "a module with no LONG_RUN declaration")
    assert_can_fail([Mutation(me, "    if not resumable:\n",
                              "    if False:\n", expect_occurrences=1)],
                    test("test_a_long_run_that_cannot_resume_is_refused"),
                    "a long run that cannot resume")
    assert_can_fail([Mutation(me, "    if not keys:\n", "    if False:\n",
                              expect_occurrences=1)],
                    test("test_a_long_run_with_no_completion_marker_is_"
                         "refused"),
                    "a long run with no complete field")
    assert_can_fail([Mutation(me, "    if not prints:\n", "    if False:\n",
                              expect_occurrences=1)],
                    test("test_a_long_run_with_no_completion_marker_is_"
                         "refused"),
                    "a long run with no completion marker")
    # And the real modules: a declared long run that loses its resume.
    f166 = SRC / "f166_ulb_algorithms.py"
    assert_can_fail([Mutation(f166, "    rid, resume = provenance.start(OUT)\n",
                              "    rid, resume = provenance.start(OUT, "
                              "resumable=False)\n", expect_occurrences=1)],
                    test("test_every_module_that_starts_a_run_follows_the_"
                         "rule"),
                    "f166 losing its resume path")
