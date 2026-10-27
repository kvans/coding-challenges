-- Return sale_date, revenue, running_total, rolling_avg_7d ordered by sale_date
SELECT
    sale_date,
    revenue,
    ... AS running_total,
    ... AS rolling_avg_7d
FROM daily_sales
ORDER BY sale_date
