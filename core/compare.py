"""Comparison helpers shared by the Python and SQL runners."""
from __future__ import annotations

import datetime as _dt
import decimal
import json
import math

FLOAT_TOL = 1e-6


def normalize(value):
    """Convert a value into plain JSON-friendly Python so expected/actual compare cleanly."""
    if value is None or isinstance(value, (bool, int, str)):
        return value
    if isinstance(value, float):
        if math.isnan(value):
            return "NaN"
        if math.isinf(value):
            return "Infinity" if value > 0 else "-Infinity"
        return value
    if isinstance(value, decimal.Decimal):
        return float(value)
    if isinstance(value, _dt.datetime):
        return value.isoformat(sep=" ")
    if isinstance(value, (_dt.date, _dt.time)):
        return value.isoformat()
    if isinstance(value, _dt.timedelta):
        return value.total_seconds()
    if isinstance(value, bytes):
        return value.decode("utf-8", "replace")
    if isinstance(value, dict):
        return {str(k): normalize(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [normalize(v) for v in value]
    if isinstance(value, (set, frozenset)):
        return sorted((normalize(v) for v in value), key=sort_key)
    if hasattr(value, "tolist"):  # numpy scalars / arrays
        return normalize(value.tolist())
    if hasattr(value, "__iter__"):  # generators and other iterables
        return [normalize(v) for v in value]
    return repr(value)


def _canon(value):
    """Canonical form used only for sorting: integral floats become ints, floats are rounded."""
    if isinstance(value, bool) or value is None or isinstance(value, (int, str)):
        return value
    if isinstance(value, float):
        r = round(value, 6)
        return int(r) if r.is_integer() else r
    if isinstance(value, dict):
        return {k: _canon(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_canon(v) for v in value]
    return value


def sort_key(value):
    return json.dumps(_canon(value), sort_keys=True, default=str)


def deep_equal(expected, actual, tol: float = FLOAT_TOL) -> bool:
    if isinstance(expected, bool) or isinstance(actual, bool):
        return isinstance(expected, bool) and isinstance(actual, bool) and expected == actual
    if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
        if isinstance(expected, float) or isinstance(actual, float):
            return math.isclose(expected, actual, rel_tol=tol, abs_tol=tol)
        return expected == actual
    if isinstance(expected, list) and isinstance(actual, list):
        return len(expected) == len(actual) and all(
            deep_equal(e, a, tol) for e, a in zip(expected, actual)
        )
    if isinstance(expected, dict) and isinstance(actual, dict):
        return expected.keys() == actual.keys() and all(
            deep_equal(expected[k], actual[k], tol) for k in expected
        )
    return expected == actual


def multiset_equal(expected, actual, tol: float = FLOAT_TOL) -> bool:
    """Order-insensitive list comparison (duplicates must match in count)."""
    if not (isinstance(expected, list) and isinstance(actual, list)):
        return False
    if len(expected) != len(actual):
        return False
    return deep_equal(sorted(expected, key=sort_key), sorted(actual, key=sort_key), tol)


def compare_rows(expected_cols, expected_rows, actual_cols, actual_rows, order_matters: bool):
    """Compare two SQL result sets. Returns (passed, message, warnings)."""
    warnings = []
    exp = [normalize(list(r)) for r in expected_rows]
    act = [normalize(list(r)) for r in actual_rows]
    if len(expected_cols) != len(actual_cols):
        return (
            False,
            f"Expected {len(expected_cols)} column(s) {list(expected_cols)}, "
            f"got {len(actual_cols)} {list(actual_cols)}",
            warnings,
        )
    if [c.lower() for c in expected_cols] != [c.lower() for c in actual_cols]:
        warnings.append(
            f"Column names differ (not graded): expected {list(expected_cols)}, got {list(actual_cols)}"
        )
    if len(exp) != len(act):
        return False, f"Expected {len(exp)} row(s), got {len(act)}", warnings
    if not order_matters:
        exp = sorted(exp, key=sort_key)
        act = sorted(act, key=sort_key)
    for i, (e, a) in enumerate(zip(exp, act)):
        if not deep_equal(e, a):
            where = f"Row {i + 1}" if order_matters else f"Row {i + 1} (after sorting both sides)"
            return False, f"{where} differs: expected {e}, got {a}", warnings
    return True, "OK", warnings
