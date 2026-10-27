The `events` table records every action a user takes in the product.

| column | type | notes |
|---|---|---|
| event_id | INTEGER | unique |
| user_id | INTEGER | |
| event_type | VARCHAR | `login`, `view`, `click`, ... |
| event_ts | TIMESTAMP | when the event happened |

Write a query that returns **daily active users**: for each calendar day that has at least one event, the number of *distinct* users active that day.

Return two columns: `activity_date` (DATE) and `dau` (INTEGER). Row order does not matter.

### Example

For events

| event_id | user_id | event_type | event_ts |
|---|---|---|---|
| 1 | 1 | login | 2024-03-01 08:00:00 |
| 2 | 1 | view  | 2024-03-01 08:05:00 |
| 3 | 2 | login | 2024-03-01 23:59:00 |
| 4 | 2 | view  | 2024-03-02 00:01:00 |

the result is

| activity_date | dau |
|---|---|
| 2024-03-01 | 2 |
| 2024-03-02 | 1 |

### Why interviewers ask this

DAU/WAU/MAU is the most common metric a data engineer is asked to compute. The trap is counting events instead of users, or grouping on the raw timestamp.
