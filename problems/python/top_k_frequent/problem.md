Given a list of integers `nums` and an integer `k`, return the `k` most frequent values, ordered from most to least frequent. When two values have the same frequency, the **smaller value comes first**.

### Example 1

```
Input:  nums = [1, 1, 1, 2, 2, 3], k = 2
Output: [1, 2]
```

### Example 2

```
Input:  nums = [4, 4, 7, 7, 1], k = 2
Output: [4, 7]      # 4 and 7 tie on frequency, 4 is smaller
```

### Constraints

- `1 <= k <= number of distinct values`
- Aim for better than O(n log n). Be ready to discuss heap vs bucket-sort approaches.

### Why interviewers ask this

"Top N by count" is the most common aggregation in analytics ("top products", "top error messages"). They want to hear you reason about a heap of size k versus a full sort, and about tie-breaking.
