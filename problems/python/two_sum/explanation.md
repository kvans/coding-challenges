**Idea:** scan once, remembering each value's index. For every element check whether `target - x` has already been seen; if so, that earlier index and the current index are the answer.

**Complexity:** O(n) time, O(n) extra space.

**Talking points**
- Insert into the map *after* the lookup so an element cannot pair with itself (matters when `target = 2 * x`).
- Sorted input allows an O(1)-space two-pointer solution, but you lose the original indices unless you sort `(value, index)` pairs.
- Duplicates are fine: the first occurrence is what stays in the map, which still yields a valid pair.
