"""Consistency checks for the problem bank.

Run with:  python -m pytest tests/ -q

- every reference solution passes all of its own tests through the real runners
- every starter fails (so the tests actually discriminate)
- every problem has the files and metadata the app expects
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.problems import load_problems  # noqa: E402
from core.python_runner import run_python  # noqa: E402
from core.sql_runner import run_sql  # noqa: E402

PROBLEMS = load_problems()
IDS = sorted(PROBLEMS)
PY_IDS = [i for i in IDS if PROBLEMS[i].language == "python"]
SQL_IDS = [i for i in IDS if PROBLEMS[i].language == "sql"]


def _run(problem, code):
    return run_python(problem, code) if problem.language == "python" else run_sql(problem, code)


def _describe(result):
    lines = []
    for r in result["results"]:
        if not r["passed"]:
            lines.append(f"  - {r['name']}: {r.get('message') or ''} {(r.get('error') or '').strip().splitlines()[-1:] }")
    return "\n".join(lines)


def test_problem_bank_size():
    assert len(PY_IDS) >= 12, PY_IDS
    assert len(SQL_IDS) >= 12, SQL_IDS


@pytest.mark.parametrize("pid", IDS)
def test_metadata_and_files(pid):
    p = PROBLEMS[pid]
    assert p.difficulty in {"easy", "medium", "hard"}
    assert p.title and p.statement.strip() and p.starter.strip() and p.solution.strip()
    assert p.explanation.strip(), "explanation.md missing"
    assert len(p.hints) >= 2, "at least two hints"
    assert p.tags, "tags missing"
    if p.language == "python":
        assert p.tests and len(p.tests) >= 4, "python problems need >= 4 tests"
        if p.kind == "class":
            assert p.class_name
        else:
            assert p.function_name
        for t in p.tests:
            assert "input" in t and "expected" in t
    else:
        assert len(p.datasets) >= 2, "sql problems need >= 2 datasets"


@pytest.mark.parametrize("pid", IDS)
def test_reference_solution_passes(pid):
    p = PROBLEMS[pid]
    result = _run(p, p.solution)
    assert result["status"] == "accepted", f"{pid} reference solution failed:\n{_describe(result)}"
    assert result["passed"] == result["total"]


@pytest.mark.parametrize("pid", IDS)
def test_starter_does_not_pass(pid):
    p = PROBLEMS[pid]
    result = _run(p, p.starter)
    assert result["status"] != "accepted", f"{pid}: starter code already passes"


@pytest.mark.parametrize("pid", SQL_IDS)
def test_sql_reference_returns_rows_and_no_column_warnings(pid):
    p = PROBLEMS[pid]
    result = run_sql(p, p.solution)
    for r in result["results"]:
        assert r["expected"]["total_rows"] > 0, f"{pid}/{r['name']}: reference returns no rows"
        assert not r["warnings"], r["warnings"]


def test_python_time_limit_is_enforced():
    p = PROBLEMS["two-sum"]
    saved = p.time_limit_s
    p.time_limit_s = 1
    try:
        result = run_python(p, "def two_sum(nums, target):\n    while True:\n        pass\n")
    finally:
        p.time_limit_s = saved
    assert result["status"] == "time_limit"


def test_python_syntax_error_is_reported():
    p = PROBLEMS["two-sum"]
    result = run_python(p, "def two_sum(nums, target)\n    return 1\n")
    assert result["status"] == "error"
    assert "SyntaxError" in (result["results"][0]["error"] or "")


def test_sql_wrong_column_count_is_explained():
    p = PROBLEMS["daily-active-users"]
    result = run_sql(p, "SELECT event_ts, user_id, 1 FROM events")
    assert result["status"] == "wrong_answer"
    assert "column" in result["results"][0]["message"]
