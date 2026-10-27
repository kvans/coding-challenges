WITH ranked AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY updated_at DESC, event_id DESC
        ) AS rn
    FROM cdc_events
)
SELECT customer_id, email, status, updated_at
FROM ranked
WHERE rn = 1
  AND op <> 'D'
