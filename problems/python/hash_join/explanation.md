**Idea:** classic two-phase hash join. *Build*: hash the right input into `key -> [rows]`. *Probe*: for each left row look up its key and emit the merged rows; for a left join emit a None-padded row when nothing matched.

**Complexity:** O(|L| + |R| + |output|) time, O(|R|) extra space. Output can be larger than both inputs when keys repeat.

**Talking points**
- Build the *smaller* side. That is what Spark's broadcast join does, and why skewed keys (one key with millions of rows) blow up memory and output size.
- NULL handling: `NULL = NULL` is unknown in SQL, so `None` keys are excluded from the index and never probe successfully.
- Column collisions: real engines prefix or alias colliding columns; the problem rules them out to keep the focus on semantics.
- Sort-merge join is the alternative when both sides are too big for memory but already sorted or partitioned by the key.
