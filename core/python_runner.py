"""Run user Python code against a problem's tests in an isolated child process."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile

from .compare import deep_equal, multiset_equal

HARNESS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "harness.py")


def run_python(problem, code: str) -> dict:
    tests = problem.tests
    tmp = tempfile.mkdtemp(prefix="practice_")
    try:
        with open(os.path.join(tmp, "user_code.py"), "w", encoding="utf-8") as fh:
            fh.write(code)
        spec = {
            "function_name": problem.function_name,
            "kind": problem.kind,
            "class_name": problem.class_name,
            "iter_args": problem.iter_args,
            "tests": [{"input": t["input"]} for t in tests],
        }
        cmd = [sys.executable, "-I", "-X", "utf8", HARNESS, tmp]
        timed_out = False
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=tmp,
        )
        try:
            out, err = proc.communicate(json.dumps(spec), timeout=problem.time_limit_s)
        except subprocess.TimeoutExpired:
            timed_out = True
            proc.kill()
            out, err = proc.communicate()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    events = []
    for line in (out or "").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue

    fatal = next((e for e in events if e.get("type") == "fatal"), None)
    by_index = {e["index"]: e for e in events if e.get("type") == "test"}

    results = []
    passed = 0
    total_ms = 0.0
    tle_reported = False
    for i, test in enumerate(tests):
        item = {
            "name": test.get("name") or f"Test {i + 1}",
            "input": test["input"],
            "expected": test["expected"],
            "actual": None,
            "stdout": "",
            "error": None,
            "ms": None,
            "passed": False,
        }
        if fatal is not None:
            item["error"] = fatal["error"]
            item["stdout"] = fatal.get("stdout", "")
        elif i in by_index:
            ev = by_index[i]
            item.update(actual=ev["actual"], stdout=ev["stdout"], error=ev["error"], ms=round(ev["ms"], 2))
            total_ms += ev["ms"]
            if ev["error"] is None:
                cmp = multiset_equal if test.get("unordered") else deep_equal
                item["passed"] = cmp(test["expected"], ev["actual"])
        elif timed_out and not tle_reported:
            item["error"] = f"Time limit exceeded ({problem.time_limit_s}s for the whole test run)"
            tle_reported = True
        elif timed_out:
            item["error"] = "Not run (an earlier test timed out)"
        else:
            item["error"] = "Harness produced no result for this test." + (f"\n\nstderr:\n{err}" if err else "")
        if item["passed"]:
            passed += 1
        results.append(item)

    if fatal is not None:
        status = "error"
    elif timed_out:
        status = "time_limit"
    elif passed == len(tests):
        status = "accepted"
    elif any(r["error"] for r in results):
        status = "error"
    else:
        status = "wrong_answer"

    return {
        "status": status,
        "passed": passed,
        "total": len(tests),
        "runtime_ms": round(total_ms, 2),
        "results": results,
        "stderr": (err or "")[-4000:] if status == "error" else "",
    }
