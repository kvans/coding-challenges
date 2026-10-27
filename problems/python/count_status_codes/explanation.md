**Idea:** split each line on the double-quote character. A well-formed line yields at least three parts: prefix, request, suffix. The status is the first token of the suffix. Validate it is three digits and count it with a dict (or `collections.Counter`).

**Complexity:** O(total characters), O(distinct statuses) space.

**Talking points**
- Splitting the entire line on spaces breaks when the request path contains spaces or the user agent is appended. Anchoring on the quoted request is more robust.
- A regex such as `r'"[^"]*"\s+(\d{3})\b'` is a fine alternative; mention the trade-off (readability vs speed on huge files).
- In production you would stream the file line by line rather than loading a list, and emit counts per status *class* (2xx/4xx/5xx) for alerting.
