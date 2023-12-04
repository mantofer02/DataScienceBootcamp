from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import explode


def init_spark():
    spark = SparkSession.builder.appName("HomeWork_MarcoFerraro").getOrCreate()
    sc = spark.sparkContext
    return spark, sc


def explode_json_column(df):
    df_exploded = df.select("identificador", explode("viajes").alias("viaje"))
    result_df = df_exploded.select("identificador", "viaje.*")
    return result_df


def process_postal_data(result_df, columns):
    postal_df = result_df.select(*columns)
    postal_df = postal_df.groupBy(columns[0]).agg(
        F.count(columns[0]).alias("cantidad_de_viajes"),
        F.sum(columns[1]).alias("total_de_km")
    )
    return postal_df


def combine_postal_dataframes(origin_df, destiny_df):
    combined_df = origin_df.select(
        F.col(origin_df.columns[0]).alias("codigo_postal"),
        F.lit("origen").alias("origen_destino"),
        F.col("cantidad_de_viajes")
    ).union(
        destiny_df.select(
            F.col(destiny_df.columns[0]).alias("codigo_postal"),
            F.lit("destino").alias("origen_destino"),
            F.col("cantidad_de_viajes")
        )
    )

    combined_df = combined_df.orderBy(
        "origen_destino", F.col("codigo_postal").cast("int"))

    return combined_df


def create_total_trips_df(trips_register_df):
    origin_columns = ["codigo_postal_origen", "kilometros"]
    destiny_columns = ["codigo_postal_destino", "kilometros"]

    origin_postal_df = process_postal_data(trips_register_df, origin_columns)
    destiny_postal_df = process_postal_data(trips_register_df, destiny_columns)

    combined_df = combine_postal_dataframes(
        origin_postal_df, destiny_postal_df)

    return combined_df


def process_postal_revenue_data(result_df, columns):
    postal_df = result_df.select(*columns)
    postal_df = postal_df.groupBy(columns[0]).agg(
        F.sum(F.expr(f"{columns[1]} * {columns[2]}")).alias("ingresos")
    )
    return postal_df


def combine_revenue_dataframes(origin_df, destiny_df):
    combined_df = origin_df.select(
        F.col(origin_df.columns[0]).alias("codigo_postal"),
        F.lit("origen").alias("origen_destino"),
        F.col("ingresos")
    ).union(
        destiny_df.select(
            F.col(destiny_df.columns[0]).alias("codigo_postal"),
            F.lit("destino").alias("origen_destino"),
            F.col("ingresos")
        )
    )
    combined_df = combined_df.orderBy(
        "origen_destino", F.col("codigo_postal").cast("int"))
    return combined_df


def create_total_revenue_df(trips_register_df):
    origin_columns = ["codigo_postal_origen", "kilometros", "precio_kilometro"]
    destiny_columns = ["codigo_postal_destino",
                       "kilometros", "precio_kilometro"]

    origin_postal_df = process_postal_revenue_data(
        trips_register_df, origin_columns)
    destiny_postal_df = process_postal_revenue_data(
        trips_register_df, destiny_columns)

    combined_df = combine_revenue_dataframes(
        origin_postal_df, destiny_postal_df)

    return combined_df


def create_drivers_df(trips_register_df):
    df = trips_register_df.groupBy("identificador").agg(
        F.sum("kilometros").alias("km_total"), F.sum(F.expr("kilometros * precio_kilometro")).alias("ingresos"))

    df = df.orderBy(F.col("identificador").cast("int"))

    return df


def create_metrics_df(trips_register_df, spark):

    drivers_df = create_drivers_df(trips_register_df)

    most_km_driver = drivers_df.orderBy(F.col(
        "km_total").cast("float").desc()).select("identificador").first()[0]

    most_revenue_driver = drivers_df.orderBy(F.col(
        "ingresos").cast("float").desc()).select("identificador").first()[0]

    percentil_25_value = drivers_df.orderBy(F.col(
        "ingresos").cast("float").asc()).approxQuantile("ingresos", [0.25], 0.0)[0]

    percentil_50_value = drivers_df.orderBy(F.col(
        "ingresos").cast("float").asc()).approxQuantile("ingresos", [0.5], 0.0)[0]

    percentil_75_value = drivers_df.orderBy(F.col(
        "ingresos").cast("float").asc()).approxQuantile("ingresos", [0.75], 0.0)[0]

    total_revenue_df = create_total_revenue_df(trips_register_df)

    revenue_origin_df = total_revenue_df.filter(
        total_revenue_df["origen_destino"] == "origen")

    revenue_destiny_df = total_revenue_df.filter(
        total_revenue_df["origen_destino"] == "destino")

    most_revenue_origin = revenue_origin_df.orderBy(F.col(
        "ingresos").cast("float").desc()).select("codigo_postal").first()[0]

    most_revenue_destiny = revenue_destiny_df.orderBy(F.col(
        "ingresos").cast("float").desc()).select("codigo_postal").first()[0]

    metrics_df = [
        ("persona_con_mas_kilometros", most_km_driver),
        ("persona_con_mas_ingresos", most_revenue_driver),
        ("percentil_25", percentil_25_value),
        ("percentil_50", percentil_50_value),
        ("percentil_75", percentil_75_value),
        ("codigo_postal_origen_con_mas_ingresos", most_revenue_origin),
        ("codigo_postal_destino_con_mas_ingresos", most_revenue_destiny)
    ]

    df = spark.createDataFrame(metrics_df, schema=["metrica", "valor"])

    return df
