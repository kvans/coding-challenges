-- Return cohort_week, week_number, cohort_size, active_users, retention_pct
WITH cohorts AS (
    SELECT user_id, CAST(date_trunc('week', signup_date) AS DATE) AS cohort_week
    FROM users
)
SELECT
    ...
