{{ config(materialized='table', schema='gold') }}

WITH date_spine AS (
    SELECT explode(sequence(to_date('2010-01-01'), to_date('2030-12-31'), interval 1 day)) as calendar_date
)

SELECT
    cast(date_format(calendar_date, 'yyyyMMdd') as int) as date_sk,
    calendar_date,
    year(calendar_date) as year,
    month(calendar_date) as month,
    day(calendar_date) as day,
    date_format(calendar_date, 'EEEE') as day_name
FROM date_spine

UNION ALL

SELECT
    -1 as date_sk,
    cast('1900-01-01' as date) as calendar_date,
    1900 as year,
    1 as month,
    1 as day,
    'Unknown' as day_name