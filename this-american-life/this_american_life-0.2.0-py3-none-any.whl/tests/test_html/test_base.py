
import unittest
from unittest.mock import patch
from thisamericanlife.html.base import BaseHtmlParser
from thisamericanlife.utils.tests import TestHtmlParsingBase


patch_lxml_html = patch('thisamericanlife.html.base.lxml_html')


class TestBaseHtmlParserParsing(TestHtmlParsingBase):
    def setUp(self):
        self.html_parser_type = BaseHtmlParser

    @patch_lxml_html
    def test_initialized_with_parsed_html_when_html_provided(self, mock_lxml_html):
        self.get_mocked_html_parser('something')
        mock_lxml_html.fromstring.assert_called_once_with('something')

    @patch_lxml_html
    def test_initialized_without_document_tree_when_no_html_provided(self, mock_lxml_html):
        self.get_mocked_html_parser()
        mock_lxml_html.fromstring.assert_not_called()


if __name__ == '__main__':
    unittest.main()
