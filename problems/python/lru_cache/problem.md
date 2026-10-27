Design a **least-recently-used cache** with a fixed capacity.

Implement class `LRUCache`:

- `LRUCache(capacity: int)` - initialise with positive capacity.
- `get(key: int) -> int` - return the value if the key exists, otherwise `-1`. A successful `get` makes the key most-recently used.
- `put(key: int, value: int) -> None` - insert or update the value. The key becomes most-recently used. If inserting exceeds the capacity, evict the least-recently-used key first.

Both operations must run in **O(1)** average time.

### Example

```
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
cache.get(1)      # 1
cache.put(3, 3)   # evicts key 2
cache.get(2)      # -1
cache.put(4, 4)   # evicts key 1
cache.get(1)      # -1
cache.get(3)      # 3
cache.get(4)      # 4
```

Tests feed a sequence of operations; the harness instantiates your class and calls the methods, collecting return values (`null` for `put` and the constructor).

### Why interviewers ask this

The most common "design" question. For data engineers it maps directly to lookup caches in enrichment jobs, dimension caches in streaming joins, and the eviction logic of any buffer pool.
