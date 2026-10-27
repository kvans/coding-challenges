CREATE TABLE dim_customer (customer_id INTEGER, tier VARCHAR, valid_from DATE, valid_to DATE);
CREATE TABLE fact_orders (order_id INTEGER, customer_id INTEGER, order_date DATE, amount DECIMAL(10,2));
INSERT INTO dim_customer VALUES
(1, 'bronze', '2024-01-01', '2024-03-01'),
(1, 'gold',   '2024-03-01', NULL),
(2, 'silver', '2024-02-01', NULL);
INSERT INTO fact_orders VALUES
(1, 1, '2024-01-15', 10.00),
(2, 1, '2024-03-01', 20.00),
(3, 1, '2024-02-29', 30.00),
(4, 2, '2024-01-20', 40.00),
(5, 2, '2024-05-05', 50.00),
(6, 3, '2024-05-05', 60.00);
