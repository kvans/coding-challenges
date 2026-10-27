CREATE TABLE cdc_events (event_id INTEGER, customer_id INTEGER, op VARCHAR, email VARCHAR, status VARCHAR, updated_at TIMESTAMP);
INSERT INTO cdc_events VALUES
(1,  10, 'I', 'ten@x.com',     'active',   '2024-03-01 00:00:00'),
(2,  10, 'U', 'ten-new@x.com', 'active',   '2024-03-05 00:00:00'),
(3,  10, 'U', 'ten-old@x.com', 'inactive', '2024-03-03 00:00:00'),
(4,  11, 'I', 'e@x.com',       'active',   '2024-03-01 00:00:00'),
(5,  11, 'D', NULL,            NULL,       '2024-03-02 00:00:00'),
(6,  11, 'I', 'e-again@x.com', 'active',   '2024-03-06 00:00:00'),
(7,  12, 'D', NULL,            NULL,       '2024-03-01 00:00:00'),
(8,  13, 'I', 'm@x.com',       'active',   '2024-03-07 12:00:00'),
(9,  13, 'U', 'm@x.com',       'vip',      '2024-03-07 12:00:00'),
(10, 13, 'U', 'm@x.com',       'churned',  '2024-03-07 12:00:00'),
(11, 14, 'I', 'z@x.com',       'active',   '2024-03-08 00:00:00'),
(12, 14, 'D', NULL,            NULL,       '2024-03-09 00:00:00'),
(13, 14, 'U', 'z-late@x.com',  'active',   '2024-03-08 12:00:00');
