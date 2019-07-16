import json
import pytest
import decimal
import datetime
from optel.datalake.config.sparksession import test_session
from pyspark.sql.functions import lit
from pyspark.sql.functions import StringType
from pyspark.sql.functions import desc
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType
from pyspark.sql.types import DecimalType
from pyspark.sql.types import TimestampType
from pyspark.sql.types import DateType
from pyspark.sql.types import LongType
from pyspark.sql.types import DoubleType


@pytest.fixture(scope='session')
def spark_session():
    session = test_session("optel-datalake")
    yield session


@pytest.fixture()
def false_dataframe(mocker):
    mock_dataframe = mocker.MagicMock()
    mock_dataframe.write = mock_dataframe
    mock_dataframe.format.return_value = mock_dataframe
    mock_dataframe.option.return_value = mock_dataframe
    mock_dataframe.mode.return_value = mock_dataframe
    yield mock_dataframe


@pytest.fixture()
def false_spark(mocker):
    mock_session = mocker.MagicMock()
    mock_session.read = mock_session
    mock_session.format.return_value = mock_session
    mock_session.option.return_value = mock_session
    yield mock_session


@pytest.fixture(scope="session")
def me_df_timestamp(spark_session):
    """Data frame with a unix timestamp. An emtpy column is present
    """

    columns = [
        'date', 'string', 'number',
        'CREATEDTIME', 'COMPLETEDTIME', 'STATUSNAME', 'date2']
    vals = [
        (1503374640123, "one", 2,
         '2017-12-01 23:59:59', '2017-12-10 21:59:59', 'Open', 1503374640123),
        (1512663325123, "two", 1,
         '2017-12-02 23:59:59', '2017-12-15 19:59:59', 'Open', 1503374640123),
        (1512160044123, "three", 4,
         '2017-12-03 23:59:59', '2017-12-20 02:59:51', 'Open', 1503374640123),
        (1517480177123, "four", 6,
         '2017-12-04 23:59:59', '2017-12-22 23:59:30', 'Closed', 1503374640123),
    ]
    df = spark_session.createDataFrame(vals, columns)
    df = df.withColumn("empty", lit(None).cast(StringType()))
    df = df.withColumn("empty2", lit(None).cast(StringType()))
    df = df.sort(desc("date"))
    return df


@pytest.fixture(scope="session")
def duplicates_df(spark_session):
    """Dataframe with a duplicated row and a duplicated field"""

    columns = ["one", "two", "three"]
    vals = [
        (1503374640123, "one", 2, 3),
        (1503374640123, "one", 2, 3),
        (1503374640123, "one", 2, 4),
        (1503374644123, "one", 2, 3),
        (1503374640123, "one", 2, 3),
    ]
    df = spark_session.createDataFrame(vals, columns)
    return df


@pytest.fixture(scope="session")
def gc_instances():
    instances_names = ["cluster-datalab-01-m", "cluster-datalab-01-w-0",
                       "cluster-datalab-02-m", "cluster-datalab-02-w-0",
                       "datalake-runner", "gitlab-runner"]
    return instances_names


@pytest.fixture(scope="session")
def instances_names():
    instances_names = ["cluster-datalab-04-m", "cluster-datalab-04-w-0",
                       "cluster-datalab-04-w-1"]
    return instances_names


@pytest.fixture(scope="session")
def decimal_df(spark_session):
    """Dataframe with two decimal type columns"""
    value = decimal.Decimal(1.0)
    values = [
        (value, value, value, value),
    ]
    schema = StructType([
        StructField("one", DecimalType()),
        StructField("two", DecimalType(35, 18)),
        StructField("3", DecimalType(30, 10)),
        StructField("four", DecimalType(38, 6)),
    ])

    return spark_session.createDataFrame(values, schema)


@pytest.fixture(scope="session")
def double_df(spark_session):
    values = [(1.0, 1.1)]
    schema = StructType([
        StructField("one", DoubleType()),
        StructField("two", DoubleType()),
    ])
    return spark_session.createDataFrame(values, schema)


@pytest.fixture(scope="session")
def timestamp_df(spark_session):
    """Dataframe with two timestamp type columns"""
    values = [(datetime.datetime(1111, 11, 11, 00, 00, 00, 000),
               datetime.datetime(1001, 10, 10, 11, 10, 11, 110))]
    schema = StructType([
        StructField("one", TimestampType()),
        StructField("two", TimestampType())
    ])
    return spark_session.createDataFrame(values, schema)


@pytest.fixture(scope="session")
def date_df(spark_session):
    """Dataframe with two date type columns"""
    values = [
        (
            datetime.datetime(2000, 1, 1, 11, 11, 11),
            datetime.datetime(2000, 1, 1, 11, 11, 11),
        ),
    ]
    schema = StructType([
        StructField("one", TimestampType()),
        StructField("two", TimestampType())
    ])
    return spark_session.createDataFrame(values, schema)


@pytest.fixture(scope="session")
def all_types_df(spark_session):
    """DataFrame with pretty much every single Spark type in there"""
    values = [
        (
            datetime.datetime.now(),
            datetime.date.today(),
            "HELLO WORLD THIS IS A STRING",
            decimal.Decimal(10.15984567),
            1056659845,
            10.5555555555,
        ),
    ]
    schema = StructType([
        StructField("datetime", TimestampType()),
        StructField("date", DateType()),
        StructField("string", StringType()),
        StructField("decimal", DecimalType(28, 16)),
        StructField("long", LongType()),
        StructField("double", DoubleType()),
    ])
    return spark_session.createDataFrame(values, schema)


@pytest.fixture()
def json_file(tmpdir):
    p = tmpdir.join("test_json.json")
    to_json = [{"ID": 1, "name": "Hello"}, {"ID": 2, "name": "Hello2"}]
    is_json = json.dumps(to_json)
    p.write(is_json)
    return p
