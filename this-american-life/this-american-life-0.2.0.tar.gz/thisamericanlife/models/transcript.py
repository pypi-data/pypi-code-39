
from dataclasses import dataclass
from thisamericanlife.models.basemodel import BaseResource
from thisamericanlife.html.transcript import TranscriptHtml


@dataclass
class EpisodeMetadata(object):
    raw_title: str
    title: str = None
    number: int = None

    @staticmethod
    def from_raw(raw_string):
        episode_title, episode_number = None, None
        if raw_string:
            parsed = raw_string.split(':')
            episode_title = parsed[-1].strip()
            try:
                episode_number = int(parsed[0])
            except:
                episode_number = None

        return EpisodeMetadata(raw_string, episode_title, episode_number)


class TranscriptInstance(object):
    
    @staticmethod
    def from_html(html):
        return TranscriptInstance(body_json=TranscriptHtml(html).to_json())

    def __init__(self, body_json=None):
        self.body_json = body_json
        self.episode_metadata = EpisodeMetadata.from_raw(self.body_json['episode_title'])
        self.transcript = self.body_json['transcript']


class Transcripts(BaseResource):
    def __init__(self, client=None):
        super(Transcripts, self).__init__('transcript', client=client)

    def get(self, episode_number):
        return self._get_and_create(TranscriptInstance, episode_number=episode_number)
