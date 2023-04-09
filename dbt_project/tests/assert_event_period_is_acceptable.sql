WITH events_interval AS (
SELECT min(event_start) AS min_date, max(event_start) AS max_date
FROM {{ ref('fct_events') }})

SELECT
min_date,
max_date
FROM events_interval
WHERE min_date < {{ var('min_possible_start_date') }}
OR max_date > {{ var('max_possible_end_date') }}