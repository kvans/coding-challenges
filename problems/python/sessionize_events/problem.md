Raw clickstream events arrive unordered. Write `sessionize(events, gap_minutes=30)` that groups each user's events into sessions.

Each event is a dict `{"user_id": int, "ts": "YYYY-MM-DD HH:MM:SS"}`.

A **session** is a maximal run of a user's events (in time order) where consecutive events are at most `gap_minutes` apart. A gap **strictly greater** than `gap_minutes` starts a new session.

Return one dict per session:

```
{"user_id": ..., "session_id": n, "start": "...", "end": "...", "events": count}
```

- `session_id` is 1-based per user, in chronological order.
- `start` / `end` use the same timestamp format as the input.
- Sort the output by `user_id`, then `start`.

### Example

```
Input: events = [
    {"user_id": 1, "ts": "2024-06-01 10:00:00"},
    {"user_id": 1, "ts": "2024-06-01 10:20:00"},
    {"user_id": 1, "ts": "2024-06-01 11:30:00"},
    {"user_id": 2, "ts": "2024-06-01 09:00:00"},
  ], gap_minutes = 30
Output: [
    {"user_id": 1, "session_id": 1, "start": "2024-06-01 10:00:00", "end": "2024-06-01 10:20:00", "events": 2},
    {"user_id": 1, "session_id": 2, "start": "2024-06-01 11:30:00", "end": "2024-06-01 11:30:00", "events": 1},
    {"user_id": 2, "session_id": 1, "start": "2024-06-01 09:00:00", "end": "2024-06-01 09:00:00", "events": 1},
  ]
```

### Why interviewers ask this

Sessionization is the canonical "gaps and islands" problem and shows up in web analytics, IoT and fraud. Expect the follow-up "now do it in SQL" (there is a hard SQL problem for exactly that).
