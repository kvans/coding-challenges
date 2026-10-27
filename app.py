"""DE Interview Practice - local LeetCode-style server for Python + SQL problems.

Run:  python app.py [--port 8765]
Then open http://localhost:8765
"""
from __future__ import annotations

import argparse
import json
import mimetypes
import random
import sys
import traceback
import urllib.parse
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from core import progress
from core.problems import ProblemStore
from core.python_runner import run_python
from core.sql_runner import run_sql, schema_preview

ROOT = Path(__file__).resolve().parent
STATIC = ROOT / "static"
STORE = ProblemStore()


class ApiError(Exception):
    def __init__(self, status: int, message: str):
        super().__init__(message)
        self.status = status


def _status_of(state: dict | None) -> str:
    return (state or {}).get("status") or "unsolved"


def _stats(states):
    out = {"total": 0, "solved": 0, "by_difficulty": {}, "by_language": {}}
    for p in STORE.all().values():
        solved = _status_of(states.get(p.id)) == "solved"
        out["total"] += 1
        out["solved"] += int(solved)
        d = out["by_difficulty"].setdefault(p.difficulty, {"total": 0, "solved": 0})
        d["total"] += 1
        d["solved"] += int(solved)
        lang = out["by_language"].setdefault(p.language, {"total": 0, "solved": 0})
        lang["total"] += 1
        lang["solved"] += int(solved)
    return out


def _get_or_404(problem_id):
    p = STORE.get(problem_id)
    if p is None:
        raise ApiError(404, f"Unknown problem '{problem_id}'")
    return p


def api_problems(_params, _body):
    states = progress.all_states()
    items = []
    for p in STORE.all().values():
        s = states.get(p.id)
        item = p.summary()
        item["status"] = _status_of(s)
        item["solution_viewed"] = bool(s and s["solution_viewed"])
        item["attempts"] = s["attempts"] if s else 0
        items.append(item)
    return {"problems": items, "stats": _stats(states)}


def api_problem(problem_id, _params, _body):
    p = _get_or_404(problem_id)
    state = progress.get_state(problem_id)
    data = p.summary()
    data.update(
        statement=p.statement,
        starter=p.starter,
        hints=p.hints,
        time_limit_s=p.time_limit_s,
        status=_status_of(state),
        solution_viewed=bool(state and state["solution_viewed"]),
        draft=(state or {}).get("draft_code"),
        best_ms=(state or {}).get("best_ms"),
        attempts=(state or {}).get("attempts", 0),
    )
    if p.language == "python":
        data["function_name"] = p.function_name
        data["test_count"] = len(p.tests)
    else:
        data["schema"] = schema_preview(p)
        data["dataset_names"] = [d.name for d in p.datasets]
        data["order_matters"] = p.order_matters
    return data


def api_solution(problem_id, _params, _body):
    p = _get_or_404(problem_id)
    progress.mark_solution_viewed(problem_id)
    return {"solution": p.solution, "explanation": p.explanation}


def api_submissions(problem_id, _params, _body):
    return {"submissions": progress.submissions(problem_id)}


def api_draft(problem_id, _params, body):
    _get_or_404(problem_id)
    progress.save_draft(problem_id, body.get("code", ""))
    return {"ok": True}


def api_reset(problem_id, _params, _body):
    progress.reset_problem(problem_id)
    return {"ok": True}


def api_run(_params, body):
    problem_id = body.get("id")
    code = body.get("code", "")
    p = _get_or_404(problem_id)
    result = run_python(p, code) if p.language == "python" else run_sql(p, code)
    elapsed = body.get("elapsed_s")
    progress.record_submission(problem_id, code, result, int(elapsed) if elapsed is not None else None)
    result["problem_status"] = _status_of(progress.get_state(problem_id))
    return result


