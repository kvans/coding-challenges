-- Return user_id, streak_start, streak_end, streak_length for streaks >= 3 days
WITH days AS (
    SELECT DISTINCT user_id, login_date
    FROM logins
)
SELECT
    ...
FROM days
