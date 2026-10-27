"""SQLite-backed progress tracking: submissions, drafts, per-problem status."""
from __future__ import annotations

import datetime as dt
import sqlite3
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "progress.db"

_lock = threading.Lock()
_con: sqlite3.Connection | None = None


def _now() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


def connect(path: Path = DB_PATH) -> sqlite3.Connection:
    global _con
    if _con is None:
        path.parent.mkdir(parents=True, exist_ok=True)
        _con = sqlite3.connect(path, check_same_thread=False)
        _con.row_factory = sqlite3.Row
        _con.executescript(
            """
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                problem_id TEXT NOT NULL,
                code TEXT NOT NULL,
                status TEXT NOT NULL,
                passed INTEGER NOT NULL,
                total INTEGER NOT NULL,
                runtime_ms REAL,
                elapsed_s INTEGER,
                created_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_submissions_problem ON submissions(problem_id, id);
            CREATE TABLE IF NOT EXISTS problem_state (
                problem_id TEXT PRIMARY KEY,
                status TEXT,
                draft_code TEXT,
                solution_viewed INTEGER NOT NULL DEFAULT 0,
                best_ms REAL,
                attempts INTEGER NOT NULL DEFAULT 0,
                solved_at TEXT,
                updated_at TEXT NOT NULL
            );
            """
        )
        _con.commit()
    return _con


def _ensure_state(con, problem_id: str) -> None:
    con.execute(
        "INSERT OR IGNORE INTO problem_state(problem_id, updated_at) VALUES (?, ?)",
        (problem_id, _now()),
    )


def save_draft(problem_id: str, code: str) -> None:
    with _lock:
        con = connect()
        _ensure_state(con, problem_id)
        con.execute(
            "UPDATE problem_state SET draft_code = ?, updated_at = ? WHERE problem_id = ?",
            (code, _now(), problem_id),
        )
        con.commit()


def record_submission(problem_id: str, code: str, result: dict, elapsed_s: int | None) -> None:
    with _lock:
        con = connect()
        _ensure_state(con, problem_id)
        con.execute(
            "INSERT INTO submissions(problem_id, code, status, passed, total, runtime_ms, elapsed_s, created_at)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                problem_id,
                code,
                result["status"],
                result["passed"],
                result["total"],
                result["runtime_ms"],
                elapsed_s,
                _now(),
            ),
        )
        row = con.execute(
            "SELECT status, best_ms FROM problem_state WHERE problem_id = ?", (problem_id,)
        ).fetchone()
        accepted = result["status"] == "accepted"
        new_status = "solved" if accepted or row["status"] == "solved" else "attempted"
        best = row["best_ms"]
        if accepted and (best is None or result["runtime_ms"] < best):
            best = result["runtime_ms"]
        con.execute(
            "UPDATE problem_state SET status = ?, draft_code = ?, best_ms = ?, attempts = attempts + 1,"
            " solved_at = COALESCE(solved_at, ?), updated_at = ? WHERE problem_id = ?",
            (new_status, code, best, _now() if accepted else None, _now(), problem_id),
        )
        con.commit()


def mark_solution_viewed(problem_id: str) -> None:
    with _lock:
        con = connect()
        _ensure_state(con, problem_id)
        con.execute(
            "UPDATE problem_state SET solution_viewed = 1, updated_at = ? WHERE problem_id = ?",
            (_now(), problem_id),
        )
        con.commit()


def reset_problem(problem_id: str) -> None:
    with _lock:
        con = connect()
        con.execute("DELETE FROM submissions WHERE problem_id = ?", (problem_id,))
        con.execute("DELETE FROM problem_state WHERE problem_id = ?", (problem_id,))
        con.commit()


def all_states() -> dict[str, dict]:
    with _lock:
        con = connect()
        rows = con.execute("SELECT * FROM problem_state").fetchall()
    return {r["problem_id"]: dict(r) for r in rows}


def get_state(problem_id: str) -> dict | None:
    with _lock:
        con = connect()
        row = con.execute(
            "SELECT * FROM problem_state WHERE problem_id = ?", (problem_id,)
        ).fetchone()
    return dict(row) if row else None


def submissions(problem_id: str, limit: int = 30) -> list[dict]:
    with _lock:
        con = connect()
        rows = con.execute(
            "SELECT id, status, passed, total, runtime_ms, elapsed_s, created_at, code FROM submissions"
            " WHERE problem_id = ? ORDER BY id DESC LIMIT ?",
            (problem_id, limit),
        ).fetchall()
    return [dict(r) for r in rows]
