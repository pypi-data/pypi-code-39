from abc import ABC, abstractmethod
from os.path import join

from pyspark.sql import DataFrame

from optel.datalake.ingest import canonical_name, get_read_function
from optel.datalake.models.schemas import BaseSchema


class SourceTable(ABC):  # pragma: no cover
    @abstractmethod
    def read(self) -> DataFrame:
        ...


class DatalakeTable(SourceTable):
    def __init__(
        self,
        zone: str,
        name: str,
        schema: BaseSchema,
        source_format: str,
        base_source_uri: str,
    ):
        """Represents the information to access a table in the datalake.
        """
        self.schema = schema
        self.zone = zone
        self.name = canonical_name(name)
        self.source_format = source_format.upper()
        self.base_source_uri = base_source_uri

    @property
    def source_uri(self) -> str:
        return join(self.base_source_uri, self.zone, self.name)

    def read(self) -> DataFrame:
        raw_df = get_read_function(self.source_format)(self.source_uri)
        return self.schema.apply(raw_df)


class BigQueryTable(SourceTable):
    def __init__(
        self,
        dataset: str,
        name: str,
        schema: BaseSchema,
    ):
        """Represents the information to access a table in BigQuery."""
        self.name = name
        self.schema = schema
        self.dataset = dataset

    @property
    def full_table_name(self) -> str:
        return "{}.{}".format(self.dataset, self.name)

    def read(self) -> DataFrame:
        raw_df = get_read_function("BIGQUERY")(self.full_table_name)
        return self.schema.apply(raw_df)
