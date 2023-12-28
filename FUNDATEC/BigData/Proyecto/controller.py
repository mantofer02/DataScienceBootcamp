import functions
import pprint


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

        # database[db_name] = read_csv_data(file_path, spark)

    pp.pprint(database)
