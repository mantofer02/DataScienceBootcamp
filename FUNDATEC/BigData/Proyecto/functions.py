from pyspark.sql.functions import to_date
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import explode
from pyspark.sql.types import StructType, StructField, StringType, DoubleType


def init_spark():
    spark = SparkSession.builder.appName("HomeWork_MarcoFerraro").getOrCreate()
    sc = spark.sparkContext
    return spark, sc


# Initialize SparkSession
# spark = SparkSession.builder.appName("DateTransformAndJoin").getOrCreate()

# Sample data for DataFrame df1 with date format '2013-06-16'
# data1 = [("A", "2013-06-16"), ("B", "2013-06-17")]
# df1 = spark.createDataFrame(data1, ["Key", "Date1"])

# Sample data for DataFrame df2 with date format '7/30/2016'
# data2 = [("A", "7/30/2016"), ("C", "7/31/2016")]
# df2 = spark.createDataFrame(data2, ["Key", "Date2"])

# Transform date formats to 'yyyy-MM-dd' for both DataFrames
# df1 = df1.withColumn("Date1", to_date(df1["Date1"]))
# df2 = df2.withColumn("Date2", to_date(df2["Date2"], "M/d/yyyy"))

# Perform join operation on the common key column and date column
# joined_df = df1.join(df2, on=["Key"]).filter(df1["Date1"] == df2["Date2"])

# Show the joined DataFrame
# joined_df.show()

# Stop the SparkSession
# spark.stop()
