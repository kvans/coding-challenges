Two tables describe what was sold:

**products**

| column | type |
|---|---|
| product_id | INTEGER |
| name | VARCHAR |
| category | VARCHAR |

**order_items**

| column | type |
|---|---|
| item_id | INTEGER |
| order_id | INTEGER |
| product_id | INTEGER |
| quantity | INTEGER |
| unit_price | DECIMAL(10,2) |

Return the **three products with the highest total revenue**, where revenue is `SUM(quantity * unit_price)` across all order items.

Output columns: `product_id`, `name`, `revenue`. Order by revenue descending; break ties by `product_id` ascending. **Row order is graded.** Products with no sales cannot appear.

### Example

With a Monitor selling 300, a Keyboard 150, a Mouse 80, a Cable 50 and a Webcam with no sales, the answer is Monitor, Keyboard, Mouse.

### Why interviewers ask this

The simplest join-aggregate-rank question. The things that go wrong: forgetting the multiplication, grouping by name only (two products can share a name), and non-deterministic ties.
