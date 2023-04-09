SELECT
    _id,
    name,
    timezone,
    stats_cinemas,
    stats_cinemaHalls

FROM
    {{ source("stage", "locales") }}
WHERE
    parentID = 1
{% if var('is_test_run', default=true) %}

  LIMIT 100

{% endif %}