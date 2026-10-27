**Idea:** keep a dict `key -> best record so far`. For each record, replace the stored one when its timestamp is greater *or equal* (equal means "later in the feed", which should win). Finally emit the dict's values ordered by key.

**Complexity:** O(n + k log k) where k is the number of distinct keys. One pass, no sorting of the full input.

**Talking points**
- Sorting the whole list by `(key, ts)` and taking the last of each group also works but is O(n log n) and needs care with the tie rule.
- The SQL equivalent is `QUALIFY ROW_NUMBER() OVER (PARTITION BY key ORDER BY ts DESC, ingest_seq DESC) = 1`. Mention that a secondary ordering column (sequence number / offset) is what makes ties deterministic in real pipelines.
- At scale this is a reduce-by-key; the dict approach is exactly what a streaming job keeps in its keyed state store.
