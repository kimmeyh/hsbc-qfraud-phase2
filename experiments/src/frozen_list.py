"""One check for every list that may only shrink (Sprint 28 IMP-1).

A guard that exempts what predates its rule keeps a list of those names.
Four PR #46 reviewers found the outcome guard's list could grow while its
test stayed green, because a count, not the content, was pinned; the
retrospective found the same shape in `test_device_store_required.py`.

The pattern, used by every such list:

- `ORIGINAL`: the list as frozen when the rule landed, a literal never
  edited. `ORIGINAL_SHA256` pins it: a name added to it changes the hash.
- the current list, which may lose names, never gain them;
- for a table of counts, each count may fall, never rise.

`check` returns what is wrong; an empty list means the pin holds.
`test_frozen_lists_pinned.py` fails a test module that keeps a list named
like one of these (`*_BEFORE_RULE`, `*_FROZEN`, `*_NOT_SUBMITTING`,
`*_EXEMPT`, `EXEMPT_*`) without passing it to `check`.
"""
from __future__ import annotations

import hashlib
from collections.abc import Mapping


def canonical(entries) -> str:
    """Names one per line, sorted; a mapping of counts as name=count."""
    if isinstance(entries, Mapping):
        return "\n".join(f"{k}={int(v)}" for k, v in sorted(entries.items()))
    return "\n".join(sorted(entries))


def sha256_of(entries) -> str:
    return hashlib.sha256(canonical(entries).encode("utf-8")).hexdigest()


def check(current, original, original_sha256: str) -> list[str]:
    out = []
    if sha256_of(original) != original_sha256:
        out.append("the frozen original was edited (its SHA-256 differs)")
    new = sorted(set(current) - set(original))
    if new:
        out.append(f"names not in the frozen original: {new}")
    if isinstance(original, Mapping):
        out += [f"{k}: {int(current[k])} above its frozen {int(original[k])}"
                for k in sorted(set(current) & set(original))
                if int(current[k]) > int(original[k])]
    return out
