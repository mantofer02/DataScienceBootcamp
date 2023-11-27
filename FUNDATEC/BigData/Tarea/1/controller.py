import functions


def run(file_paths):
    spark, sc = functions.init_spark()

    database = {}

    for path in file_paths:
        if functions.is_csv_file(path) == True:

            file_name = functions.get_file_name(path)
            schema = functions.create_schema(file_name)
            df = functions.create_df(
                spark=spark, data_schema=schema, path=path)

            database[file_name] = df

    result_df = functions.query_get_best_drivers(database, write_result=True)
    print(result_df.show())
