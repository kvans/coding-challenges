**Idea:** truncate the timestamp to a day, then `COUNT(DISTINCT user_id)` per day.

```sql
SELECT CAST(event_ts AS DATE) AS activity_date,
       COUNT(DISTINCT user_id) AS dau
FROM events
GROUP BY 1;
```

**Talking points**
- `COUNT(*)` would give daily *events*, not users. Always ask "distinct of what?".
- In warehouses `COUNT(DISTINCT)` is expensive at scale; mention `APPROX_COUNT_DISTINCT` / HyperLogLog for dashboards where 1-2% error is acceptable.
- Time zones: `CAST(ts AS DATE)` uses the stored timestamp as-is. In production you would convert to the business time zone first.
