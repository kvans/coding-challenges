**Idea:** a left range join. The `ON` clause carries the key equality *and* the validity-window predicate, so unmatched orders survive with NULL attributes.

```sql
FROM fact_orders f
LEFT JOIN dim_customer d
  ON  d.customer_id = f.customer_id
  AND d.valid_from <= f.order_date
  AND (d.valid_to IS NULL OR f.order_date < d.valid_to)
```

**Talking points**
- Putting the window predicate in `WHERE` instead of `ON` turns the LEFT JOIN into an inner join and drops the NULL-tier orders.
- Half-open intervals avoid the "which version owns the boundary day" problem; with closed intervals you would need `valid_to - 1 day` arithmetic.
- Validate the dimension: windows for one key must not overlap, otherwise an order matches twice and the fact table double counts. A quick check is `COUNT(*)` before and after the join.
- At warehouse scale, range joins are expensive; engines like Databricks have range-join hints, and a common trick is to also join on a coarse bucket (month) to prune.
