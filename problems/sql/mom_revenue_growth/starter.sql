-- Return month, revenue, prev_revenue, growth_pct
WITH monthly AS (
    SELECT
        ...
    FROM orders
    WHERE status = 'completed'
    GROUP BY 1
)
SELECT
    ...
FROM monthly
