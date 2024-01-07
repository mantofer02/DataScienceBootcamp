from functions import transform_date_format, inner_join_dataframes, aggregate_dataframe, transform_date_drop_days, drop_columns, drop_null_rows


def test_transform_date_format(spark_session):
    mock_data = [("1/1/2022",),
                 ("2/2/2022",),
                 ("3/3/2022",)]

    column_names = ["date_column"]

    mock_df = spark_session.createDataFrame(mock_data, column_names)

    result_df = transform_date_format(mock_df, "date_column", 'yyyy-MM-dd')

    expected_data = [("2022-01-01",),
                     ("2022-02-02",),
                     ("2022-03-03",)]

    expected_df = spark_session.createDataFrame(expected_data, ["date_column"])

    assert result_df.collect() == expected_df.collect()


def test_drop_columns(spark_session):
    mock_data = [("1/1/2022", "1", "John"),
                 ("2/2/2022", "2", "Doe"),
                 ("3/3/2022", "3", "Smith")]

    column_names = ["date_column", "id", "name"]

    mock_df = spark_session.createDataFrame(mock_data, column_names)

    result_df = drop_columns(mock_df, ["date_column", "name"])

    expected_data = [("1",),
                     ("2",),
                     ("3",)]

    expected_df = spark_session.createDataFrame(expected_data, ["id"])

    assert result_df.collect() == expected_df.collect()


def test_drop_null_rows(spark_session):
    mock_data = [("1/1/2022", "1", "John"),
                 ("2/2/2022", None, "Doe"),
                 ("3/3/2022", "3", None)]

    column_names = ["date_column", "id", "name"]

    mock_df = spark_session.createDataFrame(mock_data, column_names)

    result_df = drop_null_rows(mock_df)

    expected_data = [("1/1/2022", "1", "John")]

    expected_df = spark_session.createDataFrame(
        expected_data, ["date_column", "id", "name"])

    assert result_df.collect() == expected_df.collect()


def test_transform_date_drop_days(spark_session):
    mock_data = [("2022-01-02",),
                 ("2022-02-03",),
                 ("2022-03-03",)]

    column_names = ["date_column"]

    mock_df = spark_session.createDataFrame(mock_data, column_names)

    result_df = transform_date_drop_days(mock_df, "date_column")

    expected_data = [("2022-01",),
                     ("2022-02",),
                     ("2022-03",)]

    expected_df = spark_session.createDataFrame(expected_data, ["date_column"])

    assert result_df.collect() == expected_df.collect()


def test_aggregate_dataframe(spark_session):
    mock_data = [("argentina", 100),
                 ("costa rica", 50),
                 ("argentina", 200),
                 ("argentina", 150)]

    column_names = ["country", "income"]

    mock_df = spark_session.createDataFrame(mock_data, column_names)

    result_df = aggregate_dataframe(mock_df, ["country"], ["income"])

    expected_data = [("costa rica", 50.0),
                     ("argentina", 150.0)
                     ]

    expected_df = spark_session.createDataFrame(
        expected_data, ["country", "income"])

    assert result_df.collect() == expected_df.collect()


def test_inner_join_dataframes(spark_session):
    # Mock data for the first DataFrame (df1)
    data_df1 = [(1, "A"),
                (2, "B"),
                (3, "C")]

    column_names_df1 = ["id1", "value_df1"]

    df1 = spark_session.createDataFrame(data_df1, column_names_df1)

    # Mock data for the second DataFrame (df2)
    data_df2 = [(1, "X"),
                (2, "Y"),
                (3, "Z")]

    column_names_df2 = ["id2", "value_df2"]

    df2 = spark_session.createDataFrame(data_df2, column_names_df2)

    result_df = inner_join_dataframes(df1, df2, "id1", "id2")

    expected_data = [(1, "A", 1, "X"),
                     (2, "B", 2, "Y"),
                     (3, "C", 3, "Z")]

    column_names_expected = ["id1", "value_df1", "id2", "value_df2"]

    expected_df = spark_session.createDataFrame(
        expected_data, column_names_expected)

    assert result_df.collect() == expected_df.collect()
