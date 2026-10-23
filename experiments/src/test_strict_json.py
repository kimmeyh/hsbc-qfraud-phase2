"""strict_json: numpy scalars convert; every other unknown type raises.

PR #46 review (silent-failure 13).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments" / "phase2" / "src"))

import strict_json  # noqa: E402


def test_numpy_scalars_become_python_values():
    doc = {"i": np.int64(25), "f": np.float32(0.5), "b": np.bool_(False)}
    back = json.loads(json.dumps(doc, default=strict_json.numpy_scalar))
    assert back == {"i": 25, "f": 0.5, "b": False}
    assert back["b"] is False                    # not the string "False"


@pytest.mark.parametrize("bad", [{1, 2}, Path("x"), np.array([1.0]), object()])
def test_any_other_type_raises(bad):
    with pytest.raises(TypeError, match="cast it at the source"):
        json.dumps({"v": bad}, default=strict_json.numpy_scalar)
