**Idea:** compute per-product revenue with a join and `GROUP BY`, sort by it, keep three rows.

```sql
SELECT p.product_id, p.name, SUM(oi.quantity * oi.unit_price) AS revenue
FROM order_items oi JOIN products p ON p.product_id = oi.product_id
GROUP BY p.product_id, p.name
ORDER BY revenue DESC, p.product_id
LIMIT 3;
```

**Talking points**
- An inner join drops products that were never sold, which is what we want here. Ask whether "top 3" should include zero-revenue products when there are fewer than three sellers.
- `LIMIT` cuts ties arbitrarily unless you add a deterministic secondary sort key. For "top N *including* ties" use `DENSE_RANK()` / `QUALIFY` instead of `LIMIT`.
- Group by the key (`product_id`), not just the name; names are not unique in real catalogs.
