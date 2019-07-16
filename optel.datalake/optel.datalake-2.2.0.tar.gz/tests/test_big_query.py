import optel.datalake.big_query as old_odbq


def test_write_to_bigquery(mocker):
    mocked = mocker.patch("optel.datalake.bigquery.write_to_bigquery")
    old_odbq.write_to_bigquery("", "", dataset="", bucket="")
    mocked.assert_called_once()


def test_append_to_bigquery(mocker):
    mocked = mocker.patch("optel.datalake.bigquery.append_to_bigquery")
    old_odbq.append_to_bigquery("", "", dataset="", bucket="")
    mocked.assert_called_once()
