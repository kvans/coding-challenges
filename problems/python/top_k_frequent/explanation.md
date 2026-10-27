**Idea:** count with a `Counter`, then select the k keys with the best `(-count, value)` key. `heapq.nsmallest` keeps a heap of size k, giving O(m log k) over m distinct values.

**Complexity:** O(n + m log k) time, O(m) space.

**Alternatives worth naming**
- Full sort: `sorted(counts, key=lambda v: (-counts[v], v))[:k]` - simplest, O(m log m).
- Bucket sort: index values by their count (counts are bounded by n), then walk buckets from high to low. O(n) time but needs a secondary sort inside buckets to honour the tie rule.
- In SQL this is `ORDER BY COUNT(*) DESC, value LIMIT k`; in streaming it becomes approximate (Count-Min Sketch / Space-Saving) once distinct values do not fit in memory.
