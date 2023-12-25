import functions


def read_csv_data(file_paths, spark):
    df = spark.read.csv(file_paths, header=True, inferSchema=True)

    return df


def run(file_paths):
    spark, sc = functions.init_spark()

    df = read_csv_data(file_paths, spark)
    print(df.show())
