# Databricks notebook source
# MAGIC %sql
# MAGIC -- 1. OVERALL BUSINESS HEALTH
# MAGIC -- Provides the core metrics for management reporting
# MAGIC SELECT 
# MAGIC     COUNT(trip_id) AS total_trips,
# MAGIC     ROUND(SUM(fare_amount), 2) AS total_revenue,
# MAGIC     ROUND(AVG(fare_amount), 2) AS avg_fare_per_trip,
# MAGIC     ROUND(SUM(distance_km), 2) AS total_distance_covered
# MAGIC FROM gold.fact_trips;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC --2.TOP 5 CUSTOMERS BY SPEND
# MAGIC -- Highlights customer loyalty and revenue concentration
# MAGIC SELECT 
# MAGIC c.fullname,
# MAGIC COUNT(f.trip_id) AS trip_count,
# MAGIC ROUND(SUM(f.fare_amount), 2) AS total_spent
# MAGIC FROM gold.fact_trips f
# MAGIC JOIN gold.dim_customers c ON f.customer_sk = c.customer_sk
# MAGIC GROUP BY 1
# MAGIC ORDER BY total_spent DESC
# MAGIC LIMIT 5;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC -- 3. PEAK OPERATIONAL HOUR
# MAGIC -- Identifies the busiest time for the fleet
# MAGIC SELECT 
# MAGIC     hour(trip_start_time) AS trip_hour, 
# MAGIC     COUNT(*) AS trip_count
# MAGIC FROM gold.fact_trips
# MAGIC GROUP BY 1
# MAGIC ORDER BY trip_count DESC
# MAGIC LIMIT 1;
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC -- 4. REVENUE BY VEHICLE MAKE
# MAGIC -- Using 'make' since 'vehicle_type' is not in the schema
# MAGIC SELECT 
# MAGIC     v.make,
# MAGIC     ROUND(SUM(f.fare_amount), 2) AS total_revenue
# MAGIC FROM gold.fact_trips f
# MAGIC JOIN gold.dim_vehicles v ON f.vehicle_sk = v.vehicle_sk
# MAGIC GROUP BY 1
# MAGIC ORDER BY total_revenue DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- 5. DATA INTEGRITY AUDIT
# MAGIC -- Proves that  pipeline successfully maintains referential integrity
# MAGIC SELECT 
# MAGIC     count(*) as total_trips,
# MAGIC     count(CASE WHEN driver_sk != sha2('-1', 256) THEN 1 END) as matched_drivers,
# MAGIC     count(CASE WHEN payment_sk != sha2('-1', 256) THEN 1 END) as matched_payments,
# MAGIC     (count(CASE WHEN driver_sk != sha2('-1', 256) THEN 1 END) / count(*)) * 100 as driver_match_rate
# MAGIC FROM gold.fact_trips;