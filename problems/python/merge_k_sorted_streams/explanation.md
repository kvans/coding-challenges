**Idea:** seed a min-heap with the head of every non-empty stream as `(value, stream_index)`. Repeatedly pop the minimum, append it, and push the next element from that same stream. The heap never holds more than k entries.

**Complexity:** O(N log k) time, O(k) extra memory (plus the output list, which in a real system you would stream out instead of collecting).

**Talking points**
- `heapq.merge(*streams)` does exactly this lazily; know it exists, then implement it by hand when asked.
- The `(value, index)` tuple makes ties comparable even if values were non-comparable objects; include a sequence counter if you ever store un-orderable payloads.
- This is the merge step of external sort: sort chunks that fit in memory, spill them, k-way merge the spills. Also how LSM-tree compaction and "merge sorted partitions" in distributed engines work.
