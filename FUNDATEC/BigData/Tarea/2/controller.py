import functions


def read_json_data(file_paths, spark):

    df = spark.read.json(file_paths, multiLine=True)
    return df


def write_to_csv(df, output_folder, output_file):
    output_path = f"{output_folder}/{output_file}"

    df.coalesce(1).write.mode("overwrite").option(
        "header", "true").csv(output_path)


def run(file_paths):
    spark, sc = functions.init_spark()

    df = read_json_data(file_paths, spark)
    trips_register_df = functions.explode_json_column(df)

    total_trips_df = functions.create_total_trips_df(trips_register_df)
    print(total_trips_df.show())
    write_to_csv(total_trips_df, output_folder="results",
                 output_file="total_viajes")

    total_revenue_df = functions.create_total_revenue_df(trips_register_df)
    print(total_revenue_df.show())
    write_to_csv(total_revenue_df, output_folder="results",
                 output_file="total_ingresos")

    metrics_df = functions.create_metrics_df(trips_register_df, spark)
    print(metrics_df.show())
    write_to_csv(metrics_df, output_folder="results", output_file="metricas")
