CREATE TABLE customers (customer_id INTEGER, name VARCHAR, signup_date DATE);
CREATE TABLE orders (order_id INTEGER, customer_id INTEGER, order_date DATE, amount DECIMAL(10,2));
INSERT INTO customers VALUES
(1, 'Ana', '2024-01-05'),
(2, 'Bo', '2024-01-06'),
(3, 'Cy', '2024-01-07'),
(4, 'Di', '2024-01-08');
INSERT INTO orders VALUES
(10, 1, '2024-02-01', 30.00),
(11, 1, '2024-02-03', 20.00),
(12, 3, '2024-02-05', 15.50);
