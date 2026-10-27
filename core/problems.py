"""Discover and load problems from the problems/ directory."""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROBLEMS_DIR = ROOT / "problems"
DIFFICULTY_RANK = {"easy": 0, "medium": 1, "hard": 2}


@dataclass
class Dataset:
    name: str
    sql: str


@dataclass
class Problem:
    id: str
    title: str
    difficulty: str
    language: str  # "python" | "sql"
    tags: list[str]
    statement: str
    starter: str
    solution: str
    explanation: str
    hints: list[str]
    time_limit_s: float
    path: str
    order: int = 0
    # python
    function_name: str | None = None
    kind: str = "function"  # "function" | "class"
    class_name: str | None = None
    iter_args: list[str] = field(default_factory=list)
    tests: list[dict] = field(default_factory=list)
    # sql
    order_matters: bool = False
    datasets: list[Dataset] = field(default_factory=list)

    def summary(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "difficulty": self.difficulty,
            "language": self.language,
            "tags": self.tags,
            "order": self.order,
        }


def _read(path: Path, default: str = "") -> str:
    return path.read_text(encoding="utf-8") if path.exists() else default


def _load_one(language: str, folder: Path) -> Problem:
    meta = json.loads((folder / "meta.json").read_text(encoding="utf-8"))
    ext = "py" if language == "python" else "sql"
    problem = Problem(
        id=meta.get("id") or folder.name.replace("_", "-"),
        title=meta["title"],
        difficulty=meta["difficulty"].lower(),
        language=language,
        tags=meta.get("tags", []),
        statement=_read(folder / "problem.md"),
        starter=_read(folder / f"starter.{ext}"),
        solution=_read(folder / f"solution.{ext}"),
        explanation=_read(folder / "explanation.md"),
        hints=meta.get("hints", []),
        time_limit_s=float(meta.get("time_limit_s", 5)),
        path=str(folder),
        order=int(meta.get("order", 0)),
    )
    if language == "python":
        problem.function_name = meta.get("function_name")
        problem.kind = meta.get("kind", "function")
        problem.class_name = meta.get("class_name")
        problem.iter_args = meta.get("iter_args", [])
        problem.tests = json.loads((folder / "tests.json").read_text(encoding="utf-8"))
    else:
        problem.order_matters = bool(meta.get("order_matters", False))
        files = sorted(folder.glob("data_*.sql"))
        names = meta.get("dataset_names", [])
        for i, f in enumerate(files):
            name = names[i] if i < len(names) else f"Dataset {i + 1}"
            problem.datasets.append(Dataset(name=name, sql=f.read_text(encoding="utf-8")))
    return problem


def load_problems() -> dict[str, Problem]:
    problems: list[Problem] = []
    for language in ("python", "sql"):
        base = PROBLEMS_DIR / language
        if not base.exists():
            continue
        for folder in sorted(p for p in base.iterdir() if p.is_dir()):
            if (folder / "meta.json").exists():
                problems.append(_load_one(language, folder))
    problems.sort(key=lambda p: (p.language, DIFFICULTY_RANK.get(p.difficulty, 9), p.order, p.title))
    out: dict[str, Problem] = {}
    for p in problems:
        if p.id in out:
            raise ValueError(f"Duplicate problem id '{p.id}' in {p.path} and {out[p.id].path}")
        out[p.id] = p
    return out


def latest_mtime() -> float:
    newest = 0.0
    for dirpath, _dirs, files in os.walk(PROBLEMS_DIR):
        for f in files:
            try:
                newest = max(newest, os.path.getmtime(os.path.join(dirpath, f)))
            except OSError:
                pass
    return newest


class ProblemStore:
    """Caches problems and reloads automatically when any problem file changes."""

    def __init__(self) -> None:
        self._problems: dict[str, Problem] = {}
        self._mtime = -1.0

    def all(self) -> dict[str, Problem]:
        mtime = latest_mtime()
        if mtime != self._mtime:
            self._problems = load_problems()
            self._mtime = mtime
        return self._problems

    def get(self, problem_id: str) -> Problem | None:
        return self.all().get(problem_id)
