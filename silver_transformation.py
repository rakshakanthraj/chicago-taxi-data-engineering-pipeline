# Databricks notebook source
# MAGIC %md
# MAGIC ### **CUSTOMERS**

# COMMAND ----------

# MAGIC %sql
# MAGIC -- select * from workspace.bronze.trips limit 10;

# COMMAND ----------

spark = spark

# COMMAND ----------

from custom_utils import transformationss as transformations

# COMMAND ----------

from pyspark.sql.functions import * 
from pyspark.sql.types import *
from pyspark.sql import functions 
from typing import List
from pyspark.sql import DataFrame
from pyspark.sql.window import Window
from delta.tables import DeltaTable


# COMMAND ----------



# class transformations:
#         def dedup(self,df:DataFrame,dedup_cols:List,cdc:str):

#             df = df.withColumn("dedupKey",concat(*dedup_cols))
#             df = df.withColumn("dedupcounts",row_number().over(Window.partitionBy("dedupKey").orderBy(desc(cdc))))
#             df = df.filter(col("dedupcounts") == 1)
#             df = df.drop("dedupKey","dedupcounts")
#             return df
        
#         def process_timestamp(self,df):
#             df = df.withColumn("processed_timestamp",current_timestamp())
#             return df
        
#         def upsert(self,df,key_cols,table,cdc):
#             merge_conditions = ' AND '.join([f"src.{i} = trg.{i}" for i in key_cols])
#             dlt_obj = DeltaTable.forName(spark,f"Workspace.silver.{table}")
#             dlt_obj.alias("trg").merge(df.alias("src"),merge_conditions)\
#             .whenMatchedUpdateAll(condition = f'src.{cdc} >= trg.{cdc}')\
#             .whenNotMatchedInsertAll()\
#             .execute()

             
             
#             return 1


# COMMAND ----------

# MAGIC %md
# MAGIC # CUSTOMERS

# COMMAND ----------

import os
import sys

# COMMAND ----------

current_directory = os.getcwd()
sys.path.append(current_directory)


# COMMAND ----------

df_cust = spark.read.table("Workspace.bronze.customers")

# COMMAND ----------

df_cust = df_cust.withColumn("domain",split(col("email"),"@")[1])

# COMMAND ----------

df_cust= df_cust.withColumn(
    "no_extension",
    regexp_replace(col("phone_number"), "(?i)x\\d+$", "")
)

df_cust = df_cust.withColumn(
    "phone_number",
    regexp_replace(col("no_extension"), "[^0-9]", "")
)

# COMMAND ----------

df_cust = df_cust.withColumn("fullname", concat(col("first_name"), lit(" "), col("last_name")))
df_cust = df_cust.drop("first_name", "last_name")

# COMMAND ----------

cust_obj = transformations()
cust_df_trans = cust_obj.dedup(df_cust,['customer_id'],'last_updated_timestamp')

# COMMAND ----------

df_cust = cust_obj.process_timestamp(cust_df_trans)
df_cust.show()

# COMMAND ----------

if  spark.catalog.tableExists("Workspace.silver.customers"):
    
    cust_obj.upsert(
        df_cust,
        ['customer_id'],
        'customers',
        'last_updated_timestamp'
    )

else:
    
    df_cust.write.format("delta") \
        .mode("append") \
        .saveAsTable("Workspace.silver.customers")

# COMMAND ----------

# MAGIC %md
# MAGIC # DRIVERS

# COMMAND ----------

df_driver = spark.read.table("Workspace.bronze.drivers")

# COMMAND ----------

df_driver = df_driver.withColumn(
    "no_extension",
    regexp_replace(col("phone_number"), "(?i)x\\d+$", "")
)

df_driver = df_driver.withColumn(
    "phone_number",
    regexp_replace(col("no_extension"), "[^0-9]", "")
)

# COMMAND ----------

df_driver = df_driver.withColumn("fullname", concat(col("first_name"), lit(" "), col("last_name")))
df_driver = df_driver.drop("first_name", "last_name")

# COMMAND ----------

driver_obj = transformations()
driver_df_trans = driver_obj.dedup(df_driver,['driver_id'],'last_updated_timestamp')

# COMMAND ----------

df_driver = driver_obj.process_timestamp(df_driver)

# COMMAND ----------

if spark.catalog.tableExists("Workspace.silver.drivers"):
    
    driver_obj.upsert(
        df_driver,
        ['driver_id'],
        'drivers',
        'last_updated_timestamp'
    )

else:
    
    df_driver.write.format("delta") \
        .mode("append") \
        .saveAsTable("Workspace.silver.drivers")

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) from workspace.silver.drivers

# COMMAND ----------

# MAGIC %md
# MAGIC # LOCATIONS

# COMMAND ----------

df_loc = spark.read.table("Workspace.bronze.locations")
display(df_loc)

# COMMAND ----------

loc_obj = transformations()
df_loc_trans = loc_obj.dedup(df_loc,['location_id'],'last_updated_timestamp')
df_loc = loc_obj.process_timestamp(df_loc_trans)
if spark.catalog.tableExists("Workspace.silver.locations"):
    
    loc_obj.upsert(
        df_loc,
        ['location_id'],
        'locations',
        'last_updated_timestamp'
    )

else:
    
    df_loc.write.format("delta") \
        .mode("append") \
        .saveAsTable("Workspace.silver.locations")


# COMMAND ----------

# MAGIC %md
# MAGIC # PAYMENTS

# COMMAND ----------

df_paym = spark.read.table("Workspace.bronze.payments")

# COMMAND ----------

df_paym = df_paym.withColumn(
    "online_payment_status",
    when((col("payment_method") == "Card") & (col("payment_status") == "Success"),
    "online_success")
    .when((col("payment_method") == "Card") & (col("payment_status") == "Failed"),
    "online_failed")
    .when((col("payment_method") == "Card") & (col("payment_status") == "Pending"),
    "online_pending")
    .otherwise("offline")
)

# COMMAND ----------

display(df_paym)

# COMMAND ----------

paym_obj = transformations()
df_paym_trans = paym_obj.dedup(df_paym,['payment_id'],'last_updated_timestamp')
df_paym = paym_obj.process_timestamp(df_paym)
if spark.catalog.tableExists("Workspace.silver.payments"):
    
    paym_obj.upsert(
        df_paym,
        ['payment_id'],
        'payments',
        'last_updated_timestamp'
    )

else:
    
    df_paym.write.format("delta") \
        .mode("overwrite") \
        .saveAsTable("Workspace.silver.payments")

# COMMAND ----------

# MAGIC %md
# MAGIC # VEHICLES

# COMMAND ----------

df_vehicle = spark.read.table("Workspace.bronze.vehicles")
display(df_vehicle)

# COMMAND ----------

df_vehicle = df_vehicle.withColumn("make",upper(col("make")))
display(df_vehicle)

# COMMAND ----------


vehi_obj = transformations()
df_vehicle_trans = vehi_obj.dedup(df_vehicle,['vehicle_id'],'last_updated_timestamp')
df_vehicle = vehi_obj.process_timestamp(df_vehicle)
if spark.catalog.tableExists("Workspace.silver.vehicles"):
    
    vehi_obj.upsert(
        df_vehicle,
        ['vehicle_id'],
        'vehicles',
        'last_updated_timestamp'
    )

else:
    
    df_vehicle.write.format("delta") \
        .mode("append") \
        .saveAsTable("Workspace.silver.vehicles")


# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA IF NOT EXISTS workspace.gold;
# MAGIC