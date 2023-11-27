from functions import get_file_name, is_csv_file, create_schema, query_get_best_drivers
from pyspark.sql.types import StructField, StructType, LongType, IntegerType, StringType
from pyspark.sql.functions import col
from pyspark.sql.types import DoubleType


def test_get_file_name():
    file_names = [
        'foo.csv',
        'data.java',
        'something.kafka',
        '20y2K.text'
    ]

    expected_results = [
        'foo',
        'data',
        'something',
        '20y2K'
    ]

    results = []

    for i in file_names:
        results.append(get_file_name(i))

    assert expected_results == results


def test_is_csv_files():
    file_names = [
        'foo.csv',
        'data.java',
        'something.csv',
        '20y2K.text'
    ]

    expected_results = [
        True,
        False,
        True,
        False
    ]

    results = []

    for i in file_names:
        results.append(is_csv_file(i))

    assert expected_results == results


def test_query_get_best_drivers(spark_session):
    mock_route = [(1, '1', 10), (2, '2', 20), (3, '3', 30)]
    mock_driver = [(100, 'Hoyt', 'A'),
                   (200, 'Patrick', 'C'),
                   (300, 'Donald', 'C'),
                   (400, 'Bailey', 'B'),
                   (500, 'Arlie', 'C')
                   ]

    mock_activity = [(3, 500, "2023-01-24"),
                     (1, 200, "2023-01-24"), (3, 400, "2023-02-24")]

    df_route = spark_session.createDataFrame(
        mock_route, schema=['codigo', 'nombre', 'kilometros'])
    df_driver = spark_session.createDataFrame(
        mock_driver, schema=['cedula', 'nombre', 'provincia'])
    df_activity = spark_session.createDataFrame(
        mock_activity, schema=['codigo', 'cedula', 'fecha'])

    database = {
        'ruta': df_route,
        'ciclista': df_driver,
        'actividad': df_activity
    }

    result_df = query_get_best_drivers(database)

    expected_result = spark_session.createDataFrame(
        [('B', 'Bailey', 30, 30), ('C', 'Arlie', 30, 30), ('C', 'Patrick', 10, 10)],
        schema=['provincia', 'nombre', 'total km', '%_kilometros_por_fecha']
    )

    expected_result = expected_result.withColumn(
        "%_kilometros_por_fecha", col(
            "%_kilometros_por_fecha").cast(DoubleType())
    )

    assert result_df.collect() == expected_result.collect()
