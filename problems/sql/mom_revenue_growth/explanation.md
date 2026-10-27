**Idea:** aggregate to months, use `LAG` to fetch the previous row's month and revenue, and only treat it as the previous period when the months are actually adjacent. Then compute the percentage with a zero/NULL guard.

**Talking points**
- `LAG` is row-based. If February is missing, March's `LAG` returns January. Comparing `prev_month = month - INTERVAL 1 MONTH` (or generating a calendar spine and left-joining) fixes that.
- Division by zero: guard with `CASE` or `NULLIF(prev_revenue, 0)`.
- Filtering `status = 'completed'` *before* aggregation is essential; filtering after would require conditional sums.
- Mention time zones and "month" definitions (fiscal vs calendar) as follow-ups.
