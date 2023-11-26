from pyspark.sql import SparkSession
from pyspark.sql.types import (IntegerType, StringType, DateType)
import sys
import os


def init_spark():
    spark = SparkSession.builder.appName("HomeWork_MarcoFerraro").getOrCreate()
    sc = spark.sparkContext
    return spark, sc


def create_df(spark, data_schema, path):
    if path:
        df = spark.read.format('.csv', schema=data_schema, path=path)
        print(df.printSchema())
        return df
    else:
        return None


def get_file_name(file_path):
    file_name_without_extension, _ = os.path.splitext(
        os.path.basename(file_path))
    return file_name_without_extension


def create_schema(file_name):
    data_schema = None

    if file_name == "Actividad":
        pass
    elif file_name == "Ciclista":
        pass
    elif file_name == "Ruta":
        pass

    return data_schema
