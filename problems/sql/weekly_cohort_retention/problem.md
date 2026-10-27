**users**

| column | type |
|---|---|
| user_id | INTEGER |
| signup_date | DATE |

**activity**

| column | type |
|---|---|
| activity_id | INTEGER |
| user_id | INTEGER |
| activity_date | DATE |

Build a weekly retention table. A user's **cohort** is the ISO week (Monday start, `date_trunc('week', ...)`) of their signup. A user is *retained in week k* if they have any activity whose week is exactly k weeks after the cohort week (week 0 is the signup week itself).

Return one row per `(cohort_week, week_number)` that has at least one active user:

| column | meaning |
|---|---|
| cohort_week | DATE, Monday of the signup week |
| week_number | 0, 1, 2, ... |
| cohort_size | number of users who signed up in that week (including users with no activity) |
| active_users | distinct users from the cohort active in that week |
| retention_pct | `ROUND(100.0 * active_users / cohort_size, 1)` |

Activity dated before the user's signup week must be ignored. Row order does not matter.

### Example

Three users sign up in the week of 2024-01-01 and one in the week of 2024-01-08. If users 1 and 2 are active again the following week and only user 1 the week after:

| cohort_week | week_number | cohort_size | active_users | retention_pct |
|---|---|---|---|---|
| 2024-01-01 | 0 | 3 | 3 | 100.0 |
| 2024-01-01 | 1 | 3 | 2 | 66.7 |
| 2024-01-01 | 2 | 3 | 1 | 33.3 |
| 2024-01-08 | 0 | 1 | 1 | 100.0 |
| 2024-01-08 | 2 | 1 | 1 | 100.0 |

### Why interviewers ask this

Cohort retention is the canonical "hard" analytics query: it combines date bucketing, a self-describing join, distinct counts and a denominator computed at a different grain than the numerator. Getting the denominator right (cohort size, not active-user count) is the point.
