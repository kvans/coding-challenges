CREATE TABLE products (product_id INTEGER, name VARCHAR, category VARCHAR);
CREATE TABLE order_items (item_id INTEGER, order_id INTEGER, product_id INTEGER, quantity INTEGER, unit_price DECIMAL(10,2));
INSERT INTO products VALUES
(1, 'Keyboard', 'Hardware'),
(2, 'Mouse', 'Hardware'),
(3, 'Monitor', 'Hardware'),
(4, 'Cable', 'Accessories'),
(5, 'Webcam', 'Hardware');
INSERT INTO order_items VALUES
(1, 100, 1, 2, 50.00),
(2, 100, 2, 1, 20.00),
(3, 101, 3, 1, 300.00),
(4, 102, 1, 1, 50.00),
(5, 103, 4, 10, 5.00),
(6, 104, 2, 3, 20.00);
