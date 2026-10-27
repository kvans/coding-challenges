Implement a tiny version of what every query engine does. Write `hash_join(left, right, on, how="inner")` that joins two lists of dicts on a single key column.

Rules (match SQL semantics):

- `how` is `"inner"` or `"left"`.
- For every left row **in input order**, emit one output row per matching right row (right matches in their input order). Duplicate keys on both sides therefore produce a cross product.
- An output row is the left row's fields plus the right row's non-key fields. Non-key column names never collide between the two inputs.
- With `how="left"`, a left row with no match is still emitted once, with every right-side non-key column set to `None`. The set of right-side columns is the union of keys seen across all right rows (minus the join key).
- `None` is never equal to anything, including another `None`: rows whose key is `None` never match.
- Do not mutate the input rows.

### Example

```
left  = [{"order_id": 1, "cust": 10}, {"order_id": 2, "cust": 20}, {"order_id": 3, "cust": 99}]
right = [{"cust": 10, "name": "Ana"}, {"cust": 20, "name": "Bo"}, {"cust": 20, "name": "Bo (dup)"}]

hash_join(left, right, "cust", "inner") ->
  [{"order_id": 1, "cust": 10, "name": "Ana"},
   {"order_id": 2, "cust": 20, "name": "Bo"},
   {"order_id": 2, "cust": 20, "name": "Bo (dup)"}]

hash_join(left, right, "cust", "left") -> the three rows above plus
   {"order_id": 3, "cust": 99, "name": None}
```

### Why interviewers ask this

It tests whether you actually understand join semantics (duplicates fan out, NULLs never match, left rows survive) rather than just typing `JOIN`. It is also the mental model for broadcast joins in Spark: build the small side, stream the big side.
