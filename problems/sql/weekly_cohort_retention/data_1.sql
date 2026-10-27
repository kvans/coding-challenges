CREATE TABLE users (user_id INTEGER, signup_date DATE);
CREATE TABLE activity (activity_id INTEGER, user_id INTEGER, activity_date DATE);
INSERT INTO users VALUES
(1, '2024-01-01'),
(2, '2024-01-02'),
(3, '2024-01-03'),
(4, '2024-01-10');
INSERT INTO activity VALUES
(1, 1, '2024-01-01'),
(2, 1, '2024-01-09'),
(3, 1, '2024-01-16'),
(4, 2, '2024-01-02'),
(5, 2, '2024-01-10'),
(6, 3, '2024-01-03'),
(7, 4, '2024-01-10'),
(8, 4, '2024-01-24');
