"""A strict `default=` for `json.dumps` in Phase 2 result writers.

PR #46 review (silent-failure 13). `default=str` wrote any value json
cannot encode as its printed text, so `np.bool_(False)` landed in an
evidence file as the string "False", which is truthy when read back.
`default=float` turned a boolean into 1.0. Both hide a type error.

This converts only numpy integer, floating and boolean scalars to their
Python values, and raises TypeError on anything else, so an unexpected
type stops the write instead of entering the evidence as text.
"""
from __future__ import annotations

import numpy as np


def numpy_scalar(obj):
    """`json.dumps(..., default=numpy_scalar)`: numpy scalars only."""
    if isinstance(obj, (np.integer, np.floating, np.bool_)):
        return obj.item()
    raise TypeError(f"not JSON serializable here: {type(obj).__name__}; "
                    "cast it at the source")
