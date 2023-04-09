WITH locations_count AS (
SELECT
COUNT(*) as cnt
FROM {{ ref('dim_locations') }})

SELECT cnt
FROM locations_count
WHERE cnt < 85