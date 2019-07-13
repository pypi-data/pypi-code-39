
import unittest
from unittest.mock import patch, MagicMock


class TestHtmlParsingBase(unittest.TestCase):

    def setUp(self):
        self.html_parser_type = None

    def get_mocked_html_parser(self, html_string=None):
        t = self.html_parser_type(html_string=html_string)
        t.document_tree = MagicMock()
        return t
