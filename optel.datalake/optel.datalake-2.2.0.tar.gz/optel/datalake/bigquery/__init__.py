import os
import re
from concurrent.futures import TimeoutError

from google.cloud import bigquery, exceptions, storage
from google.cloud.bigquery import job

from optel.datalake.ingest import write_parquet
from optel.datalake.sanity_checks import sanitize_datatypes_for_bigquery


def write_to_bigquery(
    df, table_name, *, dataset, bucket, temp_zone="pyspark/tmp"
):
    """
    Write a pyspark DataFrame to Google BigQuery. It uses a temporary folder
    in a Google Cloud Storage Bucket to do the operation. It then deletes
    everything it just wrote.

    .. Note: Needs to be run from a Google Compute Engine with access
             to Google Cloud Storage and Google BigQuery.

    Args:
        df (pyspark.sql.DataFrame): DataFrame to write to BigQuery.
        table_name (str): Name to use in BigQuery.
        bucket (str): Google Cloud Storage Bucket to use for the temp folder.
        dataset (str): Name of the dataset in BigQuery.
        temp_zone (str): Name of the temp folder we'll use as staging.
    """
    bq_client = bigquery.Client()
    bq_dataset = bq_client.dataset(dataset)

    job_config = create_bq_load_job_config("PARQUET", "WRITE_TRUNCATE")

    _transfer_to_google_bigquery(
        df, bucket, temp_zone, table_name, bq_dataset, job_config, bq_client
    )


def append_to_bigquery(
    df, table_name, *, dataset, bucket, temp_zone="pyspark/tmp"
):
    """
    Append pyspark DataFrame to a Google BigQuery table. The schema must
    be the same or have new nullable fields.
    It uses a temporary folder in a Google Cloud Storage Bucket to do the
    operation. It then deletes everything it just wrote.

    .. Note: Needs to be run from a Google Compute Engine with access
             to Google Cloud Storage and Google BigQuery.

    Args:
        df (pyspark.sql.DataFrame): DataFrame to write to BigQuery.
        table_name (str): Name to use in BigQuery.
        bucket (str): Google Cloud Storage Bucket to use for the temp folder.
        dataset (str): Name of the dataset in BigQuery.
        temp_zone (str): Name of the temp folder we'll use as staging.
    """
    bq_client = bigquery.Client()
    bq_dataset = bq_client.dataset(dataset)

    job_config = create_bq_load_job_config("PARQUET", "WRITE_APPEND")
    job_config.schema_update_options = [
        job.SchemaUpdateOption.ALLOW_FIELD_ADDITION
    ]

    _transfer_to_google_bigquery(
        df, bucket, temp_zone, table_name, bq_dataset, job_config, bq_client
    )


def _transfer_to_google_bigquery(
        df, bucket, temp_zone, table_name, bq_dataset, job_config, bq_client
):
    table_name = sanitize_name_for_bigquery(table_name)
    parquet_destination = os.path.join("gs://", bucket, temp_zone, table_name)

    df = sanitize_datatypes_for_bigquery(df)
    write_parquet(df, parquet_destination)

    try:
        load_job = bq_client.load_table_from_uri(
            os.path.join(parquet_destination, "part-*"),
            bq_dataset.table(table_name),
            job_config=job_config,
        )
        load_job.result()
    except exceptions.GoogleCloudError as e:
        raise e
    except TimeoutError as te:
        raise te
    finally:
        cleanup(bucket, temp_zone, table_name)


def sanitize_name_for_bigquery(table_name):
    """
    Remove illegal characters from a table name.

    >>> sanitize_name_for_bigquery('my_table')
    'my_table'
    >>> sanitize_name_for_bigquery('test-datalake')
    'testdatalake'
    >>> sanitize_name_for_bigquery('t1e5s&t-.+_data($)lake')
    't1e5st_datalake'

    Args:
        table_name (str): Table name in sanitize.

    Returns:
        str: sanitized table name ready to used as a name in BigQuery.

    """
    return re.sub(r'\W+', '', table_name)


def create_bq_load_job_config(source_format, write_disposition):
    config = bigquery.LoadJobConfig()
    config.source_format = source_format
    config.write_disposition = write_disposition
    return config


def cleanup(bucket, temp_zone, table_name):
    storage_bucket = get_storage_bucket(bucket)
    temp_blobs = storage_bucket.list_blobs(
        prefix=os.path.join(temp_zone, table_name)
    )
    for blob in temp_blobs:
        blob.delete()


def get_storage_bucket(bucket):
    storage_client = storage.Client()
    return storage_client.bucket(bucket)
