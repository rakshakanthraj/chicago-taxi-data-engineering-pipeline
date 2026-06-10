{{ config(materialized='table', schema='gold') }}

SELECT 
    sha2(trim(cast(customer_id as string)), 256) as customer_sk,
    CAST(customer_id AS STRING) as customer_id,
    fullname,
    email,
    CAST('1900-01-01' AS TIMESTAMP) as dbt_valid_from,
    dbt_valid_to
FROM {{ ref('DimCustomers') }}
QUALIFY row_number() OVER (PARTITION BY customer_id ORDER BY dbt_valid_from DESC) = 1

UNION ALL

SELECT 
    sha2('Unknown', 256) as customer_sk, 
    'Unknown' as customer_id, 
    'Unknown' as fullname, 
    'Unknown' as email,
    CAST('1900-01-01' AS TIMESTAMP) as dbt_valid_from, 
    CAST(NULL AS TIMESTAMP) as dbt_valid_to
