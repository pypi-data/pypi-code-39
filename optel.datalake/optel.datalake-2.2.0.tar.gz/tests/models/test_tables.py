from optel.datalake.models import tables


class TestDatalakeTable:

    def test_read(self, mocker):
        mock_schema = mocker.MagicMock()
        mock_parquet_read = mocker.MagicMock()
        mocker.patch(
            "optel.datalake.models.tables.get_read_function",
            autospec=True,
            return_value=mock_parquet_read,
        )

        parquet_table = tables.DatalakeTable(
            zone="t",
            name="@n",
            schema=mock_schema,
            source_format="PARQUET",
            base_source_uri="gs://intake",
        )

        dataframe = parquet_table.read()

        assert dataframe == mock_schema.apply.return_value

        mock_schema.apply.assert_called_once()
        mock_parquet_read.assert_called_once_with(
            "gs://intake/t/n"
        )


class TestBigQueryTable:

    def test_read(self, mocker):
        mock_bigquery_read = mocker.MagicMock()
        mocker.patch(
            "optel.datalake.models.tables.get_read_function",
            autospec=True,
            return_value=mock_bigquery_read,
        )
        mock_schema = mocker.MagicMock()

        bigquery_table = tables.BigQueryTable(
            name="hahaha", schema=mock_schema, dataset="test2"
        )

        dataframe = bigquery_table.read()

        assert dataframe == mock_schema.apply.return_value
        mock_bigquery_read.assert_called_once_with("test2.hahaha")
