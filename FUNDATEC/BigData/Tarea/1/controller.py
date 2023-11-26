import functions


def run(file_paths):
    spark, sc = functions.init_spark()

    data_base = {}

    for path in file_paths:
        if functions.is_csv_file(path) == True:

            file_name = functions.get_file_name(path)
            schema = functions.create_schema(file_name)
            df = functions.create_df(
                spark=spark, data_schema=schema, path=path)

            data_base[file_name] = df
            print(df.show())
