"""Read-only queries over the evidence library (F147, Sprint 26).

The evidence library (EvidenceBasedDB) is a separate repository, and this
repository NEVER writes to it (CLAUDE.md). This tool opens its SQLite store
read-only in two independent ways, so one mistake cannot make it writable:

- the connection URI says `mode=ro`, so SQLite refuses every write, and
- `PRAGMA query_only = ON`, so the connection refuses every write even if
  the URI were ever changed.

The store's journal mode is `delete`, not WAL, so a read-only open needs no
writable side file. A write through this tool's connection fails with
"attempt to write a readonly database" (checked 2026-10-13, and held by
`test_edb_query.py`).

Usage:
    python scripts/edb_query.py search dirac-3s
    python scripts/edb_query.py search resolution --context platform:dirac-3s
    python scripts/edb_query.py search "" --class paper --tag HW --limit 5
    python scripts/edb_query.py show dirac3s-analog-resolution-about-200-to-1
    python scripts/edb_query.py contexts
    (any command takes --json; --db overrides the store path)

Cite a record found here as `EDB: <id>`.
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from pathlib import Path

DEFAULT_DB = Path(os.environ.get(
    "EDB_PATH", "D:/Data/Harold/EvidenceBasedDB/store/evidence.db"))

CLASSES = ("assertion", "acronym", "term", "paper")
TAGS = ("HW", "SIM", "PROJ", "N/A")
CERTAINTIES = ("high", "moderate", "low", "very-low")


def connect(db: Path = DEFAULT_DB) -> sqlite3.Connection:
    """A connection that cannot write. Raises if the store is absent: a
    missing store must not read as an empty result."""
    db = Path(db)
    if not db.is_file():
        raise FileNotFoundError(f"evidence store not found: {db}")
    conn = sqlite3.connect(f"file:{db.as_posix()}?mode=ro", uri=True)
    conn.execute("PRAGMA query_only = ON")
    conn.row_factory = sqlite3.Row
    return conn


def search(conn, text: str = "", cls: str | None = None,
           context: str | None = None, tag: str | None = None,
           certainty: str | None = None, since: str | None = None,
           limit: int = 50) -> list[dict]:
    """Records whose id or value contains `text` (case-insensitive), newest
    first. A paper's value is its title."""
    sql = ["SELECT r.id, r.class, r.value, r.evidence_tag, r.certainty,",
           "       r.updated FROM records r WHERE",
           "  (instr(lower(r.value), lower(?)) > 0",
           "   OR instr(lower(r.id), lower(?)) > 0)"]
    args: list = [text, text]
    if cls:
        sql.append("AND r.class = ?")
        args.append(cls)
    if tag:
        sql.append("AND r.evidence_tag = ?")
        args.append(tag)
    if certainty:
        sql.append("AND r.certainty = ?")
        args.append(certainty)
    if since:
        sql.append("AND r.updated >= ?")
        args.append(since)
    if context:
        sql.append("AND EXISTS (SELECT 1 FROM record_contexts rc "
                   "WHERE rc.record_id = r.id AND rc.context_id = ?)")
        args.append(context)
    sql.append("ORDER BY r.updated DESC, r.id LIMIT ?")
    args.append(int(limit))
    return [dict(r) for r in conn.execute(" ".join(sql), args)]


def _col(conn, sql: str, arg: str) -> list[str]:
    return [r[0] for r in conn.execute(sql, (arg,))]


def show(conn, record_id: str) -> dict | None:
    """One record with its contexts, relations, yields and cited documents."""
    row = conn.execute("SELECT * FROM records WHERE id = ?",
                       (record_id,)).fetchone()
    if row is None:
        return None
    out = dict(row)
    out["contexts"] = _col(
        conn, "SELECT context_id FROM record_contexts WHERE record_id = ? "
              "ORDER BY context_id", record_id)
    out["relations"] = [dict(r) for r in conn.execute(
        "SELECT 'out' AS direction, relation, to_assertion_id AS other "
        "FROM assertion_relations WHERE from_assertion_id = ? "
        "UNION ALL "
        "SELECT 'in', relation, from_assertion_id "
        "FROM assertion_relations WHERE to_assertion_id = ? "
        "ORDER BY 1, 2, 3", (record_id, record_id))]
    out["yields"] = _col(
        conn, "SELECT assertion_id FROM paper_yields WHERE paper_id = ? "
              "ORDER BY 1", record_id)
    out["yielded_by"] = _col(
        conn, "SELECT paper_id FROM paper_yields WHERE assertion_id = ? "
              "ORDER BY 1", record_id)
    out["documents"] = _col(
        conn, "SELECT document FROM assertion_documents WHERE record_id = ? "
              "ORDER BY 1", record_id)
    return out


def contexts(conn) -> list[dict]:
    return [dict(r) for r in conn.execute(
        "SELECT id, description FROM contexts ORDER BY id")]


def _print_rows(rows: list[dict]) -> None:
    if not rows:
        print("(no records)")
    for r in rows:
        value = " ".join(str(r["value"]).split())
        if len(value) > 100:
            value = value[:97] + "..."
        print(f"EDB: {r['id']}  [{r['class']}, {r['evidence_tag']}, "
              f"{r['certainty'] or '-'}, {r['updated']}]")
        print(f"    {value}")


def _print_record(rec: dict) -> None:
    print(f"EDB: {rec['id']}  [{rec['class']}, {rec['evidence_tag']}, "
          f"{rec.get('certainty') or '-'}, updated {rec['updated']}]")
    print(f"  value: {rec['value']}")
    print(f"  provenance: {rec['provenance']}")
    for key in ("contexts", "yields", "yielded_by", "documents"):
        if rec[key]:
            print(f"  {key}: {', '.join(rec[key])}")
    for rel in rec["relations"]:
        arrow = "->" if rel["direction"] == "out" else "<-"
        print(f"  {rel['relation']} {arrow} {rel['other']}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--db", type=Path, default=DEFAULT_DB)
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search")
    s.add_argument("text")
    s.add_argument("--class", dest="cls", choices=CLASSES)
    s.add_argument("--context")
    s.add_argument("--tag", choices=TAGS)
    s.add_argument("--certainty", choices=CERTAINTIES)
    s.add_argument("--since", help="YYYY-MM-DD, on the record's updated date")
    s.add_argument("--limit", type=int, default=50)
    sh = sub.add_parser("show")
    sh.add_argument("id")
    sub.add_parser("contexts")
    args = ap.parse_args(argv)

    conn = connect(args.db)
    try:
        if args.cmd == "search":
            out = search(conn, args.text, args.cls, args.context, args.tag,
                         args.certainty, args.since, args.limit)
            print(json.dumps(out, indent=1)) if args.json else _print_rows(out)
        elif args.cmd == "show":
            rec = show(conn, args.id)
            if rec is None:
                print(f"no record {args.id!r}", file=sys.stderr)
                return 1
            print(json.dumps(rec, indent=1)) if args.json else _print_record(rec)
        else:
            out = contexts(conn)
            if args.json:
                print(json.dumps(out, indent=1))
            else:
                for c in out:
                    print(f"{c['id']}: {c['description']}")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
