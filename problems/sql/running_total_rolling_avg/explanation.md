**Idea:** two window aggregates over the same ordering with different frames.

```sql
SUM(revenue) OVER (ORDER BY sale_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
AVG(revenue) OVER (ORDER BY sale_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
```

**Talking points**
- The default frame for `SUM() OVER (ORDER BY ...)` is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`, which includes *peers* with the same ordering value. With unique dates it equals `ROWS`, but say `ROWS` explicitly.
- `ROWS BETWEEN 6 PRECEDING` means "7 rows", which equals 7 days only because the table has one row per day with no gaps. With gaps you need `RANGE BETWEEN INTERVAL 6 DAY PRECEDING AND CURRENT ROW` or a calendar spine.
- Partial windows at the start: decide whether to show them (as here), NULL them until 7 days exist, or compute the average with a fixed denominator of 7.
