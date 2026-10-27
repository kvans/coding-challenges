CREATE TABLE orders (order_id INTEGER, order_date DATE, amount DECIMAL(10,2), status VARCHAR);
INSERT INTO orders VALUES
(1, '2024-01-05', 60.00, 'completed'),
(2, '2024-01-20', 40.00, 'completed'),
(3, '2024-01-25', 500.00, 'cancelled'),
(4, '2024-02-02', 150.00, 'completed'),
(5, '2024-02-14', 75.00, 'refunded'),
(6, '2024-03-01', 70.00, 'completed'),
(7, '2024-03-31', 50.00, 'completed');
