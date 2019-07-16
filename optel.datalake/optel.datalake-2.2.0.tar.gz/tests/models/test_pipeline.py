import pytest
from optel.datalake.models import pipeline


class TestPipeline:

    @pytest.fixture()
    def test_pipeline(self, mocker):
        read = mocker.MagicMock()
        transform = mocker.MagicMock()
        write = mocker.MagicMock()
        return pipeline.Pipeline(read, transform, write)

    def test_execute(self, test_pipeline):
        test_pipeline.execute()

        test_pipeline.read.assert_called_once()
        test_pipeline.transform.assert_called_once_with(
            test_pipeline.read.return_value
        )
        test_pipeline.write.assert_called_once_with(
            test_pipeline.transform.return_value
        )
