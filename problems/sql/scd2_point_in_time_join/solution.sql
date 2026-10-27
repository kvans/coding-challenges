SELECT
    f.order_id,
    f.customer_id,
    f.order_date,
    d.tier,
    f.amount
FROM fact_orders f
LEFT JOIN dim_customer d
    ON  d.customer_id = f.customer_id
    AND d.valid_from <= f.order_date
    AND (d.valid_to IS NULL OR f.order_date < d.valid_to)
