Same tables as *Customers Who Never Ordered*:

**customers**(`customer_id`, `name`, `signup_date`) and **orders**(`order_id`, `customer_id`, `order_date`, `amount`).

For **every** customer return:

| column | meaning |
|---|---|
| customer_id | |
| name | |
| order_count | number of orders, 0 if none |
| total_spent | sum of `amount`, 0 if none; NULL amounts contribute nothing |

Row order does not matter. Orders with a NULL `customer_id` (guest checkouts) belong to nobody.

### Example

Ana has orders of 30 and 20, Cy has one of 15.50, Bo and Di have none:

| customer_id | name | order_count | total_spent |
|---|---|---|---|
| 1 | Ana | 2 | 50.00 |
| 2 | Bo | 0 | 0 |
| 3 | Cy | 1 | 15.50 |
| 4 | Di | 0 | 0 |

### Why interviewers ask this

It checks three habits at once: picking the correct join direction, knowing that `COUNT(*)` and `COUNT(column)` differ, and defaulting NULL aggregates.
