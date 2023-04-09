SELECT
    event_id,
    locale_id

FROM
    {{ source("stage", "event_locales") }}

{% if var('is_test_run', default=true) %}

  LIMIT 100

{% endif %}