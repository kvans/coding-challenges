CREATE TABLE events (
    event_id   INTEGER,
    user_id    INTEGER,
    event_type VARCHAR,
    event_ts   TIMESTAMP
);
INSERT INTO events VALUES
(1, 1, 'login', '2024-03-01 08:00:00'),
(2, 1, 'view',  '2024-03-01 08:05:00'),
(3, 2, 'login', '2024-03-01 23:59:00'),
(4, 2, 'view',  '2024-03-02 00:01:00'),
(5, 3, 'login', '2024-03-02 10:00:00'),
(6, 3, 'click', '2024-03-02 10:02:00'),
(7, 1, 'login', '2024-03-02 12:00:00'),
(8, 4, 'login', '2024-03-04 09:00:00'),
(9, 4, 'view',  '2024-03-04 09:01:00'),
(10, 2, 'login','2024-03-04 20:00:00');
