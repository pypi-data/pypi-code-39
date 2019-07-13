
from dataclasses import dataclass
from thisamericanlife.models.basemodel import BaseResource
from thisamericanlife.html.episode import EpisodeHtml


class EpisodeInstance(object):
    @staticmethod
    def from_html(html):
        return EpisodeInstance(body_json=EpisodeHtml(html).to_json())

    def __init__(self, body_json=None, episode_number=None, episode_title=None):
        self.body_json = body_json
        self.number = episode_number
        self.title = episode_title
        self.date_on_air = body_json['episode_metadata'].get('date_on_air')
        self.description = body_json['episode_metadata'].get('description')
        self.act_summaries = body_json['act_summaries']


class Episodes(BaseResource):
    def __init__(self, client=None):
        super(Episodes, self).__init__('episode', client=client)

    def get(self, episode_number=None, episode_title=None):
        episode_title = episode_title or self.client.transcripts.get(episode_number).episode_metadata.title

        ep_instance = self._get_and_create(EpisodeInstance, episode_number=episode_number, episode_title=episode_title)
        ep_instance.number = episode_number
        ep_instance.title = episode_title
        return ep_instance
