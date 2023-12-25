from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import explode
from pyspark.sql.types import StructType, StructField, StringType, DoubleType


def init_spark():
    spark = SparkSession.builder.appName("HomeWork_MarcoFerraro").getOrCreate()
    sc = spark.sparkContext
    return spark, sc
