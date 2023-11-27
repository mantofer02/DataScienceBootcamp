from pyspark.sql import SparkSession, Window
from pyspark.sql import functions as F
from pyspark.sql.types import StructField, StructType, IntegerType, LongType, StringType, DateType, DecimalType
import os


def init_spark():
    spark = SparkSession.builder.appName("HomeWork_MarcoFerraro").getOrCreate()
    sc = spark.sparkContext
    return spark, sc


def create_df(spark, data_schema, path):
    if path:
        df = spark.read.csv(path, schema=data_schema)
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


def query_get_best_drivers(database, write_result=False):
    df_route = database['ruta']
    df_driver = database['ciclista']
    df_activity = database['actividad']

    join_df = df_driver.join(df_activity, on='cedula', how="inner")
    join_df = join_df.join(df_route, on="codigo", how="inner")

    result_df = join_df.groupBy("provincia", df_driver["nombre"]).agg(
        F.sum("kilometros").alias("total km"), F.round((F.sum("kilometros") / F.count("fecha")), 2).alias("%_kilometros_por_fecha"))

    window_spec = Window.partitionBy("provincia").orderBy(
        F.asc('provincia'), F.desc("total km"))

    result_df_with_rank = result_df.withColumn(
        "rank", F.row_number().over(window_spec))

    top5_result_df = result_df_with_rank.filter("rank <= 5").drop("rank")

    if write_result:
        top5_result_df.write.csv("results")

    return top5_result_df
