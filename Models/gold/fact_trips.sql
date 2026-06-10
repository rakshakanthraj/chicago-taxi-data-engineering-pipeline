{{ config(materialized='table', schema='gold') }}

WITH base_trips AS (
    SELECT * FROM (
        SELECT *, ROW_NUMBER() OVER (PARTITION BY trip_id ORDER BY trip_start_time DESC) as rn
        FROM {{ ref('trips') }}
    ) WHERE rn = 1
),

customers as (SELECT customer_sk, customer_id, dbt_valid_from, dbt_valid_to FROM {{ ref('dim_customers') }}),
drivers as (SELECT driver_sk, driver_id, dbt_valid_from, dbt_valid_to FROM {{ ref('dim_driver') }}),
locations as (SELECT location_sk, location_id, dbt_valid_from, dbt_valid_to FROM {{ ref('dim_locations') }}),
payments as (SELECT payment_sk, payment_id, dbt_valid_from, dbt_valid_to FROM {{ ref('dim_payments') }}),
vehicles as (SELECT vehicle_sk, vehicle_id, dbt_valid_from, dbt_valid_to FROM {{ ref('dim_vehicles') }})

SELECT
    t.trip_id,
    CAST(t.vehicle_id AS STRING) as vehicle_id, -- Keep for debugging
    COALESCE(c.customer_sk, sha2('Unknown', 256)) as customer_sk,
    COALESCE(dr.driver_sk, sha2('Unknown', 256)) as driver_sk,
    COALESCE(l.location_sk, sha2('Unknown', 256)) as location_sk,
    COALESCE(p.payment_sk, sha2('Unknown', 256)) as payment_sk,
    COALESCE(v.vehicle_sk, sha2('Unknown', 256)) as vehicle_sk,
    COALESCE(cast(date_format(t.trip_start_time, 'yyyyMMdd') as int), -1) as trip_date_sk,
    t.trip_start_time,
    t.fare_amount,
    t.distance_km
FROM base_trips t
LEFT JOIN customers c ON CAST(t.customer_id AS STRING) = c.customer_id
    AND t.trip_start_time >= c.dbt_valid_from AND (t.trip_start_time < c.dbt_valid_to OR c.dbt_valid_to IS NULL)
LEFT JOIN drivers dr ON CAST(t.driver_id AS STRING) = dr.driver_id
    AND t.trip_start_time >= dr.dbt_valid_from AND (t.trip_start_time < dr.dbt_valid_to OR dr.dbt_valid_to IS NULL)
LEFT JOIN locations l ON CAST(t.pickup_location_id AS STRING) = l.location_id
    AND t.trip_start_time >= l.dbt_valid_from AND (t.trip_start_time < l.dbt_valid_to OR l.dbt_valid_to IS NULL)
LEFT JOIN payments p ON CAST(t.payment_id AS STRING) = p.payment_id
    AND t.trip_start_time >= p.dbt_valid_from AND (t.trip_start_time < p.dbt_valid_to OR p.dbt_valid_to IS NULL)
LEFT JOIN vehicles v ON CAST(t.vehicle_id AS STRING) = v.vehicle_id
    AND t.trip_start_time >= v.dbt_valid_from AND (t.trip_start_time < v.dbt_valid_to OR v.dbt_valid_to IS NULL)
--first commmit