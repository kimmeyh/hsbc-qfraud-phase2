"""The code of a Python module with its prose removed, for text guards.

Sprint 28 IMP-2: `device_store.py`'s docstring named the device call that
`test_phase2_device_default.py` matches as text, so the guard read a
sentence as a call and CI ran red on eight commits (39f9943 to f98ea2f).
A guard that scans source for a call pattern scans `code_text(src)`.

`code_text` blanks every comment and every docstring (a string that stands
alone as a statement) with spaces, so line and column numbers are kept and
a guard can still report the line it found.
"""
from __future__ import annotations

import io
import tokenize

_SKIP = {tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT,
         tokenize.COMMENT, tokenize.ENCODING}


def code_text(src: str) -> str:
    # Split the way tokenize reads: only at newline characters. splitlines
    # also breaks at a form feed and other separators, which shifts every
    # later row and blanks the wrong line (Sprint 28 improvement review).
    lines = io.StringIO(src).readlines()
    spans = []
    prev = None                     # the last significant token's type
    for tok in tokenize.generate_tokens(io.StringIO(src).readline):
        if tok.type == tokenize.COMMENT:
            spans.append((tok.start, tok.end))
        elif tok.type == tokenize.STRING and prev in (None, tokenize.NEWLINE,
                                                      tokenize.INDENT,
                                                      tokenize.DEDENT):
            spans.append((tok.start, tok.end))
        if tok.type in (tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT):
            prev = tok.type
        elif tok.type not in _SKIP:
            prev = tok.type
    for (r0, c0), (r1, c1) in spans:
        for r in range(r0, r1 + 1):
            line = lines[r - 1]
            body = line.rstrip("\r\n")
            end = line[len(body):]
            a = c0 if r == r0 else 0
            b = c1 if r == r1 else len(body)
            lines[r - 1] = body[:a] + " " * (b - a) + body[b:] + end
    return "".join(lines)
