"""F147 (Sprint 26): the evidence-library query tool reads and never writes.

Most tests run on a small store built in tmp_path with the library's own
table shapes, so CI (which has no evidence library) still exercises every
query. The live-store tests skip where the store is absent, and say so.
"""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import edb_query  # noqa: E402

SCHEMA = """
CREATE TABLE contexts (id TEXT PRIMARY KEY, description TEXT NOT NULL);
CREATE TABLE records (id TEXT PRIMARY KEY, class TEXT NOT NULL,
  value TEXT NOT NULL, provenance TEXT NOT NULL, evidence_tag TEXT NOT NULL,
  certainty TEXT, certainty_reasons TEXT, fidelity TEXT,
  reading_level INTEGER, updated TEXT NOT NULL, updated_reason TEXT NOT NULL);
CREATE TABLE record_contexts (record_id TEXT, context_id TEXT);
CREATE TABLE assertion_relations (from_assertion_id TEXT,
  to_assertion_id TEXT, relation TEXT);
CREATE TABLE paper_yields (paper_id TEXT, assertion_id TEXT);
CREATE TABLE assertion_documents (record_id TEXT, document TEXT);
"""


@pytest.fixture
def store(tmp_path) -> Path:
    db = tmp_path / "evidence.db"
    c = sqlite3.connect(db)
    c.executescript(SCHEMA)
    c.executemany("INSERT INTO contexts VALUES (?, ?)", [
        ("platform:dirac-3s", "QCi's Dirac-3S"), ("ml", "ML generally")])
    rec = "INSERT INTO records VALUES (?,?,?,?,?,?,NULL,NULL,NULL,?,'t')"
    c.executemany(rec, [
        ("a-res", "assertion", "Resolution is about 200:1", "guide p.18",
         "N/A", "high", "2026-10-13"),
        ("a-old", "assertion", "Old Resolution claim", "guide p.2",
         "HW", "low", "2026-09-01"),
        ("p-guide", "paper", "Dirac-3S User Guide", "QCi", "N/A", None,
         "2026-10-12")])
    c.executemany("INSERT INTO record_contexts VALUES (?, ?)", [
        ("a-res", "platform:dirac-3s"), ("a-old", "ml"),
        ("p-guide", "platform:dirac-3s")])
    c.execute("INSERT INTO assertion_relations VALUES ('a-res','a-old',"
              "'contradicts')")
    c.execute("INSERT INTO paper_yields VALUES ('p-guide', 'a-res')")
    c.execute("INSERT INTO assertion_documents VALUES ('a-res', 'notes.md')")
    c.commit()
    c.close()
    return db


def test_a_write_through_the_tools_connection_fails(store):
    conn = edb_query.connect(store)
    with pytest.raises(sqlite3.OperationalError):
        conn.execute("CREATE TABLE intruder (x)")
    with pytest.raises(sqlite3.OperationalError):
        conn.execute("UPDATE records SET value = 'x' WHERE id = 'a-res'")
    conn.close()
    after = sqlite3.connect(store).execute(
        "SELECT value FROM records WHERE id = 'a-res'").fetchone()[0]
    assert after == "Resolution is about 200:1"


def test_a_missing_store_is_an_error_not_an_empty_result(tmp_path):
    with pytest.raises(FileNotFoundError):
        edb_query.connect(tmp_path / "absent.db")
    assert not (tmp_path / "absent.db").exists(), (
        "opening a missing store must not create it")


def test_search_matches_text_case_insensitively_newest_first(store):
    conn = edb_query.connect(store)
    ids = [r["id"] for r in edb_query.search(conn, "resolution")]
    assert ids == ["a-res", "a-old"]


def test_search_filters(store):
    conn = edb_query.connect(store)
    s = edb_query.search
    assert [r["id"] for r in s(conn, "", context="platform:dirac-3s")] == [
        "a-res", "p-guide"]
    assert [r["id"] for r in s(conn, "", cls="paper")] == ["p-guide"]
    assert [r["id"] for r in s(conn, "", tag="HW")] == ["a-old"]
    assert [r["id"] for r in s(conn, "", certainty="high")] == ["a-res"]
    assert [r["id"] for r in s(conn, "", since="2026-10-12")] == [
        "a-res", "p-guide"]
    assert len(s(conn, "", limit=1)) == 1


def test_show_returns_the_record_and_its_links(store):
    conn = edb_query.connect(store)
    rec = edb_query.show(conn, "a-res")
    assert rec["contexts"] == ["platform:dirac-3s"]
    assert rec["yielded_by"] == ["p-guide"]
    assert rec["documents"] == ["notes.md"]
    assert rec["relations"] == [
        {"direction": "out", "relation": "contradicts", "other": "a-old"}]
    assert edb_query.show(conn, "p-guide")["yields"] == ["a-res"]
    assert edb_query.show(conn, "nope") is None


def test_the_cli_prints_citable_ids(store, capsys):
    assert edb_query.main(["--db", str(store), "search", "guide"]) == 0
    assert "EDB: p-guide" in capsys.readouterr().out
    assert edb_query.main(["--db", str(store), "show", "nope"]) == 1


LIVE = edb_query.DEFAULT_DB


@pytest.mark.skipif(not LIVE.is_file(),
                    reason=f"evidence library not present at {LIVE}")
def test_the_live_store_answers_a_query():
    """Reads only. The write refusal is proven on the tmp_path store above,
    never here: if the protection were ever broken, a write attempted on the
    live store would itself be a write into another repository."""
    conn = edb_query.connect(LIVE)
    assert edb_query.search(conn, "dirac", limit=1)
    assert conn.execute("PRAGMA query_only").fetchone()[0] == 1
    conn.close()
