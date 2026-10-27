You are merging `k` already-sorted inputs (think: sorted run files from an external sort, or per-partition sorted outputs) into one sorted sequence.

Write `merge_sorted_streams(streams)` where `streams` is a list of **iterators** yielding integers in non-decreasing order. Return a list with all values in non-decreasing order.

Constraints and expectations:

- Each stream is a one-shot iterator: you cannot call `len()`, index it, or rewind it. You may only call `next()` on it.
- Do **not** materialise every stream into memory and sort. Your algorithm should hold at most one element per stream at a time, so it is O(k) extra memory while producing output. (The harness cannot police memory, but your interviewer will.)
- Target O(N log k) time where N is the total number of elements.
- Streams can be empty. Values can repeat across streams.

### Example

```
Input:  streams = [iter([1, 4, 9]), iter([2, 3, 10]), iter([]), iter([0, 5])]
Output: [0, 1, 2, 3, 4, 5, 9, 10]
```

### Why interviewers ask this

K-way merge is the heart of external sorting, merging sorted partitions, log-structured storage compaction (LSM trees) and merging time-ordered event files. They want the heap, and they want to hear you say "O(k) memory".
