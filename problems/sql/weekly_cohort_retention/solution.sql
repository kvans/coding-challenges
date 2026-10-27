WITH cohorts AS (
    SELECT user_id, CAST(date_trunc('week', signup_date) AS DATE) AS cohort_week
    FROM users
),
sizes AS (
    SELECT cohort_week, COUNT(*) AS cohort_size
    FROM cohorts
    GROUP BY cohort_week
),
weekly_activity AS (
    SELECT
        c.cohort_week,
        a.user_id,
        (CAST(date_trunc('week', a.activity_date) AS DATE) - c.cohort_week) // 7 AS week_number
    FROM activity a
    JOIN cohorts c ON c.user_id = a.user_id
)
SELECT
    w.cohort_week,
    w.week_number,
    s.cohort_size,
    COUNT(DISTINCT w.user_id) AS active_users,
    ROUND(100.0 * COUNT(DISTINCT w.user_id) / s.cohort_size, 1) AS retention_pct
FROM weekly_activity w
JOIN sizes s ON s.cohort_week = w.cohort_week
WHERE w.week_number >= 0
GROUP BY w.cohort_week, w.week_number, s.cohort_size
