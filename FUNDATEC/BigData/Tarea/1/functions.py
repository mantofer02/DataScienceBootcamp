from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, IntegerType, LongType, StringType, DateType, DecimalType
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

    if file_name == "actividad":
        data_schema = StructType([
            StructField("codigo", IntegerType(), True),
            StructField("cedula", LongType(), True),
            StructField("fecha", DateType(), True)
        ])

    elif file_name == "ciclista":
        data_schema = StructType([
            StructField("cedula", LongType(), True),
            StructField("nombre", StringType(), True),
            StructField("provincia", StringType(), True)
        ])

    elif file_name == "ruta":
        data_schema = StructType([
            StructField("codigo", IntegerType(), True),
            StructField("nombre", StringType(), True),
            StructField("kilometros", DecimalType(10, 2), True)
        ])

    return data_schema


def is_csv_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower() == '.csv'
