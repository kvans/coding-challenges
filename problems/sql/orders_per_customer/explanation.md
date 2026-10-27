**Idea:** keep every customer with a `LEFT JOIN`, count a column that is NULL for unmatched rows, and default the sum.

```sql
SELECT c.customer_id, c.name,
       COUNT(o.order_id)          AS order_count,
       COALESCE(SUM(o.amount), 0) AS total_spent
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name;
```

**Talking points**
- `COUNT(*)` returns 1 for a customer with no orders because the LEFT JOIN still produces one (NULL-padded) row. `COUNT(o.order_id)` ignores NULLs.
- `SUM` skips NULL amounts, which is the intended "contribute nothing" behaviour; only an all-NULL group needs `COALESCE`.
- Putting a filter on the orders table in `WHERE` would turn the LEFT JOIN into an inner join; such filters belong in the `ON` clause.
