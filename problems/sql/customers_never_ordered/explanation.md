**Idea:** anti-join. Either of these is correct and NULL-safe:

```sql
-- NOT EXISTS
SELECT c.customer_id, c.name FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);

-- LEFT JOIN + IS NULL
SELECT c.customer_id, c.name FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL;
```

**Talking points**
- `NOT IN (subquery)` with a NULL in the subquery evaluates to UNKNOWN for every row, so the whole result is empty. Either filter `WHERE customer_id IS NOT NULL` inside the subquery or use `NOT EXISTS`.
- With the LEFT JOIN form, test `IS NULL` on a non-nullable column of the right table (the key or primary key), never on a nullable attribute.
- Optimisers turn `NOT EXISTS` into an anti-join; it is usually the clearest intent and the fastest.
