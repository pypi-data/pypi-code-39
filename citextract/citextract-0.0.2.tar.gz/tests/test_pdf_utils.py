from unittest import TestCase, mock
from citextract.utils.pdf import convert_pdf_url_to_text
from tests.utils import mocked_pdf_requests_get


class TestPDFUtils(TestCase):

    @mock.patch('requests.get', side_effect=mocked_pdf_requests_get)
    def test_convert_pdf_url_to_text(self, mock_get):
        result = convert_pdf_url_to_text('test_hello_world.pdf')
        self.assertTrue('Hello world!' in result)
