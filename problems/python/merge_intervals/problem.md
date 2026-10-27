Given a list of closed intervals `[start, end]`, merge all overlapping or touching intervals and return the result sorted by start.

Two intervals overlap when they share at least one point, so `[1, 4]` and `[4, 5]` merge into `[1, 5]`.

### Example 1

```
Input:  [[1, 3], [2, 6], [8, 10], [15, 18]]
Output: [[1, 6], [8, 10], [15, 18]]
```

### Example 2

```
Input:  [[1, 4], [4, 5]]
Output: [[1, 5]]
```

### Constraints

- `0 <= len(intervals) <= 10^5`
- `start <= end` for every interval
- The input is not necessarily sorted.

### Why interviewers ask this

Besides being a top-20 LeetCode classic, it is exactly how you collapse overlapping sessions, maintenance windows or on-call shifts in a pipeline.
