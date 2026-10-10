"""F46 step 1: report the Dirac-3 allocation balance. ZERO metered seconds.

`QciClient.get_allocations()` is a plain HTTP GET against the allocations
endpoint -- it submits no job, so it consumes no QPU time and needs no Criterion
H approval. Verified by reading the client source before calling it, rather than
assuming from the method name.

QCi's email of 2026-09-09 says 3,000 complimentary seconds were loaded. This
reads the number from the API instead of taking the email's word for it: the
account is what governs what we can run, and an email is a statement about it.

`--record` (Sprint 24 IMP-1) appends the read to
`experiments/results/allocation_reads.json`, the ONE place the current balance
lives. Documents cite that file instead of restating a figure: on 2026-10-10
the balance read 8,522 s while six live documents still stated an older one.
`test_allocation_single_source.py` enforces both halves.

Never prints the token. The client reads QCI_API_URL and QCI_TOKEN from the
environment per ADR-0011.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[2]
READS = ROOT / "experiments" / "results" / "allocation_reads.json"
GENERATOR = "experiments/src/check_allocation.py --record"


def _load_env() -> None:
    p = ROOT / ".env"
    if not p.exists():
        return
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


def record_read(allocations: dict, path: pathlib.Path = READS,
                now: datetime | None = None) -> dict:
    """Append one read to the reads file and return it.

    Accepts the live response ({"allocations": {...}}) or the inner dict, as
    `metered_call.balance` does. Refuses a response with no dirac seconds
    rather than recording a read that says nothing. Earlier reads are never
    rewritten: the file is a history, and its last entry is the balance.
    """
    inner = allocations.get("allocations", allocations)
    dirac = inner.get("dirac") if isinstance(inner, dict) else None
    if not isinstance(dirac, dict) or not isinstance(dirac.get("seconds"), int):
        raise ValueError(f"no dirac seconds in the response: {allocations!r}")
    now = now or datetime.now(timezone.utc)

    if path.exists():
        doc = json.loads(path.read_text(encoding="utf-8"))
    else:
        doc = {
            "note": ("The Dirac-3 allocation balance, one read per entry, "
                     "oldest first. The LAST read is the current balance. "
                     "Documents cite this file and do not restate the figure "
                     "(Sprint 24 IMP-1)."),
            "generator": GENERATOR,
            "evidence_tag": "HW",
            "reads": [],
        }
    read = {
        "checked_utc": now.isoformat(),
        "dirac_seconds": dirac["seconds"],
        "dirac_paid": dirac.get("paid"),
        "allocations": inner,
        "metered_seconds": 0.0,
    }
    if doc["reads"] and doc["reads"][-1]["checked_utc"] >= read["checked_utc"]:
        raise ValueError("a read must be newer than the last one recorded")
    doc["reads"].append(read)

    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
    os.replace(tmp, path)
    return read


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--record", action="store_true",
                    help=f"append the read to {READS.relative_to(ROOT)}")
    args = ap.parse_args(argv)

    _load_env()
    url, token = os.environ.get("QCI_API_URL"), os.environ.get("QCI_TOKEN")
    if not url or not token:
        print("QCI_API_URL and QCI_TOKEN must both be set (ADR-0011).")
        return 2

    from qci_client import QciClient

    client = QciClient(api_token=token, url=url)
    allocations = client.get_allocations()

    print(json.dumps(allocations, indent=2))

    # Pull the seconds out of whatever shape the response uses, without
    # asserting a schema we have not seen.
    def _walk(o, path=""):
        if isinstance(o, dict):
            for k, v in o.items():
                yield from _walk(v, f"{path}.{k}" if path else k)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                yield from _walk(v, f"{path}[{i}]")
        elif isinstance(o, (int, float)) and not isinstance(o, bool):
            yield path, o

    print("\nnumeric fields:")
    for path, val in _walk(allocations):
        print(f"  {path:48} {val}")

    if args.record:
        read = record_read(allocations)
        print(f"\nrecorded {read['dirac_seconds']} s at {read['checked_utc']} "
              f"in {READS.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
