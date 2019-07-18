from bqmigratrr.enums.DataType import DataType
from bqmigratrr.enums.Mode import Mode
from bqmigratrr.models.Column import Column

from google.cloud import bigquery
import json
import os


class BigQuery(object):
    def __init__(self, project_id: str = None):
        self.migrationsDatasetName = "bqMigrations"
        self.migrationsTable = "migrations"

        if project_id is None:
            project_id = os.environ.get("gcp_project_id")

        self.client = bigquery.Client(project=project_id)
        self._createMigrationsDatasetIfNotExist()

    def createTable(self, dataset: str, tablename: str, columns: [Column]):
        if len(columns) == 0:
            raise Exception("Columns must be defined when using record")

        table_ref = self.client.dataset(dataset).table(tablename)
        bqSchema = self._generateSchema(columns)

        table = bigquery.Table(table_ref, schema=bqSchema)
        self.client.create_table(table)

    def addColumn(self, dataset: str, tablename: str, column: Column):
        self.addColumns(dataset, tablename, [column])

    def addColumns(self, dataset: str, tablename: str, columns: [Column]):
        table_ref = self.client.dataset(dataset).table(tablename)
        table = self.client.get_table(table_ref)

        original_schema = table.schema
        new_schema = original_schema[:]

        schema = self._generateSchema(columns)
        new_schema = new_schema + schema

        table.schema = new_schema
        self.client.update_table(table, ["schema"])

    def insertMigrationRow(self, migrationname: str):
        print("inserting migration row for {}".format(migrationname))
        table_ref = self.client.dataset(
            self.migrationsDatasetName).table(self.migrationsTable)
        table = self.client.get_table(table_ref)

        rows_to_insert = [
            {"id": migrationname}
        ]

        self.client.insert_rows(table, rows_to_insert)

    def _generateSchema(self, columns: [Column]) -> []:
        schema = []
        for column in columns:
            schema.append(bigquery.SchemaField(
                column.name, column.datatype.value, column.mode.value))

        return schema

    def _createMigrationsDatasetIfNotExist(self):
        self.client.create_dataset(self.migrationsDatasetName, exists_ok=True)
        table_ref = self.client.dataset(
            self.migrationsDatasetName).table(self.migrationsTable)
        bqSchema = self._generateSchema(
            [Column("id", DataType.string, Mode.required)])
        table = bigquery.Table(table_ref, schema=bqSchema)
        self.client.create_table(table, exists_ok=True)
