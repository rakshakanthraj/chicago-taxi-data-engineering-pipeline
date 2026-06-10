# Databricks notebook source
# MAGIC %md
# MAGIC ## Step 1: Check for Duplicates

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT trip_id, COUNT(*) AS cnt
# MAGIC FROM workspace.gold.fact_trips
# MAGIC GROUP BY trip_id
# MAGIC HAVING COUNT(*) > 1;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 2: Check for Null Keys (Orphans)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     COUNT(*) as total_trips,
# MAGIC     SUM(CASE WHEN customer_sk = sha2('Unknown', 256) THEN 1 ELSE 0 END) as unknown_customers,
# MAGIC     SUM(CASE WHEN driver_sk = sha2('Unknown', 256) THEN 1 ELSE 0 END) as unknown_drivers,
# MAGIC     SUM(CASE WHEN location_sk = sha2('Unknown', 256) THEN 1 ELSE 0 END) as unknown_locations
# MAGIC FROM gold.fact_trips;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 3: Verify "Missing" Member Joins

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     COUNT(*) AS total_trips,
# MAGIC     SUM(CASE WHEN customer_sk IS NULL THEN 1 ELSE 0 END) AS null_customers,
# MAGIC     SUM(CASE WHEN driver_sk IS NULL THEN 1 ELSE 0 END) AS null_drivers,
# MAGIC     SUM(CASE WHEN vehicle_sk IS NULL THEN 1 ELSE 0 END) AS null_vehicles
# MAGIC FROM workspace.gold.fact_trips;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     COUNT(*) AS total_trips,
# MAGIC     COUNT(CASE WHEN driver_sk != sha2('-1', 256) THEN 1 END) AS matched_drivers,
# MAGIC     (COUNT(CASE WHEN driver_sk != sha2('-1', 256) THEN 1 END) * 100.0 / COUNT(*)) AS driver_match_pct
# MAGIC FROM workspace.gold.fact_trips;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 4: The Final Revenue Reconciliation

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     'SILVER_LAYER' AS layer,
# MAGIC     COUNT(trip_id) AS total_records,
# MAGIC     SUM(fare_amount) AS total_revenue
# MAGIC FROM workspace.silver.trips
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT 
# MAGIC     'GOLD_LAYER' AS layer,
# MAGIC     COUNT(*) AS total_records, 
# MAGIC     SUM(fare_amount) AS total_revenue
# MAGIC FROM workspace.gold.fact_trips;