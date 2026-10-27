-- Return order_id, customer_id, order_date, tier, amount (tier as of order_date)
SELECT
    f.order_id,
    f.customer_id,
    f.order_date,
    ... AS tier,
    f.amount
FROM fact_orders f
LEFT JOIN dim_customer d
    ON ...
