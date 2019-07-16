from deprecation import deprecated
import optel.datalake.bigquery as optelbq


@deprecated(deprecated_in="2.1.0", removed_in="3.0.0", details="use bigquery")
def write_to_bigquery(
        df, table_name, *, dataset, bucket, temp_zone="pyspark/tmp"
):
    optelbq.write_to_bigquery(
        df, table_name, dataset=dataset, bucket=bucket, temp_zone=temp_zone
    )


@deprecated(deprecated_in="2.1.0", removed_in="3.0.0", details="use bigquery")
def append_to_bigquery(
        df, table_name, *, dataset, bucket, temp_zone="pyspark/tmp"
):
    optelbq.append_to_bigquery(
        df, table_name, dataset=dataset, bucket=bucket, temp_zone=temp_zone
    )


write_to_bigquery.__doc__ = optelbq.write_to_bigquery.__doc__
append_to_bigquery.__doc__ = optelbq.append_to_bigquery.__doc__
