import pytest

from optel.datalake.bigquery.client import DataRefineryBigQueryClient

from google.cloud import bigquery


class TestDataRefineryBigQueryClient:
    CLIENT = "optel.datalake.bigquery.client.DataRefineryBigQueryClient"

    @pytest.fixture()
    def client(self):
        return DataRefineryBigQueryClient("test-bucket", project="test")

    def test_load_table_from_dataproc_w_default_job_config(
            self, mocker, client
    ):
        mock_write = mocker.patch(
            self.CLIENT + ".write_to_bucket",
            return_value="test",
            autospec=True
        )
        mock_load = mocker.patch(
            self.CLIENT + ".load_from_gcs_files",
            autospec=True,
        )
        mock_dataframe = mocker.MagicMock()
        mock_job_config = mocker.MagicMock()

        client.default_job_config = mock_job_config
        client.load_table_from_dataproc(
            mock_dataframe, "test.test"
        )

        mock_write.assert_called_once_with(
            client, mock_dataframe, "test.test", mock_job_config
        )
        mock_load.assert_called_once_with(
            client, mock_write.return_value, "test.test", mock_job_config
        )

    def test_load_table_from_dataproc_w_jobconfig(self, mocker, client):
        mock_write = mocker.patch(
            self.CLIENT + ".write_to_bucket",
            return_value="test/test/test.test",
            autospec=True,
        )
        mock_load = mocker.patch(
            self.CLIENT + ".load_from_gcs_files",
            autospec=True,
        )
        mock_dataframe = mocker.MagicMock()
        mock_job_config = mocker.MagicMock()

        # act
        client.load_table_from_dataproc(
            mock_dataframe, "test.test", job_config=mock_job_config
        )

        # verify
        mock_write.assert_called_once_with(
            client, mock_dataframe, "test.test", mock_job_config
        )
        mock_load.assert_called_once_with(
            client, mock_write.return_value, "test.test", job_config=mock_job_config
        )

    def test_write_to_bucket_in_parquet(self, mocker, client):
        mock_write_parquet = mocker.patch(
            "optel.datalake.ingest.write_parquet",
            autospec=True
        )

        mock_dataframe = mocker.MagicMock()

        load_config = bigquery.LoadJobConfig()
        load_config.source_format = bigquery.SourceFormat.PARQUET

        client.write_to_bucket(
            mock_dataframe, "test.test", load_config
        )

        mock_write_parquet.assert_called_once()

    def test_write_to_bucket_in_csv(self, mocker, client):
        mocker_write_csv = mocker.patch(
            "optel.datalake.ingest.write_csv",
            autospec=True,
        )
        mock_dataframe = mocker.MagicMock()

        load_config = bigquery.LoadJobConfig()
        load_config.source_format = bigquery.SourceFormat.CSV

        client.write_to_bucket(
            mock_dataframe, "test.test", load_config
        )

        mocker_write_csv.assert_called_once()

    def test_write_to_bucket_in_avro(self, mocker, client):
        mock_write_avro = mocker.patch(
            "optel.datalake.ingest.write_avro",
            autospec=True,
        )
        mock_dataframe = mocker.MagicMock()

        load_config = bigquery.LoadJobConfig()
        load_config.source_format = bigquery.SourceFormat.AVRO

        client.write_to_bucket(
            mock_dataframe, "test.test", load_config
        )
        mock_write_avro.assert_called_once()

    def test_write_to_bucket_source_uri(self, mocker, client):
        expected_source_uri = "gs://test-bucket/test.test"

        mock_write = mocker.MagicMock()
        mocker.patch(
            "optel.datalake.bigquery.client.get_write_function",
            autospec=True,
            return_value=mock_write,
        )
        sanitize_mock = mocker.patch(
            "optel.datalake.bigquery.client.sanitize_datatypes_for_bigquery",
            autospec=True,
        )
        mock_df = mocker.MagicMock()
        load_config_mock = mocker.MagicMock()

        source_uri = client.write_to_bucket(
            mock_df, "test.test", load_config_mock
        )

        assert source_uri == expected_source_uri
        sanitize_mock.assert_called_once_with(mock_df)
        mock_write.assert_called_once_with(
            sanitize_mock.return_value, expected_source_uri
        )

    def test_load_from_gcs_files(self, mocker, client):
        load_mock = mocker.patch(
            self.CLIENT + ".load_table_from_uri",
            autospec=True
        )
        table_ref_mock = mocker.patch(
            "optel.datalake.bigquery.client.bigquery.TableReference.from_string",
            autospec=True,
        )
        job_config_mock = mocker.MagicMock()

        client.load_from_gcs_files(
            "test://test.test/", "test.test", job_config_mock
        )

        load_mock.assert_called_once_with(
            client,
            "test://test.test/part-*",
            table_ref_mock.return_value,
            job_config_mock,
        )
