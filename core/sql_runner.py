"""Run user SQL against each dataset of a problem using in-memory DuckDB."""
from __future__ import annotations

import hashlib
import threading
import time

import duckdb

from .compare import compare_rows, normalize

PREVIEW_ROWS = 50
_expected_cache: dict[str, tuple[list[str], list[tuple]]] = {}


def _connect(dataset_sql: str):
    con = duckdb.connect(database=":memory:")
    con.execute(dataset_sql)
    return con


def _run_query(con, sql: str, timeout_s: float) -> dict:
    result: dict = {}

    def target():
        try:
            cur = con.execute(sql)
            if cur.description is None:
                result["error"] = "The query returned no result set. Submit a single SELECT statement."
                return
            result["cols"] = [d[0] for d in cur.description]
            result["rows"] = cur.fetchall()
        except Exception as exc:  # noqa: BLE001
            result["error"] = f"{type(exc).__name__}: {exc}"

    th = threading.Thread(target=target, daemon=True)
    th.start()
    th.join(timeout_s)
    if th.is_alive():
        try:
            con.interrupt()
        except Exception:  # noqa: BLE001
            pass
        th.join(2)
        return {"error": f"Time limit exceeded ({timeout_s}s)"}
    return result


def expected_for(problem, index: int) -> tuple[list[str], list[tuple]]:
    ds = problem.datasets[index]
    key = hashlib.sha1((problem.solution + "\x00" + ds.sql).encode("utf-8")).hexdigest()
    if key not in _expected_cache:
        con = _connect(ds.sql)
        try:
            res = _run_query(con, problem.solution, max(problem.time_limit_s, 10))
        finally:
            con.close()
        if "error" in res:
            raise RuntimeError(f"Reference solution failed on '{ds.name}': {res['error']}")
        _expected_cache[key] = (res["cols"], res["rows"])
    return _expected_cache[key]


def _table(cols, rows):
    return {
        "columns": list(cols),
        "rows": [normalize(list(r)) for r in rows[:PREVIEW_ROWS]],
        "total_rows": len(rows),
    }


def run_sql(problem, code: str) -> dict:
    code = (code or "").strip()
    results = []
    passed = 0
    total_ms = 0.0
    any_error = False
    timed_out = False
    for i, ds in enumerate(problem.datasets):
        exp_cols, exp_rows = expected_for(problem, i)
        item = {
            "name": ds.name,
            "passed": False,
            "message": "",
            "warnings": [],
            "expected": _table(exp_cols, exp_rows),
            "actual": None,
            "error": None,
            "ms": None,
        }
        if not code:
            item["error"] = "Empty query."
            any_error = True
            results.append(item)
            continue
        con = _connect(ds.sql)
        start = time.perf_counter()
        try:
            res = _run_query(con, code, problem.time_limit_s)
        finally:
            con.close()
        ms = (time.perf_counter() - start) * 1000.0
        item["ms"] = round(ms, 2)
        total_ms += ms
        if "error" in res:
            item["error"] = res["error"]
            any_error = True
            if res["error"].startswith("Time limit"):
                timed_out = True
        else:
            item["actual"] = _table(res["cols"], res["rows"])
            ok, message, warnings = compare_rows(
                exp_cols, exp_rows, res["cols"], res["rows"], problem.order_matters
            )
            item["passed"] = ok
            item["message"] = message
            item["warnings"] = warnings
            if ok:
                passed += 1
        results.append(item)

    if timed_out:
        status = "time_limit"
    elif passed == len(results):
        status = "accepted"
    elif any_error:
        status = "error"
    else:
        status = "wrong_answer"
    return {
        "status": status,
        "passed": passed,
        "total": len(results),
        "runtime_ms": round(total_ms, 2),
        "results": results,
        "stderr": "",
    }


def schema_preview(problem, dataset_index: int = 0, sample_rows: int = 5) -> list[dict]:
    if not problem.datasets:
        return []
    con = _connect(problem.datasets[dataset_index].sql)
    try:
        tables = [
            r[0]
            for r in con.execute(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = 'main' ORDER BY table_name"
            ).fetchall()
        ]
        out = []
        for t in tables:
            cols = [(r[0], r[1]) for r in con.execute(f'DESCRIBE "{t}"').fetchall()]
            cur = con.execute(f'SELECT * FROM "{t}" LIMIT {int(sample_rows)}')
            rows = [normalize(list(r)) for r in cur.fetchall()]
            count = con.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
            out.append(
                {
                    "name": t,
                    "columns": [{"name": c, "type": ty} for c, ty in cols],
                    "sample": rows,
                    "row_count": count,
                }
            )
        return out
    finally:
        con.close()
