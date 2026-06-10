# Databricks notebook source
# MAGIC %md
# MAGIC /Workspace/source_data

# COMMAND ----------


dbutils.fs.mkdirs("/Workspace/bronze/checkpoints/customers")


# COMMAND ----------

dbutils.fs.ls("/Workspace/bronze/checkpoints")


# COMMAND ----------

# MAGIC %md
# MAGIC ## SPARK STREAMING
# MAGIC ### bronze layer

# COMMAND ----------

entities = ["customers","payments","trips","vehicles","drivers","locations"]

# COMMAND ----------

for entity in entities:


    df_batch = spark.read.format("csv")\
    .option("header", "true")\
    .option("inferSchema", "true")\
    .load(f"/Workspace/source_data/{entity}")

    schema_entity =df_batch.schema

    df = spark.readStream.format("csv")\
    .option("header", "true")\
    .schema(schema_entity)\
    .load(f"/Workspace/source_data/{entity}/")


    df.writeStream.format("delta") \
    .outputMode("append") \
    .option(
      "checkpointLocation",
      f"/Workspace/bronze/checkpoints/{entity}"
     ) \
    .trigger(once=True) \
    .toTable(f"bronze.{entity}")
