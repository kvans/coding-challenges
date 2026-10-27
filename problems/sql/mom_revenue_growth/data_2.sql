CREATE TABLE orders (order_id INTEGER, order_date DATE, amount DECIMAL(10,2), status VARCHAR);
INSERT INTO orders VALUES
(1,  '2024-01-10', 100.00, 'completed'),
(2,  '2024-02-10', 999.00, 'cancelled'),
(3,  '2024-03-10', 50.00,  'completed'),
(4,  '2024-04-01', 40.00,  'completed'),
(5,  '2024-05-15', 0.00,   'completed'),
(6,  '2024-06-20', 80.00,  'completed'),
(7,  '2024-06-21', 20.00,  'refunded'),
(8,  '2024-07-04', 33.33,  'completed'),
(9,  '2024-07-05', 66.67,  'completed'),
(10, '2024-12-31', 10.00,  'completed'),
(11, '2025-01-01', 12.50,  'completed');
