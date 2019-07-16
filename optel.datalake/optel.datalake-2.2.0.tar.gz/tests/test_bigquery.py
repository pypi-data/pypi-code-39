import optel.datalake.bigquery as odbq


def test_create_bq_load_job_config(mocker):
    mocker.patch("optel.datalake.bigquery.bigquery.LoadJobConfig")
    config = odbq.create_bq_load_job_config("Hello", "World")
    assert config.source_format == "Hello"
    assert config.write_disposition == "World"


def test_cleanup(mocker):
    config = {
        'list_blobs.return_value': [mocker.MagicMock() for i in range(3)]
    }
    mocker.patch("optel.datalake.bigquery.get_storage_bucket", **config)
    odbq.get_storage_bucket.return_value = odbq.get_storage_bucket  # hack
    odbq.cleanup("", "", "")

    # verify each MagicMock delete mock was called once
    for mock in config['list_blobs.return_value']:
        assert mock.delete.call_count == 1


def test_get_storage_bucket(mocker):
    client_mock = mocker.patch("optel.datalake.bigquery.storage.Client")
    odbq.get_storage_bucket("")
    client_mock.assert_called_once()
