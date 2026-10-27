Given a list of integers `nums` and an integer `target`, return the indices of the two numbers that add up to `target`.

Exactly one valid answer exists for every test, and you may not use the same element twice. Return the indices in ascending order.

### Example 1

```
Input:  nums = [2, 7, 11, 15], target = 9
Output: [0, 1]
```

### Example 2

```
Input:  nums = [3, 2, 4], target = 6
Output: [1, 2]
```

### Constraints

- `2 <= len(nums) <= 10^5`
- `-10^9 <= nums[i], target <= 10^9`
- Aim for O(n) time.

### Why interviewers ask this

It is the warm-up that checks you reach for a hash map instead of nested loops. Expect a follow-up like "what if the list is sorted?" (two pointers) or "what if it is a stream?".
