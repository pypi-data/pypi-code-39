
import unittest
from unittest.mock import patch, MagicMock
from thisamericanlife.utils.tests import TestHtmlParsingBase
from thisamericanlife.html.episode import EpisodeHtml


class TestHtmlEpisodeParsing(TestHtmlParsingBase):
    def setUp(self):
        self.html_parser_type = EpisodeHtml

    @patch('thisamericanlife.html.episode.EpisodeHtml.extract_acts')
    @patch('thisamericanlife.html.episode.EpisodeHtml.extract_episode_metadata')
    def test_to_json(self, mock_extract_episode_metadata, mock_extract_acts, *args):
        res = self.get_mocked_html_parser().to_json()
        mock_extract_episode_metadata.assert_called_once()
        mock_extract_acts.assert_called_once()

        expected_result = dict(episode_metadata=mock_extract_episode_metadata(), act_summaries=mock_extract_acts())
        self.assertDictEqual(res, expected_result)


if __name__ == '__main__':
    unittest.main()
