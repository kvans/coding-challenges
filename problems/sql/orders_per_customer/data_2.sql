CREATE TABLE customers (customer_id INTEGER, name VARCHAR, signup_date DATE);
CREATE TABLE orders (order_id INTEGER, customer_id INTEGER, order_date DATE, amount DECIMAL(10,2));
INSERT INTO customers VALUES
(1, 'Ana', '2024-01-05'),
(2, 'Bo', '2024-01-06'),
(3, 'Cy', '2024-01-07');
INSERT INTO orders VALUES
(20, 1, '2024-02-01', 10.00),
(21, 1, '2024-02-02', NULL),
(22, NULL, '2024-02-03', 99.00),
(23, 3, '2024-02-04', NULL),
(24, NULL, '2024-02-05', 1.00);
