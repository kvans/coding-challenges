**customers**

| column | type |
|---|---|
| customer_id | INTEGER |
| name | VARCHAR |
| signup_date | DATE |

**orders**

| column | type | notes |
|---|---|---|
| order_id | INTEGER | |
| customer_id | INTEGER | NULL for guest checkouts |
| order_date | DATE | |
| amount | DECIMAL(10,2) | |

Return every customer who has **never placed an order**: columns `customer_id`, `name`. Row order does not matter.

### Example

Customers Ana(1), Bo(2), Cy(3), Di(4); orders exist for customers 1 and 3. Result: Bo and Di.

### Why interviewers ask this

It is a classic anti-join, and it has a famous trap: `WHERE customer_id NOT IN (SELECT customer_id FROM orders)` returns **no rows at all** if any order has a NULL customer_id. The second dataset checks exactly that.
