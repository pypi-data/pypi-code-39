from .._base import Endpoint
from ...settings import json_lib as json


class AnswerInlineQuery(Endpoint):
    def __init__(self, inline_query_id, results):
        super().__init__()
        self.args['inline_query_id'] = inline_query_id
        self.args['results'] = json.dumps([x.args for x in results])

    def cache_time(self, cache_time):
        self.args['cache_time'] = cache_time
        return self

    def is_personal(self):
        self.args['is_personal'] = True
        return self

    def next_offset(self, next_offset):
        self.args['next_offset'] = next_offset
        return self

    def switch_pm_text(self, switch_pm_text):
        self.args['switch_pm_text'] = switch_pm_text
        return self

    def switch_pm_parameter(self, switch_pm_parameter):
        self.args['switch_pm_parameter'] = switch_pm_parameter
        return self
