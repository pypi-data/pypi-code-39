import pytest
import optel.datalake.ingest as ingest


@pytest.fixture()
def tables():
    return ["1", "2", "3", "4"]


@pytest.fixture()
def base_source():
    return "base"


def test_load_sql_tables(mocker, tables, false_spark):
    dfs = ingest.load_sql_tables("db-test", tables, "", "", "", false_spark)

    for table in tables:
        assert dfs[table]

    mocker.patch("optel.datalake.ingest.default_spark")
    dfs = ingest.load_sql_tables("db-test", tables, "", "", "")
    ingest.default_spark.assert_called_once()

    for table in tables:
        assert dfs[table]


def test_read_csv(mocker, false_spark):
    mocker.patch("optel.datalake.ingest.default_spark")
    ingest.read_csv("test")
    ingest.default_spark.assert_called_once()

    ingest.read_csv("test", false_spark)

    calls = []
    call = mocker.call
    calls.append(call.format("csv"))
    calls.append(call.option("header", "true"))
    calls.append(call.option("inferSchema", "true"))
    calls.append(call.load("test"))

    false_spark.assert_has_calls(calls, any_order=True)


def test_read_json(spark_session, json_file):
    df = ingest.read_json(
        json_file.strpath, spark=spark_session, multiline="true"
    )
    assert set(df.columns) == {"ID", "name"}


def test_read_parquet(mocker, false_spark):
    mocker.patch("optel.datalake.ingest.default_spark")
    ingest.read_parquet("test")
    ingest.default_spark.assert_called_once()

    ingest.read_parquet("test", false_spark)
    false_spark.parquet.assert_called_once_with("test")


def test_write_json(all_types_df, tmpdir):
    p = tmpdir.mkdir("json_yo")
    ingest.write_json(all_types_df, p.strpath)
    assert p.listdir()


def test_write_to_elastic(mocker, false_dataframe):
    mocker.patch("optel.datalake.ingest.sanity_checks.convert_decimal_to_float")
    mocker.patch("optel.datalake.ingest.sanity_checks.convert_date_to_string")

    ingest.sanity_checks.convert_decimal_to_float.return_value = false_dataframe
    ingest.sanity_checks.convert_date_to_string.return_value = false_dataframe

    ingest.write_to_elastic(false_dataframe, "", "", "", "")

    ingest.sanity_checks.convert_decimal_to_float.assert_called_once_with(false_dataframe)
    ingest.sanity_checks.convert_date_to_string.assert_called_once_with(false_dataframe)

    calls = []
    call = mocker.call
    calls.append(call.format("org.elasticsearch.spark.sql"))
    calls.append(call.mode("overwrite"))
    calls.append(call.option("es.nodes", ""))
    calls.append(call.save())

    false_dataframe.assert_has_calls(calls,  any_order=True)


def test_write_csv(mocker, false_dataframe):
    ingest.write_csv(false_dataframe, "HELLO WORLD")
    calls = []
    call = mocker.call
    calls.append(call.mode('overwrite'))
    calls.append(call.option('header', 'true'))
    calls.append(call.option('inferSchema', 'true'))
    calls.append(call.csv("HELLO WORLD"))
    false_dataframe.assert_has_calls(calls,  any_order=True)


def test_write_parquet(false_dataframe):
    ingest.write_parquet(false_dataframe, "HELLO WORLD")
    print(false_dataframe.__dict__)
    false_dataframe.mode.assert_called_once_with("overwrite")
    false_dataframe.parquet.assert_called_once_with("HELLO WORLD")


def test_get_df_from_source(mocker, base_source, tables):
    mocker.patch("optel.datalake.ingest.read_parquet")
    dfs = ingest.get_df_from_source(base_source, tables)

    calls = [mocker.call(base_source + table) for table in tables]
    ingest.read_parquet.assert_has_calls(
        calls, any_order=True)

    for table in tables:
        assert dfs[table]


def test_canonical_name():
    assert ingest.canonical_name("ThisNameIsOkay") == "ThisNameIsOkay"
    assert ingest.canonical_name("H[@]ello") == "Hello"
    assert ingest.canonical_name("!!Hello!!") == "!!Hello!!"


def test_read_avro(mocker):
    dataframe_mock = mocker.MagicMock()

    reader_mock = mocker.MagicMock()
    reader_mock.format.return_value = reader_mock
    reader_mock.load.return_value = dataframe_mock

    spark_session_mock = mocker.MagicMock()
    spark_session_mock.read = reader_mock

    df = ingest.read_avro("test", spark_session_mock)

    assert df == dataframe_mock


def test_write_avro(mocker):
    writer_mock = mocker.MagicMock()
    writer_mock.format.return_value = writer_mock
    writer_mock.mode.return_value = writer_mock

    df = mocker.MagicMock()
    df.write = writer_mock

    destination_uri = "test/test/test"
    ingest.write_avro(df, destination_uri)

    writer_mock.format.assert_called_once_with("avro")
    writer_mock.mode.assert_called_once_with("overwrite")
    writer_mock.save.assert_called_once_with(destination_uri)
