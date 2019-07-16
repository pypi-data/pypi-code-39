"""
Standalone Python package meant to be sent to Google Cloud to test the package
in cluster condition of dataproc (i.e. not tested by pytest).
"""


def all_types_df_for_live_test():
    """
    Make a diverse schema for live tests.

    Returns:
        pyspark.sql.DataFrame: DataFrame with many different type of data.

    """
    import decimal
    import datetime
    from pyspark.sql.types import StringType
    from pyspark.sql.types import StructField
    from pyspark.sql.types import StructType
    from pyspark.sql.types import DecimalType
    from pyspark.sql.types import TimestampType
    from pyspark.sql.types import DateType
    from pyspark.sql.types import LongType
    from pyspark.sql.types import DoubleType
    from optel.datalake.config.sparksession import default_spark

    spark_session = default_spark()
    values = [
        (
            datetime.datetime.now(),
            datetime.date.today(),
            "HELLO WORLD THIS IS A STRING",
            decimal.Decimal(10.15984567),
            decimal.Decimal(11.15984567),
            1056659845,
            10.5555555555,
        ),
        (
            datetime.datetime.now(),
            datetime.date.today(),
            "HELLO WORLD THIS IS A STRING",
            decimal.Decimal(10.15984567),
            decimal.Decimal(11.15984567),
            1056659845,
            0.05654,
        )
    ]
    schema = StructType(
        [
            StructField("datetime", TimestampType()),
            StructField("date", DateType()),
            StructField("string", StringType()),
            StructField("decimal_scale", DecimalType(28, 16)),
            StructField("decimal_digits", DecimalType(38, 6)),
            StructField("long", LongType()),
            StructField("double", DoubleType()),
        ]
    )
    return spark_session.createDataFrame(values, schema)


def bigquery_client():
    """Gives the BigQuery client"""
    from google.cloud import bigquery
    return bigquery.Client()


def bigquery_parameters(live_test_name):
    """Gives the parameters to use for live BigQuery tests."""
    dataset_id = "test2"
    bucket_id = "optel-datalake"
    table_id = live_test_name
    return {"name": table_id, "dataset": dataset_id, "bucket": bucket_id}


def live_bq_write_test(all_types_df, bigquery, bq_client):
    """Try to write to BigQuery for real."""
    import optel.datalake.bigquery as odbq

    odbq.write_to_bigquery(
        all_types_df,
        bigquery["name"],
        dataset=bigquery["dataset"],
        bucket=bigquery["bucket"],
    )
    dataset_ref = bq_client.dataset(bigquery["dataset"])
    table_ref = dataset_ref.table(bigquery["name"])
    bq_table = bq_client.get_table(table_ref)

    assert bq_table.num_rows == all_types_df.count()
    assert len(bq_table.schema) == len(all_types_df.columns)


def live_bq_append_test(all_types_df, bigquery, bq_client):
    """
    Try to append to BigQuery for real.
    Also try to append with a new field.
    """
    import optel.datalake.bigquery as odbq
    from pyspark.sql.functions import lit
    from pyspark.sql.functions import when

    odbq.append_to_bigquery(
        all_types_df,
        bigquery["name"],
        dataset=bigquery["dataset"],
        bucket=bigquery["bucket"],
    )
    dataset_ref = bq_client.dataset(bigquery["dataset"])
    table_ref = dataset_ref.table(bigquery["name"])
    bq_table = bq_client.get_table(table_ref)

    assert bq_table.num_rows == all_types_df.count() * 2
    assert len(bq_table.schema) == len(all_types_df.columns)

    new_df = all_types_df.withColumn(
        "another_col",
        when(all_types_df["double"] > 1, lit("")).otherwise(lit(None))
    )
    new_df.printSchema()

    odbq.append_to_bigquery(
        new_df,
        bigquery["name"],
        dataset=bigquery["dataset"],
        bucket=bigquery["bucket"],
    )

    dataset_ref = bq_client.dataset(bigquery["dataset"])
    table_ref = dataset_ref.table(bigquery["name"])
    bq_table = bq_client.get_table(table_ref)

    assert bq_table.num_rows == all_types_df.count() * 3
    assert len(bq_table.schema) == len(all_types_df.columns) + 1


def live_bq_read_test(bigquery):
    from optel.datalake.ingest import read_bigquery
    df = read_bigquery("{}.{}".format(bigquery["dataset"], bigquery["name"]))
    assert df.count() > 0


if __name__ == "__main__":
    import glob
    from subprocess import call

    distribution = glob.glob("*.tar.gz")
    virtualenv_path = "/opt/.virtualenvs/jobs-submission/bin/python"
    call(
        [
            virtualenv_path,
            "-m",
            "pip",
            "install",
            "--upgrade",
            "--force-reinstall",
            distribution[0],
        ]
    )
    test_df = all_types_df_for_live_test()
    client = bigquery_client()
    bq_info = bigquery_parameters("test_datalake")
    live_bq_write_test(test_df, bq_info, client)
    live_bq_append_test(test_df, bq_info, client)
