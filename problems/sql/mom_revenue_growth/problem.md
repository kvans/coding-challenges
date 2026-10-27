**orders**

| column | type |
|---|---|
| order_id | INTEGER |
| order_date | DATE |
| amount | DECIMAL(10,2) |
| status | VARCHAR (`completed`, `cancelled`, `refunded`) |

Compute monthly revenue from **completed** orders and the growth versus the previous calendar month.

Output columns:

| column | meaning |
|---|---|
| month | first day of the month (DATE) |
| revenue | SUM(amount) of completed orders in that month |
| prev_revenue | revenue of the **previous calendar month**, NULL if that month had no completed orders |
| growth_pct | `ROUND(100.0 * (revenue - prev_revenue) / prev_revenue, 2)`, NULL when prev_revenue is NULL or 0 |

Only months that have at least one completed order appear. Row order does not matter.

### Example

Jan 100, Feb 150, Mar 120 (cancelled orders ignored):

| month | revenue | prev_revenue | growth_pct |
|---|---|---|---|
| 2024-01-01 | 100.00 | NULL | NULL |
| 2024-02-01 | 150.00 | 100.00 | 50.00 |
| 2024-03-01 | 120.00 | 150.00 | -20.00 |

### Why interviewers ask this

Period-over-period metrics are the bread and butter of finance dashboards. The subtle part is that `LAG` looks at the previous *row*, so a missing month silently compares against the wrong period unless you check the date too.
