from typing import List
from pyspark.sql import DataFrame
from pyspark.sql.window import Window
from delta.tables import DeltaTable
from pyspark.sql.functions import concat,row_number,current_timestamp,desc,col
from pyspark.sql.types import *
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()


class transformationss:
        def dedup(self,df:DataFrame,dedup_cols:List,cdc:str):

            df = df.withColumn("dedupKey",concat(*dedup_cols))
            df = df.withColumn("dedupcounts",row_number().over(Window.partitionBy("dedupKey").orderBy(desc(cdc))))
            df = df.filter(col("dedupcounts") == 1)
            df = df.drop("dedupKey","dedupcounts")
            return df
        
        def process_timestamp(self,df):
            df = df.withColumn("processed_timestamp",current_timestamp())
            return df
        
        def upsert(self,df,key_cols,table,cdc):
            merge_conditions = ' AND '.join([f"src.{i} = trg.{i}" for i in key_cols])
            dlt_obj = DeltaTable.forName(spark,f"Workspace.silver.{table}")
            dlt_obj.alias("trg").merge(df.alias("src"),merge_conditions)\
            .whenMatchedUpdateAll(condition =  f'src.{cdc} >= trg.{cdc}')\
            .whenNotMatchedInsertAll()\
            .execute()

             
             
            return 1
