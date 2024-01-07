import functions
import pprint

CLIMATE_TABLE = "climate_data_nepal"
MARKET_TABLE = "kalimati_market_data"


def read_csv_data(file_path, spark):
    df = spark.read.csv(file_path, header=True, inferSchema=True)

    return df


def run(file_paths):
    spark, sc = functions.init_spark()
    pp = pprint.PrettyPrinter(indent=4)

    database = {}
    for file_path in file_paths:
        db_name = file_path.split('/')[-1].split('.')[0]
        print(f"Reading data from {db_name} database...")

        database[db_name] = read_csv_data(file_path, spark)

    database[CLIMATE_TABLE] = functions.drop_null_rows(
        database[CLIMATE_TABLE])
    database[MARKET_TABLE] = functions.drop_null_rows(
        database[MARKET_TABLE])

    database[CLIMATE_TABLE] = functions.drop_columns(
        database[CLIMATE_TABLE], ["DISTRICT", "LAT", "LON", "PRECTOT", "PS", "QV2M", "RH2M", "T2MWET", "T2M_RANGE", "TS", "WS10M", "WS10M_MAX", "WS10M_MIN", "WS10M_RANGE", "WS50M", "WS50M_MAX", "WS50M_MIN", "WS50M_RANGE"])
    database[MARKET_TABLE] = functions.drop_columns(
        database[MARKET_TABLE], ["SN"])

    database[CLIMATE_TABLE] = functions.transform_date_format(
        database[CLIMATE_TABLE], "DATE")

    database[CLIMATE_TABLE] = functions.transform_date_drop_days(
        database[CLIMATE_TABLE], "DATE"
    )
    database[MARKET_TABLE] = functions.transform_date_drop_days(
        database[MARKET_TABLE], "Date"
    )

    database[CLIMATE_TABLE] = functions.aggregate_dataframe(
        database[CLIMATE_TABLE], ["DATE"], ["T2M", "T2M_MAX", "T2M_MIN"])
    database[MARKET_TABLE] = functions.aggregate_dataframe(
        database[MARKET_TABLE], ["Date", "Commodity"], ["Minimum", "Maximum", "Average"])

    database[MARKET_TABLE] = database[MARKET_TABLE].withColumnRenamed(
        "Date", "market_date")
    database[CLIMATE_TABLE] = database[CLIMATE_TABLE].withColumnRenamed(
        "DATE", "climate_date")

    df = functions.inner_join_dataframes(
        database[CLIMATE_TABLE], database[MARKET_TABLE], "climate_date", "market_date")

    df = functions.drop_columns(df, ["market_date"])

    df.write \
        .format("jdbc") \
        .mode('overwrite') \
        .option("url", "jdbc:postgresql://host.docker.internal:5433/postgres") \
        .option("user", "postgres") \
        .option("password", "testPassword") \
        .option("dbtable", "gold_table") \
        .save()

    pp.pprint(df.show())
