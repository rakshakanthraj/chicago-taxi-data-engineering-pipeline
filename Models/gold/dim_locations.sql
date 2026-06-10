{{ config(materialized='table', schema='gold') }}

SELECT 
    sha2(trim(cast(location_id as string)), 256) as location_sk,
    CAST(location_id AS STRING) as location_id,
    city,
    state,
    country,
    CAST('1900-01-01' AS TIMESTAMP) as dbt_valid_from,
    dbt_valid_to
FROM {{ ref('DimLocations') }}
QUALIFY row_number() OVER (PARTITION BY location_id ORDER BY dbt_valid_from DESC) = 1

UNION ALL

SELECT 
    sha2('Unknown', 256) as location_sk, 
    'Unknown' as location_id, 
    'Unknown' as city, 
    'Unknown' as state, 
    'Unknown' as country,
    CAST('1900-01-01' AS TIMESTAMP) as dbt_valid_from, 
    CAST(NULL AS TIMESTAMP) as dbt_valid_to
