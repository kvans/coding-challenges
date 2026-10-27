**dim_customer** is a Type 2 dimension with half-open validity windows `[valid_from, valid_to)`; the current version has `valid_to = NULL`:

| column | type |
|---|---|
| customer_id | INTEGER |
| tier | VARCHAR |
| valid_from | DATE |
| valid_to | DATE (NULL = current) |

**fact_orders**

| column | type |
|---|---|
| order_id | INTEGER |
| customer_id | INTEGER |
| order_date | DATE |
| amount | DECIMAL(10,2) |

For every order return the customer's **tier as it was on the order date**:

Output columns: `order_id`, `customer_id`, `order_date`, `tier`, `amount`.

Rules:

- An order dated exactly on a version's `valid_from` belongs to that (new) version.
- An order placed before the customer's first version, or for a customer missing from the dimension, must still be returned with `tier = NULL`.
- Every order appears exactly once. Row order does not matter.

### Example

Customer 1 was *bronze* from 2024-01-01 and *gold* from 2024-03-01. An order on 2024-02-29 is bronze; an order on 2024-03-01 is gold. Customer 2's first version starts 2024-02-01, so their order on 2024-01-20 gets a NULL tier.

### Why interviewers ask this

Joining facts to an SCD2 dimension "as of" the event date is the payoff of building SCD2 in the first place. Candidates often use closed intervals (double counting boundary days) or an inner join (silently dropping orders).
