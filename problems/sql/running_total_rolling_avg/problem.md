**daily_sales** has exactly one row per calendar day with no gaps:

| column | type |
|---|---|
| sale_date | DATE |
| revenue | DECIMAL(10,2) |

For every day return:

| column | meaning |
|---|---|
| sale_date | |
| revenue | |
| running_total | cumulative revenue from the first day up to and including this day |
| rolling_avg_7d | `ROUND(average revenue over this day and the 6 preceding days, 2)`; for the first six days use however many days exist |

Order the output by `sale_date` ascending. **Row order is graded.**

### Example

| sale_date | revenue | running_total | rolling_avg_7d |
|---|---|---|---|
| 2024-01-01 | 100.00 | 100.00 | 100.00 |
| 2024-01-02 | 200.00 | 300.00 | 150.00 |
| 2024-01-03 | 150.00 | 450.00 | 150.00 |
| ... | | | |

### Why interviewers ask this

Window frames are where many candidates get vague. Running totals and trailing averages appear in every KPI dashboard, and the `ROWS` vs `RANGE` distinction (and what happens with gaps) is a favourite follow-up.
