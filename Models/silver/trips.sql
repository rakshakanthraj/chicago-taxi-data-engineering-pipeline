{{ config(materialized='table', schema='silver') }}

SELECT
    cast(trip_id as integer) as trip_id,
    cast(customer_id as integer) as customer_id,
    cast(start_location as string) as pickup_location_id, 
    
    -- Real columns that exist in Bronze
    cast(driver_id as integer) as driver_id,
    cast(vehicle_id as integer) as vehicle_id,

    -- FIX: Rename payment_method to payment_id so Gold can join on it
    cast(payment_method as string) as payment_id, 

    cast(trip_start_time as timestamp) as trip_start_time,
    cast(trip_end_time as timestamp) as trip_end_time,
    cast(distance_km as decimal(10,2)) as distance_km,
    cast(fare_amount as decimal(10,2)) as fare_amount
FROM {{ source('source_bronze', 'trips') }}
WHERE trip_id IS NOT NULL