WITH monthly AS (
    SELECT
        CAST(date_trunc('month', order_date) AS DATE) AS month,
        SUM(amount) AS revenue
    FROM orders
    WHERE status = 'completed'
    GROUP BY 1
),
with_prev AS (
    SELECT
        month,
        revenue,
        LAG(month)   OVER (ORDER BY month) AS prev_month,
        LAG(revenue) OVER (ORDER BY month) AS prev_row_revenue
    FROM monthly
),
aligned AS (
    SELECT
        month,
        revenue,
        CASE WHEN prev_month = month - INTERVAL 1 MONTH THEN prev_row_revenue END AS prev_revenue
    FROM with_prev
)
SELECT
    month,
    revenue,
    prev_revenue,
    CASE WHEN prev_revenue IS NULL OR prev_revenue = 0 THEN NULL
         ELSE ROUND(100.0 * (revenue - prev_revenue) / prev_revenue, 2)
    END AS growth_pct
FROM aligned
