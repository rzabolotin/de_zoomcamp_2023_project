SELECT
    _id,
    createDate,
    subordination,
    type,
    nameShort,
    ticketsSold,
    status,
    category_name,
    isPushkinsCard,
    subordination_name

FROM
    {{ source("stage", "organizations") }}

{% if var('is_test_run', default=true) %}

  LIMIT 100

{% endif %}