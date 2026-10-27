SELECT
    CAST(event_ts AS DATE) AS activity_date,
    COUNT(DISTINCT user_id) AS dau
FROM events
GROUP BY 1
