CREATE TABLE cdc_events (event_id INTEGER, customer_id INTEGER, op VARCHAR, email VARCHAR, status VARCHAR, updated_at TIMESTAMP);
INSERT INTO cdc_events VALUES
(1, 1, 'I', 'a@x.com',      'active',    '2024-01-01 10:00:00'),
(2, 1, 'U', 'a2@x.com',     'active',    '2024-01-02 10:00:00'),
(3, 2, 'I', 'b@x.com',      'active',    '2024-01-01 11:00:00'),
(4, 2, 'U', 'b@x.com',      'suspended', '2024-01-03 09:00:00'),
(5, 3, 'I', 'c@x.com',      'active',    '2024-01-01 12:00:00'),
(6, 3, 'D', NULL,           NULL,        '2024-01-04 12:00:00'),
(7, 4, 'I', 'd@x.com',      'active',    '2024-01-05 08:00:00'),
(8, 4, 'U', 'd-late@x.com', 'active',    '2024-01-05 08:00:00');
