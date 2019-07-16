from google.cloud import bigquery

from optel.datalake.ingest import get_write_function
from optel.datalake.sanity_checks import sanitize_datatypes_for_bigquery

from os.path import join

from pyspark.sql import DataFrame


class DataRefineryBigQueryClient(bigquery.Client):
    def __init__(self, bucket, job_config=None, *args, **kwargs):
        super(DataRefineryBigQueryClient, self).__init__(*args, **kwargs)
        self._bucket = bucket
        self.default_job_config = job_config

    def _make_table_ref(self, destination_table_name):
        full_name = "{}.{}".format(self.project, destination_table_name)
        return bigquery.TableReference.from_string(full_name)

    def load_table_from_dataproc(
        self,
        dataframe: DataFrame,
        destination: str,
        job_config: bigquery.LoadJobConfig = None,
    ) -> None:
        job_config = job_config or self.default_job_config

        base_uri = self.write_to_bucket(dataframe, destination, job_config)
        self.load_from_gcs_files(base_uri, destination, job_config)

    def write_to_bucket(
        self,
        df: DataFrame,
        destination: str,
        job_config: bigquery.LoadJobConfig,
    ) -> str:
        destination_uri = join("gs://", self._bucket, destination)

        df = sanitize_datatypes_for_bigquery(df)

        write_func = get_write_function(job_config.source_format)
        write_func(df, destination_uri)

        return destination_uri

    def load_from_gcs_files(
        self,
        destination_uri: str,
        destination: str,
        job_config: bigquery.LoadJobConfig,
    ) -> None:
        load_job = self.load_table_from_uri(
            join(destination_uri, "part-*"),
            self._make_table_ref(destination),
            job_config,
        )
        load_job.result()
