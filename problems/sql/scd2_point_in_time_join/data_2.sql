CREATE TABLE dim_customer (customer_id INTEGER, tier VARCHAR, valid_from DATE, valid_to DATE);
CREATE TABLE fact_orders (order_id INTEGER, customer_id INTEGER, order_date DATE, amount DECIMAL(10,2));
INSERT INTO dim_customer VALUES
(7, 'free',       '2023-12-01', '2024-01-10'),
(7, 'pro',        '2024-01-10', '2024-01-20'),
(7, 'enterprise', '2024-01-20', NULL),
(8, 'free',       '2024-06-01', '2024-06-02'),
(8, 'pro',        '2024-06-02', NULL),
(9, 'free',       '2024-01-01', '2024-02-01');
INSERT INTO fact_orders VALUES
(10, 7, '2024-01-09', 1.00),
(11, 7, '2024-01-10', 2.00),
(12, 7, '2024-01-19', 3.00),
(13, 7, '2024-01-20', 4.00),
(14, 7, '2025-01-01', 5.00),
(15, 7, '2023-11-30', 6.00),
(16, 8, '2024-06-01', 7.00),
(17, 8, '2024-06-02', 8.00),
(18, 9, '2024-01-15', 9.00),
(19, 9, '2024-02-01', 10.00),
(20, 9, '2024-03-01', 11.00);
