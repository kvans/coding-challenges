**logins** records every login; a user can log in many times a day:

| column | type |
|---|---|
| login_id | INTEGER |
| user_id | INTEGER |
| login_date | DATE |

A **streak** is a maximal run of consecutive calendar days on which the user logged in at least once. Return every streak of **three or more days**:

| column | meaning |
|---|---|
| user_id | |
| streak_start | first day of the streak |
| streak_end | last day of the streak |
| streak_length | number of days |

Row order does not matter.

### Example

User 1 logs in on Jan 1, 2 (twice), 3, 5, 6. User 2 logs in Jan 10 through Jan 14. User 3 logs in Jan 1, 3, 5.

| user_id | streak_start | streak_end | streak_length |
|---|---|---|---|
| 1 | 2024-01-01 | 2024-01-03 | 3 |
| 2 | 2024-01-10 | 2024-01-14 | 5 |

### Why interviewers ask this

Gaps-and-islands is the signature "medium" SQL pattern: streaks, consecutive failures, contiguous ranges. The date-minus-row-number trick is expected knowledge for senior data engineers.
