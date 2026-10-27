You receive a full daily snapshot of the `customers` table. Build a **Slowly Changing Dimension Type 2** history from the snapshots.

Write `build_scd2(snapshots)` where `snapshots` is a list of flat dicts, each with:

- `snapshot_date` - `"YYYY-MM-DD"` string, the day the snapshot was taken
- `customer_id` - the business key
- any number of additional **tracked attributes** (for example `plan`, `country`)

Rules:

- Snapshots may arrive unordered; process them by `snapshot_date`.
- A customer's first appearance opens their first version with `valid_from = snapshot_date`.
- On each later snapshot, if **any** tracked attribute differs from the customer's current version, close the current version (`valid_to = that snapshot_date`, `is_current = False`) and open a new version with `valid_from = that snapshot_date`.
- If nothing changed, no new version is created.
- The latest version of every customer has `valid_to = None` and `is_current = True`.
- Once a customer appears they appear in every later snapshot (no deletes to handle).
- Validity is half-open: a version is valid for `valid_from <= date < valid_to`.

Return one dict per version containing `customer_id`, every tracked attribute, `valid_from`, `valid_to`, `is_current`. Sort by `customer_id`, then `valid_from`.

### Example

```
snapshots = [
  {"snapshot_date": "2024-01-01", "customer_id": 1, "plan": "free",  "country": "PT"},
  {"snapshot_date": "2024-01-02", "customer_id": 1, "plan": "free",  "country": "PT"},
  {"snapshot_date": "2024-01-03", "customer_id": 1, "plan": "pro",   "country": "PT"},
]
build_scd2(snapshots) == [
  {"customer_id": 1, "plan": "free", "country": "PT", "valid_from": "2024-01-01", "valid_to": "2024-01-03", "is_current": False},
  {"customer_id": 1, "plan": "pro",  "country": "PT", "valid_from": "2024-01-03", "valid_to": None,         "is_current": True},
]
```

### Why interviewers ask this

SCD2 is *the* dimensional-modeling topic. Building it from snapshots (rather than a CDC stream) is exactly what dbt snapshots do, and it exposes whether you understand validity windows, change detection and ordering.
