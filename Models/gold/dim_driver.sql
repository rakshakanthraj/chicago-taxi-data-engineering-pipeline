{{ config(materialized='table', schema='gold') }}

SELECT 
    sha2(trim(cast(driver_id as string)), 256) as driver_sk,
    CAST(driver_id AS STRING) as driver_id,
    fullname,
    phone_number,
    CAST(driver_rating AS FLOAT) as driver_rating,
    city,
    CAST('1900-01-01' AS TIMESTAMP) as dbt_valid_from,
    dbt_valid_to
FROM {{ ref('DimDrivers') }}
QUALIFY row_number() OVER (PARTITION BY driver_id ORDER BY dbt_valid_from DESC) = 1

UNION ALL

SELECT 
    sha2('Unknown', 256) as driver_sk, 
    'Unknown' as driver_id, 
    'Unknown' as fullname, 
    'Unknown' as phone_number, 
    0.0 as driver_rating, 
    'Unknown' as city,
    CAST('1900-01-01' AS TIMESTAMP) as dbt_valid_from, 
    CAST(NULL AS TIMESTAMP) as dbt_valid_to
