{{ config(materialized='table', schema='gold') }}

SELECT 
    sha2(trim(cast(vehicle_id as string)), 256) as vehicle_sk,
    CAST(vehicle_id AS STRING) as vehicle_id,
    make,
    model,
    CAST(year AS INT) as year,
    -- Hardcode to 1900 to catch all historical trips
    CAST('1900-01-01' AS TIMESTAMP) as dbt_valid_from,  
    dbt_valid_to     
FROM {{ ref('DimVehicles') }}
QUALIFY row_number() OVER (PARTITION BY vehicle_id ORDER BY dbt_valid_from DESC) = 1

UNION ALL

SELECT 
    sha2('Unknown', 256) as vehicle_sk, 
    'Unknown' as vehicle_id, 
    'Unknown' as make, 
    'Unknown' as model, 
    0 as year,
    CAST('1900-01-01' AS TIMESTAMP) as dbt_valid_from, 
    CAST(NULL AS TIMESTAMP) as dbt_valid_to
