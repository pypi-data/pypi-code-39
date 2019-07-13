
import unittest
from unittest.mock import patch, MagicMock
from thisamericanlife.models.episode import Episodes, EpisodeInstance


class TestEpisodeModels(unittest.TestCase):

    @patch('thisamericanlife.models.episode.Episodes._get_and_create')
    def test_episodes_get(self, mock_get_create):
        kwargs = dict(episode_number=1, episode_title='new-beginnings')
        res = Episodes().get(**kwargs)

        mock_get_create.assert_called_once_with(EpisodeInstance, **kwargs)
        self.assertEqual(res, mock_get_create())

    @patch('thisamericanlife.models.episode.Episodes._get_and_create')
    def test_episodes_get_with_name_looked_up(self, mock_get_create):
        episodes = Episodes()
        episodes.client = MagicMock()

        episode_number = 1
        res = episodes.get(episode_number=episode_number)

        episode_title = episodes.client.transcripts.get(episode_number).episode_metadata.title

        mock_get_create.assert_called_once_with(
            EpisodeInstance,
            episode_number=episode_number,
            episode_title=episode_title
        )

        self.assertEqual(res, mock_get_create())

    @patch('thisamericanlife.models.episode.EpisodeInstance')
    @patch('thisamericanlife.models.episode.EpisodeHtml')
    def test_episode_instance_from_html(self, mock_html, mock_instance):
        res = EpisodeInstance.from_html('some-html')
        mock_html.assert_called_once_with('some-html')
        mock_html().to_json.assert_called_once()
        mock_instance.assert_called_once_with(body_json=mock_html().to_json())
        self.assertEqual(mock_instance(), res)


if __name__ == '__main__':
    unittest.main()
