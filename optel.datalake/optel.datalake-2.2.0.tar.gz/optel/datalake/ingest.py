from typing import Callable, Any
from deprecation import deprecated
from google.cloud import bigquery

from optel.datalake.config.sparksession import default_spark
from optel.datalake import sanity_checks


from pyspark.sql import DataFrame, SparkSession


class DatalakeSourceFormat(object):

    PARQUET = "PARQUET"

    AVRO = "AVRO"

    CSV = "CSV"

    SQL = "SQL"

    ELASTIC = "ELASTIC"

    MULTILINE_JSON = "MULTILINE_JSON"

    JSON_LINES = "JSON_LINES"

    BIGQUERY = "BIGQUERY"


def get_read_function(
        source_format: str
) -> Callable[[Any], DataFrame]:
    """Not all functions are polymorphic, some require more parameters."""
    func_map = {
        DatalakeSourceFormat.PARQUET: read_parquet,
        DatalakeSourceFormat.AVRO: read_avro,
        DatalakeSourceFormat.BIGQUERY: read_bigquery,
        DatalakeSourceFormat.CSV: read_csv,
    }

    return func_map[source_format]


def get_write_function(
    source_format: bigquery.SourceFormat
) -> Callable[[DataFrame, str], None]:
    writer_map = {
        bigquery.SourceFormat.PARQUET: write_parquet,
        bigquery.SourceFormat.CSV: write_csv,
        bigquery.SourceFormat.AVRO: write_avro,
    }
    return writer_map[source_format]


def load_sql_tables(database, tables, server, username, password, spark=None):
    """
    Load one table or a table schema from SQL server.

    Args:
        database (str): Database from which to fetch tables.
        tables (list): A list of tables to fetch.
        server (str): The server from which to fetch data.
        username (str): The username used to connect to the server.
        password (str): The password of the aforementioned username.
        spark (pyspark.sql.SparkSession): Optional Spark session to use.  This
            will default to the session provided by
            :func:`optel.datalake.config.sparksession.default_spark`

    Returns:
        dict: Data frames keyed by table name
    """
    spark = spark or default_spark()
    dic_of_df = dict()
    for table in tables:
        print("Fetching from SQL:", database, "\n", table)
        spark_df = spark.read \
            .format("jdbc") \
            .option("url", server) \
            .option("databaseName", database) \
            .option("dbtable", table) \
            .option("user", username) \
            .option("password", password) \
            .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
            .option("header", "true") \
            .option("nullValue", "0") \
            .option("encrypt", "false") \
            .load()
        dic_of_df[table] = spark_df

    return dic_of_df


def write_to_elastic(table, destination, nodes, username, password):
    """
    Write table to Elastic search.

    Args:
        table (pyspark.sql.DataFrame): The name of the Spark DataFrame that
            will be written to Elastic.
        destination (str): The name of the index under which the DataFrame
            will be written.
        nodes (str): Elastic search nodes where to write table.
        username (str): Elasticsearch user with write access.
        password (str): Elasticsearch user password.
    """
    table = sanity_checks.convert_decimal_to_float(table)
    table = sanity_checks.convert_date_to_string(table)
    resource_name = '{}/table'.format(destination)
    table.write \
        .format("org.elasticsearch.spark.sql") \
        .mode("overwrite") \
        .option("es.mapping.date.rich", "true") \
        .option("es.index.auto.create", "true") \
        .option("es.resource", resource_name) \
        .option("es.nodes", nodes) \
        .option("es.net.ssl.protocol", "true") \
        .option("es.nodes.wan.only", "true") \
        .option("es.net.http.auth.user", username) \
        .option("es.field.read.empty.as.null", "yes") \
        .option("es.net.http.auth.pass", password) \
        .save()
    # todo: replace all option calls with a single options call


