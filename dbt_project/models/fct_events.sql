{{ config(
    materialized='table',
    partition_by={
      "field": "event_start",
      "data_type": "date",
      "granularity": "month"
    }
)}}

WITH unique_events AS (SELECT
    *,
    row_number() over(partition by _id) as row_number
FROM
    {{source('stage','events_partitioned')}})

SELECT
    _id,
    name,
    ageRestriction,
    isFree,
    price,
    COALESCE(isPushkinsCard, FALSE) AS isPushkinsCard,
    start AS event_start,
    `end` AS event_end,
    organization__id

FROM
    unique_events

WHERE
    row_number = 1

{% if var('is_test_run', default=true) %}

  LIMIT 100

{% endif %}