{{ config(materialized='table', schema='gold') }}

SELECT 
    sha2(trim(cast(payment_id as string)), 256) as payment_sk,
    CAST(payment_id AS STRING) as payment_id,
    payment_method,
    payment_status,
    CAST('1900-01-01' AS TIMESTAMP) as dbt_valid_from,
    dbt_valid_to
FROM {{ ref('DimPayments') }}
QUALIFY row_number() OVER (PARTITION BY payment_id ORDER BY dbt_valid_from DESC) = 1

UNION ALL

SELECT 
    sha2('Unknown', 256) as payment_sk, 
    'Unknown' as payment_id, 
    'Unknown' as payment_method, 
    'Unknown' as payment_status,
    CAST('1900-01-01' AS TIMESTAMP) as dbt_valid_from, 
    CAST(NULL AS TIMESTAMP) as dbt_valid_to