def read_from_elastic(index, nodes, username, password, spark=None):
    """
    Read a table from Elasic Search.

    Args:
        index (str): The name of the elastic search index to read.
        spark (pyspark.sql.SparkSession): Optional Spark session to use.  This
            will default to the session provided by
            :func:`optel.datalake.config.sparksession.default_spark`
    """
    spark = spark or default_spark()
    loaded_es_index = spark.read \
        .format("org.elasticsearch.spark.sql") \
        .option("es.nodes", nodes) \
        .option("es.net.ssl.protocol", "true") \
        .option("es.nodes.wan.only", "true") \
        .option("es.net.http.auth.user", username) \
        .option("es.net.http.auth.pass", password) \
        .load(index + "/table")
    return loaded_es_index


def write_csv(df, destination):
    """
    Write a csv table to a destination.

    Args:
        df (pyspark.sql.DataFrame): TODO
        destination (str): CSV file path.
    """
    df.write \
        .format("csv") \
        .mode("overwrite") \
        .option("header", "true") \
        .option("inferSchema", "true")\
        .csv(destination)


def write_parquet(df, destination):
    """
    Write a Spark DataFrame to a Parquet file.

    .. notes: Cannot write a DataFrame with a column of Null

    Args:
        df (pyspark.sql.DataFrame): The name of the Spark DataFrame.
        destination (str): The destination file path where to write the
            DataFrame *parquet* file.
    """
    df.write.mode("overwrite").parquet(destination)


def read_csv(source, spark=None):
    spark = spark or default_spark()
    df = spark.read \
        .format("csv") \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .load(source)
    return df


def read_json(file_path, spark=None, multiline="false"):
    """Creates a Spark DataFrame from a JSON document.

    Args:
        file_path (str): Path of the JSON file to load.
        spark: (Optional) specify a Spark session.
        multiline (str): (Optional). Specify if the JSON file is
            standard/multiline ("true") or a JSON Lines document ("false").

    Returns:
        pyspark.sql.DataFrame: A DataFrame.

    """
    spark = spark or default_spark()
    df = spark.read.option("multiline", multiline).json(file_path)
    return df


def write_json(df, file_path):
    """

    Args:
        df (pyspark.sql.DataFrame):
        file_path (str):

    """
    df.write.mode("overwrite").json(file_path)


def read_parquet(source, spark=None):
    """
    Read parquet files into a Spark DataFrame.

    Args:
        source (str): Source *parquet* file.
        spark (pyspark.sql.SparkSession): Optional Spark session to use.  This
            will default to the session provided by
            :func:`optel.datalake.config.sparksession.default_spark`

    Returns:
        pyspark.sql.DataFrame: Properly initialized data frame.
    """
    spark = spark or default_spark()
    result_df = spark.read.parquet(source)
    return result_df


@deprecated(deprecated_in="2.2.0", removed_in="3.0.0", details="use bigquery")
def get_df_from_source(base_source, tables):
    """
    Make data frames from a folder of *parquet* files.

    Args:
        base_source (str): Path to the folder containing *parquet* files.
        tables: List of parquet file names.

    Returns:
        dict: Mapping of :class:`pyspark.sql.DataFrame` objects indexed by
            file name.
    """
    dic_of_df = {}
    for table in tables:
        source = (base_source + table)
        dic_of_df[table] = read_parquet(source)
    return dic_of_df


def canonical_name(table_name):
    """Takes a table_name and remove characters not accepted in GCS.

    Args:
        table_name (str): Name

    Returns:
        Name without illegal GCS bucket name characters.

    """
    for char in ["[", "]", "@"]:
        table_name = table_name.replace(char, "")

    return table_name


def read_bigquery(table: str, sparksession: SparkSession = None) -> DataFrame:
    """
    Takes the `dataset.table` and return a DataFrame read from BigQuery.

    .. note::
        Needs the spark-bigquery-connector developed by Google to work.

    """
    spark = sparksession or default_spark()
    return spark.read.format("bigquery").option("table", table).load()


def read_avro(table_uri: str, spark_session: SparkSession = None) -> DataFrame:
    spark = spark_session or default_spark()
    return spark.read.format("avro").load(table_uri)


def write_avro(dataframe: DataFrame, destination_uri: str) -> None:
    dataframe.write.format("avro").mode("overwrite").save(destination_uri)
