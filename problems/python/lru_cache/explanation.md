**Idea:** a hash map for O(1) lookup plus an ordering structure for recency. `OrderedDict` is a hash map whose entries live in a doubly linked list, so `move_to_end` and `popitem(last=False)` are both O(1).

**Complexity:** O(1) per operation, O(capacity) space.

**Talking points**
- Be ready to implement it without `OrderedDict`: a dict mapping key -> node, plus a doubly linked list with sentinel head/tail nodes. Interviewers often ask for this after the quick version.
- `functools.lru_cache` exists for memoisation but does not expose `put`, so it does not satisfy the interface.
- Variants: LFU (evict least *frequently* used), TTL caches, and thread safety (wrap operations in a lock; discuss contention).
