# Databricks notebook source
# MAGIC %sql
# MAGIC -- 1. Uniqueness Check (Ensure no duplicate Trip IDs)
# MAGIC -- Expected: count(*) should equal count(DISTINCT trip_id)
# MAGIC SELECT 
# MAGIC     COUNT(*) AS total_records, 
# MAGIC     COUNT(DISTINCT trip_id) AS unique_records 
# MAGIC FROM gold.fact_trips;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC -- 2. Non-Null Check (Ensure critical financial data is present)
# MAGIC -- Expected: 0
# MAGIC SELECT COUNT(*) 
# MAGIC FROM gold.fact_trips 
# MAGIC WHERE fare_amount IS NULL OR trip_id IS NULL;
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC -- 3. Referential Integrity Check (Ensure every trip maps to a vehicle)
# MAGIC -- Expected: 0
# MAGIC SELECT COUNT(*) 
# MAGIC FROM gold.fact_trips f 
# MAGIC LEFT JOIN gold.dim_vehicles v ON f.vehicle_sk = v.vehicle_sk 
# MAGIC WHERE v.vehicle_sk IS NULL;
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC -- 4. Logic/Business Constraint (Ensure no negative fares)
# MAGIC -- Expected: 0
# MAGIC SELECT COUNT(*) 
# MAGIC FROM gold.fact_trips 
# MAGIC WHERE fare_amount < 0;