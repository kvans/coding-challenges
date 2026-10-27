**Idea:** three grains. (1) Per user: cohort week. (2) Per cohort: size. (3) Per activity: which week number it falls in relative to the user's cohort. Aggregate (3) to `(cohort, week_number)` with a distinct count and divide by (2).

**Talking points**
- The denominator must come from the cohort table, not from the activity table; otherwise users who never came back vanish and retention is inflated.
- `date - date` in DuckDB yields days; `// 7` is integer division. Truncating both dates to week start before subtracting makes "same calendar week" exact instead of "within 7 days of signup" (both definitions exist; state which you use).
- Negative week numbers mean activity before signup (bad data or backfilled accounts); dropping them is a documented choice.
- Pivoting the result into a triangle (week 0, 1, 2 as columns) is a presentation step, usually done in the BI tool or with `PIVOT`.
