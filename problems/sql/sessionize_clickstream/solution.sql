WITH flagged AS (
    SELECT
        user_id,
        click_ts,
        CASE
            WHEN LAG(click_ts) OVER (PARTITION BY user_id ORDER BY click_ts) IS NULL THEN 1
            WHEN click_ts - LAG(click_ts) OVER (PARTITION BY user_id ORDER BY click_ts) > INTERVAL 30 MINUTE THEN 1
            ELSE 0
        END AS is_new_session
    FROM clicks
),
numbered AS (
    SELECT
        user_id,
        click_ts,
        SUM(is_new_session) OVER (
            PARTITION BY user_id
            ORDER BY click_ts
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS session_id
    FROM flagged
)
SELECT
    user_id,
    session_id,
    MIN(click_ts) AS session_start,
    MAX(click_ts) AS session_end,
    COUNT(*)      AS click_count
FROM numbered
GROUP BY user_id, session_id
