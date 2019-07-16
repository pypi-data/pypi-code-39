import pytest


from optel.datalake.models import job


class ConfigurationTest(job.JobConfiguration):

    def __init__(self):
        self.name = "Hello"


class TestJob:

    @pytest.fixture()
    def test_configuration(self):
        return ConfigurationTest()

    @pytest.fixture()
    def test_job(self, test_configuration):
        return job.Job(test_configuration)

    def test_execute_all(self, test_job, mocker):
        get_pipeline = mocker.MagicMock()
        mocker.patch(
            "optel.datalake.models.job.iter_entry_points",
            autospec=True,
            return_value=[get_pipeline],
        )

        test_job.execute_from_entrypoints_group("test_entrypoint")

        get_pipeline().assert_called_once_with(test_job.configuration)
        get_pipeline().return_value.execute.assert_called_once()
