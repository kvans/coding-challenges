"""Child-process test harness.

Invoked as: python -I -X utf8 harness.py <code_dir>
Reads a JSON spec on stdin, imports <code_dir>/user_code.py, runs each test and
emits one JSON line per test on the real stdout. All user prints are captured.
"""
from __future__ import annotations

import importlib
import io
import json
import os
import sys
import time
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compare import normalize  # noqa: E402

MAX_STDOUT = 4000


def _json_default(obj):
    try:
        return normalize(obj)
    except Exception:  # pragma: no cover - last resort
        return repr(obj)


def _format_error(exc: BaseException) -> str:
    tb = exc.__traceback__
    # Drop harness frames so the user sees only their own code in the traceback.
    while tb is not None and os.path.basename(tb.tb_frame.f_code.co_filename) == "harness.py":
        tb = tb.tb_next
    text = "".join(traceback.format_exception(type(exc), exc, tb))
    return text.replace(os.path.dirname(os.path.abspath(sys.argv[1])) + os.sep, "")


def _call_function(mod, spec, test_input):
    fn = getattr(mod, spec["function_name"], None)
    if fn is None:
        raise NameError(f"Function '{spec['function_name']}' is not defined. Keep the starter signature.")
    # iter_args: names of arguments that hold a list of sequences; each inner
    # sequence is handed to the user as a one-shot iterator (simulates streams).
    iter_args = set(spec.get("iter_args") or [])
    if isinstance(test_input, dict):
        kwargs = {k: ([iter(s) for s in v] if k in iter_args else v) for k, v in test_input.items()}
        return fn(**kwargs)
    if isinstance(test_input, list):
        return fn(*test_input)
    return fn(test_input)


def _call_class(mod, spec, test_input):
    ops = test_input["ops"]
    args = test_input["args"]
    cls = getattr(mod, spec["class_name"], None)
    if cls is None:
        raise NameError(f"Class '{spec['class_name']}' is not defined. Keep the starter signature.")
    out = []
    instance = None
    for op, a in zip(ops, args):
        if op == spec["class_name"]:
            instance = cls(*a)
            out.append(None)
        else:
            method = getattr(instance, op)
            out.append(method(*a))
    return out


def main() -> None:
    real_stdout = sys.stdout
    sys.stdout = io.StringIO()  # swallow import-time prints

    def emit(obj):
        real_stdout.write(json.dumps(obj, default=_json_default) + "\n")
        real_stdout.flush()

    spec = json.loads(sys.stdin.read())
    code_dir = sys.argv[1]
    sys.path.insert(0, code_dir)
    sys.setrecursionlimit(20000)

    try:
        mod = importlib.import_module("user_code")
    except BaseException as exc:  # noqa: BLE001
        emit({"type": "fatal", "error": _format_error(exc), "stdout": sys.stdout.getvalue()[-MAX_STDOUT:]})
        return

    kind = spec.get("kind", "function")
    for index, test in enumerate(spec["tests"]):
        buf = io.StringIO()
        sys.stdout = buf
        actual = None
        error = None
        start = time.perf_counter()
        try:
            if kind == "class":
                actual = _call_class(mod, spec, test["input"])
            else:
                actual = _call_function(mod, spec, test["input"])
            actual = normalize(actual)
        except BaseException as exc:  # noqa: BLE001
            error = _format_error(exc)
        ms = (time.perf_counter() - start) * 1000.0
        emit({
            "type": "test",
            "index": index,
            "actual": actual,
            "error": error,
            "stdout": buf.getvalue()[-MAX_STDOUT:],
            "ms": ms,
        })
    emit({"type": "done"})


if __name__ == "__main__":
    main()