def api_random(params, _body):
    states = progress.all_states()
    difficulty = (params.get("difficulty") or "").lower()
    language = (params.get("language") or "").lower()
    include_solved = params.get("include_solved") == "1"
    pool = [
        p
        for p in STORE.all().values()
        if (not difficulty or p.difficulty == difficulty)
        and (not language or p.language == language)
        and (include_solved or _status_of(states.get(p.id)) != "solved")
    ]
    if not pool:
        return {"id": None}
    return {"id": random.choice(pool).id}


def api_stats(_params, _body):
    return _stats(progress.all_states())


class Handler(BaseHTTPRequestHandler):
    server_version = "DEPractice/1.0"

    def log_message(self, fmt, *args):  # quieter logs: API calls only
        if self.path.startswith("/api/"):
            sys.stderr.write("%s\n" % (fmt % args))

    def _send_json(self, payload, status=HTTPStatus.OK):
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _send_file(self, path: Path):
        if not path.is_file():
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        ctype = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        if path.suffix == ".js":
            ctype = "application/javascript"
        if ctype.startswith("text/") or ctype == "application/javascript":
            ctype += "; charset=utf-8"
        data = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _read_body(self) -> dict:
        length = int(self.headers.get("Content-Length") or 0)
        if not length:
            return {}
        raw = self.rfile.read(length)
        try:
            return json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise ApiError(400, f"Invalid JSON body: {exc}") from exc

    def _dispatch(self, method: str):
        parsed = urllib.parse.urlsplit(self.path)
        params = dict(urllib.parse.parse_qsl(parsed.query))
        parts = [urllib.parse.unquote(x) for x in parsed.path.strip("/").split("/") if x]
        try:
            if not parts or parts[0] != "api":
                if method != "GET":
                    self.send_error(HTTPStatus.METHOD_NOT_ALLOWED)
                    return
                if not parts:
                    rel = "index.html"
                elif parts[0] == "static":
                    rel = "/".join(parts[1:])
                else:
                    rel = "/".join(parts)
                static_root = STATIC.resolve()
                target = (STATIC / rel).resolve()
                if static_root not in target.parents:
                    self.send_error(HTTPStatus.FORBIDDEN)
                    return
                self._send_file(target)
                return
            body = self._read_body() if method == "POST" else {}
            payload = self._route(method, parts[1:], params, body)
            self._send_json(payload)
        except ApiError as exc:
            self._send_json({"error": str(exc)}, exc.status)
        except Exception:  # noqa: BLE001
            self._send_json({"error": traceback.format_exc()}, HTTPStatus.INTERNAL_SERVER_ERROR)

    def _route(self, method, parts, params, body):
        if parts == ["problems"] and method == "GET":
            return api_problems(params, body)
        if len(parts) == 2 and parts[0] == "problems" and method == "GET":
            return api_problem(parts[1], params, body)
        if len(parts) == 3 and parts[0] == "problems":
            pid, action = parts[1], parts[2]
            if action == "solution" and method == "GET":
                return api_solution(pid, params, body)
            if action == "submissions" and method == "GET":
                return api_submissions(pid, params, body)
            if action == "draft" and method == "POST":
                return api_draft(pid, params, body)
            if action == "reset" and method == "POST":
                return api_reset(pid, params, body)
        if parts == ["run"] and method == "POST":
            return api_run(params, body)
        if parts == ["random"] and method == "GET":
            return api_random(params, body)
        if parts == ["stats"] and method == "GET":
            return api_stats(params, body)
        raise ApiError(404, f"No route for {method} /api/{'/'.join(parts)}")

    def do_GET(self):  # noqa: N802
        self._dispatch("GET")

    def do_POST(self):  # noqa: N802
        self._dispatch("POST")


def main() -> None:
    parser = argparse.ArgumentParser(description="DE Interview Practice local server")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args()
    problems = STORE.all()
    counts: dict[str, int] = {}
    for p in problems.values():
        counts[p.language] = counts.get(p.language, 0) + 1
    progress.connect()
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Loaded {len(problems)} problems {counts}")
    print(f"DE Interview Practice running at http://{args.host}:{args.port}  (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
