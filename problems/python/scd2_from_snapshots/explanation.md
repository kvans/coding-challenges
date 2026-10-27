**Idea:** sort snapshots by date and fold them into per-customer version lists. Change detection is a dict comparison of the tracked attributes against the current version. A change closes the current version on the snapshot date and opens a new one on the same date (half-open intervals, so there is no gap and no overlap).

**Complexity:** O(n log n) for the sort, O(n) for the fold.

**Talking points**
- Half-open `[valid_from, valid_to)` makes point-in-time joins a clean `valid_from <= d AND (valid_to IS NULL OR d < valid_to)`; closed intervals force "minus one day" arithmetic and off-by-one bugs.
- Comparing a dict of attributes (or a hash of them) is how the dbt snapshot `check` strategy works; the `timestamp` strategy uses an `updated_at` column instead.
- Hard parts in production: deletes (close the version with no replacement), late-arriving snapshots (rebuild from that date forward), and attribute sets that change over time (schema evolution).
