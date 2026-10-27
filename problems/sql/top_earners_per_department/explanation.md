**Idea:** rank salaries within each department with `DENSE_RANK` and keep ranks 1 and 2.

```sql
SELECT department, name, salary
FROM employees
WHERE salary IS NOT NULL
QUALIFY DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) <= 2;
```

**Talking points**
- `ROW_NUMBER` would arbitrarily drop one of two tied employees. `RANK` would give 1,1,3 and exclude the real second salary value. `DENSE_RANK` gives 1,1,2.
- `WHERE` runs before the window, so filtering NULL salaries there keeps them out of the ranking. If NULLs were ranked, `ORDER BY salary DESC` puts them last in DuckDB (NULLS LAST default) but first in some other engines.
- Without `QUALIFY` (for example in Postgres) use a CTE and filter on the rank column.
