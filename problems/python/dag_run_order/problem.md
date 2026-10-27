An orchestrator (think Airflow or Dagster) has to decide in which order to run pipeline tasks.

Write `pipeline_run_order(tasks)` where `tasks` maps each task name to the list of task names it **depends on** (its upstreams).

Rules:

- Return a list with every task exactly once such that each task appears after all of its dependencies.
- When several tasks are ready to run at the same time, run the **alphabetically smallest** first. This makes the answer unique.
- A dependency that is not itself a key in `tasks` is a task with no dependencies of its own.
- If the graph contains a cycle (including a task depending on itself), return `None`.
- An empty graph returns `[]`.

### Example

```
tasks = {
  "report":    ["agg_sales", "agg_users"],
  "agg_sales": ["clean"],
  "agg_users": ["clean"],
  "clean":     ["raw"],
  "raw":       [],
  "audit":     [],
}
pipeline_run_order(tasks) == ["audit", "raw", "clean", "agg_sales", "agg_users", "report"]
```

`audit` and `raw` are both ready at the start; `audit` goes first alphabetically.

### Why interviewers ask this

Topological sort is the one graph algorithm every data engineer must know cold: DAG scheduling, dbt model ordering, dependency resolution, and detecting circular references in a lineage graph.
