WITH days AS (
    SELECT DISTINCT user_id, login_date
    FROM logins
),
grouped AS (
    SELECT
        user_id,
        login_date,
        login_date - CAST(ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS INTEGER) AS grp
    FROM days
)
SELECT
    user_id,
    MIN(login_date) AS streak_start,
    MAX(login_date) AS streak_end,
    COUNT(*)        AS streak_length
FROM grouped
GROUP BY user_id, grp
HAVING COUNT(*) >= 3
