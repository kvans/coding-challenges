**Idea:** two passes of window functions. First, `LAG` finds each click's predecessor and flags session starts (no predecessor, or gap > 30 min). Second, a cumulative `SUM` of the flags turns the flags into session numbers. Then it is an ordinary `GROUP BY`.

**Talking points**
- You cannot nest window functions, hence the CTE chain. Each CTE is one "pass" and corresponds to one shuffle/sort stage in a distributed engine.
- The frame on the running sum should be `ROWS`, not the default `RANGE`, so that two clicks with the identical timestamp do not share a boundary ambiguously.
- `>` vs `>=` on the gap is a product decision; be explicit. Google Analytics historically used 30 minutes of inactivity *or* midnight; some products also split on campaign change.
- Streaming engines implement this as a *session window* with a gap; the batch SQL version is what you use to backfill or audit it.
