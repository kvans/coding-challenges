CREATE TABLE customers (customer_id INTEGER, name VARCHAR, signup_date DATE);
CREATE TABLE orders (order_id INTEGER, customer_id INTEGER, order_date DATE, amount DECIMAL(10,2));
INSERT INTO customers VALUES
(1, 'Ana', '2024-01-05'),
(2, 'Bo', '2024-01-06'),
(3, 'Cy', '2024-01-07'),
(4, 'Di', '2024-01-08'),
(5, 'Ed', '2024-01-09');
INSERT INTO orders VALUES
(20, 2, '2024-02-01', 30.00),
(21, NULL, '2024-02-02', 12.00),
(22, 4, '2024-02-03', 20.00),
(23, NULL, '2024-02-04', 8.00),
(24, 4, '2024-02-05', 5.00);
