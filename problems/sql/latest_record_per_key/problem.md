A change-data-capture feed appends one row per change to **cdc_events**:

| column | type | notes |
|---|---|---|
| event_id | INTEGER | monotonically increasing ingest sequence |
| customer_id | INTEGER | business key |
| op | VARCHAR | `I` insert, `U` update, `D` delete |
| email | VARCHAR | NULL on deletes |
| status | VARCHAR | NULL on deletes |
| updated_at | TIMESTAMP | source change time |

Rebuild the **current state** of the customers table: one row per customer with the values from their latest event. A customer whose latest event is a delete must not appear.

"Latest" means the greatest `updated_at`; if two events share the same `updated_at`, the greater `event_id` wins.

Output columns: `customer_id`, `email`, `status`, `updated_at`. Row order does not matter.

### Example

Customer 3 is inserted then deleted (excluded). Customer 4 has two events with the same timestamp; the one with the higher `event_id` wins.

### Why interviewers ask this

"Latest row per key" is the single most common window-function question for data engineers: it is how you compact a CDC log, dedupe a Kafka replay, or build a Type 1 dimension. The ordering tie-break and the delete handling are where candidates slip.
