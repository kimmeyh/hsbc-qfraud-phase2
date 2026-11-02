"""What was done and what was not, read from files only (F168 part 5).

Run it first after any restart: a usage limit, a new session, a crash.
It stores nothing and changes nothing. It reports:

- the sprint, its phase and the task timers running
  (`.claude/sprint_status.json`);
- each agent's progress folder, `.claude/agent_progress/<name>/`: not
  started (no `progress.md`), started with nothing saved (only the first
  line), in progress (how many units, and the last), or finished (`DONE`);
- each result in `experiments/phase2/results/` that is not complete: in
  progress and resumable when its run id matches its sidecar, otherwise
  not resumable; a result is complete only when its file says
  `complete: true` (part 4: the marker, never the file's presence);
- device blocks: intent records with no saved response (a job that may
  have been sent; check the vendor's job list before any re-approval),
  and response files with no problem hash, which the resend check cannot
  match.

Usage:  python scripts/agent_status.py [--root PATH]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))
from provenance import sidecar  # noqa: E402


def _json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def sprint(root: Path) -> list[str]:
    doc = _json(root / ".claude" / "sprint_status.json")
    cur = doc.get("current_sprint") if isinstance(doc, dict) else None
    if not isinstance(cur, dict):
        return ["sprint: status file missing or unreadable "
                "(.claude/sprint_status.json)"]

    def part(name):
        value = cur.get(name)
        return value if isinstance(value, dict) else {}
    done = part("task_actuals")
    timed = sorted(t for t in part("task_started")
                   if t not in done and t not in part("task_paused"))
    paused = sorted(part("task_paused"))
    return [f"sprint {cur.get('number')}: {cur.get('status')}; "
            f"finished {sorted(done)}; timed {timed}; paused {paused}"]


def agents(root: Path) -> list[str]:
    base = root / ".claude" / "agent_progress"
    out = []
    for folder in sorted(p for p in base.glob("*") if p.is_dir()):
        prog = folder / "progress.md"
        if not prog.exists():
            out.append(f"agent {folder.name}: not started (no progress.md)")
            continue
        lines = [ln.strip() for ln in prog.read_text(
            encoding="utf-8").splitlines() if ln.strip()]
        units = lines[1:]
        if units and units[-1] == "DONE":
            out.append(f"agent {folder.name}: finished, "
                       f"{len(units) - 1} unit(s)")
        elif not units:
            out.append(f"agent {folder.name}: started, nothing saved")
        else:
            out.append(f"agent {folder.name}: in progress, {len(units)} "
                       f"unit(s); last: {units[-1]}")
    return out or ["agents: no progress folders"]


def runs(root: Path) -> list[str]:
    results = root / "experiments" / "phase2" / "results"
    out, complete = [], 0
    # A run killed before its first save has a sidecar and no result
    # (PR 74 review: it was invisible here).
    for side in sorted(results.glob("*.json.run_id")):
        if not side.with_name(side.name[:-len(".run_id")]).exists():
            out.append(f"run {side.name[:-len('.run_id')]}: started, "
                       "nothing saved (a sidecar and no result); rerun its "
                       "module to resume")
    for path in sorted(results.glob("*.json")):
        doc = _json(path)
        if doc is None:
            # Unreadable is not "not a run" (PR 74 review).
            out.append(f"run {path.name}: UNREADABLE result file")
            continue
        if not isinstance(doc, dict) or "complete" not in doc:
            continue
        if doc.get("complete") is True:
            complete += 1
            continue
        run_id = (doc.get("provenance") or {}).get("run_id")
        side = sidecar(path)
        first = side.read_text(encoding="utf-8").splitlines()[:1] \
            if side.exists() else []
        if run_id and first and first[0].strip() == run_id:
            state = "in progress, resumable (rerun its module)"
        else:
            state = "not complete and NOT resumable (no matching sidecar)"
        out.append(f"run {path.name}: {state}")
    return out + [f"runs: {complete} complete"]


def device(root: Path) -> list[str]:
    store = root / "experiments" / "phase2" / "results" / "device_samples"
    hashed, unhashed = set(), 0
    for path in sorted(store.glob("*.json")):
        doc = _json(path)
        sha = doc.get("problem_sha256") if isinstance(doc, dict) else None
        if isinstance(sha, str) and len(sha) == 64:
            hashed.add(sha)
        else:
            unhashed += 1
    out = []
    for intent in sorted((store / "intents").glob("*.json")):
        sha = intent.name.split("_", 1)[0]
        if sha not in hashed:
            out.append(f"device {intent.name}: sent, NO response saved; "
                       "check the vendor's job list before re-approval")
    return out + [f"device: {len(hashed)} problem(s) with a saved response; "
                  f"{unhashed} response file(s) with no problem hash "
                  "(not covered by the resend check)"]


# The report's phrases that need action; main() exits 1 on any of them.
PROBLEMS = ("NOT resumable", "NO response saved", "UNREADABLE",
            "nothing saved", "in progress")


def report(root: Path) -> list[str]:
    return sprint(root) + agents(root) + runs(root) + device(root)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=str(ROOT))
    args = ap.parse_args(argv)
    lines = report(Path(args.root))
    for line in lines:
        print(line)
    # Nonzero when something needs action, so a caller reading only the
    # exit code does not take a stopped run as clean (PR 74 review).
    return 1 if any(p in line for line in lines for p in PROBLEMS) else 0


if __name__ == "__main__":
    sys.exit(main())
