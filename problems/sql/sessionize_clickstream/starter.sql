-- Return user_id, session_id, session_start, session_end, click_count
WITH flagged AS (
    SELECT
        user_id,
        click_ts,
        ... AS is_new_session
    FROM clicks
),
numbered AS (
    SELECT
        user_id,
        click_ts,
        ... AS session_id
    FROM flagged
)
SELECT
    ...
FROM numbered
GROUP BY user_id, session_id
