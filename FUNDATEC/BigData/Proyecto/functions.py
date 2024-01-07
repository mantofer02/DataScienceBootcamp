from pyspark.sql.functions import to_date
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import col, to_date, date_format, year, month, concat_ws


def init_spark():
    spark = SparkSession \
        .builder \
        .appName("Basic JDBC pipeline") \
        .config("spark.driver.extraClassPath", "postgresql-42.2.14.jar") \
        .config("spark.executor.extraClassPath", "postgresql-42.2.14.jar") \
        .getOrCreate()
    sc = spark.sparkContext
    return spark, sc


def transform_date_format(df, date_column, desired_format='yyyy-MM-dd'):
    df = df.withColumn(date_column, to_date(df[date_column], 'M/d/yyyy'))

    df = df.withColumn(date_column, date_format(
        df[date_column], desired_format))

    return df


def drop_columns(df, columns_to_drop):
    updated_df = df.drop(*columns_to_drop)

    return updated_df


def drop_null_rows(df):
    updated_df = df.na.drop()

    return updated_df


def transform_date_drop_days(df, date_column):
    # Transform the date column to keep only the year and month in "yyyy-MM" format
    df = df.withColumn(date_column, date_format(df[date_column], "yyyy-MM"))

    return df


# Group by column and calculate averages
def aggregate_dataframe(df, groupby_columns, avg_columns):
    avg_exprs = [F.avg(col).alias(f"AVG_{col}") for col in avg_columns]
    aggregated_df = df.groupBy(*groupby_columns).agg(*avg_exprs)

    return aggregated_df


def inner_join_dataframes(df1, df2, join_column_df1, join_column_df2):

    # Create a Column object for the join condition
    join_condition = col(join_column_df1) == col(join_column_df2)

    # Perform inner join operation on the created join condition
    joined_df = df1.join(df2, on=join_condition, how="inner")

    return joined_df
