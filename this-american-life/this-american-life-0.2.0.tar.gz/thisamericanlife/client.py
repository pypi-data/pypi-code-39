
from thisamericanlife.http import HttpClient
from thisamericanlife.utils import cached_property
import thisamericanlife.models as tal_models


class ThisAmericanLife(object):
    def __init__(self, http_client=None):
        self.http_client = http_client or HttpClient()

    @cached_property
    def transcripts(self):
        return tal_models.transcript.Transcripts(self)

    @cached_property
    def episodes(self):
        return tal_models.episode.Episodes(self)
