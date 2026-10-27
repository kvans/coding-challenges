CREATE TABLE products (product_id INTEGER, name VARCHAR, category VARCHAR);
CREATE TABLE order_items (item_id INTEGER, order_id INTEGER, product_id INTEGER, quantity INTEGER, unit_price DECIMAL(10,2));
INSERT INTO products VALUES
(1, 'Desk', 'Furniture'),
(2, 'Chair', 'Furniture'),
(3, 'Lamp', 'Lighting'),
(4, 'Chair', 'Furniture'),
(5, 'Rug', 'Decor'),
(6, 'Shelf', 'Furniture');
INSERT INTO order_items VALUES
(1, 200, 1, 1, 250.00),
(2, 201, 2, 4, 25.00),
(3, 202, 3, 2, 50.00),
(4, 203, 4, 1, 99.99),
(5, 204, 4, 1, 0.01),
(6, 205, 5, 3, 33.33);
