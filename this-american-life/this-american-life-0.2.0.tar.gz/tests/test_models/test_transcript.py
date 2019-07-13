
import unittest
from unittest.mock import patch, MagicMock
from thisamericanlife.models.transcript import Transcripts, TranscriptInstance, EpisodeMetadata


class TestTranscriptModels(unittest.TestCase):
    @patch('thisamericanlife.models.transcript.EpisodeMetadata')
    def test_init(self, mock_ep_meta):
        body_json = dict(transcript='tr', episode_title='et')
        ti = TranscriptInstance(body_json=body_json)

        self.assertDictEqual(ti.body_json, body_json)
        mock_ep_meta.from_raw.assert_called_once_with('et')
        ti.episode_meta_info = mock_ep_meta.from_raw()
        ti.transcript = 'tr'

    def run_episode_meta_from_raw(self, *args):
        em = EpisodeMetadata.from_raw(args[0])
        self.assertTupleEqual((em.raw_title, em.title, em.number), args)

    def test_episode_meta_from_raw_success(self):
        self.run_episode_meta_from_raw('1: title', 'title', 1)

    def test_episode_meta_from_fail(self):
        self.run_episode_meta_from_raw('a: title', 'title', None)

    def test_episode_meta_from_empty(self):
        self.run_episode_meta_from_raw('', None, None)

    @patch('thisamericanlife.models.transcript.Transcripts._get_and_create')
    def test_transcripts_get(self, mock_get_create):
        res = Transcripts().get(1)

        mock_get_create.assert_called_once_with(TranscriptInstance, episode_number=1)
        self.assertEqual(res, mock_get_create())

    @patch('thisamericanlife.models.transcript.TranscriptInstance')
    @patch('thisamericanlife.models.transcript.TranscriptHtml')
    def test_transcript_instance_from_html(self, mock_transcript_html, mock_instance):
        res = TranscriptInstance.from_html('some-html')
        mock_transcript_html.assert_called_once_with('some-html')
        mock_transcript_html().to_json.assert_called_once()
        mock_instance.assert_called_once_with(body_json=mock_transcript_html().to_json())
        self.assertEqual(mock_instance(), res)


if __name__ == '__main__':
    unittest.main()
