**Idea:** bucket events per user, sort each bucket, then scan: whenever the gap to the previous event exceeds the threshold, close the current session and open a new one. Emit the final open session after the loop.

**Complexity:** O(n log n) because of the per-user sorts; O(n) space.

**Talking points**
- The boundary rule (strictly greater vs greater-or-equal) must be stated explicitly; off-by-one here silently changes every metric downstream.
- The SQL version uses `LAG(ts) OVER (PARTITION BY user_id ORDER BY ts)` to flag session starts and a running `SUM(flag)` to number them.
- In streaming systems (Flink, Spark Structured Streaming) this is a *session window*; late events can reopen a closed session, which is why batch re-sessionization over a lookback window is common.
