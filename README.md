# DE Interview Practice

A local, LeetCode-style practice app for **data engineering** interviews: Python and SQL problems with
hidden test cases, instant grading, hints, reference solutions, a per-problem timer and progress tracking.
Everything runs on your machine; the only dependency is DuckDB.

## Run it

```bash
python -m pip install -r requirements.txt
python app.py
```

Then open <http://localhost:8765>. Use `python app.py --port 9000` to change the port.

- **Python** problems run in an isolated child process with a time limit; your function is called with each
  test case's arguments and the return value is compared with the expected value (floats within 1e-6,
  dict key order ignored; some tests compare as unordered multisets).
- **SQL** problems run on in-memory **DuckDB** (Snowflake / BigQuery / Postgres-like syntax, `QUALIFY`
  supported). Your query runs against every dataset of the problem and the result set is compared with the
  reference solution's result. Column *order* matters, column *names* do not; row order matters only when
  the problem says so.
- Progress (status, drafts, submissions, solution views) is stored in `data/progress.db` (SQLite).
  Delete the file to start over, or use **Reset progress** on a single problem.

Shortcuts: `Ctrl+Enter` runs the tests. **Random unsolved** respects the language and difficulty filters.

## Problem bank (v1: 24)

| | Easy | Medium | Hard |
|---|---|---|---|
| **Python** | Two Sum, Count HTTP Status Codes, Dedupe Records (keep latest), Flatten Nested JSON | Merge Intervals, Top K Frequent, Sessionize User Events, In-Memory Hash Join, LRU Cache | Merge K Sorted Streams, SCD Type 2 from Snapshots, Pipeline DAG Run Order |
| **SQL** | Daily Active Users, Top 3 Products by Revenue, Customers Who Never Ordered, Orders per Customer | Latest Record per Key (CDC), Month-over-Month Growth, Running Total + Rolling Avg, Top-2 Earners per Dept, Login Streaks | Weekly Cohort Retention, SCD2 Point-in-Time Join, Sessionize Clickstream in SQL |

## Add your own problems

Problems are plain files under `problems/python/<slug>/` or `problems/sql/<slug>/`. The server picks up
new or edited problems automatically (no restart needed).

### Python problem

```
problems/python/my_problem/
  meta.json        id, title, difficulty, tags, function_name, hints[], time_limit_s
  problem.md       statement (Markdown)
  starter.py       what the editor shows initially
  solution.py      reference solution (must pass tests.json)
  explanation.md   shown with the solution
  tests.json       [{"name": "...", "input": {"arg": value, ...}, "expected": value, "unordered": false}]
```

`input` is passed as keyword arguments (a list is passed positionally). Extra `meta.json` options:

- `"kind": "class", "class_name": "LRUCache"` for design problems; tests then look like
  `{"input": {"ops": ["LRUCache", "put", "get"], "args": [[2], [1, 1], [1]]}, "expected": [null, null, 1]}`.
- `"iter_args": ["streams"]` turns each inner list of that argument into a one-shot iterator.

### SQL problem

```
problems/sql/my_problem/
  meta.json        id, title, difficulty, tags, hints[], order_matters, dataset_names[], time_limit_s
  problem.md       statement with the table schemas
  starter.sql
  solution.sql     reference query; expected output is computed from it per dataset
  explanation.md
  data_1.sql       CREATE TABLE + INSERT statements for dataset 1
  data_2.sql       ... as many datasets as you like (use them for edge cases)
```

## Check the bank

```bash
python -m pytest tests/ -q
```

The suite runs every reference solution through the real graders, confirms every starter fails, and
checks the metadata of every problem.

## Layout

```
app.py              stdlib HTTP server + JSON API
core/problems.py    loads problems/ (auto-reload on file change)
core/python_runner.py, core/harness.py   sandboxed Python grading
core/sql_runner.py  DuckDB grading + schema preview
core/compare.py     result comparison rules
core/progress.py    SQLite progress store
static/             single-page frontend (CodeMirror + marked via CDN)
```
