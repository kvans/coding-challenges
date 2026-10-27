**Idea:** sort by start, then sweep. Maintain the last merged block; if the next interval starts at or before the block's end, extend the block's end with `max`, otherwise start a new block.

**Complexity:** O(n log n) for the sort, O(n) for the sweep. O(n) output space.

**Talking points**
- `max` is required, not just `end`: `[1, 10]` followed by `[2, 3]` must keep 10.
- Strict vs touching overlap is a requirements question. Here touching intervals merge (`<=`); half-open intervals `[start, end)` would use `<`.
- SQL version: it is a gaps-and-islands problem using a running `MAX(end) OVER (ORDER BY start ROWS UNBOUNDED PRECEDING)`.
