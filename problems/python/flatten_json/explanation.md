**Idea:** depth-first walk carrying the path built so far. Non-empty dicts and lists recurse; everything else (scalars, `None`, and empty containers) is written to the output under the accumulated key.

**Complexity:** O(total number of nodes); recursion depth equals the nesting depth.

**Talking points**
- Lists are the design decision: indexing (`tags.0`) keeps a 1:1 mapping, while "exploding" lists into multiple rows is the other common choice (`json_normalize(record_path=...)`). Ask which the consumer wants.
- Key collisions: `{"a.b": 1, "a": {"b": 2}}` collide after flattening. A production flattener should detect or escape this.
- An iterative version with an explicit stack avoids Python's recursion limit on pathological depth.
