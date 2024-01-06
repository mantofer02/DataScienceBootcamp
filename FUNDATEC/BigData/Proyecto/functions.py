from pyspark.sql.functions import to_date
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import explode
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
from pyspark.sql.functions import to_date, date_format, year, month, concat_ws


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


def drop_columns(df, columns_to_drop):
    updated_df = df.drop(*columns_to_drop)

    return updated_df


def drop_null_rows(df):
    updated_df = df.na.drop()

    return updated_df


def transform_date_drop_days(df, date_column):
    """
    Only works with yyyy-MM-dd format
    """
    # Extract the year and month from the specified date column
    df_with_month_and_year = df.withColumn("Month_Year", concat_ws(
        "-", year(df[date_column]), month(df[date_column])))

    return df_with_month_and_year


# Group by column and calculate averages
def aggregate_dataframe(df, groupby_columns, avg_columns):
    avg_exprs = [F.avg(col).alias(f"AVG_{col}") for col in avg_columns]
    aggregated_df = df.groupBy(*groupby_columns).agg(*avg_exprs)

    return aggregated_df
