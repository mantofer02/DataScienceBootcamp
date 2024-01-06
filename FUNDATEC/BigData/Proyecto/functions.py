from pyspark.sql.functions import to_date
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import explode
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
from pyspark.sql.functions import to_date, date_format


def init_spark():
    spark = SparkSession.builder.appName("HomeWork_MarcoFerraro").getOrCreate()
    sc = spark.sparkContext
    return spark, sc


def transform_date_format(df, date_column, desired_format='yyyy-MM-dd'):
    """
    Parameters:
        df (DataFrame): Input Spark DataFrame.
        date_column (str): Name of the date column to transform.
        desired_format (str): Desired date format (e.g., 'yyyy-MM-dd').
    """

    transformed_df = df.withColumn(date_column, date_format(
        to_date(df[date_column]), desired_format))

    return transformed_df
