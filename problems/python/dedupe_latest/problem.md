A change-data-capture feed delivers the same business entity many times. Write `dedupe_latest(records, key, ts_field)` that keeps only the most recent version of each entity.

- `records` is a list of dicts.
- `key` is the name of the field that identifies the entity (for example `"customer_id"`).
- `ts_field` is the name of the field holding an ISO-8601 timestamp string such as `"2024-05-01 10:00:00"`. All timestamps share the same format.
- If two records for the same key share the exact same timestamp, the one that appears **later** in the input wins.
- Return the surviving records sorted by `key` ascending. Do not modify the records.

### Example

```
Input: records = [
    {"customer_id": 2, "email": "b@x.com", "updated_at": "2024-05-01 10:00:00"},
    {"customer_id": 1, "email": "a@x.com", "updated_at": "2024-05-01 09:00:00"},
    {"customer_id": 2, "email": "b2@x.com", "updated_at": "2024-05-02 08:00:00"},
    {"customer_id": 1, "email": "old@x.com", "updated_at": "2024-04-30 09:00:00"},
  ], key = "customer_id", ts_field = "updated_at"
Output: [
    {"customer_id": 1, "email": "a@x.com", "updated_at": "2024-05-01 09:00:00"},
    {"customer_id": 2, "email": "b2@x.com", "updated_at": "2024-05-02 08:00:00"},
  ]
```

### Why interviewers ask this

Every CDC / upsert pipeline needs "latest record per key". It is the Python twin of `ROW_NUMBER() OVER (PARTITION BY key ORDER BY ts DESC)`.
