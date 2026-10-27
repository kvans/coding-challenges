**clicks**

| column | type |
|---|---|
| click_id | INTEGER |
| user_id | INTEGER |
| click_ts | TIMESTAMP |

Group each user's clicks into sessions. A new session starts at a user's first click and whenever the gap since their previous click is **strictly greater than 30 minutes**.

Return one row per session:

| column | meaning |
|---|---|
| user_id | |
| session_id | 1-based per user, in chronological order |
| session_start | first click timestamp |
| session_end | last click timestamp |
| click_count | number of clicks |

Row order does not matter.

### Example

User 1 clicks at 10:00, 10:20 and 11:30; user 2 clicks once at 09:00.

| user_id | session_id | session_start | session_end | click_count |
|---|---|---|---|---|
| 1 | 1 | 2024-06-01 10:00:00 | 2024-06-01 10:20:00 | 2 |
| 1 | 2 | 2024-06-01 11:30:00 | 2024-06-01 11:30:00 | 1 |
| 2 | 1 | 2024-06-01 09:00:00 | 2024-06-01 09:00:00 | 1 |

### Why interviewers ask this

Sessionization in pure SQL is the hard version of gaps-and-islands: it needs two stacked window functions (`LAG` to detect boundaries, cumulative `SUM` to label islands) and precise boundary semantics. It is also the SQL twin of the Python *Sessionize User Events* problem.
