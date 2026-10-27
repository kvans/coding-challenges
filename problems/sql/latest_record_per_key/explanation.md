**Idea:** rank each customer's events newest-first with a deterministic tie-break, keep rank 1, then exclude deletes.

```sql
SELECT customer_id, email, status, updated_at
FROM cdc_events
QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id
                           ORDER BY updated_at DESC, event_id DESC) = 1
   AND op <> 'D';
```

**Talking points**
- Filter deletes *after* ranking. Filtering them first would make the previous update look current and resurrect deleted customers.
- The secondary key (`event_id`, Kafka offset, ingest sequence) is what makes the result deterministic when timestamps tie; always include one.
- `MAX(updated_at)` + self-join is the pre-window-function way; it needs the same tie handling and is slower.
- `QUALIFY` is DuckDB/Snowflake/BigQuery syntax; in Postgres wrap the window in a CTE or subquery.
